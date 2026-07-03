---
title: Applying for funding
category: Professional Development
order: 2
summary: How to approach fellowships and grants — what reviewers want and how to write a strong proposal.
---



## Fellowships & scholarships to explore

A running list of funding you can bring to — or pursue for — a spot in the lab. It
spans undergraduate through postdoc, so check the **level** and **eligibility**
columns, and always confirm the current deadline on each program's own page.

<div class="fund-table-wrap">
<table class="fund-table" id="fund-table">
<caption class="visually-hidden">Curated fellowships and scholarships</caption>
<thead>
<tr><th scope="col">Fellowship / scholarship</th><th scope="col">Level</th><th scope="col">Eligibility</th></tr>
</thead>
<tbody>
{%- for f in site.data.funding -%}
<tr class="fund-row">
<td class="fund-name" data-label="Fellowship">{% if f.url %}<a href="{{ f.url }}" rel="noopener">{{ f.name }}<span class="fund-ext" aria-hidden="true"> ↗</span></a>{% else %}{{ f.name }}{% endif %}</td>
<td class="fund-level" data-label="Level">{% if f.level %}{% assign levels = f.level | split: "," %}{% for lv in levels %}<span class="fund-pill">{{ lv | strip }}</span>{% endfor %}{% else %}<span class="fund-any">Any</span>{% endif %}</td>
<td class="fund-elig" data-label="Eligibility">{{ f.eligibility | default: "Open to all" }}</td>
</tr>
{%- endfor -%}
</tbody>
</table>
</div>
<button type="button" class="btn btn--ghost fund-toggle" data-target="fund-table" data-preview="6" aria-expanded="false" hidden>Show all {{ site.data.funding | size }} fellowships &darr;</button>

If you come across other internal or external funding opportunities, or if any links are stale, please let
Christina know. 

## The goal

You're trying to convince a panel that:

- your idea is brilliant and "transformative" for the field;
- you have the unique skills to bring the project to life; and
- the project is doable within the granting period.

<div class="callout" markdown="1">
Don't underestimate the importance of being confident and believing in yourself
while you write.
</div>

## General tips

- **Check the application details early.** Requirements are often hidden in the
  templates and formatting of the actual application form.
- **Know the foundational research** in your area so you can identify real gaps
  in the field.
- **Avoid jargon.** Explain the work plainly — it's hard to predict the expertise
  of your reviewers.
- **Consider a traditional outline:**
  - **Background**, with a summary sentence in the first paragraph (e.g., "Here,
    I will show…").
  - **Methods** — make these very clear, even listing specific equipment.
    Reviewers want to be sure you know how you'll do what you propose.
  - **Results**
  - **Discussion**
- **Get multiple reviewers.** Have several people read and edit your application,
  and give them a specific list of what the granting agency is looking for.
