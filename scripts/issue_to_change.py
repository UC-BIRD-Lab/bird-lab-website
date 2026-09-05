#!/usr/bin/env python3
"""Turn a filled-in issue form (stdin or ISSUE_BODY) into the matching _data edit.

  --kind news         → _data/updates.yml
  --kind conference   → _data/publications_manual.yml
  --kind person       → _data/people.yml (existing name: only filled fields change)
  --kind press        → _data/press.yml

Inserts preserve header comments. A missing or invalid field changes nothing and
exits non-zero so the Action can tell the submitter.

  ISSUE_BODY="$(gh issue view 42 --json body -q .body)" \\
      python scripts/issue_to_change.py --kind news    # CI: issue-to-pr.yml
"""
# Site tooling, largely AI-written (Claude), checked for behaviour not wording.
# Lab policy lives in _guide/. See accessibility.md, "How this site is made".
from __future__ import annotations
import argparse
import os
import re
import sys

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

# Form role → people.yml group id. The msc/visiting groups stay in people.yml,
# even empty, so these always have a home.
ROLE_GROUP = {
    "postdoctoral scholar": "postdoc",
    "phd candidate": "phd",
    "phd researcher": "phd",
    "msc student": "msc",
    "undergraduate researcher": "undergrad",
    "visiting undergraduate researcher": "undergrad",
    "visiting researcher": "visiting",
}
# No public email for these roles.
NO_EMAIL_ROLES = {"undergraduate researcher", "visiting undergraduate researcher"}


# Issue-form parsing
def parse_issue_form(body: str) -> dict:
    """'### Label\\n\\nvalue' blocks → {label: value}."""
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


def as_link(u: str) -> str:
    """Full URL, bare DOI, bare domain, or on-site path (kept relative for preview builds)."""
    u = (u or "").strip()
    if not u:
        return ""
    if u.startswith("/"):
        return u if u.endswith("/") or "." in u.rsplit("/", 1)[-1] else u + "/"
    return doi_or_link(u)


def doi_or_link(v: str) -> str:
    """'DOI or link' field → URL."""
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


# Builders, one per form
def snap_phrase(text: str, phrase: str) -> str:
    """The phrase as it appears in `text`, ignoring case and whitespace; "" if absent."""
    phrase = re.sub(r"\s+", " ", (phrase or "").strip()).strip(".,;:")
    if not phrase:
        return ""
    pattern = r"\s+".join(re.escape(w) for w in phrase.split(" "))
    m = re.search(pattern, text or "", re.IGNORECASE)
    return m.group(0) if m else ""


def build_news(f: dict) -> int:
    date = field(f, "Month and year", "Date")
    ntype = field(f, "Type").lower()
    text = field(f, "What happened", "Text")
    link = as_link(field(f, "Link (optional)", "Link", "URL"))
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

    # Without a matching phrase the site renders a trailing "Details" link.
    phrase = snap_phrase(text, field(f, "Words to link (optional)",
                                     "Words to link", "Link text")) if link else ""
    if link and not phrase:
        print("note: linking the whole entry with a trailing link "
              "(no matching words to link were given).")

    parts = ["date: " + dq(date), "type: " + ntype, "text: " + dq(text)]
    if link:
        parts.append("link: " + dq(link))
    if phrase:
        parts.append("link_text: " + dq(phrase))
    entry = "    - { %s }" % ", ".join(parts)
    append_to_updates(entry, year)
    print(entry)
    emit("news: " + text, "_data/updates.yml")
    return 0


def build_conference(f: dict) -> int:
    title = field(f, "Title")
    authors = field(f, "Authors")
    venue = field(f, "Venue")
    year = find_year(field(f, "Year"))
    ptype = field(f, "Type").lower()
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

    note = {"talk": "Presentation", "poster": "Poster"}.get(ptype)
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

    # Existing active member (never alumni/affiliates): update in place.
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

    role_text = role
    if home and role.lower().startswith("visiting"):
        role_text = "%s · %s" % (role, home)

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
        # Only filled-in fields change.
        updates = {"role": role_text, "start": "%d" % start}
        if pronouns:
            updates["pronouns"] = pronouns
        if fld:
            updates["field"] = dq(fld)
        if email and role.lower() not in NO_EMAIL_ROLES:
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
            print("no changes: %s already matches the submission" % existing)
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
    if email and role.lower() not in NO_EMAIL_ROLES:
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
    tag = field(f, "Reason tag (optional, for stories NOT tied to a paper)", "Reason tag", "Tag")
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


# Targeted inserts
def insert_under_key(path: str, key_line: str, block_lines: list[str]):
    """Insert block_lines right after key_line (e.g. 'conference:'), top of that list."""
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
    """Index where alumni/affiliates start; updates never go past it."""
    return next((i for i, ln in enumerate(lines)
                 if re.match(r"^(affiliates|alumni):", ln)), len(lines))


def _entry_span(lines: list[str], i: int, stop: int) -> int:
    """Index just past the member block starting at the `- name:` line i."""
    entry_indent = len(lines[i]) - len(lines[i].lstrip())
    j = i + 1
    while j < stop:
        ln = lines[j]
        if ln.strip() and (len(ln) - len(ln.lstrip())) <= entry_indent:
            break
        j += 1
    return j


def find_person(name: str) -> str | None:
    """Canonical `name:` of an active member (case-insensitive, aliases count), or None."""
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
    """Replace or append each key's line in the member's entry; returns keys changed."""
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
            # A `>-`/`|` scalar spans deeper lines; replace all of them.
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
            # New field goes before any trailing comments (the "# photo:" hint).
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
    """Insert a member block at the top of group gid's `members:` list."""
    lines = open(PEOPLE, encoding="utf-8").read().splitlines()
    gi = next((i for i, ln in enumerate(lines)
               if re.match(r"\s*- id:\s*%s\s*$" % re.escape(gid), ln)), None)
    if gi is None:
        raise SystemExit("ERROR: group id '%s' not found in people.yml" % gid)
    # `members: []` (an empty group) is rewritten as a block header.
    mi = next((j for j in range(gi + 1, len(lines))
               if re.match(r"\s*members:\s*(\[\s*\])?\s*$", lines[j])), None)
    if mi is None:
        raise SystemExit("ERROR: no 'members:' under group '%s'" % gid)
    indent = re.match(r"(\s*)members:", lines[mi]).group(1)
    lines[mi] = indent + "members:"
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
