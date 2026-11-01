"""Tumbling windows by event time vs processing time, with straggler handling.

Illustrates DDIA 2nd ed., Chapter 12, "Reasoning About Time" (pp. 518-523):
processing-time windows misattribute delayed events (Figure 12-8); event-time
windows must decide when a window is complete and what to do with stragglers
(ignore them, or publish a correction). The arrival model is the vault's own.
"""

from __future__ import annotations

import random
from collections import Counter

WINDOW = 60          # one-minute tumbling windows (seconds)
SPAN = 10 * 60       # ten minutes of events


def make_stream(seed: int = 4):
    rng = random.Random(seed)
    events = []
    for _ in range(3_000):
        t = rng.uniform(0, SPAN)
        delay = rng.expovariate(1 / 2)                          # typically ~2 s
        if rng.random() < 0.03:
            delay += rng.uniform(60, 300)                       # offline device, sent much later
        events.append((t, t + delay))
    # Consumer restarts at 300-360 s and catches up on the backlog afterwards.
    events = [(t, a if not 300 <= a < 360 else 360 + (a - 300) / 10) for t, a in events]
    return sorted(events, key=lambda e: e[1])                   # arrival order


def run(events, grace: float, policy: str):
    """Close window w at processing time (w+1)*WINDOW + grace; handle late events by policy."""
    counts, emitted, dropped, corrections = Counter(), {}, 0, Counter()
    for event_time, arrival in events:
        for w in range(SPAN // WINDOW):                         # close windows whose time has come
            if w not in emitted and (w + 1) * WINDOW + grace <= arrival:
                emitted[w] = counts[w]
        w = int(event_time // WINDOW)
        if w in emitted:
            if policy == "drop":
                dropped += 1
                continue
            corrections[w] += 1
        counts[w] += 1
    for w in range(SPAN // WINDOW):
        emitted.setdefault(w, counts[w])
    return emitted, counts, dropped, corrections


def main() -> None:
    events = make_stream()
    truth = Counter(int(t // WINDOW) for t, _ in events)
    by_arrival = Counter(min(int(a // WINDOW), SPAN // WINDOW - 1) for _, a in events)

    print("Per-minute counts (3,000 events; 3% from offline devices; consumer down 300-360 s)\n")
    em5, fin5, drop5, _ = run(events, grace=5, policy="drop")
    em60, _, drop60, _ = run(events, grace=60, policy="drop")
    _, fincorr, _, corr = run(events, grace=5, policy="correct")
    print(f"{'minute':>6} {'true':>6} {'proc-time':>10} {'ev-time+5s':>11} {'ev-time+60s':>12} {'+corrections':>13}")
    for w in range(SPAN // WINDOW):
        print(f"{w:>6} {truth[w]:>6} {by_arrival[w]:>10} {em5[w]:>11} {em60[w]:>12} "
              f"{fincorr[w]:>9} (+{corr[w]})")
    err = lambda c: sum(abs(c[w] - truth[w]) for w in range(SPAN // WINDOW))
    print(f"\nTotal absolute error   processing time: {err(by_arrival)}   "
          f"event time, 5 s grace: {err(em5)} ({drop5} dropped)   "
          f"60 s grace: {err(em60)} ({drop60} dropped)   with corrections: {err(fincorr)}")
    print("Waiting longer reduces dropped stragglers but delays every result by the grace period.")


if __name__ == "__main__":
    main()
