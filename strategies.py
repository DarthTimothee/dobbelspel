from util import remove_times


def manual(prev_score, dice):
    print(f"Choose from following dice: {dice}")
    return list(map(int, input().split()))


def choose_all(prev_score, dice):
    """
    Chooses all possible dice, in an optimal fashion

    :param prev_score:
    :param dice:
    :return:
    """
    chosen_dice = []
    for a in [2, 3, 4, 6]:
        if dice.count(a) == 6:
            chosen_dice.extend([a] * 6)
        if dice.count(a) >= 3:
            chosen_dice.extend([a] * 3)
    for die in dice:
        if die == 1 or die == 5:
            chosen_dice.append(die)
    return chosen_dice


def choose_best(prev_score, dice):
    """
    Only choose the die that will give the highest score
    (or three dice if they're the same)

    :param prev_score:
    :param dice:
    :return:
    """
    chosen_dice = []

    # If we have six the same dice, choose those
    for a in [6, 5, 4, 3, 2, 1]:
        if dice.count(a) == 6:
            chosen_dice.extend([a] * 6)
            return chosen_dice

    # If there is a die we have at least three of, choose three of those
    for a in [6, 5, 4, 3, 2, 1]:
        if dice.count(a) >= 3:
            chosen_dice.extend([a] * 3)
            return chosen_dice

    # Finally choose a 1, if we have a 1, choose a 5 otherwise
    if 1 in dice:
        chosen_dice = [1]
    elif 5 in dice:
        chosen_dice = [5]

    return chosen_dice


def choose_alt(prev_score, dice):
    """
    choose all dice of which there are three,
    choose all 1s
    choose one 5, only if there's no other option

    :param prev_score:
    :param dice:
    :return:
    """
    chosen_dice = []

    # If we have six the same dice, choose those
    for a in [6, 5, 4, 3, 2, 1]:
        if dice.count(a) == 6:
            return [a] * 6

    # Choose all of which we have three the same
    for a in [6, 5, 4, 3, 2]:
        if dice.count(a) >= 3:
            chosen_dice.extend([a] * 3)
            continue

    # Choose all 1s
    for _ in range(dice.count(1)):
        chosen_dice.append(1)

    # If we haven't chosen anything yet, choose a 5
    if len(chosen_dice) == 0 and 5 in dice:
        chosen_dice = [5]

    return chosen_dice
