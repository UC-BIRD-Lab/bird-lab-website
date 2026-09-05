# BIRD Lab website

> This and the other maintainer docs were written largely by AI (Claude) from the
> code in this repository; Christina checked that they work. Site-wide statement:
> [Accessibility](accessibility.md), *How this site is made*.

Public website of the **Bio-Informed Research & Design (BIRD) Lab**, UC Davis.
A static [Jekyll](https://jekyllrb.com/) site on GitHub Pages, kept current by
editing plain text files.

- [CONTENT-GUIDE.md](CONTENT-GUIDE.md): edit content
- [CONTRIBUTING.md](CONTRIBUTING.md): submit updates
- [MAINTENANCE.md](MAINTENANCE.md): publish, preview, fix
- [AUTOMATION.md](AUTOMATION.md): what the bots do
- [ARCHITECTURE.md](ARCHITECTURE.md): why it's built this way

## Run locally

Only for previewing; editing on github.com needs no setup.

```bash
./serve.sh        # Docker Desktop; serves http://localhost:4000
```
Native: `bundle install`, then `bundle exec jekyll serve` (macOS `eventmachine`
failure: see MAINTENANCE.md).

## What's where

```
.
├── _config.yml          site settings (title, URLs, portal link)
├── index.html           Home
├── research.html  people.html  publications.html  facilities.html  cali.html
├── news.html  join.md  contact.md  portal.md  404.html
├── lab-guide/index.html Lab Guide hub
├── _guide/*.md          Lab Guide pages
├── _data/               the content
│   ├── people.yml          team, grouped by role
│   ├── publications.yml    journal articles (auto-updated)
│   ├── publications_manual.yml  conference papers, posters, talks
│   ├── pub_links.yml       data/code/figure per paper, by DOI
│   ├── research.yml        themes and projects
│   ├── updates.yml         news timeline
│   ├── press.yml  media.yml  recognition.yml
│   ├── funders.yml  collaborators.yml  gallery.yml
│   ├── openings.yml        Join-page recruiting toggles and postings
│   ├── facilities.yml  safety.yml  funding.yml  roles.yml
│   ├── announcement.yml    site-wide banner with expiry
│   ├── review.yml          what to re-check, how often
│   ├── cali*.yml           CALI page: specs, rates, gallery, milestones, mentoring
│   └── navigation.yml      top menu
├── _layouts/  _includes/ templates
├── assets/              CSS, JS, images, video
├── scripts/             publications sync, press helper, checks, image tools
└── .github/             workflows and issue forms
```

Content is `_data/*.yml` and the `.md` pages; design is `assets/` and
`_layouts/`.

## How it's built

Jekyll on GitHub Pages: no runtime services, no database. Pull requests must pass
content validation, link/image checks and a WCAG 2.1 AA scan (the PI can push
to `main` directly; checks then run after the fact). Journal articles sync
monthly from OpenAlex by the PI's ORCID. Priorities in order: maintainability,
accessibility, scientific communication, automation, design. Trade-offs:
[ARCHITECTURE.md](ARCHITECTURE.md).

## License

Content © BIRD Lab, UC Davis. Built with Jekyll; hosted on GitHub Pages.
