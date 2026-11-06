"""Saboteurs: plant bugs in a small function and see which ones the tests catch; then sample a state space.

Illustrates The Pragmatic Programmer, Topic 51, Pragmatic Starter Kit, "Testing the Tests" and
"Testing Thoroughly" (pp. 457-458, Tips 92-93). The clamp function, its mutants and its tests are the
vault's; a / (a + b) with a, b in 0..999 is the book's.
"""
import math
import random

ORIGINAL = """
def clamp(x, lo, hi):
    if x < lo:
        return lo
    if x > hi:
        return hi
    return x
"""

# (description, text to find, replacement)
MUTATIONS = [
    ("< becomes <=", "x < lo", "x <= lo"),
    ("> becomes >=", "x > hi", "x >= hi"),
    ("return lo becomes return hi", "return lo", "return hi"),
    ("return hi becomes return lo", "return hi", "return lo"),
    ("x < lo becomes x < hi", "x < lo", "x < hi"),
    ("x > hi becomes x > hi + 1", "x > hi", "x > hi + 1"),
    ("x < lo becomes x < lo - 1", "x < lo", "x < lo - 1"),
    ("return x becomes return x + 1", "return x\n", "return x + 1\n"),
]

WEAK = [((5, 0, 10), 5)]
STRONG = WEAK + [((-3, 0, 10), 0), ((42, 0, 10), 10), ((-1, 0, 10), 0), ((11, 0, 10), 10), ((0, 0, 10), 0), ((10, 0, 10), 10)]


def compile_fn(src):
    env = {}
    exec(src, env)  # noqa: S102 - the source is this file's own mutants
    return env["clamp"]


def equivalent(fn, ref):
    return all(fn(x, 0, 10) == ref(x, 0, 10) for x in range(-20, 31))


def main():
    ref = compile_fn(ORIGINAL)
    print("Mutants of clamp(x, lo, hi), run against a weak suite (1 test) and a strong suite (7 tests)\n")
    print(f"{'mutant':<32}{'weak':>10}{'strong':>10}")
    weak_k = strong_k = real = 0
    for desc, old, new in MUTATIONS:
        fn = compile_fn(ORIGINAL.replace(old, new, 1))
        if equivalent(fn, ref):
            print(f"{desc:<32}{'(equivalent: same behaviour)':>20}")
            continue
        real += 1
        w = any(fn(*a) != e for a, e in WEAK)
        s = any(fn(*a) != e for a, e in STRONG)
        weak_k += w
        strong_k += s
        print(f"{desc:<32}{'caught' if w else 'SURVIVES':>10}{'caught' if s else 'SURVIVES':>10}")
    print(f"\nmutation score: weak {weak_k}/{real}, strong {strong_k}/{real}")

    print("\nState coverage: test(a, b) = a / (a + b) for a, b in 0..999 (1,000,000 states, one fails)\n")
    rng = random.Random(51)
    print(f"{'random tests':>12}  {'line coverage':>13}  {'runs (of 100) that hit a = b = 0':>34}")
    for k in (100, 10_000, 1_000_000):
        hits = 0
        for _ in range(100):
            # index of the first random test that draws (0, 0): geometric with p = 1e-6,
            # sampled directly instead of drawing up to a million pairs one by one
            first = math.ceil(math.log(1.0 - rng.random()) / math.log(1.0 - 1e-6))
            hits += first <= k
        print(f"{k:>12,}  {'100%':>13}  {hits:>34}")
    print("\nThe chance of finding the state with k random tests is 1 - (1 - 1e-6)^k: about 63% at a million.")


if __name__ == "__main__":
    main()
