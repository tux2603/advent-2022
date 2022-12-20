with open('input.txt') as f:
    elves = []
    total = 0

    for line in f:
        # if this is an integer, add it to the total
        # otherwise, append the total to the elves list and reset the total
        try:
            total += int(line)
        except ValueError:
            elves.append(total)
            total = 0

    # add the last total to the elves list
    elves.append(total)

print(max(elves))