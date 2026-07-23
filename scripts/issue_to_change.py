#!/usr/bin/env python3
"""
issue_to_change.py: turn a filled-in website issue FORM into the matching
`_data/*.yml` edit, so a lab member submitting a form is all it takes to get a
change drafted. An Action runs this and opens a pull request for a maintainer to
review and merge (merging closes the issue).

One script handles all four forms (routed by --kind):

  --kind news         📣 Add a news milestone   → _data/updates.yml
  --kind conference   📄 Add a conference paper → _data/publications_manual.yml
  --kind person       ➕ Add/update a member    → _data/people.yml
                        (a name already on the People page is UPDATED in place —
                        only the fields filled in are touched, photo/awards kept —
                        so members can fix pronouns, links, notes, … via the form;
                        an unknown name is inserted into its role group as before)
  --kind press        📰 Add press coverage     → _data/press.yml

It reads the issue body GitHub's issue FORMS produce (each field is a
'### Label' block) from stdin or the ISSUE_BODY env var, validates the fields,
and does a SAFE targeted insert (your header comments and hand-formatting are
preserved, same as the rest of the tooling). If a required field is missing or a
value is invalid, it changes nothing and exits non-zero with a clear message, so
the Action can tell the submitter what to fix instead of committing something broken.

Member names in text auto-link on the site, so names are written as on the People page.

Run locally:  ISSUE_BODY="$(gh issue view 42 --json body -q .body)" \
                  python scripts/issue_to_change.py --kind news
In CI:        see .github/workflows/issue-to-pr.yml
"""
from __future__ import annotations
import argparse
import os
import re
import sys

# Reuse the exact, format-preserving inserts the press/paper tooling already uses.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from add_press import (append_to_press, append_to_updates, build_entry,  # noqa: E402
                       strip_doi)

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(REPO_ROOT, "_data")
PUBS_MANUAL = os.path.join(DATA, "publications_manual.yml")
PEOPLE = os.path.join(DATA, "people.yml")

NEWS_TYPES = {"award", "paper", "talk", "funding", "build",
              "service", "people", "travel", "graduation"}
NO_RESPONSE = "_no response_"

# Role → People-page group id (the group the member is filed under in people.yml).
# Every dropdown role maps to an existing group; the msc/visiting groups are kept
# empty in people.yml precisely so these two always have a home.
ROLE_GROUP = {
    "postdoctoral scholar": "postdoc",
    "phd candidate": "phd",
    "phd researcher": "phd",
    "msc student": "msc",
    "undergraduate researcher": "undergrad",
    "visiting undergraduate researcher": "undergrad",
    "visiting researcher": "visiting",
}
# Roles for which we omit a public email (matches the People page privacy pattern).
NO_EMAIL_ROLES = {"undergraduate researcher", "visiting undergraduate researcher"}


# ── Issue-form parsing ────────────────────────────────────────────────────────
def parse_issue_form(body: str) -> dict:
    """GitHub renders a form as '### Label\\n\\nvalue' blocks → {label: value}."""
    fields, label, buf = {}, None, []
    for line in (body or "").splitlines():
        m = re.match(r"^#{2,4}\s+(.*\S)\s*$", line)
        if m:
            if label is not None:
                fields[label] = "\n".join(buf).strip()
            label, buf = m.group(1).strip(), []
        elif label is not None:
            buf.append(line)
    if label is not None:
        fields[label] = "\n".join(buf).strip()
    for k, v in list(fields.items()):
        if v.strip().lower() == NO_RESPONSE:
            fields[k] = ""
    return fields


def field(fields: dict, *names: str) -> str:
    lower = {k.lower(): v for k, v in fields.items()}
    for n in names:
        if n.lower() in lower:
            return lower[n.lower()].strip()
    return ""


def dq(s: str) -> str:
    """Double-quoted YAML scalar, newlines collapsed to spaces."""
    s = re.sub(r"\s+", " ", (s or "").strip())
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def find_year(text: str) -> int | None:
    m = re.search(r"\b(19|20)\d{2}\b", text or "")
    return int(m.group()) if m else None


def as_url(u: str) -> str:
    u = (u or "").strip()
    if not u:
        return ""
    return u if u.startswith("http") else "https://" + u.lstrip("/")


def doi_or_link(v: str) -> str:
    """Normalize a 'DOI or link' field to a URL (bare DOIs → https://doi.org/…)."""
    v = (v or "").strip()
    if not v:
        return ""
    if v.startswith("http"):
        return v
    if re.match(r"10\.\d{4,9}/", v):
        return "https://doi.org/" + v
    return as_url(v)


def fail(problems: list[str]) -> int:
    print("Could not build the change from this issue:", file=sys.stderr)
    for p in problems:
        print("  - " + p, file=sys.stderr)
    return 1


def emit(summary: str, target: str):
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as gh:
            gh.write("summary=%s\n" % re.sub(r"\s+", " ", summary).strip()[:120])
            gh.write("target=%s\n" % target)


# ── Builders (one per form) ───────────────────────────────────────────────────
def build_news(f: dict) -> int:
    date = field(f, "Month and year", "Date")
    ntype = field(f, "Type").lower()
    text = field(f, "What happened", "Text")
    problems = []
    if not date:
        problems.append("missing **Month and year**.")
    if not text:
        problems.append("missing **What happened**.")
    if ntype not in NEWS_TYPES:
        problems.append("Type %r must be one of: %s."
                        % (ntype or "(empty)", ", ".join(sorted(NEWS_TYPES))))
    year = find_year(date)
    if year is None:
        problems.append("no 4-digit year in **Month and year**.")
    if problems:
        return fail(problems)

    entry = '    - { date: %s, type: %s, text: %s }' % (dq(date), ntype, dq(text))
    append_to_updates(entry, year)
    print(entry)
    emit("news: " + text, "_data/updates.yml")
    return 0


def build_conference(f: dict) -> int:
    title = field(f, "Title")
    authors = field(f, "Authors")
    venue = field(f, "Venue")
    year = find_year(field(f, "Year"))
    ptype = field(f, "Type").lower()          # Paper / Talk / Poster
    doi = doi_or_link(field(f, "DOI or link (optional)", "DOI or link", "DOI"))
    problems = []
    for lbl, val in (("Title", title), ("Authors", authors), ("Venue", venue)):
        if not val:
            problems.append("missing **%s**." % lbl)
    if year is None:
        problems.append("missing or unparseable **Year**.")
    if ptype not in ("paper", "talk", "poster"):
        problems.append("Type must be Paper, Talk, or Poster.")
    if problems:
        return fail(problems)

    note = {"talk": "Presentation", "poster": "Poster"}.get(ptype)   # Paper → none
    lines = ["  - title: " + dq(title),
             "    authors: " + dq(authors),
             "    venue: " + dq(venue),
             "    year: %d" % year,
             "    type: conference"]
    if note:
        lines.append("    note: " + note)
    if doi:
        lines.append("    doi: " + dq(doi))
    insert_under_key(PUBS_MANUAL, "conference:", lines)
    print("\n".join(lines))
    emit("conference: " + title, "_data/publications_manual.yml")
    return 0


def build_person(f: dict) -> int:
    name = field(f, "Full name", "Name")
    role = field(f, "Role")
    start = find_year(field(f, "Year you joined the lab", "Start", "Year joined"))
    fld = field(f, "Field / discipline you trained in", "Field")
    pronouns = field(f, "Pronouns")
    email = field(f, "Email")
    note = field(f, "One-line research note", "Note")
    links = field(f, "Links (optional)", "Links")
    home = field(f, "Home institution (visiting members only)", "Home institution")

    # The form is "add OR update": if the name is already on the People page
    # (active groups only — never alumni/affiliates), we update that entry in
    # place instead of inserting a duplicate.
    existing = find_person(name) if name else None

    problems = []
    if not name:
        problems.append("missing **Full name**.")
    if not role:
        problems.append("missing **Role**.")
    if start is None:
        problems.append("missing or unparseable **Year you joined**.")
    gid = ROLE_GROUP.get(role.lower())
    if role and gid is None and existing is None:
        problems.append("role %r has no active group on the People page yet; a "
                        "maintainer needs to place this person by hand." % role)
    if problems:
        return fail(problems)

    # Visiting roles show their home institution appended to the role text.
    role_text = role
    if home and role.lower().startswith("visiting"):
        role_text = "%s · %s" % (role, home)

    # Classify the free-text links into linkedin / orcid / website.
    linkedin = orcid = website = ""
    for tok in re.split(r"[\s,;·]+", links):
        t = tok.strip().strip("·").strip()
        if not t:
            continue
        low = t.lower()
        if "linkedin" in low:
            linkedin = as_url(t)
        elif "orcid" in low:
            m = re.search(r"\d{4}-\d{4}-\d{4}-[\dxX]{4}", t)
            orcid = m.group() if m else t
        elif "." in t:
            website = as_url(t)

    if existing is not None:
        # UPDATE in place: only the fields the form filled in are touched;
        # everything else (photo, awards, aliases, scholar, …) is left alone.
        updates = {"role": role_text, "start": "%d" % start}
        if pronouns:
            updates["pronouns"] = pronouns
        if fld:
            updates["field"] = dq(fld)
        if email and role.lower() not in NO_EMAIL_ROLES:  # privacy: no undergrad email
            updates["email"] = email
        if linkedin:
            updates["linkedin"] = linkedin
        if website:
            updates["website"] = website
        if orcid:
            updates["orcid"] = orcid
        if note:
            updates["note"] = dq(note)
        changed = update_person(existing, updates)
        if changed:
            print("updated %s: %s" % (existing, ", ".join(changed)))
        else:
            print("no changes — %s already matches the submission" % existing)
        emit("person update: %s (%s)" % (existing, ", ".join(changed) or "no change"),
             "_data/people.yml")
        return 0

    lines = ["      - name: " + name,
             "        role: " + role_text,
             "        start: %d" % start]
    if pronouns:
        lines.append("        pronouns: " + pronouns)
    if fld:
        lines.append("        field: " + dq(fld))
    if email and role.lower() not in NO_EMAIL_ROLES:      # privacy: no undergrad email
        lines.append("        email: " + email)
    if linkedin:
        lines.append("        linkedin: " + linkedin)
    if website:
        lines.append("        website: " + website)
    if orcid:
        lines.append("        orcid: " + orcid)
    if note:
        lines.append("        note: " + dq(note))
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    lines.append("        # photo: /assets/img/people/%s.jpg   # add after uploading a headshot" % slug)

    insert_person(gid, lines)
    print("\n".join(lines))
    emit("person: %s (%s)" % (name, role), "_data/people.yml")
    return 0


def build_press(f: dict) -> int:
    title = field(f, "Article headline", "Headline", "Title")
    source = field(f, "Outlet / source", "Source")
    url = as_url(field(f, "Link to the article", "Link", "URL"))
    year = find_year(field(f, "Year"))
    doi = strip_doi(field(f, "Paper DOI (optional)", "Paper DOI", "DOI"))
    tag = field(f, "Reason tag (optional — for stories NOT tied to a paper)", "Reason tag", "Tag")
    problems = []
    for lbl, val in (("Article headline", title), ("Outlet / source", source),
                     ("Link to the article", url)):
        if not val:
            problems.append("missing **%s**." % lbl)
    if year is None:
        problems.append("missing or unparseable **Year**.")
    if problems:
        return fail(problems)

    # A tag applies only when there's no DOI, and never the "(none…)" placeholder.
    if doi or tag.lower().startswith("(none"):
        tag = ""
    entry = build_entry({"title": title, "source": source, "url": url,
                         "doi": doi, "tag": tag, "featured": False})
    append_to_press(entry, year)
    print(entry)
    emit("press: %s (%s)" % (title, source), "_data/press.yml")
    return 0


# ── Shared targeted inserts ───────────────────────────────────────────────────
def insert_under_key(path: str, key_line: str, block_lines: list[str]):
    """Insert block_lines right after the first line equal to key_line (e.g.
    'conference:'), i.e. at the TOP of that list. Targeted; formatting preserved."""
    lines = open(path, encoding="utf-8").read().splitlines()
    for i, ln in enumerate(lines):
        if ln.strip() == key_line.strip():
            lines[i + 1:i + 1] = block_lines
            break
    else:
        raise SystemExit("ERROR: couldn't find '%s' in %s" % (key_line, path))
    open(path, "w", encoding="utf-8").write("\n".join(lines).rstrip("\n") + "\n")


def _people_lines() -> list[str]:
    return open(PEOPLE, encoding="utf-8").read().splitlines()


def _active_section_end(lines: list[str]) -> int:
    """Index where the active `groups:` section ends (alumni/affiliates start).
    Updates never touch alumni or affiliates — retiring someone stays by-hand."""
    return next((i for i, ln in enumerate(lines)
                 if re.match(r"^(affiliates|alumni):", ln)), len(lines))


def _entry_span(lines: list[str], i: int, stop: int) -> int:
    """Given the index of a `- name:` line, return the index just past the last
    line of that member's block (fields are the more-indented lines below)."""
    entry_indent = len(lines[i]) - len(lines[i].lstrip())
    j = i + 1
    while j < stop:
        ln = lines[j]
        if ln.strip() and (len(ln) - len(ln.lstrip())) <= entry_indent:
            break
        j += 1
    return j


def find_person(name: str) -> str | None:
    """Return the canonical `name:` of an ACTIVE member matching `name`
    (exact, case-insensitive; aliases count too), or None if not found."""
    lines = _people_lines()
    stop = _active_section_end(lines)
    target = name.strip().lower()
    for i in range(stop):
        m = re.match(r"^\s*- name:\s*(.+?)\s*$", lines[i])
        if not m:
            continue
        canonical = m.group(1).strip().strip('"')
        if canonical.lower() == target:
            return canonical
        for j in range(i + 1, _entry_span(lines, i, stop)):
            a = re.match(r"^\s*aliases:\s*\[(.*)\]\s*$", lines[j])
            if a and target in [s.strip().strip('"\'').lower()
                                for s in a.group(1).split(",")]:
                return canonical
    return None


def update_person(name: str, updates: dict) -> list[str]:
    """Update an active member's entry in place: replace each key's line if the
    field exists, append it to the entry if not. Formatting, comments, and any
    fields not in `updates` (photo, awards, …) are preserved. Returns the list
    of keys that actually changed."""
    lines = _people_lines()
    stop = _active_section_end(lines)
    target = name.strip().lower()
    i = next((k for k in range(stop)
              if re.match(r"^\s*- name:\s*(.+?)\s*$", lines[k])
              and re.match(r"^\s*- name:\s*(.+?)\s*$", lines[k])
                    .group(1).strip().strip('"').lower() == target), None)
    if i is None:
        raise SystemExit("ERROR: '%s' not found in people.yml for update" % name)
    end = _entry_span(lines, i, stop)
    first_field = next((ln for ln in lines[i + 1:end]
                        if ln.strip() and not ln.lstrip().startswith("#")), None)
    indent = " " * (len(first_field) - len(first_field.lstrip())) if first_field \
        else " " * ((len(lines[i]) - len(lines[i].lstrip())) + 2)

    changed = []
    for key, val in updates.items():
        new_line = "%s%s: %s" % (indent, key, val)
        j = next((k for k in range(i + 1, end)
                  if re.match(r"^\s*%s:(\s|$)" % re.escape(key), lines[k])), None)
        if j is not None:
            # A folded/literal scalar (e.g. `note: >-`) continues on deeper
            # lines; replace the whole thing so no orphan lines remain.
            k = j + 1
            if re.search(r":\s*[>|]", lines[j]):
                key_ind = len(lines[j]) - len(lines[j].lstrip())
                while k < end and (not lines[k].strip() or
                                   (len(lines[k]) - len(lines[k].lstrip())) > key_ind):
                    k += 1
            if lines[j:k] != [new_line]:
                lines[j:k] = [new_line]
                end -= (k - j) - 1
                changed.append(key)
        else:
            # New field: append after the entry's last real line (before any
            # trailing comments, e.g. the "# photo: …" hint).
            at = end
            while at - 1 > i and (not lines[at - 1].strip()
                                  or lines[at - 1].lstrip().startswith("#")):
                at -= 1
            lines[at:at] = [new_line]
            end += 1
            changed.append(key)
    if changed:
        open(PEOPLE, "w", encoding="utf-8").write("\n".join(lines).rstrip("\n") + "\n")
    return changed


def insert_person(gid: str, block_lines: list[str]):
    """Insert a member block under the `- id: <gid>` group's `members:` list."""
    lines = open(PEOPLE, encoding="utf-8").read().splitlines()
    gi = next((i for i, ln in enumerate(lines)
               if re.match(r"\s*- id:\s*%s\s*$" % re.escape(gid), ln)), None)
    if gi is None:
        raise SystemExit("ERROR: group id '%s' not found in people.yml" % gid)
    # Accept both a block `members:` and an empty-list `members: []` (used to keep
    # empty groups build-safe). For the latter, turn it into a block header first.
    mi = next((j for j in range(gi + 1, len(lines))
               if re.match(r"\s*members:\s*(\[\s*\])?\s*$", lines[j])), None)
    if mi is None:
        raise SystemExit("ERROR: no 'members:' under group '%s'" % gid)
    indent = re.match(r"(\s*)members:", lines[mi]).group(1)
    lines[mi] = indent + "members:"          # normalize `members: []` → `members:`
    lines[mi + 1:mi + 1] = block_lines
    open(PEOPLE, "w", encoding="utf-8").write("\n".join(lines).rstrip("\n") + "\n")


BUILDERS = {"news": build_news, "conference": build_conference,
            "person": build_person, "press": build_press}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Turn a website issue form into a _data edit.")
    ap.add_argument("--kind", required=True, choices=sorted(BUILDERS))
    args = ap.parse_args(argv)

    body = os.environ.get("ISSUE_BODY")
    if body is None:
        body = sys.stdin.read()
    fields = parse_issue_form(body)
    return BUILDERS[args.kind](fields)


if __name__ == "__main__":
    raise SystemExit(main())
