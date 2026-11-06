"""Stale reads with and without quorum overlap (R + W > N).

Illustrates Database Internals, Chapter 11, "Tunable Consistency" (pp. 235-236):
with N replicas, a write acknowledged by W and a read from R replicas must
overlap when R + W > N, so the read sees the latest acknowledged write. Writes
reach the other replicas asynchronously after a random delay; replicas fail
independently. Delays, failure rate and workload are the vault's (seeded).
"""

import random

STEPS, FAIL = 20_000, 0.05


def run(n, w, r, seed=11):
    rnd = random.Random(seed)
    version = [0] * n                    # latest version each replica holds
    pending = []                         # (arrival_step, replica, version)
    latest = stale = failed_w = failed_r = 0
    for t in range(STEPS):
        for item in [p for p in pending if p[0] <= t]:
            pending.remove(item)
            version[item[1]] = max(version[item[1]], item[2])
        up = [i for i in range(n) if rnd.random() > FAIL]
        # write
        if len(up) >= w:
            latest += 1
            sync = rnd.sample(up, w)
            for i in sync:
                version[i] = latest
            for i in set(range(n)) - set(sync):
                pending.append((t + 1 + int(rnd.expovariate(1 / 3)), i, latest))
        else:
            failed_w += 1
        # read
        if len(up) >= r:
            if max(version[i] for i in rnd.sample(up, r)) < latest:
                stale += 1
        else:
            failed_r += 1
    reads = STEPS - failed_r
    return stale / reads, failed_w / STEPS, failed_r / STEPS


print(f"{STEPS:,} write+read steps, each replica down with probability {FAIL:.0%} per step,")
print("async propagation to the other replicas after ~3 steps on average\n")
print(f"{'N':>2} {'W':>2} {'R':>2} {'R+W>N':>6} {'stale reads':>12} {'writes unavailable':>19} {'reads unavailable':>18}")
for n, w, r in ((3, 1, 1), (3, 2, 1), (3, 2, 2), (3, 1, 3), (3, 3, 3), (5, 1, 1), (5, 2, 2), (5, 3, 3), (5, 2, 4)):
    s, fw, fr = run(n, w, r)
    print(f"{n:>2} {w:>2} {r:>2} {'yes' if r + w > n else 'no':>6} {s:>12.2%} {fw:>19.2%} {fr:>18.2%}")
