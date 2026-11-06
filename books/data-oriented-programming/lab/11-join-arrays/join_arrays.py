"""Joining sources by key: DOP chapter 11 (pp. 229-239).

Double field filtering with pick (listing 11.9), keyBy (listings 11.16-11.17) and
the generic joinArrays (listings 11.18-11.19), run against a mocked Open Library.
The mock's 7 Habits record uses fields from listing 11.6; The Power of Habit's uses
the fields of listing 11.19. Standard library only; no randomness, no network.
"""
import json

OPEN_LIBRARY = {   # a mock of GET https://openlibrary.org/isbn/<isbn>.json
    "978-1982137274": {"full_title": "7 Habits of Highly Effective People : Revised and Updated Powerful Lessons in Personal Change",
                       "isbn_13": ["9781982137274"], "number_of_pages": 432, "publish_date": "2020",
                       "publishers": ["Simon & Schuster, Incorporated"], "subtitle": "Powerful Lessons in Personal Change",
                       "title": "7 Habits of Highly Effective People : Revised and Updated", "revision": 3, "latest_revision": 3},
    "978-0812981605": {"title": "The Power of Habit", "subtitle": "Why We Do What We Do in Life and Business",
                       "subjects": ["Social aspects", "Habit", "Change (Psychology)"], "isbn_13": ["9780812981605"]},
}
DATABASE = [{"isbn": "978-1982137274", "available": True}, {"isbn": "978-0812981605", "available": False}]


def pick(m, fields):
    return {k: m[k] for k in fields if k in m}


def book_info(isbn, requested, relevant):
    """Listing 11.9: fetch, then pick the relevant fields, then the requested ones, then set isbn."""
    raw = OPEN_LIBRARY[isbn]
    return {**pick(pick(raw, relevant), requested), "isbn": isbn}


RELEVANT_PRINTED = ["title", "full_title", "subtitle", "publisher", "publish_date", "weight",
                    "physical_dimensions", "genre", "subjects", "number_of_pages"]
RELEVANT_FIXED = [f if f != "publisher" else "publishers" for f in RELEVANT_PRINTED]
requested = ["title", "publishers", "number_of_pages", "revision"]

print("1. Double field filtering of 7 Habits, requested:", requested)
print("   relevantFields as printed:", json.dumps(book_info("978-1982137274", requested, RELEVANT_PRINTED)))
print("   with \"publishers\":       ", json.dumps(book_info("978-1982137274", requested, RELEVANT_FIXED)))
print("   ('revision' is requested but not relevant, so the server never exposes it)")
print()


def key_by(coll, key):
    """_.keyBy: like groupBy, but one element per key; the last one wins."""
    return {x[key]: x for x in coll}


print("2. keyBy keeps the last element per key")
print("  ", json.dumps(key_by([{"isbn": "a", "n": 1}, {"isbn": "b", "n": 2}, {"isbn": "a", "n": 3}], "isbn")))
print()


def merge(a, b):
    out = dict(a)
    for k, v in b.items():
        out[k] = merge(a[k], v) if isinstance(a.get(k), dict) and isinstance(v, dict) else v
    return out


def join_arrays(a, b, key_a, key_b, conflicts=None):
    """Listing 11.18: key both arrays, merge the maps, return the values."""
    map_a, map_b = key_by(a, key_a), key_by(b, key_b)
    if conflicts is not None:
        for k in sorted(map_a.keys() & map_b.keys()):
            for f in sorted(map_a[k].keys() & map_b[k].keys()):
                if map_a[k][f] != map_b[k][f]:
                    conflicts.append((k, f, map_a[k][f], map_b[k][f]))
    return list(merge(map_a, map_b).values())


print("3. The test data of listing 11.19 (each Open Library record carries the other book's title)")
db_infos = [{"isbn": "978-1982137274", "title": "7 Habits of Highly Effective People", "available": True},
            {"isbn": "978-0812981605", "title": "The Power of Habit", "available": False}]
ol_infos = [{"isbn": "978-0812981605", "title": "7 Habits of Highly Effective People", "subtitle": "Powerful Lessons in Personal Change", "number_of_pages": 432},
            {"isbn": "978-1982137274", "title": "The Power of Habit", "subtitle": "Why We Do What We Do in Life and Business",
             "subjects": ["Social aspects", "Habit", "Change (Psychology)"]}]
conflicts = []
for row in join_arrays(db_infos, ol_infos, "isbn", "isbn", conflicts):
    print("  ", json.dumps(row, sort_keys=True))
print("   conflicts (Open Library wins silently):")
for isbn, f, a, b in conflicts:
    print(f"     {isbn} {f}: database {a!r} vs Open Library {b!r}")
print()

print("4. The enrichment flow with the mock: database rows joined with filtered Open Library records")
requested = ["title", "subtitle", "number_of_pages"]
ol = [book_info(r["isbn"], requested, RELEVANT_FIXED) for r in DATABASE]
conflicts = []
for row in join_arrays(DATABASE, ol, "isbn", "isbn", conflicts):
    print("  ", json.dumps(row, sort_keys=True))
print("   conflicts:", conflicts or "none (the database contributes only isbn and available)")
print()

print("5. An outer join: a database book with no Open Library record, and vice versa")
for row in join_arrays(DATABASE + [{"isbn": "978-0000000001", "available": True}],
                       ol + [{"isbn": "978-0000000002", "title": "Only in Open Library"}], "isbn", "isbn"):
    print("  ", json.dumps(row, sort_keys=True))
