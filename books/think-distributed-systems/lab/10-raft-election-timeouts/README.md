# Raft election timeouts

Why does Raft randomize election timeouts? Each simulated term, every follower draws a timeout between 150 ms and 150 ms + *spread*. A follower becomes a candidate when its timer fires, unless a `RequestVote` from an earlier candidate reached it first; then it votes for the first candidate it heard from. A candidate wins with a quorum; otherwise the vote is split and a new term starts. The script runs 5,000 elections per row for 3- and 5-node clusters and up to 50 rounds each.

*Illustrates Think Distributed Systems, “Leader Election protocol”, pp. 139–140 (random timeouts, split votes, new elections). The 150 ms base, the spreads, the 5–15 ms message delay and the one-vote-per-term simplification are the vault's (seeded); the Raft paper suggests timeouts of 150–300 ms.*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 raft_election_timeouts.py
```

## Expected output

```text
5,000 elections per row; timeouts uniform in [150, 150 + spread] ms; one-way delay 5-15 ms

nodes   spread  split in round 1  elected in 50  mean rounds*  worst*
    3      1 ms            100.0%           0.0%             —       —
    3      5 ms            100.0%           0.0%             —       —
    3     10 ms             89.3%          99.7%          8.58      50
    3     25 ms             31.4%         100.0%          1.45       7
    3     50 ms              9.5%         100.0%          1.11       4
    3    150 ms              1.0%         100.0%          1.01       3

    5      1 ms            100.0%           0.0%             —       —
    5      5 ms            100.0%           0.0%             —       —
    5     10 ms             96.3%          84.0%         17.94      50
    5     25 ms             39.4%         100.0%          1.67       9
    5     50 ms             12.5%         100.0%          1.15       5
    5    150 ms              1.2%         100.0%          1.01       3

* among elections that produced a leader within 50 rounds
```

## What to look for

- When the spread is smaller than the message delay, every follower times out before hearing from anyone. Everyone votes for themselves, and no leader is ever elected.
- A spread of a few message delays is enough: at 25 ms most elections succeed in the first round, and at 150 ms about 99% do.
- Five nodes split more often than three at the same spread, because more nodes can time out within one message delay of each other.
- Randomization is a liveness heuristic only. Safety never depends on it, which is the practical answer to FLP.

## Related

- Chapter note: [10. Distributed consensus](../../chapters/10-distributed-consensus.md) — “Leader Election protocol”, pp. 139–140
