# B-Tree height vs fanout

How many pages does a lookup read, and how many comparisons does it make, as nodes get bigger? This experiment bulk-loads a B⁺-Tree of one million keys at several node capacities, either completely full or about 69% full, which is a common estimate of average occupancy under random inserts. It then runs 2,000 random lookups and counts page reads and binary-search comparisons. It ends with the book's 4-billion-key example.

*Illustrates Database Internals, “B-Tree Lookup Complexity”, pp. 37–38: a lookup reads log_N(M) pages and does log₂(M) comparisons. The 69% fill level and the bulk-loading build are the vault's; so is the implementation.*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 btree_height.py
```

## Expected output

```text
1,000,000 keys; 2,000 random lookups per tree

capacity  fill  height  pages/lookup  comparisons
       4  100%      10          10.0         21.0
       4   69%      20          20.0         21.0
      16  100%       5           5.0         21.0
      16   69%       6           6.0         22.9
      64  100%       4           4.0         21.0
      64   69%       4           4.0         22.0
     256  100%       3           3.0         21.0
     256   69%       3           3.0         22.0
     500  100%       3           3.0         20.0
     500   69%       3           3.0         21.9

log2(1,000,000) = 19.9 comparisons, whatever the fanout
Book's example, 4 billion keys:
  fanout   2: ceil(log_2(4e9)) = 32 page reads
  fanout 100: ceil(log_100(4e9)) = 5 page reads
  fanout 500: ceil(log_500(4e9)) = 4 page reads
```

## What to look for

- Height, and so page reads per lookup, falls quickly with fanout: from 10 levels at capacity 4 to 3 levels at 256 or 500.
- Comparisons barely change (about 20–23). Binary search inside each node adds up to log₂(M) whatever the fanout, so high fanout saves disk reads, not CPU work.
- Half-full nodes cost an extra level only at small fanouts. At high fanout, the tree's height barely notices occupancy.
- The book's numbers: 4 billion keys need 32 comparisons, and only 4 page reads at fanout 500.

## Related

- Chapter note: [2. B-Tree Basics](../../chapters/02-b-tree-basics.md) — “B-Tree Lookup Complexity”, pp. 37–38
