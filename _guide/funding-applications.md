---
title: Funding applications
category: Professional Development
order: 1
summary: How to approach fellowships and grants, what reviewers may look for and how to write a strong proposal.
keywords: [funding, fellowships, grants, scholarships, proposals, stipend]
icon: "💰"
reviewed: 2026-07-05
---



## Fellowships & scholarships to explore

A running list of funding you can bring to, or pursue for, a spot in the lab. It spans undergraduate through postdoc, so check the **level** and **eligibility** columns, and always confirm the current deadline on each program's own page.

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
Christina know. For conference travel awards specifically, see
[Conferences]({{ '/lab-guide/conferences/' | relative_url }}).

<aside class="marginnote" markdown="1">
Most fellowship applications also need
[recommendation letters]({{ '/lab-guide/recommendation-letters/' | relative_url }});
request them early.
</aside>

## The goal

You're trying to convince a panel that:

- your idea is brilliant and "transformative" for the field;
- you have the unique skills to bring the project to life; and
- the project is doable within the granting period.

<div class="callout" markdown="1">
Don’t underestimate the importance of being confident and believing in yourself while you’re writing.
</div>

## General tips

<aside class="marginnote marginnote--warn" markdown="1">
Never use AI to draft scientific text, it'll add em dashes everywhere and the risk that it plagiarizes others is way too high to be worth it.
</aside>

- **Check the application details early.** Requirements are often hidden in the
  templates and formatting of the actual application form.
- **Know the foundational research** in your area so you can identify real gaps in the field.
- **Avoid jargon.** Explain the work in a straightforward way: it's hard to predict the expertise of your reviewers.
- **Consider a traditional outline:**
  - **Background**, with a summary sentence in the first paragraph (e.g., "Here, I will show…").
  - **Methods:** make sure to be very clear and specific, even listing specific equipment. The reviewers want to be sure you actually know how you’ll do what you’re proposing.
  - **Results**
  - **Discussion**
- **Get multiple reviewers.** Review panels are made of many people usually. You can't make everyone happy, but you can try! Have several people read and edit your application, and give them a specific list of what the granting agency is looking for.
- **Use AI appropriately.** Christina likes to use AI tools as pre-reviewers. They can check for typos and grammar, and ensure that your logical flow is sound and paragraphs are clear and understandable. See [Using AI]({{ '/lab-guide/using-ai/' | relative_url }}) for the lab's full policy.

