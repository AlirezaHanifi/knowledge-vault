---
book: the-pragmatic-programmer
chapter: 9
title: "Pragmatic Projects"
pages: "435–468"
---

# 9. Pragmatic Projects

[← 8. Before the Project](08-before-the-project.md) · [Book](../README.md) · [10. Postface →](10-postface.md)

## Summary

The last chapter moves from individual practice to project-sized issues:

- Ground rules for **pragmatic teams** (Topic 49).
- Why imitating a method's surface artifacts fails, which the book calls a **cargo cult** (Topic 50).
- The magic trio of **version control, testing and automation**, the Pragmatic Starter Kit (Topic 51).
- **Delighting** the sponsor, because the perception of success is what counts (Topic 52).
- **Signing** your work with pride (Topic 53).

The last tip in the book is a direct consequence of all the rest (pp. 435–436).

## Key takeaways

- **Maintain small, stable teams** of under 10–12 people who trust each other. Fifty people are a horde (Tip 84, pp. 437–438).
- **Apply the individual practices at team level:** no broken windows (quality is built in, not bolted on), watch for boiled frogs, schedule the knowledge portfolio, communicate team presence (Tip 85, pp. 438–441).
- **Stay DRY through frictionless communication, and organize fully functional teams** that can build tracer bullets end to end without gates and handoffs (Tip 86, pp. 442–443).
- **Do what works, not what's fashionable:** a once-a-week daily standup is a coconut airport. Pilot ideas, keep what works, and aim to **deliver when users need it** (Tips 87–88, pp. 446–451).
- **Use version control to drive builds, tests and releases.** Test early, often and automatically; coding isn't done until all the tests run (Tips 89–91, pp. 452–455).
- **Use saboteurs to test your testing, and test state coverage rather than code coverage.** Find bugs once: each escaped bug gets a test (Tips 92–94, pp. 457–459).
- **Don't use manual procedures** (Tip 95, pp. 459–460). **Delight users, don't just deliver code**: ask how everyone will know the project succeeded (Tip 96, pp. 462–464). **Sign your work** (Tip 97, pp. 465–466).

## Section outline

*From the book’s own table of contents (PDF bookmarks). Page numbers are PDF pages: this edition's reflowed text has no printed page numbers.*

- Topic 49. Pragmatic Teams — p. 437
- Topic 50. Coconuts Don’t Cut It — p. 446
- Topic 51. Pragmatic Starter Kit — p. 452
- Topic 52. Delight Your Users — p. 462
- Topic 53. Pride and Prejudice — p. 465

## Notes

| Tip | Statement | Page |
|---:|---|---|
| 84 | Maintain Small, Stable Teams | 438 |
| 85 | Schedule It to Make It Happen | 441 |
| 86 | Organize Fully Functional Teams | 443 |
| 87 | Do What Works, Not What’s Fashionable | 447 |
| 88 | Deliver When Users Need It | 450 |
| 89 | Use Version Control to Drive Builds, Tests, and Releases | 453 |
| 90 | Test Early, Test Often, Test Automatically | 454 |
| 91 | Coding Ain’t Done ’Til All the Tests Run | 455 |
| 92 | Use Saboteurs to Test Your Testing | 457 |
| 93 | Test State Coverage, Not Code Coverage | 458 |
| 94 | Find Bugs Once | 459 |
| 95 | Don’t Use Manual Procedures | 460 |
| 96 | Delight Users, Don’t Just Deliver Code | 464 |
| 97 | Sign Your Work | 465 |

### Topic 49. Pragmatic Teams

Programmers are like cats: intelligent, strong-willed, opinionated, independent (p. 437). A team is small and mostly stable. Fifty people are a horde, and people constantly pulled onto other assignments are "strangers temporarily sharing a bus stop in the rain." A pragmatic team has under 10–12 members who come and go rarely and trust each other. **Tip 84, Maintain Small, Stable Teams** (pp. 437–438). A footnote notes that communication paths grow quickly with team size, until communication breaks down (p. 467).

> **Try it:** [Team size and communication paths](../widgets/09-team-size.html) — grow a team and watch the pairwise communication paths multiply, with the book's 10–12 guideline and its "horde" of fifty marked.

| Individual practice | At team level (pp. 438–444) |
|---|---|
| **No broken windows** | Quality is a team issue; a "quality officer" is ridiculous. Quality is built in, not bolted on |
| **Boiled frogs** | Teams assume someone else is handling it. Everyone monitors for scope, time-scale and environment changes; keep metrics on new requirements (a burnup chart shows moving goalposts) |
| **Knowledge portfolio** | Schedule old-system maintenance, process reflection, new-tech experiments (vetted with prototypes) and learning. **Tip 85, Schedule It to Make It Happen** |
| **Communicate team presence** | Great teams speak with one voice externally and debate lively internally. Brand the project with an off-the-wall name and a 30-minute zany logo |
| **Don't repeat yourselves** | Communication must be instant and frictionless. Waiting a week for a meeting is friction (Andy met teams with daily standups on Fridays) |
| **Team tracer bullets** | Separate roles add gates and handoffs, which Lean calls waste. Have frontend, UX, server, DBA and QA in the team. **Tip 86, Organize Fully Functional Teams** |
| **Automation** | Formatting, tests and deploys automated; the team needs tool-building skills |
| **Know when to stop adding paint** | Give just enough structure, then let individuals shine |

The challenges include the ditch puzzle (4 workers take 6 hours, so how long for 8?) applied to coding, and reading *The Mythical Man-Month*, "buy two copies so you can read it twice as fast" (p. 445).

### Topic 50. Coconuts Don't Cut It

After the war, islanders rebuilt the airport from vines, coconut shells and palm fronds, but the planes didn't come: they imitated the form, not the content. This is a **cargo cult** (p. 446). The authors saw a "Scrum" team doing a daily standup once a week, with four-week iterations that became six or eight, because they used a popular agile scheduling tool (pp. 446–447).

**Context matters** (p. 447): copying Spotify, Netflix, Stripe or GitLab ignores market, constraints, expertise, size, culture and users. **Tip 87, Do What Works, Not What's Fashionable.** How do you know what works? Try it: pilot with a small team, keep what works, discard the rest. Those companies didn't follow their current processes while growing (pp. 447–448).

**One size fits no one well** (pp. 448–449): certification that rewards memorizing rules is worse; take the best pieces from several methods. Scrum alone doesn't cover technical practice or governance. Sidebar, "Be Like Them!": to operate like Netflix, first get a few hundred thousand servers and tens of millions of users (p. 449).

**The real goal** (pp. 449–451) is to deliver working software that gives users a new capability at a moment's notice. Shorten the cycle step by step:

```mermaid
flowchart LR
    Y["years"] --> M["months"] --> W4["four-week sprints"] --> W2["two weeks"] --> W1["one week"] --> D["daily"] --> OD["on demand"]
```

**Tip 88, Deliver When Users Need It.** On demand doesn't mean every minute. It needs the starter kit, trunk-based development and feature switches. Beginners might start with Scrum plus XP's technical practices; experienced teams might use Kanban and Lean. Over-investing in one method calcifies you: "Might as well be using coconuts" (p. 451).

### Topic 51. Pragmatic Starter Kit

A Model-T's starting instructions ran to more than two pages; modern cars start with a button (Whitehead: civilization advances by extending the operations we can perform without thinking) (p. 452). Every recurring task must be automatic and repeatable on any capable machine. The starter kit's three legs are **version control, regression testing and full automation** (pp. 452–453).

**Drive with version control** (pp. 453–454):

- Build machines become ephemeral cloud instances, not "one hallowed, creaky machine in the corner."
- Deployment configuration is versioned too.
- Commits trigger build, test and deploy in a container, and a tag specifies a release.

**Tip 89, Use Version Control to Drive Builds, Tests, and Releases.**

**Ruthless and continuous testing** (pp. 454–459). Developers test gently, avoiding the weak spots; Pragmatic Programmers find their bugs now. Fine nets (unit tests) catch minnows and coarse nets (integration tests) catch sharks. **Tip 90, Test Early, Test Often, Test Automatically.** A good project may have more test code than production code. **Tip 91, Coding Ain't Done 'Til All the Tests Run.** The test environment should match production: gaps are where bugs breed.

| Kind of test | What it shows (pp. 455–457) |
|---|---|
| **Unit** | Each module honours its contract; the foundation of everything else |
| **Integration** | Subsystems work together; often the single largest source of bugs |
| **Validation and verification** | It's what users *need*, with their real access patterns |
| **Performance** | It meets requirements under real load; is it scalable? |

**Testing the tests** (p. 457): cause the bug deliberately and make sure the test complains. **Tip 92, Use Saboteurs to Test Your Testing.** Introduce bugs on a separate branch, or use Netflix's Chaos Monkey to kill services.

**Testing thoroughly** (pp. 457–458): coverage tools give a feel, but don't expect 100%. What matters is states. `int test(int a, int b) { return a / (a + b); }` with a and b in 0–999 has 1,000,000 logical states, one of which (a + b = 0) fails, and executing the line doesn't tell you that. **Tip 93, Test State Coverage, Not Code Coverage.** Property-based testing generates states for you (p. 458).

> **Try it:** [Saboteurs and state coverage](../widgets/09-saboteurs.html) — plant bugs in a small function and see which ones its test suite catches, then sample the book's `a / (a + b)` input space and see how rarely random tests find the one failing state.

**Tightening the net** (p. 459): if a bug slips through, add a test to trap it next time. **Tip 94, Find Bugs Once**: once a human tester finds a bug, it's the last time a human finds it.

**Full automation** (pp. 459–460): use shell scripts with rsync and ssh, or Ansible, Puppet, Chef or Salt, with no manual intervention. At one client, many pages of click-here IDE setup left every machine slightly different, and bugs appeared on some machines only. **Tip 95, Don't Use Manual Procedures.** Scripts are repeatable and versioned; a manual step "just for this one part" is a very large broken window.

### Topic 52. Delight Your Users

The goal is to delight users (Guy Kawasaki's epigraph), not to mine their data or count eyeballs; delivering working software on time isn't enough (p. 462). Users' expectations aren't about software, so ask: *how will you know that we've all been successful a month (or a year) after this project is done?* (pp. 462–463).

The answers can surprise you. Recommendations might be judged on customer retention; a database consolidation on data quality or cost savings. Then (p. 463):

- Make sure everyone on the team is clear about these expectations.
- Choose the path that moves closer to them.
- Critically analyze requirements against them. Stated requirements are often an amateur implementation plan; suggest changes that move closer to the objective.
- Keep thinking about them as the project progresses.

**Tip 96, Delight Users, Don't Just Deliver Code** (p. 464). Your title should really be "Problem Solver."

### Topic 53. Pride and Prejudice

**Tip 97, Sign Your Work** (p. 465). Artisans signed their work. But code ownership can breed territorial fiefdoms and prejudice against coworkers' code, so follow the Golden Rule and mutual respect. Anonymity breeds sloppiness. Code must be owned, but not necessarily by an individual: XP's communal ownership needs practices such as pairing to guard against anonymity. Your signature should signal quality: solid, well written, tested and documented (pp. 465–466).

## Trade-offs at a glance

| Choice | Buys | Costs |
|---|---|---|
| Large or shifting teams | Headcount | Communication breaks down; no trust |
| Small, stable, full-function team | Trust, end-to-end delivery | Needs broad skills in one team |
| Specialist teams with handoffs | Deep expertise per stage | Gates, waiting, waste; context lost |
| Copy a famous company's process | Off-the-shelf answers | Different context; cargo cult |
| Pilot and keep what works | Fits your context | Requires ongoing experiment |
| Manual build and deploy | No up-front scripting | Unrepeatable; machine drift; a broken window |
| Code coverage targets | Easy to measure | Lines aren't states |
| Saboteurs, chaos testing | Confidence the alarms work | Effort; must be safe to run |
| Individual or communal ownership | Pride, accountability | Fiefdoms, or anonymity without pairing |

## Beyond the book

- **Communication paths.** The footnote on p. 467 gives the growth formula; the standard form is n(n − 1)/2 pairs, so 10 people have 45 paths and 50 people have 1,225. Brooks' law ("adding manpower to a late software project makes it later") is the [Mythical Man-Month](https://en.wikipedia.org/wiki/The_Mythical_Man-Month) result the challenge on p. 445 points to.
- **Mutation testing** automates the book's saboteurs: tools such as PIT (Java), mutmut (Python) and Stryker (JavaScript) generate small code changes and report which survive the tests. The [lab](../lab/09-saboteurs/README.md) builds a tiny version with the standard library.
- **DORA metrics** (Forsgren, Humble and Kim, *Accelerate*, 2018) measure the "deliver when users need it" goal: deployment frequency, lead time for changes, change failure rate and time to restore.

## Connections

- **Related chapters:** [1. A Pragmatic Philosophy](01-a-pragmatic-philosophy.md) (broken windows, boiled frogs, knowledge portfolio, communicate), [2. A Pragmatic Approach](02-a-pragmatic-approach.md) (DRY, tracer bullets), [3. The Basic Tools](03-the-basic-tools.md) (version control, shell games), [7. While You Are Coding](07-while-you-are-coding.md) (test to code, property-based testing), [8. Before the Project](08-before-the-project.md) (requirements, agility).
- **Run it:** [Saboteurs: do the tests catch planted bugs?](../lab/09-saboteurs/README.md) — generates mutants of a small function, runs a weak and a strong test suite against each, and reports which bugs survive; then samples the `a / (a + b)` state space.

## Check yourself

*Questions and answers are the vault's, written from the notes above; answers cite the book's PDF pages.*

1. **How big is a pragmatic team, and what isn't a team?**

   *Answer:* Under 10–12 stable members who trust each other; fifty people are a horde, and constantly reassigned strangers are "sharing a bus stop in the rain" (pp. 437–438).

2. **Why does the book call a "quality officer" ridiculous?**

   *Answer:* Quality can only come from every team member's contributions; it's built in, not bolted on (p. 438).

3. **What is a cargo cult, in the book's software example?**

   *Answer:* Imitating form without content: a team "doing Scrum" with a weekly daily standup and slipping four-week iterations, relying on an agile scheduling tool (pp. 446–447).

4. **What are the three legs of the Pragmatic Starter Kit?**

   *Answer:* Version control, regression testing, and full automation (p. 453).

5. **How should releases to staging or production be specified?**

   *Answer:* By a tag in version control; builds and tests are triggered by commits or pushes and run in a container in the cloud (pp. 453–454).

6. **Why is code coverage not enough, using the book's function?**
   - [ ] Because coverage tools are inaccurate
   - [x] `a / (a + b)` has 1,000,000 states and one fails; executing the line doesn't reveal it
   - [ ] Because integration tests matter more

   *Answer:* States aren't lines of code; test state coverage (p. 458).

7. **What does "Find Bugs Once" require?**

   *Answer:* Once a human tester finds a bug, add an automated test so it's the last time a human finds it, however trivial (p. 459).

8. **What question surfaces users' real expectations?**

   *Answer:* "How will you know that we've all been successful a month (or a year) after this project is done?" (pp. 462–463).
