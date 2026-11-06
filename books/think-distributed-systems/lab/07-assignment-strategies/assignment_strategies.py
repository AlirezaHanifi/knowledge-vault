"""Range, hash-modulo and consistent-hashing assignment, 5 -> 6 partitions.

Illustrates Think Distributed Systems, Chapter 7, Listings 7.3-7.9 and Table 7.2
(pp. 99-103). The book used /usr/share/dict/words; this script generates 200,000
words with an approximate English first-letter distribution (seeded), so the
counts differ from the book's. The hash (MD5) and 100 virtual nodes per
partition are the vault's choices.
"""
import hashlib
import random
from bisect import bisect_left
from statistics import pstdev

FREQ = dict(a=6.1, b=5.7, c=9.4, d=5.9, e=4.0, f=3.9, g=3.3, h=3.9, i=3.8, j=0.8, k=1.0, l=3.2, m=5.6,
            n=3.1, o=3.6, p=9.4, q=0.5, r=5.0, s=11.0, t=5.3, u=3.3, v=1.5, w=2.0, x=0.1, y=0.3, z=0.3)
RANGES = {5: ["abcde", "fghij", "klmno", "pqrst", "uvwxyz"],          # Listing 7.4
          6: ["abcd", "efgh", "ijkl", "mnop", "qrst", "uvwxyz"]}      # Listing 7.7
VNODES = 100


def words(n, seed=42):
    rng, out = random.Random(seed), set()
    letters, weights = list(FREQ), list(FREQ.values())
    while len(out) < n:
        first = rng.choices(letters, weights)[0]
        out.add(first + "".join(rng.choices("abcdefghijklmnopqrstuvwxyz", k=rng.randint(2, 9))))
    return sorted(out)


def h(s):
    return int.from_bytes(hashlib.md5(s.encode()).digest()[:8], "big")


def by_range(word, n):
    return next(i for i, g in enumerate(RANGES[n]) if word[0] in g)


def by_hash(word, n):
    return h(word) % n


class Ring:
    def __init__(self, n):
        pts = sorted((h(f"partition-{p}-vnode-{v}"), p) for p in range(n) for v in range(VNODES))
        self.keys = [k for k, _ in pts]
        self.owner = [p for _, p in pts]

    def __call__(self, word, n=None):
        i = bisect_left(self.keys, h(word)) % len(self.keys)
        return self.owner[i]


def main():
    ws = words(200_000)
    rings = {5: Ring(5), 6: Ring(6)}
    strategies = [("range", by_range), ("hash mod n", by_hash),
                  ("consistent hashing", lambda w, n: rings[n](w))]
    print(f"{len(ws):,} words; ideal per partition: {len(ws) // 5:,} (5 partitions), {len(ws) // 6:,} (6)\n")
    for name, f in strategies:
        a5 = [f(w, 5) for w in ws]
        a6 = [f(w, 6) for w in ws]
        c5 = [a5.count(p) for p in range(5)]
        c6 = [a6.count(p) for p in range(6)]
        stay = sum(x == y for x, y in zip(a5, a6))
        print(f"{name}")
        print(f"  5 partitions: {', '.join(f'{c:,}' for c in c5)}  (std dev {pstdev(c5):,.0f})")
        print(f"  6 partitions: {', '.join(f'{c:,}' for c in c6)}  (std dev {pstdev(c6):,.0f})")
        print(f"  5 -> 6: {stay:,} stay ({stay / len(ws):.1%}), {len(ws) - stay:,} relocate ({1 - stay / len(ws):.1%})\n")


if __name__ == "__main__":
    main()
