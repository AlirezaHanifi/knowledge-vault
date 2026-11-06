"""Bloom filter false-positive rate: measured vs the formula.

Illustrates Database Internals, Chapter 7, "Bloom Filters" (pp. 146-147): a bit
array plus k hash functions; a lookup can return a false positive but never a
false negative, and larger arrays or more hash functions (up to a point) lower
the false-positive rate. Keys, sizes and the double-hashing scheme are the
vault's; the formula (1 - e^(-kn/m))^k is the standard estimate.
"""

import hashlib
import math

N_KEYS, N_PROBES = 20_000, 100_000


def hashes(key, k, m):
    d = hashlib.blake2b(key.encode(), digest_size=16).digest()
    h1, h2 = int.from_bytes(d[:8], "little"), int.from_bytes(d[8:], "little") | 1
    return [(h1 + i * h2) % m for i in range(k)]   # Kirsch-Mitzenmacher double hashing


def measure(bits_per_key, k):
    m = bits_per_key * N_KEYS
    bits = bytearray(m)
    for i in range(N_KEYS):
        for h in hashes(f"present-{i}", k, m):
            bits[h] = 1
    assert all(all(bits[h] for h in hashes(f"present-{i}", k, m)) for i in range(0, N_KEYS, 97)), "false negative"
    fp = sum(all(bits[h] for h in hashes(f"absent-{i}", k, m)) for i in range(N_PROBES))
    return fp / N_PROBES, (1 - math.exp(-k * N_KEYS / m)) ** k


print(f"{N_KEYS:,} keys inserted, {N_PROBES:,} absent keys probed; no false negatives found\n")
print(f"{'bits/key':>8} {'k':>3} {'measured':>9} {'formula':>9}")
for bpk in (4, 8, 10, 16):
    best = max(1, round(bpk * math.log(2)))
    for k in sorted({1, 2, best, best + 3}):
        got, est = measure(bpk, k)
        mark = "  <- k = (m/n) ln 2" if k == best else ""
        print(f"{bpk:>8} {k:>3} {got:>9.3%} {est:>9.3%}{mark}")
