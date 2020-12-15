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


def legal_moves(dice):
    moves = []

    for a in [2, 3, 4, 6]:
        if dice.count(a) == 6:
            moves.append([a] * 6)
        if dice.count(a) >= 3:
            moves.append([a] * 3)

    for a in dice:
        if a in [1, 5]:
            new_moves = moves.copy()
            for move in moves:
                new_move = [a, *move]
                new_move.sort()
                if new_move not in new_moves:
                    new_moves.append(new_move)
            moves = new_moves
            if [a] not in moves:
                moves.append([a])

    if sorted(dice) == [1, 2, 3, 4, 5, 6]:
        moves.append(dice)

    return moves


def roll_dice(n):
    return [random.randint(1, 6) for _ in range(n)]


def remove_times(target, x, n):
    # Remove x from target, repeat n times
    for _ in range(n):
        target.remove(x)


def is_valid(chosen, dice):
    if len(chosen) == 0:
        return False
    if sorted(chosen) == [1, 2, 3, 4, 5, 6]:
        return True
    for a in chosen:
        if chosen.count(a) > dice.count(a):
            return False
        if a not in [1, 5] and chosen.count(a) % 3 != 0:
            return False
    return True
