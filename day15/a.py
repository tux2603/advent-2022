import re
from functools import cache
from tqdm import tqdm

sensors = []
beacons = []

with open('input.txt') as f:
    for line in f:
        data = [int(i) for i in re.findall(r'-?\d+', line)]
        sensors.append((data[0], data[1], 
        abs(data[0] - data[2]) + abs(data[1] - data[3])))
        beacons.append((data[2], data[3]))

def dist(point, sensor):
    return abs(point[0] - sensor[0]) + abs(point[1] - sensor[1])

for idx, sensor in enumerate(sensors):
    print(f'{idx + 1}: {sensor}')

# I'm going to be lazy and just see how far any of the beacons can reach ion the x direction
min_x = min(sensor[0] - sensor[2] for sensor in sensors)
max_x = max(sensor[0] + sensor[2] for sensor in sensors)
y_scan = 2000000

total = 0

print(max_x - min_x)
for x in tqdm(range(min_x, max_x + 1)):
    if (x, y_scan) in beacons:
        continue

    # Get the distance to this point from all of the sensors
    if any(dist((x, y_scan, 0), sensor) <= sensor[2] for sensor in sensors):
        total += 1

print(total)
