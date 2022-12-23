from pprint import pprint

elevations = []

def char_to_elevation(char):
    if char == 'S':
        return 0
    if char == 'E':
        return 25
    return ord(char) - ord('a')

start_row, start_col = 0, 0
end_row, end_col = 0, 0

with open("input.txt") as f:
    for row, line in enumerate(f):
        elevations.append([char_to_elevation(char) for char in line.strip()])

        if 'S' in line:
            start_row, start_col = row, line.index('S')

        if 'E' in line:
            end_row, end_col = row, line.index('E')

frontier = [(start_row, start_col, 0)]
visited = set()
visited.add((start_row, start_col))
path_data = [[None for _ in range(len(elevations[0]))] for _ in range(len(elevations))]

while frontier:
    row, col, distance = frontier.pop(0)

    if row == end_row and col == end_col:
        print(distance)
        break

    for new_row, new_col in ((row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)):
        if new_row < 0 or new_row >= len(elevations) or new_col < 0 or new_col >= len(elevations[0]):
            continue
        if (new_row, new_col) not in visited and elevations[new_row][new_col] <= elevations[row][col] + 1:
            frontier.append((new_row, new_col, distance + 1))
            visited.add((new_row, new_col))

    frontier.sort(key=lambda x: x[2])

    # Send the ansii code to clear the screen and move the cursor to the top left
    # print('\033[1;1H', end='', flush=True)

    # for row in range(len(elevations)):
    #     for col in range(len(elevations[row])):
    #         if (row, col) in visited:
    #             print('X', end='')
    #         elif (row, col) == (end_row, end_col):
    #             print('E', end='')
    #         else:
    #             print('.', end='')
    #     print()
    # print(len(frontier))
