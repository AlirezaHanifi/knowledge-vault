"""Every interleaving of the waiters in the diner's pie case.

Illustrates The Pragmatic Programmer, Topic 34, Shared State Is Incorrect State (pp. 299-304).
The step breakdown and the exhaustive enumeration are the vault's.
"""
from functools import lru_cache

PROGRAMS = {
    "no lock": ("read", "check", "promise", "take", "give"),
    "semaphore": ("lock", "read", "check", "promise", "take", "unlock", "give"),
    "get_pie_if_available": ("get", "check", "give"),
}


def explore(mode: str, waiters: int, slices: int) -> dict[str, int]:
    prog = PROGRAMS[mode]
    results = {"ok": 0, "oversold": 0}

    # state: (pcs, seen counts, promised flags, pies, lock owner)
    def step(state, w):
        pcs, seen, promised, pies, owner = state
        pcs, seen, promised = list(pcs), list(seen), list(promised)
        op = prog[pcs[w]]
        if op == "lock":
            owner = w
        elif op == "unlock":
            owner = -1
        elif op == "read":
            seen[w] = pies
        elif op == "get":
            if pies > 0:
                pies -= 1
                seen[w] = 1
                promised[w] = True
            else:
                seen[w] = 0
        elif op == "check":
            if seen[w] <= 0:          # sorry, no pie: skip to unlock (semaphore) or stop
                pcs[w] = prog.index("unlock") if "unlock" in prog else len(prog)
                return (tuple(pcs), tuple(seen), tuple(promised), pies, owner)
        elif op == "promise":
            promised[w] = True
        elif op == "take":
            pies -= 1
        pcs[w] += 1
        return (tuple(pcs), tuple(seen), tuple(promised), pies, owner)

    @lru_cache(maxsize=None)
    def count(state):
        pcs, _, promised, _, owner = state
        moves = [w for w in range(waiters) if pcs[w] < len(prog) and not (prog[pcs[w]] == "lock" and owner not in (-1, w))]
        if not moves:
            return (0, 1) if sum(promised) > slices else (1, 0)
        ok = bad = 0
        for w in moves:
            a, b = count(step(state, w))
            ok += a
            bad += b
        return ok, bad

    ok, bad = count(((0,) * waiters, (0,) * waiters, (False,) * waiters, slices, -1))
    results["ok"], results["oversold"] = ok, bad
    return results


def main() -> None:
    print("Every interleaving of the waiters' steps; 'oversold' = more promises than slices\n")
    print(f"{'protection':<22}{'waiters':>8}{'slices':>7}{'interleavings':>15}{'oversold':>10}{'share':>8}")
    for mode in PROGRAMS:
        for waiters, slices in ((2, 1), (3, 1), (3, 2)):
            r = explore(mode, waiters, slices)
            total = r["ok"] + r["oversold"]
            print(f"{mode:<22}{waiters:>8}{slices:>7}{total:>15,}{r['oversold']:>10,}{r['oversold'] / total:>8.1%}")


if __name__ == "__main__":
    main()
