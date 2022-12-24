#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <time.h>

#define DEBUG
// #define TEST_DATA

#ifdef TEST_DATA
#    define NUM_SENSORS 14
#    define INPUT_FILE "cleaned_input_test.txt"
#    define MAX_SEARCH 20
#else
#    define NUM_SENSORS 38
#    define INPUT_FILE "cleaned_input.txt"
#    define MAX_SEARCH 4000000
#endif

// Found using the cuda occupancy calculator
#define THREADS_PER_BLOCK 768
#define BLOCKS_PER_SM 2
#define ITERATIONS_PER_KERNEL 40

#define MIN(a, b) (((a) < (b)) ? (a) : (b))

typedef struct {
    int32_t x;
    int32_t y;
    int32_t range;
} sensor_t;

__global__ void search_kernel(sensor_t *sensors, int32_t *out_x, int32_t *out_y, bool *found, int start_y, int end_y) {
    __shared__ sensor_t shared_sensors[NUM_SENSORS];

    // Copy the sensor data into shared memory since we're going to be using it so much
    if (threadIdx.x == 0) {
        for (int i = 0; i < NUM_SENSORS; i++) {
            shared_sensors[i] = sensors[i];
        }
    }

    // Resync all the threads now that the data is copied
    __syncthreads();

    for (int32_t y = start_y + blockIdx.x; y < end_y; y += gridDim.x) {
        for (int32_t x = threadIdx.x; x <= MAX_SEARCH; x += blockDim.x) {
            bool in_range = false;

            for (uint8_t i = 0; i < NUM_SENSORS; i++) {
                int32_t distance = abs(shared_sensors[i].x - x) + abs(shared_sensors[i].y - y);

                in_range |= (distance <= shared_sensors[i].range);
            }

            if (!in_range) {
                *out_x = x;
                *out_y = y;
                *found = true;
            }
        }
    }
}

/**
 * @brief Reads the raw sensor data from a precleaned input file
 * 
 * @param fp A file pointer already opened and pointing at the input file
 * @param sensors A pointer to a shared array that will hold the sensor data
 */
void parse_sensor_data(FILE *fp, sensor_t *sensors) {
    char *buffer = NULL;
    size_t length;

    // Parse the sensor data from the file
    for (int i = 0; i < NUM_SENSORS; i++) {
        // Read a line from the file
        if (getline(&buffer, &length, fp) == -1) {
            printf("Error reading file\n");
            return;
        }

        else {
            int32_t beacon_x, beacon_y;

            // Parse the sensor data
            sscanf(buffer, "%d %d %d %d", &sensors[i].x, &sensors[i].y, &beacon_x, &beacon_y);

            // Calculate the range of the sensor
            sensors[i].range = abs(beacon_x - sensors[i].x) + abs(beacon_y - sensors[i].y);
        }
    }

    // Free the buffer
    if (buffer) {
        free(buffer);
    }
}


int main(int argc, char **argv) {

    // Create two 32 bit unsigned integers to copy back beacon location into, and a boolean flag to indicate if the beacon was found
    int32_t *x, *y;
    bool *found;
    cudaMallocManaged(&x, sizeof(int32_t));
    cudaMallocManaged(&y, sizeof(int32_t));
    cudaMallocManaged(&found, sizeof(bool));
    *x = 0;
    *y = 0;
    *found = false;

    // Create a shared array to store the sensor data
    sensor_t *sensors;
    cudaMallocManaged(&sensors, NUM_SENSORS * sizeof(sensor_t));


    // Open the file "cleaned_input.txt" for parsing
    FILE *fp = fopen(INPUT_FILE, "r");

    // Parse the sensor data from the file
    parse_sensor_data(fp, sensors);

    // Close the file
    fclose(fp);

#ifdef DEBUG
    // Print out all of the sensors for debugging
    for (int i = 0; i < NUM_SENSORS; i++) {
        printf("Sensor %d is at (%d, %d) with range of %d\n", i + 1, sensors[i].x, sensors[i].y, sensors[i].range);
    }
#endif

    // Get some information on the cuda device that this is running on
    int device;
    cudaGetDevice(&device);
    cudaDeviceProp prop;
    cudaGetDeviceProperties(&prop, device);

    // I'm going to be lazy and assume a device with compute capability of 8.6 when doing the math to figure out
    //  how many threads to use per block and how many blocks to use per grid.
    int major_version = prop.major;
    int minor_version = prop.minor;
    int sm_count = prop.multiProcessorCount;
    int max_concurrent_blocks = sm_count * BLOCKS_PER_SM;

    if (major_version != 8 || minor_version != 6) {
        printf("\033[1;31mWARNING!\033[0m This program was optimized for cuda devices with compute capability 8.6, but this device has compute capability %d.%d\n", major_version, minor_version);
        printf("         The program will probably still run, it just might be a bit slower than it would be otherwise because of reduced occupancy\n");
    }

#ifdef DEBUG
    printf("There are %d SMs on this device, this will allow %d thread blocks to run simultaneously\n", sm_count, max_concurrent_blocks);
#endif

#ifdef TEST_DATA
    search_kernel<<<MAX_SEARCH, MAX_SEARCH>>>(sensors, x, y, found, 0, MAX_SEARCH);
    cudaDeviceSynchronize();
#else
#    ifdef DEBUG
    clock_t start = clock();
#    endif

    // Search for the beacon
    for (int i = 0; i <= MAX_SEARCH; i += max_concurrent_blocks * ITERATIONS_PER_KERNEL) {
        int32_t end_y = MIN(MAX_SEARCH, i + max_concurrent_blocks * ITERATIONS_PER_KERNEL);
        search_kernel<<<max_concurrent_blocks, THREADS_PER_BLOCK>>>(sensors, x, y, found, i, end_y);

        // Wait for the kernel to finish
        cudaDeviceSynchronize();

#    ifdef DEBUG
        clock_t elapsed = clock();
        printf("Searching for beacon... %d / %d lines searched (%d%%)", i, MAX_SEARCH, (int)((float)i / (float)MAX_SEARCH * 100.0f));
        float seconds_elapsed = (float)(elapsed - start) / (float)CLOCKS_PER_SEC;
        float estimated_total_time = seconds_elapsed * ((float)MAX_SEARCH / (float)i);
        float estimated_time_remaining = estimated_total_time - seconds_elapsed;
        printf(" (%.2f seconds elapsed, ETA %.2f seconds)\n", seconds_elapsed, estimated_time_remaining);
#    endif

        // Check if the beacon was found
        if (*found) {
            break;
        }
    }
#endif

    // Print out the beacon location
    if (*found) {
        printf("Beacon found at (%d, %d)\n", *x, *y);
        uint64_t frequency = (uint64_t)*x * 4000000 + (uint64_t)*y;
        printf("Frequency is %lu\n", frequency);
    }

    else {
        printf("Beacon not found\n");
    }
    return 0;
}