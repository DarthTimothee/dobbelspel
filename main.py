import numpy as np
import matplotlib.pyplot as plt

from util import max_score, roll_dice, remove_times
import strategies as strat


def simulate(dice, prev_score=0, strategy=strat.choose_all):
    # print(f"{dice}, prev={prev_score}")

    check = dice.copy()
    for a in [1, 2, 3, 4, 5, 6]:
        if check.count(a) == 6:
            check = []
            break
        if check.count(a) >= 3:
            remove_times(check, a, 3)
        if a == 1 or a == 5:
            for _ in range(check.count(a)):
                check.remove(a)

    remaining = len(check)
    score = prev_score + max_score(dice)

    if remaining == 0:
        score += simulate(roll_dice(6), strategy=strategy)
        return 0 if score < 350 else score
    if remaining == 1:
        return 0 if score < 350 else score
    if remaining == len(dice):
        return 0

    chosen_dice, remaining_dice = strategy(dice)
    assert len(chosen_dice) + len(remaining_dice) == len(dice)
    score = prev_score + max_score(chosen_dice)

    final_score = simulate(roll_dice(len(remaining_dice)), score, strategy)
    return 0 if final_score < 350 else final_score


N = 100000
throws_all = np.zeros(N)
throws_best = np.zeros(N)
throws_alt = np.zeros(N)
print(f"n = {N}")
for i in range(N):
    if i % 10000 == 0:
        print(i)
    throws_all[i] = simulate(roll_dice(6), strategy=strat.choose_all)
    throws_best[i] = simulate(roll_dice(6), strategy=strat.choose_best)
    throws_alt[i] = simulate(roll_dice(6), strategy=strat.choose_alt)

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
