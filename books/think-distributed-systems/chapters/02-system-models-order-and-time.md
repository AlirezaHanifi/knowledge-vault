---
book: think-distributed-systems
chapter: 2
title: "System models, order, and time"
pages: "23–39"
---

# 2. System models, order, and time

[← 1. Thinking in distributed systems: Models, mindsets, and mechanics](01-thinking-in-distributed-systems-models-mindsets-and-mechanics.md) · [Book](../README.md) · [3. Failure tolerance →](03-failure-tolerance.md)

## Summary

Every algorithm is correct only *relative to* a **system model**: a set of assumptions about components, the network and timing (p. 24). The chapter goes through the timing models (synchronous, asynchronous with no or a weak notion of time, and partially synchronous), the component failure models (Crash-Stop, Omission, Crash-Recovery, Byzantine) and the network failures (reordering, duplication, loss) (pp. 25–30). It then states the author's **realistic system model**: partially synchronous, non-Byzantine components that crash and recover, over an unreliable network (p. 30).

The second half is about **order**. Most actions don't commute, so establishing order is fundamental (p. 30). The chapter defines a race condition over executions and fixes the example with a coordinator that tags requests (pp. 30–32). It covers Lamport's **happened-before** relation, causality, and a precise definition of concurrency versus parallelism (pp. 32–35). It closes with **clock consistency** and the two kinds of clock: physical clocks (skew, drift, NTP, time-of-day vs. monotonic) and logical clocks (Lamport clocks, Kafka offsets, etcd sequence numbers) (pp. 35–38).

## Key takeaways

- **A system model is the rules of the game.** An algorithm that is correct under one set of assumptions may be wrong under another; a small rule change can unravel a strategy (p. 24).
- **"Asynchronous" is ambiguous.** With *no* notion of time, a component can't use timeouts. With a *weak* notion (unsynchronized clocks of unknown deviation), it can. Some problems are solvable only in the second (pp. 25–26).
- **Real systems are partially synchronous**, synchronous most of the time and asynchronous sometimes. Protocols therefore guarantee safety and liveness while things are synchronous, and keep **safety over liveness** otherwise (p. 26).
- **Four component failure models:** Crash-Stop (ceases to exist), Omission (takes a break, keeps its memory), Crash-Recovery (may lose state) and Byzantine (anything, including deception) (pp. 27–28).
- **The network may reorder, duplicate or lose messages, but it cannot lie** (pp. 28–30).
- **Happened-before** (Lamport, 1978) is a partial order built from intra-component order and send→receive pairs, closed under transitivity. It captures *potential* causality (pp. 32–34).
- **Concurrency is logical; parallelism is physical.** Two operations are concurrent if neither's end happened before the other's begin, and parallel if they overlap in time (pp. 34–35).
- **Clock consistency:** a → b ⇒ C(a) < C(b). Physical clocks measure durations within a component; logical clocks order events across components (pp. 35, 38).

## Section outline

*From the book’s own table of contents (PDF bookmarks); printed page numbers.*

- 2.1 System models — p. 23
  - 2.1.1 Theory and practice — p. 24
  - 2.1.2 Synchronous distributed systems — p. 25
  - 2.1.3 Asynchronous distributed systems — p. 25
  - 2.1.4 Partially synchronous systems — p. 26
  - 2.1.5 Component and network behavior — p. 27
  - 2.1.6 Realistic system models — p. 30
- 2.2 Order and time — p. 30
  - 2.2.1 The happened-before relationship — p. 32
  - 2.2.2 Time and clocks — p. 35
  - 2.2.3 Physical time and physical clocks — p. 35
  - 2.2.4 Logical time and logical clocks — p. 37
  - 2.2.5 Physical clocks vs. logical clocks — p. 38

## Notes

### 2.1 System models

A **system model** is a set of assumptions about the system's components, its network and its timing behavior (Table 2.1) (p. 24):

| One system model | Another system model |
|---|---|
| Components may not fail | Components may fail |
| Messages may not get lost | Messages may get lost |
| Clocks are perfectly synchronized | Clocks are not perfectly synchronized |

The book's aha! moment compares a system model to a **board game**: the rules set the stage, and even a slight rule change can make a carefully devised strategy ineffective (p. 24).

#### Theory and practice (pp. 24–25)

| Kind | Typically used to reason about | Example |
|---|---|---|
| **Theoretical** | Impossibilities, and lower and upper bounds on components or messages | — |
| **Practical** | Possibilities, weighed against development and operational cost, scalability and reliability | — |
| **Both** | — | The models underlying Viewstamped Replication, Paxos and Raft |

#### Timing models (pp. 25–26)

![A spectrum from the synchronous system model through the partially synchronous model to the asynchronous model; the two ends are labelled theoretical and the middle, highlighted, practical](../figures/02-02.png)

*Figure 2.2 (p. 26): the two extremes are theoretical; real systems are partially synchronous.*

| Model | Clocks | Event timing | Consequence |
|---|---|---|---|
| **Synchronous** | Perfectly synchronized, or deviating by a known upper bound | Strict, or with bounded delay | Strong notion of physical time |
| **Asynchronous, no notion of time** | None | Arbitrary time or arbitrary delay | **No timeouts**, and timeouts are crucial for failure detection and mitigation |
| **Asynchronous, weak notion of time** | Unsynchronized, with unknown deviation | Arbitrary | **Timeouts are possible** |
| **Partially synchronous** | — | Synchronous most of the time, asynchronous at other times | Matches experience, like home internet that is usually fast but sometimes times out |

Neither the synchronous nor the asynchronous model says anything about component failure or message loss; those are separate assumptions (pp. 25–26). When you meet the term *asynchronous system*, first work out which notion of time it assumes, then whether that matters in context (p. 25). The typical protocol design is to guarantee safety and liveness when the system runs synchronously, and to put **safety over liveness** when it runs asynchronously: nothing bad happens, even if nothing good happens for a while (p. 26).

#### 2.1.5 Component and network behavior (pp. 27–30)

The component failure models are nested (Figure 2.3): each is more general than the one before.

| Component failure | What happens (pp. 27–28) | In short |
|---|---|---|
| **Crash-Stop** | Stops executing steps at an arbitrary moment and never performs another | It ceases to exist |
| **Omission** | Stops for an arbitrary duration, then resumes from the state where it stopped | It takes a break, with no memory loss |
| **Crash-Recovery** | Stops for an arbitrary duration, then resumes, but may lose state | Partial or total memory loss |
| **Byzantine** | Behaves arbitrarily, including deliberately deviating from its algorithm | Anything might happen |

| Network failure | What happens (pp. 28–29) |
|---|---|
| **Reordering** | Messages are delivered in a different order from the one they were sent in (Figure 2.8) |
| **Duplication** | A message is delivered more than once (Figure 2.9) |
| **Loss** | A message is never delivered (Figure 2.10) |

A network with these failures is called **unreliable**. However, the book assumes that *a network cannot lie*: a delivered message was sent by some component of the system (p. 30).

#### 2.1.6 Realistic system models (p. 30)

The model the author has in mind throughout the book:

- **Partially synchronous**: synchronous most of the time.
- Components subject to **Crash-Stop, Omission and Crash-Recovery** failures. They forget *volatile* state and remember *durable* state.
- Communication over an **unreliable network** that may reorder, drop or duplicate messages.
- **Byzantine failures largely ignored**, although they matter in domains such as cryptocurrency.

### 2.2 Order and time

Components don't merely communicate; they **collaborate and coordinate**, which means managing dependencies between their steps. Actions are generally not commutative, so the result depends on the order in which they're applied (p. 30).

**The proposer/acceptor example** (pp. 30–32):

- Setup: two proposers, P1 and P2, broadcast arithmetic requests to two acceptors, A1 and A2, which start at 0 and apply requests in arrival order.
- If both requests are (+2), order doesn't matter, because the operations commute.
- If P1 sends (+2) and P2 sends (×2), A1 can end at 4 (applying +2 then ×2) while A2 ends at 2 (applying ×2 then +2) (Figure 2.11).
- The book's definition: a system has a **race condition** if it has multiple possible executions, some considered correct and some incorrect (p. 31).
- The fix is a **coordinator** C that starts at 0, tags each request with its current value, broadcasts it and increments (Figure 2.12). An acceptor that sees a larger tag than expected has skipped a step, and waits for the missing request.

In Figure 2.12, P1 sends first, but the network delivers P2's (×2) to C first. That's acceptable: the proposers never coordinated, and C can't observe them sending. C broadcasts ⟨×2, 0⟩ and ⟨+2, 1⟩, and both acceptors apply them in tag order regardless of arrival order (p. 32).

> **Try it:** [Proposers, acceptors and a coordinator](../widgets/02-coordinator-ordering.html) — replay Figures 2.11 and 2.12: shuffle the network's delivery order and watch the acceptors diverge without a coordinator, then converge once requests carry the coordinator's tags.

#### 2.2.1 The happened-before relationship (pp. 32–35)

From Lamport's 1978 paper "Time, Clocks, and the Ordering of Events in a Distributed System" (pp. 32–33):

| Rule | Definition |
|---|---|
| **Intracomponent** | a and b occur at the same component and a precedes b ⇒ a → b (Figure 2.13) |
| **Intercomponent** | a is a Send Message event and b is the matching Receive Message event ⇒ a → b (Figure 2.14) |
| **Transitivity** | a → b and b → c ⇒ a → c (Figure 2.15) |

Happened-before is a **partial order**: for any two events, a → b, b → a, or a ∥ b (concurrent) (Table 2.2) (p. 33). It captures **causality** in the sense that a *potentially* influenced b, not that it actually did (p. 34).

![Events a and b on component 1 and c on component 2; b sends a message received as c, and a dashed arrow from a to c marks the transitive relation](../figures/02-15.png)

*Figure 2.15 (p. 34): a → b within a component and b → c across the message give a → c (the dashed arrow), though a never sent anything to c.*

The aha! moment on **concurrency vs. parallelism** (pp. 34–35):

- Concurrency is about *events* (moments) and parallelism about *operations* (spans), so treat an operation as a pair of begin and end events.
- Two operations are **concurrent** if neither one's end event happened before the other's begin event. Concurrency is determined by logical time.
- Two operations are **parallel** if they overlap in time. Parallelism is determined by physical time.

#### 2.2.2 Time and clocks (p. 35)

Clocks are the system's source of timestamps. To order events, a clock must guarantee **clock consistency**:

> a → b ⇒ C(a) < C(b)

#### 2.2.3 Physical time and physical clocks (pp. 35–37)

The **wall clock** is a hypothetical perfect clock that only an all-knowing observer has. Every real component has its own imperfect physical clock (p. 35).

| Problem or remedy | Meaning (pp. 35–37) |
|---|---|
| **Clock skew** | A *fixed offset* between two clocks: the book's example starts 5 minutes apart and stays 5 minutes apart (Figure 2.16) |
| **Clock drift** | A different *tick frequency*: clocks that start equal gradually diverge (Figure 2.17) |
| **NTP** | An NTP server broadcasts its reading and clients adjust their clocks to match, mitigating skew and drift |
| **Time-of-day clock** | As close as possible to wall-clock time, but may move **backward** when synchronized, so it can violate clock consistency even against itself |
| **Monotonic clock** | Independent of wall-clock time, never moves backward, consistent against itself, so comparable **only within one component** |

#### 2.2.4 Logical time and logical clocks (pp. 37–38)

A **Lamport clock** is a counter kept by each component (p. 37):

- Increment it on every internal or external step, and tag the event with its value.
- On receiving a message, set the clock to the maximum of the current value and the received timestamp, plus 1. Figure 2.18 shows max(1, 3) + 1 = 4.
- This gives causally related events strictly increasing values.

![Two component timelines with Lamport timestamps: the first counts 1, 2, 3 and sends a message at 3; the second is at 1, receives it and jumps to max(1, 3) + 1 = 4, then 5](../figures/02-18.png)

*Figure 2.18 (p. 38): on receipt the clock jumps past the sender's timestamp, so the receive event is always later than the send.*

The author has never used Lamport clocks himself, but logical clocks hide in many places (pp. 37–38):

| System | "Clock" | "Timestamp" | Comparable… |
|---|---|---|---|
| **Apache Kafka** | A partition | The message offset | Within a partition, not across partitions |
| **etcd** | A key | Its sequence number, which enables compare-and-swap | Within a key, not across keys |

> **Try it:** [Happened-before and Lamport clocks](../widgets/02-happened-before.html) — build a space-time diagram of three components, pick any two events to see whether one happened before the other or they are concurrent, and check clock consistency: whenever a → b, C(a) < C(b), but not the reverse.

#### 2.2.5 Physical clocks vs. logical clocks (p. 38)

| | Physical clocks | Logical clocks |
|---|---|---|
| Used for | Durations between events *within* a component | Order of events *across* components |
| Weakness | Skew, drift, synchronization problems | Don't measure duration |

They're commonly used together (p. 38).

## Trade-offs at a glance

| Choice | Buys | Costs |
|---|---|---|
| Synchronous model | Simple reasoning, timeouts that are always accurate | Unrealistic |
| Asynchronous, no notion of time | Algorithms that are correct anywhere | No timeouts, so some problems are unsolvable |
| Partially synchronous model | Realism, with liveness while things are well behaved | Must keep safety when things aren't |
| Time-of-day clock | Comparable with wall-clock time | May move backward |
| Monotonic clock | Never moves backward | Meaningful only within one component |
| Coordinator tagging | A single total order for every acceptor | An extra hop, and a component that can fail |

## Beyond the book

- **The converse of clock consistency fails.** Lamport clocks give a → b ⇒ C(a) < C(b), but C(a) < C(b) does *not* imply a → b: concurrent events also get ordered numbers. **Vector clocks** keep one counter per component and give a ⇔ relationship. See [DDIA Ch. 6](../../designing-data-intensive-applications/chapters/06-replication.md) and [Database Internals Ch. 11](../../database-internals/chapters/11-replication-and-consistency.md), which has a vector-clock simulation.
- **FLP.** The "no notion of time" model is the setting of Fischer, Lynch and Paterson's 1985 result: deterministic consensus is impossible with even one crash failure. Partial synchrony, from Dwork, Lynch and Stockmeyer (1988), is the standard escape hatch. The book returns to this in [Chapter 10](10-distributed-consensus.md).
- **The coordinator is a sequencer.** The coordinator of Figure 2.12 is a total-order broadcast through a single sequencer. Kafka's partition leader works similarly, as does a Raft leader assigning log indexes; consensus is what makes such a sequencer replaceable when it fails.

## Connections

- **Related chapters:** [1. Thinking in distributed systems](01-thinking-in-distributed-systems-models-mindsets-and-mechanics.md) (race conditions over interleavings), [3. Failure tolerance](03-failure-tolerance.md) (failure models in practice), [4. Message delivery and processing](04-message-delivery-and-processing.md) (living with an unreliable network), [9. Consistency](09-consistency.md) (ordering guarantees), [10. Distributed consensus](10-distributed-consensus.md) (partial synchrony and leaders).

## Check yourself

*Questions and answers are the vault's, written from the notes above; answers cite the book's pages.*

1. **Why does the meaning of "asynchronous" matter?**

   *Answer:* With no notion of time, components can't use timeouts. With a weak notion of time (unsynchronized clocks), they can, and some problems are solvable only then (pp. 25–26).

2. **How do Omission and Crash-Recovery failures differ?**

   *Answer:* Both stop for an arbitrary duration and resume. After an Omission failure the component keeps its state; after a Crash-Recovery failure it may lose some or all of it (pp. 27–28).

3. **Which of these is part of the author's realistic system model?**
   - [ ] Byzantine components
   - [x] Partial synchrony, and components that crash and recover over an unreliable network
   - [ ] A synchronous network that never loses messages

   *Answer:* Partially synchronous; Crash-Stop, Omission and Crash-Recovery failures; an unreliable network. Byzantine failures are largely ignored (p. 30).

4. **In Figure 2.11, why do A1 and A2 end with different values, and how does the coordinator fix it?**

   *Answer:* (+2) and (×2) don't commute, and the acceptors receive them in different orders. The coordinator tags requests with increasing numbers, so each acceptor applies them in tag order and waits for gaps to fill (pp. 31–32).

5. **When are two operations concurrent, and when are they parallel?**

   *Answer:* Concurrent if neither's end event happened before the other's begin event, which is logical time. Parallel if they overlap in physical time (pp. 34–35).

6. **What is the difference between clock skew and clock drift?**

   *Answer:* Skew is a fixed offset between two clocks. Drift is a difference in tick frequency, which makes clocks diverge over time (pp. 35–36).

7. **Why can't monotonic-clock readings from two components be compared?**

   *Answer:* Monotonic clocks are independent of wall-clock time; they guarantee consistency only against themselves, within one component (p. 37).
