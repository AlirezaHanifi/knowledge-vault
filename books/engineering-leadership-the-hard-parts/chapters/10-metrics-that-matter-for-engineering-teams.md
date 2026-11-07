---
book: engineering-leadership-the-hard-parts
chapter: 10
title: "Metrics That Matter for Engineering Teams"
pages: "207–226"
---

# 10. Metrics That Matter for Engineering Teams

[← 9. Collaborative Technical Practices](09-collaborative-technical-practices-and-decision-making.md) · [Book](../README.md) · [11. Fitting It All Together →](11-fitting-it-all-together.md)

## Summary

"How's the engineering team doing?" is hard to answer, and dashboards of squiggly lines rarely help. The chapter argues for a small set of metrics that spot problems early and show whether improvements work, while avoiding vanity metrics and surveillance. It treats metrics as a product: know your customers, dig past what they want to what they need, and break big questions into measurable criteria. Start with the four DORA metrics plus one or two for your biggest pain point, and use data you already have. Velocity is a capacity-planning tool, never a performance measure. Measure teams rather than individuals, beware Goodhart's Law and invisible work, keep metrics visible, version and retire them, and apply the same approach to AI (pp. 207–225).

## Key takeaways

- **Good metrics do two things:** spot problems while they're small, and tell you whether improvements work; badly used ones are worse than none (p. 208).
- **Treat metrics as a product** with three customer groups: engineers, engineering managers and leaders outside engineering (pp. 208–209).
- **Find the question behind the question** — "which team is most productive?" usually means "Are we okay?" (pp. 209–211).
- **Start with DORA,** add one or two context metrics — five or six in total — after four to six weeks of baseline (pp. 212–213).
- **Velocity is for capacity planning,** within the team; never a performance metric or cross-team comparison (pp. 215–216).
- **Measure teams, not individuals;** individual problems show up in qualitative signals first (pp. 217–218).
- **"When a measure becomes a target, it ceases to be a good measure"** — balance volume metrics with outcome and quality metrics (p. 219).
- **Metrics need maintenance:** a changelog, versions, an owner, feedback, and retirement (pp. 221–223).

## Section outline

*From the book’s own table of contents (PDF bookmarks); printed page numbers.*

- Why Measure Anything at All? — p. 207
- Metrics as a Product — p. 208
  - Design Intentionally — p. 209
  - The Trap of Want Versus Need — p. 209
  - Constructing Questions — p. 211
  - Choosing the Right Metrics for Your Context — p. 212
  - Take Stock of What You Already Measure — p. 214
- Velocity: The Most Misused Metric in Software — p. 215
  - Why Velocity Goes Wrong — p. 215
  - How to Use Velocity Correctly — p. 216
- Build Your Metrics with Your Customers in Mind — p. 216
  - The Human Side of Metrics — p. 217
  - Balancing Quantitative and Qualitative Data — p. 218
  - Humans and Metrics — p. 219
  - Make Metrics Visible and Accessible — p. 221
- Metrics Need Ongoing Maintenance, Just Like Code — p. 221
- AI Doesn’t Change Your Approach to Metrics — p. 223
- Conclusion: Measurement as Illumination — p. 224

## Notes

The aim is metrics that help you understand what's happening, find problems before they escalate, and decide where to focus — not vanity metrics, and not "an overeager hall monitor" (p. 207).

### Why Measure Anything at All?

Improving without measuring is "based on vibes rather than reality." Good metrics identify problems before they become disasters and show whether improvement efforts — that fancy CI/CD pipeline — actually work. Poor ones create perverse incentives and demoralize teams (pp. 207–208).

> **In Practice: April's Story** (p. 208). Marcus says the team is "crushing it" (10,000 requests per second), Sarah says it's struggling (slow delivery), Derek says all is fine (no database outages). April's first metric — feature cycle time from ticket to production — shows an average of 47 days, with features bouncing between siloed engineers.

### Metrics as a Product

The classic observability trap is spending 90% of the effort on infrastructure and 10% on analysis; data isn't insight. Like a product, metrics have customers, needn't be perfect at launch, and improve over time (p. 208).

#### Design Intentionally

Ask questions that one or more metrics answer, tied to real business needs, and ask your customers what they need (p. 209):

| Customer | Typical need (p. 209) |
|---|---|
| Engineers | 95% of the time, how they work and the friction in it |
| Engineering managers | Bottlenecks and improvements |
| Leaders outside engineering | Strategic concerns — costs, returns, velocity |

#### The Trap of Want Versus Need

Stakeholders ask for what sounds impressive. A CEO read GitHub and called two engineers far more productive because they committed thousands of lines — they were frontend engineers committing npm packages, JavaScript and CSS (pp. 209–210).

> **In Practice: April's Story** (p. 210). The VP of product calls Marcus the "MVP" for his solid-green contribution graph. Marcus commits 50 times a day (formatting, console.log, WIP); Derek once a week with tested features. April asks: "What decision would you make differently if you knew who committed more often?" — none — and moves to deployment frequency and change failure rate.

Questions like "Which team is most productive?" or "How many hours do engineers work?" aren't bad — they're attempts to quantify an unfamiliar domain. Don't demean the asker; find the underlying question by asking what decision the answer would change. It often boils down to "Are we okay?" — will we meet objectives, are we getting value for money, is quality sufficient, are we executing? (pp. 210–211)

> **Try it:** [Metrics picker](../widgets/10-metrics-picker.html) — translate stakeholder questions into the questions behind them, and build a five-or-six-metric set from DORA plus the context metrics for your biggest pain point.

#### Constructing Questions

Group research into themes and break big questions down by granularity — for "Is our engineering velocity acceptable?" leadership asks how fast we ship; engineering leaders ask about story points, estimate accuracy and deploy counts; engineers ask about cycle time and CI duration. Every answer needs a metric and a measurable success criterion (p. 211).

| *Table 10-1* (p. 212) | Example |
|---|---|
| High level | Our engineering velocity is acceptable and meets our business goals |
| Question | How long do CI or CI/CD runs take to build, test and deploy code? |
| Success criteria | CI test runs under 15 minutes; CI/CD runs under 30 minutes to run and deploy |
| Metrics | CI test run time; CI/CD deployment run time |
| Maintenance goal | 95% of both kinds of runs meet or beat the criteria |

#### Choosing the Right Metrics for Your Context

Metric overload is as counterproductive as none. Start with **DORA** — well tested, outcome-focused, buildable from existing tooling (pp. 212–213):

| DORA metric | Measures (p. 212) |
|---|---|
| Deployment frequency | How often you deploy to production |
| Lead time for changes | Commit to running in production |
| Change failure rate | Share of deployments needing immediate fixes |
| Time to restore service | How quickly you recover from incidents |

Then add one or two for your biggest pain point (p. 213):

| Pain point | Context metrics (p. 213) |
|---|---|
| Reliability | Incident volume by severity; mean time between failures |
| Delivery predictability | Feature cycle time (idea to production); sprint goal achievement rate |
| Quality | Bug escape rate; test coverage for critical paths |
| Team health | Quarterly developer satisfaction surveys; on-call load distribution |

Rollout: start small with DORA → collect four to six weeks of baseline → add context metrics → review quarterly which metrics drive decisions. Aim for balance, not maximizing one number (pp. 213–214).

#### Take Stock of What You Already Measure

Git, CI/CD, issue trackers and monitoring already hold most of the data; teams James worked with dropped an expensive metrics platform after combining Jira, GitHub and CircleCI. Some answer 80% of questions with a simple dashboard; others justify a vendor — start small either way. "The best metrics solution is the one your team will actually use" (pp. 214–215).

### Velocity: The Most Misused Metric in Software

**Velocity is a capacity planning tool, not a productivity metric** — comparing teams is like comparing a sports car's mileage with a delivery truck's (p. 215).

| Mistake | Why it fails (p. 215) |
|---|---|
| Treating it as performance | Points are arbitrary and unique to each team |
| Targets from past peaks | Teams inflate estimates or cut corners |
| Comparing teams | Different estimation, problems and composition — "apples to spaceships" |

James saw an organization "standardize" story points across teams: estimation arguments, inflated points, demoralized teams, worse quality — and the effort was abandoned (p. 215).

> **In Practice: April's Story** (p. 216). A previous manager's individual points leaderboard: Marcus split tasks into five one-point stories, Sarah inflated estimates, Derek stopped caring, juniors avoided anything over three points. April removed it, tracked team velocity privately with a three-sprint rolling average, and told the VP that asking who completed most points is like asking which musician played the most notes.

**Use it correctly:** for capacity planning, watching for dramatic changes, and within the team. A team James worked with saw a 40% drop over two sprints, found technical debt in a critical component, and — because the metric wasn't judging them — safely made the case for a debt sprint (p. 216).

> **Run it:** the [velocity target](../lab/10-velocity-target/README.md) experiment simulates a team planning with velocity versus one told to hit a higher points target, and counts what the extra points really buy.

### Build Your Metrics with Your Customers in Mind

Dashboards aren't the only format: reports can feed workshops and runbooks. Watch how people use them, and do more research if they struggle (pp. 216–217).

#### The Human Side of Metrics

- **Measure teams, not individuals** — individual metrics create unhealthy competition (p. 217).
- **Spot struggling people through qualitative signals:** code review patterns, collaboration, delivery patterns, knowledge sharing (p. 217).
- **Metrics as context, not judgment; support, not surveillance** — "How can I help you be more effective?" (p. 218)
- **Involve teams in choosing metrics; keep a blameless culture** (p. 218).

> **In Practice: April's Story** (p. 218). April publishes review time by reviewer; Derek is three times slower, so he starts rubber-stamping — and bug escapes triple in two weeks. His slow reviews had caught 89% of production bugs before shipping. She switches to team-level review time paired with bug escape rate, and pairs Derek with juniors.

#### Balancing Quantitative and Qualitative Data

The why behind a number may not be technical. Ask about morale in retrospectives; ask customers through NPS or a one-click happy/neutral/sad survey. The richest insight combines trends with explanations (pp. 218–219).

#### Humans and Metrics

People change behaviour in response to measurement (p. 219):

| Hazard | What happens (pp. 219–221) |
|---|---|
| **Goodhart's Law** | "When a measure becomes a target, it ceases to be a good measure" — measure outcomes as well as volumes |
| **Demand characteristics** | People guess why something is measured and subconsciously act to fit |
| **Context ignorance** | Share every metric with what it measures and what its value means, or people fill gaps with assumptions |
| **"What gets measured gets done"** | Invisible work — mentoring, documentation, careful reviews, debt, security — is crowded out; name what you don't measure, rotate focus metrics, protect time (like Google's "20% time") |

> **In Practice: April's Story** (p. 219). The board demands better velocity; points rise from 30 to 45 a sprint — by skipping documentation and "trivial" reviews and deferring debt. Two months later a routine deployment takes production down for six hours. April shows quality metrics fell as velocity rose and introduces a balanced scorecard: velocity, quality and stability must all stay within range.

#### Make Metrics Visible and Accessible

Team screens, automated reports into team channels, and reviews in meetings — part of everyday conversation (p. 221).

### Metrics Need Ongoing Maintenance, Just Like Code

- **Version and log changes:** excluding weekends from review time is a big change — minor versions for tweaks, major for breaks in comparability, or a new, well-named metric (p. 221).
- **Clear ownership:** a "product manager for your metrics" watches data quality, alignment, questions and improvements (pp. 221–222).
- **Listen and evolve:** check-ins, surveys, watching which metrics drive decisions, and removing those that don't (p. 222).
- **Keep up with change:** new data sources, deprecated tools, new ways of working such as trunk-based development (p. 222).
- **Phase out** metrics that no longer help — after checking who uses them, which reports include them, keeping historical data, and looking for better replacements (p. 223).

### AI Doesn’t Change Your Approach to Metrics

The method stays; the measurements adapt: segment AI and non-AI work, measure satisfaction, quality and outcomes, usage, collaboration, time saved — and trust in AI output (pp. 223–224).

> **In Practice: April's Story** (p. 224). After adopting GitHub Copilot, the VP expects velocity to double. Segmented data: boilerplate three times faster, complex logic barely changed; juniors 40% faster but with twice the bugs at first; seniors used it for docs, improving quality by 60%. New metrics: the share of AI code surviving review, time debugging AI suggestions, documentation completeness.

### Conclusion: Measurement as Illumination

Metrics are guides, not the destination: "instruments for understanding, not hammers for judgment." Speed, quality, cost and well-being are in constant tension; start simple and build psychological safety around measurement (pp. 224–225).

## Trade-offs at a glance

| Choice | Buys | Costs |
|---|---|---|
| Many metrics | Coverage | Overload; nobody acts on them |
| DORA plus one or two | Focus on outcomes | Blind spots — name them |
| Individual metrics | Apparent precision | Gaming, competition, worse quality |
| Team metrics plus qualitative signals | Safety; real causes | Requires managerial attention |
| Velocity as a target | Short-term points | Inflated estimates, skipped quality, fragility |
| Building on existing tools | Cheap, quick | Less polish than a platform |
| Buying a metrics platform | Analytics and visualization | Cost — prove it helps first |

## Beyond the book

- **DORA** grew out of the *State of DevOps* reports and the book *Accelerate* (Forsgren, Humble and Kim, 2018); recent DORA reports add a fifth metric for reliability and a rework rate.
- **Goodhart's Law** in the book's wording is Marilyn Strathern's 1997 paraphrase of Charles Goodhart's 1975 observation about monetary targets.
- **The SPACE framework** (Forsgren et al., 2021) — satisfaction, performance, activity, communication, efficiency — formalizes the book's mix of quantitative and qualitative measures.

## Connections

- **Run it:** [Velocity target](../lab/10-velocity-target/README.md) — a seeded simulation of planning with velocity versus targeting it, with reported points, real work and escaped bugs.
- **Related chapters:** [6. Shipping Products and Code](06-shipping-products-and-code-in-chaotic-environments.md) (estimates and process), [7. Budgeting, Costs, and Vendors](07-budgeting-costs-and-vendors.md) (cost metrics), [8. Technical Principles and Strategy](08-technical-principles-and-strategy.md) (visibility), [9. Collaborative Technical Practices](09-collaborative-technical-practices-and-decision-making.md) (psychological safety).

## Check yourself

*Questions and answers are the vault's, written from the notes above; answers cite the book's printed pages.*

1. **What two functions do good metrics serve?**

   *Answer:* They identify problems before they become disasters, and show whether improvement efforts are working (p. 208).

2. **A stakeholder asks which engineer commits the most code. What should you ask back?**

   *Answer:* What decision would the answer change — then answer the underlying question, which is often "Are we okay?" (pp. 210–211)

3. **Which is not one of the four DORA metrics?**
   - [ ] Deployment frequency
   - [ ] Change failure rate
   - [x] Story points per sprint
   - [ ] Time to restore service

   *Answer:* p. 212.

4. **What is velocity for?**

   *Answer:* Capacity planning within the team — not measuring productivity or comparing teams (p. 215).

5. **Why did bug escapes triple after April published review time by reviewer?**

   *Answer:* Derek, the slow but thorough reviewer, started rubber-stamping to improve his number; his reviews had caught 89% of production bugs (p. 218).

6. **State Goodhart's Law as the book quotes it.**

   *Answer:* "When a measure becomes a target, it ceases to be a good measure" (p. 219).

7. **How do you stop invisible work being crowded out by metrics?**

   *Answer:* Say explicitly what you don't measure and why it matters, rotate focus metrics, and protect time for unmeasured work (pp. 220–221).
