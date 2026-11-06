# Joining sources by key

Double field filtering with `pick`, `keyBy` and the generic `joinArrays`, run against a mocked Open Library, so no network is needed. The script filters a record with the printed and the corrected relevant fields, joins the test data of listing 11.19 while reporting conflicts, runs the enrichment join on the mock, and shows that the join is an outer join.

*Illustrates Data-Oriented Programming, chapter 11, pp. 229–239 (listings 11.9 and 11.16–11.19). The mock's 7 Habits record uses fields from listing 11.6, and The Power of Habit's uses those of listing 11.19. Its `isbn_13` and the extra ISBNs in step 5 are the vault's.*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 join_arrays.py
```

## Expected output

```text
1. Double field filtering of 7 Habits, requested: ['title', 'publishers', 'number_of_pages', 'revision']
   relevantFields as printed: {"title": "7 Habits of Highly Effective People : Revised and Updated", "number_of_pages": 432, "isbn": "978-1982137274"}
   with "publishers":        {"title": "7 Habits of Highly Effective People : Revised and Updated", "publishers": ["Simon & Schuster, Incorporated"], "number_of_pages": 432, "isbn": "978-1982137274"}
   ('revision' is requested but not relevant, so the server never exposes it)

2. keyBy keeps the last element per key
   {"a": {"isbn": "a", "n": 3}, "b": {"isbn": "b", "n": 2}}

3. The test data of listing 11.19 (each Open Library record carries the other book's title)
   {"available": true, "isbn": "978-1982137274", "subjects": ["Social aspects", "Habit", "Change (Psychology)"], "subtitle": "Why We Do What We Do in Life and Business", "title": "The Power of Habit"}
   {"available": false, "isbn": "978-0812981605", "number_of_pages": 432, "subtitle": "Powerful Lessons in Personal Change", "title": "7 Habits of Highly Effective People"}
   conflicts (Open Library wins silently):
     978-0812981605 title: database 'The Power of Habit' vs Open Library '7 Habits of Highly Effective People'
     978-1982137274 title: database '7 Habits of Highly Effective People' vs Open Library 'The Power of Habit'

4. The enrichment flow with the mock: database rows joined with filtered Open Library records
   {"available": true, "isbn": "978-1982137274", "number_of_pages": 432, "subtitle": "Powerful Lessons in Personal Change", "title": "7 Habits of Highly Effective People : Revised and Updated"}
   {"available": false, "isbn": "978-0812981605", "subtitle": "Why We Do What We Do in Life and Business", "title": "The Power of Habit"}
   conflicts: none (the database contributes only isbn and available)

5. An outer join: a database book with no Open Library record, and vice versa
   {"available": true, "isbn": "978-1982137274", "number_of_pages": 432, "subtitle": "Powerful Lessons in Personal Change", "title": "7 Habits of Highly Effective People : Revised and Updated"}
   {"available": false, "isbn": "978-0812981605", "subtitle": "Why We Do What We Do in Life and Business", "title": "The Power of Habit"}
   {"available": true, "isbn": "978-0000000001"}
   {"isbn": "978-0000000002", "title": "Only in Open Library"}
```

## What to look for

- `relevantFields` lists `publisher`, but the API returns `publishers`, so as printed the publishers never reach the client.
- A field that is requested but not relevant (`revision`) is dropped: the first filter is the server's whitelist.
- In listing 11.19 each Open Library record carries the other book's title, and the merge lets Open Library win silently. That's the conflict merging was supposed to avoid (see the vault note in the lesson).
- With the database contributing only `isbn` and `available`, as in the enrichment flow, there is nothing to conflict.
- Books present on only one side still appear: keying both arrays and merging the maps is an outer join.

## Related

- Chapter note: [11. Web services](../../chapters/11-web-services.md) — sections 11.4–11.6, pp. 229–239
