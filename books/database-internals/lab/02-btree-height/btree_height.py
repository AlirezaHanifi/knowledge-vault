"""B+-Tree height, page reads and comparisons as fanout grows.

Illustrates Database Internals, Chapter 2, "B-Tree Lookup Complexity" (pp. 37-38):
a lookup reads one page per level, log_N(M) pages, and does log2(M) comparisons
in total because each node is binary-searched. The tree here is bulk-loaded from
sorted keys at a chosen node occupancy; the implementation is the vault's own.
"""

import bisect
import math
import random

random.seed(2)
M = 1_000_000                      # keys in the tree


def first_key(node):
    while isinstance(node, tuple):
        node = node[1][0]
    return node[0]


def build_tree(capacity, occupancy):
    per_node = max(2, int(capacity * occupancy))
    keys = list(range(0, 2 * M, 2))
    level = [keys[i:i + per_node] for i in range(0, M, per_node)]
    height = 1
    while len(level) > 1:
        nxt = []
        for i in range(0, len(level), per_node):
            children = level[i:i + per_node]
            nxt.append(([first_key(c) for c in children[1:]], children))
        level = nxt
        height += 1
    return level[0], height


def lookup(root, key):
    pages, comps, node = 0, 0, root
    while isinstance(node, tuple):
        seps, children = node
        pages += 1
        comps += max(1, math.ceil(math.log2(len(seps) + 1)))
        node = children[bisect.bisect_right(seps, key)]
    pages += 1
    comps += max(1, math.ceil(math.log2(len(node) + 1)))
    i = bisect.bisect_left(node, key)
    return pages, comps, i < len(node) and node[i] == key


probes = [2 * random.randrange(M) for _ in range(2_000)]
print(f"{M:,} keys; 2,000 random lookups per tree\n")
print(f"{'capacity':>8} {'fill':>5} {'height':>7} {'pages/lookup':>13} {'comparisons':>12}")
for capacity in (4, 16, 64, 256, 500):
    for occupancy in (1.0, 0.69):
        root, height = build_tree(capacity, occupancy)
        stats = [lookup(root, k) for k in probes]
        assert all(found for _, _, found in stats)
        pages = sum(p for p, _, _ in stats) / len(stats)
        comps = sum(c for _, c, _ in stats) / len(stats)
        print(f"{capacity:>8} {occupancy:>5.0%} {height:>7} {pages:>13.1f} {comps:>12.1f}")

print(f"\nlog2({M:,}) = {math.log2(M):.1f} comparisons, whatever the fanout")
print("Book's example, 4 billion keys:")
for n in (2, 100, 500):
    print(f"  fanout {n:>3}: ceil(log_{n}(4e9)) = {math.ceil(math.log(4e9, n))} page reads")
