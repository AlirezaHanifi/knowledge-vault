---
book: think-distributed-systems
chapter: 5
title: "Transactions"
pages: "67–78"
---

# 5. Transactions

[← 4. Message delivery and processing](04-message-delivery-and-processing.md) · [Book](../README.md) · [6. Distributed transactions →](06-distributed-transactions.md)

## Summary

Transactions come from databases, not distributed systems, but they've become the benchmark for developer experience in distributed systems. They let you **pretend that concurrency and failure don't exist** (p. 67). Instead of the usual four ACID letters, the chapter explains transactions through **correctness** (concurrency handled) and **completeness** (failure handled) (p. 68).

It first looks at **abstractions**: Abelson and Sussman's building blocks, Tanenbaum and Bos's "ugly" and "beautiful" interfaces, Helland's agnostic and aware worlds joined by an API, and the author's own view of reduction and composition as equivalent (pp. 68–70). A money-transfer handler with no visible guardrails shows the magic: concurrent withdrawals don't lose updates, and a crash between two writes doesn't half-apply the transfer (pp. 70–72). The model comes next: programs and transactions, traces and histories, ACID, and consistency as the one application-level property (pp. 72–74). Correctness is formalized as Hoare triples and **serializability** (pp. 74–77). Completeness is explained through an **Undo log**, where Undo operations must be **restartable**: noop plus idempotent (pp. 77–78).

## Key takeaways

- **Abstractions transform worlds.** They turn an "ugly" lower-level interface into a "beautiful" higher one (an OS turns CPU, RAM and disks into processes, memory and files). Reduction (top-down) and composition (bottom-up) must be equivalent (pp. 68–70).
- **Transactions turn concurrency- and failure-agnostic definitions into concurrency- and failure-aware, failure-tolerant executions** (pp. 70, 72).
- **A transaction** is a sequence of operations on a set of objects that ends with exactly one commit or exactly one abort (p. 72).
- **Consistency is the odd one out in ACID.** It's an application-level guarantee, such as `CHECK(balance >= 0)`; atomicity, isolation and durability are platform-level (pp. 72–73).
- **A program is the definition; a transaction is the execution.** Operation → action, name → object. An interleaved execution of transactions is a **history** (pp. 73–74).
- **Serializability:** concurrent t1 ∥ t2 is correct if it's equivalent to t1;t2 *or* t2;t1. It's a consistency model, a predicate that splits histories into good and bad (pp. 75–76).
- **Implementing serializability is trivial; implementing it efficiently is hard.** One global lock forces a serial schedule, and finer locks allow more concurrency with the same semantics (pp. 76–77).
- **Undo must be restartable.** Undo operations may run against a value the operation never changed, or run several times after a crash during recovery, so each must be a **noop** when its operation didn't happen and **idempotent** (p. 78).

## Section outline

*From the book’s own table of contents (PDF bookmarks); printed page numbers.*

- 5.1 Abstractions — p. 68
- 5.2 The magic of transactions — p. 70
  - 5.2.1 Concurrency — p. 70
  - 5.2.2 Failure — p. 71
- 5.3 The model of transactions — p. 72
  - 5.3.1 Correctness — p. 74
  - 5.3.2 Serializability — p. 75
  - 5.3.3 Completeness — p. 77
  - 5.3.4 Application-level abort — p. 77
  - 5.3.5 Platform-level abort — p. 78

## Notes

### 5.1 Abstractions

*Structure and Interpretation of Computer Programs* (Abelson and Sussman) names three building blocks of programs (p. 68):

- **primitive expressions**,
- **means of combination**, and
- **means of abstraction**: naming compound elements and handling them as a unit.

What that definition doesn't stress is that abstractions *transform domains of discourse* (p. 68). Three ways of drawing this:

| View | Lower level | Higher level | Source (pp. 68–69) |
|---|---|---|---|
| **Ugly → beautiful** (Figure 5.1) | For an OS: CPU, RAM, disks. For a database: processes, memory, files | For an OS: processes, memory, files. For a database: tables of rows and columns, and transactions | Tanenbaum and Bos, *Modern Operating Systems* |
| **Aware ↔ agnostic** (Figure 5.2) | *Aware* concepts | *Agnostic* concepts, with an **API** that translates between the two worlds | Helland, "Life beyond Distributed Transactions" |
| **Reduction ↔ composition** (Figure 5.3) | Top-down, an entity is *reduced* (compiled) to lower-level entities | Bottom-up, lower-level entities are *composed* and the higher entity *emerges* | The author's preferred view |

Beauty lies in the eye of the beholder: the OS's beautiful interface is the database's ugly one (p. 68). Abstractions are **recursive**, and each boundary brings different entities, relationships and constraints, a different semantics (p. 69). Whichever level you reason at, the system must return the same result. That is **equivalence** (pp. 69–70).

### 5.2 The magic of transactions

The author didn't realize early web applications were distributed, because **transactions hid it**. Building on a transactional database extends its guarantees to the whole system (p. 70).

Listing 5.1 is a `/transfer` endpoint (overdraft allowed). It runs `BEGIN; UPDATE … balance - $1 …; UPDATE … balance + $1 …; COMMIT;` with **no visible detection or mitigation** of concurrency or failure (p. 70).

| Threat | Without transactions | With transactions (pp. 70–72) |
|---|---|---|
| **Concurrency** (Figure 5.4) | Two transfers of −10 each read 50 and write 40: final 40 instead of 30, a race between read and write | Executes as though concurrency didn't exist: **correctness** |
| **Failure** (Figure 5.5) | Crash after debiting the source (50 → 40) but before crediting the target: 40/50 instead of 40/60 | Executes as though failure didn't exist: **completeness** |

### 5.3 The model of transactions

A **transaction** is a sequence of operations on a set of objects ending in **exactly one commit or exactly one abort**. It guarantees correctness and completeness, which come from the ACID principles (p. 72):

| Letter | Guarantee (p. 72) | Level (pp. 72–73) |
|---|---|---|
| **Atomicity** | Observably equivalent to executing completely or not at all | Platform |
| **Consistency** | Moves the database from one consistent state to another | **Application** |
| **Isolation** | Executes as though it were the only transaction, so no interference | Platform |
| **Durability** | Once committed, its effects are permanent: it doesn't go back on its word | Platform |

The fun fact: Jim Gray reported that Andreas Reuter coined "ACID" because his wife, Christiane, hates sweet things and loves vinegar (p. 72).

**Consistency is application-level** (pp. 72–73): with `balance INT`, a transaction that makes a balance negative commits; with `balance INT CHECK(balance >= 0)`, the same transaction aborts. Originally, isolation meant serializability. Modern databases offer many weaker isolation levels, which the book leaves out (p. 73).

**Definition vs. execution** (Figure 5.6, Table 5.1) (pp. 73–74):

| Design time (definition) | Run time (execution) |
|---|---|
| Program P | Transaction t |
| Operation A | Action a |
| Name N | Object o |

- A database is a set of objects, each a name–value pair.
- A transaction's **trace** is a sequence of triples ⟨tx, aᵢ, oᵢ⟩, with i = 1..n. Including tx in each triple makes interleavings analyzable.
- A **history** is the interleaved execution of several transactions.
- The database turns the failure-agnostic definition into a failure-tolerant execution (Figure 5.7) (p. 74).

#### 5.3.1 Correctness (pp. 74–75)

A transaction preserves consistency, written as a Hoare triple **{ C } tₓ { C }**. Consistency may be violated *during* the transaction, for example after the debit and before the credit (Figure 5.8). A serial history composes safely:

> { C } t1 { C } ∧ { C } t2 { C } ⇒ { C } t1;t2 { C }

So concurrent transactions are correct if their effect equals some serial order:

> { C } t1 ∥ t2 { C } ⇒ { C } t1;t2 { C } ∨ { C } t2;t1 { C }

That is **serializability**: concurrency is allowed only if it introduces no inconsistency (p. 75).

#### 5.3.2 Serializability (pp. 75–77)

- A **consistency model** is a predicate on execution histories that sorts them into good (legal, valid) and bad (illegal, invalid) (Figure 5.9). You, the engineer, choose it (p. 75).
- Serializability, introduced by Edgar Codd, accepts a concurrent execution if its *(transaction result, database state)* is equivalent to t1•t2 or t2•t1 (pp. 75–76).
- In Figure 5.10, t1 = A·B and t2 = C·D run as A·C·B·D. The history is serializable if that's equivalent to (A·B)·(C·D) or to (C·D)·(A·B). It need only match *some* serial order, not a specific one (p. 76).
- **Aha! moment:** one lock over all objects forces a serial schedule, which is trivial. Finer-grained locks over subsets of objects allow concurrent schedules with serial semantics. The goal is the most concurrency that keeps serial semantics (pp. 76–77).

> **Vault note:** Chapter 1's [interleavings simulation](../widgets/01-interleavings.html) applies the same equivalence test to two read–increment–write processes, the counter version of Figure 5.4.

#### 5.3.3 Completeness (p. 77)

Chapter 3's backward and forward recovery become **Undo** and **Redo** in a database. Real systems combine both; the book focuses on Undo (p. 77).

- Every operation has an **Undo operation**.
- *Before* executing ⟨t, aᵢ, oᵢ⟩, the system appends ⟨¬aᵢ, oᵢ⟩ to the **Transaction Undo Log** object o_u.

That gives two valid traces (p. 77):

| Trace | Shape |
|---|---|
| **Commit trace** (no failure) | [⟨tx, aᵢ, oᵢ⟩ \| i = 1..n] |
| **Abort trace** (failure) | [⟨tx, aᵢ, oᵢ⟩ \| i = 1..k] followed by [⟨tx, ¬aᵢ, oᵢ⟩ \| i = k..1]: the system is back where it started |

#### 5.3.4–5.3.5 Application-level and platform-level abort (pp. 77–78)

| Abort | Trigger | What the database does |
|---|---|---|
| **Application-level** | An *explicit* abort command, or an *implicit* abort such as a consistency violation | Runs the transaction's Undo operations; straightforward |
| **Platform-level** | A crash and restart at an arbitrary point | **Recovery**: scans the Undo log for uncommitted transactions and runs their Undo operations |

The problem: recording an Undo and executing the operation are two separate steps (p. 78).

- A crash after recording the Undo but *before* the operation means the Undo will be applied to the **old** value.
- A crash *during* recovery means Undo operations run **more than once**.

So Undo operations must be **restartable**, which means noop plus idempotent (p. 78):

| Property | Equation |
|---|---|
| **Noop** | ⟨tx, aᵢ, oᵢ⟩⟨tx, ¬aᵢ, oᵢ⟩ = ⟨tx, ¬aᵢ, oᵢ⟩: applying the operation then its Undo equals applying only the Undo |
| **Idempotent** | ⟨tx, aᵢ, oᵢ⟩⟨tx, ¬aᵢ, oᵢ⟩ = ⟨tx, aᵢ, oᵢ⟩⟨tx, ¬aᵢ, oᵢ⟩ … ⟨tx, ¬aᵢ, oᵢ⟩: repeating the Undo changes nothing |

> **Try it:** [A restartable Undo log](../widgets/05-undo-log.html) — run the book's transfer with an Undo log, crash it between recording an Undo and applying its operation, or in the middle of recovery, and compare a relative Undo ("add 10 back") with one that restores the old value: only the second is noop and idempotent.

## Trade-offs at a glance

| Choice | Buys | Costs |
|---|---|---|
| One global lock | Trivially serializable | No concurrency |
| Fine-grained locks | Concurrency with serial semantics | Complexity, deadlocks |
| Weaker isolation levels (outside the book's scope) | Throughput | Anomalies the application must tolerate |
| Undo (backward recovery) | Roll back uncommitted work | A log write before every operation; Undo must be restartable |
| Redo (forward recovery) | Replay committed work | Mentioned but not covered (p. 77) |
| Consistency constraints in the schema | The database enforces the rules | Rules live in the application's definition of consistency |

## Beyond the book

- **Relative vs. absolute Undo.** A relative Undo ("add 10 back") is neither noop nor idempotent. An Undo that restores the *before-image* (the old value) is both, provided recovery knows which operations actually ran. Real systems use log sequence numbers on pages for that, as in ARIES: see [Database Internals Ch. 5](../../database-internals/chapters/05-transaction-processing-and-recovery.md) and its recovery simulation.
- **Isolation levels.** The book stops at serializability (p. 73). Read committed, snapshot isolation and their anomalies (lost update, write skew) are covered in [DDIA Ch. 8](../../designing-data-intensive-applications/chapters/08-transactions.md), which has a simulation for each level.
- **Lost update.** Figure 5.4's two transfers both reading 50 is the lost-update anomaly. `UPDATE … SET balance = balance - 10` is atomic in most databases precisely so that it can't happen even at weak isolation.

## Connections

- **Related chapters:** [1. Thinking in distributed systems](01-thinking-in-distributed-systems-models-mindsets-and-mechanics.md) (race conditions and serializability over interleavings), [3. Failure tolerance](03-failure-tolerance.md) (backward and forward recovery), [4. Message delivery and processing](04-message-delivery-and-processing.md) (transactional deduplication), [6. Distributed transactions](06-distributed-transactions.md) (completeness across resource managers), [9. Consistency](09-consistency.md) (consistency models beyond serializability).

## Check yourself

*Questions and answers are the vault's, written from the notes above; answers cite the book's pages.*

1. **What does a transaction let an application pretend?**

   *Answer:* That concurrency and failure don't exist. The database turns agnostic definitions into aware, tolerant executions (pp. 67, 72).

2. **Why is consistency different from A, I and D?**

   *Answer:* It's an application-level guarantee, defined by rules such as `CHECK(balance >= 0)`. Atomicity, isolation and durability are platform-level (pp. 72–73).

3. **In Figure 5.4 two −10 transfers run against a balance of 50. What goes wrong without isolation?**

   *Answer:* Both read 50 and write 40, so the final balance is 40 instead of 30 (p. 71).

4. **When is t1 ∥ t2 serializable?**
   - [ ] Only if it's equivalent to t1;t2
   - [x] If it's equivalent to t1;t2 or to t2;t1
   - [ ] If no two actions touch the same object

   *Answer:* Equivalence to *some* serial order is enough (pp. 75–76).

5. **What is a consistency model?**

   *Answer:* A predicate on execution histories that separates good (legal) histories from bad ones (p. 75).

6. **Describe the abort trace of a transaction that fails after k operations.**

   *Answer:* Its first k operations, followed by their Undo operations in reverse order, k..1 (p. 77).

7. **Why must Undo operations be noop and idempotent?**

   *Answer:* A crash between logging an Undo and applying its operation means the Undo runs on the old value, so it must be a noop then. A crash during recovery means Undo runs again, so it must be idempotent (p. 78).
