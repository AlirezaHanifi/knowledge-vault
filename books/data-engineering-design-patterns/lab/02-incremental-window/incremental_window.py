"""Bounded vs unbounded incremental loading during backfills.

Illustrates Data Engineering Design Patterns, Chapter 2, "Pattern: Incremental
Loader" (pp. 12-16): a delta-column loader that reads `ingestion_time >= start`
turns every backfill into a load of everything up to now, while a bounded window
(`BETWEEN start AND start + 1 hour`) keeps each run's input constant.
The workload is synthetic and seeded; the code is the vault's own.
"""

import random

random.seed(2)
HOURS = 60 * 24                                    # two months of hourly runs
rows_per_hour = [random.randint(800, 1200) for _ in range(HOURS)]
prefix = [0]
for n in rows_per_hour:
    prefix.append(prefix[-1] + n)


def read_rows(start_hour: int, now: int, bounded: bool) -> int:
    end = start_hour + 1 if bounded else now
    return prefix[end] - prefix[start_hour]


now = HOURS
print(f"Source: {prefix[-1]:,} rows over {HOURS} hourly partitions ({HOURS // 24} days)")
print(f"A normal run reads one hour: about {sum(rows_per_hour) // HOURS:,} rows\n")

print("Backfilling a single past run")
print(f"  {'run replayed':<16}{'unbounded':>14}{'bounded':>12}")
for days_ago in (1, 7, 30, 59):
    h = now - days_ago * 24
    print(f"  {str(days_ago) + ' days ago':<16}{read_rows(h, now, False):>14,}{read_rows(h, now, True):>12,}")

print("\nReplaying the last 7 days (168 runs, one after another)")
start = now - 7 * 24
unb = sum(read_rows(h, now, False) for h in range(start, now))
bnd = sum(read_rows(h, now, True) for h in range(start, now))
print(f"  unbounded total rows read: {unb:,}")
print(f"  bounded total rows read:   {bnd:,}")
print(f"  unbounded / bounded:       {unb / bnd:.1f}x")
print("\nBounded runs read disjoint hours, so the 168 replays can also run in parallel.")
