# Maintenance

Everything you need to keep the site current and healthy. Most updates are a
one- or two-line edit to a file in `_data/`. See [CONTENT-GUIDE.md](CONTENT-GUIDE.md)
for copy-paste templates.

---

## Keeping publications current

### The automated part (journal articles)
- A GitHub Action — **Update publications** — runs on the **1st of each month**
  (and on demand from the **Actions** tab → *Run workflow*).
- It calls **OpenAlex** for the PI's **ORCID** (`0000-0002-2830-0844`), finds any
  journal articles not already listed, and **opens a pull request** editing
  `_data/publications.yml`.
- You review the PR (check title, authors, venue, DOI), fix anything, and
  **merge**. Merging republishes the site.

**Why it's safe:** the committed `publications.yml` is the source of truth. If
OpenAlex is unreachable or returns nothing, the script changes nothing. It only
*adds* articles whose DOI is new, so your manual corrections are never
overwritten.

**Run it by hand / locally:**
```bash
pip install -r scripts/requirements.txt
python scripts/update_publications.py     # edits _data/publications.yml if needed
```

### The manual part (conferences, posters, talks, blogs)
OpenAlex doesn't reliably index conference posters and talks, so add those by
hand in **`_data/publications_manual.yml`**. Copy an existing block and edit it.

### If an author name or venue looks wrong
Edit the entry directly in `_data/publications.yml` and commit. Future syncs keep
your version (they match on DOI).

---

## Common content updates

| To change… | Edit this file |
| --- | --- |
| A team member (add / remove / promote) | `_data/people.yml` |
| A conference paper, talk, or poster | `_data/publications_manual.yml` |
| A research project or theme | `_data/research.yml` |
| A news milestone | `_data/updates.yml` |
| Press coverage | `_data/press.yml` |
| Funders shown on the home page | `_data/funders.yml` |
| Honors & "featured in" media | `_data/recognition.yml` |
| A facility | `_data/facilities.yml` |
| A Lab Guide page | the matching file in `_guide/` |
| The top menu | `_data/navigation.yml` |
| Site title, URLs, portal link, contact email | `_config.yml` |

Step-by-step examples with templates are in [CONTENT-GUIDE.md](CONTENT-GUIDE.md).

**No editing at all:** lab members can submit a person, paper, news item, or press
link via the repo's **Issues → New issue** forms; a maintainer applies them in
seconds. The full delegation workflow is in [CONTRIBUTING.md](CONTRIBUTING.md).

### Adding member photos
By default each person shows an initials avatar (so there are never broken
images). To use a real photo: put the file in `assets/img/people/` and add
`photo: /assets/img/people/firstname-lastname.jpg` to that person in
`people.yml`. Use a roughly square image (≈ 400×400px) and always-meaningful
filenames.

---

## Keeping it accessible (when you edit)

- **Don't skip heading levels.** Use `##` then `###`; never jump `##` → `####`.
- **Write real link text.** "See the [funding guide](…)", not "click [here](…)".
- **Every informative image needs `alt` text.** Decorative images get empty `alt`.
- **Don't hard-code colors** for text; the theme already meets AA contrast.
- **Tables are for data,** not layout.
The palette lives in `assets/css/overrides.css` (it loads after `style.css` and
wins). If you change a color, re-check text/background contrast with
[WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
(aim for 4.5:1 for body text).

---

## Periodic checks (a few minutes, quarterly)

- Skim the **Actions** tab for any red (failed) runs.
- Review/merge any open **publications** pull requests.
- Update **People** for joins, departures, and graduations.
- Add notable **News** milestones and **Press**.
- Confirm the **Join** page hiring status is current.

---

## Troubleshooting

**A build failed (red ✗ in Actions).**
Open the failed run and read the last red lines. The usual cause is a YAML typo —
often a missing space after a colon, or inconsistent indentation. YAML is
space-sensitive: use **two spaces** to indent, never tabs. Paste the file into a
[YAML linter](https://www.yamllint.com/) to find the line.

**My change didn't appear.**
Give it 1–2 minutes, then hard-refresh. Check the Actions tab shows a green run
*after* your commit. If the run is red, see above.

**A page 404s.**
Permalinks come from the file location/front matter. If you renamed a `_guide/`
file, its URL changed — update any links to it.

**The publications PR wasn't created.**
Confirm **Settings → Actions → General** allows Actions to create pull requests
(see [DEPLOYMENT.md](DEPLOYMENT.md) step 5). If there were simply no new papers,
that's expected — the run is green and no PR is opened.

**Member Portal button goes to the wrong place.**
Update `member_portal_url` in `_config.yml` to your Notion workspace link, commit,
and wait for the rebuild.

**A submitted issue form needs applying.**
Open the issue, copy its values into the matching `_data/*.yml` file using the
cheat-sheet in [CONTRIBUTING.md](CONTRIBUTING.md), commit, and close the issue.
