"""Hit ratios of FIFO, LRU, CLOCK and LFU on a B-Tree page-reference trace.

Illustrates Database Internals, Chapter 5, "Page Replacement" (pp. 85-88). Every
lookup touches the root, one internal page and one leaf, so upper levels are hot;
leaf popularity is skewed (Zipf-like). Bélády's anomaly for FIFO is checked on
the reference string 1 2 3 4 1 2 5 1 2 3 4 5. Trace and sizes are the vault's
(seeded); so is the implementation.
"""

import random
from collections import OrderedDict, Counter

random.seed(5)
LEAVES, INTERNAL, LOOKUPS = 4_000, 40, 30_000
weights = [1 / (i + 1) ** 0.9 for i in range(LEAVES)]
leaf_ids = list(range(LEAVES))
random.shuffle(leaf_ids)                      # popular leaves are scattered
trace = []
for leaf in random.choices(leaf_ids, weights, k=LOOKUPS):
    trace += ["root", f"i{leaf * INTERNAL // LEAVES}", f"l{leaf}"]
# a full scan in the middle pollutes recency-based caches
mid = len(trace) // 2
trace[mid:mid] = ["root"] + [f"l{i}" for i in range(LEAVES)]


def fifo(refs, size):
    cache, order, faults = set(), [], 0
    for p in refs:
        if p not in cache:
            faults += 1
            if len(cache) == size:
                cache.discard(order.pop(0))
            cache.add(p)
            order.append(p)
    return faults


def lru(refs, size):
    cache, faults = OrderedDict(), 0
    for p in refs:
        if p in cache:
            cache.move_to_end(p)
        else:
            faults += 1
            if len(cache) == size:
                cache.popitem(last=False)
            cache[p] = True
    return faults


def clock(refs, size):
    frames, ref, where, hand, faults = [None] * size, [0] * size, {}, 0, 0
    for p in refs:
        if p in where:
            ref[where[p]] = 1
            continue
        faults += 1
        while frames[hand] is not None and ref[hand]:
            ref[hand] = 0                     # second chance
            hand = (hand + 1) % size
        if frames[hand] is not None:
            del where[frames[hand]]
        frames[hand], ref[hand], where[p] = p, 1, hand
        hand = (hand + 1) % size
    return faults


def lfu(refs, size):
    cache, freq, faults, t = {}, Counter(), 0, 0
    for p in refs:
        t += 1
        freq[p] += 1
        if p in cache:
            cache[p] = t
            continue
        faults += 1
        if len(cache) == size:
            victim = min(cache, key=lambda q: (freq[q], cache[q]))
            del cache[victim]
        cache[p] = t
    return faults


POLICIES = (("FIFO", fifo), ("LRU", lru), ("CLOCK", clock), ("LFU", lfu))
print(f"Trace: {LOOKUPS:,} lookups (root, internal, leaf) + one {LEAVES:,}-leaf scan = {len(trace):,} page references\n")
print(f"{'cache pages':>11}" + "".join(f"{n:>9}" for n, _ in POLICIES) + "   (hit ratio)")
for size in (32, 128, 512, 1024):
    row = [1 - f(trace, size) / len(trace) for _, f in POLICIES]
    print(f"{size:>11}" + "".join(f"{h:>9.1%}" for h in row))

belady = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
print("\nBélády's anomaly, reference string", " ".join(map(str, belady)))
for frames in (3, 4):
    print(f"  FIFO with {frames} frames: {fifo(belady, frames)} faults   LRU: {lru(belady, frames)} faults")
