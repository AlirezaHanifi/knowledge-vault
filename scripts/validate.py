#!/usr/bin/env python3
"""Validate the knowledge vault: structure, metadata, links, and generated pages.

Checks:
  1. Internal Markdown links resolve to real files, and #anchors match a
     heading in the target file (GitHub slug rules). Relative href/src
     references in HTML files resolve too.
  2. Required front matter exists on book READMEs and chapter notes.
  3. Chapter notes are named NN-kebab-case-title.md and their front matter
     agrees with the filename.
  4. Every widget is embedded in at least one chapter ("> **Try it:**"), and
     every lab experiment has a README and is linked from a chapter.
  5. The book README's "Chapters" table lists exactly the chapter files.
  6. Generated HTML is up to date with its Markdown (scripts/build.py --check).
  7. No empty directories.
  8. Every "> **In practice:**" callout's "**Your turn:**" question carries an
     "*Answer:*", and the reference stack it is written against exists.
  9. Persian books use the English technical term, not a coined Persian one
     (scripts/fa_terms.tsv), no Persian Markdown line opens with a Latin word, and
     page references in Persian Markdown keep the (p. N) form.

Hidden folders (.claude skills and templates, local sources) are skipped.
Stdlib only. Exit 0 = healthy, 1 = problems found.
"""

from __future__ import annotations

import re
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {"node_modules", "vendor", "raw"}  # `raw/` holds a source's saved pages: local-only, gitignored, not vault content
IGNORED_NAMES = {".DS_Store", ".gitkeep"}

BOOK_FM_REQUIRED = ("title", "edition", "authors", "publisher", "year",
                    "toc_source", "toc_verified")
CHAPTER_FM_REQUIRED = ("book", "chapter", "title")

CHAPTER_NAME_RE = re.compile(r"^(\d{2})-([a-z0-9]+(?:-[a-z0-9]+)*)\.md$")
FM_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
HEADING_RE = re.compile(r"^ {0,3}(#{1,6})\s+(.+?)\s*#*\s*$")
LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")
HTML_REF_RE = re.compile(r'''(?:href|src)\s*=\s*["']([^"'#]+?)(?:#[^"']*)?["']''')
SEP_ROW_RE = re.compile(r"^[\s|:\-]+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

errors: list[str] = []
warnings: list[str] = []
link_targets: set[Path] = set()
slug_cache: dict[Path, set[str]] = {}


def rel(p: Path) -> str:
    try:
        return p.relative_to(ROOT).as_posix()
    except ValueError:
        return str(p)


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def parse_fm(text: str) -> dict[str, str]:
    m = FM_RE.match(text)
    fm: dict[str, str] = {}
    if not m:
        return fm
    for line in m.group(1).splitlines():
        s = line.strip()
        if not s or s.startswith(("#", "-")) or ":" not in s:
            continue
        key, _, value = s.partition(":")
        fm[key.strip()] = value.strip().strip('"')
    return fm


def strip_fences(text: str) -> str:
    out: list[str] = []
    fence = False
    for line in text.splitlines():
        if line.lstrip().startswith(("```", "~~~")):
            fence = not fence
            continue
        if not fence:
            out.append(line)
    return "\n".join(out)


def slug_set(text: str) -> set[str]:
    slugs: set[str] = set()
    counts: dict[str, int] = {}
    for line in strip_fences(text).splitlines():
        m = HEADING_RE.match(line)
        if not m:
            continue
        s = re.sub(r"`[^`]*`", "", m.group(2)).strip().lower()
        s = re.sub(r"[^\w\- ]", "", s).replace(" ", "-")
        n = counts.get(s, 0)
        counts[s] = n + 1
        slugs.add(s if n == 0 else f"{s}-{n}")
    return slugs


def section_lines(text: str, title: str) -> list[str]:
    out: list[str] = []
    capture = False
    for line in text.splitlines():
        m = HEADING_RE.match(line)
        if m and len(m.group(1)) <= 2:
            if capture:
                break
            capture = m.group(2).strip().lower() == title.lower()
        elif capture:
            out.append(line)
    return out


def slugs_for(path: Path) -> set[str]:
    if path not in slug_cache:
        slug_cache[path] = slug_set(path.read_text(encoding="utf-8"))
    return slug_cache[path]


def check_links(p: Path, body: str) -> None:
    for no, line in enumerate(body.splitlines(), 1):
        for _, raw in LINK_RE.findall(line):
            target = raw.strip()
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            file_part, _, anchor = urllib.parse.unquote(target).partition("#")
            if file_part:
                resolved = (p.parent / file_part).resolve()
                if not resolved.exists():
                    err(f"{rel(p)}:{no}: link target not found: {file_part}")
                    continue
                link_targets.add(resolved)
                if anchor and resolved.suffix == ".md" and anchor not in slugs_for(resolved):
                    err(f"{rel(p)}:{no}: anchor '#{anchor}' not found in {rel(resolved)}")
            elif anchor and anchor not in slugs_for(p):
                err(f"{rel(p)}:{no}: anchor '#{anchor}' not found in this file")


def skipped(p: Path) -> bool:
    parts = p.relative_to(ROOT).parts
    return bool(SKIP_PARTS & set(parts)) or any(x.startswith(".") for x in parts)


def check_html_links(p: Path) -> None:
    text = p.read_text(encoding="utf-8")
    for no, line in enumerate(text.splitlines(), 1):
        for target in HTML_REF_RE.findall(line):
            if re.match(r"^[a-z]+:|^//|^\$\{", target):
                continue
            resolved = (p.parent / urllib.parse.unquote(target)).resolve()
            if not resolved.exists():
                err(f"{rel(p)}:{no}: href/src target not found: {target}")
            else:
                link_targets.add(resolved)


def check_book(d: Path) -> None:
    readme = d / "README.md"
    text = readme.read_text(encoding="utf-8")
    fm = parse_fm(text)
    missing = [k for k in BOOK_FM_REQUIRED if k not in fm or not fm[k]]
    if missing:
        err(f"{rel(readme)}: missing front matter keys: {', '.join(missing)}")
    if fm.get("cover") and not (d / fm["cover"]).exists():
        err(f"{rel(readme)}: cover image not found: {fm['cover']}")

    rows = []
    if fm.get("lang", "en") not in ("en", "fa"):
        err(f"{rel(readme)}: lang must be 'en' or 'fa' (the languages scripts/build.py has labels for)")
    if fm.get("kind", "book") not in ("book", "articles"):
        err(f"{rel(readme)}: kind must be 'book' or 'articles' (the two groups the library page lists)")
    # A Persian README (`lang: fa`) names the section «فصل‌ها» (scripts/build.py, BOOK_H2_ALIASES).
    for line in section_lines(text, "Chapters") or section_lines(text, "فصل‌ها") or section_lines(text, "نوشته‌ها"):
        s = line.strip()
        if not (s.startswith("|") and s.endswith("|")) or SEP_ROW_RE.match(s):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if cells[0].isdigit():
            rows.append(cells)

    chapters_dir = d / "chapters"
    chapter_files: list[Path] = []
    if not chapters_dir.exists():
        warn(f"{rel(d)}: no chapters/ directory yet")
    else:
        for f in sorted(chapters_dir.iterdir()):
            if f.is_dir() or f.suffix == ".html":  # lessons are generated; build --check covers them
                continue
            m = CHAPTER_NAME_RE.match(f.name)
            if not m:
                err(f"{rel(f)}: chapter name must match NN-kebab-case-title.md")
                continue
            chapter_files.append(f)
            cfm = parse_fm(f.read_text(encoding="utf-8"))
            cmiss = [k for k in CHAPTER_FM_REQUIRED if not cfm.get(k)]
            if cmiss:
                err(f"{rel(f)}: missing front matter keys: {', '.join(cmiss)}")
            if cfm.get("book") and cfm["book"] != d.name:
                err(f"{rel(f)}: front matter book '{cfm['book']}' != folder '{d.name}'")
            if cfm.get("chapter", "").isdigit() and int(cfm["chapter"]) != int(m.group(1)):
                err(f"{rel(f)}: front matter chapter {cfm['chapter']} != filename {m.group(1)}")
            if f.name not in text:
                err(f"{rel(f)}: not linked from the book README Chapters table")
            if cfm.get("lang", "en") not in ("en", "fa"):
                err(f"{rel(f)}: lang must be 'en' or 'fa' (the languages scripts/build.py has labels for)")
            check_practice_callouts(f)
    if chapters_dir.exists() and chapter_files and len(chapter_files) != len(rows):
        err(f"{rel(readme)}: Chapters table has {len(rows)} rows "
            f"but chapters/ has {len(chapter_files)} files")


def check_practice_callouts(f: Path) -> None:
    """'> **In practice:**' blocks: each '**Your turn:**' needs an '*Answer:*' in the same block."""
    blocks, cur = [], None
    for line in strip_fences(f.read_text(encoding="utf-8")).split("\n"):
        if line.startswith("> **In practice:**"):
            cur = [line]
            blocks.append(cur)
        elif cur is not None and line.startswith(">"):
            cur.append(line)
        else:
            cur = None
    if blocks and not (ROOT / "practice" / "reference-stack.md").exists():
        err(f"{rel(f)}: has 'In practice' callouts but practice/reference-stack.md is missing")
    for b in blocks:
        text = "\n".join(b)
        if "**Your turn:**" in text and "*Answer:*" not in text.split("**Your turn:**", 1)[1]:
            err(f"{rel(f)}: an 'In practice' callout asks 'Your turn' without an '*Answer:*'")


FIG_LINE_RE = re.compile(r"^!\[([^\]]*)\]\(\.\./figures/([^)\s]+)\)\s*$")
FIG_CAPTION_RE = re.compile(r"^\*Figure ([\w.-]+) \(pp?\. (\d+)(?:[–-]\d+)?\): \S.*\*$")
FA_PAGE_REF = re.compile(r"\((?:صص|ص)\.\s")  # Markdown keeps (p. N); the build renders it in Persian
OFFSET_RE = re.compile(r"PDF page\s*[−-]\s*(\d+)")


def check_figures(book: Path) -> None:
    """Every figure image is recorded in figures.tsv (so it can be re-rendered from
    the PDF) and embedded in a chapter as `![alt](../figures/F)` followed by an italic
    `*Figure L (p. N): …*` caption whose label and printed page match the record."""
    folder = book / "figures"
    images = sorted(folder.glob("*.png")) if folder.exists() else []
    tsv = folder / "figures.tsv"
    rows: dict[str, list[str]] = {}
    if tsv.exists():
        for line in tsv.read_text(encoding="utf-8").splitlines()[1:]:
            cells = line.split("\t")
            if len(cells) != 4:
                err(f"{rel(tsv)}: malformed row: {line!r}")
                continue
            rows[cells[0]] = cells
            if not (folder / cells[0]).exists():
                err(f"{rel(tsv)}: lists {cells[0]}, which does not exist")
    elif images:
        err(f"{rel(folder)}: figures.tsv is missing (render figures with scripts/pdf.py figure)")
    for img in images:
        if img.name not in rows:
            err(f"{rel(img)}: not recorded in figures.tsv")
    readme = (book / "README.md").read_text(encoding="utf-8") if (book / "README.md").exists() else ""
    m = OFFSET_RE.search(parse_fm(readme).get("source_file", ""))
    offset = int(m.group(1)) if m else (0 if "all references are PDF pages" in readme else None)
    used: set[str] = set()
    for ch in sorted(book.glob("chapters/*.md")):
        lines = ch.read_text(encoding="utf-8").splitlines()
        for no, line in enumerate(lines, 1):
            if not line.startswith("!["):
                continue
            fm = FIG_LINE_RE.match(line)
            if not fm:
                err(f"{rel(ch)}:{no}: figure must be its own line: ![what it shows](../figures/FILE.png)")
                continue
            alt, file = fm.groups()
            used.add(file)
            if len(alt.split()) < 3 or alt.lower().startswith(("figure", "image", "diagram")):
                err(f"{rel(ch)}:{no}: alt text must say what the figure shows, not name it")
            nxt = next((l for l in lines[no:] if l.strip()), "")
            cm = FIG_CAPTION_RE.match(nxt)
            if not cm:
                err(f"{rel(ch)}:{no}: figure needs a caption line: *Figure L (p. N): what to look at.*")
                continue
            row = rows.get(file)
            if row and cm.group(1) != row[1]:
                err(f"{rel(ch)}:{no}: caption says Figure {cm.group(1)}, figures.tsv says {row[1]}")
            if row and offset is not None and int(cm.group(2)) != int(row[2]) - offset:
                err(f"{rel(ch)}:{no}: caption page {cm.group(2)} != printed page "
                    f"{int(row[2]) - offset} of the crop (PDF page {row[2]})")
    for img in images:
        if img.name not in used:
            err(f"{rel(img)}: not used by any chapter")


def main() -> int:
    md_files = [p for p in sorted(ROOT.rglob("*.md")) if not skipped(p)]
    html_files = [p for p in sorted(ROOT.rglob("*.html")) if not skipped(p)]
    for p in html_files:
        check_html_links(p)
    texts = {p: p.read_text(encoding="utf-8") for p in md_files}

    for p, text in texts.items():
        check_links(p, strip_fences(text))

    # Books: schema, chapter table, chapter files.
    books_dir = ROOT / "books"
    for d in sorted(books_dir.iterdir()) if books_dir.exists() else []:
        if d.is_dir():
            check_book(d)

    # Widgets are embedded in a lesson; experiments have a README and are linked.
    for book in sorted(books_dir.glob("*/")) if books_dir.exists() else []:
        notes = "\n".join(c.read_text(encoding="utf-8") for c in sorted(book.glob("chapters/*.md")))
        # A book's framework page (framework.md, the vault's synthesis) may embed widgets too.
        framework = (book / "framework.md").read_text(encoding="utf-8") if (book / "framework.md").exists() else ""
        # Every book with written chapters gets a framework (.claude/skills/add-book/framework.md).
        if not framework and re.search(r"^## (Summary|خلاصه)", notes, re.M):
            warn(f"{rel(book)}: no framework.md (see .claude/skills/add-book/framework.md)")
        for w in sorted(book.glob("widgets/*.html")):
            embedded = any(f"**Try it:** [" in src and f"widgets/{w.name})" in src for src in (notes, framework))
            if not embedded:
                err(f"{rel(w)}: not embedded in any chapter or framework (add a '> **Try it:**' line)")
            # A widget that links to lesson slides (`LESSON = "../chapters/x.html#"`
            # plus `slide: "id"`) must name slides that exist in that lesson.
            wtext = w.read_text(encoding="utf-8")
            lesson = re.search(r'LESSON\s*=\s*"\.\./chapters/([^"#]+\.html)#', wtext)
            if lesson:
                lp = book / "chapters" / lesson.group(1)
                ids = set(re.findall(r'id="([^"]+)"', lp.read_text(encoding="utf-8"))) if lp.exists() else set()
                for sid in sorted(set(re.findall(r'slide:\s*"([^"]+)"', wtext)) - ids):
                    err(f"{rel(w)}: slide '{sid}' does not exist in {lesson.group(1)}")
        for exp in sorted(p for p in book.glob("lab/*") if p.is_dir()):
            if not (exp / "README.md").exists():
                err(f"{rel(exp)}: experiment missing README.md")
            elif f"../lab/{exp.name}/README.md" not in notes:
                err(f"{rel(exp)}: not linked from any chapter's Connections")

    # Book figures: recorded crops, each used by a chapter with a proper caption.
    for book in sorted(books_dir.glob("*/")) if books_dir.exists() else []:
        check_figures(book)

    # Persian books: English technical terms, Persian-first lines (scripts/fa_terms.py).
    sys.path.insert(0, str(ROOT / "scripts"))
    import fa_terms  # noqa: E402
    for hit in fa_terms.scan(False, set()):
        err(f"{hit} (coined Persian term; see scripts/fa_terms.tsv)")
    for b in fa_terms.persian_books():
        for f in fa_terms.files(b):
            if f.suffix in (".md", ".html") and "§" in f.read_text(encoding="utf-8"):
                err(f"{rel(f)}: '§' means nothing to a Persian reader; cite a post's section as (بخش «عنوان»)")
            if f.suffix == ".md":
                text = f.read_text(encoding="utf-8")
                for n in fa_terms.latin_first(text):
                    err(f"{rel(f)}:{n}: Persian line opens with a Latin word")
                for n, line in enumerate(text.split("\n"), 1):
                    if "lab" not in f.parts and FA_PAGE_REF.search(line):  # lab READMEs are read on GitHub as they are
                        err(f"{rel(f)}:{n}: page reference in Persian form; write (p. N) or (pp. N–M), the lesson shows it in Persian")

    # Generated pages must match their sources.
    sys.path.insert(0, str(ROOT / "scripts"))
    import build  # noqa: E402
    for path, text in build.outputs().items():
        if not path.exists() or path.read_text(encoding="utf-8") != text:
            err(f"{rel(path)}: generated page is stale — run python3 scripts/build.py")

    # Hygiene: no empty directories.
    for p in sorted(ROOT.rglob("*")):
        if not p.is_dir() or skipped(p):
            continue
        if not [c for c in p.iterdir() if c.name not in IGNORED_NAMES]:
            err(f"empty directory: {rel(p)}")

    print(f"Checked {len(md_files)} Markdown and {len(html_files)} HTML files, "
          f"{len(link_targets)} internal "
          f"link targets, {len(list(books_dir.glob('*/README.md')))} book(s).")
    for w in warnings:
        print(f"  warning: {w}")
    for e in errors:
        print(f"  error:   {e}")
    print(f"Vault: {len(errors)} error(s), {len(warnings)} warning(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
