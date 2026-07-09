#!/usr/bin/env python3
"""
check_links.py: an annual health check for the OUTBOUND links the site depends on,
the ones GitHub can't see are broken — every paper DOI, every "In the news" press
and media URL, and the data/code/preprint/open-access links attached to papers.

WHY a dedicated checker (not just the lychee guide sweep): these live in the data
files (_data/*.yml), point at publishers and news sites that quietly move or delete
pages, and are the links a visitor is most disappointed to find dead. This reads the
YAML directly, so the report says exactly which paper or story a dead link belongs to.

SAFE / low-false-alarm by design:
  * Only a "gone" verdict (HTTP 404/410) or a hard connection/DNS failure counts as
    BROKEN. Publishers and news sites routinely answer bots with 403/429/503; those
    are reported as "couldn't verify" (a heads-up), never as broken, so the yearly
    issue doesn't cry wolf.
  * Sends a real browser User-Agent and follows redirects (DOIs are 302s to the
    publisher). Tries HEAD first, falls back to GET when a server dislikes HEAD.
  * Read-only: it never edits your files. It writes a Markdown report and exits 1
    only when something is truly broken (so CI can open an issue on that).

Run locally:   python scripts/check_links.py                 # report to the console
               python scripts/check_links.py --out report.md # ...and/or to a file
In CI:         see .github/workflows/link-rot-check.yml
"""
from __future__ import annotations
import argparse
import concurrent.futures
import os
import sys
import urllib.error
import urllib.request

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install -r scripts/requirements.txt")

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(REPO_ROOT, "_data")

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
HEADERS = {"User-Agent": UA, "Accept": "*/*", "Accept-Language": "en-US,en;q=0.9"}
TIMEOUT = 30
GONE = {404, 410}                       # the only codes we treat as "broken"


def load(name):
    path = os.path.join(DATA, name)
    try:
        with open(path, encoding="utf-8") as fh:
            return yaml.safe_load(fh) or {}
    except FileNotFoundError:
        return {}


def doi_url(doi):
    if not doi:
        return ""
    d = str(doi).strip()
    if d.startswith("http"):
        return d
    return "https://doi.org/" + d.lstrip("/")


def collect_targets():
    """Return a de-duplicated list of (label, url). Label says what the link is for,
    so the report is actionable ('DOI · <title>', 'Press · <source>', …)."""
    targets = {}

    def add(label, url):
        if url and str(url).startswith("http"):
            targets.setdefault(str(url).strip(), label)

    # Paper DOIs (auto-synced journal/conference articles).
    for p in (load("publications.yml") or []):
        if isinstance(p, dict) and p.get("doi"):
            add("DOI · " + (p.get("title") or "")[:70], doi_url(p["doi"]))

    # Hand-maintained talks/posters/blogs (some carry a doi or a url).
    manual = load("publications_manual.yml")
    for section in ("conference", "journal", "blog"):
        for p in (manual.get(section) or []):
            if not isinstance(p, dict):
                continue
            if p.get("doi"):
                add("DOI · " + (p.get("title") or "")[:70], doi_url(p["doi"]))
            if p.get("url"):
                add("Link · " + (p.get("title") or "")[:70], p["url"])

    # Per-paper resources: data / code / preprint / open-access PDF / correction.
    for e in (load("pub_links.yml") or []):
        if not isinstance(e, dict):
            continue
        tag = (e.get("doi") or "")[:40]
        for field, name in (("data", "Data"), ("code", "Code"), ("preprint", "Preprint"),
                            ("pdf", "Open-access PDF"), ("correction", "Correction")):
            if e.get(field):
                add("%s · %s" % (name, tag), e[field])

    # Open-access links auto-filled onto publications.yml (checked with the papers).
    for p in (load("publications.yml") or []):
        if isinstance(p, dict) and p.get("oa_url"):
            add("Open access · " + (p.get("title") or "")[:60], p["oa_url"])

    # "In the news" — written press (grouped by year) and media (flat list).
    for yr in (load("press.yml") or []):
        for it in (yr.get("items") or []) if isinstance(yr, dict) else []:
            add("Press · " + (it.get("source") or it.get("title") or "")[:60], it.get("url"))
    for it in (load("media.yml") or []):
        if isinstance(it, dict):
            add("Media · " + (it.get("source") or it.get("title") or "")[:60], it.get("url"))

    return sorted(((lbl, url) for url, lbl in targets.items()))


def check(url):
    """Return (status, detail). status ∈ {'ok','broken','unverified'}."""
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, headers=HEADERS, method=method)
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                return "ok", "HTTP %s" % r.status
        except urllib.error.HTTPError as e:
            if e.code in GONE:
                return "broken", "HTTP %s (page gone)" % e.code
            if method == "HEAD" and e.code in (403, 405, 501):
                continue                       # server dislikes HEAD → retry with GET
            return "unverified", "HTTP %s (couldn't confirm; likely bot-blocked)" % e.code
        except urllib.error.URLError as e:
            reason = getattr(e, "reason", e)
            # DNS failure / refused / no route = genuinely broken; timeouts are transient.
            text = str(reason).lower()
            if "name or service not known" in text or "nodename nor servname" in text \
                    or "no address associated" in text or "connection refused" in text:
                return "broken", "cannot reach host (%s)" % reason
            return "unverified", "network error (%s)" % reason
        except Exception as e:                 # noqa: BLE001 — never crash the sweep
            return "unverified", "error (%s)" % e
    return "unverified", "no response"


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check the site's outbound DOI/press links.")
    ap.add_argument("--out", default="", help="Also write the Markdown report to this file.")
    ap.add_argument("--workers", type=int, default=8, help="Parallel requests (default 8).")
    args = ap.parse_args(argv)

    targets = collect_targets()
    print("Checking %d outbound links…" % len(targets), file=sys.stderr)

    broken, unverified = [], []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = pool.map(lambda t: (t[0], t[1], check(t[1])), targets)
        for label, url, (status, detail) in results:
            if status == "broken":
                broken.append((label, url, detail))
            elif status == "unverified":
                unverified.append((label, url, detail))

    # ── Markdown report ──
    lines = ["# Outbound link check", "",
             "Checked **%d** links: **%d** broken, **%d** couldn't be verified, "
             "**%d** OK." % (len(targets), len(broken), len(unverified),
                             len(targets) - len(broken) - len(unverified)), ""]
    if broken:
        lines += ["## ❌ Broken — please fix", ""]
        for label, url, detail in broken:
            lines.append("- **%s** — %s\n  - <%s>" % (label, detail, url))
        lines.append("")
    if unverified:
        lines += ["## ⚠️ Couldn't verify (often bot-blocked or a slow server; "
                  "worth a quick manual click, but usually fine)", ""]
        for label, url, detail in unverified:
            lines.append("- %s — %s\n  - <%s>" % (label, detail, url))
        lines.append("")
    if not broken and not unverified:
        lines += ["Everything resolved. 🎉", ""]
    report = "\n".join(lines)

    print(report)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(report)
        print("Wrote report to %s" % args.out, file=sys.stderr)

    # Exit non-zero ONLY on genuinely broken links, so CI opens an issue just then.
    return 1 if broken else 0


if __name__ == "__main__":
    raise SystemExit(main())
