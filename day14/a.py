import re

# Input parsing will be in two steps. First, find the minimum and maximum x and y coordinates present in the input
# Then, create a 2D array of the correct size and fill it with the lines specified in the input
lines = [line.strip() for line in open('input.txt').readlines()]


x_coords = [500]
y_coords = [0]

# Extract all the numbers from the input
for line in lines:
    x_coords.extend([int(x[:-1]) for x in re.findall(r'\d+,', line)])
    y_coords.extend([int(y[1:]) for y in re.findall(r',\d+', line)])

min_x, max_x = min(x_coords), max(x_coords)
min_y, max_y = min(y_coords), max(y_coords)

# Create a 2D array of the correct size
grid = [['.' for _ in range(max_x - min_x + 1)] for _ in range(max_y - min_y + 1)]

for line in lines:
    # extract each pair of coordinates
    coords = [eval(f'({match})') for match in re.findall(r'\d+,\d+', line)]
    
    # Add a little # character to the grid at each point along the specified line
    for start, stop in zip(coords[:-1], coords[1:]):
        if start[0] == stop[0]:
            for y in range(min(start[1], stop[1]), max(start[1], stop[1]) + 1):
                grid[y - min_y][start[0] - min_x] = '#'
        else:
            for x in range(min(start[0], stop[0]), max(start[0], stop[0]) + 1):
                grid[start[1] - min_y][x - min_x] = '#'

# for row in grid:
#     print(''.join(row))

sand_x, sand_y = 500 - min_x, 0 - min_y

while sand_x >= 0 and sand_x < len(grid[0]) and sand_y >= 0 and sand_y < len(grid) - 1:
    # Get the string of the three tiles below the sand
    next_row = ['.', *grid[sand_y + 1], '.'][sand_x:sand_x + 3]
    
    match next_row:
        case _, '.', _:
            # The sand falls down
            sand_y += 1
        case '.', '#' | 'O', _:
            # The sand falls down and to the left
            sand_y += 1
            sand_x -= 1
        case '#' | 'O', '#' | 'O', '.':
            # The sand falls down and to the right
            sand_y += 1
            sand_x += 1
        case '#' | 'O', '#' | 'O', '#' | 'O':
            # The sand has reached the bottom of the grid
            grid[sand_y][sand_x] = 'O'
            sand_x, sand_y = 500 - min_x, 0 - min_y

# Find the amount of sand in the grid
print(sum(row.count('O') for row in grid))