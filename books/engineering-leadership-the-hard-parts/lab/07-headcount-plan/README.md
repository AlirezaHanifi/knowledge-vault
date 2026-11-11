# Headcount plan

What do three engineering hires really cost, and how much do they add in their first year? The script applies the book's rules of thumb for fully loaded cost to April's three $150,000 hires, then compares hiring all three at once with staggering them, using the book's ramp-up figures.

*Illustrates Engineering Leadership: The Hard Parts, “Headcount Planning and Costs”, pp. 133–136. The implementation is the vault’s own: the existing team of ten and the hiring months are assumptions; the cost ranges, ramp-up and drag figures are the book's; the calculation is deterministic.*

## Run

Python 3.10+, standard library only, deterministic:

```sh
python3 headcount_plan.py
```

## Expected output

```text
3 hires at $150,000 base; existing team of 10

case     per hire  x base  three hires  vs $450,000 budget
low       220,975    1.47      662,925            +212,925
high      258,975    1.73      776,925            +326,925

Year-one capacity (engineer-months; no hires = 120)
plan                          delivered   added  worst month
batch (all in month 1)            147.0   +27.0         70%
staggered (months 1, 3, 5)        141.0   +21.0         90%

Attrition at 10-15% a year on 13 people: 1.3-1.9 backfills a year
```

## What to look for

- Both ends of the book's ranges land inside its 1.3–1.8× rule, and the low end is close to the book's "closer to $675,000" for April's three hires (p. 134) — a budget of $450,000 is short by a third or more.
- "Worst month" is the existing team's capacity in its hardest month. Batch hiring drops it to 70% in month 1 (three hires × 10% drag), the onboarding bottleneck the book warns about (p. 134); staggering never goes below 90%.
- Batch hiring still delivers more over the year, because the hires ramp up sooner. Three hires add roughly two engineers' worth of output in year one, not three.
- Attrition means some of next year's hiring is replacement, not growth.

## Related

- Chapter note: [7. Budgeting, Costs, and Vendors](../../chapters/07-budgeting-costs-and-vendors.md) — “Headcount Planning and Costs”, pp. 133–136
