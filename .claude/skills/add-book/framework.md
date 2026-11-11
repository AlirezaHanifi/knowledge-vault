# The book's framework (`framework.md`)

Every book gets one `framework.md` once its chapters are written: the vault's own whole-to-part reading of the book, rendered to `framework.html` as a slide deck and linked from the hub and from every lesson's last slide. It is synthesis, not summary, so it says so in its first paragraph, and every claim links the chapters it rests on. Models: `books/designing-data-intensive-applications/framework.md` (a technical book) and `books/engineering-leadership-the-hard-parts/framework.md` (a management book).

## Front matter

```yaml
book: <slug>
title: "چارچوب کتاب: <one line naming the book's arc>"
lang: fa            # when the book is Persian
post_map: "نقشه‌ی فصل‌ها"   # the `##` heading of the chapter map, which lessons link to
```

## Shape (every book, in this order)

The deck goes from the whole to the parts in five levels, and each level's first slide says which one it is (`*سطح ۱ از ۵: کل.*` … `*سطح ۵ از ۵: جزء.*`).

| Section (`##`) | Level | What it holds |
|---|---|---|
| Title, nav line, intro | — | `[کتاب](README.md) · [فصل ۱ ←](chapters/01-….md)`; two paragraphs: this is the vault's synthesis, and its three layers (map, principles, decision guide and stack). |
| تصویر کل | — | `### کل کتاب در سه جمله` (three bold sentences, each with chapter links) and `### از کل به جزء` (a Mermaid chain of the five levels). |
| نقشه‌ی کتاب | 1, whole | A Mermaid map of the book's own structure (parts, layers, the ladder it climbs), then a table: layer · main question · chapters. If the book has its own synthesis (a closing chapter that names layers), use it and cite it. |
| N اصل | 2, view | One generic four-box Mermaid (trap → principle → tool → result), then one `###` per principle: its own four-box chain and three bullets, each a bold claim with chapter links. Four to six principles; the book's own principles when it names them. |
| از پرسش/موقعیت/مسئله به فصل | 3, decision | Table: a situation the reader meets · read first · then. |
| دام‌ها | 3 | A numbered list of the book's traps, each bolded and linked. |
| در stack شما | 4, work | Link `../../practice/reference-stack.md`; a table: stack part · principle · chapters · reminder; then one `> **In practice:**` callout with *Your turn* and *Answer* citing chapters. |
| نقشه‌ی فصل‌ها | 5, part | Table: every chapter · its layer · its principle(s) · its role in the framework. |

## Rules

- Everything is the vault's reading (rule 2), so it cites chapters, not pages; a claim no chapter supports is left out. Pattern, principle and tip names are the book's own, checked against the chapter notes.
- The repository is public: the stack table and callout use only `practice/reference-stack.md`.
- Persian frameworks follow [`write-chapter/persian.md`](../write-chapter/persian.md): English technical terms, Persian digits in links and prose, every line starting with a Persian word (bold bullets too: «**رفتن سراغ scale…**», not «**scale…**»). Run `python3 scripts/fa_terms.py --fix <slug>`, then build and validate.
