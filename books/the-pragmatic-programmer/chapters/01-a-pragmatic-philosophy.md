---
book: the-pragmatic-programmer
chapter: 1
title: "A Pragmatic Philosophy"
pages: "34–72"
---

# 1. A Pragmatic Philosophy

[Book](../README.md) · [2. A Pragmatic Approach →](02-a-pragmatic-approach.md)

## Summary

The first chapter is about the programmer rather than the program. Pragmatic Programmers think beyond the immediate problem, place it in a larger context, and take responsibility for what they do (pp. 34–35). The seven topics build that attitude:

- **Agency:** you can change your environment, or change environments (Topic 1).
- **Responsibility:** offer options, not excuses (Topic 2).
- **Fighting entropy:** don't live with broken windows (Topic 3).
- **Catalysing change** without being boiled by it (Topic 4).
- **Good-enough software,** with users in the quality trade-off (Topic 5).
- **A knowledge portfolio** managed like a financial one (Topic 6).
- **Communication** treated as a programming language of its own (Topic 7).

The chapter carries Tips 3 to 13. Tips 1 and 2, *Care About Your Craft* and *Think! About Your Work*, come from the preface (p. 30).

## Key takeaways

- **You have agency.** The authors call it the most important tip in the book: if your environment is bad, try to fix it, but not forever (Tip 3, p. 37).
- **Provide options, don't make lame excuses.** Rehearse the conversation first, to the rubber duck or the cat if need be, and arrive with what *can* be done (Tip 4, pp. 40–41).
- **Neglect accelerates rot faster than any other factor.** Fix a broken window as soon as you find it, or at least board it up (Tip 5, pp. 43–44).
- **Be a catalyst for change, and remember the big picture.** Stone soup gets people to join an ongoing success; the boiled frog doesn't notice gradual decline (Tips 6–7, pp. 47–48).
- **Quality is a requirements issue.** Let users decide when software is good enough, and know when to stop polishing (Tip 8, pp. 51–52).
- **Knowledge is an expiring asset.** Invest in it regularly, diversify, manage risk, and think critically about what you read (Tips 9–10, pp. 54–60).
- **Communication is half the job.** Know what you want to say and your audience; how you say it matters as much as what (Tips 11–13, pp. 63–69).

## Section outline

*From the book’s own table of contents (PDF bookmarks). Page numbers are PDF pages: this edition's reflowed text has no printed page numbers.*

- Topic 1. It’s Your Life — p. 36
- Topic 2. The Cat Ate My Source Code — p. 38
- Topic 3. Software Entropy — p. 42
- Topic 4. Stone Soup and Boiled Frogs — p. 46
- Topic 5. Good-Enough Software — p. 50
- Topic 6. Your Knowledge Portfolio — p. 54
- Topic 7. Communicate! — p. 63

## Notes

The book is a collection of short, self-contained topics that can be read in any order, with numbered **tips**, open-ended **challenges**, and **exercises** whose possible answers are in an appendix (p. 20). Each topic ends with a list of related sections. These notes keep the tip numbers so they can be cross-referenced.

| Tip | Statement | Page |
|---:|---|---|
| 3 | You Have Agency | 37 |
| 4 | Provide Options, Don't Make Lame Excuses | 40 |
| 5 | Don't Live with Broken Windows | 43 |
| 6 | Be a Catalyst for Change | 47 |
| 7 | Remember the Big Picture | 48 |
| 8 | Make Quality a Requirements Issue | 51 |
| 9 | Invest Regularly in Your Knowledge Portfolio | 57 |
| 10 | Critically Analyze What You Read and Hear | 60 |
| 11 | English is Just Another Programming Language | 64 |
| 12 | It's Both What You Say and the Way You Say It | 68 |
| 13 | Build Documentation In, Don't Bolt It On | 68 |

### Topic 1. It’s Your Life

Many developers feel stuck: stagnating, underpaid, passed by technology. The authors' answer is always the same question: why can't you change it? Software development offers unusual control. Skills are in demand, knowledge crosses borders and remote work is possible (p. 36).

- **Tip 3, You Have Agency** (p. 37). Try to fix a bad environment, but don't try forever. Martin Fowler's line: you can change your organization or change your organization.
- If technology is passing you by, study in your own time; it's an investment in yourself (p. 37).
- If you want to work remotely, ask; if the answer is no, find someone who says yes (p. 37).

### Topic 2. The Cat Ate My Source Code

A cornerstone of the philosophy is **taking responsibility** for your career, learning, project and daily work, and not being afraid to admit ignorance or error (p. 38).

| Idea | What the book says |
|---|---|
| **Team trust** | Trust is essential for creativity and collaboration; a team must be able to rely on you, and you on them (pp. 38–39) |
| **Responsibility is agreed to** | You commit to ensuring something is done right without controlling every aspect. You may decline an impossible, too risky or ethically sketchy responsibility (p. 39) |
| **Accountability** | Once you accept, you're accountable. Admit mistakes honestly and offer options (p. 39) |
| **No blame** | Don't blame vendors, languages, management or coworkers. If a vendor might fail you, you should have had a contingency plan; if a disk dies without a backup, it's your fault (pp. 39–40) |

**Tip 4, Provide Options, Don't Make Lame Excuses** (p. 40). Before delivering bad news, run the conversation in your head: what will they ask? Then propose what *can* be done: refactoring, prototyping, better testing or automation, more resources, more time with users, or learning a technique (pp. 40–41). A challenge: follow "I don't know" with "but I'll find out" (p. 41).

### Topic 3. Software Entropy

Disorder in software is **software rot**; some call it "technical debt", implying they'll pay it back someday, which they probably won't (p. 42). Psychology, or culture, is the most important factor (p. 42).

The **broken window** story comes from research on urban decay: one unrepaired broken window gives a sense that nobody cares, and the decline accelerates from there (p. 43). In the original experiment an abandoned car sat untouched for a week, but once a window was broken it was stripped within hours (p. 45).

- **Tip 5, Don't Live with Broken Windows** (p. 43). Bad designs, wrong decisions and poor code should be fixed as soon as they're found. Without time to fix properly, **board it up**: comment out the offending code, show "Not Implemented", or substitute dummy data, so that the damage stops spreading (p. 43).
- **First, do no harm** (pp. 44–45). Firefighters at a burning house rolled out a mat before dragging their hoses over a priceless carpet. In a crisis, don't cause collateral damage. On a pristine codebase, people take extra care not to be the first to make a mess.

> **Try it:** [Broken windows](../widgets/01-broken-windows.html) — let a team keep working on a codebase where every visible mess makes the next one more likely, then compare ignoring broken windows with boarding them up and with fixing them at once.

### Topic 4. Stone Soup and Boiled Frogs

In the **stone soup** story, soldiers boil stones and coax hungry villagers into adding carrots, potatoes, beef and herbs until there is a real meal (pp. 46–47). The soldiers act as a **catalyst** for a result nobody could produce alone (p. 47).

- When permission is hard to get ("start-up fatigue"), work out what you can reasonably ask for, develop it well, and show it. Then let people ask for the rest: people find it easier to join an ongoing success (p. 47). **Tip 6, Be a Catalyst for Change** (p. 47).
- The villagers' side is a warning about **gradual deception**: most disasters start too small to notice, and most overruns happen a day at a time (p. 48). **Tip 7, Remember the Big Picture** (p. 48).
- The **boiled frog** differs from broken windows: broken windows make people stop caring, while the frog simply doesn't notice the change (p. 48).

The challenges ask whether you're making stone soup or frog soup when you catalyze change, and practise situational awareness: without looking, how many lights are in the ceiling above you? (p. 49)

### Topic 5. Good-Enough Software

Perfect, bug-free software isn't achievable, but you can discipline yourself to write software that is **good enough** for users, maintainers and your own peace of mind (pp. 50–51, after Yourdon). This doesn't mean sloppy code: systems must meet requirements and basic performance, privacy and security standards (p. 51).

- **Involve users in the trade-off.** For pacemakers, autopilots or widely used libraries, the bar is fixed and high. For a new product, scope and quality should be discussed as part of the requirements (p. 51). **Tip 8, Make Quality a Requirements Issue** (p. 51).
- Many users prefer software with rough edges today to a perfect version in a year, and early feedback leads to a better solution (p. 52; see Topic 12, Tracer Bullets).
- **Know when to stop.** Like a painting lost in the paint, a program can be spoiled by overembellishment and overrefinement (p. 52).

### Topic 6. Your Knowledge Portfolio

Knowledge and experience are your most important professional assets, and they **expire** (p. 54). Managing a knowledge portfolio is like managing a financial one (p. 55):

| Investment rule | Applied to knowledge (pp. 55–57) |
|---|---|
| **Invest regularly** | A habit, at a consistent time and place; the habit matters as much as the amounts |
| **Diversify** | Know your current technology in depth, then others, including non-technical skills |
| **Manage risk** | Spread across risky, high-reward technologies and low-risk standards |
| **Buy low, sell high** | Learn an emerging technology early, as Java's early adopters did |
| **Review and rebalance** | Last month's hot technology may be cold now |

**Tip 9, Invest Regularly in Your Knowledge Portfolio** (p. 57). Suggested goals: learn at least one new language every year; read a technical book each month; read nontechnical books too; take classes; join user groups and meetups; experiment with different environments; stay current (pp. 57–58). The value is in the learning itself, whether or not you use the technology (p. 59). When asked something you don't know, take it as a personal challenge to find out (p. 59).

**Tip 10, Critically Analyze What You Read and Hear** (p. 60). Beware of hype and of commercial placement in search results and bookshops (p. 60). Questions to ask (pp. 60–61):

- Ask "why?" at least five times (the **Five Whys**).
- Who does this benefit?
- What's the context: best for whom?
- When or where would this work? Use second-order thinking: what happens after that?
- Why is this a problem? What is the underlying model?

### Topic 7. Communicate

A good idea is an orphan without effective communication (p. 63). Treat natural language like code, applying DRY, ETC and automation to it: **Tip 11, English is Just Another Programming Language** (pp. 63–64).

| Practice | What it means (pp. 64–68) |
|---|---|
| **Know your audience** | Pitch the same change differently to users, marketing, managers and developers. Gather feedback: "the meaning of your communication is the response you get" |
| **Know what you want to say** | Plan and outline, then check that it communicates |
| **Choose your moment** | Six o'clock on a bad Friday is no time to ask for a laptop upgrade. Ask "is this a good time?" |
| **Choose a style** | Formal briefing or long chat, expert or newcomer. If in doubt, ask; push back if a paragraph can't do the job |
| **Make it look good** | Use style sheets, headers, spelling checks (automatic and by hand) |
| **Involve your audience** | Early drafts and feedback; the process often matters more than the document |
| **Be a listener** | If you don't listen to them, they won't listen to you |
| **Get back to people** | Always respond, even if only to say you'll get back later |

**Tip 12, It's Both What You Say and the Way You Say It** (p. 68).

**Documentation.** **Tip 13, Build Documentation In, Don't Bolt It On** (p. 68). Generate documentation from comments on modules and exported functions, but don't comment every declaration mechanically: that means two things to update and violates DRY. Non-API comments should explain **why**: trade-offs, decisions and discarded alternatives (pp. 68–69).

**Online communication** (sidebar, p. 70): proofread before sending, keep the format simple, keep quoting minimal and attributed, don't flame, check the recipients, and remember that email and posts are forever.

## Trade-offs at a glance

| Choice | Buys | Costs |
|---|---|---|
| Fix a broken window now | Stops the spread; signals that someone cares | Time taken from today's task |
| Board it up | Contains the damage cheaply | The real fix is still owed |
| Leave it | Nothing today | Rot spreads and morale drops |
| Ship good-enough software early | Feedback; users get value sooner | Rough edges, which must be agreed with users |
| Keep polishing | Fewer rough edges | Late delivery; overrefinement |
| Stone soup (show a small success) | Avoids start-up fatigue; people join | It can shade into deception, or frog soup |
| Low-risk knowledge investments | Steady value | Miss emerging opportunities |
| High-risk knowledge investments | Large payoff if they take off | May expire worthless |

## Beyond the book

- **The broken windows theory is contested.** The source the book cites, Wilson and Kelling's 1982 article, led to policing policies whose effect on crime is disputed in criminology. As a metaphor for code, the idea is supported by a related observation: developers imitate the style and quality of the code around them. The vault's [broken-windows simulation](../widgets/01-broken-windows.html) is a model of that contagion, not data.
- **Technical debt as a deliberate choice.** Ward Cunningham's original debt metaphor described consciously shipping imperfect understanding and repaying it by refactoring. The book is sceptical that the debt gets repaid; [Topic 40, Refactoring](07-while-you-are-coding.md) is where it returns to the repayment.
- **Psychological safety.** Google's Project Aristotle (2015) found that psychological safety was the strongest predictor of team effectiveness, which echoes the book's emphasis on team trust and admitting mistakes.

## Connections

- **Related chapters:** [2. A Pragmatic Approach](02-a-pragmatic-approach.md) (DRY and ETC, which Topic 7 applies to writing; tracer bullets for early feedback), [7. While You Are Coding](07-while-you-are-coding.md) (refactoring as fixing broken windows; programming by coincidence as the frog's blind spot), [8. Before the Project](08-before-the-project.md) (requirements and users in the quality trade-off), [9. Pragmatic Projects](09-pragmatic-projects.md) (broken windows and boiled frogs at team level).

## Check yourself

*Questions and answers are the vault's, written from the notes above; answers cite the book's PDF pages.*

1. **Which tip do the authors call the most important in the book?**

   *Answer:* Tip 3, You Have Agency (p. 37).

2. **What should you do before telling someone something can't be done?**

   *Answer:* Run the conversation in your head (or explain it to the rubber duck or the cat), anticipate their questions, and come with options rather than excuses (Tip 4, pp. 40–41).

3. **You find a badly designed module and have no time to fix it properly. What does the book suggest?**
   - [ ] Leave it until the next release
   - [x] Board it up: comment it out, show "Not Implemented", or substitute dummy data
   - [ ] Rewrite the whole subsystem

   *Answer:* Take some action that prevents further damage and shows you're on top of it (p. 43).

4. **How does the boiled frog differ from the broken window?**

   *Answer:* With broken windows, people stop fighting entropy because no one seems to care. The frog simply doesn't notice the gradual change (p. 48).

5. **Who should decide when software is good enough?**

   *Answer:* The users should participate: scope and quality are part of the requirements (Tip 8, p. 51).

6. **Name the five rules of the knowledge portfolio.**

   *Answer:* Invest regularly, diversify, manage risk, buy low and sell high, review and rebalance (pp. 55–57).

7. **What should a non-API code comment explain?**

   *Answer:* Why something is done: its purpose, trade-offs and discarded alternatives. The code already shows how (p. 69).
