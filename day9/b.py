with open('input.txt') as f:
    instructions = [(line[0], int(line[2:])) for line in f.readlines()]


rope = [[0, 0] for _ in range(10)]

visited = set()

for direction, distance in instructions:
    for i in range(distance):
        if direction == 'U':
            rope[0][1] += 1
        elif direction == 'D':
            rope[0][1] -= 1
        elif direction == 'R':
            rope[0][0] += 1
        elif direction == 'L':
            rope[0][0] -= 1

        # move all the rest of the rope bits
        for i in range(1, 10):
            dx, dy = rope[i-1][0] - rope[i][0], rope[i-1][1] - rope[i][1]

            if dx == 1 and dy in (-2, 2):
                rope[i][0] += 1
            elif dx == -1 and dy in (-2, 2):
                rope[i][0] -= 1

            if dy == 1 and dx in (-2, 2):
                rope[i][1] += 1
            elif dy == -1 and dx in (-2, 2):
                rope[i][1] -= 1

            if dx == 2:
                rope[i][0] += 1
            elif dx == -2:
                rope[i][0] -= 1
            
            if dy == 2:
                rope[i][1] += 1
            elif dy == -2:
                rope[i][1] -= 1


        visited.add((rope[9][0], rope[9][1]))

        # print(f'({head_x}, {head_y}), ({rope[i][0]}, {rope[i][1]})')

print(len(visited))
