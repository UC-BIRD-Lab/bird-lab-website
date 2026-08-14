# How the automation works (a plain-English guide)

> **How this file was written.** Website documentation, largely written by AI
> (Claude) from the code in this repository. Christina checked that it works, not
> that every sentence is how she would put it. The site-wide statement is on the
> [Accessibility page](accessibility.md) under *How this site is made*.

What the little robots do, when they run, and how to change them. You don't need
to be a programmer: if you can edit a text file, you can adjust all of it.

## The rule behind all of them

Every automation is **"when X happens, run a small program, and propose the result
for a human to approve."** Nothing it does goes live on its own. It writes up a
change and waits for someone to click **Merge**. That rule is why this is safe:
the robot can only ever *suggest*.

## Two kinds of files, working as a pair

- A **workflow** is a `.yml` file in `.github/workflows/`. The recipe card: **when**
  to run, and **what steps** to take.
- A **script** is a `.py` file in `scripts/`. The worker that does the thinking.
  Scripts can also be run by hand on your own computer.

## What each robot does

| Robot (workflow file) | Runs when… | What it does | Result |
|---|---|---|---|
| **Site checks** (`site-checks.yml`) | Every pull request | Three checks: content validation, broken links & missing images, and a WCAG 2.1 AA accessibility scan | **Blocks the merge** if any fails |
| **Optimize images** (`optimize-images.yml`) | Pull requests touching `assets/`, and merges to `main` | On a PR, fails if any image, video, GIF or SVG breaks the budget. After merge, compresses what it can | Blocks the merge, or opens a PR with smaller files |
| **Build & deploy** (`deploy.yml`) | Every merge to `main` | Rebuilds and publishes | The live site updates |
| **Update publications** (`update-publications.yml`) | 1st of each month | Checks OpenAlex for new papers by your ORCID; fills in a free **Open access** link where one exists | Opens a PR editing `_data/publications.yml` |
| **Issue form to PR** (`issue-to-pr.yml`) | Someone submits a website issue form | Turns the form (news / conference / person / press) into the right `_data` entry | Opens a PR and closes the issue when you merge |
| **Quarterly review sweep** (`review-sweep.yml`) | 5 Jan / Apr / Jul / Oct | Lists content that may have gone out of date: overdue guide pages, everything in `_data/review.yml`, an expired site banner | Rewrites **one** issue, and closes it when nothing is due |
| **Guide link check** (`guide-link-check.yml`) | 12 Jan / Apr / Jul / Oct | Checks the Lab Guide's outside links | Rewrites one issue listing broken ones |
| **Link rot check** (`link-rot-check.yml`) | 19 Jan / Apr / Jul / Oct | Checks every paper DOI, press link and data/code link | Rewrites one issue listing only the genuinely dead ones |

The scheduled checks each own **one** issue and rewrite it, rather than opening a
new one every time.

Scripts you can run yourself, any time:

```
python3 scripts/validate_content.py     # the content checks
python3 scripts/review_sweep.py         # what's due for review
python3 scripts/optimize_images.py      # compress oversized images (--check to report)
python3 scripts/check_links.py          # test outbound DOI/press links
python3 scripts/add_press.py …          # draft a press entry or paper announcement
```

## How to change the common things

**How often a scheduled robot runs.** Edit the `cron:` line in its workflow. The
five fields are *minute, hour, day-of-month, month, day-of-week*; `*` means
"every", and a comma lists several. For example, in `review-sweep.yml`:

```yaml
- cron: "0 9 5 1,4,7,10 *"   # 09:00 on the 5th of Jan, Apr, Jul and Oct
```

For twice a year instead, change `1,4,7,10` to `1,7`. Times are UTC, a few hours
ahead of California.

**Image and video size limits.** The numbers near the top of
`scripts/optimize_images.py`: `MAX_WIDTH`, `JPEG_BUDGET_KB`, `PNG_BUDGET_KB`,
`VIDEO_BUDGET_KB`, `GIF_BUDGET_KB`.

**What gets reviewed, and how often.** `_data/review.yml`. Each entry has an
owner, an interval and a `last_reviewed:` date.

**The wording a robot writes** (a PR title, an issue comment) lives in the
workflow file, in quotes. Edit it like any sentence.

**A new person role or news type.** The allowed values are at the top of
`scripts/issue_to_change.py` (`ROLE_GROUP` and `NEWS_TYPES`); the matching
dropdowns are in `.github/ISSUE_TEMPLATE/`. Keep the two in sync; the content
check will fail the pull request if they drift apart.

**Run a robot right now.** **Actions** tab → pick the workflow → **Run workflow**.
Anything on a schedule has that button.

## If something looks wrong

Open the **Actions** tab and click the run with a red ✗. The last red line usually
says it plainly, and **Content validation** names the file and what to change.
Nothing is live at that point, so there's no rush. Re-run it, fix the input, or
make the change by hand. When in doubt, close the robot's pull request. That
discards the suggestion and changes nothing.
