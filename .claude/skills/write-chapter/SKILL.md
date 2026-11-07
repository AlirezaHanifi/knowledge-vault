---
name: write-chapter
description: Write or extend a chapter note for a book in the vault — summary, takeaways, section-by-section notes with page references, Mermaid diagrams, trade-offs, a separated "Beyond the book", connections, and a "Check yourself" quiz — then regenerate its interactive lesson. Use when processing, summarizing, or improving a chapter.
---

# Write a chapter

The chapter note `books/<slug>/chapters/NN-*.md` is the single source of truth: `scripts/build.py` turns it into the slide lesson `NN-*.html` beside it. Write for both readers — the Markdown must read well on GitHub, and every heading becomes a slide.

## Steps

1. **Read the chapter in the source** (its own summary first, then each section). Extract text with `python3 scripts/pdf.py text books/<slug>/book.pdf /tmp/book.txt` if needed.
2. **Fill the template** [`chapter.md`](chapter.md), keeping its section order (the lesson generator relies on these exact `##` headings):
   - `## Summary` (one paragraph) and `## Key takeaways` (4–7 bullets, with pages).
   - `## Section outline` — the book's nested TOC with printed pages (already there from `add-book`).
   - `## Notes` — one `###` per top-level book section; use `####` to split a long section (each becomes its own slide; a trailing `(pp. a–b)` becomes the slide's page chip). Every book claim carries a printed page reference. Where the book draws the mechanism, show **its own figure** (the `add-figures` skill: `![what it shows](../figures/NN-MM.png)` then `*Figure N-M (p. n): what to look at.*`) instead of describing or redrawing it; use Mermaid for the vault's own diagrams, and caption a diagram of your own synthesis as such. Aim for depth that is easy to scan: read the chapter's full text (`scripts/pdf.py text`), keep the book's own numbers, examples and named systems, and put comparisons into tables (the book's own tables verbatim, with their figure/table number), sequences into `sequenceDiagram`s, and pipelines into flowcharts. Text before the first `###` becomes an *Introduction* slide.
   - Embed a simulation where it fits, on its own line inside the relevant section:
     `> **Try it:** [Title](../widgets/NN-slug.html) — one-line description.`
   - `## Trade-offs at a glance` when the chapter compares approaches.
   - `## Beyond the book` — anything not from the authors (outside sources, interpretation). Shorter in-line asides use `> **Vault note:** …`.
   - `## Connections` — `**Run it:**` experiments (`../lab/NN-slug/README.md`) and related chapters.
   - `## Check yourself` — 4–6 numbered questions testing understanding. Give two or three of them options as task items (`- [x]` marks the right one); every question ends with an `*Answer:*` paragraph citing pages. Questions without options become reveal cards.
3. **Glossary.** If the chapter introduces an idea that recurs across chapters, add or extend its row in the book README's *Key concepts* table (term, one-sentence definition, chapter links). There are no separate concept files.
4. **Figures.** Run `add-figures` for the chapter: list its captions, pick the ones that teach, crop, look at each crop, place it and trim the prose it now carries.
5. **Fact-check** with the `fact-check` skill before calling it done.
6. **Rebuild and validate:** `python3 scripts/build.py && python3 scripts/validate.py`, then open the lesson (see `check-site`).

## Done when

- Every section of the book's outline is covered under *Notes*; no placeholders remain.
- The book's key figures appear where they explain best, each with alt text and a `*Figure N-M (p. n): …*` caption.
- Author content and *Beyond the book* are clearly separated; every book claim has a page reference that `fact-check` confirmed.
- The lesson builds, every slide renders, and the validator passes.
