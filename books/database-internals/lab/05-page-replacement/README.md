# Page-replacement hit ratios

Which eviction policy keeps a buffer pool most useful? This experiment replays a page-reference trace shaped like a B-Tree workload. Every lookup touches the root, one internal page and one leaf, and leaf popularity is skewed. Halfway through, one full scan reads every leaf once. The trace runs under FIFO, LRU, CLOCK and LFU at four cache sizes. The experiment also replays the classic reference string that shows Bélády's anomaly.

*Illustrates Database Internals, “Page Replacement”, pp. 85–88 (FIFO and LRU, CLOCK, LFU and TinyLFU). The trace, its skew and the cache sizes are the vault's (seeded); so is the implementation. Bélády's reference string is the standard textbook example.*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 page_replacement.py
```

## Expected output

```text
Trace: 30,000 lookups (root, internal, leaf) + one 4,000-leaf scan = 94,001 page references

cache pages     FIFO      LRU    CLOCK      LFU   (hit ratio)
         32    45.9%    49.4%    48.4%    62.0%
        128    65.2%    71.5%    69.8%    78.1%
        512    78.6%    81.2%    80.8%    84.4%
       1024    83.6%    85.3%    85.0%    87.7%

Bélády's anomaly, reference string 1 2 3 4 1 2 5 1 2 3 4 5
  FIFO with 3 frames: 9 faults   LRU: 10 faults
  FIFO with 4 frames: 10 faults   LRU: 8 faults
```

## What to look for

- FIFO evicts the root and internal pages even though every lookup needs them, so it has the lowest hit ratio at every size.
- CLOCK stays within about two points of LRU while needing only a reference bit per frame, which is why it's used as a cheaper LRU approximation.
- LFU wins on this trace: frequency protects hot pages from the one-off scan, which pushes them out of LRU's recency order.
- Bélády's anomaly: FIFO has *more* faults with 4 frames than with 3 (10 against 9). LRU can't do that, because it is a stack algorithm.

## Related

- Chapter note: [5. Transaction Processing and Recovery](../../chapters/05-transaction-processing-and-recovery.md) — “Buffer Management”, pp. 81–88
