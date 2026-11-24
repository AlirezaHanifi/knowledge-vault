/* Knowledge Vault — interactive kit.
   A tiny set of helpers shared by every explorable. Classic script (no modules)
   so pages work when opened straight from disk. Exposes a single global: Kit. */
(function (global) {
  "use strict";

  /* ---------- language ---------- */

  // A page written in Persian (<html lang="fa" dir="rtl">) gets Persian control
  // labels and Persian digits. t(en, fa) picks the string for the page language.
  var FA = document.documentElement.lang === "fa";
  function t(en, fa) { return FA ? fa : en; }
  var FA_DIGITS = "۰۱۲۳۴۵۶۷۸۹";
  // Persian digits for numbers in prose: digits glued to Latin letters (p99, S3,
  // 2PC, v1) stay as they are; decimal and thousands separators become ٫ and ٬.
  function digits(text) {
    if (!FA || text === null || text === undefined) return text;
    return String(text).replace(/[A-Za-z_]*[0-9][0-9.,]*[A-Za-z_]*/g, function (m) {
      if (/[A-Za-z_]/.test(m)) return m;
      return m.replace(/([0-9])\.(?=[0-9])/g, "$1٫").replace(/([0-9]),(?=[0-9]{3})/g, "$1٬")
              .replace(/[0-9]/g, function (d) { return FA_DIGITS[+d]; });
    });
  }
  // On a Persian page, every text node outside code, keyboard keys, .mono and
  // [lang=en] shows Persian digits, including text the simulation writes later.
  var SKIP = "code, kbd, pre, .mono, .kv, .chip, .diagram, .mermaid, [lang=en], script, style, textarea";
  function localizeNode(node) {
    if (node.nodeType === 3) {
      var p = node.parentElement;
      if (!p || (p.closest && p.closest(SKIP))) return;
      var v = digits(node.nodeValue);
      if (v !== node.nodeValue) node.nodeValue = v;
    } else if (node.nodeType === 1 && !(node.matches && node.matches(SKIP))) {
      for (var c = node.firstChild; c; c = c.nextSibling) localizeNode(c);
    }
  }
  if (FA && global.MutationObserver) {
    var observe = function () {
      localizeNode(document.body);
      new MutationObserver(function (list) {
        list.forEach(function (m) {
          if (m.type === "characterData") localizeNode(m.target);
          else Array.prototype.forEach.call(m.addedNodes, localizeNode);
        });
      }).observe(document.body, { subtree: true, childList: true, characterData: true });
    };
    if (document.body) observe(); else document.addEventListener("DOMContentLoaded", observe);
  }

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
    list.classList.add("kit-log");
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
    var PLAY = t("▶ Play", "▶ پخش"), PAUSE = t("❚❚ Pause", "❚❚ توقف");
    var playBtn = el("button", { class: "btn primary", type: "button", "aria-label": t("Play", "پخش") }, PLAY);
    var stepBtn = el("button", { class: "btn", type: "button" }, t("Step ›", "یک قدم ‹"));
    var resetBtn = el("button", { class: "btn", type: "button" }, t("↺ Reset", "↺ از اول"));
    var speedSel = null;
    if (o.speeds !== false) {
      speedSel = el("select", { "aria-label": t("Speed", "سرعت") },
        (o.speeds || [0.5, 1, 2, 4]).map(function (s) {
          return el("option", { value: s, selected: s === 1 }, s + "×");
        }));
      speedSel.addEventListener("change", function () {
        speed = parseFloat(speedSel.value);
        if (timer) { pause(); play(); }
      });
    }
    var bar = el("div", { class: "row", role: "group", "aria-label": t("Simulation controls", "کنترل‌های شبیه‌سازی") },
      playBtn, stepBtn, resetBtn, speedSel);
    if (o.mount) o.mount.appendChild(bar);

    function tick() {
      if (o.step() === false) pause();
    }
    function play() {
      if (timer) return;
      playBtn.textContent = PAUSE;
      playBtn.setAttribute("aria-label", t("Pause", "توقف"));
      timer = setInterval(tick, (o.interval || 700) / speed);
    }
    function pause() {
      clearInterval(timer); timer = null;
      playBtn.textContent = PLAY;
      playBtn.setAttribute("aria-label", t("Play", "پخش"));
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
        else if (e.key === (FA ? "ArrowLeft" : "ArrowRight") || e.key === ".") { if (t.type !== "range") { e.preventDefault(); stepOnce(); } }
        else if (e.key === "r" || e.key === "R") { reset(); }
      });
    }
    return { play: play, pause: pause, stepOnce: stepOnce, reset: reset,
             playing: function () { return !!timer; }, element: bar };
  }

  /* ---------- tour: a narrated scenario that plays on its own ---------- */

  // A stage page (body.stage-page) opens on a running scenario: each step changes
  // the model, redraws, and says in one caption what just happened. The reader can
  // pause, step back and forth, restart, or take over with the page's own controls.
  //
  // tour({ mount, steps: [{ say, run }], reset, render, interval, end })
  //   steps[i].run()  mutates the model (deterministic: replayed to step back)
  //   steps[i].say    caption, a string or a function returning one
  //   reset()         puts the model back to its opening state
  //   render()        redraws after every change
  //   end             caption shown after the last step (an invitation to tweak)
  // -> { play, pause, restart, goto(i), say(text, kind), free(text), playing() }
  // Starts playing ~0.7 s after load unless the reader prefers reduced motion.
  function tour(o) {
    // dirty: the reader changed the state by hand; playing again first replays the scenario to this step.
    var i = 0, timer = null, speed = 1, steps = o.steps, dirty = false;
    // Icons are inline SVG (crisp at any size); "dir" icons point the reading direction and flip in RTL.
    var ICONS = {
      play: "M7 4.5v15l12.5-7.5z", pause: "M6.5 4.5h4v15h-4zM13.5 4.5h4v15h-4z",
      prev: "M15 5l-7 7 7 7", next: "M9 5l7 7-7 7", restart: "M4.5 12a7.5 7.5 0 1 0 2.2-5.3M4.5 4.5v4h4"
    };
    function icon(name) {
      var filled = name === "play" || name === "pause";
      var e = svg("svg", { class: "ico" + (name === "prev" || name === "next" ? " ico-dir" : ""), viewBox: "0 0 24 24", width: 18, height: 18,
        "aria-hidden": "true", focusable: "false", fill: filled ? "currentColor" : "none", stroke: filled ? "none" : "currentColor",
        "stroke-width": 2.6, "stroke-linecap": "round", "stroke-linejoin": "round" });
      e.appendChild(svg("path", { d: ICONS[name] }));
      return e;
    }
    // "Next" carries its arrow after the word, so both arrows point outward from the play button.
    function label(btn, ic, txt) {
      clear(btn); var w = el("span", { class: "btn-label" }, txt);
      if (ic === "next") { btn.appendChild(w); btn.appendChild(icon(ic)); } else { btn.appendChild(icon(ic)); btn.appendChild(w); }
    }
    var count = el("span", { class: "tour-count" });
    var text = el("span", { class: "tour-text" });
    var caption = el("div", { class: "tour-caption", "aria-live": "polite" }, count, text);
    var playBtn = el("button", { class: "btn primary tour-play", type: "button" });
    var prevBtn = el("button", { class: "btn tour-step", type: "button", "aria-label": t("Previous step", "قدم قبلی") });
    var nextBtn = el("button", { class: "btn tour-step", type: "button", "aria-label": t("Next step", "قدم بعدی") });
    var restartBtn = el("button", { class: "btn icon-only", type: "button", title: t("Restart (R)", "از اول (R)"), "aria-label": t("Restart", "از اول") });
    label(prevBtn, "prev", t("Back", "قبلی")); label(nextBtn, "next", t("Next", "بعدی")); restartBtn.appendChild(icon("restart"));
    function setPlay(playing) {
      var ended = !playing && i >= steps.length;
      label(playBtn, playing ? "pause" : ended ? "restart" : "play", playing ? t("Pause", "توقف") : ended ? t("Replay", "پخش دوباره") : t("Play", "پخش"));
    }
    // Speed is a slider with four stops (0.5×, 1×, 1.5×, 2×), the current one shown beside it.
    var SPEEDS = [0.5, 1, 1.5, 2];
    function speedText(s) { return digits(String(s)) + "×"; }
    // The datalist draws a tick at each stop.
    var speedTicks = el("datalist", { id: "kit-speed-ticks" }, SPEEDS.map(function (_, k) { return el("option", { value: k }); }));
    var speedIn = el("input", { type: "range", min: 0, max: SPEEDS.length - 1, step: 1, value: 1, list: "kit-speed-ticks",
      "aria-label": t("Playback speed", "سرعت پخش"), "aria-valuetext": speedText(1) });
    var speedOut = el("output", { class: "tour-speed-val", "aria-hidden": "true" }, speedText(1));
    var speedSel = el("label", { class: "tour-speed", title: t("Playback speed", "سرعت پخش") },
      el("span", { class: "tour-speed-label" }, t("Speed", "سرعت")), speedIn, speedTicks, speedOut);
    // One dot per step: click to jump there. The current one fills while it waits for the next step.
    var dots = el("div", { class: "tour-dots" + (steps.length > 12 ? " tour-many" : ""), role: "group", "aria-label": t("Steps", "قدم‌ها") },
      steps.map(function (_, k) {
        var b = el("button", { class: "tour-dot", type: "button", title: t("Step ", "قدم ") + digits(k + 1),
          "aria-label": t("Go to step ", "رفتن به قدم ") + digits(k + 1) }, el("i"));
        b.addEventListener("click", function () { goto(k + 1); });
        return b;
      }));
    var endNote = el("p", { class: "tour-end", hidden: true });
    var transport = el("div", { class: "tour-transport" }, prevBtn, playBtn, nextBtn);
    var tools = el("div", { class: "tour-tools" }, restartBtn, speedSel);
    var bar = el("div", { class: "tour-bar", role: "group", "aria-label": t("Scenario controls", "کنترل‌های سناریو") },
      transport, dots, endNote, tools);
    // The "change it yourself" drawer: hidden at first so the reader sees the picture, the
    // caption and the numbers; opening it (or touching any control in it) pauses the scenario.
    var tweak = o.tweak, tweakBtn = null;
    if (tweak) {
      if (!tweak.id) tweak.id = "kit-tweak";
      tweak.hidden = true;
      tweakBtn = el("button", { class: "btn tweak-toggle", type: "button", "aria-expanded": "false", "aria-controls": tweak.id },
        t("🎛 Change it yourself", "🎛 خودتان تغییر بدهید"));
      tools.appendChild(tweakBtn);
      tweakBtn.addEventListener("click", function () { openTweak(tweak.hidden); });
      ["input", "click"].forEach(function (ev) {
        tweak.addEventListener(ev, function (e) {
          if (e.target === tweak || e.target === tweakBtn) return;
          if (/^(INPUT|SELECT|BUTTON)$/.test(e.target.tagName)) dirty = true;
          if (timer) pause();
        });
      });
    }
    function openTweak(open) {
      if (!tweak) return;
      tweak.hidden = !open;
      tweakBtn.setAttribute("aria-expanded", String(open));
      tweakBtn.classList.toggle("primary", open);
      if (open) { cancelAuto(); pause(); say(o.tweakIntro || t("Your turn: change something below and watch the picture and the numbers.",
        "نوبت شماست: چیزی را پایین عوض کنید و تصویر و عددها را ببینید."), "free"); }
      if (embedded) reportHeight();
    }
    if (o.mount) { o.mount.appendChild(caption); o.mount.appendChild(bar); }
    if (o.captionMount) o.captionMount.appendChild(caption);
    if (o.barMount) o.barMount.appendChild(bar);

    function sayStep(k) {
      var s = steps[k - 1];
      count.textContent = digits(k) + t(" of ", " از ") + digits(steps.length);
      count.hidden = false;
      text.textContent = digits(typeof s.say === "function" ? s.say() : s.say);
      caption.className = "tour-caption" + (s.kind ? " " + s.kind : "");
    }
    function update() {
      Array.prototype.forEach.call(dots.children, function (d, k) {
        // Namespaced state classes: widgets have their own .now / .done styles.
        d.className = "tour-dot" + (k < i - 1 ? " tour-done" : k === i - 1 ? " tour-now" : "");
        if (k === i - 1) d.setAttribute("aria-current", "step"); else d.removeAttribute("aria-current");
      });
      prevBtn.disabled = i === 0;
      nextBtn.disabled = i >= steps.length;
      // The last step keeps its caption; the "what next" invitation shows beside the dots.
      var ended = i >= steps.length && !timer;
      endNote.hidden = !ended;
      endNote.textContent = ended ? digits(o.end || t("End of the scenario.", "سناریو تمام شد.")) : "";
      endNote.title = endNote.textContent;
      bar.classList.toggle("tour-ended", ended);
      setPlay(!!timer);
    }
    // The current dot fills over the time the step stays up while playing.
    function runFill(ms) {
      var d = dots.children[i - 1];
      Array.prototype.forEach.call(dots.children, function (x) { x.classList.remove("tour-run"); });
      if (!d || !ms) return;
      d.style.setProperty("--dwell", ms + "ms");
      void d.offsetWidth;
      d.classList.add("tour-run");
    }
    function apply(k) { steps[k].run(); }
    function forward() {
      if (i >= steps.length) { pause(); return false; }
      apply(i); i++;
      o.render(); sayStep(i); update();
      return true;
    }
    function goto(k) {
      pause(); dirty = false;
      k = Math.max(0, Math.min(steps.length, k));
      o.reset();
      for (i = 0; i < k; i++) apply(i);
      o.render();
      if (k) sayStep(k); else say(o.intro || t("Press Play to watch the scenario.", "برای دیدن سناریو «پخش» را بزنید."));
      update();
    }
    function say(msg, kind) {
      count.hidden = true;
      text.textContent = digits(msg);
      caption.className = "tour-caption" + (kind ? " " + kind : "");
    }
    // Each step stays up long enough to read its caption: at least o.interval, more for long text.
    function dwell() {
      var len = text.textContent.length;
      return Math.max(o.interval || 2600, 1400 + len * 38) / speed;
    }
    // While playing, every step, the last included, stays up for its full dwell before moving on.
    function schedule() {
      var ms = dwell();
      runFill(i ? ms : 0);
      timer = setTimeout(function () { if (forward() && timer) schedule(); }, ms);
    }
    function play() {
      cancelAuto();
      if (timer) return;
      if (i >= steps.length) goto(0);
      else if (dirty) goto(i);
      timer = true; setPlay(true);
      if (i === 0) forward();
      if (timer) schedule();
    }
    function pause() {
      cancelAuto(); clearTimeout(timer); timer = null; hiddenPause = false;
      runFill(0); update();
    }
    playBtn.addEventListener("click", function () { timer ? pause() : play(); });
    prevBtn.addEventListener("click", function () { goto(i - 1); });
    nextBtn.addEventListener("click", function () { if (dirty) goto(i); else pause(); forward(); });
    restartBtn.addEventListener("click", function () { goto(0); play(); });
    speedIn.addEventListener("input", function () {
      speed = SPEEDS[+speedIn.value] || 1;
      speedOut.textContent = speedText(speed);
      speedIn.setAttribute("aria-valuetext", speedText(speed));
      if (timer) { clearTimeout(timer); timer = true; schedule(); }
    });
    document.addEventListener("keydown", function (e) {
      var tg = e.target;
      if (o.keys === false) return;
      if (tg && (tg.tagName === "INPUT" && tg.type !== "range" && tg.type !== "checkbox" || tg.tagName === "TEXTAREA" || tg.tagName === "SELECT")) return;
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      // Arrow keys on a focused slider move the slider, not the scenario.
      if (tg && tg.type === "range" && /^Arrow/.test(e.key)) return;
      if (e.key === " " && tg.tagName !== "BUTTON") { e.preventDefault(); timer ? pause() : play(); }
      else if (e.key === (FA ? "ArrowLeft" : "ArrowRight") || e.key === ".") { e.preventDefault(); if (!nextBtn.disabled) nextBtn.click(); }
      else if (e.key === (FA ? "ArrowRight" : "ArrowLeft") || e.key === ",") { e.preventDefault(); goto(i - 1); }
      else if (e.key === "r" || e.key === "R") { goto(0); play(); }
    });
    // Pause while the page is hidden (another tab, or the lesson moved to another slide).
    var hiddenPause = false;
    document.addEventListener("visibilitychange", function () {
      if (document.hidden && timer) { pause(); hiddenPause = true; }
      else if (!document.hidden && hiddenPause) { hiddenPause = false; play(); }
    });
    global.addEventListener("message", function (e) { if (e.data && e.data.kvPause) pause(); });

    // Autoplay starts shortly after load, unless the reader has already taken a control.
    var auto = null;
    function cancelAuto() { clearTimeout(auto); auto = null; }
    goto(0);
    if (o.autoplay !== false && !reducedMotion()) auto = setTimeout(function () { auto = null; play(); }, 700);
    return {
      play: play, pause: pause, restart: function () { goto(0); play(); }, goto: goto,
      // The reader took over: stop the scenario and narrate what they did instead.
      say: say, free: function (msg, kind) { pause(); dirty = true; if (msg) say(msg, kind); }, tweak: openTweak,
      playing: function () { return !!timer; }, step: function () { return i; }
    };
  }

  /* ---------- lens map: one pipeline seen through several lenses ---------- */

  // lensMap({scene, captionMount, barMount, tweak, stages: [{id, zone, name}],
  //          lenses: {key: {label, axis: [low, high], cells: {stageId: {tag, level 0–4, pages, slide, text}}}},
  //          lesson: "../chapters/NN-….html#"})
  // The scenario walks every stage under every lens; the reader can switch lens or pick a stage.
  function lensMap(o) {
    var keys = Object.keys(o.lenses), lens = keys[0], current = o.stages[0].id, tr;
    var head = el("div", { class: "lm-head" });
    var pipe = el("div", { class: "lm-pipe", role: "group", "aria-label": t("Pipeline stages", "مرحله‌های pipeline") });
    var foot = el("p", { class: "lm-foot" });
    o.scene.appendChild(head); o.scene.appendChild(pipe); o.scene.appendChild(foot);
    function stage(id) { return o.stages.filter(function (x) { return x.id === id; })[0]; }
    function story(k, id) {
      var L = o.lenses[k], c = L.cells[id];
      return L.label + " · " + stage(id).name + ": " + c.tag + ". " + c.text;
    }
    function meter(level, axis) {
      var bars = [];
      for (var i = 0; i < 5; i++) bars.push(el("i", { class: i <= level ? "on" : "" }));
      return el("div", { class: "lm-meter", role: "img",
        "aria-label": digits((level + 1) + t(" of 5 toward ", " از ۵ به سمت ")) + axis[1] }, bars);
    }
    function render() {
      var L = o.lenses[lens], c = L.cells[current];
      clear(head);
      head.appendChild(el("span", { class: "lm-lens" }, L.label));
      head.appendChild(el("span", { class: "lm-axis" }, el("b", null, "▮"), " " + L.axis[0]));
      head.appendChild(el("span", { class: "lm-axis" }, el("b", null, "▮▮▮▮▮"), " " + L.axis[1]));
      clear(pipe);
      o.stages.forEach(function (s) {
        var cell = L.cells[s.id];
        pipe.appendChild(el("button", { type: "button", class: "lm-stage", "aria-pressed": String(s.id === current),
          onclick: function () { current = s.id; render(); if (tr) tr.free(story(lens, current)); } },
          el("span", { class: "lm-zone" }, s.zone), el("span", { class: "lm-name" }, s.name),
          meter(cell.level, L.axis), el("span", { class: "lm-tag" }, cell.tag)));
      });
      clear(foot).appendChild(document.createTextNode(t("In the book: ", "در کتاب: ") + c.pages + " · "));
      foot.appendChild(el("a", { href: o.lesson + c.slide, target: "_top" }, t("open this slide in the lesson", "همین اسلاید را در درس باز کنید")));
      if (seg) seg.set(lens);
    }
    var seg = null;
    if (o.tweak) {
      seg = segmented({ label: "lens", value: lens,
        options: keys.map(function (k) { return { value: k, label: o.lenses[k].label }; }),
        onChange: function (v) { lens = v; render(); tr.free(story(lens, current)); } });
      o.tweak.appendChild(el("p", { class: "panel-title" }, t("Lens", "lens")));
      o.tweak.appendChild(seg.element);
      o.tweak.appendChild(el("p", { class: "lm-hint" }, t("Click any stage in the pipeline to read it under this lens.",
        "روی هر مرحله‌ی pipeline کلیک کنید تا با همین lens توضیحش را بخوانید.")));
    }
    var steps = [];
    keys.forEach(function (k) {
      o.stages.forEach(function (s) {
        steps.push({ say: function () { return story(k, s.id); }, run: function () { lens = k; current = s.id; } });
      });
    });
    tr = tour({ captionMount: o.captionMount, barMount: o.barMount, tweak: o.tweak, steps: steps, render: render,
      reset: function () { lens = keys[0]; current = o.stages[0].id; }, interval: 4000,
      intro: o.intro || t("The scenario walks the pipeline stage by stage under each lens.", "سناریو pipeline را با هر lens مرحله‌به‌مرحله طی می‌کند."),
      end: o.end || t("That was every lens. Open “Change it yourself” to switch lens, or click any stage.",
        "همه‌ی lensها را دیدید. «خودتان تغییر بدهید» را باز کنید تا lens را عوض کنید، یا روی هر مرحله کلیک کنید.") });
    return tr;
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
    function set(v) {
      current = v;
      buttons.forEach(function (x, k) { x.setAttribute("aria-pressed", String(o.options[k].value === v)); });
    }
    return { element: group, value: function () { return current; }, set: set };
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
        if (FA) d = -d;
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
          verdict.appendChild(el("strong", null, right ? t("Correct. ", "درست است. ") : t("Not quite. ", "نه دقیقاً. ")));
          verdict.appendChild(document.createTextNode(item.explain || ""));
        });
        return label;
      });
      mount.appendChild(el("fieldset", null, el("legend", null, digits(qi + 1) + ". " + item.q), labels, verdict));
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
    function label() {
      var fa = FA;
      btn.textContent = isDark() ? (fa ? "☀ روشن" : "☀ Light") : (fa ? "☾ تیره" : "☾ Dark");
      btn.setAttribute("aria-label", fa ? (isDark() ? "رفتن به تم روشن" : "رفتن به تم تیره")
                                        : "Switch to " + (isDark() ? "light" : "dark") + " theme");
    }
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
    var W = o.width || 520, H = o.height || 220, R = 12, T = 12;
    var xMax = o.xMax, yMax = o.yMax || 1, x0 = o.xMin || 0;
    var yt = o.yTicks || 4, xt = o.xTicks || 5;
    clear(root);
    root.setAttribute("viewBox", "0 0 " + W + " " + H);
    root.classList.add("chart");
    // Margins follow the rendered text, so ticks never run into the axis titles at the
    // kit's minimum font size: the y ticks' widest label sets the left margin.
    function textWidth(str, cls) {
      var t = svg("text", { class: cls, x: 0, y: -100 }, str), w = 0;
      root.appendChild(t);
      try { w = t.getComputedTextLength(); } catch (e) { /* not rendered */ }
      root.removeChild(t);
      return w || String(str).length * 7.5;
    }
    var tickW = 0;
    for (var a = 0; a <= yt; a++) tickW = Math.max(tickW, textWidth((o.yFormat || String)(yMax * a / yt), "chart-tick"));
    var L = Math.max(44, Math.ceil(tickW) + 10 + (o.yLabel ? 22 : 0)), B = o.xLabel ? 44 : 28;
    function X(v) { return L + (v - x0) / (xMax - x0) * (W - L - R); }
    function Y(v) { return T + (1 - Math.min(v, yMax) / yMax) * (H - T - B); }
    (o.bands || []).forEach(function (b) {
      root.appendChild(svg("rect", { class: "chart-band", x: X(b.from), y: T, width: X(b.to) - X(b.from), height: H - T - B }));
      if (b.label) root.appendChild(svg("text", { class: "chart-note", x: X(b.from) + 4, y: T + 28 }, b.label));
    });
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
    // Mark labels sit just above the axis; one that would touch an earlier label moves up a row.
    var placed = [];
    (o.marks || []).forEach(function (m) {
      root.appendChild(svg("line", { class: "chart-mark", x1: X(m.x), x2: X(m.x), y1: T, y2: H - B }));
      if (!m.label) return;
      var x = X(m.x) + 4, w = textWidth(m.label, "chart-note"), row = 0;
      if (x + w > W - R) x = X(m.x) - 4 - w;
      while (placed.some(function (p) { return p.row === row && x < p.x + p.w + 6 && p.x < x + w + 6; })) row++;
      placed.push({ x: x, w: w, row: row });
      root.appendChild(svg("text", { class: "chart-note", x: x, y: H - B - 6 - row * 16 }, m.label));
    });
    if (o.legend !== false && (o.series || []).some(function (s) { return s.label; })) {
      var lx = L + 8;
      (o.series || []).forEach(function (s) {
        if (!s.label) return;
        root.appendChild(svg("line", { class: "chart-line " + (s.cls || "s1"), x1: lx, x2: lx + 16, y1: T + 8, y2: T + 8 }));
        var t = svg("text", { class: "chart-tick chart-legend", x: lx + 20, y: T + 12 }, s.label);
        root.appendChild(t);
        var w = 0;
        try { w = t.getComputedTextLength(); } catch (e) { /* not rendered yet */ }
        lx += 28 + (w || s.label.length * 6.2);
      });
    }
    return { x: X, y: Y };
  }

  /* ---------- formatting ---------- */

  function fmtMs(v) { return v >= 1000 ? (v / 1000).toFixed(2) + " s" : Math.round(v) + " ms"; }
  function pct(v, places) { return (v * 100).toFixed(places === undefined ? 1 : places) + (FA ? "٪" : "%"); }
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
  // A stage page (body.stage-page) wide enough for its side-by-side layout asks the
  // lesson to give it the whole slide instead of growing to its content height.
  function stageFill() {
    return document.body && document.body.classList.contains("stage-page") && global.innerWidth >= 640;
  }
  // The least height a stage needs: caption, numbers and bar at their own size, and the
  // scene row at least SCENE_MIN tall (less if its content is shorter) and tall enough for
  // the open controls beside it. Opening the controls never squeezes the picture.
  var SCENE_MIN = 280;
  function stageNeed() {
    var st = document.querySelector(".sim-stage"), scene = st && st.querySelector(".stage-scene");
    if (!scene) return 0;
    var gap = parseFloat(getComputedStyle(st).rowGap) || 0, need = 0, rows = 0;
    ["stage-caption", "stage-side", "stage-bar"].forEach(function (c) {
      var n = st.querySelector("." + c);
      if (n && n.offsetHeight) { need += n.offsetHeight; rows++; }
    });
    var tweak = st.querySelector(".stage-tweak");
    var row = Math.max(Math.min(scene.scrollHeight, SCENE_MIN), tweak && !tweak.hidden ? contentHeight(tweak) : 0);
    return need + row + rows * gap + 8;
  }
  // The height a box's children need, not its stretched height: scrollHeight never drops below
  // clientHeight, so reporting it for a stretched drawer would grow the frame on every report.
  function contentHeight(box) {
    var kids = box.children, cs = getComputedStyle(box);
    if (!kids.length) return 0;
    var top = Infinity, bottom = -Infinity;
    Array.prototype.forEach.call(kids, function (k) {
      if (!k.offsetHeight) return;
      var r = k.getBoundingClientRect(); top = Math.min(top, r.top); bottom = Math.max(bottom, r.bottom);
    });
    if (top === Infinity) return 0;
    return bottom - top + ["paddingTop", "paddingBottom", "borderTopWidth", "borderBottomWidth"].reduce(function (n, p) { return n + (parseFloat(cs[p]) || 0); }, 0);
  }
  function reportHeight() {
    var fill = stageFill();
    document.documentElement.classList.toggle("stage-fill", fill);
    global.parent.postMessage({ kvStage: fill, kvHeight: fill ? stageNeed() : document.documentElement.scrollHeight }, "*");
  }

  // Auto-mount the theme toggle into any [data-kit-theme] slot.
  document.addEventListener("DOMContentLoaded", function () {
    var slot = document.querySelector("[data-kit-theme]");
    if (slot) themeToggle(slot);
    if (embedded) {
      reportHeight();
      if (global.ResizeObserver) new ResizeObserver(reportHeight).observe(document.body);
      global.addEventListener("load", reportHeight);
      global.addEventListener("resize", reportHeight);
    }
  });
  // Follow the embedding lesson's theme.
  global.addEventListener("message", function (e) {
    if (e.data && e.data.kvTheme) document.documentElement.setAttribute("data-theme", e.data.kvTheme);
    if (e.data && e.data.kvMeasure && embedded) reportHeight();
  });

  global.Kit = {
    el: el, svg: svg, $: $, clear: clear, rng: rng, log: log, player: player, tour: tour, lensMap: lensMap,
    slider: slider, segmented: segmented, tabs: tabs, quiz: quiz, themeToggle: themeToggle, lineChart: lineChart,
    reducedMotion: reducedMotion, fmtMs: fmtMs, t: t, fa: FA, digits: digits, pct: pct, percentile: percentile
  };
})(window);
