# Consistent hashing vs mod N

How much data moves when a node joins? This experiment assigns 100,000 keys to 10 nodes, adds an 11th, and counts the keys that change owner. It compares three schemes: `hash mod N`, a consistent-hashing ring with one position per node, and a ring with 100 virtual nodes per node. It also reports how evenly the keys are spread afterwards.

*Illustrates Database Internals, “Database Partitioning” and “Consistent Hashing”, pp. 270–271: mod N remaps most keys when N changes, while a ring moves about K/n. Virtual nodes are the vault's addition, to show load balance. The hash choice, key names and implementation are the vault's.*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 consistent_hashing.py
```

## Expected output

```text
100,000 keys, 10 nodes -> 11 nodes; ideal movement K/n = 9,090 keys

scheme                      keys moved   share  max/mean load  load CV
hash mod N                      90,949   90.9%           1.01     0.01
ring, 1 token per node           1,162    1.2%           3.12     0.82
ring, 100 vnodes per node        9,515    9.5%           1.15     0.09
```

## What to look for

- `hash mod N` moves about 91% of the keys, nearly everything, as p. 271 warns.
- A ring with one token per node moves only the keys the new node takes over. Here that's just 1.2%, but the load is very uneven, with the busiest node holding three times the mean.
- With 100 virtual nodes per node, about 9.5% of keys move, close to the ideal K/n = 9.1%, and the load evens out.
- Load CV is the coefficient of variation of keys per node. Lower means more even.

## Related

- Chapter note: [13. Distributed Transactions](../../chapters/13-distributed-transactions.md) — “Database Partitioning”, pp. 270–271
