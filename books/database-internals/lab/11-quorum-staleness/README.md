# Quorum overlap and stale reads

When does a read miss the latest write? This experiment runs 20,000 write-then-read steps against N replicas. Each write is acknowledged by W live replicas and reaches the others asynchronously after a few steps. Each read asks R live replicas and keeps the newest version. Replicas are down independently 5% of the time, and an operation fails when too few replicas are up.

*Illustrates Database Internals, “Tunable Consistency”, pp. 235–236: with R + W > N, the read and write sets always share at least one replica. The failure rate, propagation delay and workload are the vault's (seeded); so is the implementation.*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 quorum_staleness.py
```

## Expected output

```text
20,000 write+read steps, each replica down with probability 5% per step,
async propagation to the other replicas after ~3 steps on average

 N  W  R  R+W>N  stale reads  writes unavailable  reads unavailable
 3  1  1     no       64.16%               0.01%              0.01%
 3  2  1     no       28.74%               0.66%              0.01%
 3  2  2    yes        0.00%               0.78%              0.78%
 3  1  3    yes        0.00%               0.01%             14.11%
 3  3  3    yes        0.00%              14.11%             14.11%
 5  1  1     no       78.63%               0.00%              0.00%
 5  2  2     no       26.58%               0.00%              0.00%
 5  3  3    yes        0.00%               0.13%              0.13%
 5  2  4    yes        0.00%               0.01%              2.21%
```

## What to look for

- Every configuration with R + W > N has zero stale reads: some replica in the read set always holds the latest acknowledged write.
- Without overlap, stale reads are common. Their rate depends on how fast asynchronous propagation catches up.
- Overlap costs availability. W = 3 (or R = 3) of 3 fails whenever any replica is down, about 14% of steps here. Majorities, 2 of 3 or 3 of 5, keep both low.
- W = 2, R = 4 with N = 5 shows the trade-off between read and write cost: writes stay cheap while reads still overlap.

## Related

- Chapter note: [11. Replication and Consistency](../../chapters/11-replication-and-consistency.md) — “Tunable Consistency”, pp. 235–236
