"""Single gate vs. triple modular redundancy with majority voting.

Illustrates Think Distributed Systems, Chapter 8, "Redundancy" (pp. 107-108,
Figure 8.1): three replicas coordinated by R = (a & b) | (b & c) | (a & c), with
the majority gate itself replicated. The failure model (each component is right
with probability p, independently) and the trial counts are the vault's.
"""
import random

TRIALS = 200_000


def maj(a, b, c):
    return (a and b) or (b and c) or (a and c)


def trial(rng, p):
    gates = [rng.random() < p for _ in range(3)]          # True = this gate is right
    m = maj(*gates)                                        # what a perfect voter outputs
    one_voter = m if rng.random() < p else not m
    voters = [m if rng.random() < p else not m for _ in range(3)]
    return gates[0], m, one_voter, maj(*voters)


def main():
    print(f"{TRIALS:,} trials per row; a component is right with probability p\n")
    print(f"{'p':>6} {'single':>9} {'3p²−2p³':>9} {'TMR, perfect voter':>19} {'TMR, 1 voter':>13} {'TMR, 3 voters':>14}")
    for i, p in enumerate([0.4, 0.5, 0.7, 0.9, 0.95, 0.99, 0.999]):
        rng = random.Random(1000 + i)
        s = [0, 0, 0, 0]
        for _ in range(TRIALS):
            for k, ok in enumerate(trial(rng, p)):
                s[k] += ok
        f = 3 * p * p - 2 * p ** 3
        print(f"{p:>6} {s[0] / TRIALS:>9.4f} {f:>9.4f} {s[1] / TRIALS:>19.4f} {s[2] / TRIALS:>13.4f} {s[3] / TRIALS:>14.4f}")


if __name__ == "__main__":
    main()
