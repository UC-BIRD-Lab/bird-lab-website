# Maintaining the BIRD Lab website

Almost everything on the site is filled in from small text files in `_data/`.
Edit one, open a pull request, and GitHub rebuilds the site a minute or two after
it merges. Templates: [CONTENT-GUIDE.md](CONTENT-GUIDE.md). Issue forms for
members: [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Monthly (about 10 minutes)

1. **Merge the publications PR.** On the 1st a bot checks OpenAlex for new
   journal articles. Review title, authors, venue, DOI; merge. No PR means no new
   papers, unless the run is red in **Actions** (OpenAlex unreachable): re-run it.
2. **Add press:** `python scripts/add_press.py "<url>" --doi <doi> --featured`
   (add `--append` to insert; `--media video|podcast|radio|model` for the "Watch &
   listen" strip).
3. **Add milestones** to the top of the current year in `_data/updates.yml`, or
   file the 📣 issue form and merge the PR it opens. New paper:
   `python scripts/add_press.py --paper <doi>`.
4. **People:** add, promote (change `role:`), or move to `alumni:` with a `now:`.
5. **Join page:** the three `open:` toggles in `_data/openings.yml` still true.
6. **Actions tab:** all green. Red: see *If something breaks*.
7. Optional: add data/code/figure for a new paper in `_data/pub_links.yml`.

---

## Publishing a change

On github.com: pencil icon, **Commit changes**, keep *Create a new branch and
start a pull request*, merge when checks are green. In RStudio: branch, then
Pull → tick files → Commit → Push, open a PR.

> Don't push several times in a row. Each push redeploys and GitHub throttles
> Pages; deploys then queue and stall. Push once, wait for the green ✓ on
> **deploy**. If a deploy sits on "queued" and times out, wait an hour and run
> one.

`main` is protected: changes go through a pull request, which runs the checks
(build, links, images, content) first. A direct push is refused.

> **Exception:** the PI (@christinaharvey) can push directly to `main`, so
> one-line fixes don't stall. Checks still run and report after the fact.
> Remove the exception once a second person has write access.

> **Bot PRs aren't checked** (publications sync, issue forms, image
> compression): GitHub doesn't run checks on PRs a workflow opens. Push any
> commit to the bot's branch to run them, or review the one-file diff by eye.

---

## Editing in RStudio

Repo: `https://github.com/UC-BIRD-Lab/bird-lab-website.git`.

**Once**

1. Install Git (macOS: `xcode-select --install`; Windows:
   [Git for Windows](https://git-scm.com/download/win)). **Tools → Global
   Options → Git/SVN** should show a path.
2. `install.packages(c("usethis", "gitcreds"))`
3. `usethis::use_git_config(user.name = "Your Name", user.email = "you@ucdavis.edu")`
4. Token: `usethis::create_github_token()` (keep defaults, copy), then
   `gitcreds::gitcreds_set()` and paste.
5. Project: **File → New Project → Version Control → Git**, paste the repo URL.
   Existing folder instead: in the Terminal, `git init`, `git branch -M main`,
   `git remote add origin <url>`, `git add .`, `git commit -m "…"`,
   `git pull origin main --allow-unrelated-histories`, `git push -u origin main`,
   then **File → New Project → Existing Directory**.

**Each time:** save, **Pull** first, Stage → Commit → **Push**. The site
rebuilds in 1–2 minutes.

**Problems**

- "Push rejected" / "non-fast-forward": Pull, resolve, Push.
- Merge conflict: keep the right lines between `<<<<<<<` / `>>>>>>>`, delete the
  markers, save, commit.
- Auth failing: `gitcreds::gitcreds_set()` with a fresh token.
- No Git tab: not an RStudio project with Git; redo step 5.
- Nothing under Actions: the Git pane hides dotfiles, so `.github/` was never
  committed. `git add .github .gitignore && git commit -m "Add workflows" && git push`.
- Large first push fails (`HTTP 400`): `git config --global http.postBuffer 524288000`
  and `git config --global http.version HTTP/1.1`, push again.

Reference: [Happy Git and GitHub for the useR](https://happygitwithr.com/).

---

## Preview locally (optional)

- `./serve.sh` (Docker Desktop) serves http://localhost:4000 with no Ruby.
- Native: `bundle install` once, then `bundle exec jekyll serve`.
- Or push a branch and let the PR build it.

On recent macOS `bundle install` can fail on the `eventmachine` gem
(`__builtin_ctzg`): an old gem vs Apple's headers. Use `./serve.sh`, or
`conda deactivate` and reinstall the Command Line Tools
(`sudo rm -rf /Library/Developer/CommandLineTools && xcode-select --install`).

---

## Content check

Jekyll happily renders a `lead:` that matches nobody, a DOI matching no paper,
or a photo path with no file. `python3 scripts/validate_content.py` finds these
and runs on every PR (the **Content validation** check). It verifies project
leads and news names against `people.yml`; DOIs in `pub_links.yml`, `press.yml`
and `research.yml` against the publications; image paths; facility alt text;
exactly one featured facility; issue-form dropdowns against
`scripts/issue_to_change.py`.

To add a check, copy a `check_*` function and write the message for someone who
has never opened that file; `scripts/test_validate_content.py` proves each
check fires.

---

## Quarterly review issue

On 5 January, April, July and October a bot rewrites one issue, *"Site review:
what needs a human look"*, and closes it when nothing is due. It changes no
content. It watches Lab Guide pages past their `reviewed:` interval, everything
in `_data/review.yml`, and the banner deadline in `_data/announcement.yml`
(warning two weeks out, flag after).

Clear an item: check it, set `last_reviewed:` (review.yml) or `reviewed:` (guide
front matter) to today. Run locally: `python3 scripts/review_sweep.py`.

Dead external links are checked quarterly too, one issue for the Lab Guide and
one for publication/press links.

> GitHub disables scheduled workflows after 60 days without repository
> activity. Weekly Dependabot PRs keep it alive; if no review issue appears for
> two quarters, check Actions.

---

## Gem versions (`Gemfile.lock`)

`Gemfile.lock` pins the exact gem versions; `./serve.sh` and Actions both read
it, so a stranger's release can't break the site. To update on purpose:
`./scripts/update-lockfile.sh`, commit `Gemfile.lock` on a branch, open a PR. If
`./serve.sh` says Gemfile and lockfile disagree, run the script and commit both.

---

## Undo a change

Open the commit history, find the last good commit, **Revert** (or
`git revert <sha>`). The site rebuilds.

---

## Where things are

| To change… | Edit |
| --- | --- |
| Team member | `_data/people.yml` |
| News milestone | `_data/updates.yml` |
| Press | `_data/press.yml` |
| Data / code / figure for a paper | `_data/pub_links.yml` |
| Conference paper, talk, poster | `_data/publications_manual.yml` |
| Research project | `_data/research.yml` |
| Facility | `_data/facilities.yml` |
| Funders (home) | `_data/funders.yml` |
| Partner organizations (home) | `_data/collaborators.yml` |
| Honors, "featured in" | `_data/recognition.yml` |
| Lab Guide page | `_guide/` |
| Lab operations role | `_data/roles.yml` |
| Mark a guide page reviewed | `reviewed:` in its front matter |
| Menu | `_data/navigation.yml` |
| Title, URLs, portal link, PI links, analytics | `_config.yml` |

Member photos: ~600×600 px, ≤ 80 KB, in `assets/img/people/`, plus `photo:` on
the person.

---

## Publications automation

**Update publications** runs on the 1st (or **Actions → Run workflow**), reads
the PI's ORCID (`0000-0002-2830-0844`) from OpenAlex, and opens a PR adding new
DOIs to `_data/publications.yml`. It only adds entries and backfills a missing
`date`; edits you make (author, venue) are kept, matched on DOI. Open-access
papers get `oa_url:` and an **Open access** button; override with `preprint:` or
`pdf:` in `_data/pub_links.yml`. Conference papers, posters and talks go in
`_data/publications_manual.yml`. Works before `MIN_YEAR` in the script are
ignored (OpenAlex merges in another C. Harvey's 1980s papers).

Announce a paper after the PR merges:
`python scripts/add_press.py --paper <doi> --topic "plain-language hook"` drafts
the news entry and social captions (`--append` inserts the entry).

---

## Occasional

- Openings change: `open:` in `_data/openings.yml`.
- People move on: alumni `now:` lines; refresh photos and the group photo.
- Yearly: funders. Links are checked by
  [guide-link-check](.github/workflows/guide-link-check.yml) and
  [link-rot-check](.github/workflows/link-rot-check.yml) (quarterly, one issue
  each; locally `python scripts/check_links.py`).
- Images: a PR touching `assets/` fails over budget (numbers at the top of
  `scripts/optimize_images.py`); after merge
  [optimize-images](.github/workflows/optimize-images.yml) compresses and opens
  a PR. Locally `python scripts/optimize_images.py` (`--check` to list only).
- Merge Dependabot PRs one at a time.

---

## Accessibility when editing

- Heading levels step one at a time.
- Real link text, not "here".
- Informative images need `alt`; decorative ones get `alt=""`.
- Don't hard-code text colours; the palette is the `:root` block in
  `assets/css/style.css`. Body text needs 4.5:1
  ([WebAIM checker](https://webaim.org/resources/contrastchecker/)); the
  **Accessibility** check fails a PR under that.

---

## Yearly manual accessibility check (~20 min)

The PR scan covers roughly a third of WCAG 2.1 AA: it sees that alt text exists,
not whether it helps. Do this yearly and after layout, navigation or hero
changes, then set `last_reviewed:` on the accessibility entry in
`_data/review.yml`.

**Keyboard only (5 min).** Tab through the home page.
- [ ] First Tab shows **Skip to content**; Enter jumps past the nav.
- [ ] Every stop has a visible outline; order follows the page.
- [ ] Hero pause button reachable; label switches Pause/Play.
- [ ] Narrow window: menu button opens with Enter, Tab walks it, it closes.
- [ ] Publications search and type dropdown; Lab Guide search; Join funding
      show/hide: all work by keyboard.
- [ ] Focus never gets stuck.

**Reduced motion (2 min).** macOS: System Settings → Accessibility → Display.
- [ ] Home video gone (not paused) and its button with it; wing graphic still;
      nothing moves on its own. Turn the setting back off.

**Zoom and narrow (3 min).**
- [ ] 400% zoom: one column, no horizontal scroll, nothing cut off.
- [ ] Window ~320 px wide: same; Facilities and CALI tables scroll inside the
      table, not the page.

**Alt text (5 min).** People, Publications, Facilities, CALI, News.
- [ ] If an image hadn't loaded, would the page still make sense?
- [ ] Icons beside matching text have `alt=""`.
- [ ] Nothing starts "Image of" / "Photo of"; facility photos describe the
      picture, not the room name.

**Links and headings (3 min).**
- [ ] No link reads "here" / "read more" on its own.
- [ ] One long guide page read by headings alone still makes sense.

**Colour (2 min).**
- [ ] Join status pills and publication type pills work with colour ignored.

**Video (1 min).**
- [ ] Hero video silent and pausable; informative videos have a caption or text.

If something fails, open an issue as well as fixing it.

---

## If something breaks

- **Red ✗ in Actions:** read the last red lines. Usually YAML: missing space
  after a colon, or a tab. **Content validation** names file and line.
- **Change didn't appear:** wait 1–2 minutes, hard-refresh, check for a green
  run after your commit.
- **Deploy stuck on "queued":** Pages throttling. Stop pushing, wait an hour,
  **Actions → Build & deploy site → Run workflow** once.
- **404:** permalinks follow file location; a renamed `_guide/` file changed URL.
- **Dependabot PR "Cannot update this protected ref":** merge it yourself.
- **Issue form didn't become a PR:** **Actions → issue-to-pr** log names the
  bad field.

---

## Custom domain (optional)

Request the subdomain from UC Davis IT, then **Settings → Pages → Custom
domain**, keep **Enforce HTTPS**. GitHub writes a `CNAME` file; DNS needs a CNAME
to `uc-bird-lab.github.io`. Update `url:` in `_config.yml`. Old github.io links
redirect.
