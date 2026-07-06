# Keeping the BIRD Lab site up to date

The goal: keep the site current with as little effort as possible, and make it
hard to break the live site (every change is reviewed and auto-checked first).

There are **three ways** to get an update in, from least to most technical.

---

## 1. The easy way: submit a form (no coding, anyone in the lab)

Go to the repo's **Issues → New issue**, pick the matching form, fill it in, submit:

- ➕ **Add or update a lab member**
- 📄 **Add a conference paper, talk, or poster**
- 📣 **Add a news milestone**
- 📰 **Add press coverage**

That's it. The submission lands as a tidy GitHub issue for a maintainer to apply.
You only need a free GitHub account. (Journal articles aren't here: they update
themselves from OpenAlex.)

## 2. The direct way: edit the file (a little GitHub comfort)

Edit the relevant `_data/*.yml` file on github.com (pencil icon ✏️), then
**Commit → Propose changes → open a pull request**. The exact formats are in
[CONTENT-GUIDE.md](CONTENT-GUIDE.md). A check runs automatically (see below); a
maintainer reviews and merges. The site rebuilds itself.

## 3. The maintainer way: applying a submission

If you're a **web steward** (see below), you turn an issue into a commit. This
takes ~30 seconds with the cheat-sheet below: open the file, paste the block at
the **top** of the list, fill in the submitted values, commit.

---

## Maintainer cheat-sheet (issue → file)

**New member → `_data/people.yml`** (add under the right group's `members:`)
```yaml
      - name: Jane Doe
        role: PhD Researcher          # exactly as submitted; sets the bird
        start: 2026
        pronouns: they/them
        field: "Mechanical & Aerospace Engineering"
        email: jdoe@ucdavis.edu
        linkedin: https://www.linkedin.com/in/jane-doe
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
```

After committing, close the issue with a note like "Live on the next build 👍".

---

## Web stewards: who merges

Merging is handled by a small number of **web stewards**: one or two trusted lab
members (rotated yearly is ideal), alongside the PI. If you're a steward, you
handle steps 2–3 above; the PI only steps in for big changes.

Because every change goes through a pull request and the automated checks, a
steward can't accidentally break the live site: the worst case is a PR that
fails its checks and doesn't get merged.

> Steward access (GitHub **Write** permission) is granted by the repo owner under
> **Settings → Collaborators**.

## What protects the site automatically

- **`site-checks.yml`** builds every pull request and flags broken links/images
  and accessibility issues before anything merges.
- **`update-publications.yml`** opens a monthly PR with new journal articles from
  OpenAlex: just review and merge.
- **Dependabot** keeps dependencies current with small PRs.

## The one formatting rule

The `.yml` files use **spaces, not tabs**, two spaces per indent level, and a
space after every colon (`name: Ada`, not `name:Ada`). The forms avoid this
entirely; it only matters if you hand-edit.
