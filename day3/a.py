# priorities for a-z are 1-26 and priorities for A-Z are 27-52
def get_priority(c):
    if c.islower():
        return ord(c) - 96
    else:
        return ord(c) - 38

with open('input.txt') as f:
    total = sum(get_priority((set(i[:len(i) // 2]) & set(i[len(i) // 2:])).pop()) for i in f)
    print(total)