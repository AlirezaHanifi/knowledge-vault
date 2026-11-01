# Concurrent writes and version vectors

Part 1 replays the book’s shopping-cart example (Figures 6-15 and 6-16) using the single-replica algorithm the book describes: the server versions each key, keeps every value not yet overwritten as a sibling, and clients merge siblings before writing. Part 2 generalizes to version vectors across two replicas.

*Illustrates DDIA 2nd ed., “Detecting Concurrent Writes”, pp. 237–243. The implementation is the vault’s own.*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 cart.py
```

## Expected output

```text
Part 1 - one replica, two clients (the book's shopping cart)
  client 1 adds milk   (based on v0) -> server v1: [milk]
  client 2 adds eggs   (based on v0) -> server v2: [milk] | [eggs]
  client 1 adds flour  (based on v1) -> server v3: [eggs] | [flour, milk]
  client 2 adds ham    (based on v2) -> server v4: [flour, milk] | [eggs, ham, milk]
  client 1 adds bacon  (based on v3) -> server v5: [eggs, ham, milk] | [bacon, eggs, flour, milk]
  a reader merging the siblings sees: [bacon, eggs, flour, ham, milk] - no item lost

Part 2 - two replicas, version vectors
  write [milk] at A           -> {'A': 1}; replicate to B: applied
  B writes [eggs, milk]       -> {'A': 1, 'B': 1}
  A writes [flour, milk]      -> {'A': 2}   (neither saw the other: concurrent)
  replicate B's write to A: concurrent sibling kept
  A now holds siblings: [flour, milk] | [eggs, milk]
  a client merges them at A   -> {'A': 3, 'B': 1}: [eggs, flour, milk]
  replicate to B: applied; B holds [eggs, flour, milk]
```

## What to look for

- Each write overwrites exactly the siblings its client had seen and keeps the concurrent ones — the server never needs to understand the values.
- Merging siblings by set union loses no items (removals would need tombstones — see the chapter note).
- Version vectors detect that two writes on different replicas are concurrent, keep both, and let a later merged write supersede them.

## Related

- Chapter note: [6. Replication](../../chapters/06-replication.md) — “Detecting Concurrent Writes”, pp. 237–243
- Explore in the browser: [Replication lag and quorums](../../widgets/06-replication.html)
