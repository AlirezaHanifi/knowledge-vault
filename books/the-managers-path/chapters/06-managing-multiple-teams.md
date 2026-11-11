---
book: the-managers-path
chapter: 6
title: "Managing Multiple Teams"
pages: "99–123"
---

# 6. Managing Multiple Teams

[← 5. Managing a Team](05-managing-a-team.md) · [Book](../README.md) · [7. Managing Managers →](07-managing-managers.md)

## Summary

Running several teams — usually as a director, with tech leads reporting to you — means you're no longer writing much production code, and your days are sliced into meetings. The chapter is about working at that altitude: staying hands-on without coding, managing your time by importance rather than urgency, surviving the "plate spinning" of the first months by delegating according to how simple and how frequent a task is, saying no in ways that keep relationships intact, and turning your technical eye to the *systems of work* — release frequency, check-in frequency, incident frequency — that show whether teams know what to do, have the tools, and have the time. It warns against building an us-versus-them clique and ends by recommending laziness and impatience applied to process, and going home (pp. 99–123).

## Key takeaways

- **A director isn't expected to code daily but stays technical** — code reviews, debugging, systems they built — and should reach fluency in one language before entering management; keep a meeting-free half-day a week (pp. 99–102).
- **Separate importance from urgency.** Email and chat feel urgent and rarely are; the strategic, important-but-not-urgent work is what you must make time for, before it becomes urgent for your boss (Table 6-1, pp. 103–106).
- **Feeling a little overwhelmed is normal; it's plate spinning.** Keep 1-1s and team meetings — they're where you see warning signs (pp. 107–108, 109–111).
- **Delegate by complexity and frequency:** simple-frequent → delegate; simple-infrequent → do it yourself; complex-infrequent → train rising leaders; complex-frequent → delegate carefully to develop the team (Table 6-2, pp. 108–109).
- **Say no well:** "yes, and"; turn repeated nos into policies; "help me say yes"; appeal to budget; work with peers; and don't prevaricate (pp. 111–113).
- **Measure team health through the work:** frequency of releases, of code check-ins, and of incidents — balancing stability against overcaution (pp. 114–118).
- **Build purpose-driven teams, not cliques**, and treat your peers as your first team; model focus and going home (pp. 118–122).

## Section outline

*From the book’s own table of contents (PDF bookmarks); printed page numbers.*

- Managing Your Time: What’s Important, Anyway? — p. 103
- Decisions and Delegation — p. 107
  - Delegate Simple and Frequent Tasks — p. 108
  - Handle Simple and Infrequent Tasks Yourself — p. 108
  - Use Complex and Infrequent Tasks as Training Opportunities for Rising Leaders — p. 108
  - Delegate Complex and Frequent Tasks to Develop Your Team — p. 109
- Challenging Situations: Strategies for Saying No — p. 111
  - “Yes, and” — p. 111
  - Create Policies — p. 111
  - “Help Me Say Yes” — p. 112
  - Appeal to Budget — p. 112
  - Work as a Team — p. 112
  - Don’t Prevaricate — p. 113
- Technical Elements Beyond Code — p. 114
- Measuring the Health of Your Development Team — p. 115
  - Frequency of Releases — p. 115
  - Frequency of Code Check-ins — p. 117
  - Frequency of Incidents — p. 117
- Good Manager, Bad Manager: Us Versus Them, Team Player — p. 118
- The Virtues of Laziness and Impatience — p. 121
- Assessing Your Own Experience — p. 123

## Notes

Managing multiple teams comes before managing managers because the two don't always coincide (p. 99). The author's **engineering director** description (pp. 99–101):

- Leads engineers across product areas or technology functions; tech leads and ICs report in.
- Not expected to code day to day, but owns the organization's technical competence (training, hiring), stays current, helps debug and triage critical systems, can review code, and acts as the technically savvy voice asking business and product questions of the design.
- Ensures smooth execution of complex deliverables; refines standards and processes; leads recruiting, headcount, career growth; manages vendors and budget as needed.
- Grows the next generation of leaders; owns retention; balances product work against technical debt and strategy.
- Sets the example for cross-functional collaboration; explains technology to the business and business to technology; represents the company to candidates; guides goal-setting for all their teams.

**Staying hands-on without much coding** (pp. 101–102). Your schedule is now firmly a manager's: without solid blocks a few days a week, any code you write is slow. Stay engaged through code reviews (as a secondary reviewer), the systems you built, debugging and production support — or pairing and minor fixes if you weren't a strong debugger. Going hands-off is riskier without fluency in at least one language first; the author took about 10 years, including degrees. And keep **a solid half-day a week free of meetings** for something creative: blog posts, talks, open source.

> **Ask the CTO: I Miss Code!** (pp. 102–103). Almost everyone questions the move. Ask whether you've internalized the idea that management isn't a real job: it is — necessary, important, and yours now. Code is full of quick wins; management has few. Nostalgia is natural, but becoming a great manager means trading away some technical focus.

### Managing Your Time: What's Important, Anyway?

Meetings pile up while your real deliverables wait: setting goals, detailing roadmaps with product, following up that tasks got finished (p. 103). The author recommends David Allen's *Getting Things Done*, but her philosophy is simpler: **understand the difference between importance and urgency** (p. 103).

| *Table 6-1. Prioritizing your time* (p. 104) | Not urgent | Urgent |
|---|---|---|
| **Important** | Strategic: make time | Obvious work |
| **Unimportant** | Obvious avoid | Tempting distractions |

- **Important and urgent** — the outage, reviews due tomorrow, an offer before a competing one expires — you'll do anyway (p. 104).
- **Urgency is felt more clearly than importance.** Email's red dot feels urgent but email is the worst channel for urgent information; chat is almost as bad for a colocated team, and moving communication to chat doesn't eliminate it. We also mistake *obvious* for urgent: a calendar meeting tells you where to be, not whether it matters (p. 104).
- **Important but not urgent** — preparing for meetings so they run well, writing job descriptions and hiring plans, reviewing a project for creeping problems, resolving a disagreement with another manager, thinking about the future. At this level your boss trusts you to handle these *before they become urgent for your boss* (pp. 104–106).
- **An efficient meetings culture** wins time back: agendas up front, preparation, clear procedures and outcomes for planning, retros and postmortems (p. 105).
- **Be careful skipping your teams' meetings.** They're where you see engagement: half the room asleep or on laptops means the meeting wastes their time, and a drained team signals trouble (p. 105).

> **The Hardest, Shortest Lesson of Becoming a Manager** (Cate Huston, p. 106). If the team needs a manager more than an engineer — to hire, coach, get what product hasn't delivered, fix process — then you can't be that engineer. If you're going to be bad at one, being a bad manager is a choice inflicted on other people; being as good a manager as you know how has to be enough.

> **Try it:** [Delegate or do it yourself?](../widgets/06-delegation-matrix.html) — sort the book's own example tasks into Table 6-1's urgency/importance quadrants and Table 6-2's complexity/frequency quadrants, and see what each placement tells you to do.

### Decisions and Delegation

The first months of managing multiple teams can feel like a death march even without long hours: the author lost her voice repeatedly; a friend made director had an assistant order her lunch because she forgot to eat (p. 107). The only way out is through — and if you *don't* feel a bit overwhelmed, you're probably missing something (p. 107).

It's **plate spinning**: the plates are people and projects, and the job is knowing how much attention each needs when. You'll drop some; your instincts for early warning signs — failing projects, people about to quit, underperforming teams — will improve. Keep regular 1-1s with every direct report (shorter or biweekly if needed): skipping them is how you miss a resignation coming (pp. 107–108).

**Delegation** is how you claw out of having too many plates: for every task, ask whether you need to be the one doing it (p. 108).

| *Table 6-2. Deciding when to delegate or do it yourself* (p. 108) | Frequent | Infrequent |
|---|---|---|
| **Simple** | Delegate | Do it yourself |
| **Complex** | Delegate (carefully) | Delegate for training purposes |

| Quadrant | Examples and approach (pp. 108–109) |
|---|---|
| **Simple and frequent → delegate** | Running standups, the weekly progress summary, minor code reviews; tech leads and senior engineers need no training |
| **Simple and infrequent → do it yourself** | If explaining takes longer than doing it: booking the occasional conference ticket, running the quarterly report script — even if it feels beneath you |
| **Complex and infrequent → train rising leaders** | Performance reviews and hiring plans are yours, but have a tech lead help with an intern's review, or a senior engineer estimate next year's headcount |
| **Complex and frequent → delegate to develop the team** | Project planning, systems design, being the key person in an outage: the biggest opportunity to grow talent. List the tasks only you know how to do — project management, onboarding, breaking product goals into deliverables, production support — and teach them |

If your teams can't operate without you, you'll find it hard to be promoted (p. 109).

> **Ask the CTO: Warning Signs** (pp. 109–111). Signals worth noticing:
>
> - A usually chatty, engaged person starts arriving late, leaving early, going quiet — a personal issue or about to quit, perhaps after a promotion or reorg where they felt overlooked.
> - A tech lead says all is well but skips 1-1s and gives thin status — often hiding slow progress or out-of-scope work; help them write a clear plan.
> - Meetings with no energy, where the PM and tech lead do all the talking — the team isn't engaged or doesn't feel it has a say.
> - A project list that changes weekly with customers' whims — no goals beyond pleasing customers.
> - A small team fragmented around "their" systems and incurious about others — identified with systems rather than the company.

### Challenging Situations: Strategies for Saying No

A manager enables, coaches and champions — and to do it must say no to the team, to peers and to the boss (p. 111).

| Strategy | How it works (pp. 111–113) |
|---|---|
| **"Yes, and"** | From improv: "Yes, we can do that project, and all we need is to delay this other one." Positivity plus the boundaries of reality turns disagreement into a negotiation about priority — hard for engineers used to listing downsides |
| **Create policies** | When you repeat the same no (a new language: who else knows it, how to run it in production, logging, testing), write the hard requirements and guidelines down, so the team knows the cost of getting to yes |
| **"Help me say yes"** | For one-offs: curious questions about the parts that seem ill-considered. People often talk themselves out of it — or surprise you |
| **Appeal to budget** | Lay out time and workload plainly. Beware "not right now": only imply "later" if later can really happen |
| **Work as a team** | Peers (product, finance) can say no together; lend your authority and call in the favour later. Good cop/bad cop is a bit dishonest — use sparingly |
| **Don't prevaricate** | If you have the authority and believe it shouldn't happen, say no quickly; apologize when wrong. Get comfortable with quick nos and yeses on low-risk decisions |

> **Ask the CTO: My Tech Lead Isn't Managing** (pp. 113–114). A tech lead was to oversee a junior engineer rewriting an app from Objective-C to Swift; there's no plan and no response to design feedback. Ask why: she may be too busy with her own code (schedule mentoring like any work), or not know how to push someone who won't commit (new tech leads often feel they lack authority). Build her skills and confidence rather than stepping in — slower, but the team learns to respect her requests.

### Technical Elements Beyond Code

Assuming this level is nontechnical is a mistake: your technical focus moves to **the systems of work your developers operate in** and the team's technical health signals (p. 114). *First, Break All the Rules* lists questions that predict productivity and satisfaction, including: do I know what's expected of me; do I have the materials and equipment to do my work right; do I have the opportunity to do what I do best every day (p. 114)? For engineers, the answers show in how often they push code: clear work, usable tools, and time free of meetings and incidents (pp. 114–115).

### Measuring the Health of Your Development Team

Design systems and processes that keep things moving; interrogate every process for its value and ask whether it can be automated further (p. 115).

| Signal | What it shows | What to do (pp. 115–118) |
|---|---|---|
| **Frequency of releases** | The most direct measure of shipping; a leading indicator of a healthy team. Even a database team can measure pushes to a beta or developer environment | Ask how long releases take, how often they fail or roll back, who decides code is ready. Slow releases usually reveal cracks — QA owning quality, slow rollbacks, release-caused incidents. Lead the fix even if you don't do it: automation, feature toggles, backward-compatible changes, rolling upgrades, small changes; push for time off the roadmap |
| **Frequency of code check-ins** | Whether people break work into small chunks | Teach it; engineers who don't write tests often struggle, and learning TDD helps. It's OK to expect work in progress in shared version control — you're not running a research team |
| **Frequency of incidents** | Whether quality is improving | Set the stability bar for the product (a new product may favour features; mission-critical systems, stability). Developer on-call puts the best people on problems but risks burnout; managers move to escalation support. If on-call is pure reaction, make time to fix recurring incidents — but over-prevention (weeks of manual QA, slow reviews, rare releases) leaves developers idle without reducing risk |

Is the team working to full capacity, challenged, growing, and able to spend most time on new code? If not, you're ignoring a problem at your peril: often the fix isn't cheerleading or pay but making them more productive (p. 116).

### Good Manager, Bad Manager: Us Versus Them, Team Player

| Diana — us versus them | Neil — team player |
|---|---|
| Hired to fix a neglected mobile team, she brings in her former BigCo people; they form a clique that feels superior, clash with product, and ship slowly. After a year she quits and the team follows | In a chaotic startup he fires cautiously, has long-tenured people vet new hires, works closely with product, sets and communicates clear goals. Slow start, then a stronger organization |

An identity built around job function or technology, set against other teams, is a shallow binding (p. 119):

| Clique (in-group) teams are… | Purpose-driven teams are… (pp. 120–121) |
|---|---|
| **Fragile to the loss of the leader** | **Resilient to loss of individuals**, loyal to the larger mission |
| **Resistant to outside ideas** — so their best people get bored and leave the company | **Driven to find better ways**, caring about an idea's merit, not its source |
| **Empire building** — competing for headcount and mandates | **First-team focused**: a leader's first team is their peers across the company, not their reports |
| **Inflexible** to reorgs, cancellations and shifts | **Open to changes** that serve the purpose |

Even when hired to fix a team, remember the company got this far through real strengths: understand its culture, and cultivate strengths rather than focusing on what's broken (p. 119). Durable teams take their purpose from the company's mission and values (p. 120).

### The Virtues of Laziness and Impatience

Larry Wall's "laziness, impatience, and hubris" from *Programming Perl* carry into leadership — directed at processes and decisions, never at people (p. 121). Model two things (pp. 121–122):

- **Figure out what's important.** Question anything inefficient: what's its value, can we deliver it faster, can we strip it down? But "faster" means **the same value in less total time** — a team working 60 hours to finish in one week what would take a week and a half hasn't gone faster; it has given the company its free time.
- **Go home.** Burnout harms individuals, families and teams. Your late emails tell the team overwork matters even if you don't expect replies: queue them for the morning, set chat to away, take a vacation without email. "We focus so we can go home," and going home forces focus.

### Assessing Your Own Experience

Questions for reflection (p. 123): what in your last and next two weeks isn't providing value? When did you last delegate, and was it simple or complex? Who are your rising leaders and what are you giving them? How smoothly do writing, releasing and supporting code run? When did you last cut scope — features, quality, or both? When did you last email after 8 pm, and did you need a reply?

## Trade-offs at a glance

| Choice | Buys | Costs |
|---|---|---|
| Keep coding as a director | Feeling for the work | Slow code without focus blocks; neglected management |
| Hands-on via reviews, debugging, pairing | Credibility, context | Must fit your strengths |
| Skip team meetings | Calendar time | Miss morale and dynamics signals |
| Delegate complex, frequent work | Grows leaders; teams run without you | Slower at first; outcomes differ from yours |
| Do simple, infrequent work yourself | Fast | Small tasks pile up if misjudged |
| Quick no | Speed, clarity | Sometimes wrong — apologize |
| "Not right now" | Avoids conflict | An implied promise you must keep |
| Developer on-call | Best people on problems | Burnout |
| Heavy incident prevention | Fewer defects in theory | Idle developers, rare releases, little real risk reduction |
| Clique around a leader | Fast cohesion | Fragile, insular, empire building |

## Beyond the book

- **The Eisenhower matrix.** Table 6-1 is the familiar urgent/important grid often attributed to Dwight Eisenhower and popularized by Stephen Covey's *The 7 Habits of Highly Effective People* (1989).
- **The Gallup Q12.** The three questions on p. 114 are items from Gallup's twelve-question engagement survey, the research behind *First, Break All the Rules*.
- **DORA's four keys.** Release frequency and incident frequency anticipate two of the four DORA metrics (deployment frequency, lead time for changes, change failure rate, time to restore service), introduced in *Accelerate* (2018), a year after this book.

## Connections

- **Related chapters:** [3. Tech Lead](03-tech-lead.md) (maker's and manager's schedules), [4. Managing People](04-managing-people.md) (delegation without micromanaging), [5. Managing a Team](05-managing-a-team.md) (not shipping; release cadence), [7. Managing Managers](07-managing-managers.md) (the next level of delegation), [9. Bootstrapping Culture](09-bootstrapping-culture.md) (core values behind purpose-driven teams).

## Check yourself

*Questions and answers are the vault's, written from the notes above; answers cite the book's printed pages.*

1. **In Table 6-1, which quadrant must a manager deliberately make time for?**
   - [ ] Urgent and important
   - [x] Important but not urgent — strategic work
   - [ ] Urgent but unimportant

   *Answer:* Urgent-important work happens anyway; the strategic quadrant needs time set aside, before it becomes urgent for your boss (pp. 104–105).

2. **Why does the author call email a poor channel for urgent information?**

   *Answer:* It *feels* urgent — the red dot — but rarely is, and is probably the worst vehicle for time-sensitive information; chat is almost as bad for a colocated team (p. 104).

3. **Using Table 6-2, what should you do with writing performance reviews and making hiring plans?**
   - [ ] Delegate them to tech leads
   - [ ] Do them yourself and never share them
   - [x] They're yours, but use them to train rising leaders

   *Answer:* Complex, infrequent tasks are training opportunities (pp. 108–109).

4. **Describe the "yes, and" way of saying no.**

   *Answer:* Agree to the request while stating its real cost — "yes, and we'll need to delay this other project" — turning a refusal into a negotiation about priority (p. 111).

5. **What three frequencies does the book use as team health signals, and what do they indicate together?**

   *Answer:* Frequency of releases, of code check-ins, and of incidents: a team that knows what to do, has the tools to do it, and has time to do it every day (pp. 114–115).

6. **Why is a clique built around its leader fragile?**

   *Answer:* It tends to dissolve and leave when the leader leaves; it also resists outside ideas, builds empires and resists change (p. 119).

7. **What does "faster" mean to the author?**

   *Answer:* The same value to the company in less total time — not more hours in fewer days, which only spends the team's free time (p. 122).
