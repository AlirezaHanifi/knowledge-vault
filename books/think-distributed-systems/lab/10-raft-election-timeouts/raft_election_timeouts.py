"""Raft leader elections with randomized election timeouts.

Illustrates Think Distributed Systems, Chapter 10, "Leader Election protocol"
(pp. 139-140): a follower whose randomized timer expires becomes a candidate,
and a split vote leads to a new election. The timing model (timeouts uniform in
[150, 150 + spread] ms, one-way delays of 5-15 ms, one vote per node per term)
and the trial counts are the vault's (seeded).
"""
import random

TRIALS = 5_000
MAX_ROUNDS = 50


def election(rng, n, spread):
    """One term. Returns True if some candidate wins a quorum."""
    timeout = sorted((150 + rng.uniform(0, spread), i) for i in range(n))
    delay = {(a, b): rng.uniform(5, 15) for a in range(n) for b in range(n) if a != b}
    candidates = []
    for t, i in timeout:
        # i becomes a candidate unless a RequestVote reached it before its timer fired
        if all(tj + delay[(j, i)] > t for tj, j in candidates):
            candidates.append((t, i))
    votes = {i: 1 for _, i in candidates}               # candidates vote for themselves
    cand = {i for _, i in candidates}
    for _, i in timeout:
        if i in cand:
            continue
        first = min(candidates, key=lambda c: c[0] + delay[(c[1], i)])
        votes[first[1]] += 1
    return max(votes.values()) > n // 2


def main():
    print(f"{TRIALS:,} elections per row; timeouts uniform in [150, 150 + spread] ms; one-way delay 5-15 ms\n")
    print(f"{'nodes':>5} {'spread':>8} {'split in round 1':>17} {'elected in 50':>14} {'mean rounds*':>13} {'worst*':>7}")
    for n in (3, 5):
        for k, spread in enumerate((1, 5, 10, 25, 50, 150)):
            rng = random.Random(n * 100 + k)
            splits, rounds, worst, elected = 0, 0, 0, 0
            for _ in range(TRIALS):
                r = 1
                won = election(rng, n, spread)
                while not won and r < MAX_ROUNDS:
                    r += 1
                    won = election(rng, n, spread)
                splits += r > 1
                if won:
                    elected += 1
                    rounds += r
                    worst = max(worst, r)
            mean = f"{rounds / elected:.2f}" if elected else "—"
            print(f"{n:>5} {spread:>6} ms {splits / TRIALS:>17.1%} {elected / TRIALS:>14.1%} {mean:>13} {worst or '—':>7}")
        print()
    print("* among elections that produced a leader within 50 rounds")


if __name__ == "__main__":
    main()
