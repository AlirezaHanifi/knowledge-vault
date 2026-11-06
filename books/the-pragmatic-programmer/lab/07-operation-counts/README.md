# Counting the orders

Test your estimates: run the code at several sizes and look at the shape. Instead of timing, which is noisy, this script counts comparisons for linear search (a miss), binary search, insertion sort on random and on sorted input, and merge sort, at n = 250 to 4,000. It then fits the growth exponent as the slope of log(count) against log(n).

*Illustrates The Pragmatic Programmer, Topic 39, Algorithm Speed, pp. 343–351 (Tips 63–64): estimate the order of your algorithms, then test the estimates by varying the input size, and use profilers to count steps rather than time. The algorithms, sizes and fitting are the vault's (seeded).*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 operation_counts.py
```

## Expected output

```text
Comparisons counted at each n; the exponent is the slope of log(count) against log(n)

algorithm                            250       500     1,000     2,000     4,000  exponent  expected
linear search (miss)                 250       500     1,000     2,000     4,000      1.00  O(n): 1
binary search                          7         8         9        10        12      0.19  O(lg n): ~0
insertion sort                    17,275    63,069   257,207   993,148 4,070,638      1.97  O(n^2): 2
insertion sort (sorted input)        249       499       999     1,999     3,999      1.00  best case: 1
merge sort                         1,672     3,845     8,672    19,406    42,847      1.17  O(n lg n): just over 1

Doubling n doubles a linear count, quadruples a quadratic one, and adds about one comparison to binary search.
```

## What to look for

- Linear search has a slope of exactly 1, and insertion sort on random input almost exactly 2: doubling n quadruples the work.
- Binary search adds about one comparison per doubling. Its slope near 0 is the log–log signature of O(lg n).
- Merge sort's slope is a little above 1, the signature of O(n lg n) over this range.
- Insertion sort on already-sorted input is linear. The book's warning cuts both ways: an algorithm's behaviour can change with the order of its input, not just its size.

## Related

- Chapter note: [7. While You Are Coding](../../chapters/07-while-you-are-coding.md) — Topic 39, Algorithm Speed, pp. 343–351
