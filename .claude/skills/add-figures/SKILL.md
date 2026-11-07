---
name: add-figures
description: Pick the book's own figures that teach a chapter best, crop them from the source PDF, and place them in the chapter note with the vault's figure standard (alt text, label, printed page, a "what to look at" caption) — replacing prose or redrawn diagrams the figure explains better. Use when writing or reviewing a chapter, or when the user asks for the book's images, figures or diagrams.
---

# Add the book's figures

A good figure replaces a paragraph. Authors draw the layouts, state changes and message flows that are hardest to say in words; a chapter note should show those figures rather than describe them, and keep its own prose for what the figure doesn't say.

## Choose

Read the chapter's captions first:

```sh
python3 scripts/pdf.py figures books/<slug> --offset N --pages 115-160
```

**Use a figure when it** shows structure (a page layout, a tree, an architecture), a change of state (before/after a split, a merge, a failover), a flow or protocol (who sends what, in which order), or a comparison the author built a picture for — and the note would otherwise need several sentences or a redrawn diagram to say the same.

**Skip a figure when it** only decorates, repeats a table or code listing already in the note, is a screenshot or chart whose point is one sentence, or becomes unreadable at slide width.

**Prefer the book's figure to a Mermaid redraw.** Where a note has a diagram captioned "after Figure X" or "the vault's drawing of Figure X", use the figure and delete the redraw — unless the redraw adds something the figure lacks (the vault's own synthesis across sections, or a sequence the book only describes in text). Mermaid stays the tool for the vault's own diagrams.

**Then trim the prose** the figure now carries: keep the mechanism's names, numbers and the "why"; drop sentence-by-sentence walk-throughs of what the reader can now see.

Budget: usually 2–6 figures per chapter, at most two per slide (`###`/`####` section). A figure belongs in the section that explains it, right after the sentence that introduces it.

## Crop

```sh
python3 scripts/pdf.py figure books/<slug> 4-2 4-3 4-7      # writes figures/04-02.png … and records them
```

The script finds each caption, takes the band between body-text lines, removes the caption and trims to the ink, then records the PDF page and crop box in `books/<slug>/figures/figures.tsv` (so `--all` can re-render everything from the PDF). File names follow the book's label: Figure 4-2 or 4.2 → `04-02.png`.

**Look at every crop** (open the PNG) before using it. Auto-detection can clip a label beside the figure, include a stray heading or tip icon, or merge two stacked figures. Fix with a manual box in PDF points (x, y from the page's top-left; measure on a page render):

```sh
python3 scripts/pdf.py figure books/<slug> 4-2 --page 141 --box 60,90,380,215
```

Books without figure labels: pass `--name NN-slug.png` with `--page` and `--box`, and caption with the page only (see below).

## Place

On its own line inside *Notes*, then a blank line, then the caption line:

```markdown
![Leaf node full of keys splits in two; key 13 moves up into the parent as a new separator](../figures/02-11.png)

*Figure 2-11 (p. 40): inserting 11 overflows the leaf, so half its keys move to a new sibling and the first of them is promoted.*
```

- **Alt text** says what the figure *shows* — enough for someone who can't see it to follow the lesson. Never "Figure 2-11" or "diagram of …".
- **Caption** starts with the book's own label and printed page exactly as `*Figure L (p. N):` (`pp.` for a figure that spans pages; the page of its caption comes first), then one sentence in the vault's words on **what to look at** — not the book's caption copied. Quote the book's caption only if it is short and word-for-word.
- The surrounding text points to it ("as Figure 2-11 shows, …") and adds what the picture can't: the why, the cost, the numbers.
- Figures are the book's content: they sit above *Beyond the book*, never in the vault's own sections.

## Check

- `python3 scripts/validate.py` checks that every image is recorded in `figures.tsv`, used by a chapter, has descriptive alt text and a caption, and that the caption's label and printed page match the crop's PDF page and the book's page offset.
- In the lesson the figure sits on a paper-coloured card (`--paper`), keeps its own colours in dark mode, fits the slide (≤ 68% of the viewport height) and opens full size on click — check it at phone width and in dark mode (`check-site`).

## Done when

- Every mechanism the chapter draws is shown with the book's figure or deliberately skipped by the rules above; no Mermaid redraw duplicates a figure.
- Every crop was looked at; captions match the book's labels and pages; the validator passes.
