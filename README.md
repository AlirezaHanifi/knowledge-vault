# Knowledge Vault

Technical books turned into interactive lessons. For each book there is one folder with faithful chapter notes (page-referenced, with diagrams), a slide-by-slide lesson generated from each note, hand-built simulations of the mechanisms the book describes, and small experiments you can run. Plain Markdown, dependency-free HTML and standard-library Python — nothing to install, works offline from disk.

**Start here: open [`index.html`](index.html) in a browser.**

## Books

| Book | Authors |
|---|---|
| [Designing Data-Intensive Applications, 2nd Edition](books/designing-data-intensive-applications/README.md) | Martin Kleppmann, Chris Riccomini |
| [Data Engineering Design Patterns](books/data-engineering-design-patterns/README.md) | Bartosz Konieczny |
| [Data-Oriented Programming](books/data-oriented-programming/README.md) | Yehonathan Sharvit |
| [Database Internals](books/database-internals/README.md) | Alex Petrov |

## Layout

```text
index.html                    library page (generated)
books/<book>/
  README.md                   metadata, chapter list and map, key concepts
  index.html                  book hub (generated)
  cover.jpg                   cover, rendered from the PDF
  book.pdf                    source PDF for fact-checking (gitignored)
  chapters/NN-*.md            chapter notes — the source of truth
  chapters/NN-*.html          interactive lesson for each note (generated)
  widgets/NN-*.html           simulations, embedded in the lessons
  lab/NN-*/                   runnable experiments with expected output
assets/                       shared design kit (kit.css/js), site styles, vendored Mermaid
scripts/                      build.py · validate.py · pdf.py
.claude/skills/               playbooks for recurring work (add a book, write a chapter, …)
```

## Working on the vault

```sh
python3 scripts/build.py       # regenerate the HTML from the Markdown
python3 scripts/validate.py    # links, front matter, structure, stale pages
python3 -m http.server 8765    # optional: browse at http://localhost:8765
```

Rules and workflows are in [`AGENTS.md`](AGENTS.md) — for people and AI agents alike. Commit messages use `area: summary`, e.g. `ddia: ch8 notes`, `ddia: fencing widget`, `site: lesson navigation`.
