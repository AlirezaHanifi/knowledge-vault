---
name: in-practice
description: Tie a chapter's ideas to the reader's day-to-day data platform — a pipeline-map widget, scenario simulations, and a short "In practice" callout in each section that maps the book's mechanism onto the reference stack (practice/reference-stack.md), with a "Your turn" question and answer drawn from real data-team situations. Use when the user wants a chapter connected to their job, their company's stack, or practical scenarios.
---

# Map a chapter to work

The book explains a mechanism; this skill shows where that mechanism lives in a real data platform and makes the reader use it there. Every callout is written against [`practice/reference-stack.md`](../../../practice/reference-stack.md), a composite "ordinary data-team stack": the data path (relational OLTP sources → dlt loader → Parquet staging → ClickHouse with Bronze/Silver/Gold layers → Metabase, notebooks, a prediction API), the platform around it (Docker images on Kubernetes, Ansible for stateful hosts, GitLab CI → Argo CD GitOps delivery, Prometheus + Grafana + OpenTelemetry, Authentik SSO) and the team that runs it (merge requests, on-call, blameless incident reviews, delivery and data-health metrics).

**Which part of the stack a book maps to:**

| Book kind | Map onto |
|---|---|
| Storage, distributed systems, data engineering (DDIA, Database Internals, Think Distributed Systems, Data Engineering Design Patterns) | The data path *and* the platform: ClickHouse internals, loader retries and idempotency, Kubernetes pods that die mid-run, Argo CD rollbacks, Prometheus alerts on lag and freshness. |
| Programming practice (The Pragmatic Programmer, Data-Oriented Programming) | The code the team writes: loader and DAG code in Python, SQL models, tests in GitLab CI, config in Git, immutable data in transformations. |
| Management and leadership (The Manager's Path, Engineering Leadership: The Hard Parts) | *How the team works*: merge-request review, on-call and incident reviews, planning under interrupts, metrics from GitLab and Grafana. |
| Product analytics (Paul Levchuk's posts) | The serving layer: Gold tables, Metabase dashboards, notebooks, the cohort and retention SQL an analyst writes on ClickHouse. |

**The repository is public.** The stack page and the callouts describe a generic platform. Never write a company name, partner name, internal table or service name, team member, volume or figure from a private document. If the user gives a private document, extract the *shape* of the stack (kinds of systems, layers, conventions) into `practice/reference-stack.md` in generic words, and nothing else.

## Steps

1. **Read `practice/reference-stack.md`** and the chapter note. If the user describes a change to their stack, update `practice/reference-stack.md` first (it is the only home of that description).
2. **For each `###` section of *Notes* (and each `####` subsection that teaches a mechanism the stack really has)** decide whether the idea shows up in the stack. Skip a subsection rather than force a link: a weak mapping teaches less than none. Most chapters get 5–10 callouts.
3. **Show before telling — as much as the material allows.** The reader came for visuals and hands-on work, not more prose: anything that can be seen should be a figure, table or diagram, and anything that can be manipulated (a parameter, an interleaving, a failure, a before/after) should be a widget the reader drives. Per chapter:
   - **One pipeline map**: copy `books/designing-data-intensive-applications/widgets/03-pipeline-map.html` and refill its lenses with the chapter's ideas, stage by stage (source → loader → Bronze → Silver → Gold → notebooks → dashboards & API). Embed it in the chapter's introduction.
   - **One or two scenario widgets** (`build-widget` skill) for the situations where the idea bites hardest on the stack: something the reader can break and then fix, e.g. `03-join-fanout.html` (a join that double-counts) or `03-incremental-delete.html` (a delete the loader never sees). Start with a prediction, show the failure, offer the fixes.
   - **Make the book's own notes visual-first, without dropping a concept.** List every concept the section teaches (bold terms, examples, named systems, page refs) before you edit, and tick each one off after. Then turn paragraphs into the form that shows the idea: a comparison table (two options × the same questions), a bullet list of consequences, a Mermaid flow for a multi-step mechanism, or the book's own figure (`add-figures`). Keep prose only for one-sentence framing. Any section still longer than one screen after that gets a widget (`03-two-models.html`, `03-graph-traversal.html`, `03-dataframe-pivot.html` are the models: the book's data first, a *Practice* toggle with the same mechanism on data-team data second).
   - **One runnable lab** (`add-experiment`) when the chapter's claims can be run as real code a data person would type: SQL in Python's built-in `sqlite3` is ideal (see `lab/03-sql-models/`). Count things (queries, rows, totals) rather than time them, so the output is deterministic.
4. **Write one short callout per section** where the stack really uses the idea, after the book's material and any `> **Try it:**` line:

   ```markdown
   > **In practice:** Where this shows up on the stack: one or two sentences.
   >
   > **Your turn:** A concrete situation, asked as a question, in one or two sentences.
   >
   > *Answer:* The reason and the fix, at most three sentences, with the book's page.
   ```

   - Where a scenario widget covers the section, drop *Your turn* and follow the one-sentence callout with the widget's `> **Try it:**` line.
   - The callout is the vault's own interpretation (rule 2): when it leans on the book, cite the page (`(p. 74)`). The cited pages must fall inside the section the callout sits in: check them against the PDF outline (`scripts/pdf.py outline`) or the section's own page references, never a guess. An `articles` source has no pages: cite the post's own section heading as `(بخش «section name»)` (two or more: `(بخش‌های «A» و «B»)`), exactly as it appears in the chapter's outline; never `§`, which a Persian reader does not know (the validator rejects it). Product behaviour (ClickHouse, Airflow, dlt, Kubernetes, Argo CD, Prometheus…) must be true for current versions; if unsure, phrase it as something to check.
   - Every chapter of every book gets at least two callouts, so each lesson ends with the reader knowing where the chapter lives in their own work. Persian books write the callout text in Persian (markers stay English).
   - Questions apply the idea instead of recalling it: diagnose a symptom, choose between two designs, predict what breaks.
5. **Persian lessons** (`lang: fa`): follow [`write-chapter/persian.md`](../write-chapter/persian.md) and the `persian-writing` skill. In short: English technical terms wherever practitioners say them in English (cloud, replica, leader, cache), never a gloss in parentheses, examples after «؛ مثلاً», Persian digits for every number a reader sees, every line starting with a Persian word, and the widgets and lab READMEs Persian as well. If a heading changes, update the `slide:` ids in the chapter's pipeline-map widget.
6. **Rebuild and check:** `python3 scripts/build.py && python3 scripts/validate.py`. The generator renders each callout as an *In practice* box with the question as a reveal card; the validator fails a *Your turn* without an *Answer*. Open the lesson and expand a few cards (see `check-site`).

## Done when

- The chapter has a pipeline map and at least one scenario widget, both embedded; no section of the book's notes is a wall of prose, and every concept the section had before is still there.
- Every section where the stack really uses the idea has one short *In practice* callout (a *Your turn* question, or a widget).
- Nothing identifies a company, partner, internal system or private figure.
- The build and validator pass, and the cards open and read well in the lesson, in light and dark mode.
