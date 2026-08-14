#!/usr/bin/env python3
"""Check _data/ for content mistakes that would build fine but publish something wrong.

Cross-references names, DOIs and image paths. Doesn't check writing or design.

    python3 scripts/validate_content.py

Runs on every pull request via site-checks.yml.

To add a check: write a check_* function that yields Problem objects and add it
to CHECKS at the bottom. Write the message for someone who has never opened this
file: what's wrong, which file, what to do.

Why this exists: MAINTENANCE.md → "Checking your content before you publish".
"""
# Website tooling, largely written by AI (Claude) and checked for behaviour
# rather than wording. It describes how the site is built, not how the lab works;
# lab policy lives in _guide/. See accessibility.md, "How this site is made".

from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is not installed. Run: pip install -r scripts/requirements.txt")

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(REPO_ROOT, "_data")
FORMS_DIR = os.path.join(REPO_ROOT, ".github", "ISSUE_TEMPLATE")


# ── Problem reporting ─────────────────────────────────────────────────────────
@dataclass
class Problem:
    """`where` is the file; `fix` is plain-English advice."""
    where: str
    what: str
    fix: str = ""
    warning: bool = False


def error(where, what, fix=""):
    return Problem(where, what, fix, warning=False)


def warn(where, what, fix=""):
    return Problem(where, what, fix, warning=True)


# ── Loading ───────────────────────────────────────────────────────────────────
def load(name):
    """Read one _data file; None if missing."""
    path = os.path.join(DATA_DIR, name)
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def norm_doi(value):
    """DOIs appear bare in pub_links/press and as full URLs in publications.
    Reduce both to the bare form so they compare equal."""
    if not value:
        return ""
    text = str(value).strip().lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if text.startswith(prefix):
            text = text[len(prefix):]
    return text.rstrip("/")


def asset_exists(web_path):
    """'/assets/img/people/jane.jpg' → is that file actually in the repo?"""
    if not web_path or not str(web_path).startswith("/"):
        return True  # external URLs and blank values are handled elsewhere
    return os.path.exists(os.path.join(REPO_ROOT, str(web_path).lstrip("/")))


def people_names(people):
    """Names plus aliases."""
    names = set()
    for group in (people or {}).get("groups", []) or []:
        for member in group.get("members") or []:
            if member.get("name"):
                names.add(member["name"].strip())
            for alias in member.get("aliases") or []:
                names.add(str(alias).strip())
    return names


def manual_entries(manual):
    """Flatten publications_manual.yml's headings into (heading, entry) pairs,
    skipping `exclude` (which isn't publications)."""
    out = []
    for heading, entries in (manual or {}).items():
        if heading == "exclude":
            continue
        for entry in entries or []:
            if isinstance(entry, dict):
                out.append((heading, entry))
    return out


def excluded_dois(manual):
    """DOIs deliberately kept off the site."""
    return {
        norm_doi(e.get("doi"))
        for e in (manual or {}).get("exclude", []) or []
        if isinstance(e, dict) and e.get("doi")
    }


def all_dois(pubs, manual):
    """Every DOI the site can display."""
    dois = {norm_doi(e["doi"]) for e in (pubs or []) if isinstance(e, dict) and e.get("doi")}
    dois |= {e["doi"] and norm_doi(e["doi"]) for _, e in manual_entries(manual) if e.get("doi")}
    return {d for d in dois if d}


# ── Checks ────────────────────────────────────────────────────────────────────
def check_yaml_parses():
    """Runs first and alone: nothing else works if a file won't parse."""
    for filename in sorted(os.listdir(DATA_DIR)):
        if not filename.endswith((".yml", ".yaml")):
            continue
        path = os.path.join(DATA_DIR, filename)
        try:
            with open(path, encoding="utf-8") as fh:
                yaml.safe_load(fh)
        except yaml.YAMLError as exc:
            mark = getattr(exc, "problem_mark", None)
            where = f"_data/{filename}" + (f" line {mark.line + 1}" if mark else "")
            yield error(
                where,
                f"This file isn't valid YAML: {getattr(exc, 'problem', exc)}",
                "Usually indentation (spaces, never tabs), a missing colon, or a curly "
                "quote pasted from Word. Check that line and the one above it.",
            )


def check_people():
    people = load("people.yml")
    if not people:
        return
    seen = {}
    for group in people.get("groups", []) or []:
        gid = group.get("id", "?")
        if not group.get("title"):
            yield error(f"_data/people.yml (group '{gid}')", "This group has no `title:`.",
                        "It's the heading on the People page.")
        for member in group.get("members") or []:
            name = (member.get("name") or "").strip()
            if not name:
                yield error(f"_data/people.yml (group '{gid}')", "A member has no `name:`.",
                            "Projects and news link to people by name.")
                continue
            if name in seen:
                yield error("_data/people.yml",
                            f"'{name}' is listed twice (in '{seen[name]}' and '{gid}').",
                            "Remove one. Duplicate names break the automatic linking in news "
                            "and projects.")
            seen[name] = gid

            if not member.get("role"):
                yield error("_data/people.yml", f"'{name}' has no `role:`.",
                            "The role sets their bird badge.")

            photo = member.get("photo")
            if photo and not asset_exists(photo):
                yield error("_data/people.yml",
                            f"'{name}' has photo `{photo}`, but that file isn't in the repo.",
                            "Upload it to assets/img/people/, or delete the `photo:` line for "
                            "an initials avatar.")

            email = member.get("email")
            if email and not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", str(email)):
                yield error("_data/people.yml", f"'{name}' has an email that looks wrong: {email}",
                            "Check for a typo or stray space.")

            orcid = member.get("orcid")
            if orcid and not re.match(r"^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$", str(orcid)):
                yield error("_data/people.yml", f"'{name}' has an ORCID that looks wrong: {orcid}",
                            "Use just the number, like 0000-0002-2830-0844, not the full "
                            "orcid.org address.")


def check_research():
    research = load("research.yml")
    people = load("people.yml")
    pubs, manual = load("publications.yml"), load("publications_manual.yml")
    if not research:
        return

    known_people = people_names(people)
    known_dois = all_dois(pubs, manual)
    theme_ids = {t.get("id") for t in research.get("themes", []) or [] if t.get("id")}

    for theme in research.get("themes", []) or []:
        if not theme.get("id"):
            yield error("_data/research.yml", f"Theme '{theme.get('title', '?')}' has no `id:`.",
                        "Projects reference themes by id.")

    for project in research.get("projects", []) or []:
        title = project.get("title", "(untitled project)")

        lead = (project.get("lead") or "").strip()
        if not lead:
            yield error("_data/research.yml", f"Project '{title}' has no `lead:`.",
                        "Use the name exactly as in _data/people.yml.")
        elif lead not in known_people:
            close = [n for n in known_people if lead.split()[-1].lower() in n.lower()] if lead.split() else []
            hint = f" Did you mean '{close[0]}'?" if close else ""
            yield error("_data/research.yml",
                        f"Project '{title}' has lead '{lead}', who isn't in _data/people.yml.{hint}",
                        "Must match a name or alias in people.yml, or the card can't link "
                        "to them. If they've left, keep them listed or reassign the project.")

        theme = project.get("theme")
        if theme and theme not in theme_ids:
            yield error("_data/research.yml",
                        f"Project '{title}' is filed under theme '{theme}', which doesn't exist.",
                        f"Use one of: {', '.join(sorted(theme_ids))}.")

        for doi in project.get("papers") or []:
            if norm_doi(doi) not in known_dois:
                yield error("_data/research.yml",
                            f"Project '{title}' lists paper {doi}, which isn't in the "
                            "publications data.",
                            "Cards look papers up by DOI, so an unknown one shows nothing. Add it "
                            "to publications_manual.yml, or wait for the monthly sync.")

        image = project.get("image")
        if image and not asset_exists(image):
            yield error("_data/research.yml",
                        f"Project '{title}' has image `{image}`, which isn't in the repo.",
                        "Upload it to assets/img/research/, or remove the `image:` line.")


def check_publications():
    pubs, manual = load("publications.yml"), load("publications_manual.yml")
    seen = {}
    entries = [("publications.yml", e) for e in (pubs or []) if isinstance(e, dict)]
    entries += [(f"publications_manual.yml ({heading})", e) for heading, e in manual_entries(manual)]

    for label, entry in entries:
        title = entry.get("title", "(untitled)")
        # Blog posts and similar have no author list; papers must have one.
        required = ["title", "year"]
        if entry.get("type") in ("journal", "conference"):
            required.append("authors")
        for field in required:
            if not entry.get(field):
                yield error(f"_data/{label}", f"'{title}' has no `{field}:`.",
                            "Publications need a title and year; papers also need authors.")

        date = entry.get("date")
        if date and not re.match(r"^\d{4}-\d{2}-\d{2}$", str(date)):
            yield error(f"_data/{label}", f"'{title}' has date '{date}'.",
                        "Dates here must be YYYY-MM-DD, e.g. 2026-07-24.")

        year = entry.get("year")
        if year and not (str(year).isdigit() and 1990 <= int(year) <= 2100):
            yield error(f"_data/{label}", f"'{title}' has an implausible year: {year}",
                        "Check for a typo.")

        doi = norm_doi(entry.get("doi"))
        if doi:
            if doi in seen:
                yield error("_data/publications*.yml",
                            f"DOI {doi} appears twice ('{seen[doi]}' and '{title}').",
                            "It will appear twice. Delete the publications_manual.yml entry; "
                            "the OpenAlex sync maintains the other.")
            seen[doi] = title


def check_pub_links():
    links, pubs, manual = load("pub_links.yml"), load("publications.yml"), load("publications_manual.yml")
    if not links:
        return
    known = all_dois(pubs, manual)
    for entry in links:
        if not isinstance(entry, dict):
            continue
        doi = norm_doi(entry.get("doi"))
        if not doi:
            yield error("_data/pub_links.yml", "An entry has no `doi:`.",
                        "Extras attach to a paper by DOI.")
            continue
        if doi in excluded_dois(manual):
            yield warn("_data/pub_links.yml",
                       f"{doi} is on the `exclude:` list in publications_manual.yml, "
                       "so it isn't shown on the site.",
                       "These extras will never appear. Remove this entry, or take the DOI "
                       "off `exclude:` if the paper should be listed.")
        elif doi not in known:
            yield error("_data/pub_links.yml",
                        f"{doi} doesn't match any paper in the publications data.",
                        "Check for a typo, or add the paper first, otherwise these show nowhere.")
        image = entry.get("image")
        if image and not asset_exists(image):
            yield error("_data/pub_links.yml",
                        f"{doi} has image `{image}`, which isn't in the repo.",
                        "Upload it to assets/img/pubs/, or remove the `image:` line.")


def check_press():
    press, pubs, manual = load("press.yml"), load("publications.yml"), load("publications_manual.yml")
    if not press:
        return
    known = all_dois(pubs, manual)
    for block in press:
        if not isinstance(block, dict):
            continue
        for item in block.get("items") or []:
            title = item.get("title", "(untitled)")
            for field in ("title", "source", "url"):
                if not item.get(field):
                    yield error("_data/press.yml", f"'{title}' has no `{field}:`.",
                                "Press entries need a title, outlet and link.")
            url = item.get("url")
            if url and not str(url).startswith(("http://", "https://")):
                yield error("_data/press.yml", f"'{title}' has a link that isn't a full address: {url}",
                            "External links must start with https://.")
            doi = norm_doi(item.get("doi"))
            if doi and doi in excluded_dois(manual):
                yield warn("_data/press.yml",
                           f"'{title}' cites DOI {doi}, which is on the `exclude:` list and "
                           "so isn't shown on the site.",
                           "The coverage will appear but won't link to a paper. Confirm that's intended.")
            elif doi and doi not in known:
                yield error("_data/press.yml",
                            f"'{title}' cites DOI {doi}, which isn't in the publications data.",
                            "Check the DOI, or add the paper to publications_manual.yml.")
            image = item.get("image")
            if image and not asset_exists(image):
                yield error("_data/press.yml", f"'{title}' has image `{image}`, which isn't in the repo.",
                            "Upload it to assets/img/news/, or remove the `image:` line.")


def check_facilities():
    facilities = load("facilities.yml")
    if not facilities:
        return
    featured = [f for f in facilities if isinstance(f, dict) and f.get("featured")]
    if len(featured) > 1:
        names = ", ".join(f.get("name", "?") for f in featured)
        yield error("_data/facilities.yml",
                    f"{len(featured)} facilities are marked `featured: true` ({names}).",
                    "Remove `featured: true` from all but one.")
    elif not featured:
        yield warn("_data/facilities.yml", "No facility is marked `featured: true`.",
                   "The Facilities page leads with the featured one.")

    for facility in facilities:
        if not isinstance(facility, dict):
            continue
        name = facility.get("name", "(unnamed)")
        photo = facility.get("photo")
        if photo:
            if not asset_exists(photo):
                yield error("_data/facilities.yml",
                            f"'{name}' has photo `{photo}`, which isn't in the repo.",
                            "Upload it to assets/img/facilities/, or remove the `photo:` line.")
            if not facility.get("photo_alt"):
                yield error("_data/facilities.yml", f"'{name}' has a photo but no `photo_alt:`.",
                            "Write one sentence describing what's visible. Screen readers need "
                            "it, and WCAG AA requires it.")


def check_updates():
    """News types must match across updates.yml, the issue form and
    issue_to_change.py, otherwise a valid form gets dropped or mislabelled."""
    updates = load("updates.yml")

    script_types = set()
    script_path = os.path.join(REPO_ROOT, "scripts", "issue_to_change.py")
    if os.path.exists(script_path):
        with open(script_path, encoding="utf-8") as fh:
            match = re.search(r"NEWS_TYPES\s*=\s*\{(.*?)\}", fh.read(), re.S)
        if match:
            script_types = set(re.findall(r'"([^"]+)"', match.group(1)))

    form_types = set()
    form_path = os.path.join(FORMS_DIR, "add-news.yml")
    if os.path.exists(form_path):
        with open(form_path, encoding="utf-8") as fh:
            form = yaml.safe_load(fh)
        for field in form.get("body", []) or []:
            if field.get("id") == "type":
                form_types = set(field.get("attributes", {}).get("options", []) or [])

    if script_types and form_types and script_types != form_types:
        only_form = ", ".join(sorted(form_types - script_types)) or "none"
        only_script = ", ".join(sorted(script_types - form_types)) or "none"
        yield error(".github/ISSUE_TEMPLATE/add-news.yml vs scripts/issue_to_change.py",
                    "The news-type options in the issue form and the script disagree. "
                    f"Only in the form: {only_form}. Only in the script: {only_script}.",
                    "Make the two lists identical, or someone can pick a type the "
                    "automation then rejects.")

    allowed = script_types or form_types
    for block in updates or []:
        if not isinstance(block, dict):
            continue
        for event in block.get("events") or []:
            if not isinstance(event, dict):
                continue
            snippet = (event.get("text") or "")[:60]
            etype = event.get("type")
            if allowed and etype not in allowed:
                yield error("_data/updates.yml",
                            f"News entry '{snippet}…' has type '{etype}', which isn't allowed.",
                            f"Use one of: {', '.join(sorted(allowed))}.")
            date = event.get("date")
            if date and not re.match(r"^[A-Z][a-z]+ \d{4}$", str(date)):
                yield error("_data/updates.yml",
                            f"News entry '{snippet}…' has date '{date}'.",
                            "Timeline dates are 'Month YYYY', e.g. June 2026.")
            if not event.get("text"):
                yield error("_data/updates.yml", "A news entry has no `text:`.",
                            "Each entry needs a sentence describing what happened.")


def check_person_roles_match_form():
    """Every role in the add-person form must map to a real people.yml group."""
    form_path = os.path.join(FORMS_DIR, "add-person.yml")
    script_path = os.path.join(REPO_ROOT, "scripts", "issue_to_change.py")
    if not (os.path.exists(form_path) and os.path.exists(script_path)):
        return

    with open(form_path, encoding="utf-8") as fh:
        form = yaml.safe_load(fh)
    form_roles = set()
    for field in form.get("body", []) or []:
        if field.get("id") == "role":
            form_roles = {r.lower() for r in field.get("attributes", {}).get("options", []) or []}

    with open(script_path, encoding="utf-8") as fh:
        match = re.search(r"ROLE_GROUP\s*=\s*\{(.*?)\n\}", fh.read(), re.S)
    script_roles = set(re.findall(r'"([^"]+)":', match.group(1))) if match else set()

    missing = form_roles - script_roles
    if missing:
        yield error(".github/ISSUE_TEMPLATE/add-person.yml vs scripts/issue_to_change.py",
                    f"The form offers role(s) the script can't file: {', '.join(sorted(missing))}.",
                    "Add them to ROLE_GROUP in issue_to_change.py, mapped to a group id in "
                    "people.yml, or picking that role breaks the automation.")

    people = load("people.yml")
    group_ids = {g.get("id") for g in (people or {}).get("groups", []) or []}
    if match and group_ids:
        for group in set(re.findall(r':\s*"([^"]+)"', match.group(1))):
            if group not in group_ids:
                yield error("scripts/issue_to_change.py",
                            f"ROLE_GROUP files someone into group '{group}', which doesn't "
                            "exist in _data/people.yml.",
                            f"Existing groups: {', '.join(sorted(i for i in group_ids if i))}. "
                            "Add the group (it can be empty) or fix the mapping.")


def check_openings():
    openings = load("openings.yml")
    if not openings:
        return
    for key in ("undergrad", "graduate", "postdoc"):
        block = openings.get(key)
        if not isinstance(block, dict):
            yield error("_data/openings.yml", f"There's no `{key}:` section.",
                        "The Join page expects undergrad, graduate and postdoc.")
            continue
        if not isinstance(block.get("open"), bool):
            yield error("_data/openings.yml",
                        f"`{key}.open` is '{block.get('open')}', which isn't true or false.",
                        "Write `open: true` or `open: false` unquoted. Quoted \"true\" is "
                        "text, and the pill will be wrong.")
        for note in ("open_note", "closed_note"):
            if not block.get(note):
                yield error("_data/openings.yml", f"`{key}` has no `{note}:`.",
                            "Both are needed so the pill reads correctly either way.")


def check_review_list():
    """A review.yml entry pointing at a deleted file silently stops being
    reviewed: the failure the reminder exists to prevent."""
    config = load("review.yml")
    if not config:
        return
    for item in config.get("items", []) or []:
        what = item.get("what", "(unnamed)")
        target = item.get("file")
        if not target:
            yield error("_data/review.yml", f"'{what}' has no `file:`.",
                        "Point it at the file to review.")
        elif not os.path.exists(os.path.join(REPO_ROOT, target)):
            yield error("_data/review.yml",
                        f"'{what}' points at `{target}`, which doesn't exist.",
                        "Renamed or deleted. Fix the path, or remove the entry.")
        if not item.get("last_reviewed"):
            yield error("_data/review.yml", f"'{what}' has no `last_reviewed:` date.",
                        "Nothing can tell when the next check is due. Use today's date if "
                        "you've just looked at it.")
        every = item.get("every_months")
        if not isinstance(every, int) or every < 1:
            yield error("_data/review.yml",
                        f"'{what}' has `every_months: {every}`, which isn't a whole "
                        "number of months.",
                        "Use a plain number, e.g. `every_months: 12`.")


CHECKS = [
    check_people,
    check_review_list,
    check_research,
    check_publications,
    check_pub_links,
    check_press,
    check_facilities,
    check_updates,
    check_person_roles_match_form,
    check_openings,
]


def main():
    # One unparseable file makes everything downstream noise.
    parse_problems = list(check_yaml_parses())
    problems = parse_problems if parse_problems else [
        p for check in CHECKS for p in check()
    ]

    errors = [p for p in problems if not p.warning]
    warnings = [p for p in problems if p.warning]

    for label, items in (("PROBLEM", errors), ("Note", warnings)):
        for p in items:
            print(f"\n{label}: {p.where}\n  {p.what}")
            if p.fix:
                print(f"  → {p.fix}")

    print()
    if errors:
        print(f"{len(errors)} problem(s) found"
              + (f", {len(warnings)} note(s)" if warnings else "")
              + ". The website would build, but it would be wrong. Please fix the above.")
        return 1
    if warnings:
        print(f"All content checks passed ({len(warnings)} note(s) above, nothing blocking).")
        return 0
    print("All content checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
