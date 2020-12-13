def three_same(dice):
    l = []
    for a in [1, 2, 3, 4, 5, 6]:
        if dice.count(a) >= 3:
            l.append(a)
    return l


def max_score(dice):
    score = 0
    for a in [1, 2, 3, 4, 5, 6]:
        if dice.count(a) >= 3:
            dice.remove(a)
            dice.remove(a)
            dice.remove(a)
            if a == 1:
                score += 1000
            else:
                score += 3 * a
    return score + dice.count(1) * 100 + dice.count(5) * 50
