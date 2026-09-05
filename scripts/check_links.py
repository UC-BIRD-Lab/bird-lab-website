#!/usr/bin/env python3
"""Check outbound links in _data/*.yml (DOIs, press/media URLs, pub_links extras).

Only 404/410 or a hard connection failure counts as broken; 403/429/503 are
reported as "couldn't verify" since publishers often block bots. Exits 1 only on
broken links, so CI opens an issue just then. Lab Guide prose links are lychee's job.

    python scripts/check_links.py [--out report.md]   # CI: link-rot-check.yml
"""
# Site tooling, largely AI-written (Claude), checked for behaviour not wording.
# Lab policy lives in _guide/. See accessibility.md, "How this site is made".
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
GONE = {404, 410}                       # the only codes counted as broken


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
    """De-duplicated (label, url) pairs; the label names the paper or story."""
    targets = {}

    def add(label, url):
        if url and str(url).startswith("http"):
            targets.setdefault(str(url).strip(), label)

    # Paper DOIs.
    for p in (load("publications.yml") or []):
        if isinstance(p, dict) and p.get("doi"):
            add("DOI · " + (p.get("title") or "")[:70], doi_url(p["doi"]))

    # Hand-maintained talks, posters, blogs.
    manual = load("publications_manual.yml")
    for section in ("conference", "journal", "blog"):
        for p in (manual.get(section) or []):
            if not isinstance(p, dict):
                continue
            if p.get("doi"):
                add("DOI · " + (p.get("title") or "")[:70], doi_url(p["doi"]))
            if p.get("url"):
                add("Link · " + (p.get("title") or "")[:70], p["url"])

    # Per-paper extras.
    for e in (load("pub_links.yml") or []):
        if not isinstance(e, dict):
            continue
        tag = (e.get("doi") or "")[:40]
        for field, name in (("data", "Data"), ("code", "Code"), ("preprint", "Preprint"),
                            ("pdf", "Open-access PDF"), ("correction", "Correction")):
            if e.get(field):
                add("%s · %s" % (name, tag), e[field])

    # Open-access links on publications.yml.
    for p in (load("publications.yml") or []):
        if isinstance(p, dict) and p.get("oa_url"):
            add("Open access · " + (p.get("title") or "")[:60], p["oa_url"])

    # Press (grouped by year) and media (flat list).
    for yr in (load("press.yml") or []):
        for it in (yr.get("items") or []) if isinstance(yr, dict) else []:
            add("Press · " + (it.get("source") or it.get("title") or "")[:60], it.get("url"))
    for it in (load("media.yml") or []):
        if isinstance(it, dict):
            add("Media · " + (it.get("source") or it.get("title") or "")[:60], it.get("url"))

    return sorted(((lbl, url) for url, lbl in targets.items()))


def check(url):
    """(status, detail); status is ok, broken or unverified."""
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, headers=HEADERS, method=method)
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                return "ok", "HTTP %s" % r.status
        except urllib.error.HTTPError as e:
            if e.code in GONE:
                return "broken", "HTTP %s (page gone)" % e.code
            if method == "HEAD" and e.code in (403, 405, 501):
                continue                       # retry with GET
            return "unverified", "HTTP %s (couldn't confirm; likely bot-blocked)" % e.code
        except urllib.error.URLError as e:
            reason = getattr(e, "reason", e)
            # DNS failure or refused = broken; timeouts are transient.
            text = str(reason).lower()
            if "name or service not known" in text or "nodename nor servname" in text \
                    or "no address associated" in text or "connection refused" in text:
                return "broken", "cannot reach host (%s)" % reason
            return "unverified", "network error (%s)" % reason
        except Exception as e:                 # noqa: BLE001
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

    lines = ["# Outbound link check", "",
             "Checked **%d** links: **%d** broken, **%d** couldn't be verified, "
             "**%d** OK." % (len(targets), len(broken), len(unverified),
                             len(targets) - len(broken) - len(unverified)), ""]
    if broken:
        lines += ["## ❌ Broken, please fix", ""]
        for label, url, detail in broken:
            lines.append("- **%s**: %s\n  - <%s>" % (label, detail, url))
        lines.append("")
    if unverified:
        lines += ["## ⚠️ Couldn't verify (often bot-blocked or a slow server; "
                  "worth a quick manual click, but usually fine)", ""]
        for label, url, detail in unverified:
            lines.append("- %s: %s\n  - <%s>" % (label, detail, url))
        lines.append("")
    if not broken and not unverified:
        lines += ["Everything resolved. 🎉", ""]
    report = "\n".join(lines)

    print(report)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(report)
        print("Wrote report to %s" % args.out, file=sys.stderr)

    return 1 if broken else 0


if __name__ == "__main__":
    raise SystemExit(main())
