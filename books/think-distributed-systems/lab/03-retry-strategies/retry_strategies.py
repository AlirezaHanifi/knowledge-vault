"""Retry strategies against transient, intermittent and permanent failures.

Illustrates Think Distributed Systems, Chapter 3, "Failure classification" and
"Failure mitigation" (pp. 47-53). The failure models, timings and strategies'
parameters are the vault's own (seeded); so is the implementation.
"""
import random

TRIALS = 10_000
BUDGET = 30.0  # seconds a step may spend retrying before it escalates


def transient(rng):
    """Each attempt fails independently: P(F2 | F1) = P(F2) = 0.3."""
    return lambda t: rng.random() < 0.3


def intermittent(rng):
    """A failure lingers: an outage lasting Exp(mean 6 s) from t = 0."""
    outage = rng.expovariate(1 / 6)
    return lambda t: t < outage or rng.random() < 0.05


def permanent(rng):
    """Here to stay: P(F2 | F1) = 1 until someone repairs it."""
    return lambda t: True


def no_retry(n, rng):
    return None


def immediate(n, rng):
    return 0.01 if n < 5 else None


def fixed(n, rng):
    return 1.0 if n < 8 else None


def exponential(n, rng):
    """Capped exponential backoff with full jitter: U(0, min(8, 0.5 * 2^n))."""
    return rng.uniform(0, min(8.0, 0.5 * 2 ** n)) if n < 12 else None


def run(failure, strategy, seed):
    rng = random.Random(seed)
    ok, attempts, times = 0, 0, []
    for _ in range(TRIALS):
        fails = failure(rng)
        t, n = 0.0, 0
        while True:
            n += 1
            if not fails(t):
                ok += 1
                times.append(t)
                break
            wait = strategy(n, rng)
            if wait is None or t + wait > BUDGET:
                break
            t += wait
        attempts += n
    mean_t = sum(times) / len(times) if times else float("nan")
    return ok / TRIALS, attempts / TRIALS, mean_t


def main():
    failures = [("transient", transient), ("intermittent", intermittent), ("permanent", permanent)]
    strategies = [("no retry", no_retry), ("immediate x5", immediate),
                  ("fixed 1 s x8", fixed), ("exp. backoff", exponential)]
    print(f"{TRIALS:,} trials per cell; a step gives up after {BUDGET:.0f} s of retrying\n")
    print(f"{'failure':<13} {'strategy':<14} {'success':>8} {'attempts':>9} {'time to success':>16}")
    for i, (fname, f) in enumerate(failures):
        for j, (sname, s) in enumerate(strategies):
            succ, att, t = run(f, s, seed=100 * i + j)
            ts = "—" if t != t else f"{t:.2f} s"
            print(f"{fname:<13} {sname:<14} {succ:>8.1%} {att:>9.2f} {ts:>16}")
        print()


if __name__ == "__main__":
    main()
