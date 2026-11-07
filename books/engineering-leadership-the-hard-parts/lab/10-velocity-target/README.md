# Velocity target

What does a team actually deliver once velocity becomes a target? The script simulates twelve sprints of a team that honestly does about 30 points of work a sprint, run two ways: planning with velocity, or told to report 45 points — the jump the board demanded of April's team.

*Illustrates Engineering Leadership: The Hard Parts, “Velocity: The Most Misused Metric in Software”, pp. 215–216, and Goodhart's Law, p. 219. The implementation is the vault’s own: the model and all its parameters (25% estimate inflation, 20% effort saved by skipping review and documentation, bug-escape and incident rates, rework costs) are invented to mirror the mechanisms in April's story; the simulation is seeded.*

## Run

Python 3.10+, standard library only, deterministic:

```sh
python3 velocity_target.py
```

## Expected output

```text
12 sprints, honest capacity ~30 points; 2,000 seeded runs (averages)

                         reported   feature work per sprint    escaped  incidents  debt work
policy                    /sprint      1-4      5-8     9-12      bugs                points
velocity for planning        26.6     26.7     26.6     26.5       2.9        0.0       35.5
target of 45 points          38.7     33.1     30.7     29.1      16.8        3.9        0.0
```

## What to look for

- **Reported velocity jumps** from about 27 to about 39 points, but a quarter of that rise is inflated estimates — the same work, relabelled.
- **Real feature work rises at first** (skipping reviews really is faster) and then **declines sprint after sprint**, as escaped bugs and incidents come back as rework. The planning team stays flat.
- The targeted team lets almost six times as many bugs escape and spends nothing on debt, so its incident risk keeps climbing — the six-hour outage in April's story is where this curve leads (p. 219).
- In this model, the planning team's only "cost" is lower reported velocity — which is why the book keeps velocity inside the team as a capacity-planning tool (p. 216).

## Related

- Chapter note: [10. Metrics That Matter for Engineering Teams](../../chapters/10-metrics-that-matter-for-engineering-teams.md) — “Velocity: The Most Misused Metric in Software”, pp. 215–216; “Humans and Metrics”, p. 219
