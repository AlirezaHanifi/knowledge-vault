---
book: the-managers-path
chapter: 9
title: "Bootstrapping Culture"
pages: "191–216"
---

# 9. Bootstrapping Culture

[← 8. The Big Leagues](08-the-big-leagues.md) · [Book](../README.md) · [10. Conclusion →](10-conclusion.md)

## Summary

A senior engineering leader sets the culture of their function, and treating culture as infrastructure — something you tend deliberately — is the chapter's theme. Startups resist "structure" and "process"; the author reframes them as *learning* and *transparency*. Drawing on Jo Freeman's "The Tyranny of Structurelessness," she argues that unstructured teams work only under narrow conditions and otherwise run on hidden hierarchies, so structure should grow with the company's people, age, infrastructure and risk tolerance — guided by failures rather than copied successes (Gall's law). The rest is practical: defining and applying core values, writing a career ladder (after a first one that flopped), building cross-functional teams, and adding engineering processes — code review, postmortems, architecture review — as risk management that depersonalizes decisions (pp. 191–216).

## Key takeaways

- **Talk about learning and transparency, not structure and process:** we encode lessons from success and failure so the organization scales (p. 191).
- **Structurelessness hides power.** Freeman's unstructured group works only if it is task-oriented, small and homogeneous, highly communicative and low in specialization — a description of many early startups (pp. 193–194).
- **Size structure to the vessel** — race car, airliner, spaceship — by people, age, existing infrastructure and risk tolerance; let failures, not successes, show where to add or remove it (pp. 195–198).
- **Culture is the unspoken shared rules of a community**; real values ("people who value innovation, data…") include more people than credentials ("MIT graduates") and work better than friendship tests for fit (pp. 198–202).
- **A borrowed career ladder can flop.** Write it with the team, in detail, with long-form descriptions, salary bands matched to the number of levels, a breakpoint level, keystone promotions and split tracks (pp. 202–208).
- **Cross-functional teams** turned "us versus them" into "us" at Rent the Runway — Conway's law favours product communication over technical elegance; keep 20% for engineering work (pp. 208–211).
- **Process is risk management:** heavy process only for rare or hidden-risk activities; code review, blameless postmortems and architecture review depersonalize decisions (pp. 211–216).

## Section outline

*From the book’s own table of contents (PDF bookmarks); printed page numbers.*

- Assessing Your Role — p. 195
- Creating Your Culture — p. 198
- Applying Core Values — p. 200
- Creating Cultural Policy — p. 202
- Writing a Career Ladder — p. 204
- Cross-Functional Teams — p. 208
  - Structuring Cross-Functional Teams — p. 210
- Developing Engineering Processes — p. 211
- Practical Advice: Depersonalize Decision Making — p. 213
  - Code Review — p. 213
  - The Outage Postmortem — p. 214
  - Architecture Review — p. 215
- Assessing Your Own Experience — p. 216

## Notes

A common failing of first-time CTOs is underestimating the importance of being deliberate about engineering culture; attend to it like any infrastructure you rely on (p. 191). At Rent the Runway the author introduced structure to a classic "scrappy startup" team, where structure sounded "slow" and "innovation-crushing" (p. 191). Her reframing: **learning instead of structure, transparency instead of process** — we build systems to learn from successes and mistakes and share those lessons transparently, which makes organizations stable and scalable (p. 191). Approach it scientifically: have a theory and test it (p. 192).

Early startups attract people who trade high uncertainty and risk for freedom; almost everything is undecided, from frameworks to vacation policy and even company values. The key behaviour is **decisiveness**: pick a strategy and run; you need a solution that gets you to the next milestone, not a perfect one. "Deciding not to decide," such as having no titles, is popular and harmless at a few people (pp. 192–193).

**"The Tyranny of Structurelessness."** Jo Freeman's essay on early feminist collectives applies to startups: pretending to lack structure creates hidden power structures. She lists when an unstructured group can work (pp. 193–194):

| Freeman's condition | In a typical early startup (p. 194) |
|---|---|
| **Task-oriented** — the task structures the group | Engineering as the execution arm of the product or founder |
| **Relatively small and homogeneous** — a common language | "Full stack" engineers hired from the team's own networks |
| **High degree of communication** — practical only at about five people, or 10–15 as overlapping subgroups, since interactions grow geometrically | A colocated team |
| **Low skill specialization** — everything can be done by more than one person | Interchangeable generalists |

Such a team is either less self-directed than it believes or run by hidden hierarchies — often both (p. 194). The same goes for code: work done task by task by interchangeable people produces spaghetti code, and refactoring means drawing out structure. **Structure is how we scale, diversify and take on complex long-term work** — in software, teams and processes alike (pp. 194–195).

Structure can come too early — a five-person reporting chain, or meetings about which toilet paper to stock — but in small companies it more often comes **too late**: one person who decides everything and changes his mind is fine with three people and costly with 50 (p. 195). A friend's analogy: an early startup is a race car (close to the ground, quick turns, you only crash yourself), then a commercial flight, then a spaceship (slow to turn, course set long in advance, but carrying many people far) (p. 195).

### Assessing Your Role

Recognize the size of the vessel you're steering (pp. 195–196):

| Factor | Effect on structure |
|---|---|
| **People** | More people need more thoughtful structure; leaders wanting control need more of it. Modern companies structure goal setting rather than top-down decisions — which still needs structure |
| **Age** | Older companies have entrenched habits, but are more likely to survive |
| **Size of existing infrastructure** | Few business rules, little code or physical infrastructure (stores, warehouses, inventory) → less structure; more of them → more clarity needed |
| **Risk tolerance** | Regulation and what's at stake; more people depending on you means less appetite for risk even without regulators |

**Gall's law** (John Gall, *Systemantics*): a complex system that works evolved from a simple system that worked; one designed from scratch never works (p. 196).

- **Let failure guide evolution.** One person quitting for lack of a career path may not justify a ladder; several quitting or declining offers might. Examine all aspects of reality behind each failure, weigh its frequency and cost, and change structure — adding *or removing* it — at the level where the failure occurs (p. 197).
- **Success is a poor teacher.** We blame failure on bad luck and credit success to ourselves; success tempts us with "one weird trick." Know the improvement you want and the context that made it work (p. 197).
- **Learning isn't free.** Investing in structure for efficiency pays off when the company will be around; if future time is worth less than present time, you won't bother (pp. 197–198).
- **Don't cling to old structure either.** Technology changes the risks — in SaaS, shipping a bug is less risky than falling behind on features, so infrequent releases are now the risky choice (p. 198).
- **Failures from too little structure:** every new hire slowed for months by no onboarding; people leaving with no growth path; the third outage from someone dropping a critical table directly in the database (p. 198).

### Creating Your Culture

"Culture is how things get done, without people having to think about it" (Frederic Laloux, quoted p. 198). **Culture is the generally unspoken shared rules of a community** — like handshakes or how you address people of different standing. People also decide by contracts or data, but where the group's needs must override the individual's, under uncertainty, **cultural values are the glue** (p. 199).

- A healthy culture won't fall out automatically; in reality culture is formed by early employees in a race for survival, often as a post hoc justification. Not everyone fits every company (p. 199).
- **Real values can reduce discrimination.** "Engineers who graduated from MIT" is not a culture; "people who value technology innovation, hard work, intellect, scientific process, and data" might be — and admits far more people who share real principles (p. 199).
- **You're measured against the founders' values** whether you realize it or not. People who embody all of them do well naturally; others feel friction. For executives, the overlap between your values and the company's largely determines how easy the fit will be (p. 200).

### Applying Core Values

| Step | How (pp. 200–202) |
|---|---|
| **Define your culture** | Map company values onto your team and add your own: the Rent the Runway tech team explicitly valued diversity (what you can do and could do, not checkboxes) and layered a learning culture on top. Subteams will differ |
| **Reinforce it by rewarding it** | Value stories at all-hands — shoutouts for "keeping it dope." Push past shyness about praise. Use performance reviews to call out values in action, and to see who embodies them |
| **Spot values conflicts** | Someone who pushes work onto others, under "roll up your sleeves"; a constant naysayer, under "happiness and positivity is a choice" (a real Rent the Runway value the author had to learn). Coaching with values names otherwise vague friction |
| **Use values in interviews** | Ask interviewers to look for matches and collisions with specific values — not "would I like being stuck in an airport with this person?" Friendship tests correlate with schooling, race, class and gender, so are almost certainly discriminatory. Be specific: an independence-loving engineer on a team that collaborates on everything; "the most analytical argument wins" in a company that values empathy and intuition |

Write the values down and use the list to evaluate candidates, praise people and shape reviews (p. 202).

### Creating Cultural Policy

Policies (career paths, pay scales, incident management) are increasingly shared publicly, but copying a starting point isn't enough (p. 202). The author's first career ladder was prompted by failure: an HR salary review revealed **no salary structure** — pay reflected previous salaries and negotiating skill — and no clarity on what "senior" meant for hiring (pp. 202–203).

| What she did | What happened (pp. 203–204) |
|---|---|
| Borrowed a friend's ladder: eight levels, four categories (technical skills, getting stuff done, impact, communication and leadership), a sentence or two per cell | Too thin, especially at the earliest levels |
| Rolled it out his way: "it's about fairness, don't obsess over your level," plus John Allspaw's "On Being a Senior Engineer" | **A flop.** Vague details made people obsess *more* and argue for higher levels |
| — | Why: his team shared a background at one large tech company; hers came from startups, finance and big tech, with no shared habits. **What works for one company doesn't translate, even between similar ones** |

### Writing a Career Ladder

> **Try it:** [Levels and salary bands](../widgets/09-salary-bands.html) — choose few wide overlapping levels or many narrow ones, starting from the book's example bands, and see how promotion pace, overlap and pay spread change.

| Guideline | Detail (pp. 204–208) |
|---|---|
| **Solicit participation** | Senior managers and engineers flagged what they didn't understand and proposed rewrites; senior ICs wrote the IC expectations |
| **Look for examples** | More ladders from friends, the best details from bigger companies with strong technical reputations — useful for describing very senior scope |
| **Be detailed** | Inspiring but matched to your company: a director of a 50-person startup team doesn't run a division. Include what you'd look for when hiring or promoting at a level |
| **Long-form and summary** | A spreadsheet to see how attributes grow level by level, and a long form that reads like a review of someone performing well at each level |
| **Relate it to salary** | Each level has a band; few levels require wide bands to cover different performers and frequent early-career raises |
| **Many early levels, narrow bands** | Promote people every year for their first two or three years; narrow bands keep pay at a level close together and help avoid bias (paying men more than women) — but adjacent levels are hard to tell apart |
| **Few levels, wide overlapping bands** | Clearer distinctions; overlap lets strong people be paid well without promotion and lets borderline hires come in low. Example: software engineer $50–100K, senior $80–150K, so a strong engineer may out-earn a senior |
| **Consider breakpoint levels** | The lowest level where someone can stay forever without underperforming — often senior engineer. Levels can get harder beyond it; expect people to cluster there |
| **Recognize achievement** | Make some keystone promotions shared and celebrated — senior, staff, principal; director, VP — spaced apart, so there's something bigger than the next raise |
| **Split management and technical tracks** | Usually above senior engineer. Don't expect equal numbers: management is volume-driven, senior technical roles depend on technical complexity and scope |
| **People skills as a mid-career requirement** | Require management or mentorship (usually as tech lead) before promotion past the split — senior ICs still manage projects and mentor |
| **Years of experience** | Not a hard rule, but keystone levels reflect maturity: a staff engineer needs a track record of completing and supporting long-running work |
| **Evolve it** | A living document. Hers, written from an infrastructure background, needed tweaks for frontend developers |

### Cross-Functional Teams

Who you work with and report to is obvious at very small and very large companies; growing companies must answer it, probably repeatedly (p. 208). At Rent the Runway, engineering began as storefront and warehouse, then frontend and backend during a rewrite from a PHP monolith to Java and Ruby microservices (pp. 208–209). An experiment changed that: a feature showing customers' own photos in dresses, with their usual size, height, weight and "shape," built by a **cross-functional team** — frontend and backend engineers, a product manager, designers, a data analyst and a customer service representative. It shipped a good feature fairly quickly, and replaced "us versus them" between functions with "us"; product engineering then moved entirely to such teams ("pods," "squads," "pillars") (p. 209).

**Conway's law** — organizations produce designs that copy their communication structures — explains it: cross-functional teams favour the communication that drives product development. They won't produce the most efficient technology, so decide where to take those system-design hits (pp. 209–210).

**Structuring cross-functional teams** (pp. 210–211):

- **Management lines didn't change:** engineers reported to engineering managers, product managers to the head of product; the pod decided who worked on what day to day.
- **A small infrastructure organization** kept core systems and specialists (web platform, mobile, data engineering) out of product work.
- **Reserve 20% of engineering time** in pods for on-call, interviewing and sustaining engineering.
- Large companies do this too — banks attach technology teams to business units, with central infrastructure.
- **Values shift:** in technology-focused structures the leaders are the best engineers by technical measures; in product-focused ones, those with product sense, speed and cross-functional communication. Choose by what matters most, and in senior management focus on what the company values most and hire for the other.

### Developing Engineering Processes

The author recalls being upset when people broke the build by skipping tests, and resenting a central bureaucracy that imposed code review, ticketing and tracking all at once without explanation (p. 211). Process is where structure meets the road: none, and teams can't scale; the wrong one, and they slow down. Balance it against your team's size and risk tolerance (p. 211).

> **Ask the CTO: Engineering Process** (pp. 212–213). A fast-growing startup has no code reviews, half-used Trello and architecture decided by whoever's working on it; engineers want reviews for all changes, and someone has quietly written a new system in Scala in a Ruby shop. **Think of process as risk management:** a proxy for how hard or rare something should be. Complicated process — long, or needing busy people's sign-off, or a very high bar — belongs only on rare activities or ones whose risks aren't obvious. Don't make frequent, low-risk, obvious-risk activities slow (keep code review light), and look for hidden risks to draw into the open. Like a good political idea, a good process "works well in half-baked form" — valuable even when imperfectly followed, mostly by socializing change and risk.

### Practical Advice: Depersonalize Decision Making

Three processes to consider as the team grows, each with behavioural expectations as well as technical details (p. 213):

| Process | Best practices (pp. 213–216) |
|---|---|
| **Code review** | **Be clear about expectations:** tests catch bugs, reviews mostly don't — except missing docs or related changes and inadequate tests; review is largely socialization. **Use a linter for style** so formatting isn't debated (nitpicking can become bullying). **Watch the review backlog** — some companies cap outstanding requests per person |
| **The outage postmortem** (a "learning review") | **Resist blame** — it makes people afraid of mistakes. **Understand the context:** missing tests, tools that would have helped; patterns. **Be realistic about takeaways:** a laundry list gets nothing done; pick the one or two high-risk, likely ones and say what you're letting go |
| **Architecture review** (new languages, frameworks, storage, developer tooling) | Ask: how many people can use it; are there production standards; how will it roll out and be taught; what are the operational considerations? **Be specific** about what needs review — not routine feature design. **The value is in preparing** — when people can meet the requirements, the "why" is usually obvious. **Choose the board wisely:** those affected, not static gurus; nothing is more demoralizing than a veto from an unrelated area |

### Assessing Your Own Experience

Questions for reflection (p. 216): which policies and practices have you written down, and when did you revisit them? What are your values and how do you recognize them? Does your ladder reflect today's team and tomorrow's? Which risks most concern you, and how can you mitigate them without unnecessary bureaucracy?

## Trade-offs at a glance

| Choice | Buys | Costs |
|---|---|---|
| Structurelessness | Speed and freedom while small and homogeneous | Hidden hierarchies; breaks with growth and diversity |
| Structure too early | Order | Slows a group that should focus elsewhere |
| Structure too late | Freedom for longer | Confusion and wasted effort; costly changes of mind |
| Learning from failure | Structure at the right level | Must examine your own contribution |
| Copying successes | Fast start | Wrong context; silver-bullet thinking |
| Many levels, narrow bands | Frequent promotions, fair pay at each level | Levels hard to distinguish |
| Few levels, wide overlapping bands | Clear distinctions; retention flexibility | Pay varies widely within a level |
| Cross-functional pods | Product focus; "us" instead of "us vs. them" | Less efficient technology; specialists elsewhere |
| Heavy process | Safety for rare, risky changes | Slows common, low-risk work |
| Blameless postmortems | People report and learn from mistakes | Requires discipline after a stressful outage |

## Beyond the book

- **Jo Freeman's essay** "The Tyranny of Structurelessness" was written in 1970 and published in the early 1970s; the book quotes its four conditions at length (pp. 193–194).
- **Public career ladders.** Since 2017 many companies have published their ladders (collected at sites such as progression.fyi), easing the "start from scratch" problem the book describes (p. 202) — while its lesson that a borrowed ladder may not fit still applies.
- **Blameless postmortems** were popularized in web operations by John Allspaw's 2012 Etsy post "Blameless PostMortems and a Just Culture"; Allspaw's "On Being a Senior Engineer" is the post the author shared with her team (p. 203).
- **Team Topologies** (Skelton and Pais, 2019) later built on Conway's law with "stream-aligned" teams — close to the book's pods — and platform teams like its infrastructure group.

## Connections

- **Related chapters:** [3. Tech Lead](03-tech-lead.md) (the tech lead as responsibilities on the ladder; the process czar), [4. Managing People](04-managing-people.md) (promotions and up-or-out levels), [6. Managing Multiple Teams](06-managing-multiple-teams.md) (purpose-driven teams built on company values), [7. Managing Managers](07-managing-managers.md) (hiring managers for culture fit), [8. The Big Leagues](08-the-big-leagues.md) (True North and role modeling).

## Check yourself

*Questions and answers are the vault's, written from the notes above; answers cite the book's printed pages.*

1. **How does the author reframe "structure" and "process" for skeptics?**

   *Answer:* As learning and transparency: we set up systems to learn from successes and mistakes and share those lessons, which is how organizations become stable and scalable (p. 191).

2. **Which is one of Freeman's conditions for an unstructured group to work?**
   - [ ] It is large and diverse
   - [x] It has a low degree of skill specialization, so no one is indispensable
   - [ ] It has a strong leader

   *Answer:* The four conditions are task orientation, small size and homogeneity, high communication, and low skill specialization (pp. 193–194).

3. **Why should failure rather than success guide changes to structure?**

   *Answer:* We tend to blame failure on bad luck until our own role is undeniable, so we're less likely to overstructure from it; success tempts us with silver bullets whose context we don't understand (p. 197).

4. **Why is "engineers who graduated from MIT" not a culture?**

   *Answer:* It admits a very narrow subset of people without guaranteeing shared values; a set of real values ("innovation, hard work, intellect, scientific process, data") admits more people who actually share principles (p. 199).

5. **Why did the author's first, lightweight career ladder fail?**
   - [ ] It had too many levels
   - [x] It was too vague for a team with diverse backgrounds, so people obsessed over levels and argued for promotion
   - [ ] HR rejected it

   *Answer:* Her friend's team shared a background at one large company; hers didn't, and needed detail (pp. 203–204).

6. **What is a breakpoint level?**

   *Answer:* The lowest level where someone can stay indefinitely without underperforming — often senior engineer; below it are "up or out" levels (p. 206).

7. **How should heavy process be allocated, if process is risk management?**

   *Answer:* Only to rare activities or ones with non-obvious risks; frequent, low-risk or obviously risky work should stay quick (e.g. light code review), while hidden risks are drawn into the open (p. 212).

8. **Name two practices for a useful postmortem.**

   *Answer:* Resist blame; understand the context and contributing factors; be realistic about takeaways — pick the one or two highest-risk items and acknowledge the rest you're letting go (p. 214).
