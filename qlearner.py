from util import *
import random

learning_rate = 0.1


class QSApairs():
    def __init__(self, score, dice):
        self.prior_reward = score
        self.prior_dice = dice
        # TODO: share same legal_moves dict if they have the exact same
        #  set of legal moves
        self.legal_moves = {tuple(action): 0 for action in legal_moves(self.prior_dice)}

    def learn(self, action, reward, discount, next_reward):
        # TODO: improve handling of next state/action pair?
        a = tuple(sorted(action))
        self.legal_moves[a] += learning_rate * (
                reward + discount * next_reward - self.legal_moves[a])

    def get_moves(self):
        return self.legal_moves.keys()

    def get_random_move(self):
        r = random.sample(self.legal_moves.keys(), 1)[0]
        return r

    def get_opt_move(self):
        opt = []
        opt_reward = -1
        for k, v in self.legal_moves.items():
            if v > opt_reward:
                opt_reward = v
                opt = list(k)
        return opt

    def get_epsilon_greedy(self, epsilon=0):
        if random.random() < epsilon:
            return self.get_random_move()
        else:
            return self.get_opt_move()

    def __repr__(self):
        return f"<QSApairs: {self.legal_moves}>"


class Qdict(dict):
    discount = 0.9

    def __missing__(self, dice_key):
        score = min(dice_key[0], 350)
        dice = sorted(list(dice_key)[1:])
        key = tuple([score, *dice])
        ret = self[key] = QSApairs(score, dice)
        return ret

    def learn(self, prior_reward, prior_dice, action, reward, discount, next_reward):
        return self[keyify(prior_reward, prior_dice)].learn(action, reward, discount, next_reward)

    def strategy_epsilon_greedy(self, prev_score, dice):
        return self[keyify(prev_score, dice)].get_epsilon_greedy()

    def strategy_opt(self, prev_score, dice):
        return self[keyify(prev_score, dice)].get_opt_move()

    def strategy_random(self, prev_score, dice):
        return self[keyify(prev_score, dice)].get_random_move()

    def print_best(self):
        print("Optimal choices:")
        for k, v in sorted(self.items(), key=lambda t: (t[1].prior_dice, t[0])):
            o = v.get_opt_move()
            print(f"   {k}: {o}")
        print(f"(table size = {len(self)})")


def keyify(score, dice):
    return tuple([min(score, 350), *sorted(dice)])
