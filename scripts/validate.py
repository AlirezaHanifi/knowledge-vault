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

Hidden folders (.claude skills and templates, local sources) are skipped.
Stdlib only. Exit 0 = healthy, 1 = problems found.
"""

from __future__ import annotations

import re
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {"node_modules", "vendor"}
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
    for line in section_lines(text, "Chapters"):
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
    if chapters_dir.exists() and chapter_files and len(chapter_files) != len(rows):
        err(f"{rel(readme)}: Chapters table has {len(rows)} rows "
            f"but chapters/ has {len(chapter_files)} files")


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
        for w in sorted(book.glob("widgets/*.html")):
            if f"**Try it:** [" not in notes or f"../widgets/{w.name})" not in notes:
                err(f"{rel(w)}: not embedded in any chapter (add a '> **Try it:**' line)")
        for exp in sorted(p for p in book.glob("lab/*") if p.is_dir()):
            if not (exp / "README.md").exists():
                err(f"{rel(exp)}: experiment missing README.md")
            elif f"../lab/{exp.name}/README.md" not in notes:
                err(f"{rel(exp)}: not linked from any chapter's Connections")

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
