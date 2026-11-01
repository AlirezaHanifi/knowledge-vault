"""Detecting concurrent writes: version numbers on one replica, version vectors
across several replicas.

Part 1 replays the book's shopping-cart example (Figures 6-15/6-16, pp. 240-241)
with the single-replica version-number algorithm described on pp. 239-240.
Part 2 generalizes to version vectors across two replicas.
The code is the vault's own implementation of the algorithm the book describes.
"""

from __future__ import annotations


class SingleReplica:
    """Server keeps a version counter per key and all values not yet overwritten (siblings)."""

    def __init__(self):
        self.version = 0
        self.siblings: dict[int, frozenset] = {}     # version -> value

    def read(self):
        return self.version, list(self.siblings.values())

    def write(self, value: frozenset, based_on: int):
        self.version += 1
        # Overwrite everything the client had seen (version <= based_on); keep concurrent values.
        self.siblings = {v: s for v, s in self.siblings.items() if v > based_on}
        self.siblings[self.version] = value
        return self.read()


def show(values) -> str:
    return " | ".join("[" + ", ".join(sorted(v)) + "]" for v in values)


def part1() -> None:
    print("Part 1 - one replica, two clients (the book's shopping cart)")
    db = SingleReplica()
    c1_ver, c1_seen = 0, []
    c2_ver, c2_seen = 0, []

    def client_write(name, seen, ver, item):
        merged = frozenset().union(*seen) | {item}            # merge siblings, then add
        new_ver, siblings = db.write(merged, ver)
        print(f"  {name} adds {item:<6} (based on v{ver}) -> server v{new_ver}: {show(siblings)}")
        return new_ver, siblings

    c1_ver, c1_seen = client_write("client 1", c1_seen, c1_ver, "milk")
    c2_ver, c2_seen = client_write("client 2", c2_seen, c2_ver, "eggs")
    c1_ver, c1_seen = client_write("client 1", c1_seen, c1_ver, "flour")
    c2_ver, c2_seen = client_write("client 2", c2_seen, c2_ver, "ham")
    c1_ver, c1_seen = client_write("client 1", c1_seen, c1_ver, "bacon")
    final = frozenset().union(*db.read()[1])
    print(f"  a reader merging the siblings sees: [{', '.join(sorted(final))}] - no item lost")


# ------------------------------------------------------------------ part 2

def compare(a: dict, b: dict) -> str:
    keys = a.keys() | b.keys()
    le = all(a.get(k, 0) <= b.get(k, 0) for k in keys)
    ge = all(a.get(k, 0) >= b.get(k, 0) for k in keys)
    if le and ge:
        return "equal"
    if le:
        return "happens-before"
    if ge:
        return "happens-after"
    return "concurrent"


class Replica:
    """Stores siblings tagged with version vectors; each replica increments its own entry."""

    def __init__(self, name: str):
        self.name = name
        self.siblings: list[tuple[dict, frozenset]] = []

    def context(self) -> dict:
        merged: dict = {}
        for vv, _ in self.siblings:
            for k, n in vv.items():
                merged[k] = max(merged.get(k, 0), n)
        return merged

    def write(self, value: frozenset, ctx: dict) -> dict:
        vv = dict(ctx)
        vv[self.name] = max(self.context().get(self.name, 0), ctx.get(self.name, 0)) + 1
        self.siblings = [(v, s) for v, s in self.siblings if compare(v, vv) == "concurrent"]
        self.siblings.append((vv, value))
        return vv

    def receive(self, vv: dict, value: frozenset) -> str:
        """Anti-entropy / replication: keep the new value unless something we hold dominates it."""
        if any(compare(vv, v) in ("happens-before", "equal") for v, _ in self.siblings):
            return "ignored (already superseded)"
        self.siblings = [(v, s) for v, s in self.siblings if compare(v, vv) != "happens-before"]
        self.siblings.append((vv, value))
        return "concurrent sibling kept" if len(self.siblings) > 1 else "applied"


def part2() -> None:
    print("\nPart 2 - two replicas, version vectors")
    a, b = Replica("A"), Replica("B")
    v1 = a.write(frozenset({"milk"}), {})
    print(f"  write [milk] at A           -> {v1}; replicate to B: {b.receive(v1, frozenset({'milk'}))}")
    ctx = b.context()
    v2 = b.write(frozenset({"milk", "eggs"}), ctx)
    v3 = a.write(frozenset({"milk", "flour"}), a.context())
    print(f"  B writes [eggs, milk]       -> {v2}")
    print(f"  A writes [flour, milk]      -> {v3}   (neither saw the other: {compare(v2, v3)})")
    print(f"  replicate B's write to A: {a.receive(v2, frozenset({'milk', 'eggs'}))}")
    print(f"  A now holds siblings: {show(s for _, s in a.siblings)}")
    merged = frozenset().union(*(s for _, s in a.siblings))
    v4 = a.write(merged, a.context())
    print(f"  a client merges them at A   -> {v4}: {show([merged])}")
    print(f"  replicate to B: {b.receive(v4, merged)}; B holds {show(s for _, s in b.siblings)}")


if __name__ == "__main__":
    part1()
    part2()
