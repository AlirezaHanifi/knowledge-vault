/* Knowledge Vault — behaviour for generated pages: lesson slides, quizzes,
   embedded simulations, diagrams, and hub filters. Classic script; needs kit.js. */
(function () {
  "use strict";

  function isDark() {
    var t = document.documentElement.getAttribute("data-theme");
    return t === "dark"; /* light unless the reader chose dark */
  }
  function typing(t) {
    return t && (/^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName) || t.isContentEditable);
  }

  /* ---------- diagrams ---------- */

  var diagrams = {
    ready: false,
    init: function () {
      if (!window.mermaid) return;
      Array.prototype.forEach.call(document.querySelectorAll("pre.mermaid"), function (pre) {
        pre.setAttribute("data-src", pre.textContent);
      });
      this.configure();
      this.ready = true;
    },
    configure: function () {
      window.mermaid.initialize({
        startOnLoad: false, securityLevel: "strict", theme: isDark() ? "dark" : "neutral",
        fontFamily: getComputedStyle(document.body).fontFamily, flowchart: { htmlLabels: true }
      });
    },
    render: function (root) {
      if (!this.ready) return;
      var nodes = root.querySelectorAll("pre.mermaid:not([data-processed])");
      if (nodes.length) window.mermaid.run({ nodes: nodes }).catch(function (e) { console.warn(e); });
    },
    reset: function (visible) {
      if (!this.ready) return;
      this.configure();
      Array.prototype.forEach.call(document.querySelectorAll("pre.mermaid"), function (pre) {
        pre.removeAttribute("data-processed");
        pre.textContent = pre.getAttribute("data-src");
      });
      this.render(visible || document);
    }
  };

  /* ---------- lesson ---------- */

  function lesson() {
    var slides = Array.prototype.slice.call(document.querySelectorAll(".slide"));
    var links = Array.prototype.slice.call(document.querySelectorAll(".toc a[data-i]"));
    var toc = document.getElementById("toc");
    var toggle = document.querySelector(".toc-toggle");
    var bar = document.querySelector(".progress-bar");
    var count = document.querySelector(".deck-count");
    var prev = document.querySelector("[data-go='-1']");
    var next = document.querySelector("[data-go='1']");
    var deck = document.getElementById("main");
    var current = -1;

    var fa = document.documentElement.lang === "fa";
    function digits(n) { return fa ? String(n).replace(/[0-9]/g, function (d) { return "۰۱۲۳۴۵۶۷۸۹"[d]; }) : String(n); }
    function indexOf(id) {
      try { id = decodeURIComponent(id); } catch (e) { /* keep it as written */ }
      for (var i = 0; i < slides.length; i++) if (slides[i].id === id) return i;
      return -1;
    }
    function show(i, focus) {
      i = Math.max(0, Math.min(slides.length - 1, i));
      if (i === current) return;
      current = i;
      slides.forEach(function (s, k) { s.hidden = k !== i; });
      links.forEach(function (a, k) {
        if (k === i) a.setAttribute("aria-current", "step"); else a.removeAttribute("aria-current");
      });
      bar.style.width = ((i + 1) / slides.length * 100) + "%";
      count.textContent = digits(i + 1) + (fa ? " از " : " / ") + digits(slides.length);
      prev.disabled = i === 0;
      next.disabled = i === slides.length - 1;
      if (history.replaceState) history.replaceState(null, "", "#" + slides[i].id);
      window.scrollTo(0, 0);
      requestAnimationFrame(function () { window.scrollTo(0, 0); }); // after any native #hash jump
      diagrams.render(slides[i]);
      // Simulations load when their slide is first shown, then size themselves.
      Array.prototype.forEach.call(slides[i].querySelectorAll(".widget-frame iframe"), function (f) {
        if (!f.getAttribute("src")) f.setAttribute("src", f.getAttribute("data-src"));
        else measure(f);
      });
      if (focus) deck.focus({ preventScroll: true });
      var link = links[i];
      if (link && link.scrollIntoView && toc.scrollHeight > toc.clientHeight) link.scrollIntoView({ block: "nearest" });
    }
    function setToc(open) {
      toc.classList.toggle("open", open);
      toggle.setAttribute("aria-expanded", String(open));
    }

    prev.addEventListener("click", function () { show(current - 1, true); });
    next.addEventListener("click", function () { show(current + 1, true); });
    toggle.addEventListener("click", function () { setToc(!toc.classList.contains("open")); });
    links.forEach(function (a, k) {
      a.addEventListener("click", function (e) { e.preventDefault(); show(k, true); setToc(false); });
    });
    document.addEventListener("keydown", function (e) {
      if (e.metaKey || e.ctrlKey || e.altKey || typing(e.target)) return;
      var rtl = document.documentElement.dir === "rtl"; // in a right-to-left lesson, ← moves forward
      var fwd = rtl ? "ArrowLeft" : "ArrowRight", back = rtl ? "ArrowRight" : "ArrowLeft";
      if (e.key === fwd || e.key === "PageDown") { e.preventDefault(); show(current + 1, true); }
      else if (e.key === back || e.key === "PageUp") { e.preventDefault(); show(current - 1, true); }
      else if (e.key === "Escape") setToc(false);
    });
    window.addEventListener("hashchange", function () {
      var k = indexOf(location.hash.slice(1));
      if (k >= 0) show(k);
    });

    var start = indexOf(location.hash.slice(1));
    show(Math.max(start, 0));
  }

  /* ---------- quizzes ---------- */

  function quizzes() {
    Array.prototype.forEach.call(document.querySelectorAll(".mcq"), function (fs) {
      var answer = parseInt(fs.getAttribute("data-answer"), 10);
      var labels = Array.prototype.slice.call(fs.querySelectorAll("label"));
      var verdict = fs.querySelector(".verdict");
      fs.addEventListener("change", function (e) {
        var chosen = parseInt(e.target.value, 10);
        var right = chosen === answer;
        labels.forEach(function (l, k) {
          l.classList.toggle("right", k === answer);
          l.classList.toggle("wrong", k === chosen && !right);
        });
        verdict.hidden = false;
        verdict.className = "verdict " + (right ? "is-right" : "is-wrong");
        var fa = document.documentElement.lang === "fa";
        verdict.querySelector(".verdict-head").textContent = right ? (fa ? "درست است." : "Correct.")
          : (fa ? "نه کاملاً؛ گزینه‌ی مشخص‌شده درست است." : "Not quite — the highlighted answer is right.");
      });
    });
  }

  /* ---------- embedded simulations ---------- */

  var all = [];
  function sendTheme(f) {
    try { f.contentWindow.postMessage({ kvTheme: isDark() ? "dark" : "light" }, "*"); } catch (err) { /* not loaded */ }
  }
  function measure(f) {
    try { f.contentWindow.postMessage({ kvMeasure: true }, "*"); } catch (err) { /* not loaded */ }
  }
  function frames() {
    all = Array.prototype.slice.call(document.querySelectorAll(".widget-frame iframe"));
    window.addEventListener("message", function (e) {
      if (!e.data || typeof e.data.kvHeight !== "number") return;
      all.forEach(function (f) {
        if (f.contentWindow === e.source && e.data.kvHeight > 100) f.style.height = Math.ceil(e.data.kvHeight) + 8 + "px";
      });
    });
    // The kit reports height on its own; asking again on load covers a report sent before we listened.
    all.forEach(function (f) {
      f.addEventListener("load", function () { sendTheme(f); measure(f); });
    });
  }

  /* ---------- hubs ---------- */

  function hubs() {
    Array.prototype.forEach.call(document.querySelectorAll("[data-filter]"), function (input) {
      var rows = document.querySelectorAll(input.getAttribute("data-filter"));
      input.addEventListener("input", function () {
        var q = input.value.trim().toLowerCase();
        Array.prototype.forEach.call(rows, function (r) {
          r.hidden = q && r.textContent.toLowerCase().indexOf(q) < 0;
        });
      });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    diagrams.init();
    quizzes();
    frames();
    var isLesson = document.body.classList.contains("lesson");
    if (isLesson) lesson();
    else { hubs(); diagrams.render(document); }
    new MutationObserver(function () {
      all.forEach(sendTheme);
      diagrams.reset(isLesson ? document.querySelector(".slide:not([hidden])") : document);
    }).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
  });
})();
