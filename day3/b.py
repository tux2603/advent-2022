from functools import reduce

# priorities for a-z are 1-26 and priorities for A-Z are 27-52
def get_priority(c):
    if c.islower():
        return ord(c) - 96
    else:
        return ord(c) - 38

with open('input.txt') as f:
    # Iterate through the file three lines at a time
    group = []
    total = 0

    for line in f:
        group.append(line.strip())

        # If we've reached the end of the group, add to the total
        if len(group) == 3:
            total += get_priority(reduce(lambda x, y: x & y, map(set, group)).pop())
            group = []

    print(total)