# Focus versus spread

Twelve engineers share a backlog of 30 priorities, each of uncertain size. A priority delivers value only once it is finished. The team keeps a fixed number of priorities open at a time — all 30, or 12, 6 or 3 — and starts the next whenever one finishes; capacity is split evenly over the open ones, and every extra priority an engineer juggles costs them focus. The script counts what is finished after one and two quarters, and how many weeks of use the finished work gets.

*Illustrates Engineering Leadership: The Hard Parts, “What Good Direction Looks Like” and the Stripe LATAM story, pp. 75–76, 78–80. The implementation is the vault’s own: the team, the priority sizes, the switching cost and “value-weeks” are invented (seeded).*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 focus_vs_spread.py
```

## Expected output

```text
12 engineers, backlog of 30 priorities (4-16 engineer-weeks each), 26 weeks; 2,000 seeded trials

open at once  focus  first done  done by wk 13  done by wk 26  value-weeks
          30    85%        13.3            1.1           16.4           94
          12   100%         5.5            9.9           27.3          263
           6   100%         3.4           12.0           26.5          301
           3   100%         2.3           12.1           25.1          302
```

## What to look for

- **With all 30 open, almost nothing finishes in the first quarter** — about one priority — even though everyone is busy the whole time. That is drift as the book describes it: activity that doesn't compound.
- **With six open, the first priority lands in about three weeks** and twelve are done by the end of the quarter; finished work starts delivering value months earlier (value-weeks roughly triple).
- Past a point, fewer open priorities stop helping much in this model (6 and 3 are close). The book's choice of two per team is a judgement about focus and coordination; the toy model only shows why far fewer than 30 is better.

## Related

- Chapter note: [5. Setting Direction](../../chapters/05-setting-direction.md) — “What Good Direction Looks Like”, pp. 79–81
