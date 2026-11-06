# Properties find the warehouse bug

The book's `Warehouse` passes its hand-written unit tests. This script builds a tiny property-based tester with the standard library: it generates orders (item from shoes or hats, quantity 1–4, as in the book), checks that stock taken plus stock left equals the original stock, and greedily shrinks any failure toward the first item and smaller quantities. It runs the property against the buggy `in_stock(item)` and the fixed `in_stock(item, quantity)`, and also with quantities up to 20.

*Illustrates The Pragmatic Programmer, “Finding Bad Assumptions” in Topic 42, Property-Based Testing, pp. 378–383: the Warehouse, `order`, the property and the fix follow the book (`proptest/stock.py` and `stock1.py`). The generator and shrinker are the vault's; the book uses Hypothesis.*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 warehouse_properties.py
```

## Expected output

```text
== buggy in_stock(item)
   hand-written unit tests: pass
   quantity 1-4  seed 1: FAIL after   3 case(s): hats, 4 -> shrunk to hats, 3 in 7 step(s): Exception: Oversold hats
   quantity 1-4  seed 2: FAIL after   6 case(s): hats, 4 -> shrunk to hats, 3 in 7 step(s): Exception: Oversold hats
   quantity 1-4  seed 3: FAIL after   2 case(s): hats, 4 -> shrunk to hats, 3 in 7 step(s): Exception: Oversold hats
   quantity 1-20 seed 1: FAIL after   1 case(s): shoes, 19 -> shrunk to shoes, 11 in 21 step(s): Exception: Oversold shoes
   quantity 1-20 seed 2: FAIL after   2 case(s): shoes, 12 -> shrunk to shoes, 11 in 21 step(s): Exception: Oversold shoes
   quantity 1-20 seed 3: FAIL after   1 case(s): shoes, 19 -> shrunk to shoes, 11 in 21 step(s): Exception: Oversold shoes

== fixed in_stock(item, qty)
   hand-written unit tests: pass
   quantity 1-4  seed 1: pass (100 cases)
   quantity 1-4  seed 2: pass (100 cases)
   quantity 1-4  seed 3: pass (100 cases)
   quantity 1-20 seed 1: pass (100 cases)
   quantity 1-20 seed 2: pass (100 cases)
   quantity 1-20 seed 3: pass (100 cases)
```

## What to look for

- The unit tests pass for both versions: they only ever order one hat.
- With the book's strategy, every seed fails within a few cases and shrinks to `hats, 3`, the book's falsifying example: there are 2 hats, and `in_stock` only checked for at least one.
- With quantities up to 20 the shrinker lands on `shoes, 11` instead: a different minimal failure of the same bug. The input strategy decides which counterexample you see.
- The fixed version passes every run, so turn `hats, 3` into a regular unit test, as the book advises, to keep the bug from coming back.

## Related

- Chapter note: [7. While You Are Coding](../../chapters/07-while-you-are-coding.md) — Topic 42, Property-Based Testing, pp. 378–383
