import numpy as np
import matplotlib.pyplot as plt

from qlearner import Qdict
from util import *
import strategies as strat


Q = Qdict()

estimated_next_reward = []
for i in [1, 2, 3, 4, 5, 6]:
    m = np.mean([max_score(roll_dice(i)) for _ in range(10000)])
    estimated_next_reward.append(m)


def simulate(dice, prev_score=0, strategy=strat.choose_all):
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

    chosen_dice = sorted(list(strategy(prev_score, dice)))
    if not is_valid(chosen_dice, dice):
        print(f"ERROR: invalid choice: {chosen_dice} out of {dice}")
        assert False

    score = prev_score + max_score(chosen_dice)
    # TODO: if remaining_dice is empty,
    #  the player can choose whether to continue or not

    remaining_dice = len(dice) - len(chosen_dice)
    next_reward = estimated_next_reward[remaining_dice]

    Q.learn(prev_score, sorted(dice), sorted(chosen_dice), score, discount=0.9, next_reward=next_reward)

    if manual:
        print(f"going to next round, current score: {score}")
    remaining = len(dice) - len(chosen_dice)
    final_score = simulate(roll_dice(remaining), score, strategy)
    return 0 if final_score < 350 else final_score


def test_expectation(N):

    # M = 250
    # groupsize = 250
    # tmp = []
    # train = []
    # print(f"Training Q table...")
    # for i in range(M):
    #     if i % 10000 == 0 and i > 0:
    #         print(i)
    #     if i % groupsize == 0 and i > 0:
    #         train.append(np.mean(tmp))
    #         tmp = []
    #
    #     dice = roll_dice(6)
    #     simulate(dice.copy(), strategy=Q.strategy_epsilon_greedy)
    #     r = simulate(dice, strategy=Q.strategy_opt)
    #     tmp.append(r)
    #
    # print(f"Done training!")
    #
    # plt.figure()
    # plt.plot(train, label="average over 50 rounds")
    # plt.legend()
    # plt.show()

    print(f"Evaluating...")
    throws = np.zeros((5, N))
    for i in range(N):
        if i % 10000 == 0 and i > 0:
            print(i)

        dice = roll_dice(6)

        throws[:, i] = np.array([
            simulate(dice, strategy=Q.strategy_opt),
            simulate(dice, strategy=strat.choose_all),
            simulate(dice, strategy=strat.choose_best),
            simulate(dice, strategy=strat.choose_alt),
            simulate(dice, strategy=Q.strategy_random),
        ])

    print(f"n = {N}")
    print("expectations:")
    print(f"Q opt  = {np.mean(throws[0, :])}")
    print(f"Q rand = {np.mean(throws[4, :])}")
    print(f"ALL    = {np.mean(throws[1, :])}")
    print(f"BEST   = {np.mean(throws[2, :])}")
    print(f"ALT    = {np.mean(throws[3, :])}")

    # after 10**6 episodes training
    # Q opt  = 412.28
    # Q rand = 330.065
    # ALL    = 334.07
    # BEST   = 383.395
    # ALT    = 377.615

    # after 10**5 episodes training
    # Q opt  = 404.68
    # Q rand = 324.57
    # ALL    = 344.76
    # BEST   = 370.93
    # ALT    = 371.395

    plt.figure()
    plt.xlim(0, 1000)
    plt.hist(throws[0, :], density=True, bins=150, alpha=0.5, label="Q opt")
    plt.hist(throws[4, :], density=True, bins=150, alpha=0.5, label="Q random")
    plt.hist(throws[1, :], density=True, bins=150, alpha=0.5, label="choose all")
    plt.hist(throws[2, :], density=True, bins=150, alpha=0.5, label="choose some")
    plt.hist(throws[3, :], density=True, bins=150, alpha=0.5, label="choose alt")

    plt.xlabel("reward")
    plt.ylabel("probability density")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    test_expectation(10 ** 5)

    # while True:
    #     print(f"final score: {simulate(roll_dice(6), strategy=strat.manual)}")
    #     print(f"================\n")
