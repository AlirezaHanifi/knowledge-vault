"""Binary chop: find a regression among releases, and shrink a crashing dataset.

Illustrates The Pragmatic Programmer, Topic 20, "The Binary Chop" (pp. 174-175). Models are the vault's.
"""
import math
import random

N_COMMITS = 1000
N_RECORDS = 1000
TRIALS = 2000


def linear(bad_from: int) -> int:
    """Step back one commit at a time from the newest (known bad) to find the first bad one."""
    tests, i = 0, N_COMMITS - 2
    while i >= 0:
        tests += 1
        if i < bad_from:          # this commit passes: the next one is the culprit
            return tests
        i -= 1
    return tests


def bisect(bad_from: int) -> int:
    lo, hi, tests = 0, N_COMMITS - 1, 0   # lo known good, hi known bad
    while hi - lo > 1:
        mid = (lo + hi) // 2
        tests += 1
        if mid >= bad_from:
            hi = mid
        else:
            lo = mid
    return tests


def crashes(records: list[int], culprits: set[int]) -> bool:
    """The program crashes only if every culprit record is present."""
    return culprits <= set(records)


def halving(data: list[int], culprits: set[int]) -> tuple[int, list[int]]:
    """Keep whichever half still crashes; stop when neither half crashes alone."""
    tests = 0
    while len(data) > 1:
        half = len(data) // 2
        a, b = data[:half], data[half:]
        tests += 1
        if crashes(a, culprits):
            data = a
            continue
        tests += 1
        if crashes(b, culprits):
            data = b
            continue
        break
    return tests, data


def ddmin(data: list[int], culprits: set[int]) -> tuple[int, list[int]]:
    """Zeller's delta debugging (complement version): minimal crashing subset."""
    tests, n = 0, 2
    while len(data) >= 2:
        size = math.ceil(len(data) / n)
        chunks = [data[i:i + size] for i in range(0, len(data), size)]
        reduced = False
        for c in chunks:
            tests += 1
            if crashes(c, culprits):
                data, n, reduced = c, 2, True
                break
        if not reduced:
            for i in range(len(chunks)):
                comp = [x for j, ch in enumerate(chunks) if j != i for x in ch]
                tests += 1
                if crashes(comp, culprits):
                    data, n, reduced = comp, max(n - 1, 2), True
                    break
        if not reduced:
            if n >= len(data):
                break
            n = min(len(data), 2 * n)
    return tests, data


def main() -> None:
    rng = random.Random(20)
    print(f"Finding the commit that introduced a regression among {N_COMMITS:,} commits ({TRIALS:,} random culprits)\n")
    lin = [linear(b) for b in (rng.randrange(1, N_COMMITS) for _ in range(TRIALS))]
    bis = [bisect(b) for b in (rng.randrange(1, N_COMMITS) for _ in range(TRIALS))]
    print(f"{'strategy':<22}{'mean tests':>11}{'worst':>7}")
    print(f"{'step back one by one':<22}{sum(lin) / TRIALS:>11.1f}{max(lin):>7}")
    print(f"{'binary chop':<22}{sum(bis) / TRIALS:>11.1f}{max(bis):>7}   (log2 {N_COMMITS} = {math.log2(N_COMMITS):.1f})")

    print(f"\nShrinking a {N_RECORDS:,}-record dataset that crashes the program ({TRIALS // 4:,} trials each)\n")
    print(f"{'crash needs':<20}{'strategy':<16}{'mean tests':>11}{'mean records left':>19}{'minimal':>9}")
    for k in (1, 2):
        for name, fn in (("halving", halving), ("delta debugging", ddmin)):
            t_sum = left_sum = minimal = 0
            r = random.Random(100 + k)
            for _ in range(TRIALS // 4):
                culprits = set(r.sample(range(N_RECORDS), k))
                t, left = fn(list(range(N_RECORDS)), culprits)
                t_sum += t
                left_sum += len(left)
                minimal += set(left) == culprits
            label = "1 bad record" if k == 1 else "2 records together"
            print(f"{label:<20}{name:<16}{t_sum / (TRIALS // 4):>11.1f}{left_sum / (TRIALS // 4):>19.1f}{minimal / (TRIALS // 4):>9.0%}")


if __name__ == "__main__":
    main()
