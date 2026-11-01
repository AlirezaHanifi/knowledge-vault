#!/usr/bin/env python3
"""Source-PDF helpers for onboarding and fact-checking a book (needs poppler: pdftohtml, pdftotext).

    python3 scripts/pdf.py outline BOOK.pdf --offset 24          # nested TOC from PDF bookmarks, printed pages
    python3 scripts/pdf.py text BOOK.pdf OUT.txt                 # full text, pages separated by form feeds
    python3 scripts/pdf.py find OUT.txt --offset 24 "phrase" ... # printed pages where each phrase occurs
    python3 scripts/pdf.py find OUT.txt --offset 24 --pages 115-160 "memtable|SSTable"

`--offset` is PDF page minus printed page (record it in the book README).
In `find`, "a|b" matches either alternative; matching ignores case, line
breaks and hyphenation. Printed results are the evidence for a page reference.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import xml.etree.ElementTree as ET


def outline(pdf: str, offset: int) -> None:
    xml = subprocess.run(["pdftohtml", "-xml", "-i", "-stdout", "-f", "1", "-l", "1", pdf],
                         capture_output=True, text=True, check=True).stdout
    m = re.search(r"<outline>.*</outline>", xml, re.S)
    if not m:
        sys.exit("No bookmark outline in this PDF; build the TOC from its contents pages instead.")
    root = ET.fromstring(m.group(0))

    def walk(node, depth):
        for child in node:
            if child.tag == "item":
                page = child.get("page")
                printed = f" — p. {int(page) - offset}" if page and int(page) - offset > 0 else ""
                print("  " * depth + f"- {(child.text or '').strip()}{printed}")
            elif child.tag == "outline":
                walk(child, depth + 1)

    walk(root, 0)


def text(pdf: str, out: str) -> None:
    subprocess.run(["pdftotext", "-layout", pdf, out], check=True)
    print(f"Wrote {out}")


def find(txt: str, offset: int, pages: str | None, phrases: list[str]) -> int:
    raw = open(txt, encoding="utf-8").read().split("\f")
    lo, hi = (int(x) for x in pages.split("-")) if pages else (-10**9, 10**9)
    norm = {}
    for i, page in enumerate(raw):
        printed = i + 1 - offset
        if lo <= printed <= hi:
            page = re.sub(r"[-‐]\s*\n\s*", "", page)  # join hyphenated line breaks
            norm[printed] = re.sub(r"\s+", " ", page).lower()
    missing = 0
    for phrase in phrases:
        alts = [a.lower() for a in phrase.split("|")]
        hits = [p for p, t in norm.items() if any(a in t for a in alts)]
        missing += not hits
        print(f"{'OK' if hits else 'XX'}  {phrase}: {hits[:12]}{' …' if len(hits) > 12 else ''}")
    return 1 if missing else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    o = sub.add_parser("outline"); o.add_argument("pdf"); o.add_argument("--offset", type=int, default=0)
    t = sub.add_parser("text"); t.add_argument("pdf"); t.add_argument("out")
    f = sub.add_parser("find"); f.add_argument("txt"); f.add_argument("phrases", nargs="+")
    f.add_argument("--offset", type=int, default=0); f.add_argument("--pages")
    a = ap.parse_args()
    if a.cmd == "outline":
        outline(a.pdf, a.offset)
    elif a.cmd == "text":
        text(a.pdf, a.out)
    else:
        return find(a.txt, a.offset, a.pages, a.phrases)
    return 0


if __name__ == "__main__":
    sys.exit(main())
