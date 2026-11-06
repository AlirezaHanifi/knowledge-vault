# Schema-based unit tests

Generates random catalogs that conform to the catalog schema, a small stand-in for JSON Schema Faker. Each test searches by the first letter of the first book's title and lets the function's return-value validation decide pass or fail. The script runs 1,000 seeds with the search as printed, then with Dave's `"Not available"` fix.

*Illustrates Data-Oriented Programming, chapter 12, section 12.5, pp. 262–268 (figure 12.3; listings 12.10 and 12.21–12.28). The generator, its word list and the number of books and authors are the vault's (seeded).*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 schema_based_tests.py
```

## Expected output

```text
First five seeds, as printed (listing 12.1):
  seed 1: false searchBooksByTitle returned an invalid value: data/0/authorNames/0 must be string
  seed 2: false searchBooksByTitle returned an invalid value: data/0/authorNames/0 must be string
  seed 3: false searchBooksByTitle returned an invalid value: data/1/authorNames/0 must be string
  seed 4: false searchBooksByTitle returned an invalid value: data/1/authorNames/0 must be string
  seed 5: false searchBooksByTitle returned an invalid value: data/0/authorNames/0 must be string

Seeds 1-1000, as printed: 134 passed, 866 failed (86.6%)
Seeds 1-1000, with "Not available" (listing 12.28): 1000 passed, 0 failed (0.0%)

Why some unfixed runs pass:
  matching books cite no author at all: 134
  matching books cite only authors that exist: 0
```

## What to look for

- Most runs fail with `authorNames/… must be string`. Random author IDs in books and random keys in `authorsById` almost never line up, so the names are missing. That's the bug the book's test found.
- The runs that pass are lucky: every one of them is a case where the matching books cite no author at all. None passes because a random author happens to exist.
- With the fix, a missing author is the string `"Not available"`, and all 1,000 runs pass.
- There is no explicit assertion: the function's own dev-mode check throws, and the test turns that into `false`.

## Related

- Chapter note: [12. Advanced data validation](../../chapters/12-advanced-data-validation.md) — section 12.5, pp. 262–268
