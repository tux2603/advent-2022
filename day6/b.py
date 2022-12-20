with open('input.txt') as f:
    data = f.readline().strip()

for i in range(len(data)):
    # check the number of unique characters in the four character substring starting at i
    if len(set(data[i:i+14])) == 14:
        print(i+14)
        break
