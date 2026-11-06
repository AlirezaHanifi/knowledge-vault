"""Schema-based unit tests: DOP chapter 12, section 12.5 (pp. 262-268).

Generates random catalogs that conform to the catalog schema (a small stand-in for
JSON Schema Faker), searches by the first letter of the first book's title (listing
12.24), and lets return-value validation decide pass or fail (listings 12.21-12.27).
Then applies Dave's "Not available" fix (listing 12.28) and reruns.
Standard library only; seeded.
"""
import random

WORDS = ["lorem", "ipsum", "dolor", "sit", "amet", "ullamco", "laboris", "nisi", "aliquip", "commodo",
         "consequat", "duis", "aute", "irure", "culpa", "officia", "deserunt", "mollit", "anim", "est"]


def generate_catalog(rnd):
    """Random data conforming to catalogSchema (listings 12.3-12.6): independent random IDs."""
    def key():
        return rnd.choice(WORDS) + str(rnd.randrange(100))

    def text():
        return " ".join(rnd.choice(WORDS) for _ in range(rnd.randint(1, 3)))

    books = {}
    for _ in range(rnd.randint(1, 4)):
        book = {"title": text(), "isbn": key(), "authorIds": [key() for _ in range(rnd.randint(0, 3))],
                "bookItems": [{"id": key(), "libId": key(), "purchaseDate": text(), "isLent": rnd.random() < .5}
                              for _ in range(rnd.randint(0, 2))]}
        if rnd.random() < .5:
            book["publicationYear"] = rnd.randint(1900, 2021)
        books[key()] = book
    authors = {key(): {"id": key(), "name": text(), "bookIsbns": [key() for _ in range(rnd.randint(0, 2))]}
               for _ in range(rnd.randint(0, 3))}
    return {"booksByIsbn": books, "authorsById": authors}


def valid_response(infos):
    """searchBooksResponseSchema (listing 12.10): title, isbn strings, authorNames an array of strings."""
    for i, b in enumerate(infos):
        for k in ("title", "isbn"):
            if not isinstance(b.get(k), str):
                return f"data/{i}/{k} must be string"
        for j, n in enumerate(b.get("authorNames", [])):
            if not isinstance(n, str):
                return f"data/{i}/authorNames/{j} must be string"
    return None


def search_books_by_title(catalog, query, fixed):
    """Listing 12.1 with the dev-mode return-value check of listing 12.11."""
    infos = [{"title": b["title"], "isbn": b["isbn"],
              "authorNames": [catalog["authorsById"].get(a, {}).get("name", "Not available" if fixed else None)
                              for a in b["authorIds"]]}
             for b in catalog["booksByIsbn"].values() if query in b["title"]]
    err = valid_response(infos)
    if err:
        raise ValueError("searchBooksByTitle returned an invalid value: " + err)
    return infos


def search_books_test(seed, fixed):
    """Listings 12.24-12.27: query = first letter of the first title; return true or false."""
    rnd = random.Random(seed)
    catalog = generate_catalog(rnd)
    query = next(iter(catalog["booksByIsbn"].values()))["title"][0]
    try:
        search_books_by_title(catalog, query, fixed)
        return True, None
    except ValueError as e:
        return False, str(e)


print("First five seeds, as printed (listing 12.1):")
for seed in range(1, 6):
    ok, err = search_books_test(seed, fixed=False)
    print(f"  seed {seed}: {str(ok).lower():5} {err or ''}")
print()
for fixed in (False, True):
    results = [search_books_test(seed, fixed) for seed in range(1, 1001)]
    failed = sum(1 for ok, _ in results if not ok)
    label = "with \"Not available\" (listing 12.28)" if fixed else "as printed"
    print(f"Seeds 1-1000, {label}: {1000 - failed} passed, {failed} failed ({failed / 10:.1f}%)")

print()
print("Why some unfixed runs pass:")
none = known = 0
for seed in range(1, 1001):
    ok, _ = search_books_test(seed, False)
    if ok:
        c = generate_catalog(random.Random(seed))
        q = next(iter(c["booksByIsbn"].values()))["title"][0]
        ids = [a for b in c["booksByIsbn"].values() if q in b["title"] for a in b["authorIds"]]
        none += not ids
        known += bool(ids) and all(a in c["authorsById"] for a in ids)
print(f"  matching books cite no author at all: {none}")
print(f"  matching books cite only authors that exist: {known}")
