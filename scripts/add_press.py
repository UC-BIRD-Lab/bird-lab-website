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

Examples:
  python scripts/add_press.py "https://news.site/story" --doi 10.1098/rsif.2025.0868 --featured
  python scripts/add_press.py "https://news.site/story"                 # not featured, just print
  python scripts/add_press.py "https://news.site/story" --featured --append

Requires: Python 3.8+ . Pillow is used to resize/compress the image when --featured
(optional: without it the raw image is saved and you can shrink it later).
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
    if f.get("featured"):
        lines.append(indent + "featured: true")
        if f.get("image"):
            lines.append(indent + "image: " + f["image"])
    return "\n".join(lines)


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


# ── Main ──────────────────────────────────────────────────────────────────────
def main(argv=None):
    p = argparse.ArgumentParser(description="Build a press.yml entry from a news URL.")
    p.add_argument("url", help="Article URL")
    p.add_argument("--doi", default="", help="DOI of the paper the story covers (bare or URL)")
    p.add_argument("--featured", action="store_true", help="Promote to the big News cards + fetch image")
    p.add_argument("--year", type=int, help="Override the year (else read from the page)")
    p.add_argument("--source", help="Override the outlet name")
    p.add_argument("--title", help="Override the headline")
    p.add_argument("--image", help="Override image URL or local /assets path (implies --featured)")
    p.add_argument("--append", action="store_true", help="Insert into _data/press.yml (else just print)")
    args = p.parse_args(argv)

    if args.image:
        args.featured = True

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
    elif args.source and args.title and (args.image or not args.featured):
        # Site blocked us, but you supplied the essentials by hand: carry on.
        print("Note: couldn't fetch the page (%s); using the values you passed."
              % fetch_err, file=sys.stderr)
    else:
        need = '--source "Outlet" --title "Headline"'
        if args.featured:
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

    fields = {"title": title, "source": source, "url": args.url,
              "author": author, "doi": doi, "featured": args.featured}

    warnings = []
    if not title:
        warnings.append("no headline found: fill in `title:` by hand (or pass --title).")
    if not source:
        warnings.append("no outlet name found: fill in `source:` (or pass --source).")

    if args.featured:
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

    entry = build_entry(fields)

    # ── Console summary + the paste-ready block ──
    print("\n" + "-" * 66, file=sys.stderr)
    print("  source   : %s" % (source or "(!) missing"), file=sys.stderr)
    print("  title    : %s" % (title or "(!) missing"), file=sys.stderr)
    print("  author   : %s" % (author or "(none found)"), file=sys.stderr)
    print("  year     : %s" % year, file=sys.stderr)
    print("  doi      : %s" % (doi or "(none)"), file=sys.stderr)
    print("  featured : %s" % ("yes" if args.featured else "no"), file=sys.stderr)
    if fields.get("image"):
        print("  image    : %s" % fields["image"], file=sys.stderr)
    for w in warnings:
        print("  ! %s" % w, file=sys.stderr)
    print("-" * 66, file=sys.stderr)

    if args.append:
        append_to_press(entry, year)
        print("Inserted into _data/press.yml under %d. Review the diff before committing."
              % year, file=sys.stderr)
    else:
        print("Paste this under `- year: %d` (items:) in _data/press.yml:\n" % year,
              file=sys.stderr)
        print(entry)   # to stdout so it's easy to copy/redirect


if __name__ == "__main__":
    main()
