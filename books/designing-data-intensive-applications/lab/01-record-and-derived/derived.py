"""Chapter 1 in real SQL: OLTP vs OLAP, systems of record vs derived data, and erasure.

Runs on Python's built-in sqlite3, in memory, with seeded data, so the output is the
same on every run. It counts rows touched, never time, because counts don't depend
on the machine.

    python3 derived.py
"""
import random
import sqlite3

random.seed(1)
STORES = ["north", "centre", "south"]
PRODUCTS = ["bananas", "bread", "milk", "diapers", "baby food"]

db = sqlite3.connect(":memory:")
touched = 0


def touch(_):
    """Called once for every row a query actually examines."""
    global touched
    touched += 1
    return 1


db.create_function("touch", 1, touch, deterministic=False)


def run(sql, *args):
    global touched
    touched = 0
    rows = db.execute(sql, args).fetchall()
    return rows, touched


print("1. Point query vs analytical query (pp. 5-6)")
db.execute("""CREATE TABLE sales (id INTEGER PRIMARY KEY, store TEXT, customer INTEGER,
              product TEXT, month TEXT, amount INTEGER)""")
for i in range(1, 20_001):
    db.execute("INSERT INTO sales VALUES (?, ?, ?, ?, ?, ?)",
               (i, random.choice(STORES), random.randint(1, 2_000), random.choice(PRODUCTS),
                f"2026-{random.randint(1, 3):02d}", random.randint(1, 40)))
rows, n = run("SELECT * FROM sales WHERE id = ? AND touch(id)", 4217)
print(f"   OLTP: fetch sale #4217 by key           -> {len(rows)} row returned,  {n:>6,} row touched")
rows, n = run("""SELECT store, SUM(amount) FROM sales WHERE touch(id) AND month = '2026-01'
                 GROUP BY store ORDER BY store""")
print(f"   OLAP: revenue per store in January      -> {len(rows)} rows returned, {n:>6,} rows touched")
for store, total in rows:
    print(f"         {store:<7} {total:>7,}")
print("   One query asks for one record and reads one; the other asks for three numbers and reads them all.")

print()
print("2. Systems of record and derived data (pp. 10-11)")
db.execute("""CREATE TABLE revenue_by_store_month AS
              SELECT store, month, SUM(amount) AS revenue FROM sales GROUP BY store, month""")
first = db.execute("SELECT * FROM revenue_by_store_month ORDER BY store, month").fetchall()
db.execute("DROP TABLE revenue_by_store_month")
print("   Derived table dropped: the system of record still has every sale.")
db.execute("""CREATE TABLE revenue_by_store_month AS
              SELECT store, month, SUM(amount) AS revenue FROM sales GROUP BY store, month""")
again = db.execute("SELECT * FROM revenue_by_store_month ORDER BY store, month").fetchall()
print(f"   Rebuilt from the source: {len(again)} rows, identical to before: {again == first}")
db.execute("UPDATE sales SET amount = amount + 100 WHERE id = 4217")
stale = db.execute("SELECT SUM(revenue) FROM revenue_by_store_month").fetchone()[0]
truth = db.execute("SELECT SUM(amount) FROM sales").fetchone()[0]
print(f"   After one source update: derived total {stale:,}, source total {truth:,} "
      f"(stale by {truth - stale}) until something rebuilds it.")

print()
print("3. Erasing one customer (pp. 24-25)")
CUSTOMER = 417
db.execute("CREATE TABLE sales_log AS SELECT * FROM sales")          # append-only history
db.execute("CREATE TABLE export_2026_02 AS SELECT * FROM sales WHERE customer = ?", (CUSTOMER,))  # a CSV someone kept


def rebuild():
    db.execute("DROP TABLE IF EXISTS customer_profile")
    db.execute("""CREATE TABLE customer_profile AS
                  SELECT customer, COUNT(*) AS visits, SUM(amount) AS spend
                  FROM sales_log GROUP BY customer""")


def copies():
    found = {}
    for table in ["sales", "sales_log", "customer_profile", "export_2026_02"]:
        found[table] = db.execute(f"SELECT COUNT(*) FROM {table} WHERE customer = ?", (CUSTOMER,)).fetchone()[0]
    return found


def show(step):
    found = copies()
    left = ", ".join(f"{t} {c}" for t, c in found.items() if c) or "none"
    print(f"   {step:<44} rows still about #{CUSTOMER}: {left}")


rebuild()
show("Before:")
db.execute("DELETE FROM sales WHERE customer = ?", (CUSTOMER,))
show("Deleted from the system of record:")
rebuild()
show("Rebuilt the derived profile from the log:")
db.execute("DELETE FROM sales_log WHERE customer = ?", (CUSTOMER,))
rebuild()
show("Rewrote the log, rebuilt again:")
db.execute("DROP TABLE export_2026_02")
db.execute("CREATE TABLE export_2026_02 (customer INTEGER)")
show("Found and deleted the exported snapshot:")
