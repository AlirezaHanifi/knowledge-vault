"""A persistent vector in Python: DOP chapter 9, section 9.2 (pp. 178-183).

A list is stored as a tree whose leaves hold up to B elements and whose inner
nodes hold up to B children. Updating one element copies only the nodes on the
path from the root to that leaf (path copying); every other node is shared with
the previous version. Compared with copying a whole Python list on every update.
Standard library only; seeded.
"""
import math
import random

random.seed(9)


class PVec:
    """An immutable vector of fixed size n with branching factor b."""

    def __init__(self, root, n, b, depth):
        self.root, self.n, self.b, self.depth = root, n, b, depth

    @classmethod
    def from_list(cls, xs, b):
        level, depth = [tuple(xs[i:i + b]) for i in range(0, len(xs), b)], 1
        while len(level) > 1:
            level, depth = [tuple(level[i:i + b]) for i in range(0, len(level), b)], depth + 1
        return cls(level[0], len(xs), b, depth)

    def _digits(self, i):
        return [(i // self.b ** (self.depth - 1 - lv)) % self.b for lv in range(self.depth)]

    def get(self, i):
        node = self.root
        for d in self._digits(i):
            node = node[d]
        return node

    def set(self, i, v, counter=None):
        def rec(node, ds):
            new = list(node)                       # copy this node: len(node) slots
            if counter is not None:
                counter[0] += 1
                counter[1] += len(node)
            new[ds[0]] = rec(node[ds[0]], ds[1:]) if len(ds) > 1 else v
            return tuple(new)
        return PVec(rec(self.root, self._digits(i)), self.n, self.b, self.depth)


def nodes(root, seen):
    if isinstance(root, tuple) and id(root) not in seen:
        seen[id(root)] = len(root)
        for c in root:
            nodes(c, seen)
    return seen


N = 100_000
data = list(range(N))
print(f"Updating one element of a {N:,}-element list")
print(f"{'strategy':>16} {'depth':>6} {'nodes copied':>13} {'slots copied':>13}")
print(f"{'copy whole list':>16} {'-':>6} {'1':>13} {N:>13,}")
for b in (2, 4, 8, 16, 32, 64):
    v = PVec.from_list(data, b)
    c = [0, 0]
    w = v.set(54_321, "x", c)
    assert w.get(54_321) == "x" and v.get(54_321) == 54_321 and w.get(54_320) == 54_320
    print(f"{'path copy, b=' + str(b):>16} {v.depth:>6} {c[0]:>13} {c[1]:>13,}")

print()
print("Depth bounds from the book (p. 182): log2 and log32 of the collection size")
for n in (1_000, 100_000, 10_000_000, 10_000_000_000):
    print(f"  N = {n:>14,}   log2 N = {math.log2(n):5.2f}   log32 N = {math.log2(n) / 5:4.2f}")

print()
print("Memory kept by 1,001 versions (1,000 random single-element updates), N = 100,000")
print(f"{'strategy':>16} {'slots kept':>14} {'vs one version':>15}")
print(f"{'copy whole list':>16} {N * 1001:>14,} {1001:>14.0f}x")
for b in (2, 32):
    v = PVec.from_list(data, b)
    versions = [v]
    for _ in range(1000):
        v = v.set(random.randrange(N), random.random())
        versions.append(v)
    seen = {}
    for ver in versions:
        nodes(ver.root, seen)
    one = sum(nodes(versions[0].root, {}).values())
    kept = sum(seen.values())
    print(f"{'path copy, b=' + str(b):>16} {kept:>14,} {kept / one:>14.2f}x")
