# Flexible Paxos quorum intersection

Do all of Paxos's quorums have to be majorities? For 3 to 7 acceptors, this experiment enumerates every election (phase 1) quorum of size Q₁ and every replication (phase 2) quorum of size Q₂. It checks whether each pair always overlaps and prints a disjoint pair when one exists. It also shows how many failures each phase tolerates, and does the PBFT arithmetic for n = 3f + 1.

*Illustrates Database Internals, “Flexible Paxos”, pp. 296–297 (only Q₁ + Q₂ > N is required) and “PBFT Algorithm”, p. 306 (n = 3f + 1, quorums of 2f and 2f + 1). The brute-force check is the vault's own.*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 flexible_paxos.py
```

## Expected output

```text
Safe (Q1, Q2) pairs: every election quorum meets every replication quorum

N=3: safe exactly when Q1 + Q2 > 3; minimal pairs (3,1) (2,2) (1,3)
N=4: safe exactly when Q1 + Q2 > 4; minimal pairs (4,1) (3,2) (2,3) (1,4)
N=5: safe exactly when Q1 + Q2 > 5; minimal pairs (5,1) (4,2) (3,3) (2,4) (1,5)
N=6: safe exactly when Q1 + Q2 > 6; minimal pairs (6,1) (5,2) (4,3) (3,4) (2,5) (1,6)
N=7: safe exactly when Q1 + Q2 > 7; minimal pairs (7,1) (6,2) (5,3) (4,4) (3,5) (2,6) (1,7)

N=5 configurations
 Q1  Q2  safe  election survives  replication survives
  3   3   yes            2 failed               2 failed
  4   2   yes            1 failed               3 failed
  5   1   yes            0 failed               4 failed
  3   2    no            2 failed               3 failed   e.g. {0, 1, 2} and {3, 4} are disjoint

PBFT: n = 3f + 1, commit quorum 2f + 1
 f   n  prepare 2f  commit 2f+1  min overlap  honest in overlap
 1   4           2            3            2                  1
 2   7           4            5            3                  1
 3  10           6            7            4                  1
```

## What to look for

- The brute force agrees with the book's rule: a configuration is safe exactly when Q₁ + Q₂ > N.
- With five acceptors, Q₁ = 4 and Q₂ = 2 is safe. Replication then survives three failures, but a new election needs four live acceptors: the availability-for-latency trade on p. 297.
- With Q₁ = 3 and Q₂ = 2 there is a disjoint pair, so a new leader could miss a value the old one replicated.
- In PBFT, any two commit quorums of 2f + 1 overlap in at least f + 1 replicas, so at least one honest replica is in both.

## Related

- Chapter note: [14. Consensus](../../chapters/14-consensus.md) — “Flexible Paxos”, pp. 296–297; “PBFT Algorithm”, p. 306
