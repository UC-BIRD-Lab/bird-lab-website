# Content guide

Copy-paste templates for common edits. No coding: open a file on github.com,
click the pencil, edit, **Commit changes** (keep *Create a new branch and start a
pull request*), merge when the checks are green.

> `.yml` files: two-space indents, no tabs, a space after every colon
> (`name: Ada`).

No files at all: lab members can submit a person, paper, news item or press link
through the GitHub issue forms, see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Team member: `_data/people.yml`

Everyone except the PI is one "The team" grid. `groups:` (`postdocs`, `phd`,
`masters`, `undergrad`) only sets order. Only `name` and `role` are required.

```yaml
      - name: Jordan Rivera
        role: PhD Researcher                # sets the bird: PhD 🦢
        start: 2026                         # year joined; sorts the grid
        pronouns: they/them
        field: "Mechanical Engineering"     # discipline tag(s), comma-separated
        email: jrivera@ucdavis.edu
        linkedin: https://www.linkedin.com/in/jordan-rivera
        orcid: 0000-0000-0000-0000
        website: https://example.com
        note: One short line about their project.
        photo: /assets/img/people/jordan-rivera.jpg
        awards:
          - "Best Student Paper, AIAA Aviation 2026"
        aliases: ["Dr. Rivera"]             # other name forms for news auto-linking
```

- Bird from `role` words: Postdoc 🦉 · PhD 🦢 · MSc 🦜 · Undergrad 🐥 · Visiting
  🕊️ · PI 🦅. Override with `role_icon: "🦅"`.
- `email`, `website`, `scholar`, `orcid`, `linkedin`, `github` become icon
  buttons. Privacy convention: no contact links on undergraduates.
- `awards:` is a list; one 🏆 with the awards stacked beside it.
- `field:` is what they trained in.
- Promote someone: change `role:` (move the block to reorder).
- Someone left: move their block to `alumni:` and add `now:`. Extra fields are
  ignored; `role:` and `start:` are required (the check errors on a missing
  `start:`). `role:` sets the section (postdocs, PhDs, MSc, undergrads,
  visiting; unmatched roles sort last with a warning), `start:` orders
  newest-first within it. Keep `aliases:` so old news items still link.
  ```yaml
    - { name: Jordan Rivera, role: "PhD Researcher", start: 2024, now: "Boeing" }
  ```
- Photo: square JPG in `assets/img/people/` (or original in `_raw/` then
  `bash scripts/apply-images.sh`). No photo = initials avatar.

---

## Publication

Journal articles arrive automatically. By hand, top of `_data/publications.yml`:
```yaml
- title: "Your exact paper title"
  authors: "A. Author, C. Harvey, B. Coauthor"
  venue: "Journal Name"
  year: 2026
  type: journal
  doi: "https://doi.org/10.xxxx/xxxxx"
```

Conference paper / poster / talk, under `conference:` in
`_data/publications_manual.yml`:
```yaml
  - title: "Talk or paper title"
    authors: "C. Harvey, K. Bordner"
    venue: "AIAA SciTech Forum, Orlando, FL"
    year: 2026
    type: conference
    note: Poster          # or "Presentation"; omit for a conference paper
    doi: "https://…"      # optional
```
Type pill: journal article (green), conference paper (amber, no `note`),
presentation/poster (gray, `note` set).

---

## Data, code, figure for a paper: `_data/pub_links.yml`

Extras the sync can't know, matched by bare DOI. The sync never touches this file.

```yaml
- doi: "10.1098/rsif.2025.0868"   # bare DOI, no "https://doi.org/"
  data: "https://figshare.com/…"
  code: "https://github.com/UC-BIRD-Lab/…"
  image: /assets/img/research/perchaero.jpg # standout papers only
  kind: review                    # or "commentary"; journals only, default "Research article"
  award: "AIAA Jefferson Goblet Student Paper Award"  # gold 🏆 pill
  correction: "https://doi.org/…" # shows a "Correction" pill; correction_label: changes the word
```

- Not a paper (journal profile, indexed talk)? Add its bare DOI under `exclude:`
  in `publications_manual.yml` with a `reason:`; the sync removes it for good.
- The sync skips corrigenda and prints them; link one via `correction:` above.
- Entries show once the paper is on the Publications page.
- Press is not listed here: tag the story with the paper's `doi:` in `press.yml`
  and the "In the news" badge counts it.

---

## News milestone: `_data/updates.yml`

Top of the current year's `events:`. `type` is one of `award, paper, talk,
funding, build, service, people, travel, graduation`.
```yaml
    - { date: "June 2026", type: award, text: "Ada won a best-paper award at AIAA Aviation." }
```
New year: new block at the very top:
```yaml
- year: 2027
  events:
    - { date: "January 2027", type: people, text: "…" }
```

Names written as on the People page auto-link (alumni link to the alumni table,
which opens). Don't add your own `<a>` around a name. Short forms go in that
person's `aliases:` in `people.yml`.

Link out with `link:` + `link_text:`, where `link_text:` is words copied from
`text:`:
```yaml
    - { date: "June 2026", type: talk, text: "Kaleb Bordner presented at the AIAA AVIATION Forum.",
        link: "https://www.aiaa.org/aviation", link_text: "the AIAA AVIATION Forum" }
```
One link per item; site pages as paths (`/join/`). A person's name can't be the
`link_text:` (already linked); then, or with no `link_text:`, a "Details ↗" link
is added at the end. Raw `<a>` in `text:` works but is easy to break.

---

## Press: `_data/press.yml`

```yaml
- year: 2026
  items:
    - title: "Headline of the article"
      source: "Outlet name"
      url: "https://…"
      doi: "10.1098/rsif.2025.0868"   # paper covered → "Paper" pill + badge on Publications
      tag: Feature                     # only without doi: Center, Award, Funding, Profile, Feature
      featured: true                   # big card at the top of News
      image: /assets/img/research/perchaero.jpg   # required if featured; local path or article image URL
```
Existing year: add a `- title:` block under its `items:`.

Script (~1 min): reads outlet, headline and author; with `--featured` downloads
and compresses the lead image into `assets/img/news/`; `--append` inserts it.
```bash
python scripts/add_press.py "https://outlet.com/story" --doi 10.1098/rsif.2025.0868 --featured
```
Use `--tag Center` etc. instead of `--doi` for non-paper coverage.

### Videos, podcasts, 3D models: `_data/media.yml`

The "Watch & listen" strip on News (link-outs, not embeds). Fields: `title`,
`kind` (`video` / `podcast` / `radio` / `model`), `source`, `year`, `url`.
Default is a compact row; `featured: true` makes a thumbnail card (YouTube
thumbnail automatic, else `image:`). Optional `doi:` (📄 Paper link) or `tag:`
(same vocabulary as press); one chip, `doi` wins.

```bash
python scripts/add_press.py "https://youtu.be/XXXX" --media video --featured --append
python scripts/add_press.py "https://pod.site/ep"  --media podcast --append
```

---

## Fellowships: `_data/funding.yml`

The table on the Lab Guide "Applying for funding" page.

```yaml
- name: Brooke Owens Fellowship
  level: "UG"                       # e.g. "UG", "Masters, PhD", "Post Doc"
  url: http://www.brookeowensfellowship.org/
  eligibility: …                    # optional: the program's own rules
```

---

## Research project: `_data/research.yml`

```yaml
  - title: New project title
    lead: Kaleb Bordner          # exactly as their name: in people.yml
    papers:                      # DOIs; looked up on the Publications page
      - "10.2514/6.2026-4380"
    contact: lead@ucdavis.edu    # optional; "Ask the lead" button
    theme: mechanics-dynamics    # morphology-kinematics · mechanics-dynamics · sensing-control
    image: /assets/img/research/yourfig.jpg   # optional
    blurb: >-
      One sentence describing the project.
```
A paper must already be on the Publications page to show. Project ended: delete
the block.

---

## Facility: `_data/facilities.yml`

One block each. The first `featured: true` is the flagship band; the rest are
alternating photo rows. House pattern: chips (what a visitor can *do*) then an
`equipment:` table (what with, in numbers); a chip never repeats a table figure.
`specs:` tiles exist but are unused on purpose. Short is the point; the contact
note at the foot of the page covers the rest.

```yaml
- name: Center for Animal Locomotion and Innovation (CALI)
  featured: true                     # exactly one; use a real photo
  tagline: >-
    One credible line shown with the name.
  partner: Co-directed with Dr. …    # optional
  location: California Raptor Center, UC Davis   # optional
  url: https://…                     # optional "Learn more" button
  url_label: Visit the CALI consortium
  photo: /assets/img/facilities/cali.jpg
  photo_note: AI rendering based on real photos.   # italic caption; omit for real photos
  photo_alt: >-                      # falls back to "Inside {name}"
    The CALI flight hall, a long bright room lined with white curtains
    and motion capture cameras.
  funding:                           # optional logo badge on the flagship photo
    note: "DURIP support from:"
    name: DEVCOM Army Research Laboratory
    logo: /assets/img/partners/arl.png
    url: https://www.arl.army.mil/
  capabilities:
    - Sub-millisecond, sub-millimeter tracking
    - Daylight-balanced lighting for live birds
  equipment:                         # optional table; vendor spelling for model names
    - label: Motion capture
      value: "44 × OptiTrack VersaX 120 — 12.6 MP, 300 fps"
      also: "Second line under the same label (optional)"
```

---

## Positions: `_data/openings.yml`

The three pills on Join (undergrad, graduate, postdoc): flip `open:` and the pill
and its `open_note` / `closed_note` follow. Graduate and postdoc pill wording is
in `join.md`. Write `open: true` unquoted; the check catches `"true"`.

### Postings above the pills

`featured:` and a smaller `second:` block, same fields. `join.md` renders
whatever is there. Both hide after `deadline`.

```yaml
featured:
  enabled: true
  id: postdoctoral-scholar     # the #anchor the banner links to
  pill: Now hiring
  title: Postdoctoral Scholar
  deadline: 2026-09-30
  body:                        # one paragraph per item; HTML, so <strong> not **
    - >-
      A <strong>full-time, two-year position</strong> ...
  terms: "Full-time - two years - Davis, California ..."
  apply_subject: "..."         # mailto; or apply_url: for a form link
  apply_body: |
    Hi Dr. Harvey, ...
  apply_cta: Email your application
  flyer: /assets/img/join/postdoctoral-scholar-flyer.png   # optional
  flyer_alt: "..."
```

Take a posting down: `enabled: false` here and in `_data/announcement.yml`.

---

## Site-wide banner: `_data/announcement.yml`

```yaml
enabled: true
label: "Now hiring"
text: "We're recruiting a postdoctoral scholar to help lead research at CALI, our new animal-locomotion facility."
cta: "Learn more & apply"
url: "/join/#postdoctoral-scholar"
deadline: 2026-09-30      # always set: build stops rendering it, main.js hides it before the next build, the sweep flags it
```

---

## Review reminders: `_data/review.yml`

Things that go stale without breaking. Four times a year a bot opens one issue
naming what is due.

```yaml
  - what: Funding opportunities, eligibility rules and application links
    file: _data/funding.yml
    owner: "@christinaharvey"
    every_months: 12
    last_reviewed: 2026-07-06
```
Clear an item: check it, set `last_reviewed:` to today. Lab Guide pages use
`reviewed:` in their own front matter instead.

---

## Safety training: `_data/safety.yml`

The required-training list on the Lab safety page: `name`, `who`, optional
`link`, optional `note`. Six-month review cycle.

---

## CALI page: `_data/cali*.yml`

`cali.yml` (sections, equipment), `cali_rates.yml` (rates and `effective:`
date; update both when Costing Policy & Analysis re-approves), `cali_gallery.yml`,
`cali_milestones.yml`. Headers explain fields.

### Peer mentoring: `_data/cali_mentoring.yml`

Switch (`signups: open:`), form link and dates; words are in `cali.html`. Each
fall: set dates, check the link, flip the switch.

---

## Lab Guide page: `_guide/`

One Markdown file each. New page:
```markdown
---
title: My new page
category: Working in the Lab   # must be in guide_order: in _config.yml
order: 4                       # position within the category
summary: One sentence shown on the Lab Guide hub.
description: One sentence for link previews (Slack, email, search); ~100-160 characters, about the lab not a person.
reviewed: 2026-07-03
---

Your content here. Use ## for section headings.
```
Without `description:` Jekyll uses the first block of the page, often a margin
note. New category: add it to `guide_order:`.

Callouts:
```markdown
<div class="callout" markdown="1">A tip.</div>
<div class="callout callout--warn" markdown="1">A caution.</div>
<div class="callout callout--stop" markdown="1">A hard rule.</div>
```

### Keeping pages fresh

Each guide page shows its last git change date under the title. A "Needs
review" band appears after a year without an edit or `reviewed:` date; clear it
by editing or setting `reviewed:` to today. The quarterly sweep lists overdue
pages in one issue.

### Lab operations roles: `_data/roles.yml`

One entry per role: `name`, `tagline`, `purpose`, `owns`, `can`. Table and cards
both update. Routines and handoffs stay in the Notion portal.

---

## Menu: `_data/navigation.yml`

`cta: true` on exactly one item (Join). Public destinations only; Contact and
the Member Portal are in the footer (`_includes/footer.html`).

## Site settings: `_config.yml`

Title, tagline, portal URL, contact email, ORCID, interest-form link, LinkedIn,
GitHub org, FigShare URL, social-share image. Analytics: cookieless GoatCounter
via `analytics: { goatcounter: }`; blank it to collect nothing.

---

## Research figure: `assets/img/research/`

Optimized JPG there, then `image:` on the project in `research.yml`. `theme:`
must match a theme `id` in the same file (`morphology-kinematics`,
`mechanics-dynamics`, `sensing-control`); each theme's `why:` is one sentence
shown on Home and Research.

---

## Honors and "Featured in": `_data/recognition.yml`

`awards:` (`name`, `who`, `org`, `year`) and `media:` (`name`, `url`).

---

## Photos

- Headshots: originals in `assets/img/people/_raw/`, run
  `bash scripts/apply-images.sh`, add `photo:` to the person.
- PI bio: prose at the top of `people.html`.
- Group photo: `bash scripts/apply-images.sh "/path/to/group-photo.jpg"` makes
  `assets/img/lab-photo.jpg`; set `lab_photo:` under `assets:` in `_config.yml`.
  Shows on People and as the "In the field" band on Home.
- Scenes (People): photos in `assets/img/lab/` (or `_raw/`); in
  `_data/gallery.yml` set `file:`, `alt`, `caption`, `ready: true`. Needs both
  `ready: true` and `alt:` to show.
- Join culture photo: `culture_photo:` under `assets:` in `_config.yml`.

---

## Home page

Text in `index.html`: video hero (`assets/video/bird-glide.mp4`, poster
`assets/img/facilities/cali.jpg`, hidden for reduce-motion), "Bio-informed, not
just bio-inspired", CALI band. From data: research cards (`research.yml`),
partners (`collaborators.yml`: `name`, `sub`, `photo`, `url`), funders
(`funders.yml`: `name`, `short`, `url`, `logo`), open science, selected work,
recognition, featured in, latest news. Logos in `assets/img/partners/`.

---

## Image budget

| Asset | Aim for | Enforced |
|---|---|---|
| Research figure / card | ~1280 px wide, ≤ 120 KB | 1600 px · 300 KB JPEG / 600 KB PNG |
| Lab group photo | ~1600 px wide, ≤ 300 KB | same |
| Headshot | 600 × 600 px, ≤ 80 KB | same |
| Social/OG image | 1200 × 630 px, ≤ 200 KB | same |
| Background video | 1080p, short loop | 2.5 MB |
| Animated GIF | prefer MP4 | 700 KB |

Over the limit fails the **Media budget** check. Images are compressed after
merge; video and GIFs are not. Mac one-liner:
```bash
sips -s format jpeg -s formatOptions 82 input.jpg --resampleWidth 1280 --out output.jpg
```
