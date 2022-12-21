from pprint import pprint

# read in the grid of number from the input file
trees = []
with open("input.txt") as f:
    for line in f.readlines():
        trees.append([int(i) for i in line.strip()])

max_score = 0

for y, row in enumerate(trees):
    for x, tree in enumerate(row):
        view_left, view_right, view_up, view_down = -1, -1, -1, -1
        depth = 0

        while view_left == -1 or view_right == -1 or view_up == -1 or view_down == -1:
            # Check to see if the tree depth trees away is the same height or taller
            # If it is, then it is visible, and we can stop checking in that direction
            if view_left == -1:
                if x - depth <= 0:
                    view_left = depth
                elif depth != 0 and trees[y][x - depth] >= tree:
                    view_left = depth

            if view_right == -1:
                if x + depth >= len(row) - 1:
                    view_right = depth
                elif depth != 0 and trees[y][x + depth] >= tree:
                    view_right = depth

            if view_up == -1:
                if y - depth <= 0:
                    view_up = depth
                elif depth != 0 and trees[y - depth][x] >= tree:
                    view_up = depth

            if view_down == -1:
                if y + depth >= len(trees) - 1:
                    view_down = depth
                elif depth != 0 and trees[y + depth][x] >= tree:
                    view_down = depth

            depth += 1

        print(f'({x}, {y}): {view_left}, {view_right}, {view_up}, {view_down}')
        if view_left * view_right * view_up * view_down > max_score:
            max_score = view_left * view_right * view_up * view_down


print(max_score)