---
title: Funding applications
category: Professional Development
order: 1
summary: How to approach fellowships and grants, what reviewers may look for and how to write a strong proposal.
description: "Fellowships worth applying for, and what reviewers tend to reward when they read a proposal."
keywords: [funding, fellowships, grants, scholarships, proposals, stipend]
icon: "💰"
reviewed: 2026-09-14
---

## The goal

You're trying to convince a panel that:

- your idea is brilliant and could change what the field understands;
- you have the unique skills to bring the project to life; and
- the project is doable within the granting period.

For a fellowship, the panel is judging you as well as the project, so your
statements and letters matter as much as the research plan.

<aside class="marginnote" markdown="1">
Most fellowship applications also need
[recommendation letters]({{ '/lab-guide/recommendation-letters/' | relative_url }});
request them early.
</aside>

<div class="callout" markdown="1">
Don’t underestimate the importance of being confident and believing in yourself while you’re writing.
</div>

## What reviewers look for {#what-reviewers-look-for}

Use these ten points as a checklist when you outline, and again before you send a draft for feedback.

1. <span id="outside-reader"></span>**Write for someone outside your specialty.** Make the question, rationale, and significance clear without requiring reviewers to fill in missing reasoning.
2. <span id="enough-detail"></span>**Give enough detail to assess the science.** An exciting idea still needs a convincing experimental design, sample size justification, and analysis plan.
3. <span id="answer-the-question"></span>**Explain how the data will answer the question.** Go beyond promising to collect or “integrate” data. Show what different outcomes would mean for your hypotheses and broader understanding.
4. <span id="pitfalls"></span>**Identify pitfalls and realistic alternatives.** Explain how you will adapt if an approach fails, especially when later aims depend on earlier results.
5. <span id="payoff"></span>**Make the scientific payoff explicit.** What could we understand differently if the work succeeds? Explain that contribution rather than relying on labels such as “novel” or “transformative.”
6. <span id="scope"></span>**Match the scope to the resources.** The proposed work should be achievable with the available time, people, and budget. Adding more work does not automatically strengthen an application.
7. <span id="broader-impacts"></span>**Evaluate broader impacts when requested.** Identify who should benefit, what should improve, and how you will assess whether the activity worked.
8. <span id="methods-serve-question"></span>**Choose methods that serve the question.** Use AI or another priority area when it contributes to the science, and explain why it belongs.
9. <span id="feedback-early"></span>**Seek feedback early.** Ask an experienced proposal writer outside your immediate specialty to read the draft while there is still time for substantive revision.
10. <span id="persist-revise"></span>**Persist and revise.** Strong proposals can remain unfunded. Use reviewer feedback to improve both the explanation and the research plan before submitting again.

## General tips

<aside class="marginnote marginnote--warn" markdown="1">
**Lab policy:** never use AI for first drafts. It'll add em dashes everywhere, and the risk that it plagiarizes others is way too high to be worth it. Instead, Christina prefers to use AI tools as "pre-reviewers": she uses prompts to request checks for typos and grammar, and ensure that the logical flow is sound and paragraphs are clear and understandable. See [Using AI]({{ '/lab-guide/using-ai/' | relative_url }}) for the lab's full policy.
</aside>

- **Check the application details early.** Requirements are often hidden in the
  templates and formatting of the actual application form.
- **Borrow the paper drafting cycle.** Proposals don't need every step, but an outline and a short check-in with Christina before you write, and feedback on a complete draft, help you catch problems while there's still time to fix them. See the [drafting cycle]({{ '/lab-guide/writing-papers/' | relative_url }}#the-drafting-cycle).
- **Know the foundational research** in your area so you can identify real gaps in the field.
- **Consider a standard proposal outline,** unless the application sets its own sections:
  - **Background**, with a summary sentence in the first paragraph (e.g., "Here, I will show…").
  - **Aims:** the specific questions or hypotheses the work will test.
  - **Methods:** make sure to be very clear and specific, even listing specific equipment. The reviewers want to be sure you actually know how you’ll do what you’re proposing.
  - **Expected results:** what different outcomes would mean (see [how the data will answer the question](#answer-the-question)).
  - **Pitfalls, alternatives, and timeline:** how you'll adapt, and why the work fits the time and budget (see [pitfalls](#pitfalls) and [scope](#scope)).
- **Use the paper-writing guidance.** Clear writing works the same way in a proposal; see [what every reader needs]({{ '/lab-guide/writing-papers/' | relative_url }}#what-readers-need) and the [writing reference]({{ '/lab-guide/writing-papers/' | relative_url }}#reference) for precise words and paragraph structure.
- **Get multiple reviewers.** Review panels are made of many people usually. You can't make everyone happy, but you can try! Have several people read and edit your application, and give them a specific list of what the granting agency is looking for. See [Getting feedback]({{ '/lab-guide/writing-papers/' | relative_url }}#feedback) for how review rounds work in the lab.

Before you submit, work through the
[Before you submit checklist]({{ '/lab-guide/before-you-submit/' | relative_url }}), including the grant and fellowship items.

## Report what you apply for and what you win

<div class="callout callout--stop" markdown="1">
**Email Christina every time you apply for, or receive, a fellowship, award, or funded contract.** Federal grant applications require Christina to certify the lab's current and pending support, including outside funding for people in the lab, so she needs these on file.
</div>

- **When you apply:** what you applied for, the amount requested, and the proposed start and end dates.
- **When you hear back:** the outcome, either way. If funded, forward the award letter and note whether it covers your full stipend or salary.
- **If anything changes:** renewals, supplements, or withdrawals.

## Fellowships & scholarships to explore

A running list of funding you can bring to, or pursue for, a spot in the lab. It spans undergraduate through postdoc, so check the **level** and **eligibility** columns, and always confirm the current deadline on each program's own page.

<details class="guide-details" markdown="1">
<summary>Show all {{ site.data.funding | size }} fellowships and scholarships</summary>

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

</details>

If you come across other internal or external funding opportunities, or if any links are stale, please let
Christina know. For conference travel awards specifically, see
[Conferences]({{ '/lab-guide/conferences/' | relative_url }}).
