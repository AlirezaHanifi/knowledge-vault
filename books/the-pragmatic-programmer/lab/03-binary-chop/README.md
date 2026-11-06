# Binary chop

How many test runs does it take to find what broke? First, a regression hides among 1,000 commits: step back one commit at a time from the newest, or chop the range in half each time. Second, a 1,000-record dataset crashes the program. Halving keeps whichever half still crashes. Delta debugging (Zeller's *ddmin*) also tries complements and finer splits. Both are run against a crash caused by one bad record, and against one that needs two particular records together.

*Illustrates The Pragmatic Programmer, “The Binary Chop” in Topic 20, Debugging, pp. 174–175: chop releases and datasets in half to isolate a bug. The sizes, the two-record crash and the delta-debugging comparison are the vault's (seeded).*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 binary_chop.py
```

## Expected output

```text
Finding the commit that introduced a regression among 1,000 commits (2,000 random culprits)

strategy               mean tests  worst
step back one by one        503.2    999
binary chop                  10.0     10   (log2 1000 = 10.0)

Shrinking a 1,000-record dataset that crashes the program (500 trials each)

crash needs         strategy         mean tests  mean records left  minimal
1 bad record        halving                15.1                1.0     100%
1 bad record        delta debugging        15.0                1.0     100%
2 records together  halving                 3.6              664.7       0%
2 records together  delta debugging       122.9                2.0     100%
```

## What to look for

- Bisection needs exactly ⌈log₂ 1000⌉ = 10 tests every time; stepping back averages about 500 and can take 999.
- For a single bad record, halving and delta debugging both find it in about 15 runs.
- When the crash needs two records together, plain halving stalls as soon as they land in different halves: neither half crashes, so it stops with hundreds of records left.
- Delta debugging keeps going by testing complements, and always isolates the pair, at the cost of about 120 runs.

## Related

- Chapter note: [3. The Basic Tools](../../chapters/03-the-basic-tools.md) — “The Binary Chop”, pp. 174–175
