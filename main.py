import numpy as np
import matplotlib.pyplot as plt

from util import max_score, roll_dice, remove_times, is_valid
import strategies as strat


def simulate(dice, prev_score=0, strategy=strat.choose_all):
    # print(f"{dice}, prev={prev_score}")
    manual = strategy == strat.manual

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

    # TODO: according to wikipedia (https://nl.wikipedia.org/wiki/5000en),
    #  you get a bit more own choices here
    if remaining == 0:
        if manual: print(f"you rolled {dice}, starting new round! current score: {score}")
        score += simulate(roll_dice(6), strategy=strategy)
        return 0 if score < 350 else score
    if remaining == 1:
        if manual: print(f"you rolled {dice}, finished!")
        return 0 if score < 350 else score
    if remaining == len(dice):
        if manual: print(f"you rolled {dice}, too bad!")
        return 0

    chosen_dice, remaining_dice = strategy(dice)
    if not is_valid(chosen_dice, dice) or \
            len(chosen_dice) + len(remaining_dice) != len(dice):
        print(f"ERROR: invalid choice: {chosen_dice}")
        assert False

    score = prev_score + max_score(chosen_dice)
    # TODO: if remaining_dice is empty,
    #  the player can choose whether to continue or not

    if manual: print(f"going to next round, current score: {score}")
    final_score = simulate(roll_dice(len(remaining_dice)), score, strategy)
    return 0 if final_score < 350 else final_score


def test_expectation(N):
    throws = np.zeros((3, N))

    for i in range(N):
        if i % 10000 == 0:
            print(i)

        dice = roll_dice(6)
        throws[:, i] = np.array([
            simulate(dice, strategy=strat.choose_all),
            simulate(dice, strategy=strat.choose_best),
            simulate(dice, strategy=strat.choose_alt)
        ])

    print(f"n = {N}")
    print("expectations:")
    print(f"ALL  = {np.mean(throws[0, :])}")
    print(f"BEST = {np.mean(throws[1, :])}")
    print(f"ALT  = {np.mean(throws[2, :])}")

    plt.figure()
    plt.xlim(0, 1000)
    plt.hist(throws[0, :], density=True, bins=100, color="b", alpha=0.5, label="choose all")
    plt.hist(throws[1, :], density=True, bins=100, color="r", alpha=0.5, label="choose only best")
    plt.hist(throws[2, :], density=True, bins=100, color="g", alpha=0.5, label="choose alt")

    plt.xlabel("reward")
    plt.ylabel("probability density")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    test_expectation(10**5)

    while True:
        print(f"final score: {simulate(roll_dice(6), strategy=strat.manual)}")
        print(f"================\n")

