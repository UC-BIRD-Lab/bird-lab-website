# Automation

Every bot follows one rule: when X happens, run a script and propose the result
as a pull request. Nothing goes live until a human merges. Workflows
(`.github/workflows/*.yml`) say when and what; scripts (`scripts/*.py`) do the
work and can be run by hand.

| Workflow | Runs | Does | Result |
|---|---|---|---|
| `site-checks.yml` | every PR | content validation, links and images, WCAG 2.1 AA scan | blocks merge on failure |
| `optimize-images.yml` | PRs touching `assets/`; merges to `main` | PR: fails over budget. Merge: compresses | blocks merge, or PR with smaller files |
| `deploy.yml` | merge to `main` | build and publish | live site updates |
| `update-publications.yml` | 1st of the month | new OpenAlex papers by ORCID, with open-access links | PR editing `_data/publications.yml` |
| `issue-to-pr.yml` | issue form submitted | form → `_data` entry | PR; issue closes on merge |
| `review-sweep.yml` | 5 Jan/Apr/Jul/Oct | overdue guide pages, `_data/review.yml`, expired banner | rewrites one issue |
| `guide-link-check.yml` | 12 Jan/Apr/Jul/Oct | Lab Guide outside links | rewrites one issue |
| `link-rot-check.yml` | 19 Jan/Apr/Jul/Oct | DOIs, press, data/code links | rewrites one issue |

Run any by hand: **Actions → workflow → Run workflow**. Locally:

```
python3 scripts/validate_content.py
python3 scripts/review_sweep.py
python3 scripts/optimize_images.py      # --check to report only
python3 scripts/check_links.py
python3 scripts/add_press.py …
```

## Changing things

- **Schedule:** the `cron:` line (minute hour day month weekday, UTC), e.g.
  `"0 9 5 1,4,7,10 *"`; twice a year is `1,7`.
- **Media limits:** constants at the top of `scripts/optimize_images.py`.
- **What gets reviewed:** `_data/review.yml`.
- **Bot wording** (PR titles, comments): quoted strings in the workflow file.
- **Roles and news types:** `ROLE_GROUP` and `NEWS_TYPES` in
  `scripts/issue_to_change.py`, matching the dropdowns in
  `.github/ISSUE_TEMPLATE/`; the content check fails if they drift.

## If a run is red

Open it in **Actions**; the last red line says why, and Content validation
names the file. Nothing is live. Fix the input and re-run, or close the bot's PR
to discard it.
