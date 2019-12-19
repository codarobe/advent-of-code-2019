from collections import Counter


def generate_passwords():
    total = 0
    for a in range(1, 7):
        for b in range(a, 10):
            for c in range(b, 10):
                for d in range(c, 10):
                    for e in range(d, 10):
                        for f in range(e, 10):
                            if a == b or b == c or c == d or d == e or e == f:
                                string = str(a) + str(b) + str(c) + str(d) + str(e) + str(f)
                                counts = Counter(string)
                                fits_criteria = False
                                # print(counts)
                                for i in counts:
                                    if counts[i] == 2:
                                        fits_criteria = True
                                if fits_criteria:
                                    num = int(string)
                                    print(num)
                                    if 156218 <= num <= 652527:
                                        total += 1
                                    elif num > 652527:
                                        return total
    return total


if __name__ == "__main__":
    print(generate_passwords())
