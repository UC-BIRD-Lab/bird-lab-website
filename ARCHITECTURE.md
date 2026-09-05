# Architecture

Why the site is built this way. What the site contains is in `_config.yml`,
`_data/*.yml` and the pages themselves; nothing is duplicated here.

## The decision

A static [Jekyll](https://jekyllrb.com/) site on GitHub Pages, with GitHub
Actions for deployment, the publications sync, pre-merge checks and scheduled
reviews, plus Dependabot.

Priorities in order: maintainability, accessibility (WCAG 2.1 AA), scientific
communication, automation, visual design. Where two conflict the higher wins:
content is plain data files rather than a headless CMS because a non-technical
member making a safe edit matters more.

1. **Maintainability.** Content is `_data/*.yml` and Markdown, edited in
   GitHub's web editor. No servers, database or installs. Templates are separate
   from content, so editing words can't break the design.
2. **Accessibility.** Static HTML with semantic landmarks, skip link, visible
   focus, AA contrast, keyboard navigation, `prefers-reduced-motion`, and no
   dependence on JavaScript. A blocking WCAG 2.1 AA scan runs on every PR; the
   manual remainder is in [MAINTENANCE.md](MAINTENANCE.md).
3. **Scientific communication.** Full control of layout lets pages lead with
   the lab's idea rather than read like a directory.
4. **Automation.** Actions only; no third-party service.
5. **Design.** A small hand-built system: palette from the logo, serif + sans,
   restrained SVG motion.

### Alternatives

| Option | Why not |
| --- | --- |
| Hugo / Eleventy | Comparable; Jekyll is native to GitHub Pages and best documented for lab sites. |
| Headless CMS (Notion API, Contentful) | Runtime dependency, account, failure mode. Notion stays the private portal only. |
| Wix / Squarespace / WordPress | Cost, lock-in, weaker accessibility and performance control. |
| React / Next SPA | Heavier toolchain, worse no-JS baseline. |
| Jekyll academic theme (al-folio) | Opinionated, hard to keep distinctive. |

### Dependencies

Jekyll plus `jekyll-feed`, `jekyll-seo-tag`, `jekyll-sitemap`,
`jekyll-last-modified-at`, pinned in `Gemfile.lock`. One web font (Spectral)
with system fallback. Vanilla JS only (mobile menu, search, video pause), all
optional. Scripts: Python standard library plus PyYAML.

## Public vs. internal

Lab Guide content is public unless deliberately private. Safety, animal welfare
and support resources stay public and prominent. Emergency contacts, protocols
and onboarding live in the private Notion Member Portal, linked from the footer
rather than the top bar (which is public destinations ending in one call to
action, Join). The site has no authentication; nothing in `_data/` or `_guide/`
is private.

## Content structure

Pages are the root `*.html` / `*.md` files plus `lab-guide/`. Lab Guide pages
are one Markdown file each in `_guide/` with a `category:`; categories and their
order are defined once in `guide_order:` in `_config.yml`, read by the hub and
the sidebar (the hub warns on an unlisted category). Everything else is
`_data/*.yml` rendered by `_layouts/` and `_includes/`.

## Data flow

```
_data/*.yml ─┐
_guide/*.md ─┼─► Jekyll (_layouts/ + _includes/) ─► static HTML in _site/
*.md / *.html┘                                              │
scripts/update_publications.py ──(monthly Action, PR)──► _data/publications.yml
        every pull request ──► site-checks.yml (build + links + a11y)
                          deploy.yml ──► GitHub Pages
```

Journal articles sync from OpenAlex by the PI's ORCID into a PR. Talks and
posters are hand-added in `_data/publications_manual.yml`. Every PR must pass
content validation, link/image checks, a WCAG 2.1 AA scan and a media budget. A
quarterly sweep opens one issue for stale content. No bot edits published
content; every bot proposes a PR a human merges.
