# Write skew under snapshot isolation and SSI

A small MVCC engine with snapshot reads, first-committer-wins write conflicts, and a simplified serializable-snapshot-isolation check. Replays the book’s on-call doctors example, then 1,000 random interleavings of the same two transactions.

*Illustrates DDIA 2nd ed., “Write Skew and Phantoms” and “Serializable Snapshot Isolation”, pp. 303–323. The implementation is the vault’s own.*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 mvcc.py
```

## Expected output

```text
Snapshot isolation, the book's interleaving:
    T1 (aaliyah) counts 2 doctors on call
    T2 (bryce) counts 2 doctors on call
    T1 (aaliyah) sets aaliyah off call
    T2 (bryce) sets bryce off call
    T1 (aaliyah) commits
    T2 (bryce) commits
  -> doctors still on call: 0  (aborted transactions: 0)

Serializable (SSI), the book's interleaving:
    T1 (aaliyah) counts 2 doctors on call
    T2 (bryce) counts 2 doctors on call
    T1 (aaliyah) sets aaliyah off call
    T2 (bryce) sets bryce off call
    T1 (aaliyah) commits
    T2 (bryce) ABORTED: read aaliyah which changed after the snapshot
  -> doctors still on call: 1  (aborted transactions: 1)

1,000 random interleavings of the same two transactions (38 happen to be serial):
  Snapshot isolation   nobody on call in  843 runs;    0 aborts (retry needed)
  Serializable (SSI)   nobody on call in    0 runs;  843 aborts (retry needed)
```

## What to look for

- Under snapshot isolation the two transactions write different rows, so nothing conflicts and both commit — leaving nobody on call.
- The SSI check aborts precisely the interleavings that would have violated the invariant (843 of 843) and none of the safe ones.
- Every abort is a retry the application must perform — the cost of optimistic concurrency control.

## Related

- Chapter note: [8. Transactions](../../chapters/08-transactions.md) — “Write Skew and Phantoms” and “Serializable Snapshot Isolation”, pp. 303–323
- Explore in the browser: [Isolation levels stepper](../../widgets/08-isolation.html)
