# Architecture

Why the BIRD Lab site is built the way it is. This document is deliberately
durable: it explains decisions and trade-offs, not the current contents. Anything
that changes as you edit the site (which pages exist, how many people or papers,
the exact menu) is not repeated here, because the site itself is the source of
truth. For the live structure, read `_config.yml` (`guide_order`),
`_data/navigation.yml`, and the `_data/*.yml` files.

---

## The decision

A static [Jekyll](https://jekyllrb.com/) site: content as Markdown and YAML,
hosted free on GitHub Pages, with a few GitHub Actions (deploy, publications
sync, and a build plus broken-link and accessibility check) and Dependabot.

The design priorities, in order, were **maintainability, then accessibility
(WCAG 2.1 AA), then scientific communication, then automation, then visual
design.** Where two of these traded off, the higher one won. The clearest
example: content lives in plain editable data files rather than a headless CMS,
because a non-technical member being able to make a safe edit matters more than
any convenience a CMS would add.

### Why this satisfies the priorities

1. **Maintainability.** Content is plain `_data/*.yml` and Markdown. A member
   edits a file in GitHub's web editor and the site rebuilds itself: no servers,
   no database, no build tooling on their machine. Templates are separated from
   content, so editing words cannot break the design.
2. **Accessibility.** Static, server-rendered HTML is the most robust foundation
   for assistive technology. The build ships semantic landmarks, a skip link,
   visible focus states, AA-contrast colors, keyboard-operable navigation,
   `prefers-reduced-motion` support, and content that works with JavaScript off.
   The living accessibility checklist is in [MAINTENANCE.md](MAINTENANCE.md).
3. **Scientific communication.** Full control of layout and typography lets the
   pages lead with the lab's central idea rather than read like a directory.
4. **Automation.** GitHub Actions handle deployment, the publications feed, and a
   per-pull-request quality check, with Dependabot keeping dependencies current.
   No third-party service to maintain.
5. **Design.** A small hand-built design system (brand palette from the logo, a
   serif and sans pairing, restrained SVG motion) gives a distinctive, credible
   look without a heavyweight theme.

### Alternatives considered

| Option | Why not |
| --- | --- |
| **Hugo / Eleventy** | Comparable quality, but Jekyll is natively understood by GitHub Pages and is the most documented choice for academic/lab sites: lowest onboarding cost for future maintainers. |
| **Headless CMS (Notion API, Contentful, etc.)** | Adds a runtime dependency, an account, and a failure mode. Conflicts with the maintainability priority. Notion stays as the *private* portal only. |
| **Wix / Squarespace / WordPress** | Recurring cost, lock-in, weaker accessibility and performance control, and a templated look we wanted to avoid. |
| **React / Next SPA** | Heavier toolchain, worse no-JS accessibility baseline, more to maintain. Not warranted for a content site. |
| **Jekyll academic theme (e.g. al-folio)** | Fast to stand up but opinionated and harder to keep distinctive and lean. We kept dependencies minimal instead. |

### Dependencies (deliberately few)

- **Jekyll** plus first-party plugins (`jekyll-feed`, `jekyll-seo-tag`,
  `jekyll-sitemap`, `jekyll-last-modified-at`), all supported on GitHub Pages.
- **One web font** (Spectral, via Google Fonts) with a full system-font
  fallback, so the site is fine if the font fails to load.
- **No JavaScript framework.** A little vanilla JS purely enhances (mobile menu,
  search/filter, hero video pause); everything works without it.
- **Python standard library plus PyYAML** for the publications script.

---

## Public vs. internal

Lab-guide content is public unless deliberately kept private. Protective,
decision-relevant rules (safety, animal welfare, support resources) stay public
and prominent. Step-by-step internal workflows and anything genuinely private
(emergency contacts, approved protocols, onboarding operations) live in the
private Notion **Member Portal**, which the site links to but does not host. No
authentication is implemented on the site itself, so nothing added to `_data/` or
`_guide/` should assume privacy.

---

## Content structure (where it lives, not what it says)

- **Pages** are the `*.html` / `*.md` files at the repository root, plus the Lab
  Guide hub at `lab-guide/`.
- **Lab Guide pages** are one Markdown file each in `_guide/`. Each declares a
  `category:` in its front matter; the categories and their order are defined
  once in `guide_order:` in `_config.yml`, which both the guide hub and the wiki
  sidebar read. The hub warns loudly if a page's category is missing from that
  list, so nothing is dropped silently.
- **Everything else** (people, publications, research themes and projects, news,
  press, facilities, funders, partners) is data in `_data/*.yml`, rendered by
  templates in `_layouts/` and `_includes/`. To see the current site structure,
  read those files; they are the source of truth, which is why no page list or
  count is duplicated here.

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
ORCID and open a pull request for review. Conference talks and posters without a
DOI are added by hand in `_data/publications_manual.yml`. Everything else is
hand-curated in `_data/`.
