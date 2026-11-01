"""Snapshot isolation lets write skew through; serializable snapshot isolation
(SSI) catches it.

Replays the book's on-call doctors example (pp. 303-304) and then runs many
random interleavings of the same two transactions. The MVCC engine is the
vault's own simplification: snapshot reads, first-committer-wins on write-write
conflicts, and an SSI check that aborts a read-write transaction at commit if
anything it read was overwritten by a transaction that committed after its
snapshot was taken.
"""

from __future__ import annotations

import random


class Abort(Exception):
    pass


class Database:
    def __init__(self, rows: dict):
        self.versions = {k: [(0, v)] for k, v in rows.items()}   # key -> [(commit_ts, value)]
        self.clock = 0

    def begin(self, serializable: bool) -> "Txn":
        return Txn(self, serializable)

    def latest(self, key):
        return self.versions[key][-1]


class Txn:
    def __init__(self, db: Database, serializable: bool):
        self.db, self.ssi = db, serializable
        self.snapshot: int | None = None              # taken at the first statement
        self.writes: dict = {}
        self.reads: set = set()

    def read(self, key):
        if self.snapshot is None:
            self.snapshot = self.db.clock
        self.reads.add(key)
        if key in self.writes:
            return self.writes[key]
        return next(v for ts, v in reversed(self.db.versions[key]) if ts <= self.snapshot)

    def write(self, key, value):
        self.writes[key] = value

    def commit(self) -> None:
        for key in self.writes:                                   # write-write conflict
            if self.db.latest(key)[0] > self.snapshot:
                raise Abort(f"concurrent update to {key}")
        if self.ssi and self.writes:                              # stale premise (rw-conflict)
            stale = [k for k in self.reads if self.db.latest(k)[0] > self.snapshot]
            if stale:
                raise Abort(f"read {', '.join(sorted(stale))} which changed after the snapshot")
        self.db.clock += 1
        for key, value in self.writes.items():
            self.db.versions[key].append((self.db.clock, value))


def go_off_call(txn: Txn, doctor: str):
    """Generator: yields between statements so we can interleave two transactions."""
    on_call = sum(txn.read(d) for d in ("aaliyah", "bryce"))
    yield f"counts {on_call} doctors on call"
    if on_call >= 2:
        txn.write(doctor, False)
        yield f"sets {doctor} off call"
    txn.commit()
    yield "commits"


def run(serializable: bool, order: list[int], verbose: bool = False) -> tuple[int, int]:
    db = Database({"aaliyah": True, "bryce": True})
    names = ["aaliyah", "bryce"]
    txns = [db.begin(serializable), db.begin(serializable)]
    gens = [go_off_call(t, n) for t, n in zip(txns, names)]
    live, aborts = [True, True], 0
    for who in order:
        if not live[who]:
            continue
        try:
            msg = next(gens[who])
            if verbose:
                print(f"    T{who + 1} ({names[who]}) {msg}")
        except StopIteration:
            live[who] = False
        except Abort as e:
            live[who] = False
            aborts += 1
            if verbose:
                print(f"    T{who + 1} ({names[who]}) ABORTED: {e}")
    on_call = sum(db.latest(d)[1] for d in names)
    return on_call, aborts


def main() -> None:
    order = [0, 1, 0, 1, 0, 1, 0, 1]
    for label, ssi in (("Snapshot isolation", False), ("Serializable (SSI)", True)):
        print(f"{label}, the book's interleaving:")
        on_call, aborts = run(ssi, order, verbose=True)
        print(f"  -> doctors still on call: {on_call}  (aborted transactions: {aborts})\n")

    rng = random.Random(1)
    orders = [rng.sample([0, 0, 0, 0, 1, 1, 1, 1], 8) for _ in range(1_000)]
    serial = sum(o in ([0] * 4 + [1] * 4, [1] * 4 + [0] * 4) for o in orders)
    print(f"1,000 random interleavings of the same two transactions ({serial} happen to be serial):")
    for label, ssi in (("Snapshot isolation", False), ("Serializable (SSI)", True)):
        violations = aborted = 0
        for order in orders:
            on_call, aborts = run(ssi, order)
            violations += on_call == 0
            aborted += aborts
        print(f"  {label:<20} nobody on call in {violations:4d} runs; {aborted:4d} aborts (retry needed)")


if __name__ == "__main__":
    main()
