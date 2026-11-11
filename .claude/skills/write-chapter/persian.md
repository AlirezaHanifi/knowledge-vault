# Writing a Persian chapter (`lang: fa`)

A Persian book is Persian everywhere a reader looks: the book README and its hub page, the chapter note and its lesson, the widgets, the lab READMEs. Write it with the `persian-writing` skill (semi-formal written register, ZWNJ, Persian punctuation), and follow these vault rules on top.

## Words

- **Use the English technical term whenever practitioners say it in English.** The reader is an engineer or data person; for them «cloud»، «self-hosted»، «replica»، «leader»، «follower»، «shard»، «cache»، «index»، «throughput»، «latency»، «write skew» are the plain words. Never coin a Persian equivalent nobody says aloud: «ابر» for cloud, «میزبانی خودی» for self-hosting, «رهبر/پیرو» for leader/follower, «حافظه‌ی نهان» for cache are all wrong here. Test: how would a Persian-speaking engineer say it to a colleague?
- **The banned list is [`scripts/fa_terms.tsv`](../../../scripts/fa_terms.tsv)**: every coined word met so far («هم‌روند» → concurrent، «پردازه» → process، «تغییرناپذیر» → immutable، «کارخواه» → client، «خطی‌پذیر» → linearizable، «دقیقاً‌یک‌بار» → exactly-once، «بازپخش» → replay، «زنده‌بودن» → liveness …), with the books it applies to. `scripts/validate.py` fails on any of them; `python3 scripts/fa_terms.py --fix` rewrites them. When you meet a new calque, add a row there instead of fixing one file, so it never comes back.
- **Same Persian word, different English term**: a rule can be scoped to books. «گذرا» is *transient* for failures but *transitive* for schema compatibility; «جهش» is *mutation* in DOP, a *mutant* in mutation testing and a *spike* in a chart. Read the sentence before you add a row.
- **Keep Persian words that engineers really use:** دیتابیس، کوئری، جدول، ستون، ردیف، تراکنش، سرور، شبکه، داده، خطا، حذف، نوشتن، خواندن.
- **One form, not both.** No «تکثیر (replication)» and no «replication (تکثیر)»: write the one form the field uses.
- **Parentheses only when nothing else works.** Examples follow «؛ مثلاً …», a second clause or a new sentence: «بار خیلی تغییر می‌کند؛ مثلاً تحلیل تعاملی با بار ناگهانی», not «بار خیلی تغییر می‌کند (مثلاً …)». Page references `(p. N)` are the exception: the validator needs them.
- **Plural and ezafe on English terms** take Persian suffixes: replicaها، شاردِ داغ → «shard داغ»، «leaderِ جدید» → «leader جدید». Keep each Latin run whole (orthography rule 2 of `persian-writing`).

## Layout and digits

- **Every Persian line starts with a Persian word**: sentences, bullets, headings, outline items, quiz options, lab README titles. Lead with a word that names what the term is: «مفهوم consistency…»، «الگوریتم Raft…»، «ساختار B-Tree…»، «سیستم Kafka…»، «نقش leader…»، «عمل compaction…»، «بخش …» for an outline item, «همه‌ی processها…» for a plural, «یک process…» for an indefinite. A book's own sidebar is «کادر Ask the CTO: …». Table cells, code, figure captions and lines that open with a vault marker are exempt. The validator checks this too (`scripts/fa_terms.py`).
- **All numbers a reader sees are Persian**: prose, outline text, figure references («شکل ۴-۲»), quiz numbering, the takeaway cards, the slide counter, widget readouts. Latin digits stay only where they are part of a name or code: p95, S3, 2PC, SOC 2, N+1, version numbers, code, SQL, page references in the Markdown source (the lesson shows those in Persian).
- **Headings** are Persian with technical terms in English: `### LSM-tree و SSTable` → «### ساختار SSTable و LSM-tree». The `##` headings use the Persian names in `H2_ALIASES` (`scripts/build.py`). When a heading changes, update the `slide:` ids in the chapter's pipeline-map widget.
- **Page references stay Latin in the source:** `(p. 74)`, `(pp. 74–75)`, never `(ص. ۷۴)` or `(صص. ۷۴–۷۵)` in a chapter note or book README; the validator rejects the Persian form and the lesson renders the Latin one in Persian. Only widgets and lab READMEs write `ص.`.
- **The lesson sidebar shows bare section titles.** The build drops page references and section numbers («۵.۳.۱»، «موضوع ۱۲») from the sidebar list; the slide heading keeps them. Don't strip numbers from the headings by hand.
- **Markers stay English in the source** (`**In practice:**`, `**Your turn:**`, `*Answer:*`, `**Try it:**`, `**Run it:**`, `*Figure N-M (p. X):*`); the lesson shows them in Persian.

## Widgets of a Persian book

- `<html lang="fa" dir="rtl">`; every visible string Persian (title, description, eyebrow, lede, source note, labels, buttons, log lines, *What to notice*, quiz, breadcrumbs, *Related*), technical terms English.
- The kit does the rest: Vazirmatn, Persian labels on the player and quiz, Persian digits in every text node outside `code`, `.mono`, `.kv`, `.chip` and `[lang=en]`, and SVG kept left to right so charts still line up. Write numbers in JavaScript as numbers; don't convert them by hand.
- Page references inside a widget are written in Persian (`ص. ۶`, `صص. ۵–۷`); the `(p. N)` form is only for chapter notes, where the validator reads it.
- Code, SQL, keys and record values stay English (put them in `code` or `.mono`). Strings that mix a Latin identifier with Persian go in a `<bdi>` or start with a Persian word.

## Labs of a Persian book

- The README is Persian (`## اجرا`, `## خروجی مورد انتظار`, `## به چه چیزی نگاه کنید`, `## پیوندها`), with one line saying the output is English because most terminals render right-to-left text badly. The script and its output stay English.

## The book README and hub

- The README sets `lang: fa` in its front matter and uses the Persian `##` names in `BOOK_H2_ALIASES` (`scripts/build.py`): «درباره‌ی کتاب»، «محتوای این پوشه»، «کتاب چطور به هم وصل است»، «فصل‌ها»، «مفهوم‌های کلیدی»، «منابع همراه»، «این یادداشت‌ها چطور نوشته شده‌اند»، «منبع». The `#` title, the front matter, the authors' names and the publisher stay English.
- The *Chapters* table lists each chapter by its `translated_title`, with Persian digits in the number and page columns. Glossary names keep the English term practitioners use; definitions are Persian.
- The reading-map Mermaid diagram is Persian, and every label opens with a Persian word («فصل ۵: encoding و تکامل», not «۵ · encoding و تکامل»), or Latin-first labels read left to right.
- Name the book's own sections in Persian wherever they are quoted, in notes, widgets and lab READMEs: «ذخیره‌سازی log-structured», not «Log-Structured Storage». Titles of outside papers and talks stay as published.

## Before you finish

Read every paragraph once more for a Persian word that should have been English, a gloss in parentheses, an example in parentheses, and a Latin digit. Then rebuild and open the lesson.
