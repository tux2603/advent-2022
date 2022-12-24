from tqdm import tqdm
from numba import njit
import numpy as np

# Data is in the format "Valve XX has flow rate=##; tunnels lead to valves AA, BB, CC, DD"
valves = {}

with open('input.txt') as f:
    for line in f:
        words = line.split()
        valves[words[1]] = [
            int(words[4][5:-1]),
            (''.join(words[9:])).split(',')
        ]

# Good news, all tunnels are bi-directional

# I think the best way to do this will be to build a distance matrix of all of the valves that have some amount of flow
# Once that is built it should be easier to find the maximum amount of pressure release that we can get by bouncing around the matrix
# Also I'm lazy and slapping AA in here even though it doesn't technically have any flow
valves_with_flow = tuple(['AA', *(name for name, data in valves.items() if data[0] > 0)])

# Build the distance matrix
valve_distances = {name: {name:-1 for name in valves_with_flow} for name in valves_with_flow}

for valve_name in valves_with_flow:

    for other_valve in valves_with_flow:
        if other_valve == valve_name:
            valve_distances[valve_name][other_valve] = 0

        else:
            # Use BFS to find the shortest path between the two valves
            queue = [(valve_name, 0)]
            visited = set()
            while queue:
                current_valve, distance = queue.pop(0)
                if current_valve == other_valve:
                    valve_distances[valve_name][other_valve] = distance
                    break

                visited.add(current_valve)
                for next_valve in valves[current_valve][1]:
                    if next_valve not in visited:
                        queue.append((next_valve, distance+1))

# Will it ever be better to skip a valve? I dunno, let's assume not for now
max_flow = sum(valves[name][0] for name in valves_with_flow)
path = {'AA': 0}


def get_paths(valve_name, flow, path, depth=0):
    # Make a local copy of the path so we don't modify the one passed in
    path = path.copy()

    # If the depth is equal to 26, we are done looking
    if depth == 26:
        return [path]

    # If all the valves are open, we are done looking, but we need to add the pressure released
    if flow == max_flow:
        return [path]

    # If we can open this valve, do so
    if valves[valve_name][0] != 0:
        flow += valves[valve_name][0]
        depth += 1
        path[valve_name] = depth

    paths = []
    for other_valve in valves_with_flow:
        # Don't bother going to this valve again
        if other_valve in path:
            continue

        # Don't go to the valve if it's too far away
        distance = valve_distances[valve_name][other_valve]
        if distance > 26 - depth:
            continue

        paths.extend(get_paths(other_valve, flow, path, depth + distance))

    return paths or [path]

path_dicts = get_paths('AA', 0, path)
print(len(path_dicts))

# Check to make sure all of the valves are in all of the paths. If they aren't, add them with a value of 26
for path in path_dicts:
    for valve_name in valves_with_flow:
        if valve_name not in path:
            path[valve_name] = 26

# Convert the paths to a list of tuples
path_lists = []
for path in path_dicts:
    path_lists.append(np.array([path[name] for name in valves_with_flow], dtype=np.int32))

max_pressure_release = 0

flows = np.array([valves[name][0] for name in valves_with_flow], dtype=np.int32)

# This function takes three tuples of integers
@njit('int32(int32[:], int32[:], int32[:])', cache=True, fastmath=True, nogil=True)
def get_released_pressure(path_a, path_b, flows):
    # Combine the two paths by taking the minimum value for each valve
    released_pressure = 0
    for i in range(len(path_a)):
        released_pressure += flows[i] * (26 - min(path_a[i], path_b[i]))

    return released_pressure

for path_a in tqdm(path_lists):
    for path_b in path_lists:
        pressure_release = get_released_pressure(path_a, path_b, flows)

        if pressure_release > max_pressure_release:
            max_pressure_release = pressure_release

print(max_pressure_release)