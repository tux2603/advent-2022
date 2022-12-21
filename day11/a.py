# Input parsing for this would suck. We're hardcoding values

class Monkey:
    def __init__(self, starting_queue, worry_lambda, target_lambda):
        self.queue = starting_queue
        self.worry_lambda = worry_lambda
        self.target_lambda = target_lambda
        self.inspections = 0

    def step(self):
        while self.queue:
            item = self.queue.pop(0)
            item = self.worry_lambda(item) // 3
            target = self.target_lambda(item)
            self.inspections += 1
            yield (target, item)

monkeys = []

# Monkey 0:
#   Starting items: 54, 61, 97, 63, 74
#   Operation: new = old * 7
#   Test: divisible by 17
#     If true: throw to monkey 5
#     If false: throw to monkey 3
monkeys.append(Monkey([54, 61, 97, 63, 74], lambda x: x * 7, lambda x: 5 if x % 17 == 0 else 3))

# Monkey 1:
#   Starting items: 61, 70, 97, 64, 99, 83, 52, 87
#   Operation: new = old + 8
#   Test: divisible by 2
#     If true: throw to monkey 7
#     If false: throw to monkey 6
monkeys.append(Monkey([61, 70, 97, 64, 99, 83, 52, 87], lambda x: x + 8, lambda x: 7 if x % 2 == 0 else 6))

# Monkey 2:
#   Starting items: 60, 67, 80, 65
#   Operation: new = old * 13
#   Test: divisible by 5
#     If true: throw to monkey 1
#     If false: throw to monkey 6
monkeys.append(Monkey([60, 67, 80, 65], lambda x: x * 13, lambda x: 1 if x % 5 == 0 else 6))

# Monkey 3:
#   Starting items: 61, 70, 76, 69, 82, 56
#   Operation: new = old + 7
#   Test: divisible by 3
#     If true: throw to monkey 5
#     If false: throw to monkey 2
monkeys.append(Monkey([61, 70, 76, 69, 82, 56], lambda x: x + 7, lambda x: 5 if x % 3 == 0 else 2))

# Monkey 4:
#   Starting items: 79, 98
#   Operation: new = old + 2
#   Test: divisible by 7
#     If true: throw to monkey 0
#     If false: throw to monkey 3
monkeys.append(Monkey([79, 98], lambda x: x + 2, lambda x: 0 if x % 7 == 0 else 3))

# Monkey 5:
#   Starting items: 72, 79, 55
#   Operation: new = old + 1
#   Test: divisible by 13
#     If true: throw to monkey 2
#     If false: throw to monkey 1
monkeys.append(Monkey([72, 79, 55], lambda x: x + 1, lambda x: 2 if x % 13 == 0 else 1))

# Monkey 6:
#   Starting items: 63
#   Operation: new = old + 4
#   Test: divisible by 19
#     If true: throw to monkey 7
#     If false: throw to monkey 4
monkeys.append(Monkey([63], lambda x: x + 4, lambda x: 7 if x % 19 == 0 else 4))

# Monkey 7:
#   Starting items: 72, 51, 93, 63, 80, 86, 81
#   Operation: new = old * old
#   Test: divisible by 11
#     If true: throw to monkey 0
#     If false: throw to monkey 4
monkeys.append(Monkey([72, 51, 93, 63, 80, 86, 81], lambda x: x * x, lambda x: 0 if x % 11 == 0 else 4))


for _ in range(20):
    for i, monkey in enumerate(monkeys):
        # print(f'Monkey {i} has {len(monkey.queue)} items')
        for target, item in monkey.step():
            # print(f'  Monkey {i} threw {item} to monkey {target}')
            monkeys[target].queue.append(item)

inspections = [monkey.inspections for monkey in monkeys]
print(inspections)
inspections.sort()
print(inspections[-1] * inspections[-2])