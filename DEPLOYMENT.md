# Deployment

How to put the BIRD Lab site online with **GitHub Pages**. You do this once;
after that, every change you commit republishes automatically. No command line
is strictly required — the steps below use github.com.

---

## One-time setup

### 1. Create the repository
1. Sign in to [github.com](https://github.com) with the lab account.
2. Click **New repository**. Name it (e.g. `birdlab-website`). Make it **Public**.
3. Upload these files: on the empty repo page choose **uploading an existing
   file**, drag in the whole project folder, and **Commit**.
   *(Or, if you use git: `git init`, `git add .`, `git commit`, `git remote add
   origin …`, `git push -u origin main`.)*

### 2. Turn on GitHub Pages (Actions build)
1. In the repo, go to **Settings → Pages**.
2. Under **Build and deployment → Source**, choose **GitHub Actions**.
3. That's it — the included `Build & deploy site` workflow takes over. Open the
   **Actions** tab to watch the first build; when it's green, your site is live.

### 3. Set the site URL
GitHub Pages serves either at `https://<user>.github.io/<repo>/` (project site)
or at a custom domain.

- **Project site:** in `_config.yml` set
  `baseurl: "/<repo>"` and `url: "https://<user>.github.io"`, then commit.
- **Custom domain (e.g. `birdlab.ucdavis.edu`):**
  1. In **Settings → Pages → Custom domain**, enter the domain and save (this
     creates a `CNAME` file).
  2. Ask UC Davis IT to add a DNS **CNAME** record pointing the subdomain to
     `<user>.github.io`.
  3. In `_config.yml` set `url: "https://birdlab.ucdavis.edu"` and `baseurl: ""`.
  4. Tick **Enforce HTTPS** once the certificate is issued.

### 4. Set the Member Portal link
The Member Portal page simply links to your private Notion workspace. In
`_config.yml`, set:
```yaml
member_portal_url: "https://www.notion.so/your-workspace-link"
```
Commit. Access is managed inside Notion; the site itself has no login.

### 5. Allow the publications bot to open pull requests
So the monthly publications sync can open PRs:
**Settings → Actions → General → Workflow permissions** → select **Read and write
permissions** and tick **Allow GitHub Actions to create and approve pull
requests** → **Save**.

---

## Day-to-day: how publishing works

```
edit a file on github.com  ─►  commit  ─►  "Build & deploy" Action runs  ─►  site updates (~1–2 min)
```

You never deploy by hand. Every commit to the **main** branch rebuilds and
republishes. Check the **Actions** tab if something doesn't appear — a red run
means the build failed (see Troubleshooting in [MAINTENANCE.md](MAINTENANCE.md)).

You can commit either **on github.com** (edit → Commit, as above) **or from your
own computer with RStudio** (next section). Both push to `main` and trigger the
same rebuild — use whichever you prefer.

---

## Editing locally and pushing with RStudio

Repository: **https://github.com/UC-BIRD-Lab/bird-lab-website.git**

RStudio has a built-in **Git** panel, so you can edit the site on your computer
and publish without the command line. Once it's set up, the loop is always the
same:

```
edit files  ─►  Git tab: Pull  ─►  Stage (tick boxes)  ─►  Commit (+message)  ─►  Push  ─►  site rebuilds
```

### One-time setup

1. **Install Git** if you don't have it. macOS: run `xcode-select --install` in
   Terminal. Windows: install [Git for Windows](https://git-scm.com/download/win).
   Then in RStudio confirm **Tools → Global Options → Git/SVN** shows a Git path.

2. **Install the helper R packages** (they make GitHub sign-in painless):
   ```r
   install.packages(c("usethis", "gitcreds"))
   ```

3. **Tell Git who you are** (use the email on your GitHub account):
   ```r
   usethis::use_git_config(user.name = "Christina Harvey",
                           user.email = "harvey@ucdavis.edu")
   ```

4. **Create a GitHub access token.** GitHub no longer accepts your password over
   HTTPS — you authenticate with a Personal Access Token (PAT) instead. Run:
   ```r
   usethis::create_github_token()   # opens GitHub; keep the defaults, click "Generate", copy the token
   gitcreds::gitcreds_set()         # paste the token when prompted
   ```
   You only do this once per computer; RStudio remembers it.

5. **Connect your project folder to the repo.** Pick the case that matches you:

   **A — You already have the site folder on your computer** (most likely). Open
   the RStudio **Terminal** (Tools → Terminal → New Terminal), make sure you're in
   the project folder, and run:
   ```bash
   git init
   git branch -M main
   git remote add origin https://github.com/UC-BIRD-Lab/bird-lab-website.git
   git add .
   git commit -m "Initial local commit"
   git pull origin main --allow-unrelated-histories   # merges anything already on GitHub (e.g. the README)
   git push -u origin main
   ```
   Then turn the folder into an RStudio Project so the Git pane appears:
   **File → New Project → Existing Directory →** choose this folder → **Create
   Project**. (You'll now see a **Git** tab in the top-right pane.)

   **B — Start from a fresh copy of the repo.** **File → New Project → Version
   Control → Git**, paste the URL above, pick a location, **Create Project**.
   RStudio clones the repo and the Git pane is ready immediately.

### Day-to-day: push a change

1. Edit and **save** your files (e.g. `_data/people.yml`).
2. Open the **Git** tab (top-right pane).
3. Click **Pull** (⬇) **first** — this grabs anything changed on GitHub since you
   last synced (a browser edit, or a merged publications PR). *Always pull before
   you push.*
4. **Stage** your changes: tick the checkbox next to each changed file.
5. Click **Commit**, write a short message ("Add new student to People"), and
   click **Commit**.
6. Click **Push** (⬆). That's it — GitHub's Action rebuilds and the site updates
   in ~1–2 minutes (watch the **Actions** tab).

### If something goes wrong

- **"Push rejected" / "non-fast-forward":** GitHub is ahead of you. Click **Pull**
  to merge, resolve any conflict RStudio flags, then **Push** again.
- **A merge conflict** (rare): RStudio marks the file with `<<<<<<<` / `>>>>>>>`
  sections. Keep the correct lines, delete the markers, save, then Stage → Commit
  → Push.
- **Auth keeps failing:** rerun `gitcreds::gitcreds_set()` and paste a fresh token
  from `usethis::create_github_token()`.
- **You don't see a Git tab:** the folder isn't an RStudio Project with Git — redo
  step 5 (New Project → Existing Directory), or check Tools → Global Options →
  Git/SVN.

> **Note:** build artifacts (`_site/`, `.jekyll-cache/`, etc.) are already listed
> in `.gitignore`, so RStudio won't offer to commit them — only your real edits
> show up in the Git pane. That's expected.

For a friendly, in-depth reference on Git + RStudio, see
[Happy Git and GitHub for the useR](https://happygitwithr.com/).

---

## Preview changes before publishing (optional)

**Easiest — no Ruby on your machine:** run `./serve.sh` (needs Docker Desktop).
It runs Jekyll inside a container and serves the site at http://localhost:4000.
This avoids compiling any native gems on your Mac.

**Native Ruby:**
```bash
bundle install                # one-time
bundle exec jekyll serve      # then open http://localhost:4000
```

**Or skip local preview entirely** — push to a branch and open a pull request;
GitHub builds it, and merging to `main` publishes.

### Troubleshooting native `bundle install` on macOS

On recent macOS, `bundle install` can fail while building the **`eventmachine`**
gem (Jekyll uses it only for the live-reload server) with errors like
`use of undeclared identifier '__builtin_ctzg'`. This is an incompatibility
between that old gem and Apple's newest C++ headers — not your setup. Options, in
order of least hassle:

1. **Use Docker instead:** `./serve.sh` (above). Recommended.
2. **Preview on GitHub:** push and let the Actions build show the site.
3. **Fix the toolchain (only if you want native Jekyll):** make sure Conda is not
   active (`conda deactivate`), then refresh the Command Line Tools
   (`sudo rm -rf /Library/Developer/CommandLineTools && xcode-select --install`).
   If it still fails, your Apple compiler is older than your SDK — installing a
   newer compiler via `brew install llvm` and building with it can resolve it, but
   Docker is far simpler.

---

## Rollback
Every change is a commit. To undo one: open the repo's **commit history**, find
the last good commit, and use **Revert** (or `git revert <sha>`). The site
rebuilds from the reverted state automatically.
