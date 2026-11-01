# How much data moves when a node joins

Assigns 20,000 keys to nodes four ways — hash mod N, a fixed number of shards, a consistent-hashing ring with virtual nodes, and rendezvous hashing — and measures the share of keys that move when the cluster grows from N−1 to N nodes, plus the resulting load imbalance.

*Illustrates DDIA 2nd ed., “Sharding by Hash of Key”, pp. 258–263. The implementation is the vault’s own.*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 rebalance.py
```

## Expected output

```text
Share of 20,000 keys that move when going from N-1 to N nodes (ideal: 1/N)

  N   ideal        hash mod N  256 fixed shards   ring, 64 vnodes        rendezvous
  3   33.3%             66.8%             33.4%             38.2%             33.0%
  4   25.0%             75.5%             25.2%             25.9%             25.5%
  5   20.0%             79.7%             19.7%             18.5%             20.2%
  6   16.7%             83.3%             16.4%             16.2%             16.7%
  7   14.3%             85.5%             13.7%             16.7%             14.2%
  8   12.5%             87.4%             12.7%             11.4%             12.0%
  9   11.1%             89.1%             11.0%              9.7%             11.1%
 10   10.0%             89.9%              9.9%             10.3%             10.5%

Load imbalance at N = 10 (busiest node / mean)
  hash mod N         1.03x
  256 fixed shards   1.04x
  ring, 64 vnodes    1.18x
  rendezvous         1.05x
```

## What to look for

- Hash mod N moves (N−1)/N of the keys — almost everything — on each addition.
- Fixed shards and rendezvous hashing move ≈ 1/N, the minimum needed to give the new node a fair share.
- The ring with 64 virtual nodes is close to 1/N but noticeably less balanced; balance improves with more virtual nodes.

## Related

- Chapter note: [7. Sharding](../../chapters/07-sharding.md) — “Sharding by Hash of Key”, pp. 258–263
- Explore in the browser: [Sharding and rebalancing](../../widgets/07-sharding.html)
