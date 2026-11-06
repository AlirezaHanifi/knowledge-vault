# Range, hash and consistent hashing

How evenly does each assignment strategy spread items, and how many move when five partitions become six? Following the shape of the book's experiment, this script assigns 200,000 words to partitions by first-letter range (the book's letter groups), by `hash mod n`, and by a consistent-hashing ring with 100 virtual nodes per partition. It prints per-partition counts and their standard deviation, then the share of words that stay put on 5 → 6.

*Illustrates Think Distributed Systems, Listings 7.3–7.9 and Table 7.2, pp. 99–103. The book used `/usr/share/dict/words` (235,976 words) and the `uhashring` package; this script generates words with an approximate English first-letter distribution (seeded) and builds its own ring with MD5. The counts differ from the book's; the pattern doesn't.*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 assignment_strategies.py
```

## Expected output

```text
200,000 words; ideal per partition: 40,000 (5 partitions), 33,333 (6)

range
  5 partitions: 60,217, 31,341, 32,918, 60,212, 15,312  (std dev 17,618)
  6 partitions: 52,227, 29,940, 17,872, 42,498, 42,151, 15,312  (std dev 13,503)
  5 -> 6: 100,719 stay (50.4%), 99,281 relocate (49.6%)

hash mod n
  5 partitions: 40,097, 39,792, 39,885, 40,232, 39,994  (std dev 155)
  6 partitions: 33,124, 33,287, 33,335, 33,335, 33,360, 33,559  (std dev 128)
  5 -> 6: 33,553 stay (16.8%), 166,447 relocate (83.2%)

consistent hashing
  5 partitions: 43,792, 40,276, 37,992, 41,569, 36,371  (std dev 2,612)
  6 partitions: 37,987, 30,267, 29,524, 38,033, 31,833, 32,356  (std dev 3,437)
  5 -> 6: 167,644 stay (83.8%), 32,356 relocate (16.2%)
```

## What to look for

- Range partitioning follows the language: the a–e and p–t partitions get four times as many words as u–z.
- `hash mod n` is almost perfectly even, but only about 1 in 6 words keeps its partition on 5 → 6 (16.8% here, 16.7% in the book).
- Consistent hashing keeps about 84% of words in place, so only about n/m move (the book measured 81.5% staying), at the cost of a somewhat less even spread.
- Range relocation is about half here (51.4% in the book): moving letter boundaries moves every word whose first letter changes group.

## Related

- Chapter note: [7. Partitioning](../../chapters/07-partitioning.md) — “Repartitioning” and “Consistent hashing”, pp. 101–103
