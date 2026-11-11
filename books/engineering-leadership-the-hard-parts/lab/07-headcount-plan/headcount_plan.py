"""Headcount plan: what three engineering hires really cost, and what they add in year one.

Illustrates Engineering Leadership: The Hard Parts, Chapter 7, "Headcount Planning and Costs"
(pp. 133-136): fully loaded cost is typically 1.3-1.8x base salary (US payroll taxes about 7.65%,
benefits 20-30%, equipment $5,000-$10,000, training $2,000-$5,000, recruiting fees 15-25% of base);
new hires work at about 50% productivity for three months; each new hire reduces team capacity by
10% in their first month and 5% in their second; attrition runs 10-15% a year. April budgets three
engineers at $150,000 each. The team size and hiring months are the vault's assumptions; the
calculation is deterministic.
"""
BASE = 150_000
HIRES = 3
TEAM = 10                       # vault assumption: existing engineers
PAYROLL_TAX = 0.0765

# (label, benefits share, equipment, training, recruiting share) at the low and high ends of the book's ranges
CASES = [("low", 0.20, 5_000, 2_000, 0.15), ("high", 0.30, 10_000, 5_000, 0.25)]

PLANS = {"batch (all in month 1)": [1, 1, 1], "staggered (months 1, 3, 5)": [1, 3, 5]}


def loaded_cost(benefits, equipment, training, recruiting):
    return BASE * (1 + PAYROLL_TAX + benefits) + equipment + training + BASE * recruiting


def capacity(start_months):
    """Engineer-months delivered over 12 months by the existing team plus the hires."""
    total, worst = 0.0, 1.0
    for month in range(1, 13):
        drag, hires_output = 0.0, 0.0
        for start in start_months:
            age = month - start + 1          # 1 = the hire's first month
            if age < 1:
                continue
            drag += {1: 0.10, 2: 0.05}.get(age, 0.0)
            hires_output += 0.5 if age <= 3 else 1.0
        team_factor = max(0.0, 1 - drag)
        worst = min(worst, team_factor)
        total += TEAM * team_factor + hires_output
    return total, worst


def main():
    print(f"{HIRES} hires at ${BASE:,} base; existing team of {TEAM}\n")
    print(f"{'case':<6} {'per hire':>10} {'x base':>7} {'three hires':>12} {'vs $450,000 budget':>19}")
    for label, *parts in CASES:
        one = loaded_cost(*parts)
        print(f"{label:<6} {one:>10,.0f} {one / BASE:>7.2f} {one * HIRES:>12,.0f} {one * HIRES - BASE * HIRES:>+19,.0f}")

    print(f"\nYear-one capacity (engineer-months; no hires = {TEAM * 12})")
    print(f"{'plan':<28} {'delivered':>10} {'added':>7} {'worst month':>12}")
    for name, starts in PLANS.items():
        total, worst = capacity(starts)
        print(f"{name:<28} {total:>10.1f} {total - TEAM * 12:>+7.1f} {worst:>11.0%}")

    team = TEAM + HIRES
    print(f"\nAttrition at 10-15% a year on {team} people: {team * 0.10:.1f}-{team * 0.15:.1f} backfills a year")


if __name__ == "__main__":
    main()
