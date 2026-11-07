"""Skip-level load: the time quarterly skip-level 1-1s and team lunches take, by organization size.

Illustrates The Manager's Path, Chapter 7, "Skip-Level Meetings" (pp. 128-129): with about 60 working
days in a quarter, one 1-1 per person per quarter means one a day at 60 people, and at 1,000 people
you'd do nothing else in a 40-hour week. The author's alternative is skip-level lunches with whole
teams, a couple of times a quarter per team. Meeting length, team size and lunch length are the
vault's assumptions; the arithmetic is deterministic.
"""
WORKING_DAYS = 60          # per quarter (the book's figure)
WEEKS = 12                 # the book's "five a week for 12 weeks"
ONE_ON_ONE_H = 0.5         # vault assumption: 30-minute skip-levels
TEAM_SIZE = 7              # vault assumption
LUNCHES_PER_TEAM = 2       # "a couple of times a quarter for each team"
LUNCH_H = 1.0              # vault assumption
WORK_WEEK_H = 40


def main():
    print(f"Quarter: {WORKING_DAYS} working days, {WEEKS} weeks; 1-1s {ONE_ON_ONE_H * 60:.0f} min; "
          f"teams of {TEAM_SIZE}, {LUNCHES_PER_TEAM} lunches/team/quarter, {LUNCH_H:.0f} h each\n")
    print(f"{'people':>7} {'1-1s/day':>9} {'1-1 h/week':>11} {'% of 40 h':>10} {'lunch h/week':>13} {'% of 40 h':>10}")
    for n in (15, 30, 60, 120, 250, 500, 1000):
        per_day = n / WORKING_DAYS
        h_week = n * ONE_ON_ONE_H / WEEKS
        teams = -(-n // TEAM_SIZE)
        lunch_week = teams * LUNCHES_PER_TEAM * LUNCH_H / WEEKS
        print(f"{n:>7,} {per_day:>9.2f} {h_week:>11.1f} {h_week / WORK_WEEK_H:>10.0%} "
              f"{lunch_week:>13.1f} {lunch_week / WORK_WEEK_H:>10.0%}")


if __name__ == "__main__":
    main()
