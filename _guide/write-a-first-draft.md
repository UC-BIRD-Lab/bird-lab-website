---
title: Write a first draft
category: Writing & Dissemination
order: 1
summary: Core principles, checklists, and authorship policy for manuscripts, preprints, and conference papers.
---

Strong scientific writing makes your *reasoning* visible — it doesn't ask the
reader to guess what matters or hunt for the takeaway. The goal isn't to imitate
anyone's style, but to write like an independent researcher whose argument stands
on its own. Every claim carries your name and your co-authors' names; treat each
one as something you personally vouch for. This page is the writing-side companion
to [Design your figures]({{ '/lab-guide/design-your-figures/' | relative_url }}).

<div class="callout callout--warn" markdown="1">
**Lab policy — the non-negotiables**

- Christina has the draft ≥2 weeks before any external deadline (she reserves the right to pull late submissions).
- No submission without explicit approval from Christina *and* all co-authors.
- ≥2 labmate pre-reviews before the draft reaches Christina (post in #phone-a-friend).
- Reference managers required (BibTeX / Zotero / EndNote) — no manually typed references.
- Data and code are made public on publication, except where privacy, ethics, legal, proprietary, or collaborator constraints require otherwise — raise these early.
</div>

## Core principles

**1 · Lead with the question, not the background.** State the problem and its
stakes early. A strong introduction is well cited — but synthesized: each citation
is there because it builds the case for *your* question, not to show how much
you've read.

**2 · One takeaway, visible everywhere.** Your paper has one or two core
takeaways. The *same* takeaways must appear in the abstract, introduction,
results, discussion, conclusion, and figure captions. The conclusion summarizes
what you found and why it matters — it doesn't restate the introduction or add new
information.

**3 · Make each paragraph do one job, in order.** At the document level, use the
hourglass: broad → specific question and method → broad implications. At the
paragraph level: topic sentence → evidence → interpretation → mini-takeaway. Use
plain signposts ("To test this, we…", "This result suggests…").

**4 · Keep claims proportional to evidence.**

<div class="callout callout--warn" markdown="1">
This is the principle most tied to your reputation. An overclaim is a credibility
problem — a reviewer who catches one starts doubting *everything*, and the doubt
attaches to every name on the paper. Honesty about limitations is what makes your
supported claims trustworthy.
</div>

Keep three things separate and visible: what the data directly show, what you
infer, and what remains uncertain. Watch empty intensifiers (*drastically, very,
significant* used loosely). The fix is rarely deletion — it's scoping the claim to
what you measured. *e.g.* ❌ "Our design dramatically improves flight efficiency." →
✅ "Our design reduced power consumption by 12% in level flight (wind tunnel,
*n* = 8 trials); we did not test maneuvering or gust conditions."

**5 · Report results so they can be checked.** "Improved" means nothing without
*compared to what, by how much, on what metric.* Always report sample size (*n*),
the test used, the test statistic, the exact *p*-value, and what the error bars
represent — plus effect size, confidence intervals, and inclusion/exclusion
criteria where appropriate. Reproducibility is a *writing* requirement: report
provenance, software versions, mesh/calibration details, and environmental
conditions.

<div class="callout callout--warn" markdown="1">
**Lab requirement:** maintain an annotated script that traces every number in the
draft back to its source. This is how we catch errors before reviewers do.
</div>

**6 · Use words precisely, or don't use them.** Load-bearing words must carry their
exact meaning, consistently across sections: *significant* (only statistical —
name the test), *robust* (to what?), *converged* (what, to what value, under what
condition?), *improved* (vs. what, by how much, on what metric?). Cut *very,
obviously, extremely, actually*. Every "this" needs a following noun. Define
acronyms at first use.

**7 · Write directly.** Prefer "We found…", "We show…", "The data indicate…" over
"It was observed that…". Past tense for what you did and found; present for general
facts and figure descriptions. Passive voice is fine in Methods where the actor is
irrelevant.

**8 · Make figures carry weight.** Figures are often where a reader looks first.
They must be self-contained, with mechanics in the caption (not the body text).
See [Design your figures]({{ '/lab-guide/design-your-figures/' | relative_url }}).

**9 · Write so everyone can follow you.** Our work sits at the aerospace–biology
interface, and your reader rarely lives in both fields. Decide your primary
audience, then write so the secondary field can still follow without feeling
lectured. Give half a sentence of grounding the first time a term is load-bearing
in one field but unfamiliar to the other. Scope every claim to what you actually
studied — one wingbeat, one individual, one species — not silently "birds."

**10 · Name the limitations and uncertainty before a reviewer does.** Interface
work always contains an abstraction gap (a wind-tunnel model is not a flying
animal; a CFD simulation is not a wind tunnel). Name it first. Be precise about
which kind of uncertainty your error bars represent: biological variation,
measurement noise, or numerical/model error.

**11 · Label bio-inspiration by its evidence, not its appeal.** *Bio-inspired*,
*biomimetic*, and *bio-informed* are load-bearing terms. For every such claim,
report three things together: the specific source of inspiration, the level of
design mimicry, and the strength of biological evidence. Reserve *biomimetic* for
near-mimicry and *bio-informed* for designs integrating a principle supported by at
least single-species primary evidence. See
[Harvey (2026), *How bio-inspired is your design?*](https://doi.org/10.1038/s44172-026-00641-4)

**12 · Revision is the work, not the cleanup.** Strong writing comes from many full
passes. Read the whole draft top to bottom, repeatedly — it's the only way to see
whether the *argument* holds.

<div class="callout" markdown="1">
For reference, Christina's own papers routinely reach ~version 20 before
submission — that's normal and healthy. It's her job to help you revise, so don't
hold back.
</div>

## How expectations ramp

Standards scale with two things: how permanent and scrutinized the output is, and
how many passes the draft has been through. The more public and peer-reviewed the
venue, the harder every claim is pushed (journal paper = top of the ramp). Early
drafts get feedback on *structure and message*; as sentences stabilize, feedback
moves into terminology, statistics, and notation. Big-picture comments early aren't
ignoring details — they're saving them for when they'll stick.

## Journal article vs. conference paper

The core principles hold for both; what changes is strategy.

| | Journal article | Conference paper |
| --- | --- | --- |
| **Goal** | The complete, definitive account | A solid, citable checkpoint |
| **What to include** | Strongest, fully validated results | Boring-but-bulletproof results; hold exciting findings back |
| **Risk posture** | Claims fully defended; limits stated | Even more conservative |
| **Scope** | Broad enough to support the full argument | Narrow, self-contained, finishable |
| **Reuse** | Stands alone | Shouldn't "spend" results you need for the journal version |

**Null and underperformance results count** — a clean negative result, honestly
reported, is exactly what a conference paper is for. *Rule of thumb: Journal = your
best work, fully defended. Conference = your safest work, cleanly presented.*

## Protecting your name (and your co-authors')

Once a paper is public it is permanent and collective. The habits that protect
everyone on the author list: never claim more than the data support; trace every
number; at conferences stake only what you can defend; every co-author signs off
before submission (send drafts to one reviewer at a time); disclose honestly
(funding, conflicts, data/image permissions, AI use, ethics approvals); and give
review the time it needs.

## Before you send a draft (checklist)

- [ ] Main takeaway in one sentence, and the same one in the abstract, results, and conclusion.
- [ ] Introduction makes the question and stakes clear within two paragraphs.
- [ ] Every paragraph has one job; its first sentence says what.
- [ ] Claims proportional to evidence; observation, inference, and uncertainty are distinguishable.
- [ ] Each "bio-inspired" claim reports source organism, level of mimicry, and strength of evidence.
- [ ] Results quantified — *n*, test, statistic, exact *p*, error-bar meaning.
- [ ] Conclusion lands the existing argument and adds no new idea.
- [ ] Figures stand on their own and are each referenced; run the [figure checklist]({{ '/lab-guide/design-your-figures/' | relative_url }}).
- [ ] Load-bearing terms defined or cut; empty intensifiers removed; every "this" has a noun.
- [ ] Units, spelling, hyphenation, and notation consistent; every number internally consistent.
- [ ] An annotated script traces every number to its source.
- [ ] Venue requirements and all disclosures met.
- [ ] ≥2 labmate pre-reviews done; Christina has the draft ≥2 weeks before the deadline; all co-authors approved.

## Authorship policy

**Roles.** The project lead who contributes the largest share (≥50% across
conception/design, data, analysis, and writing) is first author; comparable
contributions are listed as co-first with an equal-contribution note. Christina is
generally last (supervising) author on lab-led work. Lead PhD students may serve as
corresponding author if they can respond to editor/reviewer/media email within two
business days during active review.

**Eligibility** (all four required, per [ICMJE](https://www.icmje.org/recommendations/browse/roles-and-responsibilities/defining-the-role-of-authors-and-contributors.html)):
substantial contributions to conception/design or data; drafting or critical
revision; final approval; and accountability for the work. Proofreading,
brainstorming, and routine technical help normally earn acknowledgements, not
authorship.

**Order** reflects relative contribution at submission; we create an authorship
plan at project start, revisit at milestones, and finalize before submission. AI
systems are not authors. Raise any questions with Christina early.

## Step-by-step: publishing a journal paper

1. Select the target journal (look at where the papers you cite were published).
2. Create the figures and draft their captions *before* writing.
3. Run figures + captions by all co-authors.
4. Review the journal's "Information for Authors" page.
5. Outline by drafting a topic sentence per major paragraph.
6. Write the main-text draft; complete the checklist above.
7. Choose a declarative, short title.
8. Write the abstract ([Nature summary-paragraph style](https://www.nature.com/documents/nature-summary-paragraph.pdf)).
9. Send the full draft to reviewers one at a time (repeat 2–3×).
10. Send the updated draft to the last author.
11. Upload supporting data/code to [FigShare](https://figshare.com); reserve a DOI for the collection (don't publish yet).
12. Draft the cover letter; send to the last author for approval.
13. Re-read everything calmly.
14. Submit (do this with Christina the first time).
