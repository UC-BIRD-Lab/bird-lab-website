#!/usr/bin/env python3
"""
Update _data/publications.yml from OpenAlex, keyed on the PI's ORCID.

Why OpenAlex? It exposes a free, well-documented, key-less API that resolves an
author's works by ORCID and returns clean, structured metadata (title, authors,
venue, year, DOI). Google Scholar has no official API and actively blocks
scraping, so it is unsuitable for an automated, reliable pipeline.

Design choices that make this SAFE to run unattended:
  * The committed YAML is the source of truth. If the API is unreachable or
    returns nothing, we exit WITHOUT modifying the file (never destructive).
  * We only ADD journal articles whose DOI is not already present, so any manual
    corrections to existing entries are preserved.
  * Conference papers/posters/talks are NOT touched here: they live in
    _data/publications_manual.yml and are curated by hand.

Run locally:   python scripts/update_publications.py
In CI:         see .github/workflows/update-publications.yml
"""

from __future__ import annotations
import json
import os
import sys
import urllib.parse
import urllib.request

try:
    import yaml  # PyYAML, for reading the existing file
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")

ORCID = os.environ.get("LAB_ORCID", "0000-0002-2830-0844")
MAILTO = os.environ.get("OPENALEX_MAILTO", "harvey@ucdavis.edu")
OUT = os.path.join(os.path.dirname(__file__), "..", "_data", "publications.yml")

# OpenAlex work types we treat as peer-reviewed journal articles.
JOURNAL_TYPES = {"article", "review", "letter"}

HEADER = """\
# ────────────────────────────────────────────────────────────
#  PUBLICATIONS: peer-reviewed journal articles
#
#  ⚙️  THIS FILE IS AUTO-MANAGED by scripts/update_publications.py.
#  The "Update publications" GitHub Action opens a pull request when new works
#  appear on OpenAlex for the lab's ORCID. Review and merge it. You may also
#  hand-edit any entry to fix a detail; future runs preserve existing DOIs.
#  Conference papers/posters/talks live in publications_manual.yml.
#
#  Fields: title, authors, venue, year, type (journal), doi (URL)
#  Keep newest first.
# ────────────────────────────────────────────────────────────
"""


def fetch_works() -> list[dict]:
    """Page through every work for the ORCID. Returns [] on any failure."""
    works, cursor = [], "*"
    base = "https://api.openalex.org/works"
    while cursor:
        params = {
            "filter": f"author.orcid:{ORCID}",
            "per-page": "200",
            "cursor": cursor,
            "mailto": MAILTO,
            "select": "title,publication_year,doi,type,authorships,primary_location",
        }
        url = base + "?" + urllib.parse.urlencode(params)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": f"BIRDLab-site ({MAILTO})"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.load(resp)
        except Exception as exc:  # network/JSON/HTTP: fail safe
            print(f"::warning::OpenAlex fetch failed ({exc}); leaving file unchanged.")
            return []
        works.extend(data.get("results", []))
        cursor = data.get("meta", {}).get("next_cursor")
    return works


def fmt_authors(authorships: list[dict]) -> str:
    names = []
    for a in authorships:
        full = (a.get("author") or {}).get("display_name", "").strip()
        if not full:
            continue
        parts = full.split()
        last = parts[-1]
        initials = " ".join(p[0].upper() + "." for p in parts[:-1] if p[0].isalpha())
        names.append(f"{initials} {last}".strip())
    return ", ".join(names)


def norm_doi(doi: str | None) -> str:
    if not doi:
        return ""
    return doi.lower().replace("https://doi.org/", "").replace("http://dx.doi.org/", "").strip()


def to_entry(work: dict) -> dict | None:
    if work.get("type") not in JOURNAL_TYPES:
        return None
    doi = work.get("doi")
    if not doi or not work.get("title") or not work.get("publication_year"):
        return None
    loc = work.get("primary_location") or {}
    source = (loc.get("source") or {}).get("display_name") or ""
    return {
        "title": work["title"].strip(),
        "authors": fmt_authors(work.get("authorships", [])),
        "venue": source,
        "year": int(work["publication_year"]),
        "type": "journal",
        "doi": doi if doi.startswith("http") else f"https://doi.org/{norm_doi(doi)}",
    }


def dq(s: str) -> str:
    """YAML double-quoted scalar."""
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'


def dump(entries: list[dict]) -> str:
    lines = [HEADER]
    for e in entries:
        lines.append(f"- title: {dq(e['title'])}")
        lines.append(f"  authors: {dq(e['authors'])}")
        lines.append(f"  venue: {dq(e['venue'])}")
        lines.append(f"  year: {e['year']}")
        lines.append(f"  type: {e['type']}")
        if e.get("doi"):
            lines.append(f"  doi: {dq(e['doi'])}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    with open(OUT, encoding="utf-8") as fh:
        existing = yaml.safe_load(fh) or []
    existing_dois = {norm_doi(e.get("doi")) for e in existing}

    works = fetch_works()
    if not works:
        print("No works returned; not modifying publications.yml.")
        return 0

    new = []
    for w in works:
        entry = to_entry(w)
        if entry and norm_doi(entry["doi"]) not in existing_dois:
            new.append(entry)
            existing_dois.add(norm_doi(entry["doi"]))

    if not new:
        print("Up to date: no new journal articles found.")
        return 0

    combined = existing + new
    combined.sort(key=lambda e: e.get("year", 0), reverse=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(dump(combined))

    print(f"Added {len(new)} new article(s):")
    for e in new:
        print(f"  + ({e['year']}) {e['title']}")
    # Expose a summary for the GitHub Action PR body.
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as gh:
            gh.write(f"added={len(new)}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
