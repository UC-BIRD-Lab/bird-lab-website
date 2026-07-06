---
title: Data management
category: Research Workflow
order: 4
summary: Data hygiene, backups, file naming, and version control expectations.
keywords: [data management, backup, file naming, storage, Box, organization, data hygiene]
icon: "🗄️"
reviewed: 2026-07-05
---

## Scientific data practices

<div class="callout callout--stop" markdown="1">
**Never** modify any source files. Do all data cleaning programmatically, and
never overwrite or touch original files once they're generated. Save any
adjustments as separate *derived* files so the raw data stays untouched.
</div>

- Don't encode information in cell colors in Excel.
- Variable names should be short but descriptive.
- Store output data as `.csv` when possible.
- Read up on [tidy data](https://r4ds.had.co.nz/tidy-data.html).
- Write a script that outputs every number you report in a paper.

Once your data is clean and backed up, see [Data analysis]({{ '/lab-guide/data-analysis/' | relative_url }}) for how we explore, quantify, and report it with uncertainty.

## Back up your files

The lab's shared Box folder is the system of record for all data, documents,
photos, and videos. UC Davis provides it with unlimited storage, and it keeps a
version history of recent changes. Work out of Box so your files are backed up at
all times.

Once a month, back up your Box data to an external lab hard drive. Keeping a
second copy off the cloud is your responsibility as much as the PI's.

- Don't use spaces in file names.
- Don't load data files directly into Notion; keep data in Box and keep only lab documentation in Notion.
- Use the format `YYYY_MM_DD_LastName_FileDescription.ext` for shared files, and consider it for personal files too.

## Share and archive on publication

We manage data to be [FAIR](https://www.go-fair.org/fair-principles/): findable,
accessible, interoperable, and reusable. In practice that means:

- When a paper is published, its data (both raw and derived) are made public with
  a citable DOI, and the associated code repositories are made public alongside it.
- Data are archived for the long term so the work stays reproducible after the
  project ends.

Operational details, including retention periods and where physical backups live,
are in the [member portal]({{ '/portal/' | relative_url }}).

## Version control

All code-based projects must be version-controlled and linked to a remote
repository in the UC-BIRD-Lab organization. For Git setup, workflow, and naming
conventions, see [Code]({{ '/lab-guide/code/' | relative_url }}).
