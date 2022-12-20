# A is rock
# B is paper
# C is scissors
# X means you need to lose
# Y means you need to tie
# Z means you need to win
# 1 point for rock, 2 points for paper, 3 points for scissors
# 0 points for losing, 3 points for a tie, 6 points for winning

with open('input.txt') as f:
    score = 0

    for line in f:
        line = line.strip()
        match line:
            # handle all the rock cases
            case 'A Y' | 'B X' | 'C Z':
                score += 1
            # handle all the paper cases
            case 'A Z' | 'B Y' | 'C X':
                score += 2
            # handle all the scissors cases
            case 'A X' | 'B Z' | 'C Y':
                score += 3

        match line[-1]:
            case 'X':
                score += 0
            case 'Y':
                score += 3
            case 'Z':
                score += 6

    print(score)
            

