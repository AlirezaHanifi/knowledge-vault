# Bounded vs unbounded incremental backfills

A delta-column Incremental Loader that reads `ingestion_time >= start` behaves like a bounded one in normal runs, because nothing newer exists yet. When you replay an old run, though, it reads everything from that run up to now. This experiment builds two months of hourly data and compares how much each implementation reads when single runs, or a whole week, are backfilled.

*Illustrates Data Engineering Design Patterns, “Pattern: Incremental Loader”, pp. 12–16 (the bounded window `BETWEEN ingestion_time AND ingestion_time + INTERVAL '1 HOUR'` is on p. 14). The workload is synthetic; the implementation is the vault’s own.*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 incremental_window.py
```

## Expected output

```text
Source: 1,444,469 rows over 1440 hourly partitions (60 days)
A normal run reads one hour: about 1,003 rows

Backfilling a single past run
  run replayed         unbounded     bounded
  1 days ago              24,639         804
  7 days ago             170,731         979
  30 days ago            721,537         999
  59 days ago          1,420,335       1,057

Replaying the last 7 days (168 runs, one after another)
  unbounded total rows read: 14,431,698
  bounded total rows read:   170,731
  unbounded / bounded:       84.5x

Bounded runs read disjoint hours, so the 168 replays can also run in parallel.
```

## What to look for

- Replaying a run from 59 days ago with the unbounded loader reads almost the whole table. The backfill has become a full load, as the book warns.
- The bounded loader reads one hour whatever the run's age, so its compute is predictable.
- Replaying a week sequentially costs about 85 times more without the bound, because every replay reads the hours of all later replays again.

## Related

- Chapter note: [2. Data Ingestion Design Patterns](../../chapters/02-data-ingestion-design-patterns.md) — “Pattern: Incremental Loader”, pp. 12–16
- Explore in the browser: [Incremental loading and backfills](../../widgets/02-incremental-loader.html)
