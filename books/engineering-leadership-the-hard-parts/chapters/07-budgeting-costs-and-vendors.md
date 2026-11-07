---
book: engineering-leadership-the-hard-parts
chapter: 7
title: "Budgeting, Costs, and Vendors"
pages: "123–145"
---

# 7. Budgeting, Costs, and Vendors

[← 6. Shipping Products and Code](06-shipping-products-and-code-in-chaotic-environments.md) · [Book](../README.md) · [8. Technical Principles and Strategy →](08-technical-principles-and-strategy.md)

## Summary

Engineering leaders tend to see budgets as "business problems," but solving them is how you get people and resources — and in chaos a budget is an anchor that ties into planning and prioritization. The chapter (explicitly a layperson's guide, not financial or legal advice) covers why budgeting matters, including unit economics such as COGS, CAC, LTV and gross margin; fixed, variable and step costs; how to build and track a budget, with a detailed look at the fully loaded cost of headcount, ramp-up and attrition; vendor management and the build-versus-buy decision; treating contractors as part of the team; and ethics (pp. 123–145).

## Key takeaways

- **Budgeting is prioritization with dollar signs attached** — the impact-versus-effort thinking from Chapter 6 scales up to it (p. 127).
- **Your spending must match your stated priorities;** if it doesn't, change the strategy or the spending (p. 124).
- **Unit economics turn technical decisions into business decisions:** $50,000 a month of AWS for 1,000 customers is $50 of COGS each; gross margin = (revenue − COGS) ÷ revenue (pp. 125–126).
- **Know how costs behave:** fixed, variable, and step costs that jump at thresholds; and who pays (pp. 130–131).
- **A person costs 1.3–1.8× base salary fully loaded;** new hires reduce team capacity at first; budget for 10–15% attrition and failed hires (pp. 133–136).
- **Prepare best, expected and worst-case budgets;** review big costs monthly, explain variances, and share overruns (pp. 137–138).
- **Build only your core business;** buy commodity services; never outsource your core hiring process; treat contractors as teammates (pp. 139–142).
- **Ethics:** fair pay and decent treatment — would you be proud to see this decision on tomorrow's front page? (pp. 142–144)

## Section outline

*From the book’s own table of contents (PDF bookmarks); printed page numbers.*

- Why Budgeting Matters — p. 124
  - Strategic Alignment — p. 124
  - Cost Management — p. 124
  - Risk Mitigation — p. 127
  - Performance Monitoring — p. 127
  - Resource Optimization — p. 127
  - Stakeholder Management — p. 128
  - Innovation and Growth — p. 129
  - Organizational Learning — p. 129
  - Competitive Advantage — p. 129
- Understanding Cost Management — p. 129
  - Fixed Costs: The Foundation — p. 130
  - Variable Costs: The Flex Players — p. 130
  - Step Costs: The Level-Up Costs — p. 130
  - Who Pays? — p. 131
  - The Human Side of Cost Management — p. 131
- Creating and Managing a Budget — p. 131
  - Starting with History — p. 132
  - Categorizing Expenses — p. 132
  - Headcount Planning and Costs — p. 133
  - Setting Goals That Make Sense — p. 136
  - Creating Your Budget Template — p. 137
  - Tracking and Managing — p. 138
  - Learning from Experience — p. 138
- Vendor Management — p. 139
  - The Great Build-Versus-Buy Debate — p. 139
  - Picking Your Partners — p. 140
  - Managing the Relationship — p. 140
  - Outsourced People and Teams — p. 141
- Ethics — p. 142
  - Taking Care of Our People — p. 143
  - Being a Good Neighbor — p. 143
  - The Global Perspective — p. 143
  - Looking to the Future — p. 144
  - Making It Real — p. 144
- Conclusion: Budget as Strategy — p. 144

## Notes

Budgeting is a strategic process that bridges where you are and where you want to be, not just number crunching (though there will be spreadsheets). The authors stress they are not accountants: work on budgets with your CFO or finance team (p. 123).

### Why Budgeting Matters

The budget is the bridge between "Wouldn't it be cool if we…" and "We actually did it!" (p. 124)

| Reason | What it means (pp. 124–129) |
|---|---|
| **Strategic alignment** | Spending matches stated priorities — customer experience can't be top priority if everything goes to internal tools |
| **Cost management** | Understanding the relationship between spending and value, not just the cheapest option |
| **Risk mitigation** | Provisions for financial (largest customer leaves), operational (database fails) and strategic (product made obsolete) risks |
| **Performance monitoring** | Leading and lagging indicators, not vanity metrics |
| **Resource optimization** | "Budgeting is simply prioritization with dollar signs attached" — your budget is the company-level backlog |
| **Stakeholder management** | The budget communicates priorities to investors, employees and customers |
| **Innovation and growth** | Fund both incremental improvement and transformative bets — tomatoes this summer and trees for later |
| **Organizational learning** | Each cycle is an experiment |
| **Competitive advantage** | Respond quickly; invest at the right time. Start simple — you can add budgeting process but rarely remove it |

> **In Practice: April's Story** (p. 124). StudioOps claims collaboration and mentorship as priorities, yet its Q1 budget has $15,000 for individual IDE licences, $5,000 for unused productivity tracking, nothing for pair-programming tools, and $500 of "quarterly pizza" for team building. April cuts the tracking tools, buys a team pair-programming licence ($8,000), starts weekly team lunches ($600 a month) and sets aside $10,000 for a code review tool.

#### Understanding the income side

Engineering leaders rarely own revenue, but **unit economics** turn you from a cost centre into a strategic partner (p. 125):

| Concept | Definition and example (p. 125) |
|---|---|
| **Cost of goods sold (COGS)** | Direct costs of delivering the service: infrastructure, third-party fees, support. $50,000 a month in AWS for 1,000 customers = $50 per customer |
| **Customer acquisition cost (CAC)** | Cost to land a customer; missing features that force a $5,000 sales effort per enterprise customer have a dollar impact |
| **Lifetime value (LTV)** | Total revenue over the relationship; at $1,000 a month, churning after 10 months instead of 12 loses $2,000 of LTV |
| **Gross margin** | (Revenue − COGS) ÷ revenue — what's left for salaries, offices and the coffee machine. At 70% aiming for 80%, optimizing a query that eats 20% of infrastructure may beat a new feature |

> **In Practice: April's Story** (p. 126). Sales discounts because competitors ship faster; churn spikes after outages. Slow bug fixing is costing PixelCurl $30,000 a month in churned revenue — now an input to April's budget and headcount.

With unit economics, priorities become comparable: Feature A cuts infrastructure by $10,000 a month (+2% gross margin); Feature B enables enterprise pricing (LTV from $10,000 to $25,000). A DevOps hire can be framed as cutting infrastructure COGS by 25%, raising gross margin from 72% to 76% — "$2 million to our valuation at standard SaaS multiples." Cost management is understanding how costs behave; sometimes spending more saves money, like Terry Pratchett's Sam Vimes "Boots" theory (p. 126).

> **Try it:** [Unit economics](../widgets/07-unit-economics.html) — set infrastructure spend, customers, price and churn, starting from the book's examples, and watch COGS per customer, gross margin and LTV move.

#### Resource optimization in practice

Estimation uncertainty scales up: as with ±25% sprint estimates, budget a three-month contractor for four months, and ask what happens if a $50,000 upgrade costs $65,000 (p. 128). Treat deferred upgrades like technical debt — what's the interest rate? (p. 128)

> **In Practice: April's Story** (p. 128). If the team underestimates by 30%, headcount planning is off by the same margin, so April runs budget planning as extended sprint planning, with dollar amounts on both impact-versus-effort axes.

### Understanding Cost Management

Costs tell half the story; they matter in relation to the value created (pp. 129–130).

| Cost type | Examples and management (pp. 130–131) |
|---|---|
| **Fixed costs** — the foundation | Office, permanent salaries, insurance, core infrastructure. Too many make you rigid; too few, unable to grow |
| **Variable costs** — the flex players | Usage-based cloud and SaaS. Balance efficiency against effectiveness |
| **Step costs** — the level-up costs | Jump at thresholds: a higher SaaS tier, a new office, expanded infrastructure — be ready before you jump |
| **Who pays?** | Direct costs (people) are easy to allocate; indirect, shared costs (a customer's share of infrastructure) need working out — you must show investments were worthwhile |

**The human side:** build a culture where senior engineers consider the cost of an architecture choice — a new tool or step cost — as part of capacity planning (p. 131).

### Creating and Managing a Budget

Even with a finance team, you spend the budget and are responsible for it (p. 131).

- **Start with history** — at least three years if possible: seasons (ecommerce costs around Black Friday), customer dependencies, expense trends, one-off incidents, and the *why* behind the numbers (p. 132).
- **Categorize expenses** — people first (base, variable pay, benefits, training, travel, entertainment), then infrastructure (cloud, space, equipment) and services (SaaS from CRM to observability, recruiting tools, lawyers, accountants, security) (p. 132).

#### Headcount Planning and Costs

The **fully loaded cost** of an employee is typically **1.3–1.8× base salary** (pp. 133–134):

| Component | Typical size (p. 133) |
|---|---|
| Payroll taxes and mandates | Roughly 7.65% in the US |
| Benefits | 20–30% of base |
| Equipment and licences | $5,000–$10,000 a year for engineers |
| Training and development | $2,000–$5,000 a year |
| Recruiting | Agency fees of 15–25% of base, or recruiter time |
| Onboarding inefficiency | New hires at about 50% productivity for three months |

> **In Practice: April's Story** (p. 134). April budgets three engineers at $150,000 each — $450,000 — but the real cost is closer to $675,000, before counting senior engineers' mentoring time.

- **Growth and attrition.** Engineering attrition runs 10–15% a year, so a 20-person team replaces two or three people annually. Each new hire reduces team capacity by 10% in their first month and 5% in their second, becoming additive in the third (p. 134).
- **Timing.** Q4 hiring is harder; batch hiring creates an onboarding bottleneck but saves recruiter time; hire in Q1 for someone productive in Q3; don't miss the annual headcount window (p. 134).
- **Scenarios.** April budgets best, expected and worst cases (hard-to-find DevOps talent needing contractor cover), including mentor time and the knowledge-transfer dip (p. 135).

| *Table 7-1. Estimated salary ranges* (p. 135) | Cost estimate | Considerations |
|---|---|---|
| **Senior** | $180,000–$300,000+ | Technical leadership, architecture, mentorship |
| **Mid** | $120,000–$180,000 | Core execution, growing autonomy |
| **Junior** | $80,000–$120,000 | High potential, need investment, future pipeline |

Startups may skew senior for speed; established companies invest in juniors. April's senior-heavy team lacks the middle layer that helps juniors grow (p. 135). **Hidden costs:** a bad hire can cost two to three times their salary, so budget 10–15% extra; key roles take three to six months; counteroffers may need 10–20% above budget; keep a fund for retention (pp. 135–136).

**The headcount business case** frames a hire as an investment: revenue enabled ("drives $X in revenue"), opportunity cost ("delaying pushes the launch by X months"), cost avoidance ("without it we'll spend $X on contractors and outages"), and team health ("current overtime rates are unsustainable") (p. 136).

> **Run it:** the [headcount plan](../lab/07-headcount-plan/README.md) experiment applies the book's fully loaded cost, ramp-up and attrition rules to hiring three engineers in a batch or staggered.

#### Goals, Template, Tracking and Learning

- **Goals need budgets and metrics**, absolute ("reach $10 million in revenue") or relative ("grow faster than the market") (p. 136).
- **The template** shows costs (and income, if relevant) month by month; prepare best, expected and worst-case variants (pp. 137–138).

![Spreadsheet laid out month by month with income at the top, then expense sections for people, infrastructure, services and office, each with subtotals and a yearly total column](../figures/07-01.png)

*Figure 7-1 (p. 137): note the structure — a projected balance at the top, people as the largest block of expenses, and monthly columns with yearly totals on the right.*

- **Tracking:** review significant costs (headcount, cloud) monthly, with cloud budget alerts; strategic reviews quarterly; a new budget annually (p. 138). Explain variances — price, volume, timing, efficiency — and **share overruns**; hiding them never works. Give each audience the right level of detail (p. 138).
- **Learning:** after each cycle ask what worked, what failed, what surprised you and what you learned (pp. 138–139).

### Vendor Management

Vendors are now strategic partners who can propel you or hold you back (p. 139).

- **Build versus buy.** **Build your core business** — what gives a competitive edge — and buy the rest; custom solutions bring years of maintenance. Your own database (unless you're a database company), scheduler or authentication and encryption are "an indulgence, not a requirement" (pp. 139–140).

> **In Practice: April's Story** (p. 139). A homegrown CI/CD system built years ago consumes 20% of two senior engineers' time. Deployment isn't PixelCurl's advantage — its animation rendering engine is — so April migrates to a commercial platform and frees the seniors to mentor.

- **Picking partners** is like hiring: capability, track record, stability, cultural fit, must-haves versus nice-to-haves, longevity and cost. Good contracts define what you get, how success is measured, and what happens when things go wrong (p. 140).
- **Managing the relationship:** regular check-ins and reviews — a partnership, not a transaction (p. 140). April's quarterly vendor reviews find three engineers separately paying for similar code-analysis tools (p. 141).
- **Outsourced people and teams.** Partners may optimize skills and compliance over culture and growth. **Never outsource your core hiring process** — let partners find people, then use your own interviews: trust, but verify. Treat external engineers as part of the team — 1-1s, standups, architecture discussions, overlapping meeting times (James held morning US Eastern meetings to overlap with Ukraine) — and weigh legal, regulatory and data-privacy issues; you get what you pay for (pp. 141–142).

> **In Practice: April's Story** (p. 141). April's interim DevOps contractor joins standups and architecture discussions and pairs with juniors — and spots a critical infrastructure issue the siloed seniors had missed.

### Ethics

Do the right thing because it's right — or at least to avoid damaging your brand (pp. 142–143).

| Area | What it asks (pp. 143–144) |
|---|---|
| **Taking care of our people** | Fair pay, development, safe conditions. April finds juniors paid 30% below market for "learning on the job" and budgets market-rate adjustments plus mentorship time |
| **Being a good neighbor** | Environmental and community impact |
| **The global perspective** | Respect local customs while keeping consistent ethical and labour standards |
| **Looking to the future** | AI and automation, intellectual property, privacy, sustainability |
| **Making it real** | Training and safety to speak up — James saw Microsoft's scenario-based program. Ask: would we be proud to see this decision on tomorrow's front page? |

### Conclusion: Budget as Strategy

Budgeting, costs and vendors may not be why you became a leader, but bringing engineering rigour to them creates the conditions to deliver the technical vision — and the skills matter for senior ICs too (pp. 144–145).

## Trade-offs at a glance

| Choice | Buys | Costs |
|---|---|---|
| More fixed costs | Stable foundation | Rigidity |
| Variable, usage-based services | Flexibility; scale with demand | Costs grow with use; less predictable |
| Crossing a step cost | Next level of capacity | A jump in spending before value arrives |
| Batch hiring | Recruiter efficiency | Onboarding bottleneck; bigger productivity dip |
| Senior-heavy team | Speed and autonomy | Cost; weak junior pipeline without a middle layer |
| Building in-house | Control; fits exactly | Years of maintenance; distraction from the core |
| Buying commodity services | Focus on core business | Vendor dependency |
| Treating contractors as teammates | Shared knowledge, culture | More management time |

## Beyond the book

- **SaaS valuation multiples** vary widely with growth rates and market conditions; the book's "$2 million at standard SaaS multiples" (p. 126) is an illustration, not a rule.
- **The Rule of 40** — growth rate plus profit margin of at least 40% — is a common SaaS health heuristic that finance teams may use alongside gross margin.
- **Fully loaded cost** ratios depend heavily on country: the book's payroll-tax figure is for the US (p. 133). The [lab](../lab/07-headcount-plan/README.md) uses the book's rules of thumb with invented salaries.

## Connections

- **Run it:** [Headcount plan](../lab/07-headcount-plan/README.md) — fully loaded cost and first-year capacity of three hires, batch versus staggered, with the book's ramp-up and attrition rules.
- **Related chapters:** [6. Shipping Products and Code](06-shipping-products-and-code-in-chaotic-environments.md) (impact versus effort; estimates), [4. Building Cohesive Teams](04-building-cohesive-teams.md) (growing when ready), [8. Technical Principles and Strategy](08-technical-principles-and-strategy.md) (choose boring technology), [10. Metrics That Matter](10-metrics-that-matter-for-engineering-teams.md) (leading and lagging indicators).

## Check yourself

*Questions and answers are the vault's, written from the notes above; answers cite the book's printed pages.*

1. **How does the book summarize resource optimization?**

   *Answer:* "Budgeting is simply prioritization with dollar signs attached" — your budget is your company-level backlog (p. 127).

2. **$50,000 a month in AWS serves 1,000 customers. What is the infrastructure COGS per customer?**
   - [ ] $5
   - [x] $50
   - [ ] $500

   *Answer:* p. 125.

3. **What is a step cost?**

   *Answer:* A cost that jumps at a threshold rather than growing linearly — a higher SaaS tier, a new office, expanded infrastructure (p. 130).

4. **Why did April's $450,000 for three engineers become about $675,000?**

   *Answer:* The fully loaded cost — taxes, benefits, equipment, training, recruiting, onboarding — runs 1.3–1.8× base salary (pp. 133–134).

5. **What happens to team capacity when a new person joins, by the book's rule of thumb?**

   *Answer:* It drops by 10% in the first month and 5% in the second, and the hire becomes additive in the third month (p. 134).

6. **What should you build in-house?**
   - [ ] Your own authentication and encryption
   - [x] What gives your business a competitive advantage — its core
   - [ ] Your own database, to save licence fees

   *Answer:* Buy commodity services; building them is "an indulgence" (pp. 139–140).

7. **Why never outsource your core hiring process?**

   *Answer:* Partners may optimize for skills and compliance rather than culture and growth; let them source people but run them through your own interviews — trust, but verify (pp. 141–142).
