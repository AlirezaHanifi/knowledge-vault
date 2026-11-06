# Bloom filter false positives

How large should a Bloom filter be, and how many hash functions should it use? This experiment inserts 20,000 keys into filters of 4, 8, 10 and 16 bits per key with several numbers of hash functions. It probes 100,000 keys that were never inserted, counts the false positives, and compares the count with the standard estimate (1 − e^(−kn/m))^k.

*Illustrates Database Internals, “Bloom Filters”, pp. 146–147: false positives are possible and false negatives are not, and more bits and well-chosen hash functions lower the false-positive rate. The formula, the double-hashing scheme and the sizes are the vault's.*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 bloom_filter.py
```

## Expected output

```text
20,000 keys inserted, 100,000 absent keys probed; no false negatives found

bits/key   k  measured   formula
       4   1   22.247%   22.120%
       4   2   15.782%   15.482%
       4   3   14.765%   14.689%  <- k = (m/n) ln 2
       4   6   22.076%   21.983%
       8   1   11.820%   11.750%
       8   2    4.953%    4.893%
       8   6    2.139%    2.158%  <- k = (m/n) ln 2
       8   9    2.835%    2.922%
      10   1    9.592%    9.516%
      10   2    3.318%    3.286%
      10   7    0.785%    0.819%  <- k = (m/n) ln 2
      10  10    1.031%    1.019%
      16   1    6.090%    6.059%
      16   2    1.335%    1.381%
      16  11    0.049%    0.046%  <- k = (m/n) ln 2
      16  14    0.063%    0.053%
```

## What to look for

- Measured rates match the formula to within a few hundredths of a percent.
- More hash functions help only up to k ≈ (m/n)·ln 2. Past that, each key sets too many bits and the rate rises again.
- About 10 bits per key with 7 hash functions gives under 1% false positives, a common default in LSM-based stores.
- No present key is ever reported absent: a filter can only produce false positives.

## Related

- Chapter note: [7. Log-Structured Storage](../../chapters/07-log-structured-storage.md) — “Bloom Filters”, pp. 146–147
