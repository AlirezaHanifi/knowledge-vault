"""Cost of removing one user's personal data: Vertical Partitioner vs In-Place Overwriter.

Illustrates Data Engineering Design Patterns, Chapter 7, "Data Removal"
(pp. 198-207). With a Vertical Partitioner, personal attributes live once per
user in a separate table, so a removal deletes one row. An In-Place Overwriter
has to rewrite every file that holds one of the user's records; the book's
example is a user with 2,000 records (p. 205). File sizes, the number of users
and visits are synthetic and seeded; the code is the vault's own.
"""

import random

random.seed(7)
USERS, DAYS, FILES_PER_DAY = 5_000, 90, 4
ROW_BYTES, CONTEXT_BYTES = 300, 120

# visits per user: most users visit a little, a few heavy users visit a lot
visits = {u: max(1, int(random.paretovariate(1.3) * 15)) for u in range(USERS)}
visits[0] = 2_000                                   # the book's example user
files = {}                                          # (day, file) -> {user: rows}
for u, n in visits.items():
    for _ in range(n):
        f = (random.randrange(DAYS), random.randrange(FILES_PER_DAY))
        files.setdefault(f, {}).setdefault(u, 0)
        files[f][u] += 1
rows_total = sum(visits.values())
file_rows = {f: sum(c.values()) for f, c in files.items()}
CONTEXT_FILES = 20
context_file_rows = USERS / CONTEXT_FILES


def in_place(users):
    touched = {f for f, c in files.items() if any(u in c for u in users)}
    rewritten = sum(file_rows[f] for f in touched)
    deleted = sum(visits[u] for u in users)
    return deleted, len(touched), rewritten


def vertical(users):
    touched = {u % CONTEXT_FILES for u in users}
    return len(users), len(touched), int(len(touched) * context_file_rows)


print(f"Visits dataset: {rows_total:,} rows in {len(files)} files ({DAYS} days x {FILES_PER_DAY} files)")
print(f"User context table (Vertical Partitioner): {USERS:,} rows in {CONTEXT_FILES} files\n")

print("Removing user 0 (2,000 visits)")
print(f"  {'':<22}{'rows deleted':>14}{'files rewritten':>17}{'rows rewritten':>16}{'MB written':>12}")
for name, fn, size in (("In-Place Overwriter", in_place, ROW_BYTES), ("Vertical Partitioner", vertical, CONTEXT_BYTES)):
    d, f, r = fn([0])
    print(f"  {name:<22}{d:>14,}{f:>17,}{r:>16,}{r * size / 1e6:>12.2f}")

typical = sorted(visits, key=visits.get)[USERS // 2]
d, f, r = in_place([typical])
print(f"\nA median user ({visits[typical]} visits) still makes the In-Place Overwriter rewrite {f} files ({r:,} rows)")

batch = random.sample(range(1, USERS), 100)
one_by_one = sum(in_place([u])[2] for u in batch)
together = in_place(batch)[2]
print("\n100 removal requests, In-Place Overwriter")
print(f"  processed one by one:   {one_by_one:,} rows rewritten")
print(f"  batched into one run:   {together:,} rows rewritten ({one_by_one / together:.1f}x less)")
