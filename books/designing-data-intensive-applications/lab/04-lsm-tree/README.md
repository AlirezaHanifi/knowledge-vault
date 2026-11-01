# A minimal LSM-tree

A complete, small LSM storage engine (~200 lines): write-ahead log, memtable, SSTables written as sorted files with a sparse index (one entry per 16-key block), per-SSTable Bloom filters, size-tiered compaction, tombstones for deletes, and crash recovery by WAL replay. A skewed workload checks every read against a reference dict.

*Illustrates DDIA 2nd ed., “Log-Structured Storage”, pp. 118–125. The implementation is the vault’s own.*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 lsm.py
```

## Expected output

```text
Workload: 30,000 writes (5% deletes) over 5,000 keys, memtable limit 500
  SSTables on disk now:         2
  compactions run:              17
  write amplification:          4.09x (bytes written to disk / bytes written by the application)
  SSTable reads per get, without Bloom filters  1.91
  SSTable reads per get, with Bloom filters     0.45
  Bloom false-positive rate:    0.94% (10 bits/key, 7 hashes)

Crash: lost 245 memtable entries; replayed 258 WAL records; all 4901 keys correct after recovery: True
```

## What to look for

- Write amplification ≈ 4×: each logical write is written to the WAL, to an SSTable on flush, and again on every compaction that rewrites it.
- Bloom filters cut SSTable reads per lookup by ~4× — most of the saving comes from keys that do not exist.
- The measured false-positive rate (~1%) matches the textbook figure for 10 bits per key.
- After a simulated crash the memtable is rebuilt from the WAL and every key reads back correctly.

## Related

- Chapter note: [4. Storage and Retrieval](../../chapters/04-storage-and-retrieval.md) — “Log-Structured Storage”, pp. 118–125
- Explore in the browser: [Inside an LSM-tree](../../widgets/04-lsm-tree.html)
