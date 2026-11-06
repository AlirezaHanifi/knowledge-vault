"""How long should an iteration be? A client whose wishes drift, and work wasted between feedback points.

Illustrates The Pragmatic Programmer, Topic 45 (short iterations that end with client feedback minimize
time lost in a wrong direction, p. 410) and Topic 48's agile loop (pp. 431-432). The model is the vault's:
the client's target is a point that drifts by a random walk; the team builds toward its last known
position and only learns the new one at each feedback point. Each feedback point costs time.
"""
import math
import random

WEEKS = 52
DAYS = WEEKS * 5
TRIALS = 500
FEEDBACK_COST = 0.25   # days per feedback session


def run(iteration_days: int, drift: float, rng: random.Random) -> tuple[float, float]:
    target = [0.0, 0.0]
    aim = [0.0, 0.0]
    useful = wasted = 0.0
    for day in range(DAYS):
        if day % iteration_days == 0:
            aim = list(target)                          # feedback: learn where the client wants to go now
            wasted += FEEDBACK_COST
        target[0] += rng.gauss(0, drift)
        target[1] += rng.gauss(0, drift)
        miss = math.dist(aim, target)
        value = max(0.0, 1.0 - miss)                    # a day's work is worth less the further the aim is off
        useful += value
        wasted += 1.0 - value
    return useful, wasted


def main():
    rng = random.Random(45)
    print(f"{TRIALS:,} simulated one-year projects per cell ({DAYS} working days); feedback costs {FEEDBACK_COST} day each\n")
    lengths = (1, 5, 10, 20, 60, 130)
    print(f"{'drift / day':>11}" + "".join(f"{str(n) + ' d':>9}" for n in lengths) + "   (share of days wasted)")
    for drift in (0.01, 0.03, 0.06):
        row = []
        for n in lengths:
            w = sum(run(n, drift, rng)[1] for _ in range(TRIALS))
            row.append(w / (TRIALS) / (DAYS + DAYS / n * FEEDBACK_COST))
        best = lengths[row.index(min(row))]
        print(f"{drift:>11}" + "".join(f"{x:>9.1%}" for x in row) + f"   best: {best} d")


if __name__ == "__main__":
    main()
