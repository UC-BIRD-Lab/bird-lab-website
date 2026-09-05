/* BIRD Lab site behaviour. Progressive enhancement; the site works without JS. */
(function () {
  "use strict";

  // ---- Mobile nav toggle ----
  var toggle = document.querySelector(".nav__toggle");
  var links = document.getElementById("nav-links");
  if (toggle && links) {
    toggle.addEventListener("click", function () {
      var open = links.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    links.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        links.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  // ---- Publications filter (search + type) ----
  var pubSearch = document.getElementById("pub-search");
  var pubType = document.getElementById("pub-type");
  if (pubSearch || pubType) {
    var pubs = Array.prototype.slice.call(document.querySelectorAll(".pub"));
    var years = Array.prototype.slice.call(document.querySelectorAll(".pub-year"));
    function filterPubs() {
      var q = (pubSearch && pubSearch.value || "").toLowerCase().trim();
      var t = (pubType && pubType.value) || "all";
      pubs.forEach(function (el) {
        var text = el.getAttribute("data-search") || el.textContent.toLowerCase();
        var type = el.getAttribute("data-type") || "";
        var show = (!q || text.indexOf(q) !== -1) && (t === "all" || type === t);
        el.hidden = !show;
      });
      // Hide year headings with no visible pubs.
      years.forEach(function (h) {
        var sib = h.nextElementSibling, any = false;
        while (sib && !sib.classList.contains("pub-year")) {
          if (sib.classList.contains("pub") && !sib.hidden) { any = true; break; }
          sib = sib.nextElementSibling;
        }
        h.hidden = !any;
      });
      var noRes = document.getElementById("pub-noresults");
      if (noRes) noRes.hidden = pubs.some(function (p) { return !p.hidden; });
    }
    if (pubSearch) pubSearch.addEventListener("input", filterPubs);
    if (pubType) pubType.addEventListener("change", filterPubs);
  }

  // ---- Lab Guide hub: filter + rank cards (title matches before body-only) ----
  var guideSearch = document.getElementById("guide-search");
  if (guideSearch) {
    var cards = Array.prototype.slice.call(document.querySelectorAll(".card--link"));
    // Card sections; empty ones hide while searching.
    var sections = Array.prototype.slice.call(document.querySelectorAll(".guide-start, .guide-cat"));
    var guideNoResults = document.getElementById("guide-noresults");
    // .is-searching hides the journey panel and category chips (CSS).
    var guideHub = guideSearch.closest(".guide-hub-top");
    guideSearch.addEventListener("input", function () {
      var q = guideSearch.value.toLowerCase().trim();
      if (guideHub) guideHub.classList.toggle("is-searching", !!q);
      cards.forEach(function (c) {
        var h = c.querySelector("h3");
        var kw = (c.getAttribute("data-keywords") || "").toLowerCase();
        var inTitle = q && h && h.textContent.toLowerCase().indexOf(q) !== -1;
        var inText = q && (c.textContent.toLowerCase().indexOf(q) !== -1 || kw.indexOf(q) !== -1);
        c.hidden = !!q && !inText;
        // Title matches rank above body-only matches.
        c.style.order = q ? (inTitle ? "0" : "1") : "";
      });
      var anyVisible = false;
      sections.forEach(function (s) {
        var visible = s.querySelectorAll(".card--link:not([hidden])").length;
        s.hidden = q && visible === 0;
        if (visible) anyVisible = true;
      });
      if (guideNoResults) guideNoResults.hidden = !(q && !anyVisible);
    });
  }

  // ---- Fellowships table: preview rows, reveal the rest on demand (JS off: all rows, no button) ----
  document.querySelectorAll(".fund-toggle").forEach(function (btn) {
    var table = document.getElementById(btn.getAttribute("data-target"));
    if (!table) return;
    var rows = Array.prototype.slice.call(table.querySelectorAll("tbody tr"));
    var preview = parseInt(btn.getAttribute("data-preview"), 10) || 6;
    if (rows.length <= preview) return;
    var collapsed = true;
    function apply() {
      rows.forEach(function (r, i) { r.hidden = collapsed && i >= preview; });
      btn.innerHTML = collapsed
        ? ("Show all " + rows.length + " fellowships ↓")
        : "Show fewer ↑";
      btn.setAttribute("aria-expanded", collapsed ? "false" : "true");
    }
    btn.hidden = false;
    apply();
    btn.addEventListener("click", function () { collapsed = !collapsed; apply(); });
  });

  // ---- Hero video pause/play (WCAG 2.2.2) ----
  // Under prefers-reduced-motion the CSS hides the video, so pause it and hide the button.
  var heroVideo = document.querySelector(".hero .section-bg");
  var heroToggle = document.querySelector(".video-toggle");
  if (heroVideo && heroToggle) {
    var reduceMotion = window.matchMedia
      && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    function setToggleState(playing) {
      heroToggle.setAttribute("aria-pressed", playing ? "false" : "true");
      heroToggle.setAttribute(
        "aria-label", playing ? "Pause background video" : "Play background video");
      heroToggle.classList.toggle("is-paused", !playing);
    }

    if (reduceMotion) {
      try { heroVideo.pause(); } catch (e) {}
      heroToggle.hidden = true;
    } else {
      setToggleState(!heroVideo.paused);
      var userPaused = false;   // set only by the visitor's toggle click
      heroToggle.addEventListener("click", function () {
        if (heroVideo.paused) {
          userPaused = false;
          heroVideo.play();
          setToggleState(true);
        } else {
          userPaused = true;
          heroVideo.pause();
          setToggleState(false);
        }
      });
      heroVideo.addEventListener("play", function () { setToggleState(true); });
      heroVideo.addEventListener("pause", function () { setToggleState(false); });

      // Mobile browsers may ignore autoplay (Low Power Mode, data saver): nudge once now
      // and once on first touch. Never overrides the visitor's own pause.
      function nudgePlay() {
        if (!heroVideo.paused || userPaused) return;
        var p = heroVideo.play();
        if (p && p.catch) p.catch(function () {});
      }
      nudgePlay();
      document.addEventListener("touchstart", function onFirstTouch() {
        document.removeEventListener("touchstart", onFirstTouch);
        nudgePlay();
      }, { passive: true });
    }
  }

  // ---- Wiki sidebar fold ----
  // The <details> ships open (no-JS fallback); closed below 820px, reopened if the window widens.
  var wikiFold = document.querySelector(".wiki-fold");
  if (wikiFold && window.matchMedia) {
    var foldMq = window.matchMedia("(max-width: 820px)");
    function syncWikiFold() { wikiFold.open = !foldMq.matches; }
    syncWikiFold();
    if (foldMq.addEventListener) foldMq.addEventListener("change", syncWikiFold);
    else if (foldMq.addListener) foldMq.addListener(syncWikiFold);
  }

  // ---- Print: open every collapsed <details>, restore afterwards ----
  // CSS cannot force a closed <details> to render, so folds would print empty.
  var printOpened = [];
  function expandFoldsForPrint() {
    printOpened = [];
    document.querySelectorAll("details:not([open])").forEach(function (d) {
      printOpened.push(d);
      d.open = true;
    });
  }
  function restoreFoldsAfterPrint() {
    printOpened.forEach(function (d) { d.open = false; });
    printOpened = [];
  }
  window.addEventListener("beforeprint", expandFoldsForPrint);
  window.addEventListener("afterprint", restoreFoldsAfterPrint);
  // Safari fires no beforeprint/afterprint; use the print media query.
  if (window.matchMedia) {
    var printMq = window.matchMedia("print");
    var onPrintChange = function (mq) {
      if (mq.matches) expandFoldsForPrint(); else restoreFoldsAfterPrint();
    };
    if (printMq.addEventListener) printMq.addEventListener("change", onPrintChange);
    else if (printMq.addListener) printMq.addListener(onPrintChange);
  }

  // ---- Wiki search (filters the side nav) ----
  var wikiSearch = document.getElementById("wiki-search");
  if (wikiSearch) {
    var items = Array.prototype.slice.call(document.querySelectorAll(".wiki-nav li"));
    wikiSearch.addEventListener("input", function () {
      var q = wikiSearch.value.toLowerCase().trim();
      items.forEach(function (li) {
        var kw = (li.getAttribute("data-keywords") || "").toLowerCase();
        var text = li.textContent.toLowerCase();
        li.hidden = q && text.indexOf(q) === -1 && kw.indexOf(q) === -1;
      });
    });
  }
})();

// ---- People: legend chips highlight and count matching members ----
(function () {
  var teamGrid = document.getElementById("team-grid");
  if (!teamGrid) return;

  document.querySelectorAll(".role-chip").forEach(function (chip) {
    var role = chip.dataset.role;
    var cards = teamGrid.querySelectorAll('.person[data-role="' + role + '"]');
    var pips  = teamGrid.querySelectorAll('.role-pip[data-role="' + role + '"]');

    var count = chip.querySelector(".role-count");
    if (count) count.textContent = cards.length;   // shown even when 0

    function set(active) {
      teamGrid.classList.toggle("filtering", active);
      chip.classList.toggle("active", active);
      cards.forEach(function (c) { c.classList.toggle("highlight", active); });
      pips.forEach(function (b) { b.classList.toggle("highlight", active); });
    }

    chip.addEventListener("mouseenter", function () { set(true); });
    chip.addEventListener("mouseleave", function () { set(false); });
    chip.addEventListener("focusin",  function () { set(true); });
    chip.addEventListener("focusout", function () { set(false); });
  });
})();

// ---- Lab Guide: copy-link button on each H2/H3 with an id (kramdown generates ids) ----
(function () {
  var article = document.querySelector(".wiki-content");
  if (!article) return;

  article.querySelectorAll("h2[id], h3[id]").forEach(function (h) {
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "anchor-link";
    btn.setAttribute("aria-label", "Copy link to this section");
    btn.title = "Copy link to this section";
    btn.innerHTML = "<span aria-hidden=\"true\">#</span>";

    btn.addEventListener("click", function () {
      var url = location.origin + location.pathname + "#" + h.id;
      var done = function () {
        btn.classList.add("copied");
        var live = document.getElementById("anchor-live");
        if (live) live.textContent = "Section link copied";
        setTimeout(function () { btn.classList.remove("copied"); }, 1600);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(done, function () {
          location.hash = h.id; done();
        });
      } else {
        location.hash = h.id; done();
      }
    });

    h.appendChild(btn);
  });

  // Live region for the "copied" confirmation.
  var live = document.createElement("div");
  live.id = "anchor-live";
  live.className = "visually-hidden";
  live.setAttribute("aria-live", "polite");
  article.appendChild(live);
})();

/* ---- Announcement bar (_includes/announcement-banner.html) ----
   Removes the bar once the deadline passes (the site only rebuilds on push) and lets visitors
   dismiss it for the session. The dismissal key includes the deadline so a new announcement shows again. */
(function () {
  "use strict";
  var bar = document.querySelector(".announce");
  if (!bar) return;

  var deadline = bar.getAttribute("data-deadline") || "";
  if (deadline) {
    // Visible through the deadline day (local time).
    var end = new Date(deadline + "T23:59:59");
    if (!isNaN(end.getTime()) && new Date() > end) { bar.remove(); return; }
  }

  var key = "birdlab-announce-dismissed-" + (deadline || "current");
  try {
    if (sessionStorage.getItem(key) === "1") { bar.remove(); return; }
  } catch (e) { /* private mode: dismissal lasts one page */ }

  var close = bar.querySelector(".announce__close");
  if (close) {
    close.addEventListener("click", function () {
      try { sessionStorage.setItem(key, "1"); } catch (e) {}
      bar.remove();
    });
  }
})();

/* ---- People: open the alumni <details> when linked to #alumni ---- */
(function () {
  "use strict";
  var box = document.querySelector("#alumni .alumni-details");
  if (!box) return;

  function openIfTargeted() {
    if (location.hash !== "#alumni") return;
    if (!box.open) {
      box.open = true;
      // Opening the list shifts the page; re-scroll to the heading.
      var head = document.getElementById("alumni");
      if (head) head.scrollIntoView();
    }
  }

  openIfTargeted();
  window.addEventListener("hashchange", openIfTargeted);
})();
