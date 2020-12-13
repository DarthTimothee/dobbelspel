def example(dice):
    """
    Example that shows how to implement a strategy

    :param dice:
    :return:
    """
    chosen_dice = []
    remaining_dice = dice
    return chosen_dice, remaining_dice


def choose_all(dice):
    """
    Chooses all possible dice, in an optimal fashion

    :param dice:
    :return:
    """
    chosen_dice = []
    remaining_dice = []
    for a in [1, 2, 3, 4, 5, 6]:
        if dice.count(a) >= 3:
            chosen_dice.append([a] * 3)
    for die in dice:
        if die == 1 or die == 5:
            chosen_dice.append(die)
        else:
            remaining_dice.append(die)
    return chosen_dice, remaining_dice


def choose_best(dice):
    """
    Only choose the die that will give the highest score
    (or three dice if they're the same)

    :param dice:
    :return:
    """
    chosen_dice = []
    remaining_dice = dice
    for a in [6, 5, 4, 3, 2, 1]:
        if dice.count(a) >= 3:
            chosen_dice.append([a] * 3)
            remaining_dice.remove(a)
            remaining_dice.remove(a)
            remaining_dice.remove(a)
            return chosen_dice, remaining_dice

    if 1 in dice:
        chosen_dice = [1]
        remaining_dice.remove(1)
    elif 5 in dice:
        chosen_dice = [5]
        remaining_dice.remove(5)

    return chosen_dice, remaining_dice


def choose_alt(dice):
    """
    choose all dice of which there are three,
    choose all 1s
    choose one 5, only if there's no other option

    :param dice:
    :return:
    """

    chosen_dice = []
    remaining_dice = dice
    for a in [6, 5, 4, 3, 2, 1]:
        if dice.count(a) >= 3:
            chosen_dice.append([a] * 3)
            remaining_dice.remove(a)
            remaining_dice.remove(a)
            remaining_dice.remove(a)

    if 1 in dice:
        count = remaining_dice.count(1)
        for _ in range(count):
            chosen_dice.append(1)
            remaining_dice.remove(1)

    if len(chosen_dice) == 0 and 5 in dice:
        chosen_dice = [5]
        remaining_dice.remove(5)

    return chosen_dice, remaining_dice
