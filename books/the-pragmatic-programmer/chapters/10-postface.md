---
book: the-pragmatic-programmer
chapter: 10
title: "Postface"
pages: "469–473"
---

# 10. Postface

[← 9. Pragmatic Projects](09-pragmatic-projects.md) · [Book](../README.md)

## Summary

In the twenty years since the first edition, software has grown from business machinery to something that has "truly taken over the world" (p. 469). Developers build the future, and with that power comes an extraordinary responsibility, which is rarely discussed (pp. 469–470). The postface gives a moral compass of two questions about every piece of code: *have I protected the user?* and *would I use this myself?* It closes with the last three tips: First, Do No Harm; Don't Enable Scumbags; and Share it, Celebrate it, Build it (pp. 471–473).

## Key takeaways

- **Software is everywhere, and so is its potential for harm:** embedded devices control power plants, cars and medical equipment, and even a heating controller can kill if poorly built (p. 470).
- **Non-embedded systems cut both ways:** social media, big data, loan decisions and surveillance can do great good or great harm, and the difference may be subtle (p. 470).
- **First, do no harm.** Protect users: security patches for the baby monitor, manual control when the thermostat fails, store only the data you need, encrypt anything personal (Tip 98, p. 471).
- **Don't enable scumbags.** Apply the Golden Rule: would you be happy to be a user? If the project skirts ethics, you're as responsible as its sponsors (Tip 99, pp. 471–472).
- **Imagine the future you want,** have the courage to say "no!", and build it (Tip 100, p. 473).

## Section outline

*The PDF bookmarks list the postface without sub-entries; these are its own headings. Page numbers are PDF pages: this edition's reflowed text has no printed page numbers.*

- The Moral Compass — p. 471
- Imagine the Future you Want — p. 473

## Notes

| Tip | Statement | Page |
|---:|---|---|
| 98 | First, Do No Harm | 471 |
| 99 | Don’t Enable Scumbags | 472 |
| 100 | It’s Your Life. Share it. Celebrate it. Build it. | 473 |

The postface opens with Fred Brooks' image, from *The Mythical Man-Month*, of the programmer as a poet building castles in the air from pure thought-stuff (p. 469). Its examples of software's reach: Twitter helping people plan revolutions, the processor in your car stopping a skid, the smartphone that remembers daily details for you (p. 469).

### The Moral Compass

The price of this power is vigilance (p. 471).

| Question | What it asks (pp. 471–472) |
|---|---|
| **1. Have I protected the user?** | Did I list the consequences and protect users from harm? If you can't truthfully say you tried, you bear some responsibility when things go bad. **Tip 98, First, Do No Harm** |
| **2. Would I use this myself?** | A Golden Rule judgment: do I want my details shared, my movements given to retailers, to be driven by this autonomous vehicle? No degree of separation removes your responsibility. **Tip 99, Don't Enable Scumbags** |

### Imagine the Future you Want

The next twenty years are built from your imagination, hopes and concerns. Recognize when you're working against the future you'd want to inhabit and have the courage to say no; envision a better one and have the courage to create it (p. 473). The book ends with **Tip 100**: *It's Your Life. Share it. Celebrate it. Build it.* And have fun (p. 473).

## Trade-offs at a glance

| Choice | Buys | Costs |
|---|---|---|
| Ship and let users cope | Speed | Harm you could have foreseen; shared responsibility |
| List consequences and protect users | Safer, trustworthy systems | Time; harder conversations with sponsors |
| "Just following the spec" | Avoids conflict | Doesn't remove responsibility (p. 472) |
| Saying "no!" | Keeps the future you want | Courage; possibly the project |

## Beyond the book

- **Professional codes.** The ACM Code of Ethics and Professional Conduct (2018) makes the postface's first question explicit: its principle 1.2 is "Avoid harm."
- **Safety-critical practice.** Standards such as IEC 61508 and ISO 26262 for automotive systems turn "however the thermostat fails, the customer still has manual control" into required hazard analysis and fail-safe design.
- **Data minimization.** "Am I storing only the data I need?" (p. 471) is a legal requirement in the EU's GDPR, Article 5(1)(c).

## Connections

- **Related chapters:** [1. A Pragmatic Philosophy](01-a-pragmatic-philosophy.md) (take responsibility; "it's your life"), [7. While You Are Coding](07-while-you-are-coding.md) (stay safe out there; encrypt sensitive data), [9. Pragmatic Projects](09-pragmatic-projects.md) (delight your users; sign your work).

## Check yourself

*Questions and answers are the vault's, written from the notes above; answers cite the book's PDF pages.*

1. **What two questions should you ask of every piece of code you deliver?**

   *Answer:* Have I protected the user? Would I use this myself? (p. 471)

2. **Give two of the book's examples of protecting users.**

   *Answer:* Ongoing security patches for a baby monitor; manual control however a thermostat fails; storing only the data you need and encrypting anything personal (p. 471).

3. **According to the book, does working several steps removed from an unethical project's sponsors excuse you?**
   - [ ] Yes, responsibility lies with the sponsors
   - [x] No, you are just as responsible
   - [ ] Only if you raised concerns

   *Answer:* No matter how many degrees of separation you rationalize, you are just as responsible; don't enable scumbags (pp. 471–472).

4. **Why does the book single out embedded devices?**

   *Answer:* They outnumber laptops, desktops and data-centre computers by an order of magnitude and often control life-critical systems (p. 470).
