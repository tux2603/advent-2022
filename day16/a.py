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
valves_with_flow = ['AA', *(name for name, data in valves.items() if data[0] > 0)]

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


def get_max_pressure_release(valve_name, flow, visited=(), pressure_released=0, depth=0):
    print(f'{" " * depth}- Arrived at valve {valve_name} at minute {depth}. Current flow is {flow} and {pressure_released} pressure has been released')
    # If the depth is equal to 30, we are done looking
    if depth == 30:
        return pressure_released

    # If all the valves are open, we are done looking, but we need to add the pressure released
    if flow == max_flow:
        print(f'{" " * depth}  All valves have been opened with {30 - depth} minutes left')
        return pressure_released + flow * (30 - depth)
    
    # If we can open this valve, do so
    if valves[valve_name][0] != 0:
        print(f'{" " * depth}  Opening valve {valve_name}. This takes one minute and increases flow by {valves[valve_name][0]} to {flow + valves[valve_name][0]}')
        pressure_released += flow
        flow += valves[valve_name][0]
        depth += 1

    visited += (valve_name,)

    options = []
    for other_valve in valves_with_flow:
        # Don't bother going to this valve again
        if other_valve in visited:
            continue

        # Don't go to the valve if it's too far away
        distance = valve_distances[valve_name][other_valve]
        if distance > 30 - depth:
            continue

        print(f'{" " * depth} Going to valve {other_valve} which is {distance} minutes away')

        options.append(get_max_pressure_release(other_valve, flow, visited, pressure_released + flow * distance, depth + distance))

    # If there were no options, just sit here
    if not options:
        print(f'{" " * depth} No options, sitting here for {30 - depth} minutes')
        return pressure_released + flow * (30 - depth)

    return max(options)

print(get_max_pressure_release('AA', 0, ('AA',)))
