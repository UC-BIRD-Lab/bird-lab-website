#!/usr/bin/env python3
"""Build the accessibility scanner's page list from the site's own sitemap.

WHY THIS EXISTS
    The list of pages to scan used to be typed by hand in pa11yci.json. That
    drifts: a new Lab Guide page gets written and nobody remembers to add it, so
    it is never checked; a page gets renamed and the old address stays in the
    list, where it quietly 404s and the scanner reports the error page as fine.
    Both had happened by August 2026.

    Jekyll already publishes a complete list of every page it built, in
    _site/sitemap.xml. Reading that means a new page is covered the moment it
    exists, and a deleted page disappears from the list on its own.

WHAT YOU MAINTAIN
    pa11y.settings.json — the scanning rules (standard, timeouts, and any
    deliberate exclusions, each with a reason). Not the page list.

USAGE
    python3 scripts/build_pa11y_config.py          # after `jekyll build`
    → writes pa11yci.generated.json, which the workflow passes to pa11y-ci.
"""

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

# Pages Jekyll builds but leaves out of the sitemap (it only lists indexable
# pages). The 404 page is a real page a visitor can land on, so it gets checked.
ALWAYS_INCLUDE = ["/404.html"]


def main():
    if not os.path.exists(SITEMAP):
        sys.exit(
            "Can't find _site/sitemap.xml — build the site first:\n"
            "  bundle exec jekyll build"
        )

    with open(SETTINGS, encoding="utf-8") as fh:
        settings = json.load(fh)

    excluded = {e["path"]: e.get("reason", "") for e in settings.pop("exclude", [])}

    tree = ET.parse(SITEMAP)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

    paths = []
    for loc in tree.getroot().findall(".//sm:url/sm:loc", ns):
        # The sitemap carries whatever host Jekyll was configured with; only the
        # path matters, since we always scan the locally served copy.
        path = urlparse((loc.text or "").strip()).path or "/"
        # jekyll-sitemap also lists non-HTML files it copied through (PDFs, for
        # instance). An accessibility scanner can only read web pages, so keep
        # directory-style URLs and .html files and drop the rest.
        if not (path.endswith("/") or path.endswith(".html")):
            continue
        paths.append(path)

    for extra in ALWAYS_INCLUDE:
        if extra not in paths:
            paths.append(extra)

    skipped = [p for p in paths if p in excluded]
    urls = [BASE + p for p in sorted(set(paths) - set(excluded))]

    if not urls:
        sys.exit("No pages found in the sitemap — refusing to write an empty scan list.")

    # Drop the _comment keys: they're notes for whoever edits the settings file,
    # and pa11y-ci shouldn't be handed configuration keys it doesn't understand.
    config = {k: v for k, v in settings.items() if not k.startswith("_")}
    config["urls"] = urls
    with open(OUTPUT, "w", encoding="utf-8") as fh:
        json.dump(config, fh, indent=2)
        fh.write("\n")

    print(f"Wrote {os.path.relpath(OUTPUT, REPO_ROOT)} with {len(urls)} pages to scan.")
    for path in skipped:
        print(f"  skipping {path} — {excluded[path]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
