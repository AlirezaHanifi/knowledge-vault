---
book: the-pragmatic-programmer
chapter: 4
title: "Pragmatic Paranoia"
pages: "188–225"
---

# 4. Pragmatic Paranoia

[← 3. The Basic Tools](03-the-basic-tools.md) · [Book](../README.md) · [5. Bend, or Break →](05-bend-or-break.md)

## Summary

The chapter opens with **Tip 36, You Can't Write Perfect Software**, and turns it into an advantage (p. 188). Like defensive drivers, programmers code defensively against other people's code and bad input; Pragmatic Programmers also defend against *their own* mistakes (pp. 188–189). The five defenses:

- **Design by Contract:** clients and suppliers agree on rights and responsibilities (Topic 23).
- **Crash early,** because a dead program does less damage than a crippled one (Topic 24).
- **Assertions** that actively check what "can never happen" (Topic 25).
- **Balanced resources:** whoever allocates a resource frees it (Topic 26).
- **Small steps,** so you never outrun your headlights (Topic 27).

## Key takeaways

- **A contract says: if the caller meets the preconditions, the routine guarantees its postconditions and invariants.** Breaking it is a bug, so preconditions are not for validating user input (pp. 192–193).
- **Be strict in what you accept and promise as little as possible in return** ("lazy" code), and design with contracts (Tip 37, p. 195).
- **Crash early.** Don't catch and re-raise every exception; when the impossible happens the program is no longer viable, so stop it (Tip 38, pp. 204–206).
- **Use assertions to prevent the impossible, and leave them on in production,** except the few that really hurt performance (Tip 39, pp. 207–210).
- **Finish what you start, and act locally.** The routine that allocates a resource frees it; scope the resource to a block; nest allocations and always take them in the same order (Tips 40–41, pp. 212–216).
- **Take small steps, always, and avoid fortune-telling.** The rate of feedback is your speed limit; design to be replaceable rather than for a guessed future (Tips 42–43, pp. 223–225).

## Section outline

*From the book’s own table of contents (PDF bookmarks). Page numbers are PDF pages: this edition's reflowed text has no printed page numbers.*

- Topic 23. Design by Contract — p. 191
- Topic 24. Dead Programs Tell No Lies — p. 203
- Topic 25. Assertive Programming — p. 207
- Topic 26. How to Balance Resources — p. 212
- Topic 27. Don’t Outrun Your Headlights — p. 222

## Notes

| Tip | Statement | Page |
|---:|---|---|
| 36 | You Can't Write Perfect Software | 188 |
| 37 | Design with Contracts | 195 |
| 38 | Crash Early | 205 |
| 39 | Use Assertions to Prevent the Impossible | 207 |
| 40 | Finish What You Start | 212 |
| 41 | Act Locally | 216 |
| 42 | Take Small Steps—Always | 223 |
| 43 | Avoid Fortune-Telling | 225 |

As Woody Allen put it, paranoia is just good thinking when everybody really is out to get you (p. 190).

### Topic 23. Design by Contract

A contract defines both parties' rights and responsibilities and the repercussions of breaking it (p. 191). Bertrand Meyer developed **Design by Contract (DBC)** for Eiffel. A correct program does no more and no less than it claims to do; documenting and verifying that claim is the heart of DBC (p. 192).

| Element | Meaning (pp. 192–193) |
|---|---|
| **Precondition** | What must be true for the routine to be called. The *caller* must pass good data |
| **Postcondition** | What the routine guarantees on completion; it implies the routine terminates |
| **Class invariant** | Always true from the caller's perspective: it may be broken during a routine but must hold on exit. A class can't give unrestricted write access to data in the invariant |

The contract: *if the caller meets all preconditions, the routine guarantees all postconditions and invariants on completion* (p. 193). A broken contract invokes an agreed remedy, such as an exception or termination, and is always a **bug**, which is why preconditions shouldn't do user-input validation (p. 193).

- **Clojure** has `:pre` and `:post` conditions: `accept-deposit` requires a positive amount and an open account, and promises the new transaction is among the account's transactions (pp. 193–194).
- **Elixir guard clauses** dispatch on the amount (over 100,000: call the manager; over 10,000: extra federal reporting). With an amount of zero or less no clause matches, so the function simply can't be called with bad arguments (pp. 194–195).
- **Tip 37, Design with Contracts** (p. 195). Where Topic 10 asked for *shy* code, this asks for *lazy* code: accept little, promise little. A contract that accepts anything and promises the world means a lot of code.

**DBC and TDD** (sidebar, pp. 195–196). Both serve correctness. DBC needs no setup or mocking, defines success for all cases rather than one, stays active beyond test time, checks internal invariants, and is DRY-er than defensive programming where everyone validates in case no one else does.

Invariants are really about **state**, so they apply to functional code too, where state is passed in and returned (p. 196).

**Implementing DBC** (pp. 196–198):

- Just enumerating the input domain, boundary conditions and promises before coding is a huge step; without it you're programming by coincidence. Contracts can live in comments or unit tests.
- **Assertions** emulate DBC only partially: they aren't inherited by overriding methods, invariants must be called manually, they may be turned off, there's no built-in `old` value (Eiffel has `old expression`), and libraries don't check them.
- **Who's responsible?** (sidebar, p. 198). For `sqrt` with a precondition of non-negative input, the caller decides what to do with a negative number from the console. Expressing the domain as a precondition shifts the burden of correctness to the caller, where it belongs.

**DBC and crashing early** (pp. 198–199): a failed precondition such as `sqrt_arg_must_be_positive` with a stack trace is much easier to diagnose than a `NaN` that surfaces far away.

**Semantic invariants** (pp. 199–200) are inviolate requirements, a "philosophical contract". In the authors' debit-card transaction switch, a transaction must never be applied twice: on failure, err toward not processing rather than duplicating. Stated plainly: *Err in favor of the consumer.* Don't confuse such laws with policies that change with management.

**Dynamic contracts and agents** (pp. 200–201): autonomous agents may renegotiate contracts, but if we can't use contracts by hand, we won't be able to use them automatically.

Exercise 14 asks for pre- and postconditions and an invariant for a kitchen blender with ten speeds (0 is off) that can't run empty and changes speed one step at a time (pp. 201–202).

> **Try it:** [The blender contract](../widgets/04-blender-contract.html) — drive the book's Exercise 14 blender with the contract switched on or off, try the calls that break it, and see which party each failure blames.

### Topic 24. Dead Programs Tell No Lies

Often a library notices trouble first: a nil, an empty list, a missing key, a `case` selector that isn't 1, 2 or 3. Every `case` needs a default clause so you know when the "impossible" happened (p. 203). Don't fall into "it can't happen": check that files close, that the code in production is the code you think, that the right dependency versions loaded (p. 203). All errors give information (pp. 203–204).

**Catch and release is for fish** (p. 204). Catching every exception just to log and re-raise it buries the application code and *couples* the caller to the callee's list of exceptions. Plain `add_score_to_board(score)` propagates any new exception automatically.

**Tip 38, Crash Early** (p. 205). **Crash, don't trash**: continuing may write corrupted data or command a washing machine into its twentieth spin cycle (p. 205).

- Erlang and Elixir embrace it: Joe Armstrong is often quoted as saying "Defensive programming is a waste of time. Let it crash!" Failures are managed by **supervisors**, which restart or clean up, arranged in supervisor trees (p. 205).
- Elsewhere, simply exiting may leave resources, transactions or other processes in a bad state, but the principle holds: once the impossible has happened, everything the program does is suspect (pp. 205–206).
- A dead program normally does a lot less damage than a crippled one (p. 206).

### Topic 25. Assertive Programming

"This can never happen" is self-deception: the app will never be used abroad, the count can't be negative, logging can't fail (p. 207). **Tip 39, Use Assertions to Prevent the Impossible** (p. 207).

- Assert non-null results, with a descriptive message; assert that a clever `my_sort` really sorted (pp. 207–208).
- Assertions are **not error handling**: asserting that a user typed Y or N is a very bad idea (p. 208).
- Your own assertion handler needn't terminate; it can free resources, as long as it doesn't rely on the data that failed (p. 208).
- **Side effects:** `assert(iter.nextElement() != null)` advances the iterator, so the loop processes only half the elements. Such a check that changes behavior is a kind of Heisenbug (pp. 208–209).

**Leave assertions turned on** (pp. 209–210). The argument for turning them off assumes testing finds all bugs, and forgets that production is dangerous: rats gnaw cables, memory runs out, logs fill disks. Turning them off is like crossing a high wire without a net because you once made it in practice. Disable only those that really hurt, such as an extra pass over data in a critical sort. A sidebar tells of a network-device startup that left informative assertions on in production, fixed the obscure bugs they revealed, and was acquired for hundreds of millions of dollars (p. 210).

Exercise 16 asks which "impossible" things can happen, from a month with fewer than 28 days to `(a + 1) <= a` (p. 211).

### Topic 26. How to Balance Resources

Resources (memory, transactions, threads, connections, files, timers) follow a pattern: allocate, use, deallocate (p. 212). **Tip 40, Finish What You Start** (p. 212): the function or object that allocates a resource is responsible for deallocating it.

The book's Ruby example (pp. 212–215):

1. `read_customer` opens a file and stores it in an instance variable; `write_customer` closes it. They're coupled through that hidden variable.
2. A maintenance change skips `write_customer` for negative amounts, and production dies after hours with too many open files.
3. Closing the file in the new `else` branch "fixes" it but couples three routines. Not balanced.
4. The fix: `update_customer` opens the file, passes it as a parameter, and closes it. Better still, Ruby's block form of `File.open` closes the file when the block ends.

**When in doubt, reduce scope. Tip 41, Act Locally** (pp. 215–216). A sidebar on **balancing over time** asks about log rotation, stray debug files and expiring log records: for anything that uses a finite resource, plan how it gets released (p. 216).

**Nest allocations** (p. 216):

- Deallocate in the **opposite order** to allocation, so you don't orphan resources that reference each other.
- Allocate the same set of resources in the **same order** everywhere, to reduce deadlock. If A holds resource 1 and wants 2 while B holds 2 and wants 1, both wait forever.

**Objects and exceptions** (pp. 217–219):

- Wrap resources in classes so constructors allocate and destructors free.
- With exceptions, use **variable scope** (C++ or Rust destructors, as with Rust's `File::open`) or a **`finally`** clause.
- **An antipattern:** allocating *inside* the `begin…finally` means a failed allocation runs the `finally` and deallocates something that was never allocated. Allocate first, then enter the protected block.

**When you can't balance** (pp. 219–220): for dynamic data structures, set a semantic invariant for who frees substructures: the top level frees them recursively, orphans them, or refuses to be freed while it has any. Choose explicitly per structure and implement it consistently, perhaps in a module per structure.

**Checking the balance** (p. 220): wrap resources to track allocations, check at known points such as the top of a server's main loop that usage hasn't grown, and use leak-checking tools.

> **Vault note:** the first refactored `update_customer` on p. 215 reads, updates and closes the file but omits the call to `write_customer`; the block version that follows includes it.

### Topic 27. Don’t Outrun Your Headlights

Headlights have a limited **throw distance**. Per the NHTSA, low beams illuminate about 160 feet, but the stopping distance is 189 feet at 40 mph and 464 feet at 70 mph, assuming 1.5 s reaction time and a deceleration of 17.02 ft/s² (pp. 222–223). Software "headlights" are limited too (p. 223).

**Tip 42, Take Small Steps—Always** (p. 223). Take small, deliberate steps, checking for feedback before proceeding: **the rate of feedback is your speed limit**. Feedback is anything that independently confirms or disproves your action: REPL results, unit tests, user demos and conversations (p. 223).

A task is **too big** if it needs fortune-telling: estimating completion dates months ahead, designing for future maintenance or extensibility, guessing users' future needs or future technology (pp. 223–224). Design for the future only as far ahead as you can see; otherwise, make code **replaceable**, which also helps cohesion, coupling and DRY (p. 224).

**Black swans** (p. 224): Taleb argues that significant events come from rare, hard-to-predict outliers. Around the first edition, forums debated whether Motif or OpenLook would win the desktop GUI wars; neither did, and the browser took over. **Tip 43, Avoid Fortune-Telling** (p. 225).

> **Try it:** [Outrunning your headlights](../widgets/04-headlights.html) — compare stopping distance with headlight throw using the book's NHTSA numbers, then set how far ahead a team commits before getting feedback and see how much work a change of direction throws away.

## Trade-offs at a glance

| Choice | Buys | Costs |
|---|---|---|
| Contracts (DBC) | Correctness stated for all cases; blame is clear | Thinking up front; partial support in most languages |
| Defensive programming everywhere | Robustness against unknown callers | Duplicated checks (not DRY); unclear responsibility |
| Catch-log-reraise every exception | Log lines | Coupling to the callee's exceptions; buried logic |
| Crash early | No corrupted data; accurate diagnostics | Downtime unless supervised and restarted |
| Assertions on in production | Catches bugs testing missed, with real data | Some overhead; disable only the expensive ones |
| Resources scoped to a block | Release is guaranteed | Restructuring code around the block |
| Big steps and long-range design | Fewer check-ins | Fortune-telling; rework when the future differs |
| Small steps with feedback | Early correction; replaceable code | More frequent feedback loops |

## Beyond the book

- **Contracts in mainstream languages.** Python has no built-in contracts, but `assert`, type hints and libraries such as `icontract` emulate them; note that `python -O` strips `assert` statements, which is exactly the "turn assertions off in production" risk the book warns about. C++26 adds language contracts (`pre`, `post`, `contract_assert`).
- **Lock ordering in practice.** The deadlock rule in Topic 26 is the standard *lock hierarchy* technique; tools such as Linux's lockdep check at run time that locks are always taken in a consistent order. The vault's [lock-ordering lab](../lab/04-lock-ordering/README.md) counts deadlocks with and without it.
- **Let it crash, carefully.** Supervision only helps if restarting fixes the problem; a crash caused by bad persistent data restarts into the same crash. Erlang supervisors therefore cap restart intensity and escalate to their own supervisor, the tree the book mentions.

## Connections

- **Related chapters:** [2. A Pragmatic Approach](02-a-pragmatic-approach.md) (shy code, replaceable code, and ETC), [3. The Basic Tools](03-the-basic-tools.md) (read the error message; failing test before fixing code), [5. Bend, or Break](05-bend-or-break.md) (decoupling, which the resource example violates), [6. Concurrency](06-concurrency.md) (deadlock and shared resources), [7. While You Are Coding](07-while-you-are-coding.md) (programming by coincidence; property-based tests check contracts and invariants).
- **Run it:** [Lock ordering and deadlock](../lab/04-lock-ordering/README.md) — runs thousands of seeded interleavings of threads that need two resources each, with and without a global acquisition order, and counts deadlocks.

## Check yourself

*Questions and answers are the vault's, written from the notes above; answers cite the book's PDF pages.*

1. **State the contract between a routine and its caller.**

   *Answer:* If the caller meets all the preconditions, the routine guarantees that all postconditions and invariants are true when it completes (p. 193).

2. **Why shouldn't preconditions be used to validate user input?**

   *Answer:* A contract violation is a bug, something that should never happen; bad user input is expected and needs real handling (p. 193).

3. **What does "lazy" code mean in Topic 23?**

   *Answer:* Be strict in what you accept before you begin and promise as little as possible in return (p. 195).

4. **What's wrong with catching every exception, logging it and re-raising it?**

   *Answer:* The error handling eclipses the code, and the caller is coupled to the callee's list of exceptions, so a new exception leaves it subtly out of date (p. 204).

5. **Should assertions be turned off in production?**
   - [ ] Yes, once the code is tested
   - [x] No, except specific ones that really hurt performance
   - [ ] Only in languages without exceptions

   *Answer:* Testing doesn't find all bugs and production is dangerous; disable only the expensive checks (pp. 209–210).

6. **What's wrong with putting `thing = allocate_resource()` inside the `begin…finally` block?**

   *Answer:* If allocation fails, the `finally` clause tries to deallocate something that was never allocated (pp. 218–219).

7. **Two code paths need resources A and B. What rule reduces deadlock?**

   *Answer:* Always allocate them in the same order everywhere (and free them in reverse order) (p. 216).

8. **What does "the rate of feedback is your speed limit" mean?**

   *Answer:* Never take a step bigger than you can get independent feedback on; tasks that need predictions far ahead are fortune-telling (p. 223).
