#!/usr/bin/env python3
"""Persian-writing checks for Persian books: coined terms and Latin-first lines.

1. Coined terms: find (and with --fix, replace) coined Persian technical terms.

The rules live in scripts/fa_terms.tsv: one coined Persian word per line and the
English term a Persian-speaking engineer actually says. scripts/validate.py
fails on any match; this script lists them, and `--fix` rewrites them in place,
keeping Persian suffixes (replicaها، processی). The rules are
ordered: phrases before the words inside them. Read the diff after a fix: a
rewritten word can land at the start of a line, which a Persian line must not.

2. Latin-first lines: a Persian line in Markdown must open with a Persian word,
   or GitHub lays it out left to right. Table rows, code, figures and lines that
   open with a vault marker (**Try it:**, *Answer:* …) are exempt. Fix by hand:
   lead with «مفهوم»، «الگوریتم»، «ساختار»، «سیستم»، «نقش»، «همه‌ی …ها» or reword.

Usage: python3 scripts/fa_terms.py [--fix] [book-slug ...]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TECH = ["data-engineering-design-patterns", "data-oriented-programming", "database-internals",
        "designing-data-intensive-applications", "think-distributed-systems", "the-pragmatic-programmer"]
GROUPS = {"TECH": TECH, "DIST": ["data-engineering-design-patterns", "database-internals",
                                 "designing-data-intensive-applications", "think-distributed-systems"]}
FA = "؀-ۿ"
SUFFIX = r"(‌?(?:هایی|های|ها|ای|اش|شان|اند|ی|ش))?"


def rules() -> list[tuple[re.Pattern, str, set[str] | None]]:
    out = []
    for line in (ROOT / "scripts" / "fa_terms.tsv").read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        pat, eng, scope = line.split("\t")
        books = None if scope == "*" else {b for part in scope.split(",") for b in GROUPS.get(part, [part])}
        out.append((re.compile(rf"(?<![{FA}‌]){pat}{SUFFIX}(?![{FA}])"), eng, books))
    return out


def persian_books() -> list[Path]:
    return [d for d in sorted((ROOT / "books").iterdir())
            if (d / "README.md").exists() and re.search(r"^lang:\s*fa\s*$", (d / "README.md").read_text(encoding="utf-8"), re.M)]


def files(book: Path) -> list[Path]:
    fs = [book / "README.md", book / "framework.md", *sorted(book.glob("chapters/*.md")),
          *sorted(book.glob("widgets/*.html")), *sorted(book.glob("lab/*/README.md"))]
    return [f for f in fs if f.exists()]


MARKER = re.compile(r"^(\*\*(In practice|Your turn|Try it|Run it|Vault note):\*\*|\*Answer:\*|\*Figure [^:]*:)")
BLOCK = re.compile(r"^(\s*(>|#{1,6}|\[[ x]\]|[-+]|\*(?=\s)|[0-9]+\.|<details><summary>[^<]*</summary>)\s*)+")
INLINE = re.compile(r"^(\s*(\*\*|\*|_|\[|«|\(|`)\s*)+")


def latin_first(text: str) -> list[int]:
    """Line numbers of Persian Markdown lines whose first word is Latin."""
    out, fence, fm = [], False, 0
    for i, line in enumerate(text.split("\n"), 1):
        if line.strip() == "---" and fm < 2 and i < 40:
            fm += 1
            continue
        if fm == 1:
            continue
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        if fence or line.lstrip().startswith(("|", "![")) or not re.search(f"[{FA}]", line):
            continue
        s = BLOCK.sub("", line.lstrip())
        if MARKER.match(s):
            continue
        m = re.search(f"[A-Za-z{FA}]", INLINE.sub("", s))
        if m and m.group().isascii():
            out.append(i)
    return out


def english(eng: str, suffix: str | None) -> str:
    if not suffix:
        return eng
    if re.match(rf"[{FA}]", eng[-1]):  # a Persian replacement keeps the suffix as written
        return eng + (suffix if suffix.startswith("\u200c") else "\u200c" + suffix)
    s = suffix.lstrip("‌")
    if s == "ی" and suffix.startswith("‌"):  # ezafe after a final ه: «پردازه‌ی» → «process»
        return eng
    if s == "ای":
        s = "ی"
    return eng + s


def scan(fix: bool, only: set[str]) -> list[str]:
    found = []
    rs = rules()
    for book in persian_books():
        if only and book.name not in only:
            continue
        for f in files(book):
            text = orig = f.read_text(encoding="utf-8")
            for rx, eng, books in rs:
                if books is not None and book.name not in books:
                    continue
                for m in rx.finditer(text):
                    line = text.count("\n", 0, m.start()) + 1
                    found.append(f"{f.relative_to(ROOT)}:{line}: «{m.group(0)}» → {eng}")
                if fix:
                    text = rx.sub(lambda m: english(eng, m.group(1)), text)
            if fix and text != orig:
                f.write_text(text, encoding="utf-8")
    return found


if __name__ == "__main__":
    args = sys.argv[1:]
    fix = "--fix" in args
    only = {a for a in args if not a.startswith("--")}
    hits = scan(fix, only)
    print("\n".join(hits))
    print(f"{len(hits)} coined term(s) {'replaced' if fix else 'found'}.")
    lat = [f"{f.relative_to(ROOT)}:{n}" for b in persian_books() if not only or b.name in only
           for f in files(b) if f.suffix == ".md" for n in latin_first(f.read_text(encoding="utf-8"))]
    print("\n".join(lat))
    print(f"{len(lat)} Persian line(s) open with a Latin word.")
