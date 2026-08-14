#!/usr/bin/env python3
"""Build the accessibility scanner's page list from _site/sitemap.xml.

A hand-kept list drifts: new pages go unchecked, renamed ones 404 and the
scanner reports the error page as fine. Both had happened by August 2026.

You maintain pa11y.settings.json (the scanning rules). Not the page list.

    python3 scripts/build_pa11y_config.py   # after `jekyll build`
    → writes pa11yci.generated.json for pa11y-ci.
"""
# Website tooling, largely written by AI (Claude) and checked for behaviour
# rather than wording. It describes how the site is built, not how the lab works;
# lab policy lives in _guide/. See accessibility.md, "How this site is made".

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

# Built but absent from the sitemap. Visitors do land on 404s, so check it.
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
        # Only the path matters; we always scan the locally served copy.
        path = urlparse((loc.text or "").strip()).path or "/"
        # jekyll-sitemap also lists PDFs and similar, which a scanner can't read.
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

    # _comment is a note for whoever edits the settings; pa11y-ci shouldn't see it.
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
