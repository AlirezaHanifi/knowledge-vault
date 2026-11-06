# Duplication drift

What does it cost to keep one piece of knowledge in several places? A fact (a tax rate, say) lives in *k* copies and changes 20 times during a project. At each change, the authoritative copy is always updated, but a developer misses each other copy with probability 10%. The script counts how often the copies contradict each other, and how many projects end with a stale copy, for 1 to 8 copies.

*Illustrates The Pragmatic Programmer, Topic 9, DRY—The Evils of Duplication, pp. 79–81: with two copies, the question isn't whether you'll forget to change one, but when. The miss rate, the number of changes and the model are the vault's (seeded).*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 duplication_drift.py
```

## Expected output

```text
10,000 projects per row; the fact changes 20 times; each extra copy is missed 10% of the time

copies   changes with a contradiction   projects ending inconsistent
     1                           0.0%                           0.0%
     2                          10.0%                           9.6%
     3                          19.0%                          18.8%
     5                          34.4%                          34.5%
     8                          52.3%                          52.2%

Once a copy is missed it stays wrong until a later change happens to reach it.
```

## What to look for

- With a single authoritative copy there is never a contradiction: that is the DRY principle doing its job.
- Each extra copy adds roughly another 10% chance per change of a contradiction. Eight copies disagree after about half of all changes.
- A missed copy stays wrong until some later change happens to reach it, so most of the damage lasts until the end of the project.
- The fix the book recommends isn't more care: it's removing the copies, or generating them from one source.

## Related

- Chapter note: [2. A Pragmatic Approach](../../chapters/02-a-pragmatic-approach.md) — Topic 9, DRY, pp. 79–81
