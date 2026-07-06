# Content guide

Copy-paste templates for the most common edits. **No coding required.** You can
do all of this in your browser: open a file on github.com, click the ✏️ pencil,
edit, then **Commit changes**. The site rebuilds itself.

> **The one rule:** these `.yml` files use spaces, not tabs. Indent with **two
> spaces**, and keep a space after every colon (`name: Ada`, not `name:Ada`).

**Don't want to touch files at all?** Lab members can submit a person, paper,
news item, or press link through the site's **GitHub issue forms** (no YAML):
see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Add or update a team member: `_data/people.yml`

Everyone except the PI shows in one combined **"The team" grid**; each card gets a
bird badge (from the `role` text) and optional discipline tags. In the file,
members sit under `groups:` (`postdocs`, `phd`, `masters`, `undergrad`), which only
sets the **order** they appear.

Add a block under the right group's `members:` list. Only `name` and `role` are required.

```yaml
      - name: Jordan Rivera
        role: PhD Researcher                # drives the bird: PhD 🦢
        start: 2026                         # year they joined; sorts the grid
        pronouns: they/them
        field: "Mechanical Engineering"     # optional discipline tag(s); comma-separate
        email: jrivera@ucdavis.edu
        linkedin: https://www.linkedin.com/in/jordan-rivera
        orcid: 0000-0000-0000-0000          # optional
        website: https://example.com        # optional
        note: One short line about their project.   # optional
        photo: /assets/img/people/jordan-rivera.jpg # optional
        awards:                             # optional; see "Awards" below
          - "Best Student Paper, AIAA Aviation 2026"
        aliases: ["Dr. Rivera"]             # optional; see "Auto-linking" below
```

- **The bird is automatic** from the `role` words: Postdoc 🦉 · PhD 🦢 · MSc 🦜 ·
  Undergrad 🐥 · Visiting 🕊️ · PI 🦅. Force a different one with `role_icon: "🦅"`.
- **Contact links become icons** automatically. Add any of `email`, `website`,
  `scholar`, `orcid`, `linkedin`, `github` and each shows as a small icon button:
  no wording needed. This works the same on the PI's featured block.
- **`awards:`** is a list. The card shows a single 🏆 with the awards stacked
  beside it, so two or three honors stay tidy (no repeated trophies).
- **`aliases:`** lists other name forms (a nickname, or "Dr. Rivera") that should
  also auto-link in the news timeline: see *Auto-linking* under news milestones.
- **`field:`** shows small tags (e.g. `Aerospace`, `Biology`, `Animal Behavior`,
  `Computer Science`) so the lab's engineering/biology mix is visible. Use the
  field someone *trained in*. Comma-separate for more than one.
- **Promote someone** (e.g. undergrad → PhD): just change their `role:` text (and
  move the block if you want them earlier in the order). The bird updates itself.
- **Someone left:** cut their whole block from `groups:` and paste it into the
  `alumni:` list at the bottom, then add a `now:` line for where they went. You
  can trim it to one line or paste the full block as-is: extra fields are ignored:
  ```yaml
    - { name: Jordan Rivera, role: "PhD Researcher", start: 2024, now: "Boeing" }
  ```
  `start:` (year they joined) sorts the alumni table newest-first, and any
  `linkedin:` shows a LinkedIn icon beside their name.
- **Photo (optional):** put a small square JPG in `assets/img/people/` (or a large
  original in `assets/img/people/_raw/` then run `bash scripts/apply-images.sh`),
  and add the `photo:` line above. No photo = a clean initials avatar.

---

## Add a publication

**Journal article**: usually automatic. If you need to add one by hand, put it
at the **top** of `_data/publications.yml`:
```yaml
- title: "Your exact paper title"
  authors: "A. Author, C. Harvey, B. Coauthor"
  venue: "Journal Name"
  year: 2026
  type: journal
  doi: "https://doi.org/10.xxxx/xxxxx"
```

**Conference paper / poster / presentation**: add under `conference:` in
`_data/publications_manual.yml`:
```yaml
  - title: "Talk or paper title"
    authors: "C. Harvey, K. Bordner"
    venue: "AIAA SciTech Forum, Orlando, FL"
    year: 2026
    type: conference
    note: Poster          # or "Presentation"; OMIT for a conference paper
    doi: "https://…"      # optional
```
Each entry shows a colored type pill at the front of the title: **journal
article** (green), **conference paper** (amber, shown when you omit `note`), and
**presentation / poster** (muted gray, shown when `note` is set). So leaving
`note` off is what marks something as a full conference paper.

---

## Add data / code / a figure to a paper: `_data/pub_links.yml`

Journal articles sync automatically, so the "extras" a bot can't know: a dataset
link, a code repo, a figure: go in this separate file, matched to the paper by
its **bare DOI**. The auto-sync never touches it, so your extras are safe.

```yaml
- doi: "10.1098/rsif.2025.0868"   # bare DOI, no "https://doi.org/"
  data: "https://figshare.com/…"  # optional: dataset link
  code: "https://github.com/UC-BIRD-Lab/…"  # optional: code repo
  image: /assets/img/research/perchaero.jpg # optional: only for major papers
  kind: review                    # optional: "review" or "commentary" (journals only)
  award: "AIAA Jefferson Goblet Student Paper Award"  # optional: gold 🏆 pill
  correction: "https://doi.org/…" # optional: a correction/corrigendum for this paper
```

- Add `image:` **sparingly**: just standout papers, or the list gets busy.
- **`kind:`** sets a journal article's type pill. Leave it off and the paper reads
  **Research article** (the default). Add `kind: review` or `kind: commentary` for the
  exceptions. The pill stays green either way: only the wording changes. (Conference
  papers and posters are labelled from `publications_manual.yml`, not here.)
- **`award:`** shows a gold 🏆 pill next to the paper: use it for a best-paper award,
  a prize, etc.
- **Something showed up that isn't a paper?** (a journal profile of the PI, a talk
  OpenAlex indexed like an article.) Add its bare DOI under `exclude:` in
  `_data/publications_manual.yml` with a short `reason:`: the sync removes it and never
  re-adds it.
- **Corrections/corrigenda:** the auto-sync skips them (it prints any it sees). If one
  corrects a listed paper, add a `correction:` link to that paper's block here and it
  shows as a small "Correction" pill next to it. Add `correction_label: "Corrigendum"`
  to change the wording.
- Nothing appears until the paper is on the Publications page, so you can add this
  as soon as a paper is accepted.
- **Press/news is not listed here**: tag a story with the paper's `doi:` in
  `_data/press.yml` and it's counted automatically as the "In the news" badge.

---

## Add a news milestone: `_data/updates.yml`

Add an item to the top of the current year's `events:` list. `type` picks the
label; use one of: `award, paper, talk, funding, build, service, people, travel,
graduation`.
```yaml
    - { date: "June 2026", type: award, text: "Ada won a best-paper award at AIAA Aviation." }
```
Starting a new year? Add a new block at the very top:
```yaml
- year: 2027
  events:
    - { date: "January 2027", type: people, text: "…" }
```

**Auto-linking (names + links).** Just write a lab member's name the way it
appears on the People page: "Kaleb Bordner": and it becomes a link to their
card automatically. Alumni names link to the alumni table. **Don't** wrap names in
your own `<a>` tag (that would double-link). For a nickname or short form, add an
`aliases:` line to that person in `people.yml`. To link to an outside page (a
paper, an event), you can paste plain HTML: use single quotes so the YAML stays
valid: `text: "We spoke at <a href='https://example.com'>the workshop</a>."`

---

## Add press coverage: `_data/press.yml`

```yaml
- year: 2026
  items:
    - title: "Headline of the article"
      source: "Outlet name"
      url: "https://…"
      doi: "10.1098/rsif.2025.0868"   # optional: see below
      featured: true                   # optional: see below
      image: /assets/img/research/perchaero.jpg   # needed if featured
```
(If the year already exists, just add another `- title:` block under its `items:`.)

- **`doi:`**: the DOI of the paper the story covers. When set, that paper on the
  Publications page shows an "In the news · N" badge counting its stories.
- **`featured: true` + `image:`**: promotes the story to the big cards at the top
  of the News page. `image:` can be a local file (`/assets/img/…`) **or** a direct
  URL to the article's own image (`https://outlet.com/story.jpg`). A static site
  can't fetch a story's image on its own, so paste the link once here.

**Shortcut: let the script do it** (~1 min). Instead of filling the block by hand, run:

```bash
python scripts/add_press.py "https://outlet.com/story" --doi 10.1098/rsif.2025.0868 --featured
```

It reads the outlet, headline, and author from the page, and: only with `--featured`:
downloads the lead image into `assets/img/news/` (resized/compressed), then prints a
ready-to-paste entry. Add `--append` to have it inserted into `press.yml` for you. Drop
`--featured` for a normal (non-card) story. See the script's header for all options.

### Videos, podcasts & 3D models: `_data/media.yml`

Non-article coverage (talks, podcast episodes, an interactive model) lives here and
shows in the **"Watch & listen"** strip on the News page: as link-out cards, not
embeds, so the page stays fast and cookie-free. Each entry has `title`, `kind`
(`video` / `podcast` / `model`), `source`, `year`, `url`. For a YouTube link the
thumbnail is generated automatically; podcasts and models get an icon tile.

---

## Fellowships & scholarships list: `_data/funding.yml`

The funding table on the Lab Guide **"Applying for funding"** page (linked from Join)
is generated from this file. Copy a block to add one; omit `eligibility` or `url`
when there isn't one.

```yaml
- name: Brooke Owens Fellowship
  level: "UG"                       # e.g. "UG", "Masters, PhD", "Post Doc"
  eligibility: "US citizen · Woman/Non-binary"   # optional; leave off if open
  url: http://www.brookeowensfellowship.org/
```

---

## Edit a research project: `_data/research.yml`

Projects are small cards under `projects:`: a one-sentence blurb, a theme tag,
the lead (linked to their People entry), and an "Ask the lead" email button.
Because each card is just a sentence, it rarely needs touching; when a project
ends, just delete its block (or move the lead to `alumni:` and remove the card).

```yaml
  - title: New project title
    lead: Kaleb Bordner          # MUST match the person's name in people.yml
    papers:                      # DOIs of papers that belong to THIS project
      - "10.2514/6.2026-4380"
    contact: lead@ucdavis.edu    # optional; powers the "Ask the lead" button
    theme: mechanics-dynamics    # morphology-kinematics · mechanics-dynamics · sensing-control
    image: /assets/img/research/yourfig.jpg   # optional figure
    blurb: >-
      One sentence describing the project.
```

- **The lead links to their People card.** Keep `lead` spelled exactly as their
  `name:` in `people.yml` (e.g. `Dr. Alfonso Martínez-Carmena`).
- **Link a paper by pasting its DOI** under `papers:` (one per line). The card
  looks the DOI up in the publications data and shows the title, year, and link:
  so when a new paper comes out, you add one line here and it appears. Leave
  `papers:` out and no paper line shows. (The paper must already be listed on the
  Publications page: journal articles arrive automatically; add conference papers
  in `_data/publications_manual.yml`.)

---

## Edit a facility: `_data/facilities.yml`

Each facility is one block. The first one with `featured: true` becomes the big
photo band at the top of the Facilities page; the rest render as alternating
photo rows. Prefer **specs** (big-number tiles) and short capability **chips** over
long paragraphs.

```yaml
- name: Center for Animal Locomotion and Innovation (CALI)
  featured: true                     # ONE facility only → the flagship band
  tagline: >-
    One credible line shown with the name.
  partner: Co-directed with Dr. …    # optional
  location: California Raptor Center, UC Davis   # optional
  url: https://…                     # optional "Learn more" button
  url_label: Visit the CALI consortium
  photo: /assets/img/facilities/cali.jpg
  photo_note: AI rendering based on real photos, to illustrate the setup.  # optional caption
  funding:                           # optional credit badge in the photo corner
    note: "DURIP support from:"
    name: DEVCOM Army Research Laboratory
    logo: /assets/img/partners/arl.png
    url: https://www.arl.army.mil/
  specs:                             # big-number tiles; keep `value` short
    - { value: "48", label: "OptiTrack motion-capture cameras" }
    - { value: "9", label: "high-speed Phantom cameras" }
  capabilities:                      # short qualitative chips
    - Sub-millisecond, sub-millimeter tracking
    - Daylight-balanced lighting for live birds
```

- **`featured:`**: set on exactly one facility. Its `photo` becomes the flagship band; a real photo works best (not the AI renderings).
- **`photo_note:`**: a small italic caption under the image (used to mark the wind-tunnel/specimen renderings as AI-based). Leave it off for real photos.
- **`funding:`**: shows a small "thanks to…" logo badge in the top corner of the flagship photo. Logos live in `assets/img/partners/`.

---

## Edit a Lab Guide page: `_guide/`

Each page is one Markdown file. Edit the text below the `---` block normally.
To **add a new guide page**, create `_guide/my-page.md` starting with:
```markdown
---
title: My new page
category: Working in the Lab
order: 4
summary: One sentence shown on the Lab Guide hub.
reviewed: 2026-07-03   # date you last checked the page (see "Keeping pages fresh")
---

Your content here. Use ## for section headings.
```
`category` must be one of the categories listed in `guide_order:` in
`_config.yml`: that list is the single source of truth for the category names
and their sidebar order. `order` sets the position within that category. To add a
brand-new category, add its name to `guide_order:` in `_config.yml`; the wiki
sidebar and the Lab Guide hub both read from there (the hub warns you if a page's
category isn't listed). The page automatically appears in the wiki sidebar and on
the Lab Guide hub.

Useful callout boxes (paste directly into a guide page):
```markdown
<div class="callout" markdown="1">
A helpful tip.
</div>

<div class="callout callout--warn" markdown="1">
A caution.
</div>

<div class="callout callout--stop" markdown="1">
Something important / a hard rule.
</div>
```

### Keeping pages fresh

Every guide page shows a **"Needs review" band** at the top once it hasn't been
reviewed or edited in over a year. To clear it, either edit the page or, if you
read it through and nothing needs changing, set `reviewed:` in its front matter
to today's date (for example `reviewed: 2026-07-03`). That records the review
without a content change. A page with no `reviewed:` date and no recent edit
shows the band by design, so nothing goes stale silently.

### Lab operations roles: `_data/roles.yml`

The public **Lab operations roles** page is generated from `_data/roles.yml`:
one entry per role with its `name`, `tagline`, `purpose`, `owns`, and `can`
(authority). Edit that file to add, retire, or reword a role; both the
at-a-glance table and the role cards update. Leave `_includes/lab-roles.html`
(the template) alone. Each role's detailed routine, what it avoids, and its
handoff live in the private Notion member portal, not on the public page.

---

## Change the menu: `_data/navigation.yml`
Reorder, rename, or add items. `cta: true` makes an item the pill button.

## Change site-wide settings: `_config.yml`
Title, tagline, the **member portal URL**, contact email, ORCID, the
undergraduate interest-form link, the PI **LinkedIn** and **GitHub org**, the
**FigShare** data URL, and the **social-share image** all live here. After
editing `_config.yml`, the change appears on the next build.

**Turn on analytics (optional).** The site ships with privacy-friendly,
cookieless analytics ([GoatCounter](https://www.goatcounter.com/)) that stay
**off** until you add a code. Make a free GoatCounter site, then set
`analytics: { goatcounter: "yourcode" }` in `_config.yml`. It collects only
anonymous page counts: no cookies, no personal data: so no consent banner is
needed (the [Privacy]({{ '/privacy/' | relative_url }}) page explains this to
visitors). Leave it blank to collect nothing.

---

## Add a research figure: `assets/img/research/`

Each project card on the Research page can show one figure. To add or change one:

1. Put an optimized JPG in `assets/img/research/` (see the image budget below).
2. In `_data/research.yml`, point that project's `image:` at it, e.g.
   `image: /assets/img/research/airfoil.jpg`. No `image:` = the card simply shows
   no figure (still valid).

`theme:` on each project must match a theme `id` in the same file. The three ids
are: **`morphology-kinematics`**, **`mechanics-dynamics`**, **`sensing-control`**.
A matching theme shows its label as a tag on the card. Each theme also has a
`why:` line ("why it matters") shown on the Home and Research pages: keep it to
one plain-language sentence.

---

## Recognition & media strips: `_data/recognition.yml`

The Home page shows an **Honors & awards** grid and a **Featured in** row from
this file. Add an award under `awards:` (`name`, `who`, `org`, `year`) or an
outlet under `media:` (`name`, `url`). Keep awards accurate and specific.

---

## People photos & the lab group photo

- **Headshots:** drop originals in `assets/img/people/_raw/`, run
  `bash scripts/apply-images.sh` (~1 min; resizes and compresses everything), then
  add `photo: /assets/img/people/<name>.jpg` to that person on `_data/people.yml`.
  No photo = a clean initials avatar.
- **PI bio:** Christina's featured bio is written directly in `people.html`
  (top of the page); edit the prose there.
- **Group photo:** run `bash scripts/apply-images.sh "/path/to/group-photo.jpg"`
  to create `assets/img/lab-photo.jpg`, then set `lab_photo: /assets/img/lab-photo.jpg`
  under `assets:` in `_config.yml`. This shows it at the top of People **and** as
  the cinematic "In the field" band under the Home hero.

### Role badges (the bird taxonomy 🦉🦢🦜🐥🕊️)
Each person card shows a small bird, chosen automatically from words in their
`role`: Postdoc 🦉 · PhD 🦢 · MSc 🦜 · Undergrad 🐥 · Visiting 🕊️ (the PI 🦅 is the
featured block, not a card). A legend appears above the team grid. To override
one person's bird, add `role_icon: "🦅"` to them in `_data/people.yml`.

### "Scenes from the lab" & the Join culture photo
- **Scenes (People):** put optimized photos in `assets/img/lab/` (or a large
  original in `assets/img/lab/_raw/` and run `apply-images.sh`). In
  `_data/gallery.yml`, point each scene's `file:` at your image, write the `alt`
  and `caption`, and set `ready: true`. A scene only shows when `ready: true`.
- **Join culture photo:** set `culture_photo:` under `assets:` in `_config.yml`
  to a photo in `assets/img/lab/` to show it on the Join page.

Every one of these is optional and only appears once its file/flag is set, so the
site never shows a broken image.

---

## Home page components (where the copy lives)

These live directly in `index.html` (edit the text in place):

- **Video hero**: background video is `assets/video/bird-glide.mp4` with a dark
  overlay and a pause/play button. It auto-hides for visitors who set "reduce
  motion." To swap the clip, replace the `.mp4` (keep it small: see budget). The
  poster frame shown before the video loads is `assets/img/facilities/cali.jpg`.
- **Brand band**: the logo + one-line "principles, not mimicry" statement.
- **"A signature idea"**: the three-axis bio-inspired reporting framework
  (source / mimicry / evidence) tied to Harvey 2026.
- **"We run our lab in the open"**: links to the Lab Guide, GitHub, and blog.
- **Supported by / In partnership with**: funder logos from `_data/funders.yml`
  and partner organizations from `_data/collaborators.yml` (see below).

### Funders & partners: two files
- **`_data/funders.yml`**: the home page **"Supported by"** logo band (AFOSR,
  Packard, NSF, ARL, CITRIS…). Each entry has `name`, `short` (the name shown
  under the logo), `url`, and `logo:`. Logos sit in a fixed-height box so their
  names line up across the row.
- **`_data/collaborators.yml`**: the home page **"In partnership with"** strip of
  partner *organizations* (California Raptor Center, California Hawking Club, the
  museum). Each entry: `name`, `sub` (short descriptor), `photo` (square image in
  `assets/img/partners/`), `url`. Individual academic collaborators stay in
  `people.yml` under `affiliates`.

Drop all logos in `assets/img/partners/`.

---

## Image size budget (keep the site fast & accessible)

| Asset | Target size | Max file |
|---|---|---|
| Research figure / card | ~1280 px wide | ≤ 120 KB |
| Lab group photo | ~1600 px wide | ≤ 300 KB |
| Headshot | 600 × 600 px | ≤ 80 KB |
| Social/OG image | 1200 × 630 px | ≤ 200 KB |
| Background video | 1080p, short loop | ≤ 3 MB |

**One-liner to optimize a JPG on a Mac** (built-in `sips`, no installs):

```bash
sips -s format jpeg -s formatOptions 82 input.jpg --resampleWidth 1280 --out output.jpg
```

`scripts/apply-images.sh` does all of the above for the group photo, OG image,
and headshots in one step.
