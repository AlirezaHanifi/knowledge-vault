# Skip-level load

How much of a week do skip-level meetings take as an organization grows? The script works through the book's arithmetic — one short 1-1 per person per quarter, in a quarter of 60 working days and 12 weeks — for organizations from 15 to 1,000 people, and compares the author's alternative: lunch with each whole team a couple of times a quarter.

*Illustrates The Manager's Path, “Skip-Level Meetings”, pp. 128–129. The implementation is the vault’s own: 30-minute 1-1s, teams of seven and one-hour lunches are assumptions; the calculation is deterministic.*

## Run

Python 3.10+, standard library only, deterministic:

```sh
python3 skip_level_load.py
```

## Expected output

```text
Quarter: 60 working days, 12 weeks; 1-1s 30 min; teams of 7, 2 lunches/team/quarter, 1 h each

 people  1-1s/day  1-1 h/week  % of 40 h  lunch h/week  % of 40 h
     15      0.25         0.6         2%           0.5         1%
     30      0.50         1.2         3%           0.8         2%
     60      1.00         2.5         6%           1.5         4%
    120      2.00         5.0        12%           3.0         8%
    250      4.17        10.4        26%           6.0        15%
    500      8.33        20.8        52%          12.0        30%
  1,000     16.67        41.7       104%          23.8        60%
```

## What to look for

- At 60 people the book's "one every day" appears: exactly one 1-1 per working day.
- At 1,000 people, half-hour 1-1s take more than a full 40-hour week — the book's "nothing but these 1-1s."
- Team lunches grow with the number of teams, not people, so they stay affordable longer — at the cost of individual career coaching and candour about managers, which the book notes group settings lose.

## Related

- Chapter note: [7. Managing Managers](../../chapters/07-managing-managers.md) — “Skip-Level Meetings”, pp. 128–129
