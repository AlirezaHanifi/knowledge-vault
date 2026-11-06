# Three-way merge in Python

A port of the chapter's commit phase: the structural `diff`, `informationPaths`, `havePathInCommon`, the merge and `reconcile`. It replays the tiny library of listings 5.6–5.7: one mutation changes Watchmen's publication year, the other its title and an author's name. Then it shows two pitfalls of the printed code. Finally it measures how often two concurrent mutations abort as they crowd onto fewer fields.

*Illustrates Data-Oriented Programming, chapter 5, sections 5.2–5.5, pp. 94–108 (listings 5.4–5.16). The abort experiment, with one random field per mutation, is the vault's (seeded).*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 three_way_merge.py
```

## Expected output

```text
diff(previous, next):    {"catalog": {"booksByIsbn": {"978-1779501127": {"publicationYear": 1986}}}}
diff(previous, current): {"catalog": {"booksByIsbn": {"978-1779501127": {"title": "The Watchmen"}}, "authorsById": {"dave-gibbons": {"name": "David Chester Gibbons"}}}}
paths of next's diff:    [['catalog', 'booksByIsbn', '978-1779501127', 'publicationYear']]
paths of current's diff: [['catalog', 'booksByIsbn', '978-1779501127', 'title'], ['catalog', 'authorsById', 'dave-gibbons', 'name']]
table 5.4, array addition: diff([1], [1, 2]) = [null, 2]

reconcile(current, previous, next), condition fixed:
{
 "catalog": {
  "booksByIsbn": {
   "978-1779501127": {
    "isbn": "978-1779501127",
    "title": "The Watchmen",
    "publicationYear": 1986,
    "authorIds": [
     "alan-moore",
     "dave-gibbons"
    ]
   }
  },
  "authorsById": {
   "alan-moore": {
    "name": "Alan Moore",
    "bookIsbns": [
     "978-1779501127"
    ]
   },
   "dave-gibbons": {
    "name": "David Chester Gibbons",
    "bookIsbns": [
     "978-1779501127"
    ]
   }
  }
 }
}

Fast-forward when nothing else committed: True
Listing 5.16 as printed, on these NON-conflicting mutations: Conflicting concurrent mutations.
Both set publicationYear, paths compared by value: Conflicting concurrent mutations.
Both set publicationYear, paths compared by identity: merged silently, year = 1986 (1988 lost)

Two concurrent mutations, each setting one random field out of F (1,000 trials each)
   F  aborted  abort rate
   1     1000     100.0%
   2      484      48.4%
   4      263      26.3%
   8      119      11.9%
  16       63       6.3%
  64       17       1.7%
```

## What to look for

- With the code as listed, the name change sits under `catalog`, so the merged result has a single `catalog` with all three changes. That differs from the printed output of listing 5.14 (see the vault note in the lesson).
- `diff([1], [1, 2])` gives `[null, 2]`, as in table 5.4: equal elements become null.
- Listing 5.16 as printed throws *Conflicting concurrent mutations* on the book's own non-conflicting example, because its condition is inverted.
- Comparing paths by identity, as Lodash's `_.intersection` does for arrays, never finds a common path. Two mutations of the same year then merge silently, and one of them is lost.
- With one random field each, the abort rate is about 1/F. Optimistic concurrency pays off when mutations rarely touch the same fields.

## Related

- Chapter note: [5. Basic concurrency control](../../chapters/05-basic-concurrency-control.md) — sections 5.2–5.5, pp. 94–108
