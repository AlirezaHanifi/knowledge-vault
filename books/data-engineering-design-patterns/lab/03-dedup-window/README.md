# Deduplication window vs missed duplicates

A streaming Windowed Deduplicator remembers the keys it has seen for a fixed time window. This experiment replays a stream of 200,000 events in which 5% are retried by the producer. Most retries return within seconds and a few after several minutes. It measures how many duplicates get through, and how many keys the state store holds, for windows from 5 seconds to 15 minutes.

*Illustrates Data Engineering Design Patterns, “Pattern: Windowed Deduplicator”, pp. 46–50, and its space-vs-time consequence (p. 49). The retry delays are synthetic; the implementation is the vault’s own.*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 dedup_window.py
```

## Expected output

```text
Stream: 200,000 events, 9,978 producer retries (5.0%)

  window   duplicates missed  missed %   peak keys in state
     5 s               5,873     58.9%                  269
    10 s               3,629     36.4%                  520
    30 s               1,240     12.4%                1,518
   1 min               1,028     10.3%                3,028
   5 min                 721      7.2%               15,067
  15 min                   0      0.0%               45,001
```

## What to look for

- Missed duplicates fall quickly at first: a 30-second window already catches almost every fast retry.
- The last few duplicates are expensive. Catching the slow retries needs a 15-minute window and about 170 times the state of a 5-second one.
- State grows linearly with the window, because every key is remembered for the whole window. This is the book's space-vs-time trade-off.

## Related

- Chapter note: [3. Error Management Design Patterns](../../chapters/03-error-management-design-patterns.md) — “Pattern: Windowed Deduplicator”, pp. 46–50
- Explore in the browser: [Watermarks and late data](../../widgets/03-watermark.html)
