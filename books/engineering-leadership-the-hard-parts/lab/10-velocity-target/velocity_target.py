"""Velocity target: what happens when velocity stops being a planning tool and becomes a target.

Illustrates Engineering Leadership: The Hard Parts, Chapter 10, "Velocity: The Most Misused Metric in
Software" (pp. 215-216) and Goodhart's Law (p. 219). In April's story the board demands better
velocity; points rise from 30 to 45 a sprint by inflating estimates, skipping documentation and
"trivial" reviews and deferring all technical debt, until a routine deployment takes production down.

The model is the vault's own, with invented parameters: a team that honestly delivers about 30 points
a sprint either plans with velocity (reviews everything, spends 10% on debt) or must report 45 (inflates
estimates by 25%, skips review on enough stories to close the gap, does no debt work). Escaped bugs and
incidents cost rework in later sprints. Seeded; averages over 2,000 runs.
"""
import random

SPRINTS = 12
CAPACITY = 30.0           # honest points of work per sprint
TARGET = 45.0             # the board's demand
INFLATE = 1.25            # estimate inflation under the target
SKIP_SAVING = 0.20        # effort saved on a story whose review and docs are skipped
STORY = 3.0               # points per story
ESCAPE_REVIEWED, ESCAPE_SKIPPED = 0.03, 0.15
BUG_COST, INCIDENT_COST = 2.0, 8.0
TRIALS = 2000


def run(policy, rng):
    carry = 0.0  # rework owed from earlier sprints
    debt = 0     # sprints of deferred debt work
    out = dict(reported=0.0, f1=0.0, f2=0.0, f3=0.0, bugs=0, incidents=0, debtwork=0.0)
    for sprint in range(SPRINTS):
        avail = max(0.0, CAPACITY + rng.gauss(0, 2) - carry)
        carry = 0.0
        if policy == "plan":
            features, skip = 0.9 * avail, 0.0
            reported = features
            out["debtwork"] += 0.1 * avail
        else:
            skip = min(1.0, max(0.0, (1 - INFLATE * avail / TARGET) / SKIP_SAVING))
            features = avail / (1 - SKIP_SAVING * skip)
            reported = INFLATE * features
            debt += 1
        stories = int(features / STORY)
        bugs = sum(rng.random() < (ESCAPE_SKIPPED if rng.random() < skip else ESCAPE_REVIEWED) for _ in range(stories))
        incident = rng.random() < min(0.6, 0.05 * debt)
        carry += bugs * BUG_COST + (INCIDENT_COST if incident else 0.0)
        out["reported"] += reported
        out["f%d" % (sprint // 4 + 1)] += features / 4
        out["bugs"] += bugs
        out["incidents"] += incident
    return out


def main():
    print(f"{SPRINTS} sprints, honest capacity ~{CAPACITY:.0f} points; {TRIALS:,} seeded runs (averages)\n")
    print(f"{'':<23} {'reported':>9}  {'feature work per sprint':^25}  {'escaped':>8} {'incidents':>10} {'debt work':>10}")
    print(f"{'policy':<23} {'/sprint':>9}  {'1-4':>7} {'5-8':>8} {'9-12':>8}  {'bugs':>8} {'':>10} {'points':>10}")
    for policy, label in (("plan", "velocity for planning"), ("target", "target of 45 points")):
        rng = random.Random(42)
        tot = dict(reported=0.0, f1=0.0, f2=0.0, f3=0.0, bugs=0, incidents=0, debtwork=0.0)
        for _ in range(TRIALS):
            for k, v in run(policy, rng).items():
                tot[k] += v
        a = {k: v / TRIALS for k, v in tot.items()}
        print(f"{label:<23} {a['reported'] / SPRINTS:>9.1f}  {a['f1']:>7.1f} {a['f2']:>8.1f} {a['f3']:>8.1f}  "
              f"{a['bugs']:>8.1f} {a['incidents']:>10.1f} {a['debtwork']:>10.1f}")


if __name__ == "__main__":
    main()
