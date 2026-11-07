---
book: designing-data-intensive-applications
chapter: 7
title: "Sharding"
pages: "251–276"
---

# 7. Sharding

[← 6. Replication](06-replication.md) · [Book](../README.md) · [8. Transactions →](08-transactions.md)

## Summary

When data or query load outgrows one machine, it is split into **shards** (partitions), each a small database of its own, usually also replicated. The goal is to spread data and load evenly and avoid **hot spots**. The chapter compares sharding by **key range** (efficient range scans, risk of hot spots on sequential keys) with sharding by **hash of key** (even spread, no efficient range scans) — including why *hash mod N* is a bad idea and how a fixed number of shards, hash-range sharding, and consistent hashing rebalance with little data movement. It then covers skewed workloads, automatic versus manual rebalancing, **request routing** (often via a coordination service), and the two ways to shard **secondary indexes** (local and global).

## Key takeaways

- **Sharding is for scale; replication is for redundancy** — systems usually combine them, each node holding replicas of several shards (pp. 251–253).
- **Shard only when needed**: it adds complexity, makes cross-shard queries and transactions hard, and is often unnecessary on modern hardware (pp. 253–254).
- **Multitenancy** maps naturally onto sharding — one shard per tenant brings isolation, per-tenant backup, and data residency — but very large tenants may need splitting (pp. 254–255).
- **Key range sharding** supports range scans but hot-spots on sequential keys (timestamps); **hash sharding** spreads keys but scatters ranges (pp. 256–262).
- **Never use hash mod N**: changing N moves almost every key. Use many more shards than nodes, hash ranges that split, or consistent hashing (pp. 258–263).
- **Hashing doesn't fix skew on a single key** (a celebrity); application-level key splitting trades write spreading for read fan-in (pp. 263–264).
- **Local secondary indexes** make writes cheap and reads scatter/gather; **global secondary indexes** make reads cheap and writes multi-shard (pp. 268–271).

## Section outline

*From the book’s own table of contents (PDF bookmarks); printed page numbers.*

- Pros and Cons of Sharding — p. 253
- Sharding for Multitenancy — p. 254
- Sharding of Key-Value Data — p. 255
  - Sharding by Key Range — p. 256
  - Sharding by Hash of Key — p. 258
  - Skewed Workloads and Relieving Hot Spots — p. 263
  - Operations: Automatic Versus Manual Rebalancing — p. 264
- Request Routing — p. 265
- Sharding and Secondary Indexes — p. 268
  - Local Secondary Indexes — p. 268
  - Global Secondary Indexes — p. 270
- Summary — p. 271

## Notes

A distributed database spreads data in two ways: **replication** (copies of the same data, Ch. 6) and **sharding** — splitting data too big, or written too fast, for one node into **shards** (partitions), each record belonging to exactly one. The two combine: each shard is replicated, and a node may lead some shards while following others (Figure 7-1) (pp. 251–252).

![Four nodes each holding leader and follower replicas of shards 1–4; every shard's leader sits on one node and replication streams run to its followers on other nodes](../figures/07-01.png)

*Figure 7-1 (p. 252): each node leads some shards and follows others, so leadership — and write load — is spread across the cluster.*

**Names for a shard** (p. 252): partition (Kafka), range (CockroachDB), region (HBase, TiDB), vBucket (Couchbase), vnode (Riak), token-range (Cassandra), tablet (Bigtable, YugabyteDB, ScyllaDB). In PostgreSQL, *partitioning* splits a table into files on one machine, unlike sharding across machines. “Shard” may come from *Ultima Online*’s shattered crystal, or a lost 1980s acronym. Nothing to do with **network partitions** (Ch. 9).

### Pros and cons of sharding

Sharding is the main tool for **horizontal scaling** of data volume and **write** throughput — read throughput alone can be solved with read replicas (p. 253). It is heavyweight, so avoid it if one machine copes (pp. 253–254):

| Cost | Why |
|---|---|
| Choosing a **partition key** | Records with the same key share a shard; finding a record without it means searching every shard; the scheme is hard to change |
| Relational data | Secondary indexes and joins span shards |
| Cross-shard writes | Need **distributed transactions** — slower, possibly a bottleneck (Ch. 8) |

Some systems shard *within* one machine — one single-threaded process per core, or per NUMA memory bank — e.g. Redis, VoltDB, FoundationDB (p. 254).

### Sharding for multitenancy

SaaS products are **multitenant**: each tenant (customer) has a self-contained dataset — one shard per tenant, or small tenants grouped, as separate databases (even embedded ones) or managed parts of one logical database (p. 254).

| Advantage (pp. 254–255) | |
|---|---|
| Resource isolation | One tenant’s expensive work doesn’t slow others |
| Permission isolation | An access-control bug is less likely to leak data across tenants |
| **Cell-based architecture** | Services *and* storage for a set of tenants form a self-contained cell; faults stay inside it |
| Per-tenant backup/restore | Undo one tenant’s accidental deletion without touching others |
| Regulatory compliance | Exporting or deleting a person’s data = operating on one shard |
| Data residence | Place a tenant’s shard in a required jurisdiction |
| Gradual schema rollout | Migrate one tenant at a time (hard to do transactionally) |

Challenges (p. 255): a tenant too big for a node (shard within it); per-tenant shards for many tiny tenants cost too much, but grouped tenants must be moved as they grow; cross-tenant features become cross-shard joins.

### Sharding of key-value data

Goal: spread data and queries evenly so 10 nodes handle 10× the data and throughput, and rebalance when nodes come and go. Unfairness is **skew**; a shard with disproportionate load is a **hot shard / hot spot**; a single very busy key is a **hot key** (pp. 255–256).

#### Sharding by key range (pp. 256–258)

Each shard owns a contiguous key range, like encyclopedia volumes — volume 1 is A–B but volume 12 is T–Z, because boundaries must follow the data (Figure 7-2). Boundaries are set manually (Vitess) or automatically (Bigtable, HBase, MongoDB’s range option, CockroachDB, RethinkDB, FoundationDB; YugabyteDB offers both). Keys are sorted within a shard, so **range scans** are easy — e.g. a month of sensor readings.

- **Hot spot on sequential keys**: with timestamp keys, all current writes hit “this month’s” shard. Prefix with the sensor ID to spread writes — then a time range across sensors needs one query per sensor (p. 257).
- **Rebalancing**: **pre-split** an empty database if you know the key distribution (HBase, MongoDB); later **split** shards that grow too big (HBase default **10 GB**) or carry too much write load, and merge small ones — like the top of a B-tree. Splitting rewrites all the shard’s data, often while it is already overloaded (pp. 257–258).

#### Sharding by hash of key (pp. 258–263)

When nearby keys needn’t be together (e.g. tenant IDs), hash first. The hash needn’t be cryptographic — MongoDB uses MD5, Cassandra and ScyllaDB Murmur3 — but must be **stable across processes**, unlike Java’s `Object.hashCode()` or Ruby’s `Object#hash` (p. 258).

| Scheme | How | Adding a node | Trade-off | Used by |
|---|---|---|---|---|
| **Hash mod N** | `hash(key) % N` nodes | Most keys move (Figure 7-3: key 3 → node 3, 6 → node 2, 9 → node 1) | Simple, terrible rebalancing | — |
| **Fixed number of shards** | e.g. 1,000 shards on 10 nodes; `hash(key) % 1000`; track shard → node | Move whole shards to the new node (Figure 7-4); keys never change shard | Pick a count with many divisors; weight bigger machines with more shards; can’t exceed shard count; resharding is expensive; shard size grows with data | Citus, Riak, Elasticsearch, Couchbase |
| **Hash range** | Each shard owns a range of hash values (16-bit example: 0–16,383 → shard 0, …) (Figure 7-5) | Split shards as needed | Shard count adapts; no range queries on the partition key — but compound keys keep later columns sorted within a partition | YugabyteDB, DynamoDB, MongoDB option |
| **Cassandra/ScyllaDB variant** | Hash space split into ranges with random boundaries, several per node — 16 per node in Cassandra, 256 in ScyllaDB (Figure 7-6) | New node takes parts of a few ranges from several nodes | Imbalances even out over many ranges | Cassandra, ScyllaDB |
| **Consistent hashing** (rendezvous / highest random weight, jump) | Keys spread evenly; minimal keys move | New node receives individual keys scattered across all nodes | “Consistent” ≠ replica or ACID consistency | Various |

Data warehouses do the same with different words: BigQuery’s partition key + **cluster columns**, Snowflake’s micro-partitions + cluster keys, Delta Lake — clustering also helps compression and filtering (p. 262).

![Keys 0–23 spread over three nodes by hash mod 3, then over four nodes by hash mod 4: almost every key ends up on a different node](../figures/07-03.png)

*Figure 7-3 (p. 259): changing N in hash mod N moves most keys, which is why rebalancing schemes avoid it.*

![The hash range 0–1024 split at random boundaries into ranges owned by nodes 0–2; adding node 3 takes over parts of several existing ranges](../figures/07-06.png)

*Figure 7-6 (p. 262): with random boundaries and several ranges per node, a new node takes a share from each existing node.*

> **Try it:** [Sharding and rebalancing](../widgets/07-sharding.html) — add a node under hash mod N, fixed shards and rendezvous hashing, and create and relieve hot spots.

#### Skewed workloads and relieving hot spots (pp. 263–264)

Even keys don’t mean even load: a celebrity’s post can concentrate reads and writes on one key. Range-based schemes can give a hot key its own shard or machine. At the application level, **append two random digits** to split a hot key’s writes across 100 keys — but reads must fetch and combine all 100, the read load per shard isn’t reduced, and you need bookkeeping for which keys are split. Load shifts over time (a viral post calms down after days), and keys can be hot for reads or for writes. Some clouds automate this: Amazon’s **heat management** / **adaptive capacity** (p. 264).

#### Operations: automatic versus manual rebalancing (pp. 264–265)

| Automatic (e.g. DynamoDB scaling shards in minutes) | Human in the loop (Couchbase and Riak suggest, an admin commits) |
|---|---|
| Less routine work; can autoscale | Slower but fewer surprises |
| Moving data can overload network and nodes; near max write throughput, splitting may not keep up | Pre-emptive rebalancing before known surges — Cyber Monday, World Cup ticket sales |
| **Dangerous with automatic failure detection**: a slow, overloaded node is declared dead, its load moves to others, which slow down and get declared dead — a cascading failure | |

### Request routing

Which node — IP and port — holds a key? Like service discovery, except any stateless service instance can serve a request, while only a replica of the right shard can serve a key (p. 265). Three approaches (Figure 7-7):

| Approach | How |
|---|---|
| Any node | Round-robin to any node, which forwards if it doesn’t own the shard |
| **Routing tier** | A shard-aware load balancer that handles no requests itself |
| **Shard-aware client** | The client knows the assignment and connects directly |

Open problems (pp. 266–267): who decides the assignment (a single coordinator must itself fail over without split brain); how routers learn of changes; requests in flight during a shard’s cutover.

![Three ways to route a request for "foo": (1) the client contacts any node, which forwards it; (2) a routing tier forwards it; (3) the client knows the assignment and contacts node 2 directly](../figures/07-07.png)

*Figure 7-7 (p. 266): the hatched component is whatever must know which shard lives on which node.*

| Coordination | Systems (pp. 267–268) |
|---|---|
| ZooKeeper / etcd (consensus) | HBase, SolrCloud; Kubernetes uses etcd for service instances |
| Own config servers + `mongos` routers | MongoDB |
| Built-in Raft | Kafka, YugabyteDB, TiDB, ScyllaDB |
| **Gossip** among nodes — weaker, split brain possible, tolerable with weak guarantees | Riak |

Node IP addresses change slowly enough for **DNS**. Analytical databases shard too, but run each query across many shards in parallel (Ch. 11) (p. 268).

### Sharding and secondary indexes

Secondary indexes search by value — all actions by user 123, articles containing *hogwash*, cars whose colour is red — so they don’t map neatly onto shards. Standard in relational and document databases and the raison d’être of Solr and Elasticsearch (p. 268). The book’s example: used-car listings sharded by ID (0–499 → shard 0, 500–999 → shard 1) with indexes on colour and make.

| | **Local** (document-partitioned) — Figure 7-9 | **Global** (term-partitioned) — Figure 7-10 |
|---|---|---|
| What each shard indexes | Only its own records (`color:red` → its red cars) | A slice of the whole index by term: colours a–r on index shard 0, s–z on shard 1; makes split between f and h |
| Write | Touches only the record’s shard | May update several index shards — needs a distributed transaction, or is applied **asynchronously** (DynamoDB: reads may be stale) |
| Read by one term | **All shards** (scatter/gather) — expensive, tail-latency amplification, more shards don’t add query throughput (unless any matches will do, or the partition key is known) | One index shard for the postings list; fetching records may hit several |
| Read by several terms (AND) | Each shard intersects locally | Postings lists on different shards must be shipped and intersected — slow if long |
| Used by | MongoDB, Riak, Cassandra, Elasticsearch, SolrCloud, VoltDB | CockroachDB, TiDB, YugabyteDB; DynamoDB offers both |
| Good fit | Write-heavy | Read throughput > write throughput, short postings lists |

Building your own secondary index in a key-value store means keeping it consistent yourself — race conditions and partial failures easily desynchronize it (p. 269).

![Two shards, each with a primary key index of cars and a local secondary index on color and make; a query for red cars must ask both shards](../figures/07-09.png)

*Figure 7-9 (p. 269): a local index covers only its shard's records, so a query by color is scattered to every shard.*

![The same two shards with a global secondary index that is itself sharded by term: colors a–r on shard 0, s–z on shard 1; the query for red cars reads one index shard](../figures/07-10.png)

*Figure 7-10 (p. 270): a global index sends the read to one place but makes a write update index shards elsewhere.*

> **Try it:** [Local vs global secondary indexes](../widgets/07-secondary-indexes.html) — search the book's used-car listings and count the shards each read and write touches.

## Trade-offs at a glance

| | Key range | Hash of key (hash range / fixed shards) |
|---|---|---|
| Range queries on partition key | Efficient | Scatter to all shards |
| Sequential keys (timestamps) | Hot spot on the newest range | Spread evenly |
| Rebalancing | Split ranges as they grow | Move whole shards / split hash ranges |
| Single hot key | Can isolate it in its own shard | Still one shard — needs key splitting |

| Secondary index | Write cost | Read cost | Freshness |
|---|---|---|---|
| Local | One shard | All shards | Synchronous |
| Global | Several index shards | One index shard (+ record fetches) | Often asynchronous |

## Beyond the book

- Consistent hashing as a ring with virtual nodes (Karger et al., 1997; popularized by Dynamo) is the form most engineers meet; the vault's [rebalancing experiment](../lab/07-rebalancing/README.md) shows it moves ≈1/N of keys but balances load less evenly than rendezvous hashing at 64 virtual nodes.
- Jump consistent hash (Lamping and Veach, 2014) needs no storage at all but only supports adding or removing the highest-numbered bucket.

## Connections

- **Run it:** [How much data moves when a node joins](../lab/07-rebalancing/README.md).
- **Related chapters:** [2. Nonfunctional requirements](02-defining-nonfunctional-requirements.md) (celebrity skew), [6. Replication](06-replication.md), [8. Transactions](08-transactions.md) (cross-shard atomicity), [10. Consistency and Consensus](10-consistency-and-consensus.md).

## Check yourself

*Questions and answers are the vault's, written from the notes above; answers cite the book's pages.*

1. **Why does hash mod N move almost all keys when N changes, while a fixed number of shards moves only about 1/N?**

   *Answer:* With mod N a key's node depends on N, so changing N reassigns most keys. With many more shards than nodes, a key always belongs to the same shard; a new node takes over whole shards from the others, so only those shards move (pp. 258–262).

2. **You shard sensor readings by timestamp. What goes wrong?**
   - [ ] Range queries become impossible
   - [x] All current writes go to the shard holding the latest time range, creating a hot spot
   - [ ] Shards can no longer be split
   - [ ] Timestamps cannot be sorted

   *Answer:* With key-range sharding on time, today's shard receives every write. Prefixing the key with the sensor ID spreads writes, at the cost of needing one range query per sensor to read a time range across all sensors (pp. 256–258).

3. **Why can automatic rebalancing make an overload worse?**

   *Answer:* If an overloaded node is slow to respond, the system may conclude it is dead and start moving its data — adding load to it and the network at the worst moment, possibly triggering cascading failure. A human in the loop can be safer (pp. 264–265).

4. **A query filters on a secondary attribute. Compare its cost with local and global secondary indexes.**

   *Answer:* With local (document-partitioned) indexes every shard indexes its own documents, so a read must query all shards (scatter/gather) while writes stay on one shard. A global (term-partitioned) index serves the read from the shard(s) holding that term, but a single write may need to update several index shards (pp. 268–271).

5. **Why does splitting a hot key over 100 sub-keys not reduce read load?**
   - [ ] Because sub-keys are stored on the same node
   - [x] Because every read must now fetch and combine all 100 sub-keys
   - [ ] Because writes to sub-keys must be serialized
   - [ ] Because hashing the sub-keys is expensive

   *Answer:* Adding a random suffix spreads writes, but a reader no longer knows which sub-key holds the data and must read them all (pp. 263–264).
