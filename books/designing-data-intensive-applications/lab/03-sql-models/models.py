"""Chapter 3 in real SQL: N+1, join fan-out, graph traversal, cycles, schema-on-read.

Runs on Python's built-in sqlite3, in memory. Deterministic: no randomness, no clock.
Illustrates DDIA 2nd ed., Chapter 3; the implementation and toy data are the vault's own.
"""
import json
import sqlite3


class Counting(sqlite3.Connection):
    """A connection that counts the SELECT statements it runs."""
    queries = 0


def connect():
    db = sqlite3.connect(":memory:", factory=Counting)

    def count(statement):
        if statement.lstrip().upper().startswith(("SELECT", "WITH")):
            db.queries += 1

    db.set_trace_callback(count)
    return db


def heading(title):
    print()
    print(title)
    print("-" * len(title))


# 1. N+1 queries (p. 69) ---------------------------------------------------------------
def n_plus_one():
    heading("1. N+1 queries versus one join (p. 69)")
    db = connect()
    db.execute("CREATE TABLE users (user_id INTEGER PRIMARY KEY, name TEXT)")
    db.execute("CREATE TABLE comments (comment_id INTEGER PRIMARY KEY, author_id INTEGER, body TEXT)")
    db.executemany("INSERT INTO users VALUES (?, ?)", [(i, f"user{i}") for i in range(1, 11)])
    db.executemany("INSERT INTO comments VALUES (?, ?, ?)",
                   [(c, (c * 7) % 10 + 1, f"comment {c}") for c in range(1, 51)])

    db.queries = 0
    rows = []
    for cid, author_id, body in db.execute("SELECT comment_id, author_id, body FROM comments ORDER BY comment_id").fetchall():
        (name,) = db.execute("SELECT name FROM users WHERE user_id = ?", (author_id,)).fetchone()
        rows.append((cid, name))
    loop_queries = db.queries

    db.queries = 0
    joined = db.execute("""SELECT c.comment_id, u.name FROM comments c
                           JOIN users u ON u.user_id = c.author_id ORDER BY c.comment_id""").fetchall()
    join_queries = db.queries

    print(f"  ORM-style loop: {loop_queries:>3} queries for {len(rows)} comments with their authors")
    print(f"  one join:       {join_queries:>3} query  for {len(joined)} comments with their authors")
    print(f"  same result:    {rows == joined}")


# 2. Join fan-out on a many-to-many relationship (pp. 75-77) ---------------------------
def fan_out():
    heading("2. Many-to-many join fan-out (pp. 75-77)")
    db = connect()
    db.execute("CREATE TABLE transactions (tx_id TEXT, account_id TEXT, amount INTEGER)")
    db.execute("CREATE TABLE account_holders (account_id TEXT, customer TEXT, is_primary INTEGER)")
    db.executemany("INSERT INTO transactions VALUES (?, ?, ?)", [
        ("T1", "A1", 120), ("T2", "A2", 300), ("T3", "A2", 80),
        ("T4", "A3", 500), ("T5", "A3", 200), ("T6", "A1", 50)])
    db.executemany("INSERT INTO account_holders VALUES (?, ?, ?)", [
        ("A1", "Ava", 1), ("A2", "Ben", 1), ("A2", "Cyrus", 0),
        ("A3", "Dana", 1), ("A3", "Eli", 0), ("A3", "Ava", 0)])

    queries = {
        "per account (no join)": "SELECT sum(amount) FROM transactions",
        "per customer, all holders": """SELECT sum(t.amount) FROM transactions t
            JOIN account_holders h ON h.account_id = t.account_id""",
        "per customer, primary only": """SELECT sum(t.amount) FROM transactions t
            JOIN account_holders h ON h.account_id = t.account_id AND h.is_primary = 1""",
        "per customer, split evenly": """SELECT sum(t.amount * 1.0 / n.holders) FROM transactions t
            JOIN account_holders h ON h.account_id = t.account_id
            JOIN (SELECT account_id, count(*) AS holders FROM account_holders GROUP BY account_id) n
              ON n.account_id = t.account_id""",
    }
    (rows_after_join,) = db.execute("""SELECT count(*) FROM transactions t
        JOIN account_holders h ON h.account_id = t.account_id""").fetchone()
    print(f"  6 transactions become {rows_after_join} rows after joining account_holders")
    for label, sql in queries.items():
        (total,) = db.execute(sql).fetchone()
        mark = "ok" if round(total, 6) == 1250 else "WRONG"
        print(f"  {label:<28} total = {round(total, 2):>7g}   {mark}")


# 3. The book's graph query in SQL (Figure 3-6, Example 3-6, pp. 86-92) ----------------
GRAPH_VERTICES = [
    (1, "location", {"name": "North America", "type": "continent"}),
    (2, "location", {"name": "United States", "type": "country"}),
    (3, "location", {"name": "Idaho", "type": "state"}),
    (4, "location", {"name": "Europe", "type": "continent"}),
    (5, "location", {"name": "United Kingdom", "type": "country"}),
    (6, "location", {"name": "England", "type": "country"}),
    (7, "location", {"name": "London", "type": "city"}),
    (8, "location", {"name": "France", "type": "country"}),
    (9, "location", {"name": "Normandy", "type": "region"}),
    (10, "location", {"name": "Manche", "type": "departement"}),
    (11, "location", {"name": "Saint-Lo", "type": "city"}),
    (100, "person", {"name": "Lucy"}),
    (101, "person", {"name": "Alain"}),
]
GRAPH_EDGES = [  # (tail, head, label)
    (3, 2, "within"), (2, 1, "within"), (7, 6, "within"), (6, 5, "within"), (5, 4, "within"),
    (11, 10, "within"), (10, 9, "within"), (9, 8, "within"), (8, 4, "within"),
    (100, 3, "born_in"), (100, 7, "lives_in"), (101, 7, "lives_in"), (101, 11, "born_in"),
    (100, 101, "married"),
]

EXAMPLE_3_6 = """
WITH RECURSIVE
  in_usa(vertex_id) AS (
      SELECT vertex_id FROM vertices
        WHERE label = 'location' AND json_extract(properties, '$.name') = 'United States'
    UNION
      SELECT edges.tail_vertex FROM edges
        JOIN in_usa ON edges.head_vertex = in_usa.vertex_id
        WHERE edges.label = 'within'
  ),
  in_europe(vertex_id) AS (
      SELECT vertex_id FROM vertices
        WHERE label = 'location' AND json_extract(properties, '$.name') = 'Europe'
    UNION
      SELECT edges.tail_vertex FROM edges
        JOIN in_europe ON edges.head_vertex = in_europe.vertex_id
        WHERE edges.label = 'within'
  ),
  born_in_usa(vertex_id) AS (
    SELECT edges.tail_vertex FROM edges
      JOIN in_usa ON edges.head_vertex = in_usa.vertex_id
      WHERE edges.label = 'born_in'
  ),
  lives_in_europe(vertex_id) AS (
    SELECT edges.tail_vertex FROM edges
      JOIN in_europe ON edges.head_vertex = in_europe.vertex_id
      WHERE edges.label = 'lives_in'
  )
SELECT json_extract(vertices.properties, '$.name') FROM vertices
  JOIN born_in_usa     ON vertices.vertex_id = born_in_usa.vertex_id
  JOIN lives_in_europe ON vertices.vertex_id = lives_in_europe.vertex_id;
"""


def graph_query():
    heading("3. Variable-length traversal with WITH RECURSIVE (pp. 90-92)")
    db = connect()
    db.execute("CREATE TABLE vertices (vertex_id INTEGER PRIMARY KEY, label TEXT, properties TEXT)")
    db.execute("""CREATE TABLE edges (edge_id INTEGER PRIMARY KEY, tail_vertex INTEGER, head_vertex INTEGER,
                                      label TEXT, properties TEXT)""")
    db.execute("CREATE INDEX edges_tails ON edges (tail_vertex)")
    db.execute("CREATE INDEX edges_heads ON edges (head_vertex)")
    db.executemany("INSERT INTO vertices VALUES (?, ?, ?)", [(i, l, json.dumps(p)) for i, l, p in GRAPH_VERTICES])
    db.executemany("INSERT INTO edges (tail_vertex, head_vertex, label, properties) VALUES (?, ?, ?, '{}')", GRAPH_EDGES)

    names = dict((i, p["name"]) for i, _, p in GRAPH_VERTICES)
    for start in ("United States", "Europe"):
        found = db.execute("""
            WITH RECURSIVE inside(vertex_id, depth) AS (
                SELECT vertex_id, 0 FROM vertices WHERE json_extract(properties, '$.name') = ?
              UNION
                SELECT e.tail_vertex, inside.depth + 1 FROM edges e
                  JOIN inside ON e.head_vertex = inside.vertex_id WHERE e.label = 'within')
            SELECT vertex_id, depth FROM inside ORDER BY depth, vertex_id""", (start,)).fetchall()
        deepest = max(d for _, d in found)
        print(f"  within {start + ':':<15} {len(found):>2} locations, deepest {deepest} edge{'s' if deepest != 1 else ''} down "
              f"({', '.join(names[v] for v, d in found if d == deepest)})")

    lines = [l for l in EXAMPLE_3_6.strip().splitlines() if l.strip()]
    result = [r[0] for r in db.execute(EXAMPLE_3_6)]
    print(f"  Example 3-6 ({len(lines)} lines of SQL here, comments removed): {result}")
    print("  The Cypher version (Example 3-5) is 4 lines.")


# 4. Cycles: UNION versus UNION ALL ----------------------------------------------------
def cycles():
    heading("4. A cycle in the graph: UNION versus UNION ALL (p. 92)")
    db = connect()
    db.execute("CREATE TABLE transfers (from_account TEXT, to_account TEXT)")
    db.executemany("INSERT INTO transfers VALUES (?, ?)", [
        ("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E"),
        ("E", "A"), ("E", "F"), ("F", "G"), ("G", "H")])

    reach = db.execute("""
        WITH RECURSIVE reach(account) AS (
            SELECT 'A'
          UNION
            SELECT t.to_account FROM transfers t JOIN reach r ON t.from_account = r.account)
        SELECT account FROM reach""").fetchall()
    print(f"  UNION, no limit:        stops by itself; {len(reach)} rows = accounts {''.join(sorted(a for (a,) in reach))}")

    counts = []
    for limit in range(1, 9):
        (n,) = db.execute("""
            WITH RECURSIVE reach(account, hops) AS (
                SELECT 'A', 0
              UNION ALL
                SELECT t.to_account, r.hops + 1 FROM transfers t
                  JOIN reach r ON t.from_account = r.account WHERE r.hops < ?)
            SELECT count(*) FROM reach""", (limit,)).fetchone()
        counts.append(f"{limit}:{n}")
    print(f"  UNION ALL, hop limit -> rows (one per path): {'  '.join(counts)}")

    (n,) = db.execute("""
        WITH RECURSIVE reach(account) AS (
            SELECT 'A'
          UNION ALL
            SELECT t.to_account FROM transfers t JOIN reach r ON t.from_account = r.account
          LIMIT 10000)
        SELECT count(*) FROM reach""").fetchone()
    print(f"  UNION ALL, no hop limit: still going at {n:,} rows; only the safety LIMIT stopped it")


# 5. Schema-on-read: splitting a name field (p. 81) ------------------------------------
def schema_on_read():
    heading("5. Schema-on-read: old and new records side by side (p. 81)")
    db = connect()
    db.execute("CREATE TABLE raw_users (user_id INTEGER, doc TEXT)")  # what a loader lands as JSON
    db.executemany("INSERT INTO raw_users VALUES (?, ?)", [
        (1, json.dumps({"name": "Ada Lovelace"})),
        (2, json.dumps({"name": "Alan Turing"})),
        (3, json.dumps({"first_name": "Grace", "last_name": "Hopper"})),
    ])
    rows = db.execute("""
        SELECT user_id,
               coalesce(json_extract(doc, '$.first_name'),
                        substr(json_extract(doc, '$.name'), 1, instr(json_extract(doc, '$.name'), ' ') - 1))
                 AS first_name,
               CASE WHEN json_extract(doc, '$.first_name') IS NULL THEN 'old format, split at read time'
                    ELSE 'new format, read as is' END AS fmt
        FROM raw_users ORDER BY user_id""").fetchall()
    for user_id, first_name, fmt in rows:
        print(f"  user {user_id}: first_name = {first_name:<6} ({fmt})")


if __name__ == "__main__":
    print("Chapter 3 in SQLite " + sqlite3.sqlite_version.split(".")[0] + ".x")
    n_plus_one()
    fan_out()
    graph_query()
    cycles()
    schema_on_read()
