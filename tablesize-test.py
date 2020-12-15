from collections import defaultdict
from pprint import pprint

if __name__ == "__main__":

    dice = [1, 2, 3, 4, 5, 6]
    D = defaultdict(lambda: 0)

    for a in dice:
        for b in dice:
            D[tuple(sorted([a, b]))] += 1

            for c in dice:
                D[tuple(sorted([a, b, c]))] += 1

                for d in dice:
                    D[tuple(sorted([a, b, c, d]))] += 1

                    for e in dice:
                        D[tuple(sorted([a, b, c, d, e]))] += 1

                        for f in dice:
                            D[tuple(sorted([a, b, c, d, e, f]))] += 1

    pprint(dict(D))
    print(len(D))
    # Out[1]: 917
