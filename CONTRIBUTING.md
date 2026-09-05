# Submitting updates

Three ways in, least to most technical. Every change is checked before it
publishes.

## 1. Issue form (anyone with a GitHub account)

**Issues → New issue**, pick a form, submit:

- ➕ Add or update a lab member
- 📄 Add a conference paper, talk, or poster
- 📣 Add a news milestone
- 📰 Add press coverage

A bot drafts the change, opens a pull request and links it on your issue. A
maintainer merges, which closes the issue. A missing field gets a comment
instead. Journal articles update themselves from OpenAlex.

## 2. Edit the file

Edit the `_data/*.yml` file on github.com (pencil icon), **Commit → Propose
changes → open a pull request**. Formats: [CONTENT-GUIDE.md](CONTENT-GUIDE.md).

## 3. Maintainer: applying a submission by hand

Only if the bot couldn't draft one. Paste at the top of the list, fill in the
values, commit on a branch, close the issue.

**Member → `_data/people.yml`**, under the group's `members:`
```yaml
      - name: Jane Doe
        role: PhD Researcher          # as submitted; sets the bird
        start: 2026
        pronouns: they/them
        field: "Mechanical & Aerospace Engineering"
        email: jdoe@ucdavis.edu       # contact links: omit for undergraduates
        linkedin: https://www.linkedin.com/in/jane-doe
        note: One short line about their project.
        # photo: /assets/img/people/jane-doe.jpg
```

**Conference item → `_data/publications_manual.yml`**, top of `conference:`
```yaml
  - title: "Exact title"
    authors: "J. Doe, C. Harvey"
    venue: "AIAA SciTech Forum, Orlando, FL"
    year: 2026
    type: conference
    note: Talk            # or Poster; delete for a paper
    doi: "https://…"      # omit if none
```

**News → `_data/updates.yml`**, top of the current year's `events:`
```yaml
    - { date: "June 2026", type: award, text: "What happened, in a sentence." }
```

**Press → `_data/press.yml`**, under the year's `items:`
```yaml
    - title: "Article headline"
      source: "Outlet name"
      url: "https://…"
      doi: "10.1098/rsif.2025.0868"   # if given
      tag: Center                      # else the reason tag; never both
```

## Who merges

One or two web stewards (GitHub **Write** access, **Settings → Collaborators**),
ideally rotated yearly, alongside the PI. A steward can't break the live site:
the worst case is an unmerged pull request.

## Checks on every pull request

Content validation (names, DOIs, image paths resolve), links and images,
WCAG 2.1 AA scan, media budget. The PI's direct pushes are checked after the
fact (MAINTENANCE.md). Monthly publications PR, quarterly staleness sweep and
Dependabot run on top.

## YAML

Two-space indents, no tabs, a space after every colon (`name: Ada`). The
content check names the file and line if this is wrong.
