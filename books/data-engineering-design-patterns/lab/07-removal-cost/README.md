# Cost of a personal-data removal

When a user asks to be forgotten, how much has to be rewritten? This experiment builds a synthetic visits dataset with 90 daily partitions of 4 files each, plus one heavy user with the book's 2,000 visits. It compares two approaches. The **In-Place Overwriter** rewrites every file that holds one of the user's rows. With the **Vertical Partitioner**, the user's personal attributes are stored once in a separate user-context table. It then compares processing 100 removal requests one at a time with batching them into one run.

*Illustrates Data Engineering Design Patterns, “Pattern: Vertical Partitioner” and “Pattern: In-Place Overwriter”, pp. 198–207. The cost consequence, 2,000 records against one and batching removal requests, is on p. 205. The data layout is synthetic; the implementation is the vault’s own.*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 removal_cost.py
```

## Expected output

```text
Visits dataset: 296,580 rows in 360 files (90 days x 4 files)
User context table (Vertical Partitioner): 5,000 rows in 20 files

Removing user 0 (2,000 visits)
                          rows deleted  files rewritten  rows rewritten  MB written
  In-Place Overwriter            2,000              360         296,580       88.97
  Vertical Partitioner               1                1             250        0.03

A median user (25 visits) still makes the In-Place Overwriter rewrite 25 files (21,012 rows)

100 removal requests, In-Place Overwriter
  processed one by one:   3,204,008 rows rewritten
  batched into one run:   296,580 rows rewritten (10.8x less)
```

## What to look for

- The heavy user's 2,000 visits are spread over every file, so the In-Place Overwriter rewrites the entire dataset to delete them.
- The Vertical Partitioner deletes one row and rewrites one small file. The visits table keeps only `user_id`, which no longer links to anything personal.
- Even a median user touches dozens of files, because visits are spread across days.
- Batching removal requests, as the book recommends, rewrites each file once instead of once per request.

## Related

- Chapter note: [7. Data Security Design Patterns](../../chapters/07-data-security-design-patterns.md) — “Data Removal”, pp. 198–207
