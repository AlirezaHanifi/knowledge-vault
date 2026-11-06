"""Push gossip: rounds to reach every node, messages and redundancy.

Illustrates Database Internals, Chapter 12, "Gossip Dissemination" (pp. 250-253):
an infected node pushes to `fanout` random peers per round; information spreads
in roughly logarithmic rounds, and later messages mostly hit nodes that already
know (redundancy). Here infected nodes keep pushing until everyone is infected
(no interest loss). Cluster sizes, fanouts and seeds are the vault's.
"""

import math
import random

RUNS = 20


def spread(n, fanout, rnd):
    infected = {0}
    rounds = messages = redundant = 0
    while len(infected) < n:
        rounds += 1
        new = set()
        for _ in infected:
            for peer in rnd.sample(range(n), fanout):
                messages += 1
                if peer in infected or peer in new:
                    redundant += 1
                else:
                    new.add(peer)
        infected |= new
    return rounds, messages, redundant


print(f"Push gossip from one node, averaged over {RUNS} seeded runs\n")
print(f"{'nodes':>6} {'fanout':>6} {'rounds':>7} {'log2 N':>7} {'messages/node':>14} {'redundant':>10}")
for n in (100, 1_000, 10_000):
    for fanout in (1, 2, 3):
        rnd = random.Random(n * 10 + fanout)
        res = [spread(n, fanout, rnd) for _ in range(RUNS)]
        rounds = sum(r[0] for r in res) / RUNS
        msgs = sum(r[1] for r in res) / RUNS
        red = sum(r[2] for r in res) / sum(r[1] for r in res)
        print(f"{n:>6} {fanout:>6} {rounds:>7.1f} {math.log2(n):>7.1f} {msgs / n:>14.1f} {red:>10.0%}")
