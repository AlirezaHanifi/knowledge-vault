"""Structural sharing in numbers: a Python port of setImmutable (DOP listing 4.4, p. 81).

Counts how many maps an immutable set creates and how many it shares, compares that
with a deep copy, and measures the memory kept by a thousand versions of the library.
Standard library only; the random updates are seeded.
"""
import copy
import random

random.seed(4)


def set_immutable(m, path, v):
    """Listing 4.4: recurse down the path, shallow-clone each map on the way back up."""
    k, rest = path[0], path[1:]
    modified = set_immutable(m[k], rest, v) if rest else v
    res = dict(m)          # Object.assign({}, map): a shallow clone
    res[k] = modified
    return res


def maps(x, seen=None):
    """The ids of every dict reachable from x."""
    seen = set() if seen is None else seen
    if isinstance(x, dict) and id(x) not in seen:
        seen.add(id(x))
        for v in x.values():
            maps(v, seen)
    elif isinstance(x, list):
        for v in x:
            maps(v, seen)
    return seen


def library(n_books, n_members):
    """A library shaped like the book's (figure 4.2): catalog plus user management."""
    books = {f"isbn-{i:05}": {"isbn": f"isbn-{i:05}", "title": f"Book {i}", "publicationYear": 1950 + i % 70,
                             "authorIds": [f"author-{i % 300}"],
                             "bookItems": [{"id": f"item-{i}-{j}", "libId": "nyc-central-lib", "isLent": False} for j in range(2)]}
             for i in range(n_books)}
    authors = {f"author-{a}": {"id": f"author-{a}", "name": f"Author {a}", "bookIsbns": []} for a in range(300)}
    members = {f"m{i}@x.org": {"email": f"m{i}@x.org", "isBlocked": False, "bookLendings": []} for i in range(n_members)}
    return {"name": "Klafim", "address": "Somewhere",
            "catalog": {"booksByIsbn": books, "authorsById": authors},
            "userManagement": {"librariansByEmail": {"franck@gmail.com": {"email": "franck@gmail.com"}},
                               "membersByEmail": members}}


print("One update: set a book's publication year")
print(f"{'books':>7} {'maps in library':>16} {'new maps':>9} {'slots copied':>13} {'shared maps':>12} {'deep copy':>10}")
for n in (10, 100, 1000, 10000):
    lib = library(n, n // 2)
    before = maps(lib)
    nxt = set_immutable(lib, ["catalog", "booksByIsbn", "isbn-00003", "publicationYear"], 2000)
    after = maps(nxt)
    new, shared = len(after - before), len(after & before)
    slots = sum(len(d) for d in (nxt, nxt["catalog"], nxt["catalog"]["booksByIsbn"], nxt["catalog"]["booksByIsbn"]["isbn-00003"]))
    deep = len(maps(copy.deepcopy(lib)))
    print(f"{n:>7} {len(before):>16,} {new:>9} {slots:>13,} {shared:>12,} {deep:>10,}")

print()
print("The previous version is untouched:")
lib = library(3, 2)
nxt = set_immutable(lib, ["catalog", "booksByIsbn", "isbn-00001", "title"], "Watchmen")
print("  previous title:", lib["catalog"]["booksByIsbn"]["isbn-00001"]["title"])
print("  next title:    ", nxt["catalog"]["booksByIsbn"]["isbn-00001"]["title"])
print("  userManagement shared by reference:", lib["userManagement"] is nxt["userManagement"])
print("  sibling book shared by reference:  ", lib["catalog"]["booksByIsbn"]["isbn-00000"] is nxt["catalog"]["booksByIsbn"]["isbn-00000"])

print()
print("Keeping 1,000 versions of a 1,000-book library (one random update each)")
lib = library(1000, 500)
versions, v = [lib], lib
for _ in range(1000):
    isbn = f"isbn-{random.randrange(1000):05}"
    v = set_immutable(v, ["catalog", "booksByIsbn", isbn, "publicationYear"], random.randrange(1900, 2022))
    versions.append(v)
retained = set()
for ver in versions:
    maps(ver, retained)
one = len(maps(lib))
print(f"  maps in one version:               {one:,}")
print(f"  maps kept by 1,001 shared versions: {len(retained):,}  ({len(retained) / one:.2f}x one version)")
print(f"  maps kept by 1,001 deep copies:     {one * 1001:,}  ({1001:.0f}x)")
