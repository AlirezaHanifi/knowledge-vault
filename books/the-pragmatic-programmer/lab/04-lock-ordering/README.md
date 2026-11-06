# Lock ordering and deadlock

How much does a global lock order help? Each thread picks two of the shared resources, locks them one after the other, works, and unlocks. A random scheduler interleaves the threads' steps; a schedule deadlocks when every remaining thread is waiting for a lock another one holds. The script runs 20,000 schedules per row, with each thread taking its resources in any order, and with every thread taking them in the same global order (lowest number first).

*Illustrates The Pragmatic Programmer, Topic 26, How to Balance Resources, pp. 212–216: allocate the same resources in the same order everywhere to reduce the chance of deadlock. The thread and resource counts, the scheduler and the model are the vault's (seeded).*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 lock_ordering.py
```

## Expected output

```text
20,000 random schedules per row; each thread locks two resources, works, then unlocks

threads resources   any order  global order
      2         2      24.81%         0.00%
      2         3       8.12%         0.00%
      3         3      24.45%         0.00%
      4         4      25.51%         0.00%
      8         4      77.70%         0.00%

Percentages are the share of schedules that ended with every remaining thread waiting forever.
```

## What to look for

- With no ordering, about a quarter of the schedules deadlock as soon as two threads want the same two resources, and more than three quarters do with 8 threads on 4 resources.
- With a global order, no schedule deadlocks: a cycle of waiting threads would need someone to hold a higher-numbered lock while waiting for a lower one, which the order forbids.
- More resources per thread make collisions rarer (2 threads on 3 resources) but never make deadlock impossible. Only the ordering rule does.

## Related

- Chapter note: [4. Pragmatic Paranoia](../../chapters/04-pragmatic-paranoia.md) — Topic 26, How to Balance Resources, pp. 212–216
