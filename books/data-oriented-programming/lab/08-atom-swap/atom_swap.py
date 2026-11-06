"""Atoms in a seeded scheduler: DOP chapter 8 (pp. 164-174).

Threads increment a shared counter of database accesses. Each increment is split
into steps, and a seeded scheduler interleaves the steps of all threads, so every
strategy runs on reproducible interleavings:

  none   read; write(read + 1)                  -- can lose updates
  mutex  lock (wait if held); read; write; unlock   (listing 8.1)
  atom   snapshot; compute; compare-and-set, retry on failure   (listing 8.3)

Standard library only; seeded.
"""
import random


def run(strategy, threads, increments, seed, work=0):
    rnd = random.Random(seed)
    counter = 0
    lock_owner = None
    state = [{"left": increments, "pc": 0, "tmp": None} for _ in range(threads)]
    waits = retries = steps = 0
    while any(s["left"] for s in state):
        i = rnd.choice([j for j, s in enumerate(state) if s["left"]])
        s = state[i]
        steps += 1
        if strategy == "none":
            if s["pc"] == 0:
                s["tmp"], s["pc"] = counter, 1
            else:
                counter, s["pc"] = s["tmp"] + 1, 0
                s["left"] -= 1
        elif strategy == "mutex":
            if s["pc"] == 0:
                if lock_owner is None:
                    lock_owner, s["pc"] = i, 1
                else:
                    waits += 1                       # blocked: this step is spent waiting
            elif s["pc"] == 1:
                s["tmp"], s["pc"] = counter, 2
            elif s["pc"] == 2:
                counter, s["pc"] = s["tmp"] + 1, 3
            else:
                lock_owner, s["pc"] = None, 0
                s["left"] -= 1
        else:  # atom
            if s["pc"] == 0:
                s["snap"], s["pc"] = counter, 1      # snapshot = state
            elif s["pc"] < 1 + work:
                s["pc"] += 1                          # f(snapshot) takes `work` extra steps
            elif s["pc"] == 1 + work:
                s["tmp"], s["pc"] = s["snap"] + 1, 2 + work
            else:                                     # atomicCompareAndSet(state, snapshot, next)
                if counter == s["snap"]:
                    counter = s["tmp"]
                    s["left"] -= 1
                else:
                    retries += 1
                s["pc"] = 0
    expected = threads * increments
    return {"final": counter, "lost": expected - counter, "waits": waits, "retries": retries, "steps": steps}


INC = 1000
print(f"Each thread increments the counter {INC:,} times; 5 seeded interleavings per row (sum shown)")
print(f"{'threads':>7} {'strategy':>8} {'expected':>9} {'lost updates':>13} {'mutex waits':>12} {'CAS retries':>12} {'steps':>9}")
for threads in (1, 2, 4, 8):
    for strategy in ("none", "mutex", "atom"):
        tot = {"lost": 0, "waits": 0, "retries": 0, "steps": 0}
        for seed in range(5):
            r = run(strategy, threads, INC, seed)
            for k in tot:
                tot[k] += r[k]
        print(f"{threads:>7} {strategy:>8} {threads * INC * 5:>9,} {tot['lost']:>13,} {tot['waits']:>12,} {tot['retries']:>12,} {tot['steps']:>9,}")

print()
print("Atom with a slower update function (4 threads, seed 0): retries grow, nothing is lost")
print(f"{'extra steps in f':>16} {'CAS retries':>12} {'retries per update':>19} {'lost':>5}")
for work in (0, 2, 5, 10, 20):
    r = run("atom", 4, INC, 0, work)
    print(f"{work:>16} {r['retries']:>12,} {r['retries'] / (4 * INC):>19.2f} {r['lost']:>5}")
