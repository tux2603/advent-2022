import re

# The data is a bit weird tp parse in this one, so we're just going to take the easy way out and do it in two steps
rows = []
moves = []
done_with_rows = False
moves_started = False

with open('input.txt') as f:
    for line in f:
        if not done_with_rows:
            line = line[1::4]
            
            if not line.isnumeric():
                rows.append(line)
            else:
                done_with_rows = True
        
        elif done_with_rows and not moves_started:
            if not line.strip():
                moves_started = True

        elif moves_started:
            moves.append(line.strip())

rows.reverse()

stacks = [[] for _ in rows[0]]

for row in rows:
    for i, c in enumerate(row):
        if c == ' ':
            continue
        stacks[i].append(c)

for move in moves:
    # Get the numerical data from the move string
    count, from_stack, to_stack = [int(x) for x in re.findall(r'\d+', move)]
    from_stack -= 1
    to_stack -= 1

    for _ in range(count):
        stacks[to_stack].append(stacks[from_stack].pop())

print(''.join([stack[-1] for stack in stacks]))