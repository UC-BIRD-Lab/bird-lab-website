# Maintaining the BIRD Lab website

Everything you need to keep the site current and healthy: written so any lab
member can do it, no coding required.

**How the site works in one sentence:** almost everything on the site is filled
in from small text files in `_data/`; you edit a file, publish it, and GitHub
rebuilds the site automatically in a minute or two.

- **Copy-paste templates for every kind of edit:** [CONTENT-GUIDE.md](CONTENT-GUIDE.md)
- **Editing locally, previewing, and Git fixes:** [Editing on your computer with RStudio](#editing-on-your-computer-with-rstudio) (below)
- **Letting members submit changes without editing files:** [CONTRIBUTING.md](CONTRIBUTING.md)

---

## The monthly check (about 10 minutes)

Do these once a month. None of them require the command line.

1. **Merge the publications update.** On the 1st, a bot checks ORCID for new
   journal articles and opens a **pull request**. Open the **Pull requests** tab,
   review the new entry (title, authors, venue, DOI), fix anything, and **Merge**.
   No PR that month just means no new papers: that's normal.
2. **Add any new press** (~2 min each). Run the helper:
   `python scripts/add_press.py "<url>" --doi <doi> --featured`: it reads the
   outlet, headline, and author, downloads the lead image (only with `--featured`),
   and prints a paste-ready block (add `--append` to insert it for you). Include the
   paper's `doi:` and the story shows up as the "In the news" badge on Publications.
   Prefer to do it by hand? Template and all flags are in CONTENT-GUIDE → *Add press
   coverage*. The same helper adds a **video, podcast, or radio interview** to the
   "Watch & listen" strip — just add `--media video|podcast|radio|model` (see
   CONTENT-GUIDE → *Videos, podcasts & 3D models*).
3. **Add notable milestones.** Awards, talks, funding, new members, graduations →
   add a one-line entry to the top of the current year in `_data/updates.yml`.
   Member names link themselves automatically.
4. **Update People** (`_data/people.yml`):
   - **Add** a new member, or **promote** someone by changing their `role:` (the bird badge updates itself).
   - **Retire** someone: cut their whole block from `groups:` and paste it under `alumni:`, then add a `now:` line. Their `start:` (year joined) and any `linkedin:` carry over, and a LinkedIn icon appears beside their name in the alumni table.
5. **Confirm the Join page** hiring status still reads correctly. All three
   status pills (undergrad, graduate, postdoc) are one-line `open:` toggles in
   `_data/openings.yml`.
6. **Glance at the Actions tab.** Every run should have a green ✓. A red ✗ means a
   build failed: see *If something breaks* below.
7. **(Optional) enrich a new paper.** When a paper's data/code/figure are ready,
   add them in `_data/pub_links.yml` (see *Publications* below).

---

## How to publish a change

If you edit on **github.com** (the ✏️ pencil on any file): just click **Commit
changes**. Done: the site rebuilds itself.

If you edit **locally in RStudio**: in the **Git** pane, **Pull → tick the changed
files → Commit (with a message) → Push**. Full setup and troubleshooting is in
[Editing on your computer with RStudio](#editing-on-your-computer-with-rstudio) below.

> **One important habit: don't push many times in a row.** Every push republishes
> the site, and GitHub limits how often a site can deploy. If you push five times
> in five minutes, deployments start to **queue up and stall**. Instead, make all
> your edits, push **once**, and wait for the green ✓ on the **deploy** step
> before pushing again. If a deploy ever sits on "queued" and times out, that's
> the cause: wait about an hour and run it once.

---

## Editing on your computer with RStudio

Prefer to edit locally instead of on github.com? RStudio has a built-in **Git**
pane, so you can publish without the command line. Repo:
`https://github.com/UC-BIRD-Lab/bird-lab-website.git`.

**One-time setup**

1. **Install Git.** macOS: run `xcode-select --install` in Terminal. Windows:
   install [Git for Windows](https://git-scm.com/download/win). In RStudio,
   **Tools → Global Options → Git/SVN** should show a Git path.
2. **Install helper packages:** `install.packages(c("usethis", "gitcreds"))`.
3. **Tell Git who you are** (your own name, and the email on your GitHub account):
   ```r
   usethis::use_git_config(user.name = "Your Name", user.email = "you@ucdavis.edu")
   ```
4. **Create a GitHub token** (GitHub no longer accepts passwords over HTTPS). Run
   `usethis::create_github_token()` (opens GitHub; keep defaults, Generate, copy the
   token), then `gitcreds::gitcreds_set()` and paste it. Once per computer.
5. **Connect the project to the repo.** If you already have the folder: in the
   RStudio **Terminal**, from the project folder, run `git init`, `git branch -M
   main`, `git remote add origin <repo URL>`, `git add .`, `git commit -m "…"`,
   `git pull origin main --allow-unrelated-histories`, `git push -u origin main`;
   then **File → New Project → Existing Directory** to get the Git pane. Or start
   fresh: **File → New Project → Version Control → Git** and paste the repo URL.

**Day-to-day: push a change**

1. Edit and **save** your files.
2. In the **Git** pane, click **Pull** (⬇) *first* to grab anything changed on
   GitHub (a browser edit, or a merged publications PR). Always pull before you push.
3. **Stage** (tick the changed files), **Commit** with a short message, then
   **Push** (⬆). The site rebuilds in ~1–2 minutes (watch the Actions tab).

**If something goes wrong**

- **"Push rejected" / "non-fast-forward":** GitHub is ahead. Click **Pull**,
  resolve any conflict RStudio flags, then **Push** again.
- **Merge conflict:** RStudio marks the file with `<<<<<<<` / `>>>>>>>`. Keep the
  right lines, delete the markers, save, then Stage → Commit → Push.
- **Auth keeps failing:** rerun `gitcreds::gitcreds_set()` with a fresh token.
- **No Git tab:** the folder isn't an RStudio Project with Git; redo step 5.
- **Nothing appears under Actions / the site never builds:** the `.github/` folder
  probably wasn't committed. RStudio's Git pane **hides dotfiles**, so the
  checkboxes skip `.github/` and `.gitignore`. In the Terminal:
  `git add .github .gitignore && git commit -m "Add workflows" && git push`.
- **Large first push fails** (`HTTP 400` / `unexpected disconnect`): the push is
  choking on Git's small buffer. Run once
  `git config --global http.postBuffer 524288000` and
  `git config --global http.version HTTP/1.1`, then push again.

Build artifacts (`_site/`, `.jekyll-cache/`, …) are in `.gitignore`, so RStudio
won't offer to commit them. For a friendly Git + RStudio reference, see
[Happy Git and GitHub for the useR](https://happygitwithr.com/).

---

## Preview locally before publishing (optional)

- **Easiest (no Ruby):** `./serve.sh` (needs Docker Desktop); serves
  http://localhost:4000 with no native gems to compile.
- **Native Ruby:** `bundle install` once, then `bundle exec jekyll serve`.
- **Or skip it:** push to a branch, open a pull request, and let GitHub build it.

On recent macOS, `bundle install` can fail building the **`eventmachine`** gem
(`use of undeclared identifier '__builtin_ctzg'`): an incompatibility between that
old gem and Apple's newest headers, not your setup. Easiest fix: use `./serve.sh`
(Docker), or preview on GitHub via a pull request. Only if you want native Jekyll,
make sure Conda is off (`conda deactivate`) and refresh the Command Line Tools
(`sudo rm -rf /Library/Developer/CommandLineTools && xcode-select --install`).

---

## Undo a change (rollback)

Every change is a commit. To undo one: open the repo's **commit history**, find
the last good commit, and click **Revert** (or `git revert <sha>`). The site
rebuilds from the reverted state automatically.

---

## The updates you'll do most

Each is a small edit to one file; full templates are in
[CONTENT-GUIDE.md](CONTENT-GUIDE.md).

| To change… | Edit this file |
| --- | --- |
| A team member (add / promote / move to alumni) | `_data/people.yml` |
| A news milestone | `_data/updates.yml` |
| Press coverage | `_data/press.yml` |
| Data / code / a figure for a paper | `_data/pub_links.yml` |
| A conference paper, talk, or poster | `_data/publications_manual.yml` |
| A research project | `_data/research.yml` |
| A facility (tagline, specs, funding) | `_data/facilities.yml` |
| Funders shown on the home page | `_data/funders.yml` |
| Partner organizations (home "in partnership with") | `_data/collaborators.yml` |
| Honors & "featured in" media | `_data/recognition.yml` |
| A Lab Guide page | the matching file in `_guide/` |
| A lab operations role (add / edit / retire) | `_data/roles.yml` |
| Mark a guide page reviewed (no edits needed) | set `reviewed:` in its front matter to today |
| The top menu | `_data/navigation.yml` |
| Site title, URLs, portal link, PI links, analytics | `_config.yml` |

**No editing at all:** members can submit a person, paper, news item, or press
link through the repo's **Issues → New issue** forms; a maintainer copies the
values into the right file in seconds. Full workflow in
[CONTRIBUTING.md](CONTRIBUTING.md).

### Adding member photos
Put a roughly square image (≈ 600×600 px, ≤ 80 KB) in `assets/img/people/` and
add `photo: /assets/img/people/firstname-lastname.jpg` to that person in
`people.yml`. No photo = a clean initials avatar, so nothing ever looks broken.

---

## Publications: how the automation works

**Journal articles are automatic.** A GitHub Action, **Update publications**, runs
on the **1st of each month** (and on demand from **Actions → Run workflow**). It
reads the PI's ORCID (`0000-0002-2830-0844`) from OpenAlex and opens a pull
request adding any new articles to `_data/publications.yml`. You review and merge.

- **It's safe:** the bot only *adds* articles with a new DOI (and fills in a missing
  publication `date`); it never overwrites text you've edited, so your corrections are safe.
- **Ordering by month:** each entry stores a `date:` (`YYYY-MM-DD`) so the list sorts
  correctly *within* a year, not just by year. The sync backfills this onto older entries
  the next time it runs: to update them right now, run
  `python scripts/update_publications.py` locally and commit the result.
- **Fix a wrong author/venue:** edit the entry in `_data/publications.yml`
  directly. Future syncs keep your version (they match on DOI).
- **Conference papers, posters, talks, blogs:** OpenAlex doesn't index these:
  add them by hand in `_data/publications_manual.yml`.

**Data, code, and figures** for a paper live in `_data/pub_links.yml`, matched to
the paper by its DOI. This is separate on purpose, so the automation above can
never overwrite them. Add a data link, a code repo, and (for major papers only) a
small figure:

```yaml
- doi: "10.1098/rsif.2025.0868"
  data: "https://figshare.com/…"
  code: "https://github.com/UC-BIRD-Lab/…"
  image: /assets/img/research/perchaero.jpg   # optional; only for standout papers
```

Nothing shows until the paper itself is on the Publications page, so you can add
this the moment a paper is accepted.

---

## Occasional / yearly

- **When openings change:** flip the matching `open:` line in
  `_data/openings.yml` (undergrad, graduate, or postdoc).
- **Each term / as people move on:** review **alumni** destinations and add where people landed.
- **As the team changes:** refresh **photos** and the lab **group photo**.
- **Yearly:** confirm **funders** and any external links (guides, forms) still work. (The [guide-link-check Action](.github/workflows/guide-link-check.yml) already sweeps the lab guide's external links once a year and files an issue for any that break.)
- **When convenient:** merge Dependabot's **dependency-bump** PRs (they clear
  deprecation warnings). Because `main` is protected, merge them yourself; you're
  on the bypass list. Do them one at a time.

---

## Keeping it accessible (when you edit)

- **Don't skip heading levels**: use `##` then `###`, never jump `##` → `####`.
- **Write real link text**: "see the [funding guide](…)", not "click [here](…)".
- **Every informative image needs `alt` text;** decorative images get empty `alt`.
- **Don't hard-code text colors**: the theme already meets AA contrast. The
  palette lives in the `:root` block at the top of `assets/css/style.css` (the
  site's single stylesheet); if you change a color, re-check it
  with the [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
  (aim for 4.5:1 for body text). The **Site checks** Action re-tests links,
  images, and accessibility on every push.

---

## If something breaks

**A build failed (red ✗ in Actions).** Open the failed run and read the last red
lines. The usual cause is a YAML typo: a missing space after a colon, or a tab
instead of spaces. Paste the file into [yamllint.com](https://www.yamllint.com/)
to find the line. YAML uses **two spaces** to indent, never tabs.

**My change didn't appear.** Give it 1–2 minutes and hard-refresh. Check the
Actions tab shows a green run *after* your commit.

**The deploy is stuck on "queued" or times out.** This is GitHub throttling Pages
because too many deploys happened close together (see the publishing habit
above). Stop pushing, wait about an hour, then trigger **one** deploy
(**Actions → Build & deploy site → Run workflow**). The site stays live from the
last good deploy in the meantime.

**A page 404s.** Permalinks come from the file location. If a `_guide/` file was
renamed, its URL changed: update links to it.

**A Dependabot PR won't merge ("Cannot update this protected ref").** Expected:
`main` is protected. Merge it yourself (you're on the bypass list); if needed,
tick "Merge without waiting for requirements to be met."

**A submitted issue form needs applying.** Open the issue, copy its values into the
matching `_data/*.yml` file using the cheat-sheet in
[CONTRIBUTING.md](CONTRIBUTING.md), commit, and close the issue.

---

## Moving to a custom domain later (optional)

If the lab ever wants `birdlab.ucdavis.edu` or similar instead of
`uc-bird-lab.github.io`: request the subdomain from UC Davis IT (or buy a
domain), then in the repo go to **Settings → Pages → Custom domain**, enter it,
and keep **Enforce HTTPS** checked. GitHub writes a `CNAME` file to the repo;
your DNS host needs a matching CNAME record pointing at
`uc-bird-lab.github.io`. Afterward, update `url:` in `_config.yml` so absolute
links and the sitemap use the new address. Old links keep redirecting from the
github.io address automatically.

## Built to last

- **It's data-driven.** New students maintain it by editing text files: point
  them at [CONTENT-GUIDE.md](CONTENT-GUIDE.md) and this page. Nothing here needs a
  web developer.
- **Some numbers count themselves.** The home-page "Researchers" and "Publications"
  stats come straight from `people.yml` and `publications.yml`, so they're never out
  of date and there's no funding figure to keep updating.
- **It never shows broken images.** Photos, figures, and the group/culture shots
  only appear once their file is set, so a missing image is simply absent, never a
  broken icon.
- **It checks itself.** Every push runs link, image, and accessibility checks, so
  regressions are caught before anyone sees them.
- **Access is controlled.** Only the Graduate Students & Postdocs team (plus the
  PI) can push to `main`, and every change goes through a reviewed pull request.
