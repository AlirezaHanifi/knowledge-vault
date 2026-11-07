"""Release cadence and contention: the same changes shipped weekly or daily.

Illustrates The Manager's Path, Chapter 5, "Debugging Dysfunctional Teams" (pp. 79-80): infrequent
releases hide pain, and the author's team moved from painful weekly releases to daily ones because
releases had become a point of resource contention. The model is the vault's own: five engineers
merge changes; each change is broken with a fixed chance; a release ships every change merged since
the last one, and one broken change blocks the whole batch for a day while it is found and fixed.
"""
import random

ENGINEERS = 5
DAYS = 120                  # working days simulated
CHANGES_PER_DAY = 1.0       # chance each engineer merges a change on a given day
P_BROKEN = 0.04             # chance a change breaks the release
TRIALS = 300


def simulate(every, rng):
    """Return releases, blocked releases, mean batch size and mean days from merge to production."""
    pending, waits, batches, blocked = [], [], [], 0
    for day in range(DAYS):
        for _ in range(ENGINEERS):
            if rng.random() < CHANGES_PER_DAY:
                pending.append((day, rng.random() < P_BROKEN))
        if day % every == every - 1 and pending:
            broken = sum(b for _, b in pending)
            blocked += broken > 0
            ship_day = day + broken          # each broken change holds the whole batch a day
            batches.append(len(pending))
            waits += [ship_day - d for d, _ in pending]
            pending = []
    return len(batches), blocked, sum(batches) / len(batches), sum(waits) / len(waits)


def main():
    rng = random.Random(79)
    print(f"{ENGINEERS} engineers, {DAYS} working days, each change broken with p = {P_BROKEN}; {TRIALS} seeded trials\n")
    print(f"{'cadence':<9} {'releases':>9} {'blocked':>8} {'changes/release':>16} {'days merge->prod':>17}")
    for label, every in (("weekly", 5), ("daily", 1)):
        runs = [simulate(every, rng) for _ in range(TRIALS)]
        r, b, size, wait = (sum(x[i] for x in runs) / TRIALS for i in range(4))
        print(f"{label:<9} {r:>9.1f} {b / r:>8.0%} {size:>16.1f} {wait:>17.1f}")


if __name__ == "__main__":
    main()
