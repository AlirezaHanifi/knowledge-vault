"""Deduplication window length vs missed duplicates and state size.

Illustrates Data Engineering Design Patterns, Chapter 3, "Pattern: Windowed
Deduplicator" (pp. 46-50): a streaming deduplicator remembers keys for a time
window. A short window keeps little state but misses duplicates that arrive
late; a long window catches more but holds more keys. Producer retries are
synthetic and seeded; the code is the vault's own.
"""

import random
from collections import deque

random.seed(3)
EVENTS, RATE = 200_000, 50                  # 200k events at 50 per second (~67 minutes)
DUP_SHARE = 0.05                            # 5% of events are retried by the producer

stream = []                                 # (arrival_time_s, key)
for i in range(EVENTS):
    t = i / RATE
    stream.append((t, i))
    if random.random() < DUP_SHARE:
        # most retries come back within seconds, a few after minutes
        delay = random.expovariate(1 / 8) if random.random() < 0.9 else random.uniform(60, 900)
        stream.append((t + delay, i))
stream.sort()
dups = len(stream) - EVENTS


def deduplicate(window_s: float):
    """Return (records emitted, peak number of keys held in state)."""
    seen, expiry, emitted, peak = {}, deque(), 0, 0
    for t, key in stream:
        while expiry and expiry[0][0] <= t:          # forget keys older than the window
            exp_t, k = expiry.popleft()
            if seen.get(k) == exp_t:
                del seen[k]
        if key in seen:
            continue                                 # duplicate caught
        emitted += 1
        seen[key] = t + window_s
        expiry.append((t + window_s, key))
        peak = max(peak, len(seen))
    return emitted, peak


print(f"Stream: {EVENTS:,} events, {dups:,} producer retries ({dups / EVENTS:.1%})\n")
print(f"{'window':>8}{'duplicates missed':>20}{'missed %':>10}{'peak keys in state':>21}")
for w in (5, 10, 30, 60, 300, 900):
    emitted, peak = deduplicate(w)
    missed = emitted - EVENTS
    label = f"{w} s" if w < 60 else f"{w // 60} min"
    print(f"{label:>8}{missed:>20,}{missed / dups:>10.1%}{peak:>21,}")
