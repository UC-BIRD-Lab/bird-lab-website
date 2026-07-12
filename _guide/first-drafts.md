---
title: First drafts
category: Writing & Dissemination
order: 2
summary: Core principles, checklists, and authorship policy for manuscripts, preprints, and conference papers.
keywords: [writing, manuscript, paper, draft, authorship, preprint, publishing]
icon: "✍️"
reviewed: 2026-07-11
math: true
---

<aside class="marginnote" markdown="1">
This is the writing-side companion to
[Figures]({{ '/lab-guide/figures/' | relative_url }}).
</aside>

<div class="guide-glance">
<div><span class="k">Jump to</span><a href="#non-negotiables">The non-negotiables</a> · <a href="#core-principles">Core principles</a> · <a href="#before-you-send-a-draft-checklist">Pre-send checklist</a> · <a href="#authorship">Authorship</a> · <a href="#step-by-step-publishing-a-journal-paper">Publishing steps</a></div>
</div>

Strong scientific writing makes your *reasoning* visible; it doesn't ask the
reader to guess what matters or hunt for the takeaway. The goal isn't to imitate
anyone's style, but to write like an independent researcher whose argument stands
on its own. Every claim carries your name and your co-authors' names; treat each
one as something you personally vouch for.

<aside class="marginnote" markdown="1">
**Why "#phone-a-friend"?** It's the channel in the lab's private Slack workspace
where you post work-in-progress and request peer review (ask Christina or your
mentor if you're not in it yet). Routing drafts through peers isn't just about catching
errors early. Giving feedback trains you to read critically (a skill you'll need
as a reviewer), and receiving it in a low-stakes setting builds the thick skin
peer review demands. Both get easier with practice.
</aside>

<div class="callout callout--stop" markdown="1" id="non-negotiables">
**Lab policy: the non-negotiables**

- Christina has the draft ≥2 weeks before any external deadline (drafts that arrive too late for co-author review may be deferred to a later submission window).
- No submission without explicit approval from Christina *and* all co-authors.
- ≥2 labmate pre-reviews before the draft reaches Christina (post in **#phone-a-friend** on the lab Slack; see [giving and receiving feedback]({{ '/lab-guide/communication/' | relative_url }}#giving-and-receiving-feedback)).
- Reference managers required (BibTeX / Zotero / EndNote); no manually typed references.
- Data and code are made public on publication, except where privacy, ethics, legal, proprietary, or collaborator constraints require otherwise; raise these early.

These exist to protect the work and everyone whose name is on it, and they cut both
ways: you get the same care and lead time in return.
</div>

## Core principles {#core-principles}

These apply to everything the lab publishes. Read them once; after that you'll
mostly live in the checklists below.

### 1 · Lead with the question, not the background

<aside class="marginnote" markdown="1">
🔍 **Ask yourself:** if a reader stopped after my first two paragraphs, would they
know what I'm studying and why it matters, and does every citation earn its place?
</aside>

State the problem and its
stakes early. A strong introduction is well cited, but synthesized: each citation
is there because it builds the case for *your* question, not to show how much
you've read.

### 2 · One takeaway, visible everywhere

<aside class="marginnote" markdown="1">
🔍 **Ask yourself:** can I state my main point in one sentence, and does every
section add support for that same point?
</aside>

Your paper has one or two core
takeaways. The *same* takeaways must appear in the abstract, introduction,
results, discussion, conclusion, and figure captions. The conclusion summarizes
what you found and why it matters; it doesn't restate the introduction or add new
information.

### 3 · Make each paragraph do one job, in order

<aside class="marginnote" markdown="1">
🔍 **Ask yourself:** what is this paragraph's one job, and does its opening sentence
say so?
</aside>

At the document level, use the
hourglass: broad → specific question and method → broad implications. At the
paragraph level: topic sentence → evidence → interpretation → mini-takeaway. Use
plain signposts ("To test this, we…", "This result suggests…").

### 4 · Keep claims proportional to evidence

<aside class="marginnote" markdown="1">
🔍 **Ask yourself:** can a reader tell which statements are observations, which are
inferences, and which are open questions?
</aside>

Keep three things separate and
visible: what the data directly show, what you infer, and what remains uncertain.
Watch empty intensifiers (*drastically, very, significant* used loosely). The fix
is rarely deletion; it's scoping the claim to what you measured. *e.g.*
❌ "Our design dramatically improves flight efficiency." →
✅ "Our design reduced power consumption by 12% in level flight (wind tunnel,
*n* = 8 trials); we did not test maneuvering or gust conditions."

<div class="callout callout--warn" markdown="1">
This is the principle most tied to your reputation. An overclaim is a credibility
problem. A reviewer who catches one starts doubting *everything*, and the doubt
attaches to every name on the paper. Honesty about limitations is what makes your
supported claims trustworthy.
</div>

### 5 · Report results so they can be checked

<aside class="marginnote" markdown="1">
🔍 **Ask yourself:** for each number I report, could a reader find where it came from
and how it was tested?
</aside>

"Improved" means nothing without
*compared to what, by how much, on what metric.* Always report sample size ($$n$$),
the test used, the test statistic, the exact $$p$$-value, and what the error bars
represent, plus effect size, confidence intervals, and inclusion/exclusion
criteria where appropriate. Reproducibility is a *writing* requirement: report
provenance, software versions, mesh/calibration details, and environmental
conditions. See [Data analysis]({{ '/lab-guide/data-analysis/' | relative_url }}) for
how we quantify and report uncertainty.

A result that satisfies this principle carries all of it in one place, e.g.

$$\bar{x} = 12.4 \pm 0.8~\text{W}\ (U,\ k=2,\ \text{95\% coverage}),\qquad
t(7) = 3.42,\quad p = 0.011,\quad d = 1.21$$

The value, its uncertainty and what that uncertainty means, the test, the statistic with its
degrees of freedom, the exact $$p$$, and the effect size. Report $$p = 0.011$$, not
$$p < 0.05$$; a threshold hides the number a reader needs.

<div class="callout callout--warn" markdown="1">
**Lab requirement:** maintain an annotated script that traces every number in the
draft back to its source. This is how we catch errors before reviewers do.
</div>

### 6 · Use words precisely, or don't use them

<aside class="marginnote" markdown="1">
🔍 **Ask yourself:** have I used a strong-sounding word without saying exactly what I
mean by it?
</aside>

Load-bearing words must carry their
exact meaning, consistently across sections: *significant* (only statistical, name
the test), *robust* (to what?), *converged* (what, to what value, under what
condition?), *improved* (vs. what, by how much, on what metric?). Cut *very,
obviously, extremely, actually*. Every "this" needs a following noun. Define
acronyms at first use.

### 7 · Write directly

<aside class="marginnote" markdown="1">
🔍 **Ask yourself:** does this sentence engage directly with the science, or describe
it from a distance?
</aside>

Prefer "We found…", "We show…", "The data indicate…" over
"It was observed that…". Past tense for what you did and found; present for general
facts and figure descriptions. Passive voice is fine in Methods where the actor is
irrelevant.

### 8 · Make figures carry weight

<aside class="marginnote" markdown="1">
🔍 **Ask yourself:** could each figure be understood on its own, and does my text say
what to look at?
</aside>

Figures are often where a reader looks first.
They must be self-contained, with mechanics in the caption (not the body text).
See [Figures]({{ '/lab-guide/figures/' | relative_url }}).

### 9 · Write so everyone can follow you

<aside class="marginnote" markdown="1">
🔍 **Ask yourself:** could a reviewer from the field I'm *less* trained in follow
this, and would they feel respected, not lectured?
</aside>

Our work sits at the aerospace-biology
interface, and your reader rarely lives in both fields. Decide your primary
audience, then write so the secondary field can still follow without feeling
lectured. Give half a sentence of grounding the first time a term is load-bearing
in one field but unfamiliar to the other. Scope every claim to what you actually
studied (one wingbeat, one individual, one species), not silently "birds."

### 10 · Name the limitations and uncertainty before a reviewer does

<aside class="marginnote" markdown="1">
🔍 **Ask yourself:** where does my model stop standing in for reality, have I named
that limit myself before a reviewer does, and have I said which kind of
uncertainty my numbers carry?
</aside>

Interface
work always contains an abstraction gap (a wind-tunnel model is not a flying
animal; a CFD simulation is not a wind tunnel). Name it first. Be precise about
which kind of uncertainty your error bars represent: biological variation,
measurement noise, or numerical/model error. These are different quantities and a reader cannot
tell them apart from the bar alone. A combined measurement uncertainty
$$u_c = \sqrt{u_A^2 + u_B^2}$$ is not the same thing as the biological spread across individuals,
and neither is the fluctuation of an unsteady flow; say in the caption which one you plotted. See
[Data analysis]({{ '/lab-guide/data-analysis/' | relative_url }}#error-and-uncertainty).

### 11 · Label bio-inspiration by its evidence, not its appeal

<aside class="marginnote" markdown="1">
🔍 **Ask yourself:** have I named the source organism, the level of mimicry, and the
strength of evidence behind every bio-inspired claim?
</aside>

*Bio-inspired*,
*biomimetic*, and *bio-informed* are load-bearing terms. For every such claim,
report three things together: the specific source of inspiration, the level of
design mimicry, and the strength of biological evidence. Reserve *biomimetic* for
near-mimicry and *bio-informed* for designs integrating a principle supported by at
least single-species primary evidence. See
[Harvey (2026), *How bio-inspired is your design?*](https://doi.org/10.1038/s44172-026-00641-4)

### 12 · Revision is the work, not the cleanup

<aside class="marginnote" markdown="1">
🔍 **Ask yourself:** when did I last read this draft all the way through, and what
changed because I did?
</aside>

<aside class="marginnote" markdown="1">
For reference, Christina's own papers routinely reach ~version 20 before
submission; that's normal and healthy. It's her job to help you revise, so don't
hold back.
</aside>

Strong writing comes from many full
passes. Read the whole draft top to bottom, repeatedly; it's the only way to see
whether the *argument* holds.

## How expectations ramp

<aside class="marginnote" markdown="1">
**Tip.** Once Christina is "in the weeds," she edits by reading out loud and fixes
any sentence she even slightly stumbles on; a stumble means it wasn't clear.
</aside>

Standards scale with two things: how permanent and scrutinized the output is, and
how many passes the draft has been through. The more public and peer-reviewed the
venue, the harder every claim is pushed (journal paper = top of the ramp). Early
drafts get feedback on *structure and message*; as sentences stabilize, feedback
moves into terminology, statistics, and notation. Big-picture comments early aren't
ignoring details; they're saving them for when they'll stick.

## Journal article vs. conference paper

<aside class="marginnote" markdown="1">
**Why hold exciting results back at a conference?** A conference is a fast, lightly
reviewed checkpoint, the wrong venue to stake a major claim, and publishing early
can weaken the novelty of the journal paper. Lead with the result you would defend
in your sleep.
</aside>

The core principles hold for both; what changes is strategy.

| Aspect | Journal article | Conference paper |
| --- | --- | --- |
| **Goal** | The complete, definitive account | A solid, citable checkpoint |
| **What to include** | Strongest, fully validated results | Boring-but-bulletproof results; hold exciting findings back |
| **Risk posture** | Claims fully defended; limits stated | Even more conservative |
| **Scope** | Broad enough to support the full argument | Narrow, self-contained, finishable |
| **Reuse** | Stands alone | Shouldn't "spend" results you need for the journal version |

**Null and underperformance results count.** A clean negative result, honestly
reported, is exactly what a conference paper is for. *Rule of thumb: Journal = your
best work, fully defended. Conference = your safest work, cleanly presented.*

## Protecting your name (and your co-authors')

Once a paper is public it is permanent and collective. The habits that protect
everyone on the author list: never claim more than the data support; trace every
number; at conferences stake only what you can defend; every co-author signs off
before submission (send drafts to one reviewer at a time); disclose honestly
(funding, conflicts, data/image permissions, [AI use]({{ '/lab-guide/using-ai/' | relative_url }}), ethics approvals); and give
review the time it needs.

## Before you send a draft (checklist)

<aside class="marginnote" markdown="1">
**The comments Christina leaves most often:** Where are the stats? Percent relative
to what? What in the data shows this? Is this significant, or within your error
bars? Are you using this term the way the field does?
</aside>

<aside class="marginnote" markdown="1">
**Major vs. minor.** Not every item matters equally. Issues that affect whether
your *argument holds* are major; style and consistency are real but fixable. Don't
polish commas while an overclaim sits in your abstract.
</aside>

Run this yourself first. Most revision requests come straight off this list, so
clearing it yourself saves a full review cycle.

- Main takeaway in one sentence, and the same one in the abstract, results, and conclusion.
- Introduction makes the question and stakes clear within two paragraphs.
- Every paragraph has one job; its first sentence says what.
- Claims proportional to evidence; observation, inference, and uncertainty are distinguishable.
- Each "bio-inspired" claim reports source organism, level of mimicry, and strength of evidence.
- Results quantified: $$n$$, test, statistic, exact $$p$$, error-bar meaning.
- Conclusion lands the existing argument and adds no new idea.
- Figures stand on their own and are each referenced; run the [figure checklist]({{ '/lab-guide/figures/' | relative_url }}).
- Load-bearing terms defined or cut; empty intensifiers removed; every "this" has a noun.
- Units, spelling, hyphenation, and notation consistent; every number internally consistent.
- An annotated script traces every number to its source.
- Venue requirements and all disclosures met.
- ≥2 labmate pre-reviews done via **#phone-a-friend** on the lab Slack; Christina has the draft ≥2 weeks before the deadline; all co-authors approved.
{: .checklist}

## Authorship

Settle authorship early, and write it down. Who earns authorship, how order is
decided, and how we agree it up front all live on the
[Authorship policy]({{ '/lab-guide/authorship-policy/' | relative_url }}) page.

## Step-by-step: publishing a journal paper

<aside class="marginnote" markdown="1">
Heard back from the journal? [Paper revisions]({{ '/lab-guide/paper-revisions/' | relative_url }})
covers responding to reviewers and what to do once the paper is published.
</aside>

1. Select the target journal (look at where the papers you cite were published).
2. Create the figures and draft their captions *before* writing.
3. Run figures + captions by all co-authors.
4. Review the journal's "Information for Authors" page.
5. Outline by drafting a topic sentence per major paragraph.
6. Write the main-text draft; complete the checklist above.
7. Post the draft in **#phone-a-friend** on the lab Slack and collect ≥2 labmate pre-reviews; revise before it goes any further.
8. Choose a declarative, short title.
9. Write the abstract ([Nature summary-paragraph style](https://www.nature.com/documents/nature-summary-paragraph.pdf)).
10. Send the full draft to reviewers one at a time (repeat 2 to 3 times).
11. Send the updated draft to the last author.
12. Upload supporting data/code to [FigShare](https://figshare.com); reserve a DOI for the collection (don't publish yet).
13. Draft the cover letter; send to the last author for approval.
14. Re-read everything calmly.
15. Submit (do this with Christina the first time).
