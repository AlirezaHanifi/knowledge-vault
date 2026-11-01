"""A minimal LSM-tree storage engine: WAL, memtable, SSTables, sparse index,
Bloom filters, size-tiered compaction, tombstones, and crash recovery.

Illustrates DDIA 2nd ed., Chapter 4, "Log-Structured Storage" (pp. 118-125).
The design follows the book's description; the code is the vault's own and
favours clarity over performance (SSTables are JSON-lines files).
"""

from __future__ import annotations

import hashlib
import json
import os
import random
import tempfile

TOMBSTONE = None          # a deleted key is stored as a null value
BLOCK = 16                # keys per block; the sparse index stores each block's first key


class BloomFilter:
    def __init__(self, n_keys: int, bits_per_key: int = 10, k: int = 7):
        self.m = max(64, n_keys * bits_per_key)
        self.k = k
        self.bits = bytearray(self.m // 8 + 1)

    def _positions(self, key: str):
        digest = hashlib.blake2b(key.encode(), digest_size=16).digest()
        h1, h2 = int.from_bytes(digest[:8], "little"), int.from_bytes(digest[8:], "little")
        return ((h1 + i * h2) % self.m for i in range(self.k))   # double hashing

    def add(self, key: str) -> None:
        for p in self._positions(key):
            self.bits[p // 8] |= 1 << (p % 8)

    def might_contain(self, key: str) -> bool:
        return all(self.bits[p // 8] & (1 << (p % 8)) for p in self._positions(key))


class SSTable:
    """Immutable sorted file plus an in-memory sparse index and Bloom filter."""

    def __init__(self, path: str, items: list[tuple[str, str | None]]):
        self.path = path
        self.index: list[tuple[str, int]] = []      # (first key of block, byte offset)
        self.bloom = BloomFilter(len(items))
        with open(path, "w", encoding="utf-8") as f:
            for i, (key, value) in enumerate(items):
                if i % BLOCK == 0:
                    self.index.append((key, f.tell()))
                f.write(json.dumps([key, value]) + "\n")
                self.bloom.add(key)
        self.size = os.path.getsize(path)

    def get(self, key: str):
        """Return (found, value). Binary-search the sparse index, scan one block."""
        lo, hi = 0, len(self.index) - 1
        if hi < 0 or key < self.index[0][0]:
            return False, None
        while lo < hi:                               # last block whose first key <= key
            mid = (lo + hi + 1) // 2
            if self.index[mid][0] <= key:
                lo = mid
            else:
                hi = mid - 1
        with open(self.path, encoding="utf-8") as f:
            f.seek(self.index[lo][1])
            for _ in range(BLOCK):
                line = f.readline()
                if not line:
                    break
                k, v = json.loads(line)
                if k == key:
                    return True, v
                if k > key:
                    break
        return False, None

    def items(self):
        with open(self.path, encoding="utf-8") as f:
            for line in f:
                k, v = json.loads(line)
                yield k, v


class LSMTree:
    def __init__(self, directory: str, memtable_limit: int = 500, tier_threshold: int = 4):
        self.dir = directory
        self.memtable: dict[str, str | None] = {}
        self.limit = memtable_limit
        self.threshold = tier_threshold
        self.tables: list[SSTable] = []             # newest first
        self.seq = 0
        self.wal_path = os.path.join(directory, "wal.log")
        self.wal = open(self.wal_path, "a", encoding="utf-8")
        self.user_bytes = 0
        self.disk_bytes = 0
        self.compactions = 0

    # -- writes ---------------------------------------------------------
    def put(self, key: str, value: str | None) -> None:
        record = json.dumps([key, value]) + "\n"
        self.wal.write(record)                       # 1. durability: append to the log
        self.wal.flush()
        self.user_bytes += len(record)
        self.disk_bytes += len(record)
        self.memtable[key] = value                   # 2. update the in-memory table
        if len(self.memtable) >= self.limit:
            self.flush()

    def delete(self, key: str) -> None:
        self.put(key, TOMBSTONE)

    def flush(self) -> None:
        if not self.memtable:
            return
        self.seq += 1
        table = SSTable(os.path.join(self.dir, f"sst-{self.seq:05d}.jsonl"), sorted(self.memtable.items()))
        self.tables.insert(0, table)
        self.disk_bytes += table.size
        self.memtable.clear()
        self.wal.close()                             # the memtable is durable now: start a new log
        self.wal = open(self.wal_path, "w", encoding="utf-8")
        if len(self.tables) >= self.threshold:
            self.compact()

    def compact(self) -> None:
        """Size-tiered: merge all tables (newest value wins); drop tombstones at the bottom."""
        merged: dict[str, str | None] = {}
        for table in reversed(self.tables):          # oldest first, so newer overwrite older
            for k, v in table.items():
                merged[k] = v
        live = [(k, v) for k, v in sorted(merged.items()) if v is not TOMBSTONE]
        self.seq += 1
        new = SSTable(os.path.join(self.dir, f"sst-{self.seq:05d}.jsonl"), live)
        for t in self.tables:
            os.remove(t.path)
        self.tables = [new]
        self.disk_bytes += new.size
        self.compactions += 1

    # -- reads ----------------------------------------------------------
    def get(self, key: str, use_bloom: bool = True):
        """Return (value, number of SSTable files actually read)."""
        if key in self.memtable:
            return self.memtable[key], 0
        reads = 0
        for table in self.tables:                    # newest first
            if use_bloom and not table.bloom.might_contain(key):
                continue
            reads += 1
            found, value = table.get(key)
            if found:
                return value, reads
        return None, reads

    # -- recovery -------------------------------------------------------
    def crash_and_recover(self) -> int:
        """Lose the memtable, then rebuild it by replaying the WAL."""
        self.memtable.clear()
        self.wal.close()
        replayed = 0
        with open(self.wal_path, encoding="utf-8") as f:
            for line in f:
                k, v = json.loads(line)
                self.memtable[k] = v
                replayed += 1
        self.wal = open(self.wal_path, "a", encoding="utf-8")
        return replayed


def main() -> None:
    rng = random.Random(7)
    keys = [f"user:{i:05d}" for i in range(5_000)]
    truth: dict[str, str | None] = {}

    with tempfile.TemporaryDirectory() as d:
        db = LSMTree(d)
        for i in range(30_000):                      # skewed writes: low key numbers are hot
            key = keys[int(len(keys) * rng.random() ** 2)]
            if rng.random() < 0.05:
                db.delete(key)
                truth[key] = None
            else:
                value = f"v{i}"
                db.put(key, value)
                truth[key] = value

        print("Workload: 30,000 writes (5% deletes) over 5,000 keys, memtable limit 500")
        print(f"  SSTables on disk now:         {len(db.tables)}")
        print(f"  compactions run:              {db.compactions}")
        print(f"  write amplification:          {db.disk_bytes / db.user_bytes:.2f}x "
              f"(bytes written to disk / bytes written by the application)")

        probes = rng.sample(keys, 2_000) + [f"missing:{i}" for i in range(2_000)]
        for use_bloom in (False, True):
            reads = 0
            for k in probes:
                value, n = db.get(k, use_bloom)
                assert value == truth.get(k), k
                reads += n
            label = "with Bloom filters" if use_bloom else "without Bloom filters"
            print(f"  SSTable reads per get, {label:<22} {reads / len(probes):.2f}")

        fp = sum(1 for i in range(10_000) for t in db.tables if t.bloom.might_contain(f"absent:{i}"))
        checks = 10_000 * len(db.tables)
        print(f"  Bloom false-positive rate:    {fp / checks:.2%} (10 bits/key, 7 hashes)")

        in_memory = len(db.memtable)
        replayed = db.crash_and_recover()
        ok = all(db.get(k)[0] == v for k, v in truth.items())
        print(f"\nCrash: lost {in_memory} memtable entries; replayed {replayed} WAL records; "
              f"all {len(truth)} keys correct after recovery: {ok}")


if __name__ == "__main__":
    main()
