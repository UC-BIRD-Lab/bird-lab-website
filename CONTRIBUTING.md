# Keeping the BIRD Lab site up to date

> **How this file was written.** Website documentation, largely written by AI
> (Claude) from the code in this repository. Christina checked that it works, not
> that every sentence is how she would put it. The site-wide statement is on the
> [Accessibility page](accessibility.md) under *How this site is made*.

Keep the site current with as little effort as possible, and make it hard to
break. Every change is reviewed and checked automatically first.

**Three ways** to get an update in, from least to most technical.

---

## 1. The easy way: submit a form (no coding, anyone in the lab)

Go to the repo's **Issues → New issue**, pick the matching form, fill it in, submit:

- ➕ **Add or update a lab member**
- 📄 **Add a conference paper, talk, or poster**
- 📣 **Add a news milestone**
- 📰 **Add press coverage**

You only need a free GitHub account. (Journal articles aren't here; they update
themselves from OpenAlex.)

**The forms apply themselves.** A bot drafts the matching change, opens a pull
request and comments on your issue with the link. A maintainer checks it and
merges; merging closes your issue. Nothing to copy by hand. If a required field
is missing, the bot comments to say what to fix instead.

## 2. The direct way: edit the file (a little GitHub comfort)

Edit the relevant `_data/*.yml` file on github.com (pencil icon ✏️), then
**Commit → Propose changes → open a pull request**. Formats are in
[CONTENT-GUIDE.md](CONTENT-GUIDE.md). The checks run automatically; a maintainer
reviews and merges, and the site rebuilds itself.

## 3. The maintainer way: applying a submission

Most submissions arrive as a ready-made pull request, so there's nothing to
apply. If a bot couldn't draft one, the cheat-sheet below takes about 30 seconds:
open the file, paste the block at the **top** of the list, fill in the submitted
values, commit on a branch.

---

## Maintainer cheat-sheet (issue → file)

**New member → `_data/people.yml`** (add under the right group's `members:`)
```yaml
      - name: Jane Doe
        role: PhD Researcher          # exactly as submitted; sets the bird
        start: 2026
        pronouns: they/them
        field: "Mechanical & Aerospace Engineering"
        email: jdoe@ucdavis.edu           # personal contact links (email, linkedin,
        linkedin: https://www.linkedin.com/in/jane-doe  # orcid, etc.): omit for undergraduates (privacy)
        note: One short line about their project.
        # photo: /assets/img/people/jane-doe.jpg   # after adding the image
```

**Conference item → `_data/publications_manual.yml`** (top of `conference:`)
```yaml
  - title: "Exact title"
    authors: "J. Doe, C. Harvey"
    venue: "AIAA SciTech Forum, Orlando, FL"
    year: 2026
    type: conference
    note: Talk            # or Poster; delete this line for a Paper
    doi: "https://…"      # omit if none
```

**News milestone → `_data/updates.yml`** (top of the current year's `events:`)
```yaml
    - { date: "June 2026", type: award, text: "What happened, in a sentence." }
```

**Press → `_data/press.yml`** (under the matching year's `items:`)
```yaml
    - title: "Article headline"
      source: "Outlet name"
      url: "https://…"
      doi: "10.1098/rsif.2025.0868"   # if the issue gave a DOI (shows a "Paper" pill)
      tag: Center                      # else use the issue's reason tag (no doi + tag together)
```
The issue form collects an optional DOI and, for stories not tied to a paper, a reason
tag (`Center` / `Award` / `Funding` / `Profile` / `Feature`). Add whichever the issue
provides: a story has **either** a `doi:` **or** a `tag:`, not both.

After committing, close the issue with a note like "Live on the next build 👍".

---

## Web stewards: who merges

Merging is handled by a small number of **web stewards**: one or two trusted lab
members, ideally rotated yearly, alongside the PI. Stewards handle steps 2–3; the
PI steps in for big changes.

A steward can't accidentally break the live site. Every change goes through a
pull request that must pass the checks, so the worst case is a pull request that
stays unmerged.

> Steward access (GitHub **Write** permission) is granted by the repo owner under
> **Settings → Collaborators**.

## What protects the site automatically

Every pull request must pass before it can merge (the PI's direct pushes are checked after the fact instead; see MAINTENANCE.md):

- **Content validation**: names, DOIs and image paths actually resolve, so a
  page can't publish something untrue.
- **Links and images**: nothing internal is broken or missing.
- **Accessibility**: a WCAG 2.1 AA scan of every page.
- **Media budget**: no oversized image or video reaches the site.

On top of that, **Update publications** opens a monthly PR with new articles from
OpenAlex, a **quarterly sweep** flags content that may have gone stale, and
**Dependabot** keeps dependencies current.

## The one formatting rule

The `.yml` files use **spaces, not tabs**, two per indent level, and a space
after every colon (`name: Ada`, not `name:Ada`). The forms avoid this entirely;
it only matters if you hand-edit. If you get it wrong, the content check names
the file and line.
