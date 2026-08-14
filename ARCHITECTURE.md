# Architecture

> **How this file was written.** Website documentation, largely written by AI
> (Claude) from the code in this repository. Christina checked that it works, not
> that every sentence is how she would put it. The site-wide statement is on the
> [Accessibility page](accessibility.md) under *How this site is made*.

Why the site is built this way. Decisions and trade-offs, not contents: anything
that changes as you edit (which pages exist, how many people, the menu) lives in
`_config.yml`, `_data/navigation.yml` and the `_data/*.yml` files, which are the
source of truth.

---

## The decision

A static [Jekyll](https://jekyllrb.com/) site: Markdown and YAML on GitHub
Pages, with GitHub Actions for deployment, the publications sync, the pre-merge
checks and the scheduled reviews, plus Dependabot.

Priorities, in order: **maintainability, accessibility (WCAG 2.1 AA), scientific
communication, automation, visual design.** Where two conflicted, the higher one
won. Clearest example: content lives in plain data files rather than a headless
CMS, because a non-technical member making a safe edit matters more than any
convenience a CMS adds.

### Why this satisfies the priorities

1. **Maintainability.** Content is plain `_data/*.yml` and Markdown. A member
   edits a file in GitHub's web editor and the site rebuilds itself. No servers,
   no database, nothing installed. Templates are separate from content, so
   editing words cannot break the design.
2. **Accessibility.** Static, server-rendered HTML is the most robust foundation
   for assistive technology. The build ships semantic landmarks, a skip link,
   visible focus states, AA-contrast colours, keyboard-operable navigation,
   `prefers-reduced-motion`, and content that works with JavaScript off. A
   blocking WCAG 2.1 AA scan runs on every pull request; the manual checks it
   can't cover are in [MAINTENANCE.md](MAINTENANCE.md).
3. **Scientific communication.** Control of layout and typography lets pages lead
   with the lab's central idea rather than read like a directory.
4. **Automation.** GitHub Actions handle deployment, the publications feed, the
   pre-merge checks and the quarterly review reminders. No third-party service.
5. **Design.** A small hand-built system (brand palette from the logo, a serif
   and sans pairing, restrained SVG motion) gives a distinctive, credible look
   without a heavyweight theme.

### Alternatives considered

| Option | Why not |
| --- | --- |
| **Hugo / Eleventy** | Comparable, but Jekyll is native to GitHub Pages and the best-documented choice for lab sites: lowest onboarding cost for whoever inherits this. |
| **Headless CMS (Notion API, Contentful)** | Adds a runtime dependency, an account and a failure mode. Conflicts with maintainability. Notion stays the *private* portal only. |
| **Wix / Squarespace / WordPress** | Recurring cost, lock-in, weaker accessibility and performance control, templated look. |
| **React / Next SPA** | Heavier toolchain, worse no-JS baseline, more to maintain. Not warranted for a content site. |
| **Jekyll academic theme (al-folio)** | Fast to stand up, but opinionated and hard to keep distinctive. We kept dependencies minimal instead. |

### Dependencies (deliberately few)

- **Jekyll** plus first-party plugins (`jekyll-feed`, `jekyll-seo-tag`,
  `jekyll-sitemap`, `jekyll-last-modified-at`). Exact versions are pinned in a
  committed `Gemfile.lock`, so the build can't change underneath us.
- **One web font** (Spectral) with a full system-font fallback.
- **No JavaScript framework.** A little vanilla JS enhances the mobile menu,
  search and hero-video pause; everything works without it.
- **Python standard library plus PyYAML** for the scripts.

---

## Public vs. internal

Lab-guide content is public unless deliberately kept private. Protective,
decision-relevant rules (safety, animal welfare, support resources) stay public
and prominent. Internal workflows and anything genuinely private (emergency
contacts, approved protocols, onboarding) live in the private Notion **Member
Portal**, which the site links to but does not host. The site has no
authentication, so nothing in `_data/` or `_guide/` should assume privacy.

The portal is reached from the footer, not the primary nav: the top bar is
reserved for public destinations and ends in a single call to action (**Join**).
Current members can bookmark the Notion workspace; a first-time visitor should
never spend attention on a door they can't open.

---

## Content structure (where it lives, not what it says)

- **Pages** are the `*.html` / `*.md` files at the repository root, plus the Lab
  Guide hub at `lab-guide/`.
- **Lab Guide pages** are one Markdown file each in `_guide/`, each declaring a
  `category:`. The categories and their order are defined once in `guide_order:`
  in `_config.yml`, read by both the hub and the wiki sidebar. The hub warns
  loudly if a page's category is missing, so nothing is dropped silently.
- **Everything else** (people, publications, research, news, press, facilities,
  funders, partners) is data in `_data/*.yml`, rendered by `_layouts/` and
  `_includes/`. Read those files for the current structure; no page list is
  duplicated here.

---

## Rendering and data flow

```
_data/*.yml ─┐
_guide/*.md ─┼─► Jekyll (Liquid templates in _layouts/ + _includes/) ─► static HTML in _site/
*.md / *.html┘                                                              │
                                                                            ▼
scripts/update_publications.py ──(monthly Action, opens PR)──► _data/publications.yml
                                                                            │
        every pull request ──► site-checks.yml (build + broken-link + a11y scan)
                                                                            │
                          GitHub Actions (deploy.yml) ──build──► GitHub Pages (live site)
```

Journal articles and DOI-bearing conference papers sync from OpenAlex by the PI's
ORCID and open a pull request for review. Talks and posters without a DOI are
added by hand in `_data/publications_manual.yml`.

Nothing reaches `main` without passing the checks: content validation
(cross-referenced names, DOIs and image paths), broken links and missing images,
a WCAG 2.1 AA scan, and a media weight budget. Four times a year a sweep opens
one issue listing content that may have gone out of date. No automation edits
published content: every bot proposes a pull request a human merges.
