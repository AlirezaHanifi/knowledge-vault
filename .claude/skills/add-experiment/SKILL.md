---
name: add-experiment
description: Add a runnable, deterministic Python experiment (standard library only) that measures a claim from a book chapter, with its README and real expected output, and link it from the chapter. Use when a mechanism is best understood by running code and looking at numbers.
---

# Add a lab experiment

An experiment lives in `books/<slug>/lab/NN-slug/` (NN = the chapter): one script and a `README.md`. Choose an experiment over a widget when the insight is in numbers — counts, sizes, distributions, amplification — or when "the algorithm does X" is best proved by running it.

## Steps

1. **Script:** Python 3.10+, standard library only, no network, seeded randomness, writes nothing outside a temp directory. Print a compact, labelled report.
2. **README**, in this order (the book hub reads the title, the first paragraph and the first command under *Run*):
   - `# Title`, then one paragraph saying what it demonstrates.
   - `*Illustrates <Book>, “<Section>”, pp. a–b. The implementation is the vault’s own.*`
   - `## Run` with a `sh` code block: `python3 script.py`
   - `## Expected output` — pasted from a real run, never typed by hand.
   - `## What to look for` — 3–5 bullets tying numbers to the book's claims.
   - `## Related` — the chapter lesson (`../../chapters/NN-slug.md`) and any widget (`../../widgets/NN-slug.html`).
3. **Link it** from the chapter note's *Connections* as `**Run it:**` (the lesson shows the command automatically).
4. **Verify:** run it twice — the output must be identical and match the README — then `python3 scripts/build.py && python3 scripts/validate.py`.

## Done when

- A fresh run matches *Expected output* exactly.
- Book numbers the script reproduces were checked with the `fact-check` skill.
