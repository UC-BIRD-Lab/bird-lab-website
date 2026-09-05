# BIRD Lab website

> **How this file was written.** Website documentation, largely written by AI
> (Claude) from the code in this repository. Christina checked that it works, not
> that every sentence is how she would put it. The site-wide statement is on the
> [Accessibility page](accessibility.md) under *How this site is made*.

The public website for the **Bio-Informed Research & Design (BIRD) Lab** at UC Davis. A static [Jekyll](https://jekyllrb.com/) site on **GitHub Pages**, built so non-technical lab members can keep it current by editing plain text files.

> **New here? Read these in order:**
> - [CONTENT-GUIDE.md](CONTENT-GUIDE.md) (edit content)
> - [CONTRIBUTING.md](CONTRIBUTING.md) (submit updates)
> - [MAINTENANCE.md](MAINTENANCE.md) (keep it running: publish, preview, fixes)
> - [AUTOMATION.md](AUTOMATION.md) (the robots, in plain English: what they do & how to change them)
> - [ARCHITECTURE.md](ARCHITECTURE.md) (why it's built this way)

---

## Quick start (run it on your computer)

Only needed to preview changes locally. Editing through GitHub's website (see [CONTENT-GUIDE.md](CONTENT-GUIDE.md)) needs no setup.

**Recommended:** install [Docker Desktop](https://www.docker.com/products/docker-desktop/), then:
```bash
./serve.sh        # builds in a container, serves http://localhost:4000
```
This uses the same Ruby and `Gemfile.lock` as the live build, and avoids compiling gems on your Mac.

**Native Ruby:** `bundle install`, then `bundle exec jekyll serve`. On recent macOS this can fail on the `eventmachine` gem. Fix in [MAINTENANCE.md](MAINTENANCE.md#preview-locally-before-publishing-optional).

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
│   ├── openings.yml        Join-page recruiting status (one-line toggles)
│   ├── facilities.yml      facilities: tagline, specs, capabilities, funding
│   ├── safety.yml  funding.yml  media.yml  roles.yml
│   ├── announcement.yml    site-wide banner (with its expiry date)
│   ├── review.yml          what to re-check, and how often
│   ├── cali*.yml           CALI facility page: specs, rates, gallery, milestones
│   └── navigation.yml      top menu
├── _layouts/  _includes/ ← page templates (rarely touched)
├── assets/              ← CSS, JS, logo, images
├── scripts/             ← publications sync · press helper · content + link checks · image tools
├── CONTRIBUTING.md      ← how lab members submit updates + delegation
└── .github/             ← workflows + issue forms
```

**Rules of thumb:**
- Content lives in `_data/*.yml` and the `_guide/*.md` / `*.md` pages.
- Design lives in `assets/` and `_layouts/`. Almost all day-to-day updates leave the design alone.

---

## How it's built (in brief)

- Static **Jekyll** on **GitHub Pages**: Markdown and YAML, no runtime services, no database. GitHub Actions handle deployment, the publications sync, the pre-merge checks and the scheduled reviews; Dependabot keeps gems current.
- Changes go through a pull request that must pass three checks: content validation, broken links and missing images, and a WCAG 2.1 AA scan. (The PI can push to `main` directly; the checks then run after the fact. See MAINTENANCE.md.)
- Journal articles and DOI-bearing conference papers sync monthly from **OpenAlex** by the PI's **ORCID** and open a pull request for review. Talks and posters without a DOI are hand-curated in `_data/`.
- Priorities, in order: **maintainability → accessibility (WCAG 2.1 AA) → scientific communication → automation → design.** Where two conflicted the higher one won: plain editable data files over a headless CMS, for instance.

Decisions and trade-offs: [ARCHITECTURE.md](ARCHITECTURE.md).

---

## License / credit
Content © BIRD Lab, UC Davis. Lab logo is the lab's own mark. Built with Jekyll;
hosted on GitHub Pages.
