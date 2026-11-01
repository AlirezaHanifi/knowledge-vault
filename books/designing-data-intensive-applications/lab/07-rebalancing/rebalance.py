"""How much data moves when a node joins? Compares hash mod N, a fixed number
of shards, a consistent-hashing ring with virtual nodes, and rendezvous hashing.

Illustrates DDIA 2nd ed., Chapter 7, "Sharding by Hash of Key" (pp. 258-263).
The ring with virtual nodes is a widely used variant of consistent hashing;
the book names consistent hashing, rendezvous and jump hashing generally.
Code is the vault's own.
"""

from __future__ import annotations

import bisect
import hashlib

KEYS = [f"user:{i}" for i in range(20_000)]


def h(s: str) -> int:
    return int.from_bytes(hashlib.blake2b(s.encode(), digest_size=8).digest(), "big")


KEY_HASH = [h(k) for k in KEYS]


def mod_n(n: int) -> list[int]:
    return [x % n for x in KEY_HASH]


def fixed_shards(n: int, shards: int = 256) -> list[int]:
    """Shards are dealt to nodes; a new node steals shards evenly from the existing ones."""
    owner = [0] * shards
    for nodes in range(2, n + 1):
        counts = [owner.count(i) for i in range(nodes - 1)]
        for _ in range(shards // nodes):
            donor = counts.index(max(counts))
            s = max(i for i, o in enumerate(owner) if o == donor)
            owner[s] = nodes - 1
            counts[donor] -= 1
    return [owner[x % shards] for x in KEY_HASH]


def ring(n: int, vnodes: int = 64) -> list[int]:
    points = sorted((h(f"node{i}#{v}"), i) for i in range(n) for v in range(vnodes))
    positions = [p for p, _ in points]
    out = []
    for x in KEY_HASH:
        j = bisect.bisect(positions, x) % len(points)    # first point clockwise from the key
        out.append(points[j][1])
    return out


def rendezvous(n: int) -> list[int]:
    return [max(range(n), key=lambda i: h(f"{x}:{i}")) for x in KEY_HASH]


def imbalance(assign: list[int], n: int) -> float:
    counts = [0] * n
    for a in assign:
        counts[a] += 1
    return max(counts) / (len(assign) / n)


def main() -> None:
    strategies = [("hash mod N", mod_n), ("256 fixed shards", fixed_shards),
                  ("ring, 64 vnodes", ring), ("rendezvous", rendezvous)]
    print("Share of 20,000 keys that move when going from N-1 to N nodes (ideal: 1/N)\n")
    header = f"{'N':>3} {'ideal':>7}" + "".join(f"{name:>18}" for name, _ in strategies)
    print(header)
    prev = {name: fn(2) for name, fn in strategies}
    for n in range(3, 11):
        row = f"{n:>3} {1 / n:7.1%}"
        for name, fn in strategies:
            cur = fn(n)
            moved = sum(a != b for a, b in zip(prev[name], cur)) / len(KEYS)
            row += f"{moved:18.1%}"
            prev[name] = cur
        print(row)
    print("\nLoad imbalance at N = 10 (busiest node / mean)")
    for name, fn in strategies:
        print(f"  {name:<18} {imbalance(fn(10), 10):.2f}x")


if __name__ == "__main__":
    main()
