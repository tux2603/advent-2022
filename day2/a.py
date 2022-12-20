# A and X are rock
# B and Y are paper
# C and Z are scissors
# 1 point for rock, 2 points for paper, 3 points for scissors
# 0 points for losing, 3 points for a tie, 6 points for winning

with open('input.txt') as f:
    score = 0

    for line in f:
        line = line.strip()
        match line:
            # handle all the losing cases
            case 'A Z' | 'B X' | 'C Y':
                score += 0
            # handle all the tie cases
            case 'A X' | 'B Y' | 'C Z':
                score += 3
            # handle all the winning cases
            case 'A Y' | 'B Z' | 'C X':
                score += 6

        match line[-1]:
            case 'X':
                score += 1
            case 'Y':
                score += 2
            case 'Z':
                score += 3

    print(score)
            

