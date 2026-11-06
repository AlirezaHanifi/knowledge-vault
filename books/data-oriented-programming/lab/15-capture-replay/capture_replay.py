"""Capture and replay: DOP chapter 15 (pp. 311-330).

Dumps a function context (its arguments) to a JSON file named by context and UUID
(listings 15.15-15.21), reads it back synchronously and replays the call (listing
15.22), runs the eight queries of listings 15.25-15.26 against the three versions of
the search, and shows what an asynchronous dump records when the data is mutated
meanwhile. Files go to a temporary directory. Standard library only; the UUIDs are
seeded, and the race is ordered with events, so the output is deterministic.
"""
import json
import os
import random
import re
import shutil
import tempfile
import threading
import uuid

rnd = random.Random(15)
CATALOG = {"booksByIsbn": {
    "978-1982137274": {"isbn": "978-1982137274", "title": "7 Habits of Highly Effective People", "authorIds": ["sean-covey", "stephen-covey"]},
    "978-1779501127": {"isbn": "978-1779501127", "title": "Watchmen", "publicationYear": 1987, "authorIds": ["alan-moore", "dave-gibbons"]}},
    "authorsById": {"stephen-covey": {"name": "Stephen Covey", "bookIsbns": ["978-1982137274"]},
                    "sean-covey": {"name": "Sean Covey", "bookIsbns": ["978-1982137274"]},
                    "dave-gibbons": {"name": "Dave Gibbons", "bookIsbns": ["978-1779501127"]},
                    "alan-moore": {"name": "Alan Moore", "bookIsbns": ["978-1779501127"]}}}

MATCH = {
    "15.8 lowercase startsWith": lambda title, q: title.lower().startswith(q.lower()),
    "15.12 word startsWith": lambda title, q: any(w.startswith(q) for w in title.split(" ")),
    "15.24 lowercase \\b regex": lambda title, q: re.search(r"\b" + q.lower(), title.lower()) is not None,
}


def search_books_by_title(catalog, query, version):
    return [{"title": b["title"], "isbn": b["isbn"], "authorNames": [catalog["authorsById"][a]["name"] for a in b["authorIds"]]}
            for b in catalog["booksByIsbn"].values() if MATCH[version](b["title"], query)]


root = tempfile.mkdtemp()


def file_path(context):
    """Listing 15.15, with the UUID actually concatenated."""
    return os.path.join("test-data", context + "-" + str(uuid.UUID(int=rnd.getrandbits(128), version=4)) + ".json")


def dump_data(data, context, before_write=None):
    """Listing 15.16 with listing 15.20's indentation; the write happens on another thread."""
    path = file_path(context)

    def write():
        if before_write:
            before_write.wait()            # slow I/O: the caller goes on meanwhile
        os.makedirs(os.path.join(root, "test-data"), exist_ok=True)
        with open(os.path.join(root, path), "w") as f:
            f.write(json.dumps(data, indent=2))
    t = threading.Thread(target=write)
    t.start()
    return path, t


def read_data(path):
    """Listing 15.22: synchronous, since the test can't run before the data is read."""
    with open(os.path.join(root, path)) as f:
        return json.load(f)


print("1. Capture: console.log versus JSON.stringify (listings 15.5-15.6)")
sentence = 'I like the word "reproducibility"'
print("   console.log:   ", sentence)
print("   JSON.stringify:", json.dumps(sentence))
for label, text in (("console.log", sentence), ("JSON", json.dumps(sentence))):
    try:
        json.loads(text)
        print(f"   pasting the {label} output back: OK")
    except json.JSONDecodeError as e:
        print(f"   pasting the {label} output back: fails ({e.msg})")
print()

print("2. Dump the context of searchBooksByTitle(catalog, 'Watch'), then replay it")
path, t = dump_data([CATALOG, "Watch"], "searchBooksByTitle")
t.join()
print("   wrote", path, f"({os.path.getsize(os.path.join(root, path))} bytes)")
catalog, query = read_data(path)
original = search_books_by_title(CATALOG, "Watch", "15.8 lowercase startsWith")
replayed = search_books_by_title(catalog, query, "15.8 lowercase startsWith")
print("   original:", json.dumps(original))
print("   replayed:", json.dumps(replayed), "| identical:", original == replayed)
print()

print("3. The eight queries of listings 15.25-15.26 on the captured catalog")
QUERIES = [("Habit", True), ("habit", True), ("7 Habit", True), ("habits of", True),
           ("abit", False), ("bit", False), ("7 abit", False), ("habit of", False)]
print((f"   {'query':<11} {'expected':<9}" + "".join(f"{v:<28}" for v in MATCH)).rstrip())
passes = dict.fromkeys(MATCH, 0)
for q, expected in QUERIES:
    cells = []
    for v in MATCH:
        found = bool(search_books_by_title(catalog, q, v))
        passes[v] += found == expected
        cells.append(f"{('ok   ' if found == expected else 'FAIL ') + ('found' if found else 'none'):<28}")
    print((f"   {json.dumps(q):<11} {'book' if expected else 'nothing':<9}" + "".join(cells)).rstrip())
print(("   passing:  " + " " * 10 + "".join(f"{str(n) + ' / 8':<28}" for n in passes.values())).rstrip())
print()

print("4. An asynchronous dump while the caller goes on and withdraws Watchmen")
for mode in ("mutable", "immutable"):
    data = json.loads(json.dumps(CATALOG))
    seen = search_books_by_title(data, "Watch", "15.24 lowercase \\b regex")
    go = threading.Event()
    path, t = dump_data([data, "Watch"], "searchBooksByTitle", before_write=go)
    if mode == "mutable":
        del data["booksByIsbn"]["978-1779501127"]                     # changes the dumped object
    else:
        data = {**data, "booksByIsbn": {k: b for k, b in data["booksByIsbn"].items() if k != "978-1779501127"}}  # a new version
    go.set()
    t.join()
    c, q = read_data(path)
    replay = search_books_by_title(c, q, "15.24 lowercase \\b regex")
    print(f"   {mode:<9} data: the function saw {len(seen)} book(s); the replay finds {len(replay)} -> "
          + ("reproduced" if replay == seen else "NOT reproduced"))

shutil.rmtree(root)
