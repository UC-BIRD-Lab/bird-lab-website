#!/usr/bin/env python3
"""Report what is due for a human re-check: Lab Guide `reviewed:` dates,
_data/review.yml items, the banner deadline, the CALI rates `effective:` date.

    python3 scripts/review_sweep.py [--out report.md] [--quiet]   # --quiet: exit 1 if due

See MAINTENANCE.md, "The quarterly review issue".
"""
# Site tooling, largely AI-written (Claude), checked for behaviour not wording.
# Lab policy lives in _guide/. See accessibility.md, "How this site is made".

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import sys

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is not installed. Run: pip install -r scripts/requirements.txt")

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(REPO_ROOT, "_data")
GUIDE_DIR = os.path.join(REPO_ROOT, "_guide")

DEADLINE_WARN_DAYS = 14   # before a banner deadline


def load(name):
    path = os.path.join(DATA_DIR, name)
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def as_date(value):
    """date from a YAML date object or a string."""
    if isinstance(value, dt.date):
        return value
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, str):
        for fmt in ("%Y-%m-%d", "%B %d, %Y", "%b %d, %Y", "%d %B %Y"):
            try:
                return dt.datetime.strptime(value.strip(), fmt).date()
            except ValueError:
                continue
    return None


def months_since(date, today):
    return (today.year - date.year) * 12 + (today.month - date.month)


def front_matter(path):
    """YAML front matter of a Markdown file."""
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not match:
        return {}
    try:
        return yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return {}


# Checks
def overdue_guide_pages(config, today):
    interval = config.get("guide_every_months", 12)
    rows = []
    if not os.path.isdir(GUIDE_DIR):
        return rows
    for name in sorted(os.listdir(GUIDE_DIR)):
        if not name.endswith(".md"):
            continue
        meta = front_matter(os.path.join(GUIDE_DIR, name))
        title = meta.get("title", name[:-3])
        reviewed = as_date(meta.get("reviewed"))
        if reviewed is None:
            rows.append((title, name, "no `reviewed:` date", 999))
        elif months_since(reviewed, today) >= interval:
            rows.append((title, name,
                         f"last reviewed {reviewed:%-d %b %Y}", months_since(reviewed, today)))
    return sorted(rows, key=lambda r: -r[3])


def overdue_items(config, today):
    rows = []
    for item in config.get("items", []) or []:
        last = as_date(item.get("last_reviewed"))
        every = item.get("every_months", 12)
        if last is None:
            rows.append((item, "never recorded as reviewed", 999))
            continue
        elapsed = months_since(last, today)
        if elapsed >= every:
            rows.append((item, f"last reviewed {last:%-d %b %Y} ({elapsed} months ago)", elapsed))
    return sorted(rows, key=lambda r: -r[2])


def announcement_status(today):
    """Banner expired, closing soon, or undated."""
    data = load("announcement.yml") or {}
    if not data.get("enabled"):
        return None
    deadline = as_date(data.get("deadline"))
    label = data.get("label", "the banner")
    text = (data.get("text") or "").strip()
    if deadline is None:
        return ("no deadline", f"The banner (**{label}**) has no `deadline:`, so nothing "
                               "will prompt you to take it down.")
    days = (deadline - today).days
    if days < 0:
        ago = "yesterday" if abs(days) == 1 else f"{abs(days)} days ago"
        return ("expired", f"The banner (**{label}**) advertises a deadline of "
                           f"**{deadline:%-d %B %Y}**, which passed {ago}. "
                           f"It is still showing on every page.\n\n  > {text}\n\n"
                           "  Set `enabled: false` in `_data/announcement.yml`, or update it.")
    if days <= DEADLINE_WARN_DAYS:
        when = "today" if days == 0 else ("tomorrow" if days == 1 else f"in {days} days")
        return ("closing", f"The banner (**{label}**) closes on **{deadline:%-d %B %Y}**, "
                           f"{when}. Switch it off or replace it.")
    return None


def rates_status(today):
    data = load("cali_rates.yml") or {}
    effective = as_date(data.get("effective"))
    if effective and months_since(effective, today) >= 12:
        return (f"CALI rates have been effective since **{effective:%-d %B %Y}** "
                f"({months_since(effective, today)} months). UC Davis re-approves "
                "annually. Check whether newer rates exist.")
    return None


# Report
def build_report(today):
    config = load("review.yml") or {}
    guide = overdue_guide_pages(config, today)
    items = overdue_items(config, today)
    announcement = announcement_status(today)
    rates = rates_status(today)

    urgent = bool(announcement and announcement[0] == "expired")
    anything = bool(guide or items or announcement or rates)

    out = []
    out.append(f"_Swept {today:%-d %B %Y}. Rewritten each quarter, so no need to close it._\n")

    if not anything:
        out.append("Nothing is due for review. Everything on the list is current. ✅\n")
        return "\n".join(out), False, False

    out.append("Nothing is broken. These may have gone out of date, and only a person can tell.\n")

    if announcement:
        kind, message = announcement
        heading = "### ⚠️ Site banner" if kind == "expired" else "### Site banner"
        out.append(heading)
        out.append(f"- {message}\n")

    if items:
        out.append("### Content due for a check\n")
        for item, why, _ in items:
            owner = item.get("owner", "")
            out.append(f"- [ ] **{item.get('what', '?')}**: {why}")
            out.append(f"      `{item.get('file', '')}`" + (f" · {owner}" if owner else ""))
            if item.get("note"):
                out.append(f"      {' '.join(item['note'].split())}")
        out.append("")

    if rates:
        out.append("### Rates\n")
        out.append(f"- [ ] {rates}\n")

    if guide:
        out.append(f"### Lab Guide pages not reviewed recently ({len(guide)})\n")
        for title, filename, why, _ in guide:
            out.append(f"- [ ] **{title}**: {why} · `_guide/{filename}`")
        out.append("")
        out.append("_To clear one: read it, fix anything wrong, then set `reviewed:` to "
                   "today in its front matter. Setting the date after confirming nothing "
                   "needed changing is a fine outcome._\n")

    out.append("---")
    out.append("_From `_data/review.yml` via `scripts/review_sweep.py`. "
               "Edit that file to change this list._")
    return "\n".join(out), True, urgent


def main(argv=None):
    ap = argparse.ArgumentParser(description="Report what needs a human review.")
    ap.add_argument("--out", help="Write the report to this file as well as stdout.")
    ap.add_argument("--quiet", action="store_true",
                    help="Print nothing; just exit 1 if anything is due.")
    ap.add_argument("--today", help="Pretend today is this date (YYYY-MM-DD), for testing.")
    args = ap.parse_args(argv)

    today = as_date(args.today) if args.today else dt.date.today()
    if today is None:
        sys.exit("--today must look like 2026-08-13")

    report, anything_due, _urgent = build_report(today)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(report + "\n")
    if not args.quiet:
        print(report)
    return 1 if (args.quiet and anything_due) else 0


if __name__ == "__main__":
    sys.exit(main())
