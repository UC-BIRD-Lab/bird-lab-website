#!/usr/bin/env python3
"""
add_press.py: turn a news-article URL into a ready-to-paste _data/press.yml entry.

You give it the article URL, (optionally) the DOI of the paper the story covers, and
whether the story should be "featured". It fetches the page, reads the outlet name,
headline, and author from the page's own metadata, and: ONLY when --featured is set:
downloads the article's lead image into assets/img/news/ (resized and compressed to the
site's image budget). It then prints a YAML block you can paste into _data/press.yml under
the right year. Pass --append to have it inserted for you (comments/formatting preserved).

SAFE by design (same spirit as update_publications.py):
  * Read-only unless you pass --append.
  * --append does a *targeted text insert*; it never rewrites the whole file, so your
    header comments and hand-formatting stay intact.
  * If the page is missing a field, it warns and leaves that field blank to fill in.

It can also build a _data/media.yml entry (videos, podcasts, radio, 3D models) with
--media KIND. A media item is a compact row by default; add --featured to give it a
thumbnail card (YouTube thumbnails are automatic, other cards need an --image).

── Paper announcements ──────────────────────────────────────────────────────────
Give it a paper's DOI with --paper and it drafts the two things you write by hand
every time a paper lands: a _data/updates.yml news-timeline entry AND ready-to-post
LinkedIn + Instagram captions. It reads the paper's title/authors/venue/year from
your own publications.yml (canonical) and falls back to OpenAlex by DOI if the paper
isn't synced yet, so this pairs naturally with the monthly "Update publications" PR:
merge that, then run this on the new DOI.

  * Lab authors are matched against _data/people.yml and written with their full
    People-page names, so they AUTO-LINK in the timeline (same as any updates entry).
  * The lead lab author becomes the subject ("Paper led by …"); a Harvey-first paper
    reads "Paper by Dr. Harvey". Pass --topic "…" for the plain-language hook (else
    the title is used as a placeholder to tighten).
  * --append inserts the updates.yml entry under the right year (newest first),
    targeted-insert so your comments/formatting stay intact. Captions print to the
    console (or --out FILE); they are never committed to the site.

Examples:
  python scripts/add_press.py "https://news.site/story" --doi 10.1098/rsif.2025.0868 --featured
  python scripts/add_press.py "https://news.site/story"                 # not featured, just print
  python scripts/add_press.py "https://news.site/story" --featured --append
  # Media (Watch & listen strip):
  python scripts/add_press.py "https://youtu.be/XXXX" --media video --featured --append
  python scripts/add_press.py "https://pod.site/ep" --media podcast --append
  python scripts/add_press.py "https://npr.org/…" --media radio --doi 10.1098/rsif.2025.1082 --append
  # Paper announcement (news entry + social captions):
  python scripts/add_press.py --paper 10.1098/rsif.2025.1082 --topic "raptor perching behavior"
  python scripts/add_press.py --paper 10.1098/rsif.2025.1082 --append > captions.txt

Requires: Python 3.8+ . Pillow is used to resize/compress the image when --featured
(optional: without it the raw image is saved and you can shrink it later). The --paper
mode uses PyYAML (already in scripts/requirements.txt) to read your data files.
"""
from __future__ import annotations
import argparse
import datetime
import html
import io
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRESS_YML = os.path.join(REPO_ROOT, "_data", "press.yml")
MEDIA_YML = os.path.join(REPO_ROOT, "_data", "media.yml")
UPDATES_YML = os.path.join(REPO_ROOT, "_data", "updates.yml")
PUBLICATIONS_YML = os.path.join(REPO_ROOT, "_data", "publications.yml")
PUBLICATIONS_MANUAL_YML = os.path.join(REPO_ROOT, "_data", "publications_manual.yml")
PEOPLE_YML = os.path.join(REPO_ROOT, "_data", "people.yml")
IMG_DIR = os.path.join(REPO_ROOT, "assets", "img", "news")
IMG_MAXW = 1280          # matches the research-figure budget (~1280px)
IMG_MAX_KB = 140         # nudge JPEG quality down until under this
# Present as a normal browser. Many news sites sit behind a bot filter (Cloudflare,
# Akamai, a campus WAF, …) that returns 403 for anything that doesn't look like one.
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
BROWSER_HEADERS = {
    "User-Agent": UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


# ── Page parsing ──────────────────────────────────────────────────────────────
class MetaParser(HTMLParser):
    """Collect <meta> tags, the <title>, the first <h1>, and JSON-LD blocks."""

    def __init__(self):
        super().__init__()
        self.meta = {}          # keyed by property/name (lowercased)
        self.title = None
        self.h1 = None
        self.ld = []            # raw application/ld+json strings
        self._in_title = False
        self._in_h1 = False
        self._in_ld = False

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "meta":
            key = a.get("property") or a.get("name") or a.get("itemprop")
            if key and "content" in a:
                self.meta.setdefault(key.lower(), a["content"])
        elif tag == "title":
            self._in_title = True
        elif tag == "h1" and self.h1 is None:
            self._in_h1 = True
        elif tag == "script" and a.get("type", "").lower() == "application/ld+json":
            self._in_ld = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "h1":
            self._in_h1 = False
        elif tag == "script":
            self._in_ld = False

    def handle_data(self, data):
        if self._in_title and self.title is None and data.strip():
            self.title = data.strip()
        elif self._in_h1 and self.h1 is None and data.strip():
            self.h1 = data.strip()
        elif self._in_ld and data.strip():
            self.ld.append(data.strip())


def fetch(url):
    req = urllib.request.Request(url, headers=BROWSER_HEADERS)
    with urllib.request.urlopen(req, timeout=25) as r:
        raw = r.read()
        charset = r.headers.get_content_charset() or "utf-8"
    return raw.decode(charset, errors="replace")


def ld_field(ld_blocks, *keys):
    """Search JSON-LD blocks (incl. @graph) for the first present key."""
    for block in ld_blocks:
        try:
            data = json.loads(block)
        except Exception:
            continue
        items = data if isinstance(data, list) else [data]
        for it in list(items):
            if isinstance(it, dict) and isinstance(it.get("@graph"), list):
                items = items + it["@graph"]
        for it in items:
            if isinstance(it, dict):
                for k in keys:
                    if it.get(k):
                        return it[k]
    return None


def author_name(val):
    if isinstance(val, str):
        return val.strip()
    if isinstance(val, dict):
        return str(val.get("name", "")).strip()
    if isinstance(val, list):
        names = [author_name(v) for v in val]
        return ", ".join(n for n in names if n)
    return ""


# ── Small helpers ─────────────────────────────────────────────────────────────
def clean_title(title, source):
    if not title:
        return ""
    t = html.unescape(title).strip()
    if source:
        for sep in (" | ", " – ", ": ", " - ", " • "):
            suffix = sep + source
            if t.lower().endswith(suffix.lower()):
                t = t[: -len(suffix)].strip()
    return t


def domain_source(url):
    net = re.sub(r"^www\.", "", urllib.parse.urlparse(url).netloc.lower())
    return net.split(".")[0].replace("-", " ").title() if net else ""


def slugify(text, maxlen=60):
    s = re.sub(r"[^a-z0-9]+", "-", html.unescape(text or "").lower()).strip("-")
    return s[:maxlen].strip("-") or "story"


def yaml_dq(s):
    """A safe YAML double-quoted scalar."""
    return '"' + (s or "").replace("\\", "\\\\").replace('"', '\\"') + '"'


def strip_doi(doi):
    if not doi:
        return ""
    return re.sub(r"(?i)^\s*(https?://)?(dx\.)?doi\.org/", "", doi).strip()


def get_year(meta, ld, override):
    if override:
        return override
    for key in ("article:published_time", "og:article:published_time",
                "datepublished", "date"):
        v = meta.get(key, "")
        if re.match(r"\d{4}", v):
            return int(v[:4])
    d = ld_field(ld, "datePublished", "dateCreated")
    if isinstance(d, str) and re.match(r"\d{4}", d):
        return int(d[:4])
    return datetime.date.today().year


# ── Image handling ────────────────────────────────────────────────────────────
def save_image(img_url, article_url, slug):
    img_url = urllib.parse.urljoin(article_url, img_url)
    req = urllib.request.Request(img_url, headers=dict(BROWSER_HEADERS, Referer=article_url))
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    os.makedirs(IMG_DIR, exist_ok=True)
    out = os.path.join(IMG_DIR, slug + ".jpg")
    try:
        from PIL import Image
    except ImportError:
        with open(out, "wb") as f:
            f.write(data)
        return out, "saved raw (install Pillow to auto-resize/compress: pip install Pillow)"

    im = Image.open(io.BytesIO(data))
    if im.mode in ("RGBA", "LA", "P"):
        rgba = im.convert("RGBA")
        bg = Image.new("RGB", rgba.size, (255, 255, 255))
        bg.paste(rgba, mask=rgba.split()[-1])
        im = bg
    else:
        im = im.convert("RGB")
    if im.width > IMG_MAXW:
        im = im.resize((IMG_MAXW, round(im.height * IMG_MAXW / im.width)), Image.LANCZOS)
    q = 82
    im.save(out, "JPEG", quality=q, optimize=True, progressive=True)
    while os.path.getsize(out) > IMG_MAX_KB * 1024 and q > 60:
        q -= 6
        im.save(out, "JPEG", quality=q, optimize=True, progressive=True)
    return out, f"{im.width}px wide, {os.path.getsize(out) // 1024} KB"


# ── YAML entry building + optional append ─────────────────────────────────────
def build_entry(f, indent="      "):
    """Return the YAML lines for one press item (item dash at 4 spaces)."""
    lines = ["    - title: " + yaml_dq(f["title"]),
             indent + "source: " + yaml_dq(f["source"]),
             indent + "url: " + yaml_dq(f["url"])]
    if f.get("author"):
        lines.append(indent + "author: " + yaml_dq(f["author"]))
    if f.get("doi"):
        lines.append(indent + "doi: " + yaml_dq(f["doi"]))
    elif f.get("tag"):
        # `tag:` labels why a NON-paper story is in the list (Center/Award/Funding/
        # Profile/Feature). A story with a doi shows a "Paper" pill instead, so the
        # two are mutually exclusive — only emit tag when there is no doi.
        lines.append(indent + "tag: " + f["tag"])
    if f.get("featured"):
        lines.append(indent + "featured: true")
        if f.get("image"):
            lines.append(indent + "image: " + f["image"])
    return "\n".join(lines)


def build_media_entry(f):
    """Return the YAML lines for one _data/media.yml item (a flat top-level list)."""
    lines = ["- title: " + yaml_dq(f["title"]),
             "  kind: " + (f.get("kind") or "video"),
             "  source: " + yaml_dq(f["source"]),
             "  year: %s" % f["year"],
             "  url: " + yaml_dq(f["url"])]
    if f.get("doi"):
        lines.append("  doi: " + yaml_dq(f["doi"]))
    elif f.get("tag"):
        lines.append("  tag: " + f["tag"])
    if f.get("featured"):
        lines.append("  featured: true")
        if f.get("image"):
            lines.append("  image: " + f["image"])
    return "\n".join(lines)


def append_to_media(entry_block):
    """Insert one item at the TOP of media.yml (newest first), just after the
    header comment block. Targeted text insert — header/formatting preserved."""
    if not os.path.exists(MEDIA_YML):
        raise FileNotFoundError(MEDIA_YML)
    lines = open(MEDIA_YML, encoding="utf-8").read().splitlines()
    first = next((i for i, ln in enumerate(lines) if ln.startswith("- ")), len(lines))
    block = entry_block.splitlines() + [""]
    lines[first:first] = block
    open(MEDIA_YML, "w", encoding="utf-8").write("\n".join(lines).rstrip("\n") + "\n")


def append_to_press(entry_block, year):
    if not os.path.exists(PRESS_YML):
        raise FileNotFoundError(PRESS_YML)
    lines = open(PRESS_YML, encoding="utf-8").read().splitlines()
    year_at = {}
    for i, ln in enumerate(lines):
        m = re.match(r"- year:\s*(\d{4})", ln)
        if m:
            year_at[int(m.group(1))] = i
    entry_lines = entry_block.splitlines()

    if year in year_at:
        j = year_at[year] + 1
        while j < len(lines) and not re.match(r"\s*items:\s*$", lines[j]):
            j += 1
        lines[j + 1: j + 1] = entry_lines          # newest at top of that year
    else:
        block = ["- year: %d" % year, "  items:"] + entry_lines
        older = sorted([y for y in year_at if y < year], reverse=True)
        if older:                                   # insert before first older year
            pos = year_at[older[0]]
            lines[pos:pos] = block + [""]
        else:                                       # oldest so far → append
            if lines and lines[-1].strip():
                lines.append("")
            lines += block
    open(PRESS_YML, "w", encoding="utf-8").write("\n".join(lines).rstrip("\n") + "\n")


# ── Paper announcements: DOI → updates.yml entry + social captions ────────────
#
# This whole section is self-contained so the rest of add_press.py keeps working
# with zero extra dependencies; PyYAML is imported lazily, only when --paper runs.
MONTHS = ["", "January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]


def _yaml():
    """Import PyYAML on demand with a friendly message (mirrors update_publications.py)."""
    try:
        import yaml
        return yaml
    except ImportError:
        sys.exit("PyYAML is required for --paper: pip install -r scripts/requirements.txt")


def deaccent(s):
    """Fold accents so 'Martínez' matches 'Martinez' across data sources."""
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFKD", s or "")
                   if not unicodedata.combining(c))


def surname_key(author):
    """The comparable surname from one author token, e.g. 'M. G. Hawkins' → 'hawkins',
    'C. Harvey (also …poster)' → 'harvey', 'A. Martínez-Carmena' → 'martinez'."""
    a = re.sub(r"\(.*?\)", "", author or "").strip().strip(".")
    a = re.split(r"\s+", a)[-1] if a else ""
    a = deaccent(a).lower()
    return a.split("-")[0]                      # first part of a hyphenated surname


def load_people_map():
    """Map surname → the name to print (preferring the short alias the timeline uses,
    e.g. 'Dr. Alfonso Martínez', 'Adam Zhu'), plus the set of Harvey surnames.
    Covers current members, affiliates, and alumni so any co-author can link."""
    yaml = _yaml()
    try:
        with open(PEOPLE_YML, encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
    except FileNotFoundError:
        return {}, {"harvey"}

    people = {}
    def add(member):
        name = (member.get("name") or "").strip()
        if not name:
            return
        aliases = member.get("aliases") or []
        display = aliases[0].strip() if aliases else name          # timeline style
        last = (member.get("last") or name).split()[-1]
        for key in {surname_key(last), surname_key(name)}:
            if key:
                people.setdefault(key, display)

    for group in (data.get("groups") or []):
        for m in (group.get("members") or []):
            add(m)
    for bucket in ("affiliates", "alumni"):
        for m in ((data.get(bucket) or {}).get("members") or []):
            add(m)
    return people, {"harvey"}


def openalex_by_doi(doi):
    """Resolve one work from OpenAlex by DOI. Returns a paper dict or None."""
    url = "https://api.openalex.org/works/https://doi.org/" + urllib.parse.quote(doi)
    url += "?mailto=harvey@ucdavis.edu"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "BIRDLab-site (harvey@ucdavis.edu)"})
        with urllib.request.urlopen(req, timeout=25) as r:
            w = json.load(r)
    except Exception as e:
        print("Note: OpenAlex lookup failed (%s)." % e, file=sys.stderr)
        return None
    names = []
    for a in w.get("authorships") or []:
        full = ((a.get("author") or {}).get("display_name") or "").strip()
        if not full:
            continue
        parts = full.split()
        initials = " ".join(p[0].upper() + "." for p in parts[:-1] if p[:1].isalpha())
        names.append((initials + " " + parts[-1]).strip())
    venue = ((w.get("primary_location") or {}).get("source") or {}).get("display_name") or ""
    return {"title": (w.get("title") or "").strip(),
            "authors": ", ".join(names),
            "venue": venue.strip(),
            "year": w.get("publication_year"),
            "date": w.get("publication_date") or ""}


def resolve_paper(doi):
    """Prefer the site's own committed metadata (canonical), else OpenAlex by DOI."""
    yaml = _yaml()
    want = strip_doi(doi).lower()

    def scan(path, key=None):
        try:
            with open(path, encoding="utf-8") as fh:
                data = yaml.safe_load(fh) or {}
        except FileNotFoundError:
            return None
        entries = data.get(key, []) if key else data
        if isinstance(entries, dict):                 # publications.yml is a bare list
            entries = []
        for e in (entries or []):
            if isinstance(e, dict) and strip_doi(e.get("doi", "")).lower() == want and want:
                return e
        return None

    hit = scan(PUBLICATIONS_YML) or scan(PUBLICATIONS_MANUAL_YML, "conference") \
        or scan(PUBLICATIONS_MANUAL_YML, "journal")
    if hit:
        return {"title": (hit.get("title") or "").strip(),
                "authors": (hit.get("authors") or "").strip(),
                "venue": (hit.get("venue") or "").strip(),
                "year": hit.get("year"),
                "date": str(hit.get("date") or ""),
                "_source": "publications.yml"}, None

    oa = openalex_by_doi(want)
    if oa:
        oa["_source"] = "OpenAlex"
        return oa, None
    return None, ("couldn't find DOI %s in publications.yml/publications_manual.yml, "
                  "and OpenAlex had nothing. Check the DOI, or add the paper first." % want)


def month_year(paper):
    """'July 2026' from the paper's date/year (falls back to the year alone)."""
    d = (paper.get("date") or "").strip()
    m = re.match(r"(\d{4})-(\d{2})", d)
    if m:
        return "%s %s" % (MONTHS[int(m.group(2))], m.group(1))
    return str(paper.get("year") or datetime.date.today().year)


def build_update_text(paper, people, harvey_keys, topic=None):
    """Draft the timeline sentence, linking the lead lab author automatically."""
    authors = paper.get("authors") or ""
    first = authors.split(",")[0] if authors else ""
    lead_key = surname_key(first)
    venue = (paper.get("venue") or "").strip()
    title = (paper.get("title") or "").strip().rstrip(".")

    if lead_key in harvey_keys:
        subject = "Paper by Dr. Harvey"
    elif lead_key in people:
        subject = "Paper led by %s" % people[lead_key]
    else:
        subject = "Paper"                              # external lead author
    venue_clause = (" in %s" % venue) if venue else ""
    if topic:
        return "%s%s on %s." % (subject, venue_clause, topic.strip().rstrip("."))
    return "%s%s: “%s.”" % (subject, venue_clause, title)   # curly quotes


def build_update_entry(date_label, text):
    """One inline updates.yml event line (matches the file's flow-mapping style)."""
    safe = text.replace("\\", "\\\\").replace('"', '\\"')
    return '    - { date: "%s", type: paper, text: "%s" }' % (date_label, safe)


def append_to_updates(entry_line, year):
    """Insert the event as the newest item under `- year: YEAR` (targeted insert;
    header comments and formatting are preserved). Creates the year block if new."""
    if not os.path.exists(UPDATES_YML):
        raise FileNotFoundError(UPDATES_YML)
    lines = open(UPDATES_YML, encoding="utf-8").read().splitlines()
    year_at = {}
    for i, ln in enumerate(lines):
        m = re.match(r"- year:\s*(\d{4})", ln)
        if m:
            year_at[int(m.group(1))] = i

    if year in year_at:
        j = year_at[year] + 1
        while j < len(lines) and not re.match(r"\s*events:\s*$", lines[j]):
            j += 1
        lines[j + 1:j + 1] = [entry_line]              # newest at top of that year
    else:
        block = ["- year: %d" % year, "  events:", entry_line]
        older = sorted([y for y in year_at if y < year], reverse=True)
        if older:
            pos = year_at[older[0]]
            lines[pos:pos] = block + [""]
        else:
            if lines and lines[-1].strip():
                lines.append("")
            lines += block
    open(UPDATES_YML, "w", encoding="utf-8").write("\n".join(lines).rstrip("\n") + "\n")


def clean_authors_for_social(authors):
    """Human-readable author list for captions (drop the '(also … poster)' notes)."""
    return re.sub(r"\s*\(.*?\)", "", authors or "").strip().rstrip(",")


def build_social(paper, doi):
    """Return (linkedin, instagram) caption drafts. Kept deliberately editable:
    a bracketed takeaway prompt is left for the one human sentence worth writing."""
    title = (paper.get("title") or "").strip().rstrip(".")
    venue = (paper.get("venue") or "").strip()
    year = paper.get("year") or datetime.date.today().year
    authors = clean_authors_for_social(paper.get("authors"))
    link = "https://doi.org/" + strip_doi(doi)
    venue_line = ("%s (%s)" % (venue, year)) if venue else str(year)

    linkedin = (
        "\U0001F426 New from the BIRD Lab — our latest paper is out"
        + ((" in %s" % venue) if venue else "") + ".\n\n"
        "“" + title + "”\n\n"
        "[One plain-language sentence on what we found and why it matters.]\n\n"
        + (("Authors: %s\n" % authors) if authors else "")
        + "Read it: " + link + "\n\n"
        "#BioinspiredDesign #BirdFlight #AerospaceEngineering #Biomechanics #UCDavis #BIRDLab"
    )
    instagram = (
        "New paper out \U0001F985\U0001F4C4\n\n"
        "“" + title + "”\n"
        + venue_line + "\n\n"
        "[One friendly line on the finding + why it's cool.]\n"
        "\U0001F517 Full paper linked in our bio.\n\n"
        "#birdflight #bioinspired #aerospace #biomechanics #engineering #UCDavis #science #research"
    )
    return linkedin, instagram


def run_paper(args):
    """--paper pipeline: draft an updates.yml news entry + LinkedIn/Instagram captions."""
    doi = strip_doi(args.paper)
    if not doi:
        sys.exit("ERROR: --paper needs a DOI (bare or as a doi.org URL).")

    print("Resolving DOI %s ..." % doi, file=sys.stderr)
    paper, err = resolve_paper(doi)
    if err:
        sys.exit("ERROR: " + err)

    # Overrides let you fix anything the metadata got wrong.
    if args.title:
        paper["title"] = args.title
    if args.source:
        paper["venue"] = args.source
    if args.year:
        paper["year"] = args.year

    people, harvey_keys = load_people_map()
    text = build_update_text(paper, people, harvey_keys, topic=args.topic)
    date_label = month_year(paper)
    year = int(re.search(r"\d{4}", date_label).group())
    entry = build_update_entry(date_label, text)
    linkedin, instagram = build_social(paper, doi)

    # ── Console summary ──
    print("\n" + "-" * 66, file=sys.stderr)
    print("  source   : %s" % paper.get("_source", "?"), file=sys.stderr)
    print("  title    : %s" % (paper.get("title") or "(!) missing"), file=sys.stderr)
    print("  venue    : %s" % (paper.get("venue") or "(none)"), file=sys.stderr)
    print("  authors  : %s" % (paper.get("authors") or "(none)"), file=sys.stderr)
    print("  date     : %s  (year %d)" % (date_label, year), file=sys.stderr)
    lead_key = surname_key((paper.get("authors") or "").split(",")[0])
    who = people.get(lead_key) or ("Dr. Harvey" if lead_key in harvey_keys else "(external lead)")
    print("  lead link: %s" % who, file=sys.stderr)
    if not args.topic:
        print("  ! no --topic given: the title is used as a placeholder — tighten it.",
              file=sys.stderr)
    print("-" * 66, file=sys.stderr)

    if args.append:
        append_to_updates(entry, year)
        print("Inserted into _data/updates.yml under %d (newest first). Review the diff."
              % year, file=sys.stderr)
    else:
        print("Paste this as the newest event under `- year: %d` in _data/updates.yml:\n"
              % year, file=sys.stderr)
        print(entry)

    # Captions go to a file if asked, else to the console. Never committed to the site.
    social = ("=== LinkedIn ===\n%s\n\n=== Instagram ===\n%s\n" % (linkedin, instagram))
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(social)
        print("Wrote captions to %s" % args.out, file=sys.stderr)
    else:
        print("\n" + "-" * 66, file=sys.stderr)
        print("Social captions (edit the [bracketed] takeaway, then post):", file=sys.stderr)
        print("-" * 66, file=sys.stderr)
        print("\n" + social)


# ── Main ──────────────────────────────────────────────────────────────────────
def main(argv=None):
    p = argparse.ArgumentParser(
        description="Draft a press.yml / media.yml entry from a news URL, "
                    "or (with --paper DOI) a publications news entry + social captions.")
    p.add_argument("url", nargs="?", help="Article URL (omit when using --paper)")
    p.add_argument("--doi", default="", help="DOI of the paper the story covers (bare or URL)")
    p.add_argument("--paper", default="", metavar="DOI",
                   help="Paper-announcement mode: draft a _data/updates.yml news entry and "
                        "LinkedIn/Instagram captions from this DOI (bare or doi.org URL).")
    p.add_argument("--topic", default="",
                   help="[--paper] Plain-language hook for the news entry "
                        "(e.g. \"raptor perching behavior\"); default falls back to the title.")
    p.add_argument("--out", default="",
                   help="[--paper] Write the social captions to this file instead of the console.")
    p.add_argument("--tag", default="", choices=["", "Center", "Award", "Funding", "Profile", "Feature"],
                   help="Reason tag for a story NOT tied to a paper (ignored if --doi is given)")
    p.add_argument("--featured", action="store_true", help="Promote to the big News cards + fetch image")
    p.add_argument("--year", type=int, help="Override the year (else read from the page)")
    p.add_argument("--source", help="Override the outlet name")
    p.add_argument("--title", help="Override the headline")
    p.add_argument("--image", help="Override image URL or local /assets path (implies --featured)")
    p.add_argument("--media", default="", choices=["", "video", "podcast", "radio", "model"],
                   help="Build a _data/media.yml entry of this kind instead of a press entry "
                        "(video / podcast / radio / model). --featured gives it a thumbnail card.")
    p.add_argument("--append", action="store_true",
                   help="Insert into the data file (else just print). Targets media.yml with --media, else press.yml.")
    args = p.parse_args(argv)

    # Paper-announcement mode is its own pipeline (no news page to scrape).
    if args.paper:
        return run_paper(args)
    if not args.url:
        p.error("give an article URL, or use --paper DOI for a paper announcement.")

    is_media = bool(args.media)
    # A media item only needs an image when it's a featured NON-YouTube card;
    # YouTube cards get their thumbnail automatically, so don't force-fetch one.
    yt = ("youtube.com" in args.url) or ("youtu.be" in args.url)
    if args.image:
        args.featured = True
    want_image = args.featured and not (is_media and yt)

    print("Fetching %s ..." % args.url, file=sys.stderr)
    page, fetch_err = None, None
    try:
        page = fetch(args.url)
    except urllib.error.HTTPError as e:
        fetch_err = "HTTP %s %s" % (e.code, e.reason)
    except Exception as e:
        fetch_err = str(e)

    m = MetaParser()
    if page:
        m.feed(page)
    elif args.source and args.title and (args.image or not want_image):
        # Site blocked us, but you supplied the essentials by hand: carry on.
        print("Note: couldn't fetch the page (%s); using the values you passed."
              % fetch_err, file=sys.stderr)
    else:
        need = '--source "Outlet" --title "Headline"'
        if want_image:
            need += " --image <image-url>"
        sys.exit(
            "ERROR: couldn't fetch the article (%s).\n"
            "Some sites block automated requests even from a browser-like agent. Either add\n"
            "the entry by hand, or re-run with the pieces filled in yourself:\n"
            '  python scripts/add_press.py "%s" --doi %s %s%s'
            % (fetch_err, args.url, args.doi or "<doi>", need,
               " --featured" if args.featured else ""))
    meta, ld = m.meta, m.ld

    source = args.source or meta.get("og:site_name") or meta.get("application-name") \
        or domain_source(args.url)
    source = html.unescape(source).strip()

    raw_title = args.title or meta.get("og:title") or meta.get("twitter:title") \
        or m.title or m.h1 or ""
    title = clean_title(raw_title, source)

    author = meta.get("author", "").strip()
    if not author:
        aa = meta.get("article:author", "")
        if aa and not aa.lower().startswith("http"):
            author = aa
    if not author:
        author = author_name(ld_field(ld, "author", "creator"))
    author = html.unescape(author).strip()

    year = get_year(meta, ld, args.year)
    doi = strip_doi(args.doi)

    # A tag only applies to stories without a DOI (doi shows a "Paper" pill instead).
    tag = "" if doi else args.tag
    fields = {"title": title, "source": source, "url": args.url,
              "author": author, "doi": doi, "tag": tag, "featured": args.featured,
              "kind": args.media, "year": year}

    warnings = []
    if not title:
        warnings.append("no headline found: fill in `title:` by hand (or pass --title).")
    if not source:
        warnings.append("no outlet name found: fill in `source:` (or pass --source).")

    if want_image:
        img_ref = args.image
        if img_ref and img_ref.startswith("/assets/"):
            fields["image"] = img_ref            # already a local path; trust it
        else:
            img_url = img_ref or meta.get("og:image") or meta.get("og:image:url") \
                or meta.get("twitter:image") or meta.get("twitter:image:src")
            if not img_url:
                warnings.append("featured, but no lead image found: add `image:` by hand "
                                "(or pass --image URL).")
            else:
                slug = slugify((source + "-" + title) if title else args.url)
                try:
                    path, info = save_image(img_url, args.url, slug)
                    rel = "/" + os.path.relpath(path, REPO_ROOT).replace(os.sep, "/")
                    fields["image"] = rel
                    print("Saved image -> %s (%s)" % (rel, info), file=sys.stderr)
                except Exception as e:
                    warnings.append("could not download the image (%s): add `image:` by hand." % e)

    entry = build_media_entry(fields) if is_media else build_entry(fields)

    # ── Console summary + the paste-ready block ──
    print("\n" + "-" * 66, file=sys.stderr)
    print("  target   : %s" % ("media.yml (%s)" % args.media if is_media else "press.yml"), file=sys.stderr)
    print("  source   : %s" % (source or "(!) missing"), file=sys.stderr)
    print("  title    : %s" % (title or "(!) missing"), file=sys.stderr)
    if not is_media:
        print("  author   : %s" % (author or "(none found)"), file=sys.stderr)
    print("  year     : %s" % year, file=sys.stderr)
    print("  doi      : %s" % (doi or "(none)"), file=sys.stderr)
    print("  tag      : %s" % (tag or "(none)"), file=sys.stderr)
    print("  featured : %s" % ("yes" if args.featured else "no"), file=sys.stderr)
    if fields.get("image"):
        print("  image    : %s" % fields["image"], file=sys.stderr)
    for w in warnings:
        print("  ! %s" % w, file=sys.stderr)
    print("-" * 66, file=sys.stderr)

    if args.append:
        if is_media:
            append_to_media(entry)
            print("Inserted at the top of _data/media.yml. Review the diff before committing.",
                  file=sys.stderr)
        else:
            append_to_press(entry, year)
            print("Inserted into _data/press.yml under %d. Review the diff before committing."
                  % year, file=sys.stderr)
    elif is_media:
        print("Paste this at the top of _data/media.yml (newest first):\n", file=sys.stderr)
        print(entry)   # to stdout so it's easy to copy/redirect
    else:
        print("Paste this under `- year: %d` (items:) in _data/press.yml:\n" % year,
              file=sys.stderr)
        print(entry)   # to stdout so it's easy to copy/redirect


if __name__ == "__main__":
    main()
