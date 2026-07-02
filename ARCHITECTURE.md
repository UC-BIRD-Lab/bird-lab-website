# Architecture

This document records the inventory, sitemap, and the architectural decisions
behind the BIRD Lab site, including the trade-offs considered.

---

## 1 · Content inventory

Source material was the lab's Notion export (public site + lab guide) plus the
PI's Google Scholar / ORCID record. Each item was mapped to a destination and a
disposition: **kept**, **reorganized**, **consolidated**, or **excluded as
internal**.

| Source content | New location | Disposition |
| --- | --- | --- |
| Mission & Vision | Research → Mission & Values | Kept, lightly edited |
| Bio-informed definition (JEB 2023) | Home + Research callouts | Kept verbatim as a quote |
| Research (project list) | Research → themes + projects; `_data/research.yml` | Reorganized into 3 themes + project directory |
| Publications (journal CSV) | Publications; `_data/publications.yml` | Reorganized; now auto-synced |
| Conference papers/posters/talks | `_data/publications_manual.yml` | Kept; curated by hand |
| Blog posts | Publications → Blog posts | Kept |
| The Team (3 member CSVs) | People; `_data/people.yml` | Featured PI + one combined team grid (role badge + discipline tag); alumni in a collapsible table |
| Facilities | Facilities; `_data/facilities.yml` | Kept, structured with capabilities |
| Opportunities | Join | Kept, restructured |
| In the News | News → In the news; `_data/press.yml` | Kept, grouped by year |
| Updates | News → Lab milestones; `_data/updates.yml` | Reorganized into a timeline |
| Lab Guide: Work, Vacation, Find support resources | Lab Guide wiki → *Working in the Lab* | Kept |
| Lab Guide: Communicate, Discuss, Meet, Journal Club | Lab Guide wiki → *Communication & Culture* | Kept |
| Lab Guide: Apply for money, Attend a conference | Lab Guide wiki → *Professional Development* | Kept |
| Lab Guide → Internal Lab Pages: start guides | Lab Guide wiki → *Getting Started* | Published (per PI direction) |
| Lab Guide → Internal Lab Pages: hypothesis, literature, SMART goals, data, code, analysis, error, AI | Lab Guide wiki → *Research Workflow* | Published |
| Lab Guide → Internal Lab Pages: writing, figures, revisions, peer review, posters, presenting, brand | Lab Guide wiki → *Writing & Dissemination* | Published |
| Lab Guide → Internal Lab Pages: Be Safe, Pay/Ship/Travel, Lab Operations Roles | Lab Guide wiki → *Working in the Lab* | Published (one staff email redacted) |
| Lab Guide → Internal Lab Pages: recommendation letters, filing a dissertation | Lab Guide wiki → *Professional Development* | Published |
| Lab Guide → Internal Lab Pages: emergency contacts & other private items | **Member Portal (Notion)** | Excluded — removed by PI before handoff |
| Brand assets / logo | `assets/img/` | Logo kept; used site-wide |

**Public vs. internal.** Per instructions, lab-guide content is treated as
public *unless explicitly marked otherwise*. The PI curated the "Internal Lab
Pages" set by deleting genuinely private items (e.g. emergency contact
information) and directed that the remainder be published. Those retained pages
were therefore folded into the public wiki, with light editorial cleanup: Notion
artifacts removed, internal cross-links repointed to the new wiki URLs, and one
staff member's personal email redacted from the purchasing page (replaced with
"ask the lab manager"). Truly private operations remain in the Member Portal
(Notion); no authentication is implemented.

---

## 2 · Sitemap

```
Home  (/)
├── Research            (/research/)          mission, values, 3 themes, projects
├── People              (/people/)            featured PI, combined team grid,
│                                             affiliates, alumni (collapsible)
├── Publications        (/publications/)      journals (auto) + conferences + blogs + data/code
├── Facilities          (/facilities/)        CALI, wind tunnel, mocap room
├── Lab Guide           (/lab-guide/)         WIKI HUB (6 categories, 34 pages)
│   ├── Getting Started           start guides: undergrad · grad · postdoc
│   ├── Working in the Lab        work · vacation · be safe · support resources · pay · travel · ship · operations roles
│   ├── Research Workflow         hypothesis · literature · SMART goals · manage data · code · analyze data · error & uncertainty · use AI
│   ├── Writing & Dissemination   write a draft · design figures · revisions · review papers · poster · present · brand
│   ├── Communication & Culture   communicate · discussion guidelines · meetings · journal club
│   └── Professional Development   attend a conference · applying for funding · recommendation letters · file dissertation
├── News                (/news/)              lab milestones timeline + press
├── Join                (/join/)              who we seek, openings, how to apply
├── Contact             (/contact/)           PI, profiles, partner facilities
└── Member Portal       (/portal/)            → private Notion workspace (placeholder URL)
```

**Navigation philosophy.** The brief asked to favor *scientific storytelling
over directory-style navigation*. So the Home and Research pages lead with the
lab's central idea (study birds for the *principles* of flight, not to mimic them
→ the bio-informed reporting framework → three research threads) before any list.
Directory-style content (people, publications) is still one click away in the top
nav.

---

## 3 · Architecture decision

**Chosen: a static Jekyll site, content as Markdown + YAML, hosted on GitHub
Pages, with three GitHub Actions (deploy, publications sync, and a
build + broken-link + accessibility check) plus Dependabot.**

### Why this satisfies the stated priorities

1. **Maintainability.** Content is plain `_data/*.yml` and Markdown. A lab member
   edits a file in GitHub's web editor and the site rebuilds itself — no servers,
   no database, no build tooling on their machine. Templates are separated from
   content, so editing words can't break the design.
2. **Accessibility (WCAG 2.1 AA).** Static, server-rendered HTML is the most
   robust foundation for assistive tech. The build ships semantic landmarks, a
   skip link, visible focus states, AA-contrast colors, keyboard-operable nav,
   `prefers-reduced-motion` support, and content that works with JavaScript off.
3. **Scientific communication.** Full control of layout and typography lets the
   pages tell a narrative rather than read like a directory.
4. **Automation.** GitHub Actions handle deployment, the publications feed, and a
   per-pull-request quality check (broken links/images + accessibility scan),
   with Dependabot keeping dependencies current — no third-party service.
5. **Design quality & 6. visual effects.** A small hand-built design system
   (one CSS file, brand palette from the logo, a serif/sans pairing, restrained
   SVG motion) gives a distinctive, credible look without a heavyweight theme.

### Alternatives considered

| Option | Why not |
| --- | --- |
| **Hugo / Eleventy** | Comparable quality, but Jekyll is natively understood by GitHub Pages and is the most documented choice for academic/lab sites — lowest onboarding cost for future maintainers. |
| **Headless CMS (Notion API, Contentful, etc.)** | Adds a runtime dependency, an account, and a failure mode. Conflicts with priorities #1 and "minimal dependencies." Notion stays as the *private* portal only. |
| **Wix / Squarespace / WordPress** | Recurring cost, lock-in, weaker accessibility/performance control, and "looks like a template" — explicitly to be avoided. |
| **React/Next SPA** | Heavier toolchain, worse no-JS accessibility baseline, more to maintain. Not warranted for a content site. |
| **Jekyll academic theme (e.g. al-folio)** | Fast to stand up but opinionated and harder to keep distinctive and lean; we kept dependencies minimal instead. |

### Dependencies (deliberately few)

- **Jekyll** + three first-party plugins: `jekyll-feed`, `jekyll-seo-tag`,
  `jekyll-sitemap` (all supported on GitHub Pages).
- **One web font** (Spectral, via Google Fonts) with a full system-font
  fallback, so the site is fine if the font fails to load.
- **No JavaScript framework.** A little vanilla JS purely enhances (mobile menu,
  search/filter, hero video pause); everything works without it.
- **Python stdlib + PyYAML** for the publications script.

---

## 4 · Accessibility checklist (WCAG 2.1 AA)

- Semantic landmarks (`header`, `nav`, `main`, `footer`) and a **skip link**.
- Single `h1` per page; headings nest in order.
- Color contrast meets AA. The palette is logo-derived — navy `#14284f`, slate
  `#4f7094`, darkened slate `#34567f` for small text on light; text on navy uses
  light tints. (Set in `assets/css/overrides.css`.)
- Visible `:focus-visible` outlines; the mobile menu button exposes
  `aria-expanded`; current page marked with `aria-current`.
- All controls keyboard-operable; search/filter degrade gracefully without JS.
- Images: informative images take real `alt`; decorative SVG marked
  `aria-hidden`; initials avatars expose the name via `aria-label`.
- Motion respects `prefers-reduced-motion`.
- Targets are comfortably sized; line length capped (~72ch) for readability.

See [MAINTENANCE.md](MAINTENANCE.md) for how to keep these intact when editing.

---

## 5 · Rendering & data flow

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
