with open('input.txt') as f:
    instructions = [(line[0], int(line[2:])) for line in f.readlines()]

# Part 1
head_x, head_y = 0, 0
tail_x, tail_y = 0, 0

visited = set()

for direction, distance in instructions:
    for i in range(distance):
        if direction == 'U':
            head_y += 1
        elif direction == 'D':
            head_y -= 1
        elif direction == 'R':
            head_x += 1
        elif direction == 'L':
            head_x -= 1

        dx, dy = head_x - tail_x, head_y - tail_y

        if dx == 1 and dy in (-2, 2):
            tail_x += 1
        elif dx == -1 and dy in (-2, 2):
            tail_x -= 1

        if dy == 1 and dx in (-2, 2):
            tail_y += 1
        elif dy == -1 and dx in (-2, 2):
            tail_y -= 1

        if dx == 2:
            tail_x += 1
        elif dx == -2:
            tail_x -= 1
        
        if dy == 2:
            tail_y += 1
        elif dy == -2:
            tail_y -= 1


        visited.add((tail_x, tail_y))

        # print(f'({head_x}, {head_y}), ({tail_x}, {tail_y})')

print(len(visited))
