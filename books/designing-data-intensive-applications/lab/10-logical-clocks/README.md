# Physical clocks, Lamport clocks, hybrid logical clocks

Three nodes whose time-of-day clocks are skewed by up to ±40 ms exchange chat messages, many of which reply to earlier ones. Each message is stamped three ways and we count replies that a timestamp sort would place before the message they answer.

*Illustrates DDIA 2nd ed., “Logical Clocks”, pp. 420–423. The implementation is the vault’s own.*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 clocks.py
```

## Expected output

```text
300 messages, 192 of them replies; clock skew {'Aaliyah': 40, 'Bryce': -35, 'Caleb': 0}

timestamp scheme     replies ordered before their parent    max |ts - true time|
physical                                              39                   40 ms
lamport                                                0         n/a (a counter)
hlc                                                    0                   40 ms

Example violation with physical clocks:
  message by Caleb    true time 1118  physical 1118  lamport 6  hlc 1118.0
  reply   by Bryce    true time 1151  physical 1116  lamport 7  hlc 1118.1
```

## What to look for

- Physical timestamps put ~20% of replies before their parent — a clock running 35 ms slow is enough.
- Lamport timestamps never violate causality, but are counters unrelated to wall-clock time.
- Hybrid logical clocks also never violate causality, and stay within the clock skew of real time.

## Related

- Chapter note: [10. Consistency and Consensus](../../chapters/10-consistency-and-consensus.md) — “Logical Clocks”, pp. 420–423
