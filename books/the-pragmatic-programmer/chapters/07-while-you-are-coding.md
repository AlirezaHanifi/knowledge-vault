---
book: the-pragmatic-programmer
chapter: 7
title: "While You Are Coding"
pages: "324–402"
---

# 7. While You Are Coding

[← 6. Concurrency](06-concurrency.md) · [Book](../README.md) · [8. Before the Project →](08-before-the-project.md)

## Summary

The authors say the idea that coding is mechanical transcription of a design is the single biggest reason projects fail. Coding is a stream of decisions that need judgment (p. 324). The chapter covers eight topics:

- Listening to your instincts (Topic 37).
- Programming deliberately rather than by coincidence (Topic 38).
- Estimating algorithm speed with Big-O (Topic 39).
- Refactoring continuously (Topic 40).
- Testing as feedback rather than bug-hunting (Topic 41).
- Letting the computer test your assumptions with properties (Topic 42).
- Basic security (Topic 43).
- Naming (Topic 44).

Like driving, coding can be largely routine, but keeping your wits about you can prevent a disaster (p. 326).

## Key takeaways

- **Listen to your inner lizard.** Reluctance, fear of the blank page or "walking uphill in mud" are feedback. Step away, externalize the problem, or tell yourself you're only prototyping (Tip 61, pp. 327–333).
- **Don't program by coincidence.** Code that works for reasons you don't know will fail for reasons you don't know. Rely only on documented behaviour, document assumptions and test them (Tip 62, pp. 334–340).
- **Estimate the order of your algorithms and test your estimates:** loops are O(n), nested loops O(n²), halving O(lg n), permutations factorial. Plot three or four sizes (Tips 63–64, pp. 343–351).
- **Refactor early, refactor often.** Refactoring is disciplined restructuring that doesn't change external behaviour, done in small, tested steps, like weeding a garden (Tip 65, pp. 354–360).
- **Testing is not about finding bugs.** A test is the first user of your code: thinking about it reduces coupling and clarifies the API. Build end-to-end, design to test, and test your software or your users will (Tips 66–70, pp. 361–374).
- **Use property-based tests to validate your assumptions:** generated inputs check invariants that you and your code might wrongly share (Tip 71, pp. 375–383).
- **Keep it simple and minimize attack surfaces,** use least privilege and secure defaults, encrypt secrets, apply patches quickly, and never roll your own crypto (Tips 72–73, pp. 385–394).
- **Name well; rename when needed.** Names should reflect the role a thing plays; misleading names are worse than meaningless ones (Tip 74, pp. 395–401).

## Section outline

*From the book’s own table of contents (PDF bookmarks). Page numbers are PDF pages: this edition's reflowed text has no printed page numbers.*

- Topic 37. Listen to Your Lizard Brain — p. 327
- Topic 38. Programming by Coincidence — p. 334
- Topic 39. Algorithm Speed — p. 343
- Topic 40. Refactoring — p. 354
- Topic 41. Test to Code — p. 361
- Topic 42. Property-Based Testing — p. 375
- Topic 43. Stay Safe Out There — p. 385
- Topic 44. Naming Things — p. 395

## Notes

| Tip | Statement | Page |
|---:|---|---|
| 61 | Listen to Your Inner Lizard | 330 |
| 62 | Don’t Program by Coincidence | 339 |
| 63 | Estimate the Order of Your Algorithms | 350 |
| 64 | Test Your Estimates | 350 |
| 65 | Refactor Early, Refactor Often | 358 |
| 66 | Testing Is Not About Finding Bugs | 361 |
| 67 | A Test Is the First User of Your Code | 363 |
| 68 | Build End-to-End, Not Top-Down or Bottom Up | 366 |
| 69 | Design to Test | 370 |
| 70 | Test Your Software, or Your Users Will | 373 |
| 71 | Use Property-Based Tests to Validate Your Assumptions | 376 |
| 72 | Keep It Simple and Minimize Attack Surfaces | 389 |
| 73 | Apply Security Patches Quickly | 392 |
| 74 | Name Well; Rename When Needed | 400 |

### Topic 37. Listen to Your Lizard Brain

The topic opens with Gavin de Becker's *The Gift of Fear*: people who are attacked often felt uneasy beforehand and told themselves they were being silly (p. 327). Instincts are patterns packed into the nonconscious brain, some learned by repetition. With experience you lay down tacit knowledge, but instincts have no words: you feel nervous, queasy, or that a job is too much work (pp. 327–328).

| Signal | What it may mean (pp. 328–329) |
|---|---|
| **Fear of the blank page** | A doubt lurking just below perception, which deserves time to crystallize. Or simply fear of making a mistake (imposter syndrome) |
| **Fighting yourself** | Code that feels like walking uphill in mud: the structure may be wrong, or you may be solving the wrong problem |

**How to talk lizard** (Tip 61, pp. 330–332):

1. Stop. Do something mindless away from the keyboard, or sleep on it.
2. Externalize: doodle, or explain it to a coworker (preferably a non-programmer) or a rubber duck.
3. Still stuck? Prototype. Put an "I'm prototyping" sticky note on your screen, remember prototypes are meant to fail and are thrown away, write a one-sentence comment on what you want to learn, and start coding. When the nervousness gives way to urgency, delete the prototype and write the real code.

The same applies to reading other people's code (note what seems strange and look for the patterns that drove it), and to designs or requirements that feel wrong (pp. 332–333).

### Topic 38. Programming by Coincidence

A soldier probes a field for mines, finds none, concludes it's safe, and is blown up; his early probes were merely lucky (p. 334). Fred codes until it seems to work; when it stops working he can't fix it, because he never knew why it worked (pp. 334–335).

| Kind of coincidence | Example (pp. 335–339) |
|---|---|
| **Accidents of implementation** | Relying on undocumented error or boundary behaviour. Fred calls `paint(); invalidate(); validate(); revalidate(); repaint(); paintImmediately();` until the screen draws, and never removes the spurious calls |
| **Close enough isn't** | Field units set to local time gave results off by one. Developers added and subtracted 1 until the codebase was a mass of ±1s; the project was scrapped (footnote: "UTC is there for a reason") |
| **Phantom patterns** | Russian leaders alternating bald and hairy for nearly 200 years; an intermittent error every 1,000 requests may be a race, or a plain bug. Don't assume it, prove it |
| **Accidents of context** | Relying on a GUI being present, English-speaking users, a writable current directory, accurate server time, copied "cargo cult" code |
| **Implicit assumptions** | Undocumented and often conflicting between developers; the bane of all projects |

Reasons not to leave well enough alone: it may only look like it works, the boundary condition may be an accident (another screen resolution, more cores), undocumented behaviour may change in the next release, and extra calls are slower and add bugs (p. 336). For routines you call, **rely only on documented behaviour**, or document your assumption (p. 337). **Tip 62, Don't Program by Coincidence** (p. 339).

**How to program deliberately** (pp. 339–340):

- Always be aware of what you're doing; explain it to a junior.
- Don't code in the dark. Proceed from a plan.
- Rely only on reliable things. Document assumptions (DBC) and test them with assertions.
- Prioritize the hard, important parts.
- Don't be a slave to history: be ready to refactor.

### Topic 39. Algorithm Speed

Pragmatic Programmers estimate the resources algorithms use almost daily: if it runs with 1,000 records, how will it scale to 1,000,000 (p. 343)? **Big-O** notation, O(), gives an upper bound on how a resource grows with input size. It drops low-order terms and constant factors, so one algorithm may be 1,000 times faster than another with the same O(), and it never gives actual times (pp. 344–345).

| Order | Example in the book (pp. 345–346) |
|---|---|
| O(1) | Access element in array, simple statements |
| O(lg n) | Binary search; the base doesn't matter |
| O(n) | Sequential search |
| O(n lg n) | Average quicksort, heapsort |
| O(n²) | Selection and insertion sorts |
| O(n³) | Multiplying two matrices |
| O(Cⁿ) | Traveling salesman, set partitioning |

The book's worked example (p. 345): a routine takes one second for 100 records; for 1,000 records it takes:

- 1 s if O(1)
- about 3 s if O(lg n)
- 10 s if O(n)
- about 33 s if O(n lg n)
- 100 s if O(n²)

An exponential routine would take so long that you're told to make coffee.

> **Vault note:** Scaling the formulas exactly (time × f(1000)/f(100)) gives 1.5 s for O(lg n) and 15 s for O(n lg n). The book's "about three" and "some 33" correspond to multiplying by lg 10 ≈ 3.3, the logarithm of the tenfold growth. Either way the ordering is the point. The widget below shows both.

**Common sense estimation** (pp. 348–349):

- **Simple loops** are O(n): exhaustive search, maximum, checksum.
- **Nested loops** are O(m × n), for example bubble sort.
- **Binary chop** is O(lg n): binary search, tree traversal, first set bit.
- **Divide and conquer** is O(n lg n): quicksort, which is technically O(n²) on sorted input.
- **Combinatoric** algorithms are factorial: five elements to six takes six times longer, and to seven 42 times longer. Heuristics help.

**In practice** (pp. 349–351):

- **Tip 63, Estimate the Order of Your Algorithms:** ask how large the loop bounds can get, and try to turn O(n²) into O(n lg n) with divide and conquer.
- **Tip 64, Test Your Estimates:** run it at varying sizes and plot; three or four points show the curve's shape. Use profilers to count steps. Remember thrashing and sorted input. The only timing that counts is production with real data.
- **Best isn't always best:** a simple insertion sort is as good as quicksort for small inputs; beware high setup costs and premature optimization.

> **Try it:** [How does it scale?](../widgets/07-big-o-scaling.html) — set a baseline time and size, grow the input, and compare the seven orders from the book's table, with the book's own one-second example as a preset.

### Topic 40. Refactoring

Software is less like building construction (architect, contractors, tenants) and more like **gardening**: things are planted, thrive or become compost, and get split, pruned and moved (pp. 354–355). Martin Fowler defines **refactoring** as a "disciplined technique for restructuring an existing body of code, altering its internal structure without changing its external behavior" (p. 355). It is a day-to-day, low-risk activity, like weeding, and it needs good automated unit tests to guarantee behaviour hasn't changed (p. 356).

**When to refactor** (pp. 356–357): when you've learned something. Triggers: duplication (DRY), nonorthogonal design, outdated knowledge, usage, performance, and **the tests pass** (tidy up right after the test goes green).

**Real-world complications** (pp. 357–358): time pressure is the usual excuse, but code needing refactoring is like a growth, cheaper to remove while small. **Tip 65, Refactor Early, Refactor Often.** If it really takes "a week," it's a rewrite: schedule it and tell users of the code.

**How to refactor**, from Fowler (p. 359):

1. Don't refactor and add functionality at the same time.
2. Have good tests first and run them often.
3. Take short, deliberate steps, testing after each.

IDEs now automate renames and extractions. If you must change interfaces, deliberately break the build so old clients fail to compile (pp. 359–360).

### Topic 41. Test to Code

**Tip 66, Testing Is Not About Finding Bugs:** the major benefits come when you think about and write the tests, not when you run them (p. 361).

**Thinking about tests** (pp. 362–363). Writing `return_avid_viewers` (people who watch more than 10 videos a week), thinking about how to test it leads to two discoveries before any code is written:

- Pass the database in rather than using a global: `return_avid_users(db)`.
- The schema has both `opened_video` and `completed_video`, and the requirement is ambiguous, so pass the qualifying field name in as well.

**Tip 67, A Test Is the First User of Your Code** (p. 363): testable code is less coupled, and you must understand something before you can test it (pp. 363–364).

**Test-driven development** (pp. 364–366):

1. Pick a small piece of functionality.
2. Write a test that will pass once it exists.
3. Run all tests; only the new one fails.
4. Write the least code to pass.
5. Refactor.

The cycle takes minutes and helps beginners. But people become slaves to it: chasing 100% coverage, writing redundant tests, building bottom-up. **Tip 68, Build End-to-End, Not Top-Down or Bottom Up** (sidebar, pp. 365–366): we don't know what we're doing when we start, so build small end-to-end slices.

**You need to know where you're going** (pp. 366–367): Ron Jeffries' 2006 TDD Sudoku series refined the board representation over five posts and was abandoned. Peter Norvig started from constraint propagation and handled representation in a dozen lines.

**Unit testing against contract** (pp. 367–370). Chips have built-in self tests; software needs testability from the start. A square root routine's contract is: argument ≥ 0, and |result² − argument| ≤ ε·argument. The tests that follow:

- Reject a negative argument.
- Accept zero, the boundary.
- Check values across the range.

For a module A that uses a DataFeed and a LinearRegression, test DataFeed's contract, then LinearRegression's, then A's; if only A fails, the problem is in A. **Tip 69, Design to Test** (p. 370).

**Ad hoc tests and test windows** (pp. 370–372):

- Turn ad hoc REPL pokes into unit tests.
- In production, use consistently formatted logs, a hot-key or magic URL diagnostic window, or feature switches for extra diagnostics.

**A confession** (sidebar, p. 372): Dave stopped writing tests for a couple of months and his code changed "not a lot": after 30+ years, he does the thinking anyway. He still writes tests for shared code and external dependencies, because tests communicate.

**A culture of testing** (pp. 372–374): the choices are Test First, Test During, or Test Never, which is what "Test Later" really means. All tests pass all the time. Treat test code like production code and avoid fragile tests on GUI positions, timestamps or message wording. **Tip 70, Test Your Software, or Your Users Will** (p. 373).

### Topic 42. Property-Based Testing

If you write both the code and its tests, a wrong assumption can be in both (p. 375). Rather than splitting coding and testing between people, let the computer, which has no preconceptions, test for you. Contracts and invariants, together called **properties**, can drive automated tests (pp. 375–376). **Tip 71, Use Property-Based Tests to Validate Your Assumptions** (p. 376).

**Sorting** (pp. 376–377): with Python's Hypothesis and pytest, two properties are tested: the length is unchanged, and each element is ≤ its successor. Hypothesis runs each test 100 times with different lists, as if you'd written 200 tests. Strategies compose, for example lists of naturals of at most 100 elements (pp. 377–378).

**Finding bad assumptions** (pp. 378–382):

- A `Warehouse` with `{"shoes": 10, "hats": 2, "umbrellas": 0}` and an `order` function pass their hand-written unit tests.
- The property under test: stock taken plus stock remaining equals the original. It is run with item sampled from shoes and hats, quantity 1–4.
- Hypothesis reports the falsifying example `item='hats', quantity=3`: `in_stock` only checked for at least one item.
- The fix: `in_stock(item, quantity)` checks `stock >= quantity`.

**Property tests surprise you** (pp. 382–383): the test was about stock levels and found a bug in `in_stock`. When one fails, copy its parameters into a regular unit test, both to focus on the failure and to prevent regression, since random values may not recur. Property tests also help design: they make you think about what must not change (p. 383).

> **Try it:** [Hunt the falsifying example](../widgets/07-property-test.html) — run the book's stock-level property against the buggy and fixed `Warehouse`, watch random cases until one fails, then shrink it to the smallest counterexample.

### Topic 43. Stay Safe Out There

The first edition said "we don't need to be as paranoid as spies or dissidents." The authors were wrong (p. 385). Breaches happen mostly because developers were careless, not because attackers were clever. When the code works you are 90% done, with "the other 90%" to go: how it can go wrong, and how an external actor could deliberately break it. Security through obscurity doesn't work (pp. 385–386).

| Principle | In practice (pp. 386–392) |
|---|---|
| **Minimize attack surface area** | Complex code is porous. Sanitize all input: the book's Ruby `system("wc -c #{name}")` example is shown with input `test.dat; rm -rf /`, and `$SAFE = 1` taints input. Unauthenticated services, too many authenticated users, revealing output ("Password is used by another user") and debugging info are all attack vectors. **Tip 72** |
| **Least privilege** | Take the least privilege for the shortest time: Unix `login` drops root after authenticating. Saltzer (1974). Use finer grains than admin/user |
| **Secure defaults** | Most secure by default (masked passwords); let users choose convenience |
| **Encrypt sensitive data** | Don't check secrets, API or SSH keys into version control; use config or environment at deploy |
| **Maintain security updates** | **Tip 73, Apply Security Patches Quickly**: the largest breaches were on systems behind on updates |

**Password antipatterns**, NIST SP 800-63B (sidebar, pp. 391–392). Do not:

- Cap length below 64 (256 is a good maximum), or truncate.
- Restrict special characters.
- Offer hints or security questions.
- Disable paste.
- Impose composition rules.
- Force periodic changes without cause.

**Common sense vs. crypto** (pp. 393–394): never do crypto yourself. Rely on vetted, maintained libraries, and consider a third-party authentication provider rather than implementing hashing, salting and storage yourself.

### Topic 44. Naming Things

Names reveal intent and belief. Name things by the **role** they play, asking "what is my motivation to create this?" Failing to find a name often reveals the idea makes no sense (p. 395). The **Stroop effect** shows the brain reads words faster than it recognizes colours, so written names carry weight (pp. 395–396).

| Before | After (pp. 396–397) | Why |
|---|---|---|
| `user = authenticate(credentials)` | `customer` or `buyer` | Reminds you what the person is trying to do |
| `deductPercent(double amount)` | `applyDiscount(Percentage discount)` | Names intent, and a type settles 0–100 versus 0.0–1.0 |
| `Fib.fib(n)` | `Fib.of(0)`, `Fib.nth(20)` (= 4181) | Read in the module's context |

- **Honor the culture** (pp. 398–399): `i`, `j`, `k` are right in C loops and wrong in Clojure. Follow the community's camelCase or snake_case.
- **Consistency** (p. 399): every project has jargon. Spread it by pair programming or a project glossary, which becomes a pattern language.
- **Renaming is even harder** (pp. 399–400): misleading names, like a `getData` that writes to an archive, are worse than meaningless ones. **Tip 74, Name Well; Rename When Needed.** If you can't rename, that's an ETC violation to fix first.

## Trade-offs at a glance

| Choice | Buys | Costs |
|---|---|---|
| Push on through resistance | Feels productive | Ignores feedback that the design is wrong |
| Prototype to unblock | Lowers stakes; surfaces doubts | The code must be thrown away |
| Rely on observed behaviour | Quick | Breaks on the next release or another context |
| Exact Big-O analysis | Predicts scaling | Hides constants; small inputs may favour simple code |
| Refactor continuously | Cheap, small fixes; less entropy | Needs good tests; feels like "not features" |
| Strict TDD | Always have tests | Redundant tests; local polishing without direction |
| Example-based unit tests | Precise, readable | Share the author's assumptions |
| Property-based tests | Find unshared assumptions | Failures can be hard to pin down; random inputs vary |
| Clever project names | Branding (p. 398) | Not for code identifiers |

## Beyond the book

- **Shrinking** is what makes property-based tests practical: Hypothesis and QuickCheck reduce a failing input to a minimal one. The book shows the shrunken `hats, 3` but doesn't name the mechanism; the [property-test widget](../widgets/07-property-test.html) and the [lab](../lab/07-warehouse-properties/README.md) implement a simple version.
- **Measuring growth.** Plotting time against n on log–log axes turns a power law into a straight line whose slope is the exponent; counting operations instead of wall time removes noise, the idea behind the book's "use code profilers to count" advice (p. 351).
- **Naming and DDD.** Eric Evans' *ubiquitous language* (*Domain-Driven Design*, 2003) is the same idea as the project glossary on p. 399, carried into the code's types and modules.

## Connections

- **Related chapters:** [2. A Pragmatic Approach](02-a-pragmatic-approach.md) (ETC, DRY, prototypes, estimating), [3. The Basic Tools](03-the-basic-tools.md) (debugging: "don't assume it, prove it"), [4. Pragmatic Paranoia](04-pragmatic-paranoia.md) (design by contract, assertions, headlights), [9. Pragmatic Projects](09-pragmatic-projects.md) (ruthless and continuous testing).
- **Run it:** [Properties find the warehouse bug](../lab/07-warehouse-properties/README.md) — a standard-library property tester runs the book's stock-level property against the buggy and fixed `Warehouse`, and shrinks the failure to `hats, 3`.
- **Run it:** [Counting the orders](../lab/07-operation-counts/README.md) — counts comparisons for linear search, binary search, insertion sort and merge sort at growing n, and fits the growth exponent from the log–log slope.

## Check yourself

*Questions and answers are the vault's, written from the notes above; answers cite the book's PDF pages.*

1. **What are the steps of the book's prototyping "brain hack" for a blank page?**

   *Answer:* Put an "I'm prototyping" sticky note up, remind yourself prototypes fail and are thrown away, write a one-sentence comment of what you want to learn, and start coding (p. 331).

2. **Name three reasons not to leave coincidentally working code alone.**

   *Answer:* It may not really work; the boundary condition may be an accident of this context; undocumented behaviour may change next release; extra calls are slower and add bugs (p. 336).

3. **Why was the project with ±1 time corrections scrapped?**

   *Answer:* Without a proper model of time, units set to local time were "only" off by one by coincidence; the code became an untenable mass of +1 and −1, none of it correct (p. 337).

4. **A loop inside a loop over the same n items is:**
   - [ ] O(n lg n)
   - [x] O(n²)
   - [ ] O(2n)

   *Answer:* Nested loops are O(m × n), O(n²) when both bounds are n (p. 348).

5. **What are Fowler's three rules for refactoring safely?**

   *Answer:* Don't refactor and add functionality at once; have good tests first and run them often; take short, deliberate steps (p. 359).

6. **Thinking about how to test `return_avid_viewers` changed its API how?**

   *Answer:* It takes the database as a parameter instead of using a global, and the qualifying field name (opened vs completed) as a parameter (pp. 362–363).

7. **What falsifying example did Hypothesis find, and what was the bug?**

   *Answer:* `item='hats', quantity=3`; `in_stock` checked only for at least one item rather than enough to fill the order (pp. 381–382).

8. **What should you do with a property test's failing parameters?**

   *Answer:* Turn them into a regular unit test, to focus on the problem and to act as a regression test, because random inputs may not recur (p. 383).

9. **Name two NIST password recommendations the book lists.**

   *Answer:* Allow at least 64 characters (256 max), don't truncate, allow all printable characters and Unicode, no hints, allow paste, no composition rules, no arbitrary forced changes (pp. 391–392).

10. **Why is `applyDiscount(Percentage discount)` better than `deductPercent(double amount)`?**

    *Answer:* It names the intent rather than the mechanism, and the type documents whether a percentage is 0–100 or 0.0–1.0 (p. 397).
