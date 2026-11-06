"""Count comparisons at growing n and fit the growth exponent from the log-log slope.

Illustrates The Pragmatic Programmer, Topic 39, Algorithm Speed (pp. 343-351, Tips 63-64):
estimate the order, then test the estimate by running at several sizes. Counting operations
instead of timing removes noise. The algorithms and sizes are the vault's.
"""
import math
import random


class Counter:
    def __init__(self):
        self.n = 0

    def lt(self, a, b):
        self.n += 1
        return a < b


def linear_search(xs, target, c):
    for x in xs:
        c.n += 1
        if x == target:
            return True
    return False


def binary_search(xs, target, c):
    lo, hi = 0, len(xs)
    while lo < hi:
        mid = (lo + hi) // 2
        if c.lt(xs[mid], target):
            lo = mid + 1
        else:
            hi = mid
    return lo < len(xs) and xs[lo] == target


def insertion_sort(xs, c):
    xs = list(xs)
    for i in range(1, len(xs)):
        j = i
        while j > 0 and c.lt(xs[j], xs[j - 1]):
            xs[j], xs[j - 1] = xs[j - 1], xs[j]
            j -= 1
    return xs


def merge_sort(xs, c):
    if len(xs) <= 1:
        return list(xs)
    mid = len(xs) // 2
    a, b = merge_sort(xs[:mid], c), merge_sort(xs[mid:], c)
    out, i, j = [], 0, 0
    while i < len(a) and j < len(b):
        if c.lt(b[j], a[i]):
            out.append(b[j]); j += 1
        else:
            out.append(a[i]); i += 1
    return out + a[i:] + b[j:]


SIZES = [250, 500, 1000, 2000, 4000]


def measure(name, rng):
    counts = []
    for n in SIZES:
        xs = [rng.random() for _ in range(n)]
        c = Counter()
        if name == "linear search (miss)":
            linear_search(xs, -1.0, c)
        elif name == "binary search":
            s = sorted(xs)
            for t in rng.sample(s, 50):
                binary_search(s, t, c)
            c.n //= 50
        elif name == "insertion sort":
            insertion_sort(xs, c)
        elif name == "insertion sort (sorted input)":
            insertion_sort(sorted(xs), c)
        else:
            merge_sort(xs, c)
        counts.append(c.n)
    return counts


def slope(counts):
    xs = [math.log(n) for n in SIZES]
    ys = [math.log(max(c, 1)) for c in counts]
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)


def main():
    rng = random.Random(39)
    print("Comparisons counted at each n; the exponent is the slope of log(count) against log(n)\n")
    print(f"{'algorithm':<30}" + "".join(f"{n:>10,}" for n in SIZES) + f"{'exponent':>10}  expected")
    expected = {"linear search (miss)": "O(n): 1", "binary search": "O(lg n): ~0", "insertion sort": "O(n^2): 2",
                "insertion sort (sorted input)": "best case: 1", "merge sort": "O(n lg n): just over 1"}
    for name in expected:
        counts = measure(name, rng)
        print(f"{name:<30}" + "".join(f"{c:>10,}" for c in counts) + f"{slope(counts):>10.2f}  {expected[name]}")
    print("\nDoubling n doubles a linear count, quadruples a quadratic one, and adds about one comparison to binary search.")


if __name__ == "__main__":
    main()
