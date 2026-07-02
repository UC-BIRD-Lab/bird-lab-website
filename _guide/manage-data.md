---
title: Manage data
category: Research Workflow
order: 4
summary: Data hygiene, backups, file naming, and version control expectations.
---

## Scientific data practices

<div class="callout callout--stop" markdown="1">
**Never** modify any source files. Do all data cleaning programmatically, and
never overwrite or touch original files once they're generated.
</div>

- Don't encode information in cell colors in Excel.
- Variable names should be short but descriptive.
- Store output data as `.csv` when possible.
- Read up on [tidy data](https://r4ds.had.co.nz/tidy-data.html).
- Write a script that outputs every number you report in a paper.

## Back up your files

UC Davis provides storage through Box and Google Drive. Work out of a folder that
is mirrored or backed up at all times.

- Don't use spaces in file names.
- Don't load data files directly into Notion — keep documents in cloud storage and keep only lab documentation in Notion.
- Use the format `YYYY_MM_DD_LastName_FileDescription.ext` for shared files, and consider it for personal files too.

## Version control with Git

All code-based projects must be version-controlled and linked to a remote
repository. You'll need a GitHub account added to the UC-BIRD-Lab organization.

<div class="callout callout--warn" markdown="1">
Push commits at least once a day.
</div>

For first-time Git setup, install Git and set your username and email (see the
[Start guide]({{ '/lab-guide/start-guide-grads/' | relative_url }})). To start a
new project, create the repository on GitHub (owner = UC-BIRD-Lab for shared
projects), give it a unique CamelCase name with no spaces, set permissions, and
clone it from your IDE (PyCharm: *Get from VCS*; RStudio: *File → New Project →
Version Control → Git*). A Python and an R project can share the same remote
repository.
