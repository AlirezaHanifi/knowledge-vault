/* Knowledge Vault — interactive kit.
   A tiny set of helpers shared by every explorable. Classic script (no modules)
   so pages work when opened straight from disk. Exposes a single global: Kit. */
(function (global) {
  "use strict";

  /* ---------- DOM ---------- */

  // el("div", {class: "x", onclick: fn}, child, "text", [more children])
  function el(tag, attrs) {
    var node = document.createElement(tag);
    applyAttrs(node, attrs);
    appendChildren(node, Array.prototype.slice.call(arguments, 2));
    return node;
  }

  var SVG_NS = "http://www.w3.org/2000/svg";
  function svg(tag, attrs) {
    var node = document.createElementNS(SVG_NS, tag);
    applyAttrs(node, attrs);
    appendChildren(node, Array.prototype.slice.call(arguments, 2));
    return node;
  }

  function applyAttrs(node, attrs) {
    if (!attrs) return;
    Object.keys(attrs).forEach(function (k) {
      var v = attrs[k];
      if (v === null || v === undefined || v === false) return;
      if (k.slice(0, 2) === "on" && typeof v === "function") node.addEventListener(k.slice(2), v);
      else if (k === "text") node.textContent = v;
      else if (k === "html") node.innerHTML = v;
      else node.setAttribute(k, v === true ? "" : v);
    });
  }

  function appendChildren(node, children) {
    children.forEach(function (c) {
      if (c === null || c === undefined || c === false) return;
      if (Array.isArray(c)) appendChildren(node, c);
      else node.appendChild(typeof c === "object" ? c : document.createTextNode(String(c)));
    });
  }

  function $(sel, root) { return (root || document).querySelector(sel); }
  function clear(node) { while (node.firstChild) node.removeChild(node.firstChild); return node; }

  /* ---------- deterministic randomness ---------- */

  // Mulberry32: small, fast, good enough for teaching simulations.
  function rng(seed) {
    var a = seed >>> 0;
    function next() {
      a = (a + 0x6d2b79f5) >>> 0;
      var t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    }
    return {
      next: next,
      int: function (n) { return Math.floor(next() * n); },
      range: function (lo, hi) { return lo + next() * (hi - lo); },
      pick: function (arr) { return arr[Math.floor(next() * arr.length)]; },
      chance: function (p) { return next() < p; },
      // Exponential sample with the given mean (for latencies/arrivals).
      exp: function (mean) { return -Math.log(1 - next()) * mean; }
    };
  }

  /* ---------- reduced motion ---------- */

  function reducedMotion() {
    return !!(global.matchMedia && global.matchMedia("(prefers-reduced-motion: reduce)").matches);
  }

  /* ---------- event log (aria-live) ---------- */

  // log(listElement) -> { add(text, kind), clear() }; kind: ok | warn | bad | muted
  function log(list, opts) {
    opts = opts || {};
    list.classList.add("log");
    list.setAttribute("aria-live", "polite");
    list.setAttribute("aria-relevant", "additions");
    var max = opts.max || 200;
    return {
      add: function (text, kind) {
        var item = el("li", { class: kind || null }, text);
        list.appendChild(item);
        while (list.children.length > max) list.removeChild(list.firstChild);
        list.scrollTop = list.scrollHeight;
        return item;
      },
      clear: function () { clear(list); }
    };
  }

  /* ---------- player: play / pause / step / reset ---------- */

  // player({ mount, step: fn -> false when finished, reset: fn, interval: ms,
  //          speeds: [0.5,1,2] }) -> { play, pause, stepOnce, reset, playing }
  // Keyboard: Space = play/pause, → or "." = step, "r" = reset (when focus is
  // not inside a text field).
  function player(o) {
    var timer = null, speed = 1;
    var playBtn = el("button", { class: "btn primary", type: "button", "aria-label": "Play" }, "▶ Play");
    var stepBtn = el("button", { class: "btn", type: "button" }, "Step ›");
    var resetBtn = el("button", { class: "btn", type: "button" }, "↺ Reset");
    var speedSel = null;
    if (o.speeds !== false) {
      speedSel = el("select", { "aria-label": "Speed" },
        (o.speeds || [0.5, 1, 2, 4]).map(function (s) {
          return el("option", { value: s, selected: s === 1 }, s + "×");
        }));
      speedSel.addEventListener("change", function () {
        speed = parseFloat(speedSel.value);
        if (timer) { pause(); play(); }
      });
    }
    var bar = el("div", { class: "row", role: "group", "aria-label": "Simulation controls" },
      playBtn, stepBtn, resetBtn, speedSel);
    if (o.mount) o.mount.appendChild(bar);

    function tick() {
      if (o.step() === false) pause();
    }
    function play() {
      if (timer) return;
      playBtn.textContent = "❚❚ Pause";
      playBtn.setAttribute("aria-label", "Pause");
      timer = setInterval(tick, (o.interval || 700) / speed);
    }
    function pause() {
      clearInterval(timer); timer = null;
      playBtn.textContent = "▶ Play";
      playBtn.setAttribute("aria-label", "Play");
    }
    function stepOnce() { pause(); tick(); }
    function reset() { pause(); o.reset(); }

    playBtn.addEventListener("click", function () { timer ? pause() : play(); });
    stepBtn.addEventListener("click", stepOnce);
    resetBtn.addEventListener("click", reset);

    if (o.keyboard !== false) {
      document.addEventListener("keydown", function (e) {
        var t = e.target;
        if (t && (t.tagName === "INPUT" && t.type !== "range" && t.type !== "checkbox" || t.tagName === "TEXTAREA" || t.tagName === "SELECT")) return;
        if (e.metaKey || e.ctrlKey || e.altKey) return;
        if (e.key === " " && t.tagName !== "BUTTON") { e.preventDefault(); timer ? pause() : play(); }
        else if (e.key === "ArrowRight" || e.key === ".") { if (t.type !== "range") { e.preventDefault(); stepOnce(); } }
        else if (e.key === "r" || e.key === "R") { reset(); }
      });
    }
    return { play: play, pause: pause, stepOnce: stepOnce, reset: reset,
             playing: function () { return !!timer; }, element: bar };
  }

  /* ---------- labelled slider ---------- */

  var uid = 0;
  // slider({label, min, max, step, value, unit, hint, format, onInput}) -> {element, input, value()}
  function slider(o) {
    var id = "kit-s" + (++uid);
    var fmt = o.format || function (v) { return v + (o.unit || ""); };
    var out = el("output", { for: id }, fmt(o.value));
    var input = el("input", { type: "range", id: id, min: o.min, max: o.max, step: o.step || 1, value: o.value });
    input.addEventListener("input", function () {
      var v = parseFloat(input.value);
      out.textContent = fmt(v);
      if (o.onInput) o.onInput(v);
    });
    var wrap = el("div", { class: "field" },
      el("div", { class: "field-head" }, el("label", { for: id }, o.label), out),
      input,
      o.hint ? el("div", { class: "field-hint" }, o.hint) : null);
    return { element: wrap, input: input, value: function () { return parseFloat(input.value); },
             set: function (v) { input.value = v; out.textContent = fmt(v); } };
  }

  /* ---------- segmented control (single choice) ---------- */

  // segmented({label, options:[{value,label}], value, onChange}) -> {element, value()}
  function segmented(o) {
    var current = o.value;
    var buttons = o.options.map(function (opt) {
      var b = el("button", { type: "button", "aria-pressed": String(opt.value === current) }, opt.label);
      b.addEventListener("click", function () {
        current = opt.value;
        buttons.forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); });
        if (o.onChange) o.onChange(current);
      });
      return b;
    });
    var group = el("div", { class: "segmented", role: "group", "aria-label": o.label }, buttons);
    return { element: group, value: function () { return current; } };
  }

  /* ---------- tabs ---------- */

  // tabs(container) — container holds [role=tablist] with [role=tab][aria-controls]
  function tabs(container) {
    var list = container.querySelector("[role=tablist]");
    var all = Array.prototype.slice.call(list.querySelectorAll("[role=tab]"));
    function select(tab) {
      all.forEach(function (t) {
        var on = t === tab;
        t.setAttribute("aria-selected", String(on));
        t.tabIndex = on ? 0 : -1;
        document.getElementById(t.getAttribute("aria-controls")).hidden = !on;
      });
    }
    all.forEach(function (t, i) {
      t.addEventListener("click", function () { select(t); });
      t.addEventListener("keydown", function (e) {
        var d = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0;
        if (!d) return;
        var next = all[(i + d + all.length) % all.length];
        select(next); next.focus();
      });
    });
    select(all.filter(function (t) { return t.getAttribute("aria-selected") === "true"; })[0] || all[0]);
  }

  /* ---------- knowledge check ---------- */

  // quiz(mount, [{q, options:[...], answer: index, explain}])
  function quiz(mount, questions) {
    mount.classList.add("quiz");
    questions.forEach(function (item, qi) {
      var name = "kit-q" + (++uid);
      var verdict = el("div", { class: "verdict", "aria-live": "polite" });
      var labels = item.options.map(function (opt, oi) {
        var input = el("input", { type: "radio", name: name, value: oi });
        var label = el("label", null, input, el("span", null, opt));
        input.addEventListener("change", function () {
          labels.forEach(function (l) { l.classList.remove("right", "wrong"); });
          var right = oi === item.answer;
          label.classList.add(right ? "right" : "wrong");
          clear(verdict);
          verdict.appendChild(el("strong", null, right ? "Correct. " : "Not quite. "));
          verdict.appendChild(document.createTextNode(item.explain || ""));
        });
        return label;
      });
      mount.appendChild(el("fieldset", null, el("legend", null, (qi + 1) + ". " + item.q), labels, verdict));
    });
  }

  /* ---------- theme toggle ---------- */

  function themeToggle(mount) {
    var KEY = "kv-theme";
    var root = document.documentElement;
    function stored() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
    function save(v) { try { localStorage.setItem(KEY, v); } catch (e) { /* storage unavailable */ } }
    var initial = stored();
    if (initial) root.setAttribute("data-theme", initial);
    function isDark() {
      var t = root.getAttribute("data-theme");
      return t === "dark"; /* light unless the reader chose dark */
    }
    var btn = el("button", { class: "btn small", type: "button" });
    function label() { btn.textContent = isDark() ? "☀ Light" : "☾ Dark"; btn.setAttribute("aria-label", "Switch to " + (isDark() ? "light" : "dark") + " theme"); }
    btn.addEventListener("click", function () {
      var next = isDark() ? "light" : "dark";
      root.setAttribute("data-theme", next); save(next); label();
    });
    label();
    if (mount) mount.appendChild(btn);
    return btn;
  }

  /* ---------- line chart ---------- */

  // lineChart(svgElement, { width, height, xMax, yMax, xLabel, yLabel, xTicks, yTicks,
  //   series: [{ points: [[x, y], …], cls, label, dots }], bands: [{ from, to, label }],
  //   marks: [{ x, label }] }) — redraws the whole chart. Style via .chart-* classes
  // and series classes (s1…s5, ok, bad, warn) so both themes work.
  function lineChart(root, o) {
    var W = o.width || 520, H = o.height || 220, L = 44, R = 12, T = 12, B = 34;
    var xMax = o.xMax, yMax = o.yMax || 1, x0 = o.xMin || 0;
    function X(v) { return L + (v - x0) / (xMax - x0) * (W - L - R); }
    function Y(v) { return T + (1 - Math.min(v, yMax) / yMax) * (H - T - B); }
    clear(root);
    root.setAttribute("viewBox", "0 0 " + W + " " + H);
    root.classList.add("chart");
    (o.bands || []).forEach(function (b) {
      root.appendChild(svg("rect", { class: "chart-band", x: X(b.from), y: T, width: X(b.to) - X(b.from), height: H - T - B }));
      if (b.label) root.appendChild(svg("text", { class: "chart-note", x: X(b.from) + 4, y: T + 12 }, b.label));
    });
    var yt = o.yTicks || 4, xt = o.xTicks || 5;
    for (var i = 0; i <= yt; i++) {
      var yv = yMax * i / yt;
      root.appendChild(svg("line", { class: "chart-grid", x1: L, x2: W - R, y1: Y(yv), y2: Y(yv) }));
      root.appendChild(svg("text", { class: "chart-tick", x: L - 6, y: Y(yv) + 4, "text-anchor": "end" }, (o.yFormat || String)(yv)));
    }
    for (var j = 0; j <= xt; j++) {
      var xv = x0 + (xMax - x0) * j / xt;
      root.appendChild(svg("text", { class: "chart-tick", x: X(xv), y: H - B + 16, "text-anchor": "middle" }, (o.xFormat || String)(xv)));
    }
    root.appendChild(svg("line", { class: "chart-axis", x1: L, x2: W - R, y1: H - B, y2: H - B }));
    if (o.xLabel) root.appendChild(svg("text", { class: "chart-label", x: (L + W - R) / 2, y: H - 4, "text-anchor": "middle" }, o.xLabel));
    if (o.yLabel) root.appendChild(svg("text", { class: "chart-label", transform: "translate(11 " + (T + (H - T - B) / 2) + ") rotate(-90)", "text-anchor": "middle" }, o.yLabel));
    (o.series || []).forEach(function (s) {
      if (!s.points.length) return;
      var d = s.points.map(function (pt, k) { return (k ? "L" : "M") + X(pt[0]).toFixed(1) + " " + Y(pt[1]).toFixed(1); }).join(" ");
      root.appendChild(svg("path", { class: "chart-line " + (s.cls || "s1"), d: d }));
      if (s.dots) s.points.forEach(function (pt) { root.appendChild(svg("circle", { class: "chart-dot " + (s.cls || "s1"), cx: X(pt[0]), cy: Y(pt[1]), r: 2.5 })); });
    });
    (o.marks || []).forEach(function (m) {
      root.appendChild(svg("line", { class: "chart-mark", x1: X(m.x), x2: X(m.x), y1: T, y2: H - B }));
      if (m.label) root.appendChild(svg("text", { class: "chart-note", x: X(m.x) + 4, y: H - B - 6 }, m.label));
    });
    if (o.legend !== false && (o.series || []).some(function (s) { return s.label; })) {
      var lx = L + 8;
      (o.series || []).forEach(function (s) {
        if (!s.label) return;
        root.appendChild(svg("line", { class: "chart-line " + (s.cls || "s1"), x1: lx, x2: lx + 16, y1: T + 8, y2: T + 8 }));
        var t = svg("text", { class: "chart-tick", x: lx + 20, y: T + 12 }, s.label);
        root.appendChild(t);
        lx += 28 + s.label.length * 6.2;
      });
    }
    return { x: X, y: Y };
  }

  /* ---------- formatting ---------- */

  function fmtMs(v) { return v >= 1000 ? (v / 1000).toFixed(2) + " s" : Math.round(v) + " ms"; }
  function pct(v, digits) { return (v * 100).toFixed(digits === undefined ? 1 : digits) + "%"; }
  function percentile(sorted, p) {
    if (!sorted.length) return NaN;
    var i = Math.min(sorted.length - 1, Math.max(0, Math.ceil(p * sorted.length) - 1));
    return sorted[i];
  }

  /* ---------- embedding ---------- */

  // A page opened as "widget.html#embed" (inside a lesson) hides its own chrome
  // and reports its height so the lesson can size the iframe.
  var embedded = /(^|#|&)embed\b/.test(location.hash) && global.parent !== global;
  if (embedded) document.documentElement.classList.add("embed");
  function reportHeight() {
    global.parent.postMessage({ kvHeight: document.documentElement.scrollHeight }, "*");
  }

  // Auto-mount the theme toggle into any [data-kit-theme] slot.
  document.addEventListener("DOMContentLoaded", function () {
    var slot = document.querySelector("[data-kit-theme]");
    if (slot) themeToggle(slot);
    if (embedded) {
      reportHeight();
      if (global.ResizeObserver) new ResizeObserver(reportHeight).observe(document.body);
      global.addEventListener("load", reportHeight);
    }
  });
  // Follow the embedding lesson's theme.
  global.addEventListener("message", function (e) {
    if (e.data && e.data.kvTheme) document.documentElement.setAttribute("data-theme", e.data.kvTheme);
    if (e.data && e.data.kvMeasure && embedded) reportHeight();
  });

  global.Kit = {
    el: el, svg: svg, $: $, clear: clear, rng: rng, log: log, player: player,
    slider: slider, segmented: segmented, tabs: tabs, quiz: quiz, themeToggle: themeToggle, lineChart: lineChart,
    reducedMotion: reducedMotion, fmtMs: fmtMs, pct: pct, percentile: percentile
  };
})(window);
