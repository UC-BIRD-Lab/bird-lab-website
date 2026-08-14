# Maintaining the BIRD Lab website

> **How this file was written.** Website documentation, largely written by AI
> (Claude) from the code in this repository. Christina checked that it works, not
> that every sentence is how she would put it. The site-wide statement is on the
> [Accessibility page](accessibility.md) under *How this site is made*.

Keeping the site current and healthy. No coding required.

**How it works in one sentence:** almost everything on the site is filled in from
small text files in `_data/`. You edit one, open a pull request, and GitHub
rebuilds the site a minute or two after it merges.

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
   "Watch & listen" strip: just add `--media video|podcast|radio|model` (see
   CONTENT-GUIDE → *Videos, podcasts & 3D models*).
3. **Add notable milestones.** Awards, talks, funding, new members, graduations →
   add a one-line entry to the top of the current year in `_data/updates.yml`.
   Member names link themselves automatically; to link out to a paper or event,
   add `link:` and `link_text:` (CONTENT-GUIDE → *Add a news milestone*).
   *Easiest:* file the **📣 Add a news milestone** issue form; the [issue-to-pr Action](.github/workflows/issue-to-pr.yml)
   drafts the entry and opens a PR automatically; you just merge it (which closes the
   issue). Prefer the paper helper for a new paper: `python scripts/add_press.py --paper <doi>`.
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

On **github.com** (the ✏️ pencil on any file): click **Commit changes**, keep the
default *"Create a new branch and start a pull request"*, then merge the pull
request once its checks go green.

**Locally in RStudio:** make a branch first (Git pane → the purple branch icon),
then **Pull → tick the changed files → Commit → Push** and open a pull request.
Setup and troubleshooting: [Editing on your computer with
RStudio](#editing-on-your-computer-with-rstudio) below.

> **One important habit: don't push many times in a row.** Every push republishes
> the site, and GitHub limits how often a site can deploy. If you push five times
> in five minutes, deployments start to **queue up and stall**. Instead, make all
> your edits, push **once**, and wait for the green ✓ on the **deploy** step
> before pushing again. If a deploy ever sits on "queued" and times out, that's
> the cause: wait about an hour and run it once.

### Why your change goes through a pull request

`main` is protected. Changes reach the live site through a **pull request**,
which runs the checks (build, broken links, missing images, content validation)
before anything publishes. Push straight to `main` and GitHub refuses it; your
work stays safely on your computer. Make a branch and open a pull request.

Editing on github.com does this for you, offering *"Create a new branch for this
commit and start a pull request"* by default.

> **Recorded exception.** The PI (@christinaharvey) can push directly to `main`.
> This is deliberate: she makes most edits, and requiring a pull request for
> every one-line fix would discourage keeping the site current, which is the
> bigger risk. The checks still run on those pushes; they report a failure a
> minute later rather than preventing it. **Remove this exception once a second
> person has write access.**

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

## Checking your content before you publish

The build will happily publish a page that is **wrong**: a `lead:` spelled
differently from the People page, a DOI matching no paper, a photo path pointing
at a file nobody uploaded. Jekyll renders all of these without complaint.

`scripts/validate_content.py` looks for that. To run it yourself:

```
python3 scripts/validate_content.py
```

It prints each problem, its file, and what to do, or "All content checks
passed". It also runs on every pull request, so forgetting is fine: you'll see a
red ✗ on the **Content validation** check with the same explanation.

It confirms that every project lead and news name matches someone in
`people.yml`; every DOI in `pub_links.yml`, `press.yml` and `research.yml`
matches a real publication; every image path points at a file that exists; every
facility photo has alt text; exactly one facility is featured; and the issue-form
dropdowns still agree with what `scripts/issue_to_change.py` accepts, so nobody
can file a valid form the automation then drops.

To add a check, copy one of the small `check_*` functions and write the message
for someone who has never opened that file. `scripts/test_validate_content.py`
proves each check still fires; run it after editing.

---

## The quarterly review issue

Four times a year (5 January, April, July, October) a robot lists what may have
gone out of date in **one GitHub issue**, *"Site review: what needs a human
look"*. It rewrites that same issue each quarter and closes it when nothing is
outstanding. It changes no content and closes no positions; it only asks.

**What it watches:**

- Lab Guide pages whose `reviewed:` date has passed its interval.
- Everything listed in `_data/review.yml`: funding eligibility, safety training
  and contacts, CALI rates, recruiting status, facilities, the portal link.
- The banner in `_data/announcement.yml`, which keeps advertising a position
  after its deadline passes. You get a warning two weeks out and a flag after.

**To clear an item:** look at it, fix anything wrong, then set its date to today.
That's `last_reviewed:` in `_data/review.yml`, or `reviewed:` in a guide page's
front matter. Setting the date after confirming nothing needed changing is a fine
outcome; "someone checked" is the signal worth recording.

**To add, remove or re-time something,** edit `_data/review.yml`. The content
check will tell you if you point it at a file that doesn't exist.

Run it yourself any time:

```
python3 scripts/review_sweep.py
```

Broken external links are checked separately, also quarterly, and also into a
single issue each (one for the Lab Guide, one for publication and press links).

> GitHub switches off scheduled workflows after 60 days without repository
> activity. Weekly Dependabot pull requests should keep this alive, but if no
> review issue appears for two consecutive quarters, check the Actions tab.

---

## Gem versions (`Gemfile.lock`)

**You will almost never touch this**, but it's the difference between a site
that keeps building and one that breaks by itself.

`Gemfile` names the software loosely ("Jekyll 4.3 or newer"). `Gemfile.lock`
records the exact version of each one used, including the dozens of libraries
Jekyll depends on underneath. Both are committed, and `./serve.sh` and GitHub
Actions read the same lockfile, so your preview and the live site are built from
identical parts.

Without it, every publish picks whatever was newest that morning, so a
stranger's release, not any change of yours, can break the site. Dependabot also
needs the lockfile: with nothing to bump, its weekly check does nothing.

**To move to newer gems on purpose:**

```
./scripts/update-lockfile.sh     # rewrites Gemfile.lock
```

Then commit `Gemfile.lock` **on a branch** and open a pull request. The checks
build with the new versions and tell you whether they're safe; if it fails, close
the pull request and nothing reaches the live site.

If `./serve.sh` complains that the Gemfile and lockfile disagree, someone edited
`Gemfile` without rerunning that script. Run it, and commit both files.

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

**No editing at all:** members can submit a person, paper, news item or press
link through **Issues → New issue**; the automation drafts the change and opens a
pull request. Full workflow in [CONTRIBUTING.md](CONTRIBUTING.md).

### Adding member photos
Put a roughly square image (≈ 600×600 px, ≤ 80 KB) in `assets/img/people/` and add
`photo: /assets/img/people/firstname-lastname.jpg` to that person. No photo gives
a clean initials avatar, so nothing looks broken.

---

## Publications: how the automation works

**Journal articles are automatic.** The **Update publications** Action runs on the
1st of each month (and on demand from **Actions → Run workflow**). It reads the
PI's ORCID (`0000-0002-2830-0844`) from OpenAlex and opens a pull request adding
new articles to `_data/publications.yml`. You review and merge.

- **It's safe.** The bot only *adds* articles with a new DOI and fills in a
  missing `date`. It never overwrites text you've edited.
- **Open-access links are automatic.** When a paper is open access the sync fills
  `oa_url:` and an **Open access** button appears. To point at a specific copy
  instead, set `preprint:` or `pdf:` for that DOI in `_data/pub_links.yml`.
- **Announcing a paper:** once the PR merges, run
  `python scripts/add_press.py --paper <doi> --topic "plain-language hook"` to
  draft the news entry (lab authors auto-link) plus LinkedIn/Instagram captions.
  `--append` inserts the entry; the captions print for you to post.
- **Ordering within a year** uses each entry's `date:`. The sync backfills older
  entries on its next run, or run `python scripts/update_publications.py` now.
- **Fix a wrong author or venue** directly in `_data/publications.yml`. Future
  syncs match on DOI and keep your version.
- **Conference papers, posters, talks and blogs** aren't in OpenAlex. Add them to
  `_data/publications_manual.yml`.

**Data, code and figures** live in `_data/pub_links.yml`, matched by DOI. Separate
on purpose, so the sync can never overwrite them:

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
- **Yearly:** confirm **funders** and any external links (guides, forms) still work. (Two Actions do most of this for you: [guide-link-check](.github/workflows/guide-link-check.yml) sweeps the lab guide's external links each July, and [link-rot-check](.github/workflows/link-rot-check.yml) verifies every paper **DOI**, **press/media** URL, and per-paper **data/code/preprint** link each January, filing an issue only for links that are genuinely dead. You can run either any time from **Actions → Run workflow**, or locally with `python scripts/check_links.py`.)
- **Images stay light automatically.** A pull request touching `assets/` fails if
  anything is over budget (1600 px wide; ~300 KB JPEG, ~600 KB PNG, ~2.5 MB video).
  Once merged, the [optimize-images Action](.github/workflows/optimize-images.yml)
  compresses what it can and opens a PR with the smaller files. Run it yourself
  with `python scripts/optimize_images.py` (`--check` to only list problems).
- **When convenient:** merge Dependabot's dependency-bump PRs, one at a time.

---

## Keeping it accessible (when you edit)

- **Don't skip heading levels**: use `##` then `###`, never jump `##` → `####`.
- **Write real link text**: "see the [funding guide](…)", not "click [here](…)".
- **Every informative image needs `alt` text;** decorative images get empty `alt`.
- **Don't hard-code text colours.** The theme already meets AA contrast; the
  palette is the `:root` block at the top of `assets/css/style.css`. If you change
  one, check it with the [WebAIM Contrast
  Checker](https://webaim.org/resources/contrastchecker/): 4.5:1 for body text.
  The **Accessibility** check will fail the pull request if you go under.

---

## The accessibility check a person has to do

The automatic scan on every pull request covers roughly a third of WCAG 2.1 AA.
It can tell that an image has alt text; it cannot tell whether that alt text is
useful. It can find a missing label; it cannot tell you the page is unusable with
a keyboard. This is the rest of it.

Run through this **once a year**, and after any change to the layout, the
navigation, or the home page hero. It takes about twenty minutes. When you're
done, set `last_reviewed:` on the accessibility entry in `_data/review.yml` so the
quarterly sweep knows.

### 1. Keyboard only (5 min)

Put the mouse away. Open the home page and press <kbd>Tab</kbd> repeatedly.

- [ ] The first <kbd>Tab</kbd> reveals a **Skip to content** link, and
      <kbd>Enter</kbd> jumps past the navigation.
- [ ] Every stop has a **visible** outline. Nothing is focused invisibly.
- [ ] Focus order follows the visual order down the page.
- [ ] The hero **pause button** can be reached and pressed, and its label changes
      between Pause and Play.
- [ ] Narrow the window until the **menu button** appears. It opens with
      <kbd>Enter</kbd>, <kbd>Tab</kbd> walks the links, and it closes again.
- [ ] **Publications:** the search box and the type dropdown both work using only
      the keyboard.
- [ ] **Lab Guide hub:** same for its search box.
- [ ] **Join:** the funding table's show/hide button works from the keyboard.
- [ ] Focus never gets stuck. You can always <kbd>Tab</kbd> forward or
      <kbd>Shift</kbd>+<kbd>Tab</kbd> back out of anything.

### 2. Reduced motion (2 min)

macOS: **System Settings → Accessibility → Display → Reduce motion.**

- [ ] Reload the home page. The background video is **gone**, not merely paused,
      and its pause button is gone with it.
- [ ] The animated wing graphic has stopped.
- [ ] Nothing else on the page moves on its own.

Turn the setting back off afterwards.

### 3. Zoom and narrow screens (3 min)

- [ ] Zoom to **400%** (<kbd>Cmd</kbd>+<kbd>+</kbd>). Text reflows into one
      column. No horizontal scrolling, nothing overlapping or cut off.
- [ ] Same again with the browser window dragged to about **320px** wide.
- [ ] The specification and rate tables (Facilities, CALI) stay readable, with any
      sideways scrolling happening inside the table rather than the whole page.

### 4. Read the alt text (5 min)

The scanner checks alt text *exists*. Only a person can check it *says something*.

- [ ] Open People, Publications, Facilities, CALI and News. For each image ask:
      if this had not loaded, would the page still make sense?
- [ ] Icons sitting next to text that already says the same thing have `alt=""`,
      not a description repeating it.
- [ ] No alt text begins "Image of" or "Photo of".
- [ ] Facility and CALI photos describe what is actually in the picture, not just
      the name of the room.

### 5. Links and headings (3 min)

- [ ] No link reads "here", "this", or "read more" when you look at it on its own.
- [ ] Skim one long Lab Guide page reading only its headings. They step down one
      level at a time, and the sequence alone tells you the shape of the page.

### 6. Colour is never the only signal (2 min)

- [ ] The Join page status pills still make sense with the colour ignored.
- [ ] Publication type pills (journal, conference, poster) are readable as words.

### 7. Video (1 min)

- [ ] The hero video is silent and can be paused.
- [ ] Any video that carries information rather than decoration has a caption or a
      short text description beside it.

**If something fails,** open an issue rather than only fixing it. A pattern that
broke once tends to break again, and the issue is what tells the next person to
look for it.

---

## If something breaks

**A build failed (red ✗ in Actions).** Open the failed run and read the last red
lines. Usually a YAML typo: a missing space after a colon, or a tab instead of
spaces. **Content validation** names the file and line for you. YAML indents with
**two spaces**, never tabs.

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
`main` is protected. Merge it yourself; you're on the bypass list.

**A submitted issue form didn't become a pull request.** Check **Actions →
issue-to-pr** for a red ✗; the log says which field was missing or invalid.

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
