---
name: build-widget
description: Build an interactive simulation (a self-contained offline HTML page using the vault's kit) for a mechanism a book describes, and embed it in the chapter's lesson. Use when the user wants something interactive, a visualization, or a "try it" for a chapter.
---

# Build a simulation widget

A widget is one HTML page in `books/<slug>/widgets/NN-slug.html` (NN = the chapter it illustrates). It works on its own and inside a lesson, where it is embedded through an iframe in `#embed` mode (the kit then hides the page chrome and reports its height).

## Steps

1. **Write the learning goal first:** "After this, you can explain why …". If a static Mermaid diagram would teach it as well, draw that instead. Good widget material: interleavings, timelines, state changes you step through, parameters whose effect is the lesson, failures injected by hand.
2. **Ground it in the book.** Read the pages; reuse the book's own examples and values where it has them (and check them with `fact-check`). Anything invented — toy data, simplifications — is named in the `source-note`.
3. **Copy [`widget.html`](widget.html)** and keep its anatomy, a *stage page*: `body.stage-page` → `.stage-screen` (a `stage-head` with `h1`, a two-sentence `lede`, the `source-note` with pages, simplifications and "implementation is the vault’s own"; then `.sim-stage`) → `section.stage-more` (*What to notice*, *Check your understanding*, *Related* `no-embed`, footer with the keys). `.sim-stage` holds, in order: `.stage-caption#caption`, `.stage-scene` (the picture), `aside.stage-side` (`.stats`: the numbers that matter, shown as one strip), `.stage-bar#bar`, `.stage-tweak#tweak` (the controls, as `.tweak-group`s). The hub reads the `<h1>` and `<meta name="description">`.
4. **Model first, view second.** Keep state in plain variables, a `step()` that changes it and a `render()` that draws everything from state and syncs the controls (`slider.set`, `segmented.set`, which don't fire their handlers). Random choices use `Kit.rng(seed)`.
5. **Teach with a tour, then let the reader tweak.** `Kit.tour({captionMount, barMount, tweak, reset, render, interval, intro, end, steps})` plays the lesson on its own: each step is `{kind, run, say}` — `run` rebuilds its state from scratch (going back to a step resets and replays), and `say` may be a function, evaluated after `render`, so captions quote the computed numbers. Four or five steps: the normal case, the failure, the fix, a bigger run. Each caption cites its page. The drawer (“Try it yourself”) stays closed until the reader opens it; every handler there is `render(); tour.free(text, kind)`. Replace `Kit.log` with the `said` shim in the template: messages go to the caption, not to a list. Other kit helpers: `Kit.el/svg`, `Kit.slider`, `Kit.segmented`, `Kit.quiz`, `Kit.lineChart`, `Kit.digits`, `Kit.pct`. Colours come from kit tokens only, so dark mode works. Add to the kit only what a second widget needs.
6. **Make it readable at first sight.** The whole stage fits one screen without page scroll; nothing overlaps.
   - Nothing in the scene is smaller than `.8rem` (SVG text ≥ 12px at shown size); an SVG's `viewBox` is close to its shown size and gets a `max-height`.
   - Labels that can collide (two events at nearly the same time, dense rows) are offset by design — above/below, chips that wrap — not left to chance.
   - The scene does not overflow at 1280 × 800, with the drawer closed *and* open (the open drawer takes a column beside the scene, so the scene gets ~300 px narrower: let cards shrink or hide secondary text under `.sim-stage:has(.stage-tweak:not([hidden]))`). Long tables scroll inside a `max-height` box.
   - The bar under the scene stays one row; prefix the classes you invent, because the kit owns `.tour-*` and a bare `.now`/`.done` would restyle its step dots.
7. **Language.** A widget of a Persian book (`lang: fa` chapters) is written in Persian: `<html lang="fa" dir="rtl">` and every visible string Persian, with technical terms in English, as in [`write-chapter/persian.md`](../write-chapter/persian.md). The kit then supplies the font, the player and quiz labels and Persian digits; keep code and record values in `code` or `.mono` so they stay English.
8. **Accessibility:** native labelled controls, state changes announced through the caption (`aria-live`, supplied by `Kit.tour`), meaning never carried by colour alone (shapes, ✓/✗, labels).
9. **Embed it** in the chapter note with a `> **Try it:**` line (see `write-chapter`), then `python3 scripts/build.py`.
10. **Verify** with the `check-site` skill — the widget on its own *and* inside the lesson: watch the tour to the end, open the drawer mid-tour (autoplay must stop and the frame must not keep growing), and read every caption's numbers against the picture.

## Done when

- The page states the chapter, pages and simplifications, and that the implementation is the vault's own.
- It is embedded in at least one lesson and listed on the book hub (automatic once embedded file exists).
- The tour autoplays (unless reduced motion), its captions match the picture, and the scene fits 1280 × 800 with the drawer closed and open.
- Clean console; works from `file://`, at 375 px, in dark mode, and with the keyboard (<kbd>Space</kbd>, <kbd>←</kbd>/<kbd>→</kbd>, <kbd>R</kbd>).
