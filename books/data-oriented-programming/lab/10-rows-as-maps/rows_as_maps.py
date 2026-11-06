"""Rows as maps with SQLite: DOP chapter 10 (pp. 198-218).

Loads tables 10.1-10.3 into an in-memory SQLite database, fetches rows as
dictionaries (the driver step of figure 10.2), validates them against a schema,
renames keys generically (listing 10.14) and aggregates the join of listing 10.17
with groupBy and aggregateField (listings 10.20-10.26).
Standard library only (sqlite3); no randomness.
"""
import json
import sqlite3

db = sqlite3.connect(":memory:")
db.row_factory = lambda cur, row: {c[0]: v for c, v in zip(cur.description, row)}   # rows as maps
db.executescript("""
CREATE TABLE books (title VARCHAR, isbn VARCHAR PRIMARY KEY, publication_year INTEGER);
CREATE TABLE authors (id VARCHAR PRIMARY KEY, name VARCHAR);
CREATE TABLE book_authors (book_isbn VARCHAR, author_id VARCHAR);
INSERT INTO books VALUES ('The Power of Habit', '978-0812981605', 2012),
                         ('7 Habits of Highly Effective People', '978-1982137274', 1989);
INSERT INTO authors VALUES ('sean-covey', 'Sean Covey'), ('stephen-covey', 'Stephen Covey'), ('charles-duhigg', 'Charles Duhigg');
INSERT INTO book_authors VALUES ('978-1982137274', 'sean-covey'), ('978-1982137274', 'stephen-covey'), ('978-0812981605', 'charles-duhigg');
""")


def validate_rows(rows, required, types):
    """dbSearchResultSchema (listing 10.4): an array of maps with required, typed fields."""
    errs = []
    for i, r in enumerate(rows):
        errs += [f"data/{i} must have required property '{k}'" for k in required if k not in r]
        errs += [f"data/{i}/{k} must be {t.__name__}" for k, t in types.items() if k in r and not isinstance(r[k], t)]
    return errs


SCHEMA = (["title", "isbn", "publication_year"], {"title": str, "isbn": str, "publication_year": int})

print("1. The query of listing 10.6, as printed: '%$1%' inside the quotes")
try:
    db.execute("SELECT title, isbn FROM books WHERE title LIKE '%?%'", ["habit"]).fetchall()
except sqlite3.ProgrammingError as e:
    print("   ", type(e).__name__ + ":", e)
print("   (inside a quoted literal the placeholder is just text)")
print()
print("2. Corrected: LIKE '%' || ? || '%', still selecting only title and isbn")
rows = db.execute("SELECT title, isbn FROM books WHERE title LIKE '%' || ? || '%'", ["habit"]).fetchall()
print("   rows:", json.dumps(rows))
print("   validation:", validate_rows(rows, *SCHEMA) or "valid")
print()
print("3. Selecting publication_year too, as the schema requires")
rows = db.execute("SELECT title, isbn, publication_year FROM books WHERE title LIKE '%' || ? || '%'", ["habit"]).fetchall()
print("   rows:", json.dumps(rows))
print("   validation:", validate_rows(rows, *SCHEMA) or "valid")
print("   JSON (late binding: the year is written without quotes):", json.dumps(rows[0]))
db.execute("PRAGMA case_sensitive_like = ON")
cs = db.execute("SELECT title FROM books WHERE title LIKE '%' || ? || '%'", ["habit"]).fetchall()
db.execute("PRAGMA case_sensitive_like = OFF")
print("   with a case-sensitive LIKE, as in PostgreSQL:", len(cs), "rows")
print()


def rename_keys(m, key_map):
    """Listing 10.14: reduce over the key map; set the new key, omit the old one."""
    res = m
    for old, new in key_map.items():
        res = {**{k: v for k, v in res.items() if k != old}, new: res.get(old)}
    return res


def rename_result_keys(results, key_map):
    return [rename_keys(r, key_map) for r in results]


print("4. renameResultKeys, the same function for books and users (listings 10.13-10.16)")
print("  ", json.dumps(rename_result_keys(rows, {"title": "bookTitle", "publication_year": "publicationYear"})))
users = [{"email": "jennie@gmail.com", "encryptedPassword": "secret-pass"}, {"email": "franck@hotmail.com", "encryptedPassword": "my-secret"}]
print("  ", json.dumps(rename_result_keys(users, {"email": "userEmail"})))
print()


def group_by(rows, field):
    out = {}
    for r in rows:
        out.setdefault(r[field], []).append(r)
    return out


def aggregate_field(rows, field, agg):
    """Listing 10.23: first row as the basis, the field's values as a list, the field omitted."""
    base = {k: v for k, v in rows[0].items() if k != field}
    return {**base, agg: [r[field] for r in rows]}


def aggregate_fields(rows, id_field, field, agg):
    """Listing 10.26."""
    return [aggregate_field(g, field, agg) for g in group_by(rows, id_field).values()]


print("5. The join of listing 10.17, then aggregateFields (figure 10.3)")
sql_rows = db.execute("""SELECT title, isbn, authors.name AS author_name FROM books
  INNER JOIN book_authors ON books.isbn = book_authors.book_isbn
  INNER JOIN authors ON book_authors.author_id = authors.id
  WHERE books.title LIKE '%' || ? || '%' ORDER BY isbn, author_name""", ["habit"]).fetchall()
print(f"   {len(sql_rows)} rows:")
for r in sql_rows:
    print("    ", json.dumps(r))
books = aggregate_fields(sql_rows, "isbn", "author_name", "authorNames")
print(f"   {len(books)} books:")
for b in books:
    print("    ", json.dumps(b))
