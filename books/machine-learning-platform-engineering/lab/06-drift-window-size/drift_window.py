"""False drift alarms versus window size.

Draws "current" windows from the very same distributions as the reference
data, so every drift flag is a false alarm, and then shifts one distribution
to see how quickly a real drift is caught. Standard library only, seeded.
"""
import bisect
import random
import statistics

SEED, REF_SIZE, REPS, THRESHOLD = 7, 2000, 60, 0.1
WINDOWS = [10, 25, 50, 100, 250, 500, 1000]

# Eight numeric columns with different shapes (the vault's own stand-ins).
COLUMNS = {
    "age": lambda r: round(r.gauss(39, 13)),
    "hours": lambda r: round(min(99, max(1, r.gauss(40, 12)))),
    "income": lambda r: r.lognormvariate(10.5, 0.6),
    "tenure": lambda r: r.expovariate(1 / 6),
    "score": lambda r: r.uniform(0, 1),
    "visits": lambda r: int(r.expovariate(1 / 3)),
    "basket": lambda r: r.lognormvariate(3, 1.0),
    "rating": lambda r: r.choice([1, 2, 3, 3, 4, 4, 4, 5, 5]),
}


def wasserstein(ref, cur):
    """W1 between two empirical distributions: integral of |F_ref - F_cur|."""
    xs = sorted(set(ref) | set(cur))
    n, m, total = len(ref), len(cur), 0.0
    for a, b in zip(xs, xs[1:]):
        f = bisect.bisect_right(ref, a) / n
        g = bisect.bisect_right(cur, a) / m
        total += abs(f - g) * (b - a)
    return total


def score(ref, sd, cur):
    # Divided by the reference's standard deviation so 0.1 means the same on every column.
    return wasserstein(ref, sorted(cur)) / sd


def main():
    rng = random.Random(SEED)
    ref = {c: sorted(f(rng) for _ in range(REF_SIZE)) for c, f in COLUMNS.items()}
    sd = {c: statistics.pstdev(v) for c, v in ref.items()}

    print(f"reference: {REF_SIZE} rows x {len(COLUMNS)} columns; drift if normalised Wasserstein > {THRESHOLD}")
    print(f"{REPS} windows per size, drawn from the SAME distributions (every flag is false)\n")
    print("window  mean share of drifted columns  windows with share >= 0.5")
    for w in WINDOWS:
        shares = []
        for _ in range(REPS):
            flagged = sum(score(ref[c], sd[c], [f(rng) for _ in range(w)]) > THRESHOLD for c, f in COLUMNS.items())
            shares.append(flagged / len(COLUMNS))
        print(f"{w:>6}  {statistics.mean(shares):>29.3f}  {sum(s >= 0.5 for s in shares) / REPS:>26.0%}")

    print("\none column, 'age': no drift versus a real shift of +0.25 standard deviations")
    print("window  flagged without drift  flagged with real drift")
    shift, age = 0.25 * sd["age"], COLUMNS["age"]
    for w in WINDOWS:
        false = sum(score(ref["age"], sd["age"], [age(rng) for _ in range(w)]) > THRESHOLD for _ in range(REPS))
        true = sum(score(ref["age"], sd["age"], [age(rng) + shift for _ in range(w)]) > THRESHOLD for _ in range(REPS))
        print(f"{w:>6}  {false / REPS:>21.0%}  {true / REPS:>23.0%}")


if __name__ == "__main__":
    main()
