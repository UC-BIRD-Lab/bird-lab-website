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
    var sections = Array.prototype.slice.call(document.querySelectorAll(".people-group"));
    var guideNoResults = document.getElementById("guide-noresults");
    guideSearch.addEventListener("input", function () {
      var q = guideSearch.value.toLowerCase().trim();
      cards.forEach(function (c) {
        var h = c.querySelector("h3");
        var inTitle = q && h && h.textContent.toLowerCase().indexOf(q) !== -1;
        var inText = q && c.textContent.toLowerCase().indexOf(q) !== -1;
        // Hide non-matches; keep any card whose title OR body matches.
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
      heroToggle.addEventListener("click", function () {
        if (heroVideo.paused) {
          heroVideo.play();
          setToggleState(true);
        } else {
          heroVideo.pause();
          setToggleState(false);
        }
      });
      heroVideo.addEventListener("play", function () { setToggleState(true); });
      heroVideo.addEventListener("pause", function () { setToggleState(false); });
    }
  }

  // ---- Wiki search (filters side nav + jumps) ----
  var wikiSearch = document.getElementById("wiki-search");
  if (wikiSearch) {
    var items = Array.prototype.slice.call(document.querySelectorAll(".wiki-side li"));
    wikiSearch.addEventListener("input", function () {
      var q = wikiSearch.value.toLowerCase().trim();
      items.forEach(function (li) {
        li.hidden = q && li.textContent.toLowerCase().indexOf(q) === -1;
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