---
name: build-widget
description: Build an interactive simulation (a self-contained offline HTML page using the vault's kit) for a mechanism a book describes, and embed it in the chapter's lesson. Use when the user wants something interactive, a visualization, or a "try it" for a chapter.
---

# Build a simulation widget

A widget is one HTML page in `books/<slug>/widgets/NN-slug.html` (NN = the chapter it illustrates). It works on its own and inside a lesson, where it is embedded through an iframe in `#embed` mode (the kit then hides the page chrome and reports its height).

## Steps

1. **Write the learning goal first:** "After this, you can explain why …". If a static Mermaid diagram would teach it as well, draw that instead. Good widget material: interleavings, timelines, state changes you step through, parameters whose effect is the lesson, failures injected by hand.
2. **Ground it in the book.** Read the pages; reuse the book's own examples and values where it has them (and check them with `fact-check`). Anything invented — toy data, simplifications — is named in the `source-note`.
3. **Copy [`widget.html`](widget.html)** and keep its anatomy: eyebrow + `h1` + `lede` → `source-note` (pages, simplifications, "implementation is the vault’s own") → simulation → *What to notice* → *Check your understanding* → *Related* (`no-embed`). The hub reads the `<h1>` and `<meta name="description">`.
4. **Model first, view second.** Keep state in plain variables, a `step()` that returns `false` when finished, and a `render()` that draws everything from state. Random choices use `Kit.rng(seed)` so reset replays the same run.
5. **Use the kit** (`assets/kit.js`): `Kit.el/svg`, `Kit.player` (play/pause/step/reset + keyboard), `Kit.slider`, `Kit.segmented`, `Kit.tabs`, `Kit.log` (aria-live event log), `Kit.quiz`, `Kit.rng`, `Kit.lineChart` (axes, series, shaded bands, marker lines). Colours come from kit tokens only (`var(--accent)`, `--ok`, `--s1`…), never raw values, so dark mode works. Add to the kit only what a second widget needs.
6. **Lay it out to be seen at a glance.** Inside a lesson the simulation should fit one screen (about 650 px tall at 1100 px wide) — never a long vertical stack:
   - `.sim` = visual on the left, a `.stack` of panels on the right. On wide pages the kit packs that right-hand stack into two columns, with its first panel (the controls) spanning both; add `class="wide"` to any other panel that needs the full width.
   - Put event logs and secondary readouts beside or under the visual (a left-hand `.stack`), not below the controls.
   - Several small charts sit side by side in a grid (`repeat(auto-fit, minmax(240px, 1fr))`); draw them with `Kit.lineChart`.
   - Lay out lists of cards or items in grids, and put the numbers in a `.stats` grid. *What to notice* and the quiz already render as card grids.
   - Check the height: open the page with `#embed` inside a lesson at 1440 × 900.
7. **Language.** A widget of a Persian book (`lang: fa` chapters) is written in Persian: `<html lang="fa" dir="rtl">` and every visible string Persian, with technical terms in English, as in [`write-chapter/persian.md`](../write-chapter/persian.md). The kit then supplies the font, the player and quiz labels and Persian digits; keep code and record values in `code` or `.mono` so they stay English.
8. **Accessibility:** native labelled controls, state changes announced through `Kit.log`, meaning never carried by colour alone.
9. **Embed it** in the chapter note with a `> **Try it:**` line (see `write-chapter`), then `python3 scripts/build.py`.
10. **Verify** with the `check-site` skill — the widget on its own *and* inside the lesson.

## Done when

- The page states the chapter, pages and simplifications, and that the implementation is the vault's own.
- It is embedded in at least one lesson and listed on the book hub (automatic once embedded file exists).
- Clean console; works from `file://`, at 375 px, in dark mode, and with the keyboard.
