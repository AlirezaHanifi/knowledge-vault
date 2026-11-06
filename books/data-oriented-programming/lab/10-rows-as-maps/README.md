# Rows as maps with SQLite

Loads tables 10.1–10.3 into an in-memory SQLite database, with a row factory that returns each row as a dictionary: the driver step of figure 10.2. It then runs the chapter's search as printed and corrected, and validates the rows against the schema. Last, it renames keys with one generic function for books and users, and aggregates the three-row join into two books.

*Illustrates Data-Oriented Programming, chapter 10, pp. 198–218 (listings 10.4–10.26). SQLite stands in for the book's PostgreSQL; the placeholder is `?` instead of `$1`.*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 rows_as_maps.py
```

## Expected output

```text
1. The query of listing 10.6, as printed: '%$1%' inside the quotes
    ProgrammingError: Incorrect number of bindings supplied. The current statement uses 0, and there are 1 supplied.
   (inside a quoted literal the placeholder is just text)

2. Corrected: LIKE '%' || ? || '%', still selecting only title and isbn
   rows: [{"title": "The Power of Habit", "isbn": "978-0812981605"}, {"title": "7 Habits of Highly Effective People", "isbn": "978-1982137274"}]
   validation: ["data/0 must have required property 'publication_year'", "data/1 must have required property 'publication_year'"]

3. Selecting publication_year too, as the schema requires
   rows: [{"title": "The Power of Habit", "isbn": "978-0812981605", "publication_year": 2012}, {"title": "7 Habits of Highly Effective People", "isbn": "978-1982137274", "publication_year": 1989}]
   validation: valid
   JSON (late binding: the year is written without quotes): {"title": "The Power of Habit", "isbn": "978-0812981605", "publication_year": 2012}
   with a case-sensitive LIKE, as in PostgreSQL: 0 rows

4. renameResultKeys, the same function for books and users (listings 10.13-10.16)
   [{"isbn": "978-0812981605", "bookTitle": "The Power of Habit", "publicationYear": 2012}, {"isbn": "978-1982137274", "bookTitle": "7 Habits of Highly Effective People", "publicationYear": 1989}]
   [{"encryptedPassword": "secret-pass", "userEmail": "jennie@gmail.com"}, {"encryptedPassword": "my-secret", "userEmail": "franck@hotmail.com"}]

5. The join of listing 10.17, then aggregateFields (figure 10.3)
   3 rows:
     {"title": "The Power of Habit", "isbn": "978-0812981605", "author_name": "Charles Duhigg"}
     {"title": "7 Habits of Highly Effective People", "isbn": "978-1982137274", "author_name": "Sean Covey"}
     {"title": "7 Habits of Highly Effective People", "isbn": "978-1982137274", "author_name": "Stephen Covey"}
   2 books:
     {"title": "The Power of Habit", "isbn": "978-0812981605", "authorNames": ["Charles Duhigg"]}
     {"title": "7 Habits of Highly Effective People", "isbn": "978-1982137274", "authorNames": ["Sean Covey", "Stephen Covey"]}
```

## What to look for

- A placeholder inside a quoted literal is just text: SQLite refuses the extra binding. In PostgreSQL, `'%$1%'` would silently search for the characters `$1`.
- Selecting only `title` and `isbn`, as listing 10.6 does, fails `dbSearchResultSchema`, which requires `publication_year` (see the vault note in the lesson).
- SQLite's `LIKE` ignores ASCII case, so `habit` finds both titles. With a case-sensitive `LIKE`, as in PostgreSQL, it finds none, and you'd need `ILIKE` there. This is the vault's observation: the book doesn't discuss case.
- The same `renameResultKeys` reshapes book rows and user rows.
- `aggregateFields` turns the three rows of the join into two books, the Coveys' names collected in one `authorNames` list.

## Related

- Chapter note: [10. Database operations](../../chapters/10-database-operations.md) — sections 10.1–10.4, pp. 198–218
