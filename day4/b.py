with open('input.txt') as f:
    count = 0
    for line in f:
        elf1_data, elf2_data = line.strip().split(',')
        elf1 = set(range(int(elf1_data.split('-')[0]), int(elf1_data.split('-')[1]) + 1))
        elf2 = set(range(int(elf2_data.split('-')[0]), int(elf2_data.split('-')[1]) + 1))

        if len(elf1 | elf2) < len(elf1) + len(elf2):
            count += 1

    print(count)