---
book: the-managers-path
chapter: 5
title: "Managing a Team"
pages: "75–97"
---

# 5. Managing a Team

[← 4. Managing People](04-managing-people.md) · [Book](../README.md) · [6. Managing Multiple Teams →](06-managing-multiple-teams.md)

## Summary

Managing a team is more than managing its individuals: the job changes, and it is a new set of skills rather than a continuation of senior engineering. This chapter turns from people tasks back to the technical, strategic and leadership parts of running one team. It argues for staying a little in the code, gives a first-aid kit for dysfunctional teams (not shipping, people drama, overwork, collaboration problems), questions the manager-as-shield, and lays out how to drive good decisions with data, product sense and retrospectives. Conflict avoidance gets a list of dos and don'ts, toxic team members — the brilliant jerk, the noncommunicator, the person who lacks respect — get direct treatment, and the chapter closes with rules of thumb for planning a team's quarter (pp. 75–97).

## Key takeaways

- **Stay technical enough to feel the bottlenecks.** Small features and bug fixes reveal slow builds, painful deploys and on-call misery, and keep your judgement and credibility (pp. 77–78).
- **Debug the basic dysfunctions:** teams that don't ship (often infrequent releases hiding pain), people drama, overwork (dedicate 20% of planning to sustainability), and collaboration problems (pp. 79–81).
- **Shield the team from drama, not from context.** People need to know *why* goals exist; denying outside events breeds gossip; and you're not their parent (pp. 83–84).
- **You're accountable for decisions you only guide:** bring data, flex product muscles, look two steps ahead, review outcomes, and run retrospectives (pp. 84–86).
- **Tame conflict instead of avoiding it.** Don't hide behind votes; depersonalize decisions with clear processes; address issues early; be kind, not nice (pp. 86–89).
- **Toxic people destroy psychological safety.** Openly refuse to tolerate the brilliant jerk's behaviour, address the noncommunicator's fear, and ask the disrespectful person whether they want to be on the team (pp. 89–92).
- **Plan with rules of thumb:** about 10 productive weeks per engineer per quarter, 20% for sustaining work, say no near deadlines by cutting scope, double quick estimates, and shield the team from estimate requests (pp. 93–95).

## Section outline

*From the book’s own table of contents (PDF bookmarks); printed page numbers.*

- Staying Technical — p. 77
- Debugging Dysfunctional Teams: The Basics — p. 79
  - Not Shipping — p. 79
  - People Drama — p. 80
  - Unhappiness Due to Overwork — p. 80
  - Collaboration Problems — p. 81
- The Shield — p. 83
- How to Drive Good Decisions — p. 84
  - Create a Data-Driven Team Culture — p. 84
  - Flex Your Own Product Muscles — p. 85
  - Look into the Future — p. 85
  - Review the Outcome of Your Decisions and Projects — p. 85
  - Run Retrospectives for the Processes and Day-to-Day — p. 85
- Good Manager, Bad Manager: Conflict Avoider, Conflict Tamer — p. 86
  - The Dos and Don’ts of Managing Conflict — p. 87
- Challenging Situations: Team Cohesion Destroyers — p. 89
  - The Brilliant Jerk — p. 90
  - The Noncommunicator — p. 91
  - The Employee Who Lacks Respect — p. 92
- Advanced Project Management — p. 93
  - Project Management Rules of Thumb — p. 93
- Assessing Your Own Experience — p. 96

## Notes

At every step beyond this one the job is different, and the hardest thing to prepare for is doing totally different things (p. 75). The author's job description for an **engineering lead** (pp. 75–76):

- Spends less time coding, but still ships bug fixes and small features without blocking the team; mostly clears bottlenecks and roadblocks.
- Identifies the highest-value projects and keeps the team focused on them, partnering with the product lead on scope.
- Plans headcount and recruits.
- Manages people with skills different from their own, with frequent feedback — not only at review time.
- Leads the technical roadmap for the product group ("pillar"): timeline, scope and risk; identifies strategic technical debt, weighs its cost and benefit, and proposes when to pay it down.

> **Becoming a People Manager** (bethanye Blount, pp. 76–77). Made a manager in a company that had resisted managers, she managed engineers far more senior than she was and couldn't lead by knowing the most. One helped with ongoing feedback; the other transferred away, then returned months later. Being a good manager isn't about having the most technical knowledge; supporting people mattered more.

### Staying Technical

Engineering management is a technical discipline: even when you stop writing code you guide technical decisions, hold architects and senior staff accountable, and check decisions pass the "technical smell test" in the context of the team and business. Without technical credibility you face an uphill battle and limited options (p. 77).

Why write small code at this level (p. 78)?

- **You feel the bottlenecks.** A slow build, long deploys or a nightmare on-call show up when an experienced engineer struggles with trivial tasks — imagine how your team feels. Technical debt is easier to spot and prioritize after slogging through the code.
- **You can judge what's possible.** When the product manager has a crazy idea you can evaluate it (beware overconfidence), and find the shortest path through the systems.

Some companies split the tracks so cleanly that new managers get large teams at once and code only on nights and weekends. There, stay technical until you've mastered what you want to learn, then decide: stopping too early may cap you at middle management (p. 78).

### Debugging Dysfunctional Teams: The Basics

Missed deliverables, unhappy people, quitting, a frustrated product manager, low energy — something is wrong, but what (p. 79)?

| Dysfunction | What's going on | What to do (pp. 79–81) |
|---|---|---|
| **Not shipping** | Even research teams have deliverables; humans feel good setting and meeting small goals. Infrequent releases (weekly or less) hide poor release tooling, manual testing, oversized features and developers who can't break work down | Balance pushing and holding back; roll up your sleeves on the slipping part; remove the bottlenecks. The author's team went from painful hours-long weekly releases to daily ones — releases had been a **point of resource contention**, and morale improved immediately |
| **People drama** | The "brilliant asshole" kept too long; or someone who stirs drama, dwells on the negative, gossips, plays us-against-them | Be brave and act quickly. Your manager may find the brilliant jerk even harder to tackle, seeing only output; a team move may help. Give the negative person clear examples and quick corrective feedback — or help them leave on good terms |
| **Unhappiness due to overwork** | Usually has fixable roots | If production instability causes it, slow the roadmap and measure alerts, downtime and incidents; **dedicate 20% of every planning session to "sustainability" work.** In a time-critical crunch, be a cheerleader — help with the work, order dinner, promise a break — then learn from it: cut features, push back on unrealistic dates |
| **Collaboration problems** | Friction with product, design or other teams drags everyone down | Regular touchbases with peers; gather actionable feedback; never undermine peers in front of your team. Within the team, create time together that isn't about work — even introverts want relatedness |

> **Run it:** [Release cadence and contention](../lab/05-release-cadence/README.md) simulates the same stream of changes shipped weekly and daily, and counts how often a broken change blocks everyone else's.

> **Ask the CTO: Managing a Former Peer** (pp. 82–83). Acknowledge the awkwardness and ask for honest help; be a little vulnerable. Use your new power to override technical decisions very cautiously, and don't micromanage former peers, who are sensitive to you being "rewarded." Let go of old work — hand former peers control of technical areas you owned and give juniors new challenges; first-line managers write small features and fixes, not deep new systems. Pick your battles: they may even try to undermine you.

### The Shield

The advice to be a shield — a "bullshit umbrella" — is half right (pp. 83–84):

| Shielding helps | Shielding hurts |
|---|---|
| Teams exposed to irrelevant toxic drama get distracted and stressed; engineering doesn't need customer-service politics. Help people focus on what they can change | **People need context, not just goals:** if a system that isn't ready means operational problems in November, the team deserves to know — context is how they decide where to spend energy |
| Workplace drama is usually an ego-entertaining drain | **Denying outside events** (layoffs elsewhere that the team hears about secondhand) creates the feeling something bad is being hidden. Share it plainly and with low emotion |
| | **You're a shield, not a parent.** Treating the team as fragile children makes you take their mistakes and disagreements personally; they are adults owed respect |

### How to Drive Good Decisions

The product manager owns the roadmap and the tech lead the technical details, but **you are accountable for the team's progress through both** — judged on decisions you can only guide (p. 84).

| Practice | How (pp. 84–86) |
|---|---|
| **Create a data-driven team culture** | Add team productivity (time to complete features) and quality data (time on outages, bugs found in QA or after release) to the business data your product head already uses |
| **Flex your own product muscles** | Whoever depends on your work — external users, other engineers, a support team — is your customer. Customer empathy gives engineers context and shows where engineering effort matters most |
| **Look into the future** | Think two steps ahead: technical projects often win support by enabling features (rewriting checkout to add Apple Pay; a framework that streams changes over WebSockets). Ask product what's coming; follow technology |
| **Review the outcome of decisions and projects** | Did the team move faster after the rewrite? Did customers behave as predicted? What did the A/B tests teach? |
| **Run retrospectives** | Regularly, agile or not, on requirements, code quality and day-to-day — more subjective than metrics but arguably more valuable, because it is what the team itself notices |

### Good Manager, Bad Manager: Conflict Avoider, Conflict Tamer

Two overworked teams, each with a "Charles" on a pet project (pp. 86–87):

| Jason, the conflict avoider | Lydia, the conflict tamer |
|---|---|
| Asks the team to vote on which projects to drop; they vote out Charles's project — a surprise only to Charles, whom Jason never told | Tells Charles in a 1-1 that priorities changed and the team needs him on the rewrite — an unpleasant conversation she owns |
| Never says no to other teams, never asks for more people; the team can't prioritize and nurses grudges | Pushes for more people, explains why the team took the project, structures technical disagreements with options and feedback |
| Seen as cool but impossible to get decisions from; nobody feels secure | Seen as tough but fair; the team gets through disagreements and collaborates well |

Constant bickering is painful, but **artificial harmony** is worse: create a safe environment for disagreement rather than pretend it doesn't exist (p. 87).

**The dos and don'ts of managing conflict** (pp. 87–89):

| Don't | Do |
|---|---|
| **Rely exclusively on consensus or voting.** It assumes impartiality, equal stakes and equal knowledge, which teams rarely have — and it can be cruel. Don't stage votes to deliver bad news you should deliver yourself | **Set up clear processes to depersonalize decisions:** shared goals, risks and questions; a named decision owner; who is consulted and who is informed |
| **Turn a blind eye to simmering issues.** Major problems shouldn't surface first in a review — or first through several peers' feedback, which means you weren't paying attention | **Address issues without courting drama.** Is it ongoing? Have you seen it? Do many people struggle with it? Is there a power dynamic or bias? You're not the team's therapist |
| **Take it out on other teams.** Avoiders often turn bully toward outsiders after cross-team incidents, venting the accountability they won't demand at home | **Be kind, not nice.** Nice is polite-society smoothness; kind is telling someone they aren't ready for promotion, with what to do about it, or that their behaviour disrupts meetings |
| **Be afraid** — of deciding, seeming demanding, people quitting or disliking you | **Get curious** about your motives: am I pushing this decision to the team because they're best placed, or because I fear an unpopular call? |

### Challenging Situations: Team Cohesion Destroyers

A test of a happy team — do they stay for evening pizza? — is flawed (obligations aren't disengagement), but gelled teams do joke, get coffee and feel friendly (pp. 89–90). **The real goal is psychological safety**: willingness to take risks and make mistakes in front of each other. Build it by getting to know people — the birthday party, the ski trip, the marathon training — which fosters relatedness. "Culture fit" can mask discrimination but comes from a wise place: friendly teams gel faster and do better (p. 90). Toxic people make everyone around them less effective, so deal with them quickly (p. 90).

| Type | Behaviour | What to do (pp. 90–92) |
|---|---|---|
| **The brilliant jerk** | Outsized results, ego-driven; bullies with intellect, cuts down dissent, ignores those deemed unequal. Clings to brilliance like a life raft | Best of all, don't hire one; firing takes rare confidence, but at least don't promote them. Expect a fight over all feedback. **Openly refuse to tolerate bad behaviour** — here criticism may be public, neutral and in the moment ("Please do not speak to people that way; it is disrespectful") — but only for behaviour harmful to the group. Priorities: protect the team, then each individual, then yourself |
| **The noncommunicator** | Hides information, works in secret to unveil perfect work, reverts others' commits or does their tickets, avoids code and design review | Nip it in the bud, making clear it misses expectations. Look for the root: fear of being found lacking, wanting more responsibility, a harsh culture, or a team excluding someone different — then fix the team or move the person |
| **The employee who lacks respect** | Doesn't respect you, or their teammates | Ask whether they want to be on your team. Yes — lay out expectations clearly and calmly. No — move them or help them leave. Pull off the Band-Aid: the rest of the team will wonder whether they're right |

### Advanced Project Management

The organization will expect off-the-cuff estimates and concrete plans: whether your team can take a project, how big it is, how many people you'd need (p. 93). You don't own the agile day-to-day; you own the accomplishments measured in months, not weeks (p. 93).

| Rule of thumb | Detail (pp. 93–95) |
|---|---|
| **None of this replaces agile** | Agile planning smooths the day-to-day; the manager plans the larger picture |
| **10 productive engineering weeks per engineer per quarter** | Of about 13 weeks, vacations, meetings, review season, outages and onboarding take the rest. Q1 tends to be most productive, Q4 least |
| **Budget 20% for sustaining engineering** | Testing, debugging, legacy cleanup, version migrations. It chips away at mid-size legacy code each quarter or absorbs delays; scheduling features to 100% slows features down |
| **Near deadlines, it's your job to say no** | The only way to hit a date is to cut scope: say no to engineers who want prerequisite work (hack now, or the right implementation?) and to product on must-haves, giving options and their costs |
| **Double quick estimates; plan longer ones** | Off-the-cuff: guess and double it. For more than a couple of weeks, double it *and* say you need planning time — long tasks can take far more than twice the guess |
| **Be selective about what you bring to the team to estimate** | You absorb uncertainty. Don't be a telephone relaying every request — nor a black hole; set up a team process for new features and complaints |

> **Try it:** [Quarter capacity planner](../widgets/05-quarter-planner.html) — size a team, pick a quarter, set the sustaining share, and see which projects fit once estimates are doubled and the 10-week rule applies.

> **Ask the CTO: Joining a Small Team** (pp. 95–96). As a new manager of five engineers with new code: get walked through the architecture, testing and release; do the developer onboarding; read code reviews; ship at least a couple of features in your first 60 days — pair, get reviewed, do a release, take a support rotation. Management onboarding goes slower, but you gain understanding and technical credibility.

### Assessing Your Own Experience

Questions for reflection (pp. 96–97): what did you stop doing to make time for the new job? How well do you know the team's day-to-day pain? When did you last write a feature or pair? Who causes most of the negativity, and what's your plan? How does the team make decisions, and which do you own? When did you last review a finished project against its goals, or cut scope — and how did you choose?

## Trade-offs at a glance

| Choice | Buys | Costs |
|---|---|---|
| Manager keeps coding small things | Feels bottlenecks; credibility | Time; must not block the team |
| Manager stops coding early | Time for management | Technical obsolescence; capped career |
| Weekly releases | Fewer release events | Hidden pain, contention, broken last-minute changes |
| Daily releases | Small batches; less contention | Needs automation and tooling investment |
| Full shield | Focus | No context for decisions; rumours |
| Voting on decisions | Looks democratic | Unequal knowledge and stakes; cruelty; avoided accountability |
| Depersonalized decision process | Fair, predictable decisions | Setup effort; a named owner must decide |
| Features at 100% of schedule | Looks productive | Features slow down; no buffer |
| 20% sustaining work | Systems stay easy to change; slack | Fewer features this quarter |

## Beyond the book

- **Psychological safety** is Amy Edmondson's term (*Administrative Science Quarterly*, 1999); Google's Project Aristotle study of its own teams (2015) found it the most important factor in team effectiveness.
- **Small batches.** The book's release story matches a central finding of the DORA research (Forsgren, Humble and Kim, *Accelerate*, 2018): frequent deploys of small changes go with lower change failure rates. The [lab](../lab/05-release-cadence/README.md) is a toy model of why batch size matters, with invented failure rates.
- **RACI.** "Who should be consulted and who needs to be informed" (p. 87) echoes the RACI matrix — Responsible, Accountable, Consulted, Informed — used to assign decision ownership.

## Connections

- **Run it:** [Release cadence and contention](../lab/05-release-cadence/README.md) — the same changes shipped weekly and daily: batch sizes, blocked releases and waiting time.
- **Related chapters:** [3. Tech Lead](03-tech-lead.md) (project management basics), [4. Managing People](04-managing-people.md) (feedback, firing), [6. Managing Multiple Teams](06-managing-multiple-teams.md) (staying technical when you can't code; release frequency as a health measure), [9. Bootstrapping Culture](09-bootstrapping-culture.md) (depersonalizing decisions through process).

## Check yourself

*Questions and answers are the vault's, written from the notes above; answers cite the book's printed pages.*

1. **Why should an engineering lead still write small features and bug fixes?**

   *Answer:* To feel the bottlenecks — slow builds, painful deploys, bad on-call — and spot technical debt, and to judge what the systems can do when product proposes something (p. 78).

2. **How did moving from weekly to daily releases improve morale on the author's team?**
   - [ ] It cut the number of tests
   - [x] Releases were a scarce resource people contended for; making them plentiful removed the conflict
   - [ ] It let the team skip code review

   *Answer:* pp. 79–80.

3. **What is wrong with being a total shield?**

   *Answer:* People need context for their goals to make good decisions; denying outside events breeds gossip; and shielding can slide into parenting adults (pp. 83–84).

4. **Why was Jason's team vote on Charles's project a mistake?**

   *Answer:* Voting assumes equal stakes and knowledge and can be cruel; he used it to avoid delivering bad news himself, and Charles had never been told (pp. 86–87).

5. **When is public criticism appropriate with a brilliant jerk?**

   *Answer:* When the behaviour visibly harms the team and you don't want the culture to mimic it — delivered neutrally and in the moment; behaviour that only undermines you personally belongs in private (p. 91).

6. **How many productive weeks per engineer should you plan for in a quarter, and how much sustaining work?**
   - [ ] 13 weeks, 0%
   - [x] About 10 weeks, with 20% for sustaining engineering
   - [ ] 8 weeks, 50%

   *Answer:* p. 94.

7. **What is the doubling rule, and when isn't it enough?**

   *Answer:* For off-the-cuff estimates, take your guess and double it; for projects longer than a couple of weeks, double it but insist on planning time, because long tasks can take far more than twice the guess (p. 95).
