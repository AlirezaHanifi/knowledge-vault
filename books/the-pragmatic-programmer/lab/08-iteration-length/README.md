# How long should an iteration be?

The client's real target drifts: a point moving by a random walk. The team builds toward the last position it heard about, and a day's work is worth less the further that aim has drifted from the current target. At each feedback point (the end of an iteration) the team learns the new target, at a cost of a quarter day. The script measures the share of a year's days wasted for iteration lengths from 1 day to half a year, at three rates of drift.

*Illustrates The Pragmatic Programmer, Topic 45 (short iterations that end with direct client feedback minimize the time lost going in the wrong direction, p. 410) and Topic 48's loop of small steps and feedback (pp. 431–432). The drift model, the value function and the feedback cost are entirely the vault's (seeded).*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 iteration_length.py
```

## Expected output

```text
500 simulated one-year projects per cell (260 working days); feedback costs 0.25 day each

drift / day      1 d      5 d     10 d     20 d     60 d    130 d   (share of days wasted)
       0.01    21.0%     6.8%     5.2%     5.1%     6.8%     9.9%   best: 20 d
       0.03    23.0%    10.8%    10.7%    12.7%    19.3%    28.4%   best: 10 d
       0.06    26.0%    16.7%    18.8%    24.4%    37.6%    53.7%   best: 5 d
```

## What to look for

- Very long iterations waste the most: by the time feedback arrives, the team has spent months building toward a target that moved.
- Very short iterations aren't free in this model, because feedback costs time. Daily feedback spends a quarter of every day on it.
- The faster the client's needs drift, the shorter the best iteration: about 20 days at slow drift, 5 days at fast drift. The model only illustrates the book's argument; the numbers depend entirely on its assumptions.

## Related

- Chapter note: [8. Before the Project](../../chapters/08-before-the-project.md) — “Requirements Are a Process”, pp. 409–410
