---
name: add-book
description: Onboard a new book into the vault from its PDF or publisher catalog — verified metadata, the book's own nested table of contents with printed page numbers, one chapter note per chapter, and a generated hub page. Use when the user adds or uploads a new book.
---

# Add a book

Everything about a book lives in `books/<slug>/`. This skill creates that folder with verified structure only; chapter content comes later via the `write-chapter` skill.

## Steps

1. **Find the source and the page offset.** Prefer the book itself: copy the PDF to `books/<slug>/book.pdf` (ignored by git via `books/*/*.pdf`). Open any numbered page and note *PDF page − printed page*; that is the `--offset`. Render the cover for the hub page (committed, small):

   ```sh
   pdftoppm -f 1 -l 1 -jpeg -jpegopt quality=85 -scale-to-x 480 -scale-to-y -1 books/<slug>/book.pdf books/<slug>/cover && mv books/<slug>/cover-*.jpg books/<slug>/cover.jpg
   ```

2. **Extract the outline and text** (poppler required):

   ```sh
   python3 scripts/pdf.py outline books/<slug>/book.pdf --offset N   # nested TOC from the PDF's bookmarks, printed pages
   python3 scripts/pdf.py text books/<slug>/book.pdf /tmp/book.txt   # for fact-checking later
   ```

   `python3 scripts/pdf.py figures books/<slug> --offset N` lists the figure captions; chapters pick from them later (`add-figures`).

   No bookmarks? Transcribe the printed contents pages instead and say so in *Source*. Never use another edition's TOC or memory.
3. **Create `books/<slug>/README.md`** from [`book.md`](book.md). Slug: full title in kebab-case, no edition unless two editions coexist. Fill only keys you verified; `short_title` is the name used in breadcrumbs. One *Chapters* row per chapter (number, linked title, printed pages). The chapter map is the book's own structure (parts, if any); any grouping of your own must be labelled as such.
4. **Create one note per chapter** at `chapters/NN-title-slug.md` from the `write-chapter` skill's [template](../write-chapter/chapter.md): front matter, navigation line, and the verified outline pasted from step 2. Other sections are added when the chapter is written — never as empty placeholders.
5. **Register the book** with a row in the root `README.md` *Books* table (linked title, authors).
6. **Build and validate:**

   ```sh
   python3 scripts/build.py && python3 scripts/validate.py
   ```

## Done when

- Every chapter title and section heading matches the source exactly; pages are printed pages.
- `toc_source`, `toc_verified` and the *Source* section state what was checked and what wasn't, plus the page offset.
- `index.html` lists the book; the validator passes.
