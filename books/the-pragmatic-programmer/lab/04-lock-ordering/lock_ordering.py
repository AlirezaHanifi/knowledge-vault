"""Lock ordering and deadlock: random interleavings of threads that each need two resources.

Illustrates The Pragmatic Programmer, Topic 26, How to Balance Resources (pp. 212-216):
allocate resources in the same order everywhere to reduce deadlock. The model is the vault's.
"""
import random

TRIALS = 20_000


def run(threads: int, resources: int, ordered: bool, rng: random.Random) -> bool:
    """Simulate one schedule. Each thread takes two distinct resources, works, releases. True if deadlocked."""
    plans = []
    for _ in range(threads):
        a, b = rng.sample(range(resources), 2)
        if ordered:
            a, b = min(a, b), max(a, b)
        plans.append([("lock", a), ("lock", b), ("work", None), ("unlock", b), ("unlock", a)])
    owner = [None] * resources
    pc = [0] * threads
    while True:
        runnable = []
        for t in range(threads):
            if pc[t] >= len(plans[t]):
                continue
            op, r = plans[t][pc[t]]
            if op == "lock" and owner[r] is not None and owner[r] != t:
                continue
            runnable.append(t)
        if not runnable:
            return any(pc[t] < len(plans[t]) for t in range(threads))
        t = rng.choice(runnable)
        op, r = plans[t][pc[t]]
        if op == "lock":
            owner[r] = t
        elif op == "unlock":
            owner[r] = None
        pc[t] += 1


def main() -> None:
    rng = random.Random(26)
    print(f"{TRIALS:,} random schedules per row; each thread locks two resources, works, then unlocks\n")
    print(f"{'threads':>7} {'resources':>9}  {'any order':>10}  {'global order':>12}")
    for threads, resources in ((2, 2), (2, 3), (3, 3), (4, 4), (8, 4)):
        free = sum(run(threads, resources, False, rng) for _ in range(TRIALS))
        ordd = sum(run(threads, resources, True, rng) for _ in range(TRIALS))
        print(f"{threads:>7} {resources:>9}  {free / TRIALS:>10.2%}  {ordd / TRIALS:>12.2%}")
    print("\nPercentages are the share of schedules that ended with every remaining thread waiting forever.")


if __name__ == "__main__":
    main()
