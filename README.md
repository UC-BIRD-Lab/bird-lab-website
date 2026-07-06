# BIRD Lab website

The public website for the **Bio-Informed Research & Design (BIRD) Lab** at UC
Davis: built as a static [Jekyll](https://jekyllrb.com/) site, hosted free on
**GitHub Pages**, and designed so that non-technical lab members can keep it
current by editing plain text files.

> **New here? Read these in order:**
> [CONTENT-GUIDE.md](CONTENT-GUIDE.md) (edit content) ·
> [CONTRIBUTING.md](CONTRIBUTING.md) (submit updates) ·
> [MAINTENANCE.md](MAINTENANCE.md) (keep it running: publish, preview, fixes) ·
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
On recent macOS this can fail on the `eventmachine` gem: see the fix in
[MAINTENANCE.md](MAINTENANCE.md#preview-locally-before-publishing-optional).

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
│   ├── pub_links.yml        data/code/figure per paper, matched by DOI
│   ├── research.yml        research themes + active projects
│   ├── updates.yml         news/milestones timeline
│   ├── press.yml           "In the news" external coverage
│   ├── recognition.yml     home-page honors + "featured in" media
│   ├── funders.yml         home-page "supported by" logos
│   ├── collaborators.yml   home-page "in partnership with" org strip
│   ├── gallery.yml         "scenes from the lab" photos
│   ├── facilities.yml      facilities: tagline, specs, capabilities, funding
│   └── navigation.yml      top menu
├── _layouts/  _includes/ ← page templates (rarely touched)
├── assets/              ← CSS, JS, logo, images
├── scripts/             ← publications sync · press-entry helper · image tools
├── CONTRIBUTING.md      ← how lab members submit updates + delegation
└── .github/             ← workflows (deploy · publications · checks) + issue forms
```

**Rule of thumb:** content lives in `_data/*.yml` and the `_guide/*.md` /
`*.md` pages. Design lives in `assets/` and `_layouts/`. You can do almost all
day-to-day updates without touching the design.

---

## How it's built (in brief)

Static **Jekyll** site on **GitHub Pages**: content in Markdown + YAML, no runtime
services, three GitHub Actions (deploy · publications sync · link + accessibility
check) plus Dependabot. Journal articles and DOI-bearing conference papers sync
monthly from **OpenAlex** by the PI's **ORCID** and open a pull request for
review; DOI-less talks and posters and everything else are hand-curated in
`_data/`. The design prioritizes **maintainability → accessibility (WCAG 2.1
AA) → scientific communication → automation → design**, in that order, so where
they traded off the higher priority won (e.g. plain editable data files over a
headless CMS).

The decisions and trade-offs behind all of this are in
[ARCHITECTURE.md](ARCHITECTURE.md).

---

## License / credit
Content © BIRD Lab, UC Davis. Lab logo is the lab's own mark. Built with Jekyll;
hosted on GitHub Pages.
