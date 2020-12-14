import random


def max_score(dice):
    dice = dice.copy()
    score = 0
    if sorted(dice) == [1, 2, 3, 4, 5, 6]:
        return 2000
    for a in [1, 2, 3, 4, 5, 6]:
        if dice.count(a) == 6:
            return 5000
        if dice.count(a) >= 3:
            remove_times(dice, a, 3)
            if a == 1:
                score += 1000
            else:
                score += 100 * a
    return score + dice.count(1) * 100 + dice.count(5) * 50


def roll_dice(n):
    return [random.randint(1, 6) for _ in range(n)]


def remove_times(target, x, n):
    # Remove x from target, repeat n times
    for _ in range(n):
        target.remove(x)
