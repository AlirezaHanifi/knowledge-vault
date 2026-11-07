# Parallel plan: the cost of waiting for the API

A small launch — design an API, build it, build the frontend, integrate, test and launch — is scheduled twice. In the first plan the frontend waits for the real API. In the second, the team spends a day agreeing the JSON format first, so the frontend codes against dummy objects while the API is built, and integration is shorter. The script prints each plan's most likely length and critical path, then repeats both with uncertain task durations.

*Illustrates The Manager's Path, “The Main Roles of a Tech Lead”, p. 32. The implementation is the vault’s own: the tasks, durations and uncertainty are invented, and durations are drawn from a seeded triangular distribution.*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 parallel_plan.py
```

## Expected output

```text
Most likely durations (working days)

Wait for the API              24 days   critical path: design API -> build API -> build frontend -> integrate -> test and launch
Agree JSON contract first     17 days   critical path: design API -> agree JSON format -> build API -> integrate -> test and launch

10,000 seeded trials with uncertain durations

plan                         median  90th pct
Wait for the API               27.2      30.9
Agree JSON contract first      19.8      22.5
```

## What to look for

- Waiting puts the frontend on the critical path: its seven days are added to the API's eight.
- With an agreed contract, the frontend drops off the critical path; the API alone sets the pace, and a day of agreement buys about a week.
- The gap holds when durations are uncertain, and the plan's 90th percentile improves as much as its median. The numbers depend entirely on the invented tasks; the shape of the argument is the book's.

## Related

- Chapter note: [3. Tech Lead](../../chapters/03-tech-lead.md) — “The Main Roles of a Tech Lead”, p. 32
