"""Which (Q1, Q2) quorum sizes are safe? Enumerating every pair of quorums.

Illustrates Database Internals, Chapter 14, "Flexible Paxos" (pp. 296-297): only
the phase 1 (election) quorum must intersect the phase 2 (replication) quorum,
so Q1 + Q2 > N suffices; and "PBFT Algorithm" (p. 306): n = 3f + 1 with 2f + 1
commit quorums. The brute-force check is the vault's own.
"""

from itertools import combinations


def always_intersect(n, q1, q2):
    """Return None if every q1-subset meets every q2-subset, else a disjoint pair."""
    nodes = range(n)
    for a in combinations(nodes, q1):
        sa = set(a)
        for b in combinations(nodes, q2):
            if sa.isdisjoint(b):
                return a, b
    return None


print("Safe (Q1, Q2) pairs: every election quorum meets every replication quorum\n")
for n in range(3, 8):
    safe = [(q1, q2) for q1 in range(1, n + 1) for q2 in range(1, n + 1) if always_intersect(n, q1, q2) is None]
    assert all(q1 + q2 > n for q1, q2 in safe)
    assert all((q1, q2) in safe for q1 in range(1, n + 1) for q2 in range(1, n + 1) if q1 + q2 > n)
    smallest = [f"({n - q2 + 1},{q2})" for q2 in range(1, n + 1)]
    print(f"N={n}: safe exactly when Q1 + Q2 > {n}; minimal pairs " + " ".join(smallest))

print("\nN=5 configurations")
print(f"{'Q1':>3} {'Q2':>3} {'safe':>5} {'election survives':>18} {'replication survives':>21}")
for q1, q2 in ((3, 3), (4, 2), (5, 1), (3, 2)):
    bad = always_intersect(5, q1, q2)
    print(f"{q1:>3} {q2:>3} {'yes' if bad is None else 'no':>5} {5 - q1:>12} failed {5 - q2:>15} failed"
          + ("" if bad is None else f"   e.g. {set(bad[0])} and {set(bad[1])} are disjoint"))

print("\nPBFT: n = 3f + 1, commit quorum 2f + 1")
print(f"{'f':>2} {'n':>3} {'prepare 2f':>11} {'commit 2f+1':>12} {'min overlap':>12} {'honest in overlap':>18}")
for f in (1, 2, 3):
    n, q = 3 * f + 1, 2 * f + 1
    overlap = 2 * q - n
    print(f"{f:>2} {n:>3} {2 * f:>11} {q:>12} {overlap:>12} {overlap - f:>18}")
