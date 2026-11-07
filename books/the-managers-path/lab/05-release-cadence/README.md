# Release cadence and contention

Five engineers each merge one change a day for 120 working days. Each change has a 4% chance of breaking the release. A release ships every change merged since the last one; if the batch holds a broken change, the whole batch waits a day for each broken change to be found and fixed. The script compares weekly and daily releases: how many releases, how many were blocked, how big each batch was, and how long a change waited from merge to production.

*Illustrates The Manager's Path, “Debugging Dysfunctional Teams: The Basics” (not shipping), pp. 79–80. The implementation is the vault’s own: the team, the failure rate and the one-day fix are invented (seeded).*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 release_cadence.py
```

## Expected output

```text
5 engineers, 120 working days, each change broken with p = 0.04; 300 seeded trials

cadence    releases  blocked  changes/release  days merge->prod
weekly         24.0      64%             25.0               3.0
daily         120.0      18%              5.0               0.2
```

## What to look for

- A weekly batch of 25 changes almost always contains someone's broken change, so most weekly releases are blocked: everyone's work waits on one person. That is the "resource contention" the book describes.
- Daily batches are a fifth the size, so far fewer releases are blocked and a blocked one holds back only a day's work.
- Changes reach production in a fraction of a day instead of about three days. Weekly releases also hide the pain the book names (poor tooling, manual testing, oversized features), which this model leaves out.

## Related

- Chapter note: [5. Managing a Team](../../chapters/05-managing-a-team.md) — “Debugging Dysfunctional Teams: The Basics”, pp. 79–80
