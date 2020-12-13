import random

import numpy as np
import matplotlib.pyplot as plt


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


def strat_choose_all(dice):
    chosen_dice = []
    remaining_dice = []
    for a in [1, 2, 3, 4, 5, 6]:
        if dice.count(a) >= 3:
            chosen_dice.append([a]*3)
    for die in dice:
        if die == 1 or die == 5:
            chosen_dice.append(die)
        else:
            remaining_dice.append(die)
    return chosen_dice, remaining_dice


def strat_choose_best(dice):
    chosen_dice = []
    remaining_dice = dice
    for a in [6, 5, 4, 3, 2, 1]:
        if dice.count(a) >= 3:
            chosen_dice.append([a]*3)
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


def strat_choose_all_thr_ones(dice):
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
            chosen_dice.append([a]*3)
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


def simulate(n, prev_score=0, strategy=strat_choose_all):
    dice = [random.randint(1, 6) for _ in range(n)]
    # print(f"{dice}, prev={prev_score}")

    s = three_same(dice)
    remove_three = dice
    for a in s:
        remove_three.remove(a)
        remove_three.remove(a)
        remove_three.remove(a)

    remaining = len(remove_three) - remove_three.count(1) - remove_three.count(5)
    score = prev_score + max_score(dice)
    if remaining == 0:
        # print(f"no choice, score = {score}")
        return score + simulate(6, strategy=strategy)
    if remaining == 1:
        # print(f"no choice, score = {score}")
        return score
    if remaining == n:
        # print(f"no luck, score = 0")
        return 0

    chosen_dice, remaining_dice = strategy(dice)
    score = prev_score + max_score(chosen_dice)
    # print(f"yes choice, score = {score}, chose: {chosen_dice}")
    return simulate(len(remaining_dice), score, strategy)


n = 100000
throws_all = np.zeros(n)
throws_best = np.zeros(n)
throws_thr = np.zeros(n)
print(f"n = {n}")
for i in range(n):
    if i % 10000 == 0:
        print(i)
    throws_all[i] = simulate(6, strategy=strat_choose_all)
    throws_best[i] = simulate(6, strategy=strat_choose_best)
    throws_thr[i] = simulate(6, strategy=strat_choose_all_thr_ones)

print(f"ALL expectation = {np.mean(throws_all)}")
print(f"BEST expectation = {np.mean(throws_best)}")
print(f"SOME expectation = {np.mean(throws_thr)}")

plt.figure()
plt.xlim(0, 1000)
plt.hist(throws_all, density=True, bins=50, color="b", alpha=0.5, label="choose all")
plt.hist(throws_best, density=True, bins=50, color="r", alpha=0.5, label="choose only best")
plt.hist(throws_thr, density=True, bins=50, color="g", alpha=0.5, label="choose alt")

plt.xlabel("reward")
plt.ylabel("probability density")
plt.legend()
plt.show()
