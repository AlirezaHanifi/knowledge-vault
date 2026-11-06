# Saboteurs: do the tests catch planted bugs?

To test the tests, plant bugs and see whether the tests notice. The script generates eight mutants of a small `clamp(x, lo, hi)` function. It detects the ones that behave exactly like the original (equivalent mutants), and runs the rest against a weak suite (one happy-path test) and a strong suite (seven tests, including just outside both boundaries). Then it samples the book's `a / (a + b)` state space with up to a million random tests.

*Illustrates The Pragmatic Programmer, “Testing the Tests” and “Testing Thoroughly” in Topic 51, Pragmatic Starter Kit, pp. 457–458 (Tips 92–93). The clamp function, mutants and tests are the vault's; the a / (a + b) function with a and b from 0 to 999 is the book's. The first failing test is drawn from a geometric distribution rather than drawing a million pairs one by one.*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 saboteurs.py
```

## Expected output

```text
Mutants of clamp(x, lo, hi), run against a weak suite (1 test) and a strong suite (7 tests)

mutant                                weak    strong
< becomes <=                    (equivalent: same behaviour)
> becomes >=                    (equivalent: same behaviour)
return lo becomes return hi       SURVIVES    caught
return hi becomes return lo       SURVIVES    caught
x < lo becomes x < hi               caught    caught
x > hi becomes x > hi + 1         SURVIVES    caught
x < lo becomes x < lo - 1         SURVIVES    caught
return x becomes return x + 1       caught    caught

mutation score: weak 2/6, strong 6/6

State coverage: test(a, b) = a / (a + b) for a, b in 0..999 (1,000,000 states, one fails)

random tests  line coverage    runs (of 100) that hit a = b = 0
         100           100%                                   0
      10,000           100%                                   3
   1,000,000           100%                                  63

The chance of finding the state with k random tests is 1 - (1 - 1e-6)^k: about 63% at a million.
```

## What to look for

- Two of the eight mutants are equivalent (< becoming <= changes nothing at the boundary of clamp): no test could ever catch them.
- The one-test suite lets four of the six real bugs survive, though it passes and runs the main path.
- The strong suite catches all six; the off-by-one mutants that move a boundary are caught only by the tests just outside it (11 and −1).
- A hundred random tests of `a / (a + b)` give 100% line coverage and almost never find the one failing state. Even a million find it only about 63% of the time: test state coverage, not code coverage.

## Related

- Chapter note: [9. Pragmatic Projects](../../chapters/09-pragmatic-projects.md) — “Testing the Tests” and “Testing Thoroughly”, pp. 457–458
