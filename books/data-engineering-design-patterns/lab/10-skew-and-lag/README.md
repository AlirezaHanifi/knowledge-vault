# Skew and lag detectors

This experiment has two parts.

1. **Skew Detector.** Eight days of input volumes, where day 4 delivers only a third of the data and nobody fixes it. Each day is checked with the book's 50% tolerance, first against the previous day and then against the last successful run.
2. **Lag Detector.** The book's seven partition lags, summarized with the average, P90 (two definitions) and MAX.

*Illustrates Data Engineering Design Patterns, “Pattern: Skew Detector” (pp. 310–313; the fatality loop is on p. 312) and “Pattern: Lag Detector” (pp. 314–315; the lags 10, 5, 30, 2, 3, 5 and 3 s are the book's). The daily volumes are synthetic; the implementation is the vault’s own.*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 skew_and_lag.py
```

## Expected output

```text
Skew check against the previous day (tolerance 50%)
   day    MB  baseline   ratio  result
     1   306         -    1.00  ok
     2   294       306    0.96  ok
     3   307       294    1.04  ok
     4   102       307    0.33  FAIL
     5   328       102    3.22  FAIL
     6   329       328    1.00  ok
     7   314       329    0.95  ok
     8   269       314    0.86  ok
  failed days: 2

Skew check against the last successful run (tolerance 50%)
   day    MB  baseline   ratio  result
     1   306         -    1.00  ok
     2   294       306    0.96  ok
     3   307       294    1.04  ok
     4   102       307    0.33  FAIL
     5   328       307    1.07  ok
     6   329       328    1.00  ok
     7   314       329    0.95  ok
     8   269       314    0.86  ok
  failed days: 1

Partition lags (s): [10, 5, 30, 2, 3, 5, 3]
  average:                        8.3
  P90, linear interpolation:      18.0
  P90, nearest rank:              30
  MAX:                            30
```

## What to look for

- **The fatality loop.** Against the previous day, the healthy day 5 fails as well: it is more than three times bigger than the broken day 4. Against the last successful run (day 3), it passes.
- **The average trap.** The average lag (8.3 s, which the book rounds to 8) hides the 30-second partition. The book's P90 of 18 s comes from linear interpolation. A nearest-rank P90 over only seven values is the maximum, 30 s.

## Related

- Chapter note: [10. Data Observability Design Patterns](../../chapters/10-data-observability-design-patterns.md) — “Pattern: Skew Detector” and “Pattern: Lag Detector”, pp. 310–317
