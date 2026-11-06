# A persistent vector in Python

A list stored as a tree of tuples whose nodes hold up to *b* elements or children. Updating one element copies only the path from the root to that leaf. The script counts the nodes and slots copied per update for branching factors 2 to 64, prints the book's depth bounds, and measures the memory kept by 1,001 versions, all against copying a 100,000-element list.

*Illustrates Data-Oriented Programming, chapter 9, section 9.2, pp. 178–183: path copying, depth log₂ N versus log₃₂ N, and the 10-billion-element bound. The implementation is the vault's: a fixed-size vector without the tail optimizations of production libraries (seeded).*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 persistent_vector.py
```

## Expected output

```text
Updating one element of a 100,000-element list
        strategy  depth  nodes copied  slots copied
 copy whole list      -             1       100,000
  path copy, b=2     17            17            34
  path copy, b=4      9             9            34
  path copy, b=8      6             6            44
 path copy, b=16      5             5            66
 path copy, b=32      4             4           100
 path copy, b=64      3             3           153

Depth bounds from the book (p. 182): log2 and log32 of the collection size
  N =          1,000   log2 N =  9.97   log32 N = 1.99
  N =        100,000   log2 N = 16.61   log32 N = 3.32
  N =     10,000,000   log2 N = 23.25   log32 N = 4.65
  N = 10,000,000,000   log2 N = 33.22   log32 N = 6.64

Memory kept by 1,001 versions (1,000 random single-element updates), N = 100,000
        strategy     slots kept  vs one version
 copy whole list    100,100,000           1001x
  path copy, b=2        233,953           1.17x
 path copy, b=32        202,539           1.96x
```

## What to look for

- The depth falls from 17 levels at *b* = 2 to 4 at *b* = 32. That's the log₂ versus log₃₂ the book computes, rounded up.
- Slots copied per update grow with *b* (34 at *b* = 2, 100 at *b* = 32), against 100,000 for a full copy. The book picks 32 for the CPU: one 32-slot array is a pair of cache accesses, cheaper than chasing 17 nodes.
- The book's numbers: log₃₂ of ten billion is 6.64, which it calls effectively constant.
- A thousand versions keep about twice the slots of one version at *b* = 32, and a thousand times as many with full copies.

## Related

- Chapter note: [9. Persistent data structures](../../chapters/09-persistent-data-structures.md) — section 9.2, pp. 178–183
