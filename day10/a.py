with open('input.txt') as f:
    data = [line.strip() for line in f.readlines()]

reg, cycle = 1, 0
total = 0

for instruction in data:
    # noop takes 1 cycle
    # addx takes 2 cycles
    # accumulate the value of the register at the 20th, 60th, 100th, 140th, 180th, and 220th cycles
    if instruction == 'noop':
        cycle += 1

        if cycle in (20, 60, 100, 140, 180, 220):
            total += cycle * reg
            print(f'cycle {cycle} with reg = {reg} after a noop instruction')
    
    elif instruction.startswith('addx '):
        if cycle in (19, 59, 99, 139, 179, 219):
            total += (cycle + 1) * reg
            print(f'cycle {cycle+1} with reg = {reg} in the first half of instruction {instruction}')

        if cycle in (18, 58, 98, 138, 178, 218):
            total += (cycle + 2) * reg
            print(f'cycle {cycle + 2} with reg = {reg} in the second half of instruction {instruction}')

        cycle += 2
        reg += int(instruction[5:])


print(total)
    