"""Focus versus spread: the same team and backlog, 30 priorities open at once or 6.

Illustrates Engineering Leadership: The Hard Parts, Chapter 5 (pp. 75-76, 78): the Stripe LATAM team
cut 30 competing priorities to 6 (two per team), and work "started compounding instead of scattering."
The model is the vault's own: 12 engineers share a backlog of 30 priorities of uncertain size. A
priority delivers value only once it is finished. The team keeps a limited number open at a time
and starts the next when one finishes; every extra priority an engineer juggles costs focus.
Seeded randomness.
"""
import random

ENGINEERS = 12
WEEKS = 26                      # two quarters
SWITCH_COST = 0.10              # share of a week lost per extra priority each engineer juggles
TRIALS = 2000


def run(open_limit: int, rng: random.Random):
    backlog = [rng.uniform(4, 16) for _ in range(30)]    # engineer-weeks each
    active = [backlog.pop() for _ in range(min(open_limit, len(backlog)))]
    juggled = max(1.0, open_limit / ENGINEERS)
    focus = max(0.3, 1 - SWITCH_COST * (juggled - 1))
    finished_weeks = []
    for week in range(1, WEEKS + 1):
        share = ENGINEERS * focus / len(active) if active else 0
        still = []
        for left in active:
            left -= share
            if left <= 0:
                finished_weeks.append(week)
            else:
                still.append(left)
        active = still
        while len(active) < open_limit and backlog:
            active.append(backlog.pop())
    q1 = sum(w <= 13 for w in finished_weeks)
    value_weeks = sum(WEEKS - w for w in finished_weeks)  # weeks each finished priority was in use
    first = finished_weeks[0] if finished_weeks else WEEKS + 1
    return q1, len(finished_weeks), first, value_weeks, focus


def main():
    rng = random.Random(30)
    print(f"{ENGINEERS} engineers, backlog of 30 priorities (4-16 engineer-weeks each), {WEEKS} weeks; "
          f"{TRIALS:,} seeded trials\n")
    print(f"{'open at once':>12} {'focus':>6} {'first done':>11} {'done by wk 13':>14} {'done by wk 26':>14} {'value-weeks':>12}")
    for k in (30, 12, 6, 3):
        runs = [run(k, rng) for _ in range(TRIALS)]
        avg = [sum(r[i] for r in runs) / TRIALS for i in range(5)]
        print(f"{k:>12} {avg[4]:>6.0%} {avg[2]:>11.1f} {avg[0]:>14.1f} {avg[1]:>14.1f} {avg[3]:>12.0f}")


if __name__ == "__main__":
    main()
