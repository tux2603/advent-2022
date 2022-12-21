from pprint import pprint

# read in the grid of number from the input file
trees = []
is_visible = []
with open("input.txt") as f:
    for line in f.readlines():
        trees.append([int(i) for i in line.strip()])
        is_visible.append([0 for _ in line.strip()])

# Check visibility from the top
for col_idx in range(len(trees)):
    for depth in range(len(trees[col_idx])):
        # If the tree is on the edge, it is visible
        if depth == 0:
            is_visible[col_idx][depth] = 1
            continue

        # Get a list of all trees from the edge until this depth
        trees_in_path = [trees[col_idx][i] for i in range(depth)]

        # If this tree is taller than the tallest tree in the path, it is visible
        if trees[col_idx][depth] > max(trees_in_path):
            is_visible[col_idx][depth] = 1

# Check visibility from the bottom
for col_idx in range(len(trees)):
    for depth in range(len(trees[col_idx])):
        # If the tree is on the edge, it is visible
        if depth == 0:
            is_visible[col_idx][len(trees[col_idx]) - (depth + 1)] = 1
            continue

        # Get a list of all trees from the edge until this depth
        trees_in_path = [trees[col_idx][len(trees[col_idx]) - (i + 1)] for i in range(depth)]

        # If this tree is taller than the tallest tree in the path, it is visible
        if trees[col_idx][len(trees[col_idx]) - (depth + 1)] > max(trees_in_path):
            is_visible[col_idx][len(trees[col_idx]) - (depth + 1)] = 1

# Check visibility from the left
for row_idx in range(len(trees[0])):
    for depth in range(len(trees)):
        # If the tree is on the edge, it is visible
        if depth == 0:
            is_visible[depth][row_idx] = 1
            continue

        # Get a list of all trees from the edge until this depth
        trees_in_path = [trees[i][row_idx] for i in range(depth)]

        # If this tree is taller than the tallest tree in the path, it is visible
        if trees[depth][row_idx] > max(trees_in_path):
            is_visible[depth][row_idx] = 1


# Check visibility from the right
for row_idx in range(len(trees[0])):
    for depth in range(len(trees)):
        # If the tree is on the edge, it is visible
        if depth == 0:
            is_visible[len(trees) - (depth + 1)][row_idx] = 1
            continue
    
        # Get a list of all trees from the edge until this depth
        trees_in_path = [trees[len(trees) - (i + 1)][row_idx] for i in range(depth)]

        # If this tree is taller than the tallest tree in the path, it is visible
        if trees[len(trees) - (depth + 1)][row_idx] > max(trees_in_path):
            is_visible[len(trees) - (depth + 1)][row_idx] = 1

            
print (sum([sum(row) for row in is_visible]))

for y, row in enumerate(trees):
    for x, tree in enumerate(row):
        if is_visible[y][x] == 1:
            print (f'\033[1;31m{tree}\033[0m', end=' ')
        else:
            print (tree, end=' ')
    print ()