"""Keys moved when a node joins: hash mod N vs consistent hashing.

Illustrates Database Internals, Chapter 13, "Database Partitioning" and
"Consistent Hashing" (pp. 270-271): with hash(v) mod N most keys change owner
when N changes; on a ring only about K/n keys move. Virtual nodes (several ring
positions per node) are the vault's addition, to show load balance. Key names,
node counts and hash choice are the vault's.
"""

import bisect
import hashlib
import statistics

KEYS, NODES = 100_000, 10


def h(s):
    return int.from_bytes(hashlib.md5(s.encode()).digest()[:8], "big")


keys = [h(f"key-{i}") for i in range(KEYS)]


def mod_owner(nodes):
    return [k % nodes for k in keys]


def ring_owner(nodes, vnodes):
    points = sorted((h(f"node-{n}-v{v}"), n) for n in range(nodes) for v in range(vnodes))
    pos = [p for p, _ in points]
    return [points[bisect.bisect_right(pos, k) % len(points)][1] for k in keys]


def spread(owner, nodes):
    loads = [0] * nodes
    for o in owner:
        loads[o] += 1
    mean = KEYS / nodes
    return max(loads) / mean, statistics.pstdev(loads) / mean


print(f"{KEYS:,} keys, {NODES} nodes -> {NODES + 1} nodes; ideal movement K/n = {KEYS // (NODES + 1):,} keys\n")
print(f"{'scheme':<26}{'keys moved':>12}{'share':>8}{'max/mean load':>15}{'load CV':>9}")
for name, owner in (("hash mod N", mod_owner), ("ring, 1 token per node", lambda n: ring_owner(n, 1)),
                    ("ring, 100 vnodes per node", lambda n: ring_owner(n, 100))):
    before, after = owner(NODES), owner(NODES + 1)
    moved = sum(a != b for a, b in zip(before, after))
    peak, cv = spread(after, NODES + 1)
    print(f"{name:<26}{moved:>12,}{moved / KEYS:>8.1%}{peak:>15.2f}{cv:>9.2f}")
