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
  * We backfill a missing `date` (YYYY-MM-DD) onto existing entries from OpenAlex so
    the list sorts correctly within a year, but never overwrite a date you've set.
  * Corrections / corrigenda / errata are NOT listed as separate papers. We skip them
    and print them so you can attach a `correction:` link to the corrected paper in
    _data/pub_links.yml (it renders as a small "Correction" pill next to that paper).
  * AIAA works are classified journal-vs-conference by their venue NAME (AIAA
    journals and meeting papers share the 10.2514/ DOI prefix). Anything we can't
    classify is flagged in the run log and LEFT OUT for you to add by hand.
  * Conference talks/posters *without a DOI* aren't indexed by OpenAlex — add those
    by hand in _data/publications_manual.yml.
  * A do-not-list (`exclude:` in publications_manual.yml) drops items OpenAlex returns
    that aren't papers (a profile write-up, a talk indexed like an article). Listed DOIs
    are removed from publications.yml and never re-added.

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
# The hand-maintained companion; its `exclude:` list names DOIs to never list.
MANUAL = os.path.join(os.path.dirname(__file__), "..", "_data", "publications_manual.yml")

# OpenAlex work types we treat as peer-reviewed journal articles.
JOURNAL_TYPES = {"article", "review", "letter"}

# Ignore repositories and obvious supplementary materials.
EXCLUDED_SOURCE_TYPES = {"repository"}

SUPPLEMENT_KEYWORDS = (
    "supplement",
    "supplementary",
    "supplemental",
    "supporting information",
    "supporting data",
)

# Corrections/corrigenda/errata: not listed as papers. We catch them by OpenAlex type
# and by the standard title formats publishers use ("Correction to:", "Author
# Correction:", "Corrigendum: …", "Erratum: …", etc.).
CORRECTION_TYPES = {"erratum", "correction"}
CORRECTION_TITLE_PREFIXES = (
    "corrigendum",
    "erratum",
    "errata",
    "publisher correction",
    "author correction",
    "correction to",
    "correction:",
)

HEADER = """\
# ────────────────────────────────────────────────────────────
#  PUBLICATIONS — peer-reviewed journal articles
#
#  ⚙️  THIS FILE IS AUTO-MANAGED by scripts/update_publications.py.
#  The "Update publications" GitHub Action opens a pull request when new works
#  appear on OpenAlex for the lab's ORCID. Review and merge it. You may also
#  hand-edit any entry to fix a detail; future runs preserve existing DOIs.
#  Conference papers/posters/talks live in publications_manual.yml.
#
#  Fields: title, authors, venue, year, date (YYYY-MM-DD), type, doi (URL)
#  `date` is used to sort within a year (the page still groups by `year`).
#  Keep newest first — this file is written sorted by date, newest first.
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
            "select": "title,publication_year,publication_date,doi,type,authorships,primary_location",
        }
        url = base + "?" + urllib.parse.urlencode(params)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": f"BIRDLab-site ({MAILTO})"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.load(resp)
        except Exception as exc:  # network/JSON/HTTP — fail safe
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


def load_exclude() -> set:
    """Bare DOIs the maintainer marked as 'not a paper' in publications_manual.yml."""
    try:
        with open(MANUAL, encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
    except FileNotFoundError:
        return set()
    return {norm_doi(e.get("doi")) for e in (data.get("exclude") or []) if e.get("doi")}

# AIAA publishes BOTH conference/meeting papers (SciTech, AVIATION, …) AND
# peer-reviewed journals under the same "10.2514/" DOI prefix, so we can't tell them
# apart from the DOI alone. We decide from the source (venue) NAME, and only fall back
# to the AIAA DOI sub-code (/6. = meeting paper, /1.–/4. = journal) when the source is
# missing. If both are inconclusive we return None → the work is flagged and left out.
AIAA_CONFERENCE_HINTS = ("forum", "conference", "congress", "meeting", "symposium",
                         "scitech", "aviation", "propulsion and energy")
AIAA_JOURNAL_HINTS = ("journal",)


def aiaa_type(source_name: str, doi: str) -> str | None:
    s = (source_name or "").strip().lower()
    if s:
        if any(h in s for h in AIAA_CONFERENCE_HINTS):
            return "conference"
        if any(h in s for h in AIAA_JOURNAL_HINTS):
            return "journal"
    tail = doi.split("10.2514/", 1)[-1]          # fallback: AIAA DOI sub-code
    if tail.startswith("6."):
        return "conference"
    if tail[:2] in ("1.", "2.", "3.", "4."):
        return "journal"
    return None                                   # can't tell → flag & leave out


def publication_type(source_type: str, source_name: str, doi: str) -> str | None:
    """journal | conference | None (None = exclude, or flag for manual handling)."""
    if source_type == "repository":
        return None
    if doi.startswith("10.2514/"):               # AIAA — shared journal/conference prefix
        return aiaa_type(source_name, doi)
    return "journal"

def is_correction(work: dict) -> bool:
    """True for corrections/corrigenda/errata (by type or standard title format)."""
    if (work.get("type") or "") in CORRECTION_TYPES:
        return True
    title = (work.get("title") or "").strip().lower()
    return title.startswith(CORRECTION_TITLE_PREFIXES)


def has_my_orcid(work):
    my_orcid = f"https://orcid.org/{ORCID}"
    for auth in work.get("authorships", []):
        author = auth.get("author") or {}
        if author.get("orcid") == my_orcid:
            return True
    return False

def aiaa_flagged(work: dict) -> bool:
    """An AIAA (10.2514) work we couldn't type journal-vs-conference (left out)."""
    if not has_my_orcid(work) or is_correction(work):
        return False
    if work.get("type") not in JOURNAL_TYPES:
        return False
    doi = norm_doi(work.get("doi"))
    if not doi.startswith("10.2514/"):
        return False
    src = (work.get("primary_location") or {}).get("source") or {}
    return aiaa_type(src.get("display_name") or "", doi) is None


def to_entry(work: dict) -> dict | None:
    if not has_my_orcid(work):
        return None

    # Corrections/corrigenda are attached to the corrected paper via pub_links.yml,
    # never listed as their own entry.
    if is_correction(work):
        return None

    if work.get("type") not in JOURNAL_TYPES:
        return None

    doi = work.get("doi")
    title = (work.get("title") or "").strip()

    if not doi or not title or not work.get("publication_year"):
        return None

    loc = work.get("primary_location") or {}
    source = loc.get("source") or {}

    source_name = (source.get("display_name")
    or (work.get("host_venue") or {}).get("display_name")
    or "")
    source_type = source.get("type") or ""

    pub_type = publication_type(source_type, source_name, norm_doi(doi))

    if pub_type is None:
        return None

    # Exclude obvious supplementary material
    if any(k in title.lower() for k in SUPPLEMENT_KEYWORDS):
        return None

    return {
        "title": title,
        "authors": fmt_authors(work.get("authorships", [])),
        "venue": source_name,
        "year": int(work["publication_year"]),
        "date": (work.get("publication_date") or "").strip(),
        "type": pub_type,
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
        if e.get("date"):
            lines.append(f"  date: {dq(e['date'])}")
        lines.append(f"  type: {e['type']}")
        if e.get("doi"):
            lines.append(f"  doi: {dq(e['doi'])}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def sort_key(e: dict) -> str:
    """Sort by full date; entries with only a year fall to the end of that year."""
    d = e.get("date")
    return str(d) if d else f"{int(e.get('year', 0)):04d}-00-00"


def main() -> int:
    with open(OUT, encoding="utf-8") as fh:
        existing = yaml.safe_load(fh) or []

    # Drop anything the maintainer put on the do-not-list, and never re-add it.
    exclude = load_exclude()
    removed = [e for e in existing if norm_doi(e.get("doi")) in exclude]
    if removed:
        existing = [e for e in existing if norm_doi(e.get("doi")) not in exclude]
    existing_dois = {norm_doi(e.get("doi")) for e in existing}

    works = fetch_works()
    if not works:
        print("No works returned; not modifying publications.yml.")
        return 0

    # DOI -> publication_date, so we can backfill dates onto existing entries.
    date_by_doi = {norm_doi(w.get("doi")): w["publication_date"]
                   for w in works if w.get("doi") and w.get("publication_date")}

    # Backfill: add a `date` to any existing entry that lacks one (non-destructive —
    # we only fill an empty field, never change an existing value).
    backfilled = 0
    for e in existing:
        if not e.get("date"):
            d = date_by_doi.get(norm_doi(e.get("doi")))
            if d:
                e["date"] = d
                backfilled += 1

    new = []
    for w in works:
        entry = to_entry(w)
        if entry and norm_doi(entry["doi"]) not in existing_dois \
                and norm_doi(entry["doi"]) not in exclude:
            new.append(entry)
            existing_dois.add(norm_doi(entry["doi"]))

    # Corrections aren't added; surface them so they can be linked by hand.
    corrections = [w for w in works if has_my_orcid(w) and is_correction(w)]
    if corrections:
        print("Note: skipped %d correction/corrigendum item(s). If one corrects a paper on "
              "the list, add a `correction:` link to that paper in _data/pub_links.yml:"
              % len(corrections))
        for w in corrections:
            print(f"  ~ {norm_doi(w.get('doi'))}  {(w.get('title') or '').strip()}")

    # AIAA works with no clear venue name: left out for you to classify by hand.
    flagged = [w for w in works if aiaa_flagged(w)]
    if flagged:
        print("Note: %d AIAA work(s) couldn't be typed journal-vs-conference (no clear "
              "source name). Left out — add by hand to _data/publications.yml and set "
              "`type: journal` or `type: conference` yourself:" % len(flagged))
        for w in flagged:
            print(f"  ? {norm_doi(w.get('doi'))}  {(w.get('title') or '').strip()}")

    if removed:
        print("Removed %d entry(ies) on the do-not-list:" % len(removed))
        for e in removed:
            print(f"  - {norm_doi(e.get('doi'))}  {e.get('title')}")

    if not new and not backfilled and not removed:
        print("Up to date — no new articles, and every entry already has a date.")
        return 0

    combined = existing + new
    combined.sort(key=sort_key, reverse=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(dump(combined))

    if backfilled:
        print(f"Backfilled publication dates on {backfilled} existing entry(ies).")
    if new:
        print(f"Added {len(new)} new article(s):")
        for e in new:
            print(f"  + ({e.get('date') or e['year']}) {e['title']}")
    # Expose a summary for the GitHub Action PR body.
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as gh:
            gh.write(f"added={len(new)}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
