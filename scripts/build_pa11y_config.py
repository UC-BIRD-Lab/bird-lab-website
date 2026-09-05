#!/usr/bin/env python3
"""Build pa11y-ci's page list (pa11yci.generated.json) from _site/sitemap.xml.

A hand-kept list drifts (unchecked new pages, renamed pages scanned as 404s).
Scanning rules stay in pa11y.settings.json.

    python3 scripts/build_pa11y_config.py   # after `jekyll build`
"""
# Site tooling, largely AI-written (Claude), checked for behaviour not wording.
# Lab policy lives in _guide/. See accessibility.md, "How this site is made".

import json
import os
import sys
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITEMAP = os.path.join(REPO_ROOT, "_site", "sitemap.xml")
SETTINGS = os.path.join(REPO_ROOT, "pa11y.settings.json")
OUTPUT = os.path.join(REPO_ROOT, "pa11yci.generated.json")

# Where the built site is served during the scan.
BASE = "http://localhost:4000"

# Built but not in the sitemap.
ALWAYS_INCLUDE = ["/404.html"]


def main():
    if not os.path.exists(SITEMAP):
        sys.exit(
            "Can't find _site/sitemap.xml. Build the site first:\n"
            "  bundle exec jekyll build"
        )

    with open(SETTINGS, encoding="utf-8") as fh:
        settings = json.load(fh)

    excluded = {e["path"]: e.get("reason", "") for e in settings.pop("exclude", [])}

    tree = ET.parse(SITEMAP)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

    paths = []
    for loc in tree.getroot().findall(".//sm:url/sm:loc", ns):
        path = urlparse((loc.text or "").strip()).path or "/"
        # The sitemap also lists PDFs, which pa11y can't read.
        if not (path.endswith("/") or path.endswith(".html")):
            continue
        paths.append(path)

    for extra in ALWAYS_INCLUDE:
        if extra not in paths:
            paths.append(extra)

    skipped = [p for p in paths if p in excluded]
    urls = [BASE + p for p in sorted(set(paths) - set(excluded))]

    if not urls:
        sys.exit("No pages found in the sitemap; refusing to write an empty scan list.")

    # _comment keys are notes for editors, not pa11y-ci.
    config = {k: v for k, v in settings.items() if not k.startswith("_")}
    config["urls"] = urls
    with open(OUTPUT, "w", encoding="utf-8") as fh:
        json.dump(config, fh, indent=2)
        fh.write("\n")

    print(f"Wrote {os.path.relpath(OUTPUT, REPO_ROOT)} with {len(urls)} pages to scan.")
    for path in skipped:
        print(f"  skipping {path}: {excluded[path]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
