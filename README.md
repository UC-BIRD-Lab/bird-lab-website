# BIRD Lab website

The public website for the **Bio-Informed Research & Design (BIRD) Lab** at UC
Davis — built as a static [Jekyll](https://jekyllrb.com/) site, hosted free on
**GitHub Pages**, and designed so that non-technical lab members can keep it
current by editing plain text files.

> **New here? Read these in order:**
> [CONTENT-GUIDE.md](CONTENT-GUIDE.md) (edit content) ·
> [CONTRIBUTING.md](CONTRIBUTING.md) (submit updates / delegate) ·
> [DEPLOYMENT.md](DEPLOYMENT.md) (put it online) ·
> [MAINTENANCE.md](MAINTENANCE.md) (keep it running) ·
> [ARCHITECTURE.md](ARCHITECTURE.md) (why it's built this way)

---

## Quick start (run it on your computer)

You only need this to preview changes locally. Editing through GitHub's website
(see [CONTENT-GUIDE.md](CONTENT-GUIDE.md)) needs no setup at all.

**Easiest (recommended):** install [Docker Desktop](https://www.docker.com/products/docker-desktop/), then:
```bash
./serve.sh        # builds in a container, serves http://localhost:4000
```
This avoids compiling Ruby gems on your Mac.

**Native Ruby** (if you prefer): `bundle install`, then `bundle exec jekyll serve`.
On recent macOS this can fail on the `eventmachine` gem — see the fix in
[DEPLOYMENT.md](DEPLOYMENT.md#troubleshooting-native-bundle-install-on-macos).

---

## What's where

```
.
├── _config.yml          ← site-wide settings (title, URLs, member-portal link)
├── index.html           ← Home page
├── research.html        people.html  publications.html  facilities.html
├── news.html  join.md  contact.md  portal.md  404.html
├── lab-guide/index.html ← Lab Guide hub
├── _guide/*.md          ← Lab Guide wiki pages (one file per page)
├── _data/               ← THE CONTENT YOU'LL EDIT MOST
│   ├── people.yml          team members, grouped by role
│   ├── publications.yml    journal articles (auto-updated)
│   ├── publications_manual.yml  conference papers, posters, talks, blogs
│   ├── research.yml        research themes + active projects
│   ├── updates.yml         news/milestones timeline
│   ├── press.yml           "In the news" external coverage
│   ├── recognition.yml     home-page honors + "featured in" media
│   ├── funders.yml         home-page "supported by" logos
│   ├── partners.yml        partners / affiliates strip
│   ├── gallery.yml         "scenes from the lab" photos
│   ├── facilities.yml      facility descriptions
│   └── navigation.yml      top menu
├── _layouts/  _includes/ ← page templates (rarely touched)
├── assets/              ← CSS, JS, logo, images
├── scripts/             ← publications sync + image-optimization scripts
├── CONTRIBUTING.md      ← how lab members submit updates + delegation
└── .github/             ← workflows (deploy · publications · checks) + issue forms
```

**Rule of thumb:** content lives in `_data/*.yml` and the `_guide/*.md` /
`*.md` pages. Design lives in `assets/` and `_layouts/`. You can do almost all
day-to-day updates without touching the design.

---

## The four planning questions, answered

### 1 · Content inventory
The current site/lab-guide content was catalogued and mapped to its new home.
Full table in [ARCHITECTURE.md → Content inventory](ARCHITECTURE.md#1-content-inventory).
In short: public "who we are / what we do / get involved" pages became the main
nav; the how-to lab-guide pages became a searchable **wiki**; explicitly internal
pages were **excluded** and point to the private Notion portal.

### 2 · Sitemap
Home · Research · People · Publications · Facilities · Lab Guide (wiki) · News ·
Join · Contact · Member Portal. Diagram in
[ARCHITECTURE.md → Sitemap](ARCHITECTURE.md#2-sitemap).

### 3 · Architecture
Static **Jekyll** site on **GitHub Pages**, content in Markdown + YAML, zero
runtime services, three GitHub Actions + Dependabot. Rationale and trade-offs in
[ARCHITECTURE.md → Architecture](ARCHITECTURE.md#3-architecture-decision).

### 4 · Publication workflow
Journal articles sync automatically from **OpenAlex** (by the PI's **ORCID**) via
a monthly GitHub Action that opens a **pull request** for human review. The
committed file is always the source of truth, so the site never breaks if the API
is down. Conference work is curated by hand. Full details in
[MAINTENANCE.md → Publications](MAINTENANCE.md#keeping-publications-current).

---

## Priorities this build optimizes for

In the project's stated order: **maintainability → accessibility (WCAG 2.1 AA) →
scientific communication → automation → design quality → visual effects.** Where
these traded off, the higher priority won — e.g. plain editable data files over
a fancier headless CMS, and semantic HTML that works without JavaScript.

## License / credit
Content © BIRD Lab, UC Davis. Lab logo is the lab's own mark. Built with Jekyll;
hosted on GitHub Pages.
