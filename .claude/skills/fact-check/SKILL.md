---
name: fact-check
description: Verify a chapter note, quiz, simulation or experiment against the book's PDF text — every number, example, named system, figure reference, quotation and page reference — and fix or mark anything unverifiable. Use after writing or editing book-derived content, or when the user asks whether something is accurate.
---

# Fact-check against the source

The vault's first rule is never to fabricate book content. Fluent paraphrase is easy to get subtly wrong, so check specifics mechanically.

## Steps

1. **Get the text once:** `python3 scripts/pdf.py text books/<slug>/book.pdf /tmp/book.txt` (the page offset is in the book README's `source_file`).
2. **List the checkable claims** in what you wrote: numbers and units, example values and names, named systems and papers, figure/table numbers, quotations, and every page reference.
3. **Search them**, restricted to the chapter's printed page range:

   ```sh
   python3 scripts/pdf.py find /tmp/book.txt --offset 24 --pages 115-160 "sparse index" "Bloom filter" "LMDB|copy-on-write"
   ```

   `XX` means not found in that range: rephrase the search (synonyms with `|`, a shorter distinctive fragment), widen the range, or read the page.
4. **Fix every miss:** correct the page, rewrite the claim to what the book says, move it under *Beyond the book* if it is outside knowledge, or remove it. Use `TODO(unverified)` only as a temporary marker — never leave one in finished work.
5. **Quotations** must match word for word, stay under ~15 words, and carry a page.
6. **Simulations and experiments:** check the `source-note` (pages, which figures/examples are the book's) and that example data the book defines (e.g. a record and its byte sizes) reproduces exactly.

## Done when

- Every claim in the list was found on the cited pages, or was fixed.
- Keyword search can't catch a wrong *interpretation*: reread each paragraph next to its source pages for anything that changes meaning.
