"""Duplication drift: a fact copied into k places, changed over time by developers who sometimes miss a copy.

Illustrates The Pragmatic Programmer, Topic 9 (DRY, pp. 79-81). The model and numbers are the vault's.
"""
import random

CHANGES = 20          # times the fact changes during the project
TRIALS = 10_000
MISS = 0.10           # chance a developer forgets one particular copy when changing the fact


def run(copies: int, rng: random.Random) -> tuple[int, int]:
    """Return (changes after which some copy disagreed, copies still wrong at the end)."""
    values = [0] * copies
    inconsistent = 0
    for change in range(1, CHANGES + 1):
        for i in range(copies):
            # the authoritative copy (index 0) is always updated; the others may be missed
            if i == 0 or rng.random() >= MISS:
                values[i] = change
        if len(set(values)) > 1:
            inconsistent += 1
    stale = sum(1 for v in values if v != CHANGES)
    return inconsistent, stale


def main() -> None:
    rng = random.Random(15)
    print(f"{TRIALS:,} projects per row; the fact changes {CHANGES} times; each extra copy is missed {MISS:.0%} of the time\n")
    print(f"{'copies':>6}  {'changes with a contradiction':>29}  {'projects ending inconsistent':>29}")
    for copies in (1, 2, 3, 5, 8):
        tot_inc = ended_bad = 0
        for _ in range(TRIALS):
            inc, stale = run(copies, rng)
            tot_inc += inc
            ended_bad += stale > 0
        print(f"{copies:>6}  {tot_inc / TRIALS / CHANGES:>29.1%}  {ended_bad / TRIALS:>29.1%}")
    print("\nOnce a copy is missed it stays wrong until a later change happens to reach it.")


if __name__ == "__main__":
    main()
