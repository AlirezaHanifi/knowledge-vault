"""Three-way merge in Python: DOP listings 5.4-5.16 (pp. 100-107).

Ports diff, informationPaths, havePathInCommon, the merge and reconcile; replays the
book's tiny library (listings 5.6-5.7); shows the inverted condition of listing 5.16
and the array-identity pitfall of _.intersection; then counts aborts as concurrent
mutations crowd onto fewer fields. Standard library only; seeded.
"""
import json
import random

random.seed(5)
NO_DIFF = "no-diff"


def is_obj(x):
    return isinstance(x, (dict, list))


def get(x, k):
    if isinstance(x, dict):
        return x.get(k)
    if isinstance(x, list):
        return x[k] if k < len(x) else None
    return None


def diff_objects(d1, d2):
    """Listing 5.4: a recursion inside a reduce."""
    empty = [] if isinstance(d1, list) else {}
    if d1 is d2:                       # data1 == data2 compares references
        return empty
    keys = list(range(max(len(d1), len(d2)))) if isinstance(d1, list) else list(dict.fromkeys([*d1, *(d2 if isinstance(d2, dict) else [])]))
    acc = empty
    for k in keys:
        res = diff(get(d1, k), get(d2, k))
        if (is_obj(res) and not res) or res == NO_DIFF:
            continue
        if isinstance(acc, list):
            acc = acc + [None] * (k + 1 - len(acc))
            acc[k] = res
        else:
            acc = {**acc, k: res}
    return acc


def diff(d1, d2):
    if is_obj(d1) and is_obj(d2):
        return diff_objects(d1, d2)
    return d2 if d1 != d2 else NO_DIFF


def information_paths(obj, path=()):
    """Listing 5.10."""
    items = obj.items() if isinstance(obj, dict) else enumerate(obj)
    acc = []
    for k, v in items:
        acc += information_paths(v, path + (k,)) if is_obj(v) else [list(path + (k,))]
    return acc


def have_path_in_common(d1, d2):
    """Listing 5.13, comparing paths by value (as _.intersectionWith(..., _.isEqual) would)."""
    a = {tuple(p) for p in information_paths(d1)}
    return bool(a & {tuple(p) for p in information_paths(d2)})


def have_path_in_common_by_identity(d1, d2):
    """_.intersection uses SameValueZero: two separately built arrays are never equal."""
    p1, p2 = information_paths(d1), information_paths(d2)
    return any(x is y for x in p1 for y in p2)


def merge(a, b):
    """A recursive _.merge(current, patch) that returns a new map."""
    if isinstance(a, dict) and isinstance(b, dict):
        out = dict(a)
        for k, v in b.items():
            out[k] = merge(a.get(k), v) if k in a else v
        return out
    return b


def set_in(m, path, v):
    k, rest = path[0], path[1:]
    return {**m, k: set_in(m[k], rest, v) if rest else v}


class Conflict(Exception):
    pass


def three_way_merge(current, previous, nxt, printed=False, by_identity=False):
    p1, p2 = diff(previous, current), diff(previous, nxt)
    common = (have_path_in_common_by_identity if by_identity else have_path_in_common)(p1, p2)
    if printed:                       # listing 5.16 as printed: merges when there IS a common path
        common = not common
    if not common:
        return merge(current, p2)
    raise Conflict("Conflicting concurrent mutations.")


def reconcile(current, previous, nxt, **kw):
    if current is previous:           # fast-forward
        return nxt
    return three_way_merge(current, previous, nxt, **kw)


library = {"catalog": {
    "booksByIsbn": {"978-1779501127": {"isbn": "978-1779501127", "title": "Watchmen", "publicationYear": 1987,
                                       "authorIds": ["alan-moore", "dave-gibbons"]}},
    "authorsById": {"alan-moore": {"name": "Alan Moore", "bookIsbns": ["978-1779501127"]},
                    "dave-gibbons": {"name": "Dave Gibbons", "bookIsbns": ["978-1779501127"]}}}}
W = ["catalog", "booksByIsbn", "978-1779501127"]
previous = library
nxt = set_in(library, W + ["publicationYear"], 1986)
current = set_in(set_in(library, W + ["title"], "The Watchmen"), ["catalog", "authorsById", "dave-gibbons", "name"], "David Chester Gibbons")

print("diff(previous, next):   ", json.dumps(diff(previous, nxt)))
print("diff(previous, current):", json.dumps(diff(previous, current)))
print("paths of next's diff:   ", information_paths(diff(previous, nxt)))
print("paths of current's diff:", information_paths(diff(previous, current)))
print("table 5.4, array addition: diff([1], [1, 2]) =", json.dumps(diff([1], [1, 2])))
print()
print("reconcile(current, previous, next), condition fixed:")
print(json.dumps(reconcile(current, previous, nxt), indent=1))
print()
print("Fast-forward when nothing else committed:", reconcile(previous, previous, nxt) is nxt)
try:
    reconcile(current, previous, nxt, printed=True)
    print("Listing 5.16 as printed: merged")
except Conflict as e:
    print("Listing 5.16 as printed, on these NON-conflicting mutations:", e)

both_years = set_in(library, W + ["publicationYear"], 1988)
try:
    reconcile(both_years, previous, nxt)
    print("Both set publicationYear, paths compared by value: merged")
except Conflict as e:
    print("Both set publicationYear, paths compared by value:", e)
try:
    out = reconcile(both_years, previous, nxt, by_identity=True)
    print("Both set publicationYear, paths compared by identity: merged silently, year =",
          out["catalog"]["booksByIsbn"]["978-1779501127"]["publicationYear"], "(1988 lost)")
except Conflict as e:
    print("Both set publicationYear, paths compared by identity:", e)

print()
print("Two concurrent mutations, each setting one random field out of F (1,000 trials each)")
print(f"{'F':>4} {'aborted':>8} {'abort rate':>11}")
for F in (1, 2, 4, 8, 16, 64):
    base = {"fields": {f"f{i}": 0 for i in range(F)}}
    aborts = 0
    for t in range(1000):
        a = set_in(base, ["fields", f"f{random.randrange(F)}"], t + 1)
        b = set_in(base, ["fields", f"f{random.randrange(F)}"], -(t + 1))
        try:
            reconcile(a, base, b)
        except Conflict:
            aborts += 1
    print(f"{F:>4} {aborts:>8} {aborts / 1000:>10.1%}")
