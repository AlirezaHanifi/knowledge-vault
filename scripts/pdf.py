#!/usr/bin/env python3
"""Source-PDF helpers for onboarding, fact-checking and illustrating a book (needs poppler).

    python3 scripts/pdf.py outline BOOK.pdf --offset 24          # nested TOC from PDF bookmarks, printed pages
    python3 scripts/pdf.py text BOOK.pdf OUT.txt                 # full text, pages separated by form feeds
    python3 scripts/pdf.py find OUT.txt --offset 24 "phrase" ... # printed pages where each phrase occurs
    python3 scripts/pdf.py find OUT.txt --offset 24 --pages 115-160 "memtable|SSTable"

    python3 scripts/pdf.py figures books/<slug> --offset 24 --pages 115-160   # the book's figure captions
    python3 scripts/pdf.py figure books/<slug> 4-2 [4-3 …]       # crop Figure 4-2 into figures/04-02.png
    python3 scripts/pdf.py figure books/<slug> 4-2 --box 72,90,360,210 --page 141   # manual crop (points)
    python3 scripts/pdf.py figure books/<slug> --all             # re-render every figure in figures.tsv

`--offset` is PDF page minus printed page (record it in the book README).
In `find`, "a|b" matches either alternative; matching ignores case, line
breaks and hyphenation. Printed results are the evidence for a page reference.

`figure` finds the caption, takes the band between the body-text lines
around it, blanks the caption and trims to the ink. It records each crop
(PDF page and box in points) in `books/<slug>/figures/figures.tsv`, so every
image can be re-rendered from the local PDF. Always look at the result.
"""
from __future__ import annotations

import argparse
import html
import os
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

DPI = 180          # output resolution: ~2.5 px per point, sharp on high-density screens
TRIM_DPI = 72      # analysis resolution: 1 px per point
INK = 225          # grey level below which a pixel counts as ink
PAD = 6            # points of white kept around the trimmed figure
CAPTION_RE = r"(?:Figure|Fig\.)\s+{label}(?![\d.-]?\d)"


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


# ---------------------------------------------------------------- figures

class Box:
    def __init__(self, attrs: dict, inner: str, fonts):
        self.top, self.left = float(attrs["top"]), float(attrs["left"])
        self.width, self.height = float(attrs["width"]), float(attrs["height"])
        self.font = attrs["font"]
        self.size, self.family = fonts[self.font]
        self.text = html.unescape(re.sub(r"<[^>]+>", "", inner))

    @property
    def bottom(self):
        return self.top + self.height

    @property
    def right(self):
        return self.left + self.width


def page_layout(pdf: str, first: int, last: int) -> dict[int, tuple[float, float, list[Box]]]:
    """Text boxes per PDF page, in points: {page: (width, height, boxes)}."""
    xml = subprocess.run(["pdftohtml", "-xml", "-i", "-zoom", "1", "-stdout", "-f", str(first), "-l", str(last), pdf],
                         capture_output=True, text=True, check=True).stdout
    attrs = lambda s: dict(re.findall(r'(\w+)="([^"]*)"', s))
    fonts: dict[str, tuple[float, str]] = {}
    pages = {}
    # poppler's XML is not always well-formed (crossed <b>/<i>), so read it with patterns.
    for m in re.finditer(r"<page ([^>]*)>(.*?)</page>", xml, re.S):
        pa, inner = attrs(m.group(1)), m.group(2)
        for fs in re.finditer(r"<fontspec ([^>]*)/>", inner):
            fa = attrs(fs.group(1))
            fonts[fa["id"]] = (float(fa["size"]), fa["family"])
        boxes = [Box(attrs(t.group(1)), t.group(2), fonts) for t in re.finditer(r"<text ([^>]*)>(.*?)</text>", inner, re.S)]
        pages[int(pa["number"])] = (float(pa["width"]), float(pa["height"]), [b for b in boxes if b.text.strip()])
    return pages


def body_size(boxes: list[Box]) -> float:
    sizes = Counter()
    for b in boxes:
        sizes[b.size] += len(b.text)
    return sizes.most_common(1)[0][0] if sizes else 10.0


def is_prose(b: Box, size: float) -> bool:
    return b.size >= 0.9 * size and not re.search(r"It(alic)?\b|Oblique", b.family)


def captions(boxes: list[Box], label: str = r"\d+(?:[.-]\d+)?") -> list[tuple[str, list[Box]]]:
    """Figure captions on a page: (label, boxes of the caption's lines)."""
    size = body_size(boxes)
    found = []
    for b in boxes:
        m = re.match(r"\s*(?:Figure|Fig\.)\s+(" + label + r")(?![\d.-]?\d)", b.text)
        if not m or is_prose(b, size):
            continue
        if b.size > 0.85 * size and any(is_prose(o, size) and abs(o.top - b.top) < 3 for o in boxes):
            continue  # a cross-reference inside a sentence, not a caption
        lines = [b]
        for o in sorted(boxes, key=lambda o: (o.top, o.left)):
            if o is b or o.font != b.font or o.top < b.top - 1 or o.left < b.left - 2:
                continue
            if o.top - lines[-1].bottom < 0.8 * b.height:
                lines.append(o)
        found.append((m.group(1), lines))
    return found


def caption_text(lines: list[Box]) -> str:
    return re.sub(r"\s+", " ", " ".join(l.text for l in sorted(lines, key=lambda l: (round(l.top), l.left)))).strip()


def figures_list(book: str, offset: int, pages: str | None) -> None:
    pdf = str(Path(book) / "book.pdf")
    first, last = ((int(x) + offset for x in pages.split("-")) if pages else (1, 99999))
    for num, (_, _, boxes) in page_layout(pdf, first, last).items():
        for label, lines in captions(boxes):
            print(f"{label:>6}  p. {num - offset:<4} (PDF {num})  {caption_text(lines)[:150]}")


def render(pdf: str, page: int, box: tuple[float, float, float, float], dpi: int, out: str, fmt: str) -> None:
    x, y, w, h = (round(v * dpi / 72) for v in box)
    args = ["pdftoppm", "-r", str(dpi), "-f", str(page), "-l", str(page), "-x", str(x), "-y", str(y),
            "-W", str(w), "-H", str(h), "-singlefile"]
    args += {"pgm": ["-gray"], "ppm": [], "png": ["-png"], "gray-png": ["-png", "-gray"]}[fmt]
    subprocess.run(args + [pdf, out], check=True, capture_output=True)


def read_pnm(path: str) -> tuple[int, int, int, bytes]:
    data = open(path, "rb").read()
    parts = re.match(rb"P([56])\s+(\d+)\s+(\d+)\s+(\d+)\s", data)
    channels = 1 if parts.group(1) == b"5" else 3
    return int(parts.group(2)), int(parts.group(3)), channels, data[parts.end():]


def detect_box(pdf: str, page: int, label: str, layout) -> tuple[float, float, float, float]:
    width, height, boxes = layout
    size = body_size(boxes)
    caps = captions(boxes)
    mine = next((lines for l, lines in caps if l == label), None)
    if not mine:
        raise SystemExit(f"Figure {label}: no caption found on PDF page {page}; pass --box and --page")
    ctop, cbottom = min(l.top for l in mine), max(l.bottom for l in mine)
    cleft = min(l.left for l in mine)
    cap_ids = {id(l) for _, lines in caps for l in lines}
    # Body text: body-sized lines that are wide or start at a line-start shared with wide lines.
    # Labels inside a figure are usually short and start elsewhere, so they don't cut the band.
    big = [b for b in boxes if b.size >= 0.75 * size and id(b) not in cap_ids]
    col = (max((b.right for b in big), default=width) - min((b.left for b in big), default=0)) or width
    wide = [b for b in big if b.width >= 0.45 * col]
    starts, families = {round(b.left) for b in wide}, {b.family for b in wide}
    flow = wide + [b for b in big if b.width < 0.45 * col and b.family in families
                   and (b.size >= 0.95 * size or any(abs(b.left - s) <= 3 for s in starts))]
    side = cleft > width * 0.55  # Manning-style caption beside the figure
    top = max([b.bottom for b in flow if b.bottom <= ctop + 1] + [0])
    bottom = min([b.top for b in flow if b.top >= cbottom - 1] + [height])
    for l, lines in caps:  # neighbouring figures bound the band too
        if l != label:
            t, btm = min(x.top for x in lines), max(x.bottom for x in lines)
            if btm <= ctop:
                top = max(top, btm)
            elif t >= cbottom:
                bottom = min(bottom, t)
    below = not side and ctop - top > 3 * size
    if below:
        bottom = ctop - 1  # caption below the figure (O'Reilly style): keep only what is above it
    right = cleft - 2 if side else width
    with tempfile.TemporaryDirectory() as tmp:
        render(pdf, page, (0, top, right, bottom - top), TRIM_DPI, f"{tmp}/a", "pgm")
        w, h, _, px = read_pnm(f"{tmp}/a.pgm")
    blank = [(l.left - 1, l.top - top - 1, l.right + 1, l.bottom - top + 1) for _, lines in caps for l in lines]
    inked = [[xx for xx in range(w) if px[yy * w + xx] < INK
              and not any(a <= xx <= c and b <= yy <= d for a, b, c, d in blank)] for yy in range(h)]
    # Runs of inked rows separated by at least GAP points of white.
    GAP, JOIN = 8, 18
    segs: list[list[int]] = []
    for yy in range(h):
        if inked[yy]:
            if segs and yy - segs[-1][1] <= GAP:
                segs[-1][1] = yy
            else:
                segs.append([yy, yy])
    if not segs:
        raise SystemExit(f"Figure {label}: no ink found near the caption on PDF page {page}; pass --box")
    # Anchor on the run next to the caption, then take neighbours that sit close to it.
    if below:
        k = len(segs) - 1
    else:
        mid = (ctop + cbottom) / 2 - top
        k = min(range(len(segs)), key=lambda i: 0 if segs[i][0] <= mid <= segs[i][1]
                else min(abs(mid - segs[i][0]), abs(mid - segs[i][1])))
    lo = hi = k
    while lo > 0 and segs[lo][0] - segs[lo - 1][1] <= JOIN:
        lo -= 1
    while hi < len(segs) - 1 and segs[hi + 1][0] - segs[hi][1] <= JOIN:
        hi += 1
    y0, y1 = segs[lo][0], segs[hi][1]
    xs = [x for yy in range(y0, y1 + 1) for x in inked[yy][:1] + inked[yy][-1:]]
    x0, x1 = min(xs), max(xs)
    x0, x1 = max(0, x0 - PAD), min(right, x1 + PAD)
    y0, y1 = max(top, top + y0 - PAD), min(bottom, top + y1 + PAD)
    return (x0, y0, x1 - x0, y1 - y0)


def is_gray(pdf: str, page: int, box) -> bool:
    with tempfile.TemporaryDirectory() as tmp:
        render(pdf, page, box, TRIM_DPI, f"{tmp}/c", "ppm")
        _, _, _, px = read_pnm(f"{tmp}/c.ppm")
    return all(max(px[i:i + 3]) - min(px[i:i + 3]) < 24 for i in range(0, len(px) - 2, 3))


def file_for(label: str) -> str:
    a, _, b = re.split(r"([.-])", label, maxsplit=1) if re.search(r"[.-]", label) else ("", "", label)
    return f"{int(a):02d}-{int(b):02d}.png" if a else f"fig-{int(b):02d}.png"


def manifest(book: Path) -> dict[str, list[str]]:
    path = book / "figures" / "figures.tsv"
    rows = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines()[1:]:
            if line.strip():
                cells = line.split("\t")
                rows[cells[0]] = cells
    return rows


def save_manifest(book: Path, rows: dict[str, list[str]]) -> None:
    path = book / "figures" / "figures.tsv"
    head = "file\tlabel\tpdf_page\tbox_pt (x,y,w,h)\n"
    body = "".join("\t".join(r) + "\n" for _, r in sorted(rows.items()))
    path.write_text(head + body, encoding="utf-8")


def find_caption_page(pdf: str, label: str) -> int:
    cache = Path(tempfile.gettempdir()) / f"vault-{abs(hash((pdf, os.path.getmtime(pdf))))}.txt"
    if not cache.exists():
        subprocess.run(["pdftotext", pdf, str(cache)], check=True, capture_output=True)
    pages = cache.read_text(encoding="utf-8", errors="replace").split("\f")
    pat = re.compile(CAPTION_RE.format(label=re.escape(label)))
    for i, text in enumerate(pages, 1):
        if pat.search(text):
            if any(l == label for l, _ in captions(page_layout(pdf, i, i)[i][2])):
                return i
    raise SystemExit(f"Figure {label}: caption not found; pass --page and --box")


def figure(book: str, labels: list[str], page: int | None, box: str | None, name: str | None, redo: bool) -> None:
    folder = Path(book)
    pdf = str(folder / "book.pdf")
    (folder / "figures").mkdir(exist_ok=True)
    rows = manifest(folder)
    jobs = []
    if redo:
        jobs = [(r[0], r[1], int(r[2]), tuple(float(v) for v in r[3].split(","))) for r in rows.values()]
    for label in labels:
        p = page or find_caption_page(pdf, label)
        b = tuple(float(v) for v in box.split(",")) if box else detect_box(pdf, p, label, page_layout(pdf, p, p)[p])
        jobs.append((name or file_for(label), label, p, b))
    for file, label, p, b in jobs:
        out = folder / "figures" / file
        render(pdf, p, b, DPI, str(out.with_suffix("")), "gray-png" if is_gray(pdf, p, b) else "png")
        rows[file] = [file, label, str(p), ",".join(f"{v:.0f}" for v in b)]
        print(f"{out}  Figure {label}  PDF p. {p}  box {rows[file][3]}  {out.stat().st_size // 1024} KB")
    save_manifest(folder, rows)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    o = sub.add_parser("outline"); o.add_argument("pdf"); o.add_argument("--offset", type=int, default=0)
    t = sub.add_parser("text"); t.add_argument("pdf"); t.add_argument("out")
    f = sub.add_parser("find"); f.add_argument("txt"); f.add_argument("phrases", nargs="+")
    f.add_argument("--offset", type=int, default=0); f.add_argument("--pages")
    fl = sub.add_parser("figures"); fl.add_argument("book"); fl.add_argument("--offset", type=int, default=0)
    fl.add_argument("--pages")
    fg = sub.add_parser("figure"); fg.add_argument("book"); fg.add_argument("labels", nargs="*")
    fg.add_argument("--page", type=int); fg.add_argument("--box"); fg.add_argument("--name")
    fg.add_argument("--all", action="store_true")
    a = ap.parse_args()
    if a.cmd == "outline":
        outline(a.pdf, a.offset)
    elif a.cmd == "text":
        text(a.pdf, a.out)
    elif a.cmd == "figures":
        figures_list(a.book, a.offset, a.pages)
    elif a.cmd == "figure":
        figure(a.book, a.labels, a.page, a.box, a.name, a.all)
    else:
        return find(a.txt, a.offset, a.pages, a.phrases)
    return 0


if __name__ == "__main__":
    sys.exit(main())
