/* BIRD Lab — progressive enhancement. Site works without JS. */
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

  // ---- Publications filter (search + year + type) ----
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
      // hide empty year headings
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
    // Sections that hold guide cards: the "Start here" block and each category
    // band. Empty ones hide while the visitor is searching.
    var sections = Array.prototype.slice.call(document.querySelectorAll(".guide-start, .guide-cat"));
    var guideNoResults = document.getElementById("guide-noresults");
    guideSearch.addEventListener("input", function () {
      var q = guideSearch.value.toLowerCase().trim();
      cards.forEach(function (c) {
        var h = c.querySelector("h3");
        var kw = (c.getAttribute("data-keywords") || "").toLowerCase();
        var inTitle = q && h && h.textContent.toLowerCase().indexOf(q) !== -1;
        var inText = q && (c.textContent.toLowerCase().indexOf(q) !== -1 || kw.indexOf(q) !== -1);
        // Hide non-matches; keep any card whose title, body, OR keywords match.
        c.hidden = !!q && !inText;
        // Rank: title matches (order 0) rise above body-only matches (order 1).
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

  // ---- Fellowships table: show a preview, reveal the rest on demand ----
  // Progressive enhancement: with JS off, every row (and no button) shows.
  document.querySelectorAll(".fund-toggle").forEach(function (btn) {
    var table = document.getElementById(btn.getAttribute("data-target"));
    if (!table) return;
    var rows = Array.prototype.slice.call(table.querySelectorAll("tbody tr"));
    var preview = parseInt(btn.getAttribute("data-preview"), 10) || 6;
    if (rows.length <= preview) return;              // nothing to collapse
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

  // ---- Hero background video: pause/play control (WCAG 2.2.2) ----
  // The control lets anyone stop motion that lasts >5s. We also respect the
  // OS "reduce motion" setting: there the CSS hides the video, so we pause it
  // and hide the button (nothing is moving to control).
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
      var userPaused = false;   // set only by the visitor's own toggle click
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

      // Mobile browsers sometimes ignore the autoplay attribute (Low Power
      // Mode, data saver). Nudge playback once now and once on first touch;
      // if the browser still refuses, the poster + play button remain the
      // fallback. Never fights an explicit pause from the visitor.
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

  // ---- Wiki sidebar fold (small screens) ----
  // The sidebar's <details> ships open (no-JS fallback and desktop). Below
  // 820px it starts collapsed so the article isn't pushed down the page, and
  // it reopens automatically if the window widens past the breakpoint.
  var wikiFold = document.querySelector(".wiki-fold");
  if (wikiFold && window.matchMedia) {
    var foldMq = window.matchMedia("(max-width: 820px)");
    function syncWikiFold() { wikiFold.open = !foldMq.matches; }
    syncWikiFold();
    if (foldMq.addEventListener) foldMq.addEventListener("change", syncWikiFold);
    else if (foldMq.addListener) foldMq.addListener(syncWikiFold);
  }

  // ---- Wiki search (filters side nav + jumps) ----
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

// ---- People page: legend chips highlight (and count) matching members ----
(function () {
  var teamGrid = document.getElementById("team-grid");
  if (!teamGrid) return;                       // only on the People page

  document.querySelectorAll(".role-chip").forEach(function (chip) {
    var role = chip.dataset.role;
    var cards = teamGrid.querySelectorAll('.person[data-role="' + role + '"]');
    var pips  = teamGrid.querySelectorAll('.role-pip[data-role="' + role + '"]');

    // Count members of this role, once.
    var count = chip.querySelector(".role-count");
    if (count) count.textContent = cards.length;   // always show, including 0

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

// ---- Lab Guide: copyable section links ----
// Adds a small "link" affordance to each H2/H3 in a guide page that has an id
// (kramdown auto-generates these). Click copies the section's full URL to the
// clipboard so members can paste a deep link straight into Slack or a PR. Purely
// an enhancement: the headings and their anchors work with JS off.
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

  // One polite live region for the "copied" confirmation.
  var live = document.createElement("div");
  live.id = "anchor-live";
  live.className = "visually-hidden";
  live.setAttribute("aria-live", "polite");
  article.appendChild(live);
})();
