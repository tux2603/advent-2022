with open('input.txt') as f:
    raw_data = [line.strip() for line in f.readlines()]

reg = 1

# to make things easier on myself I'm going to go back through the data and add a noop instruction before each addx instruction
# this will make the logic for the second half of the addx instruction easier to write
data = []
for instruction in raw_data:
    if instruction.startswith('addx '):
        data.append('noop')
        data.append(instruction)
    else:
        data.append(instruction)

for cycle, instruction in enumerate(data):
    # print(f'cycle {cycle} with reg = {reg} and instruction {instruction}: ', end='')

    if cycle % 40 in range(reg-1, reg+2):
        print('#', end='')
    else:
        print('.', end='')

    if instruction.startswith('addx '):
        reg += int(instruction[5:])

    if cycle in (39, 79, 119, 159, 199, 239):
        print()
    