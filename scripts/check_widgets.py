#!/usr/bin/env python3
"""Drive every widget in a headless browser and report what a reader would hit.

For each books/*/widgets/*.html, at 1280×800 with reduced motion (no autoplay):

  1. load the page, then visit every tour step (the step dots), in order;
  2. open the «change it yourself» drawer and work every control in it once:
     each select option, each segmented/radio choice, each checkbox, a range at
     its minimum and maximum, each plain button;
  3. after every action check for
       - errors:   uncaught exceptions and console errors;
                   horizontal page scroll;
                   two SVG <text> labels drawn over each other;
                   the picture (.stage-scene) scrolling either way;
       - warnings: the stage screen taller than 800px;
                   text clipped by its own box (overflow hidden, content wider).

The pages stay dependency-free; this check is the one place a browser engine is
needed, so it runs in CI only (see .github/workflows/validate.yml):

    pip install playwright && python -m playwright install chromium
    python3 scripts/check_widgets.py [--chrome] [--shots DIR] [book-slug | widget path ...]

--chrome uses the installed Google Chrome instead of Playwright's Chromium;
--shots DIR saves a screenshot of every action that showed a new error.
Exits 1 when any error is found; warnings alone keep exit 0.
"""
from __future__ import annotations

import functools
import http.server
import sys
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
W, H = 1280, 800

# Runs in the page after every action; returns the problems it sees right now.
PROBE = r"""
() => {
  const out = [], de = document.documentElement;
  const shown = e => { const r = e.getBoundingClientRect(); if (!r.width || !r.height) return null;
    for (let n = e; n && n.nodeType === 1; n = n.parentNode) { const s = getComputedStyle(n);
      if (s.display === "none" || s.visibility === "hidden" || +s.opacity === 0) return null; }
    return r; };
  const label = e => (e.textContent || "").trim().replace(/\s+/g, " ").slice(0, 40);
  if (de.scrollWidth > innerWidth + 1) out.push(["error", `horizontal scroll: page is ${de.scrollWidth}px wide`]);
  // A stage page's first screen (title, picture, numbers, controls) must fit the viewport;
  // the notes below it (.stage-more) may scroll. The picture itself must not scroll.
  const screen = document.querySelector(".stage-screen"), scene = document.querySelector(".stage-scene");
  if (screen && screen.getBoundingClientRect().bottom > innerHeight + 1)
    out.push(["warn", `stage taller than the screen: ends at ${Math.round(screen.getBoundingClientRect().bottom)}px`]);
  if (scene && scene.scrollWidth > scene.clientWidth + 1) {
    // Name the innermost element that sticks out, so the fix starts in the right place.
    const box = scene.getBoundingClientRect(), pad = parseFloat(getComputedStyle(scene).paddingLeft) || 0;
    let worst = null;
    for (const e of scene.querySelectorAll("*")) {
      if (e.closest("svg") && e.tagName !== "svg") continue;
      const r = e.getBoundingClientRect();
      if (r.width && (r.right > box.right - pad + 1 || r.left < box.left + pad - 1)) worst = e;
    }
    const what = worst ? `${worst.tagName.toLowerCase()}${worst.className && typeof worst.className === "string" ? "." + worst.className.trim().split(/\s+/).join(".") : ""} «${label(worst)}»` : "";
    out.push(["error", `picture scrolls sideways: ${scene.scrollWidth}px in ${scene.clientWidth}px ${what}`.trim()]);
  }
  if (scene && scene.scrollHeight > scene.clientHeight + 1) out.push(["error", `picture scrolls: ${scene.scrollHeight}px in ${scene.clientHeight}px`]);
  // SVG labels: any two visible <text> in one <svg> whose glyphs overlap. A text box spans the
  // font's whole ascent and descent (tall for Vazirmatn), so two stacked lines would "touch";
  // compare the middle half of each box, where the letters are drawn.
  const ink = r => ({ left: r.left, right: r.right, top: r.top + r.height / 4, bottom: r.bottom - r.height / 4 });
  for (const svg of document.querySelectorAll("svg")) {
    const ts = [...svg.querySelectorAll("text")].map(e => [e, shown(e)]).filter(x => x[1] && label(x[0])).map(x => [x[0], ink(x[1])]);
    for (let a = 0; a < ts.length; a++) for (let b = a + 1; b < ts.length; b++) {
      const r = ts[a][1], q = ts[b][1];
      const dx = Math.min(r.right, q.right) - Math.max(r.left, q.left);
      const dy = Math.min(r.bottom, q.bottom) - Math.max(r.top, q.top);
      if (dx > 2 && dy > 2) out.push(["error", `SVG labels overlap: «${label(ts[a][0])}» / «${label(ts[b][0])}»`]);
    }
  }
  // HTML text clipped by its own box.
  for (const e of document.querySelectorAll("body *")) {
    if (e.closest("svg") || !e.childNodes.length || ![...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) continue;
    const s = getComputedStyle(e);
    if (!/hidden|clip/.test(s.overflowX) || s.textOverflow === "ellipsis" || !shown(e)) continue;
    if (e.scrollWidth > e.clientWidth + 1) out.push(["warn", `clipped text: «${label(e)}»`]);
  }
  return out;
}
"""

# Lists the drawer's controls as [kind, index, values]; actions find them again by index.
CONTROLS = r"""
() => {
  const tw = document.querySelector(".tweak-toggle");
  const box = tw && document.getElementById(tw.getAttribute("aria-controls"));
  if (!box) return [];
  return [...box.querySelectorAll("input, select, button")].map((e, i) => {
    if (e.disabled) return null;
    if (e.tagName === "SELECT") return ["select", i, [...e.options].map(o => o.value)];
    if (e.type === "range") return ["range", i, [e.min || "0", e.max || "100"]];
    if (e.type === "checkbox" || e.type === "radio") return [e.type, i, []];
    if (e.tagName === "BUTTON") return ["button", i, []];
    if (e.type === "number") return ["number", i, [e.min || "0", e.max || e.value]];
    return null;
  }).filter(Boolean);
}
"""

ACT = r"""
([kind, i, v]) => {
  const tw = document.querySelector(".tweak-toggle");
  const e = document.getElementById(tw.getAttribute("aria-controls")).querySelectorAll("input, select, button")[i];
  if (!e || e.disabled) return;
  if (kind === "button" || kind === "checkbox" || kind === "radio") { e.click(); return; }
  e.value = v;
  e.dispatchEvent(new Event("input", { bubbles: true }));
  e.dispatchEvent(new Event("change", { bubbles: true }));
}
"""


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args) -> None:
        pass


def serve() -> str:
    handler = functools.partial(Quiet, directory=str(ROOT))
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return f"http://127.0.0.1:{srv.server_address[1]}"


def widgets(args: list[str]) -> list[Path]:
    every = sorted(ROOT.glob("books/*/widgets/*.html"))
    if not args:
        return every
    picked = []
    for a in args:
        p = (ROOT / a).resolve()
        picked += [p] if p.is_file() else [w for w in every if w.parts[-3] == a]
    return picked


def check(page, url: str, shots: Path | None = None) -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    where = ["load"]

    def note(kind: str, msg: str) -> None:
        item = (kind, f"{where[0]}: {msg}")
        if item not in found:
            found.append(item)

    page.on("pageerror", lambda e: note("error", f"exception: {e}"))
    # The browser asks every new origin for /favicon.ico; widgets have none and need none.
    page.on("console", lambda m: m.type == "error" and not m.location.get("url", "").endswith("/favicon.ico")
            and note("error", f"console: {m.text}"))

    def probe() -> None:
        page.wait_for_timeout(60)
        before = sum(k == "error" for k, _ in found)
        for kind, msg in page.evaluate(PROBE):
            note(kind, msg)
        errors = sum(k == "error" for k, _ in found)
        if shots and errors > before:  # one picture per action that showed a new error
            # Let the picture spill for the shot (outlined), so what it hid is in the picture too.
            page.evaluate("s => { const e = document.querySelector(s); if (e) { e.dataset.ov = e.style.overflow;"
                          " e.style.overflow = 'visible'; e.style.outline = '2px solid red'; } }", ".stage-scene")
            page.screenshot(path=str(shots / f"{Path(url).stem}-{errors:02d}.png"), full_page=True)
            page.evaluate("s => { const e = document.querySelector(s); if (e) { e.style.overflow = e.dataset.ov;"
                          " e.style.outline = ''; } }", ".stage-scene")

    page.goto(url)
    page.wait_for_load_state("load")
    probe()
    dots = page.locator(".tour-dot")
    for k in range(dots.count()):
        where[0] = f"step {k + 1}"
        dots.nth(k).click()
        probe()
    toggle = page.locator(".tweak-toggle")
    if toggle.count():
        where[0] = "drawer"
        toggle.first.click()
        probe()
        for kind, i, values in page.evaluate(CONTROLS):
            for v in values or [None]:
                where[0] = f"drawer {kind} #{i}" + (f" = {v}" if v is not None else "")
                page.evaluate(ACT, [kind, i, v])
                probe()
    return found


def main() -> int:
    argv = sys.argv[1:]
    shots = None
    if "--shots" in argv:
        k = argv.index("--shots")
        shots = Path(argv[k + 1]).resolve()
        shots.mkdir(parents=True, exist_ok=True)
        del argv[k:k + 2]
    args = [a for a in argv if not a.startswith("--")]
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("check_widgets.py needs Playwright: pip install playwright && python -m playwright install chromium")
        return 2
    base, errors, warns = serve(), 0, 0
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel="chrome" if "--chrome" in sys.argv else None)
        ctx = browser.new_context(viewport={"width": W, "height": H}, reduced_motion="reduce")
        files = widgets(args)
        for w in files:
            page = ctx.new_page()
            rel = w.relative_to(ROOT).as_posix()
            try:
                found = check(page, f"{base}/{rel}", shots)
            except Exception as e:  # a hung or broken page is itself a finding
                found = [("error", f"check failed: {e}")]
            page.close()
            for kind, msg in found:
                print(f"  {kind}: {rel}: {msg}")
            errors += sum(k == "error" for k, _ in found)
            warns += sum(k == "warn" for k, _ in found)
        browser.close()
    print(f"Widgets: {len(files)} checked, {errors} error(s), {warns} warning(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
