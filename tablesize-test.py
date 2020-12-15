if __name__ == "__main__":

    dice = [1, 2, 3, 4, 5, 6]
    D = []

    for a in dice:
        for b in dice:
            l = [a, b]
            l.sort()
            if l not in D:
                D.append(l)

            for c in dice:
                l = [a, b, c]
                l.sort()
                if l not in D:
                    D.append(l)

                for d in dice:
                    l = [a, b, c, d]
                    l.sort()
                    if l not in D:
                        D.append(l)

                    for e in dice:
                        l = [a, b, c, d, e]
                        l.sort()
                        if l not in D:
                            D.append(l)

                        for f in dice:
                            l = [a, b, c, d, e, f]
                            l.sort()
                            if l not in D:
                                D.append(l)

    print(len(D))
    # Out[1]: 917
