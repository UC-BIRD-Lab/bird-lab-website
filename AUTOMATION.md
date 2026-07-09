# How the automation works (a plain-English guide)

This explains, in everyday terms, the little robots that keep the site tidy — what
they do, when they run, and how to change them yourself. You do **not** need to be a
programmer. If you can edit a text file and read a sentence, you can adjust all of it.

## The one idea to hold in your head

Every automation is just **"when X happens, run a small program, and propose the
result as a pull request for a human to approve."** Nothing it does goes live on its
own. It writes up a change and waits for you (or a steward) to click **Merge**. That
single rule is why this is safe: the robot can only ever *suggest*.

## Two kinds of files, working as a pair

Each automation is made of two files that do different jobs:

- A **workflow** — a `.yml` file in `.github/workflows/`. Think of it as the
  *recipe card*: it says **when** to run ("every month," "when an image is added,"
  "when an issue is filed") and **what steps** to take (usually: run a script, then
  open a pull request).
- A **script** — a `.py` file in `scripts/`. This is the *worker* that does the
  actual thinking (reads a DOI, compresses an image, turns an issue into a data
  entry). Scripts can also be run by hand on your own computer.

The workflow decides *when*; the script decides *what*. Change the timing? Edit the
workflow. Change the behavior or wording? Edit the script.

## What each robot does

| Robot (workflow file) | Runs when… | What it does | Result |
|---|---|---|---|
| **Update publications** (`update-publications.yml`) | 1st of each month | Checks OpenAlex for new papers by your ORCID; also fills in a free **Open access** link when a paper has one | Opens a PR editing `_data/publications.yml` |
| **Issue form to PR** (`issue-to-pr.yml`) | Someone submits a website issue form | Turns the form (news / conference / person / press) into the right `_data` entry | Opens a PR, comments on the issue, and closes it when you merge |
| **Optimize images** (`optimize-images.yml`) | An image is added to `assets/img/` | Shrinks anything too large (max 1600px wide; ~300 KB JPEG / ~600 KB PNG) | Opens a PR with the smaller files |
| **Link rot check** (`link-rot-check.yml`) | Once a year (Jan 6) | Checks every paper DOI, press link, and data/code link still works | Opens an **issue** listing only the genuinely dead ones |
| **Guide link check** (`guide-link-check.yml`) | Once a year (Jul 5) | Checks the Lab Guide's outside links | Opens an issue if any broke |
| **Site checks** (`site-checks.yml`) | Every change | Tests links, images, and accessibility | Flags problems before they ship |
| **Build & deploy** (`deploy.yml`) | Every merge to `main` | Rebuilds and publishes the site | The live site updates |

There are also two helper scripts you run **yourself** when you want to, not on a
schedule: `add_press.py` (draft a news/press entry or a paper announcement with
social captions) and `check_links.py` / `optimize_images.py` (the manual versions of
the two robots above).

## How to change the common things (with exact spots)

**Change how often a scheduled robot runs.** Open its workflow file and edit the
`cron:` line. The five numbers mean *minute, hour, day-of-month, month, day-of-week*,
and `*` means "every." For example, in `link-rot-check.yml`:

```yaml
- cron: "0 8 6 1 *"   # minute 0, hour 8, day 6, month 1 (January), any weekday
```

To run it in July instead of January, change the `1` to `7`. To run the publications
check on the 15th instead of the 1st, open `update-publications.yml` and change
`"0 13 1 * *"` to `"0 13 15 * *"`. (Times are UTC — a few hours ahead of California.)

**Change the image size limits.** Open `scripts/optimize_images.py` and edit the
three numbers near the top: `MAX_WIDTH`, `JPEG_BUDGET_KB`, `PNG_BUDGET_KB`.

**Change the wording a robot writes** (a PR title, an issue comment): that text lives
in the workflow file, in quotes — edit it like any sentence.

**Add a new person role or news type:** the allowed values live at the top of
`scripts/issue_to_change.py` (`ROLE_GROUP` and `NEWS_TYPES`). The matching dropdown
options live in the form files under `.github/ISSUE_TEMPLATE/`. Keep the two in sync.

**Run a robot right now, without waiting:** go to the **Actions** tab, click the
workflow on the left, then **Run workflow**. (Anything on a schedule also has this
button.) Or run its script on your own computer, e.g. `python scripts/check_links.py`.

## Why this is safe

- **Nothing publishes itself.** Robots open pull requests; a human merges. You are
  always the last step.
- **`main` is protected.** Even you merge through a PR, so a bad edit can't land
  silently, and every change is auto-checked (links, images, accessibility) first.
- **A robot that fails is harmless.** If a script hits a problem, the workflow just
  stops and (for the issue robot) leaves a comment explaining what to fix. It never
  half-writes a file — the inserts are careful and only touch the one spot they mean
  to. Your comments and formatting are preserved.
- **You can always fall back to doing it by hand.** Every robot is just a shortcut
  for an edit you could make yourself in the `_data/*.yml` files (see CONTENT-GUIDE.md
  and MAINTENANCE.md). The automation is a convenience, never a dependency.

## If something looks wrong

Open the **Actions** tab and click the run with a red ✗ to read what happened (the
last red line usually says it plainly). Nothing is live yet at that point, so there's
no rush. You can re-run it, fix the input, or just make the change by hand. When in
doubt, close the robot's pull request — that discards its suggestion and changes
nothing on the site.
