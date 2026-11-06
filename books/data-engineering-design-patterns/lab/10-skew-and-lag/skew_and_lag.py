"""Skew Detector baselines and the lag average trap.

Illustrates Data Engineering Design Patterns, Chapter 10:
- "Pattern: Skew Detector" (pp. 310-313): a day-to-day volume check with a 50%
  tolerance (ratio outside 0.5-1.5 fails). After one bad day that nobody fixes,
  comparing with the previous day also fails the next, normal day (the
  "fatality loop", p. 312); comparing with the last successful run doesn't.
- "Pattern: Lag Detector" (pp. 314-315): the book's seven partition lags, whose
  average hides the slow partitions.
Daily volumes are synthetic and seeded; the code is the vault's own.
"""

import math
import random
import statistics

random.seed(10)
volumes = [round(300 * random.uniform(0.85, 1.15)) for _ in range(8)]
volumes[3] = volumes[2] // 3                      # day 4: the provider delivers a third of the data


def check(baseline_rule: str):
    results, last_ok = [], None
    for day, vol in enumerate(volumes, start=1):
        if day == 1:
            base = None
        elif baseline_rule == "previous day":
            base = volumes[day - 2]
        else:
            base = last_ok
        ratio = vol / base if base else 1.0
        ok = 0.5 <= ratio <= 1.5
        if ok:
            last_ok = vol
        results.append((day, vol, base, ratio, ok))
    return results


for rule in ("previous day", "last successful run"):
    print(f"Skew check against the {rule} (tolerance 50%)")
    print(f"  {'day':>4}{'MB':>6}{'baseline':>10}{'ratio':>8}  result")
    for day, vol, base, ratio, ok in check(rule):
        print(f"  {day:>4}{vol:>6}{(base or '-'):>10}{ratio:>8.2f}  {'ok' if ok else 'FAIL'}")
    fails = sum(1 for r in check(rule) if not r[4])
    print(f"  failed days: {fails}\n")

lags = [10, 5, 30, 2, 3, 5, 3]                     # seconds, the book's example (p. 315)
s = sorted(lags)
pos = 0.9 * (len(s) - 1)
p90_linear = s[int(pos)] + (s[int(pos) + 1] - s[int(pos)]) * (pos - int(pos))
p90_rank = s[math.ceil(0.9 * len(s)) - 1]
print("Partition lags (s):", lags)
print(f"  average:                        {statistics.mean(lags):.1f}")
print(f"  P90, linear interpolation:      {p90_linear:.1f}")
print(f"  P90, nearest rank:              {p90_rank}")
print(f"  MAX:                            {max(lags)}")
