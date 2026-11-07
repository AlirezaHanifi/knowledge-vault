"""Parallel plan: how much an agreed interface shortens a small launch.

Illustrates The Manager's Path, Chapter 3, "The Main Roles of a Tech Lead" (p. 32): the project
planner breaks work into pieces that can run in parallel, e.g. the frontend codes against an agreed
JSON format with dummy objects instead of waiting for the API. The task list, durations and
uncertainty are the vault's own; durations are drawn from a seeded triangular distribution.
"""
import random

# name: (low, likely, high) working days, and dependencies, for each plan
SEQUENTIAL = {
    "design API":        ((2, 3, 5),  []),
    "build API":         ((5, 8, 14), ["design API"]),
    "build frontend":    ((5, 7, 12), ["build API"]),          # waits for the real API
    "integrate":         ((2, 3, 6),  ["build frontend"]),
    "test and launch":   ((2, 3, 5),  ["integrate"]),
}
WITH_CONTRACT = {
    "design API":        ((2, 3, 5),  []),
    "agree JSON format": ((1, 1, 2),  ["design API"]),
    "build API":         ((5, 8, 14), ["agree JSON format"]),
    "build frontend":    ((5, 7, 12), ["agree JSON format"]),  # codes against dummy objects
    "integrate":         ((1, 2, 4),  ["build API", "build frontend"]),
    "test and launch":   ((2, 3, 5),  ["integrate"]),
}
TRIALS = 10_000


def schedule(plan, durations):
    """Earliest finish of every task, and the chain of tasks that set the end date."""
    finish, via = {}, {}
    for name, (_, deps) in plan.items():               # tasks are listed in dependency order
        start = max((finish[d] for d in deps), default=0)
        via[name] = max(deps, key=lambda d: finish[d]) if deps else None
        finish[name] = start + durations[name]
    path, node = [], list(plan)[-1]
    while node:
        path.append(node)
        node = via[node]
    return finish[list(plan)[-1]], list(reversed(path))


def likely(plan):
    return {n: est[1] for n, (est, _) in plan.items()}


def sample(plan, rng):
    return {n: rng.triangular(est[0], est[2], est[1]) for n, (est, _) in plan.items()}


def percentile(xs, p):
    xs = sorted(xs)
    return xs[int(p * (len(xs) - 1))]


def main():
    rng = random.Random(32)
    print("Most likely durations (working days)\n")
    for label, plan in (("Wait for the API", SEQUENTIAL), ("Agree JSON contract first", WITH_CONTRACT)):
        days, path = schedule(plan, likely(plan))
        print(f"{label:<27} {days:>4.0f} days   critical path: {' -> '.join(path)}")
    print(f"\n{TRIALS:,} seeded trials with uncertain durations\n")
    print(f"{'plan':<27} {'median':>7} {'90th pct':>9}")
    for label, plan in (("Wait for the API", SEQUENTIAL), ("Agree JSON contract first", WITH_CONTRACT)):
        ends = [schedule(plan, sample(plan, rng))[0] for _ in range(TRIALS)]
        print(f"{label:<27} {percentile(ends, .5):>7.1f} {percentile(ends, .9):>9.1f}")


if __name__ == "__main__":
    main()
