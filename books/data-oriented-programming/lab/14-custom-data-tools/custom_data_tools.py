"""Custom data tools: DOP chapter 14 (pp. 295-310).

update, flatMap, countByBoolField and unwind in Python, run on the chapter's data,
plus what happens to update and unwind when set mutates instead of returning a new
version. Standard library only; no randomness.
"""
import json


def set_imm(m, key, v):
    """An immutable set, like Lodash FP's: returns a new map."""
    return {**m, key: v}


def set_mut(m, key, v):
    """Default Lodash's _.set: mutates and returns the same map."""
    m[key] = v
    return m


def update(m, key, fun, set_=set_imm):
    """Listing 14.3."""
    return set_(m, key, fun(m.get(key)))


def flat_map(coll, f):
    """Listing 14.9."""
    f = (lambda x, k=f: x[k]) if isinstance(f, str) else f
    return [y for x in coll for y in f(x)]


def inc(n):
    return n + 1


def count_by_bool_field(coll, field, key_true, key_false):
    """Listing 14.15: a reduce with update, starting with both keys at 0."""
    res = {key_true: 0, key_false: 0}
    for item in coll:
        res = update(res, key_true if item.get(field) else key_false, inc)
    return res


def unwind(m, field, set_=set_imm):
    """Listing 14.19: one map per element of the array field."""
    return [set_(m, field, elem) for elem in list(m[field])]


def group_by(coll, path):
    out = {}
    for x in coll:
        k = x
        for p in path.split("."):
            k = k[p]
        out.setdefault(k, []).append(x)
    return out


print("update (listings 14.2-14.4)")
m = {"position": "manager", "income": 100000}
print("  update(m, 'income', x * 2):", update(m, "income", lambda x: x * 2), "| m is unchanged:", m)
book = {"title": "Watchmen", "authors": ["Alan Moore", "Dave Gibbons", "Alan Moore"]}
print("  removeAuthorDuplicates:", update(book, "authors", lambda a: list(dict.fromkeys(a)))["authors"])
print()

books = [{"isbn": "978-1779501127", "title": "Watchmen", "authorIds": ["alan-moore", "dave-gibbons"],
          "bookItems": [{"id": "book-item-1", "libId": "nyc-central-lib", "isLent": True}]},
         {"isbn": "978-1982137274", "title": "7 Habits of Highly Effective People", "authorIds": ["sean-covey", "stephen-covey"],
          "bookItems": [{"id": "book-item-123", "libId": "hudson-park-lib", "isLent": True},
                        {"id": "book-item-17", "libId": "nyc-central-lib", "isLent": False}]}]
print("flatMap (listings 14.5-14.9)")
print("  map:    ", json.dumps([b["authorIds"] for b in books]))
print("  flatMap:", json.dumps(flat_map(books, "authorIds")))
print()
print("countByBoolField (listings 14.13-14.15)")
print("  test of listing 14.14:", count_by_bool_field([{"a": True}, {"a": True}, {"a": True}, {"a": False}], "a", "aTrue", "aFalse"))
stats = count_by_bool_field(flat_map(books, "bookItems"), "isLent", "lent", "notLent")
print("  book items:", stats, "-> lendingRatio =", round(stats["lent"] / (stats["lent"] + stats["notLent"]), 4))
print()
print("unwind (listings 14.17-14.19)")
cart = {"customer-id": "joe", "items": [{"item": "phone", "quantity": 1}, {"item": "pencil", "quantity": 10}]}
for x in unwind(cart, "items"):
    print("  ", json.dumps(x))
print("  cart is unchanged:", json.dumps(cart["items"]))
by_lib = group_by(flat_map(books, lambda b: unwind(b, "bookItems")), "bookItems.libId")
print("  books grouped by library:")
for lib, entries in by_lib.items():
    print(f"    {lib}: " + ", ".join(f"{e['title']} ({e['bookItems']['id']})" for e in entries))
print()
print("The same with a mutating set (the vault note in the lesson)")
cart = {"customer-id": "joe", "items": [{"item": "phone", "quantity": 1}, {"item": "pencil", "quantity": 10}]}
out = unwind(cart, "items", set_=set_mut)
for x in out:
    print("  ", json.dumps(x))
print("  both results are the same object:", out[0] is out[1], "| the cart itself was changed:", json.dumps(cart["items"]))
m = {"income": 100000}
nxt = update(m, "income", lambda x: x * 2, set_=set_mut)
print("  update with a mutating set changes its input: m =", m, "| same object:", nxt is m)
mut_books = json.loads(json.dumps(books))
by_lib = group_by(flat_map(mut_books, lambda b: unwind(b, "bookItems", set_=set_mut)), "bookItems.libId")
print("  books grouped by library:", {k: [e["bookItems"]["id"] for e in v] for k, v in by_lib.items()})
