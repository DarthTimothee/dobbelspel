from util import remove_times


def manual(dice):
    print(f"Choose from following dice: {dice}")
    chosen_dice = list(map(int, input().split()))
    remaining_dice = dice.copy()
    for a in chosen_dice:
        remaining_dice.remove(a)
    return chosen_dice, remaining_dice

def choose_all(dice):
    """
    Chooses all possible dice, in an optimal fashion

    :param dice:
    :return:
    """
    chosen_dice = []
    remaining_dice = dice.copy()
    for a in [1, 2, 3, 4, 5, 6]:
        if remaining_dice.count(a) == 6:
            chosen_dice.extend([a] * 6)
            remove_times(remaining_dice, a, 6)
        if remaining_dice.count(a) >= 3:
            chosen_dice.extend([a] * 3)
            remove_times(remaining_dice, a, 3)
    for die in remaining_dice:
        if die == 1 or die == 5:
            chosen_dice.append(die)
            remaining_dice.remove(die)
    return chosen_dice, remaining_dice


def choose_best(dice):
    """
    Only choose the die that will give the highest score
    (or three dice if they're the same)

    :param dice:
    :return:
    """
    chosen_dice = []
    remaining_dice = dice.copy()

    # If we have six the same dice, choose those
    for a in [6, 5, 4, 3, 2, 1]:
        if remaining_dice.count(a) == 6:
            chosen_dice.extend([a] * 6)
            remove_times(remaining_dice, a, 6)
            return chosen_dice, remaining_dice

    # If there is a die we have at least three of, choose three of those
    for a in [6, 5, 4, 3, 2, 1]:
        if remaining_dice.count(a) >= 3:
            chosen_dice.extend([a] * 3)
            remove_times(remaining_dice, a, 3)
            return chosen_dice, remaining_dice

    # Finally choose a 1, if we have a 1, choose a 5 otherwise
    if 1 in remaining_dice:
        chosen_dice = [1]
        remaining_dice.remove(1)
    elif 5 in remaining_dice:
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
    remaining_dice = dice.copy()

    # If we have six the same dice, choose those
    for a in [6, 5, 4, 3, 2, 1]:
        if remaining_dice.count(a) == 6:
            chosen_dice.extend([a] * 6)
            remove_times(remaining_dice, a, 6)
            return chosen_dice, remaining_dice

    # Choose all of which we have three the same
    for a in [6, 5, 4, 3, 2, 1]:
        if dice.count(a) >= 3:
            chosen_dice.extend([a] * 3)
            remove_times(remaining_dice, a, 3)

    # Choose all 1s
    for _ in range(remaining_dice.count(1)):
        chosen_dice.append(1)
        remaining_dice.remove(1)

    # If we haven't chosen anything yet, choose a 5
    if len(chosen_dice) == 0 and 5 in remaining_dice:
        chosen_dice = [5]
        remaining_dice.remove(5)

    return chosen_dice, remaining_dice
