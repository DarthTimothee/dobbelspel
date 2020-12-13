import random

import numpy as np
import matplotlib.pyplot as plt

from util import three_same, max_score
import strategies as strat


def simulate(n, prev_score=0, strategy=strat.choose_all):
    dice = [random.randint(1, 6) for _ in range(n)]
    # print(f"{dice}, prev={prev_score}")

    remove_three = dice.copy()
    for a in three_same(dice):
        for x in [a]*3:
            remove_three.remove(x)

    remaining = len(remove_three) - remove_three.count(1) - remove_three.count(5)
    score = prev_score + max_score(dice)

    if remaining == 0:
        # print(f"no choice, score = {score}")
        return score + simulate(6, strategy=strategy)
    if remaining == 1:
        # print(f"no choice, score = {score}")
        if score < 350:
            score = 0
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
throws_alt = np.zeros(n)
print(f"n = {n}")
for i in range(n):
    if i % 10000 == 0:
        print(i)
    throws_all[i] = simulate(6, strategy=strat.choose_all)
    throws_best[i] = simulate(6, strategy=strat.choose_best)
    throws_alt[i] = simulate(6, strategy=strat.choose_alt)

print("expectations:")
print(f"ALL  = {np.mean(throws_all)}")
print(f"BEST = {np.mean(throws_best)}")
print(f"ALT  = {np.mean(throws_alt)}")

plt.figure()
plt.xlim(0, 1000)
plt.hist(throws_all, density=True, bins=100, color="b", alpha=0.5, label="choose all")
plt.hist(throws_best, density=True, bins=100, color="r", alpha=0.5, label="choose only best")
plt.hist(throws_alt, density=True, bins=100, color="g", alpha=0.5, label="choose alt")

plt.xlabel("reward")
plt.ylabel("probability density")
plt.legend()
plt.show()
