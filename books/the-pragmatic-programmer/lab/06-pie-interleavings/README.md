# Every interleaving of the pie case

How often do the diner's waiters oversell the last slice? Each waiter runs the book's steps: read the pie count, check it, promise, take, give. With a semaphore, they lock first and unlock after taking. With `get_pie_if_available`, the check and the take are one atomic call. The script enumerates every possible interleaving of two or three waiters (with memoization) and counts those that end with more promises than slices.

*Illustrates The Pragmatic Programmer, Topic 34, Shared State Is Incorrect State, pp. 299–304. The steps follow the book's pseudo-code; the exhaustive enumeration is the vault's. The vault's [pie-case widget](../../widgets/06-pie-case.html) lets you step through the same interleavings by hand.*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 pie_interleavings.py
```

## Expected output

```text
Every interleaving of the waiters' steps; 'oversold' = more promises than slices

protection             waiters slices  interleavings  oversold   share
no lock                      2      1            246       240   97.6%
no lock                      3      1        677,610   677,520  100.0%
no lock                      3      2        749,448   745,920   99.5%
semaphore                    2      1             12         0    0.0%
semaphore                    3      1            396         0    0.0%
semaphore                    3      2            468         0    0.0%
get_pie_if_available         2      1             12         0    0.0%
get_pie_if_available         3      1            270         0    0.0%
get_pie_if_available         3      2            756         0    0.0%
```

## What to look for

- Without a lock, only the interleavings in which one waiter finishes taking before the other looks are safe: 6 of 246 for two waiters, and 90 of 677,610 for three.
- A semaphore makes every interleaving safe, and leaves far fewer of them, because one waiter's check-and-take can't be interrupted.
- The transactional `get_pie_if_available` is also always safe, and it puts the rule in the resource, so no caller can forget the convention.

## Related

- Chapter note: [6. Concurrency](../../chapters/06-concurrency.md) — Topic 34, Shared State Is Incorrect State, pp. 299–304
