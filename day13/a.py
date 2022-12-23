# get the raw lines
lines = [line.strip() for line in open('input.txt').read().splitlines()]

pairs = []

# get blocks of three lines at a time
for i in range(0, len(lines), 3):
    left = eval(lines[i])
    right = eval(lines[i+1])
    pairs.append((left, right))

# Returns -1 if the packets are in the wrong order, 1 if they are in the right order, and 0 if the order is unknown
def compare(left_packet, right_packet):
    # Check to make sure that one of the packets isn't empty.
    # If left is empty first, the inputs are in the right order
    # If right is empty first, the inputs are in the wrong order
    # If both are empty, then the order is unknown and we need to check the rest of the packets
    if not left_packet and right_packet:
        return 1
    if not right_packet and left_packet:
        return -1
    if not left_packet and not right_packet:
        return 0

    # Get the first element of each packet so there's less typing later
    left = left_packet[0]
    right = right_packet[0]

    # If both are integers, then compare them directly
    # If left is less, the inputs are in the right order
    # If right is less, the inputs are in the wrong order
    # If they are equal, then the order is unknown and we need to check the rest of the packets
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return 1
        elif right < left:
            return -1
        
    # If both are lists, then recuresively call compare on the list
    elif isinstance(left, list) and isinstance(right, list):
        result = compare(left, right)
        if result != 0:
            return result

    # If one is a list and the other is an integer, thgen convert the integer to a list and then compare
    elif isinstance(left, int):
        result = compare([left], right)
        if result != 0:
            return result

    elif isinstance(right, int):
        result = compare(left, [right])
        if result != 0:
            return result

    # If we've made it to this point, we need to check the rest of the packets
    slice_left = left_packet[1:]
    slice_right = right_packet[1:]

    while not(result := compare(slice_left, slice_right)) and (slice_left or slice_right):
        slice_left = slice_left[1:]
        slice_right = slice_right[1:]

    return result

# Check each pair of packets
total = 0
for idx, (left, right) in enumerate(pairs):
    result = compare(left, right)
    if result == 1:
        print(f'Pair {idx + 1}: right')
        total += idx + 1
    elif result == -1:
        print(f'Pair {idx + 1}: wrong')
    else:
        print(f'Pair {idx + 1}: idk')

print(total)


