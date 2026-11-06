# Atoms in a seeded scheduler

Threads increment a shared counter of database accesses, as in the chapter's example. Each increment is split into steps, and a seeded scheduler interleaves the steps of all threads, so every strategy runs on reproducible interleavings. With no protection, the counter is read then written. With a mutex, a thread locks, reads, writes and unlocks. With an atom, it takes a snapshot, computes, and compare-and-sets, retrying on failure.

*Illustrates Data-Oriented Programming, chapter 8, sections 8.1–8.2, pp. 164–170 (listings 8.1–8.3, figure 8.2). The step model and the scheduler are the vault's (seeded). A blocked thread that the scheduler picks counts one wait.*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 atom_swap.py
```

## Expected output

```text
Each thread increments the counter 1,000 times; 5 seeded interleavings per row (sum shown)
threads strategy  expected  lost updates  mutex waits  CAS retries     steps
      1     none     5,000             0            0            0    10,000
      1    mutex     5,000             0            0            0    20,000
      1     atom     5,000             0            0            0    15,000
      2     none    10,000         3,694            0            0    20,000
      2    mutex    10,000             0       29,787            0    69,787
      2     atom    10,000             0            0        5,877    47,631
      4     none    20,000        12,507            0            0    40,000
      4    mutex    20,000             0      176,419            0   256,419
      4     atom    20,000             0            0       29,465   148,395
      8     none    40,000        31,499            0            0    80,000
      8    mutex    40,000             0      832,680            0   992,680
      8     atom    40,000             0            0      112,722   458,166

Atom with a slower update function (4 threads, seed 0): retries grow, nothing is lost
extra steps in f  CAS retries  retries per update  lost
               0        5,973                1.49     0
               2        7,784                1.95     0
               5        9,098                2.27     0
              10        9,836                2.46     0
              20       10,668                2.67     0
```

## What to look for

- Without protection, updates are lost as soon as there are two threads, and more with eight.
- The mutex and the atom never lose an update. The mutex pays in waits, the atom in compare-and-set retries.
- Retries grow as the update function gets slower, since the window for another thread to commit widens. Yet every swap finishes: in this race between threads there is always a winner (p. 170).
- The counts are model steps, not time. On real hardware a failed compare-and-set is cheap, and a blocked thread is descheduled rather than spinning.

## Related

- Chapter note: [8. Advanced concurrency control](../../chapters/08-advanced-concurrency-control.md) — sections 8.1–8.2, pp. 164–170
