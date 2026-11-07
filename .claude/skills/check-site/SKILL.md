---
name: check-site
description: Rebuild and verify the vault before finishing any change — regenerate HTML, run the validator, re-run experiments, and check the affected lessons and widgets in a browser (console, phone width, dark mode, embedding). Use before saying a vault change is done.
---

# Check the site

## 1. Build and validate

```sh
python3 scripts/build.py      # regenerate lessons, hubs and the library page
python3 scripts/validate.py   # links, anchors, front matter, structure, stale HTML
```

Both must succeed. The validator fails if generated HTML is out of date, so never edit `chapters/*.html`, `books/*/index.html` or the root `index.html` by hand.

## 2. Experiments you touched

Run each from its folder and compare with its README's *Expected output*; they must match exactly.

## 3. Browser

Serve the repo (`python3 -m http.server 8765`, or the `vault` entry in `.claude/launch.json`) and open the affected pages. For each:

- **Console** is free of errors.
- **Lesson:** step through every slide with <kbd>→</kbd>; diagrams render; each embedded widget loads and sizes itself; quizzes mark answers; the last slide links to the next chapter.
- **Figures:** each loads, is legible at slide width, sits on its paper card in dark mode and opens full size on click.
- **Widget:** play, step, reset and every control work on the page itself and inside the lesson.
- **Phone width (375 px):** no horizontal page scroll; the lesson's *Contents* drawer opens and closes.
- **Dark mode:** toggle the theme; text, diagrams and embedded widgets follow it.
- **Offline:** pages load nothing from the network (`file://` works too).

## 4. Report

Say what was checked and what wasn't (e.g. a browser you didn't test), with any failures quoted.
