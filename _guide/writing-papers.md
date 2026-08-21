---
title: Writing papers
category: Writing & Dissemination
order: 2
summary: Core principles, the drafting cycle, and a pre-send checklist for manuscripts, preprints, and conference papers.
description: "How to write a paper whose argument stands on its own, and what has to be true before you circulate a draft."
keywords: [writing, manuscript, paper, draft, authorship, preprint, publishing]
icon: "✍️"
reviewed: 2026-08-13
math: true
---

<aside class="marginnote" markdown="1">
This is the writing-side companion to
[Figures]({{ '/lab-guide/figures/' | relative_url }}).
This page is continually evolving; please suggest new resources or tips.
</aside>

<div class="guide-glance">
<div><span class="k">Jump to</span><a href="#non-negotiables">The non-negotiables</a> · <a href="#the-drafting-cycle">The drafting cycle</a> · <a href="#core-principles">Core principles</a> · <a href="#before-you-send-a-draft-checklist">Pre-send checklist</a> · <a href="#tools">Tools</a> · <a href="#resources">Resources</a></div>
</div>

Strong scientific writing makes your reasoning visible, your data clear, and your science understandable.

The lab's [communication framework]({{ '/lab-guide/presentations/' | relative_url }}#core-principles)
applies to prose as much as to a talk or a figure. Every reader asks *so what?* and
*who cares?* Your job is to raise the signal and cut the noise.

<aside class="marginnote" markdown="1">
**Why "#phone-a-friend"?** It's the lab's private Slack channel where we post work-in-progress to request peer review. 
Routing drafts through peers helps catch errors early,  trains you to read critically, and creates a low-stakes setting to receive feedback. 
</aside>

<div class="callout callout--stop" markdown="1" id="non-negotiables">
**Lab policy: the non-negotiables**

- Christina must be sent the draft ≥2 weeks before any external deadline (drafts that arrive too late for co-author review may be deferred to a later submission window).
- No submission without explicit approval from Christina *and* all co-authors.
- ≥2 labmate pre-reviews before the draft reaches Christina (post in **#phone-a-friend** on the lab Slack; see [giving and receiving feedback]({{ '/lab-guide/communication/' | relative_url }}#giving-and-receiving-feedback)).
- Reference managers required (BibTeX / Zotero / EndNote); no manually typed references.
- Maintain an annotated script for where each number in the draft is sourced from in the data.
- Data and code are made public on publication, except where privacy, ethics, legal, proprietary, or collaborator constraints require otherwise; raise those constraints early.
- Disclose funding, conflicts, data and image permissions, [AI use]({{ '/lab-guide/using-ai/' | relative_url }}), and ethics approvals.

The rules protect the work and everyone whose name is on it. 
</div>

## Tools {#tools}

Draft in Overleaf or Word. Christina prefers Word, but either is fine.

Start the Overleaf project yourself. When you're ready for review, transfer
ownership to Christina. No need to purchase your own license.

Use a reference manager from the first citation: Zotero, BibTeX, EndNote, whichever
you prefer. Pick one and stay on it for the whole paper. See
[Literature reviews]({{ '/lab-guide/literature-reviews/' | relative_url }}#the-one-non-negotiable)
for how to set one up.

<div class="callout" markdown="1">
**Keep your journal draft unformatted.** Turn on line numbers in the left margin so reviewers
can point at a line. The journal typesets the accepted manuscript, so any styling you add gets thrown away.

Some conferences expect you to format the paper yourself. SciTech, for example,
publishes [LaTeX and Word templates](https://aiaa.org/events-learning/events/technical-presenter-resources/). Download the one you want and draft inside it from the start.
</div>

## The drafting cycle

0. **Figures and captions first.** Build every figure and draft its caption before you begin writing, then run them by all co-authors. See [Figures]({{ '/lab-guide/figures/' | relative_url }}).
1. **Outline:** one topic sentence per major paragraph, before any prose.
2. **Rough draft:** get the whole argument down; ugly is fine, gaps are fine.
3. **Refine structure:** fix what each paragraph is doing, and in what order.
4. **Refine sentences:** terminology, statistics, notation, citations.
5. **Review and revise:** ≥2 labmate pre-reviews in **#phone-a-friend**, then Christina.

Christina's own papers routinely reach ~version 20 before submission. 
That's normal and healthy, and it's her job to help you get there.

### How expectations ramp

Christina's feedback will track the cycle. Early on it will focus on structure and message; once the
sentences and paragraph structure is decided, it moves to terminology, statistics, and notation. Big-picture
comments early and details later. Don't be surprised if each round new comments are brought up.

Standards also scale with the venue: the more public and peer-reviewed, the more detail review is needed for every sentence.

## Core principles {#core-principles}

The principles apply to everything the lab publishes.

### 1 · Lead with the question

State the problem and its impact/consequences early. A strong introduction is well cited, but synthesized: each citation
builds the case for *your* question rather than showing how much you've read. Avoid listing author names and results without tying the story together.

### 2 · Major takeaways are consistent and visible everywhere

Your paper will have one or two core takeaways. The *same* takeaways must appear in the
abstract, introduction, results, discussion, conclusion, and figure captions. The
conclusion lands what you found and why it matters; it doesn't restate the
introduction or add anything new.

### 3 · Make prose do one job, in a logical order

At the document level, use the hourglass layout: broad reasoning → specific question, methods, results → broad implications. 

At the paragraph level: topic sentence → evidence → interpretation → mini-takeaway. 

At the sentence level: open on the idea you're discussing and end on the point you want carried forward.
Keep to one idea per sentence. Use plain signposts ("To test this, we…", "This result suggests…").

<div class="callout" markdown="1">
**Tip.** Once Christina is "in the weeds" of writing, she edits by reading out loud
and fixes any sentence she stumbles on or is too long for one breath. A stumble means it wasn't clear.

For more on topic and stress positions, read [Gopen & Swan, *The Science of Scientific Writing*](https://www.usenix.org/sites/default/files/gopen_and_swan_science_of_scientific_writing.pdf). [Nature Masterclasses](https://www.nature.com/masterclasses/writing-for-greater-impact/50732650) covers writing for greater impact.
</div>

### 4 · Keep claims proportional to evidence

Keep three things separate and visible: what the data directly show, what you infer, and what remains uncertain.
Watch empty intensifiers (*drastically, very, greatly*). 
Don't just delete the word; scope the claim to what you measured. *e.g.*
❌ "Our design dramatically improves flight efficiency." →
✅ "Our design reduced power consumption by 12% in level flight (wind tunnel,
*n* = 8 trials); we did not test maneuvering or gust conditions."

<div class="callout callout--warn" markdown="1">
This principle directly affects your (and our) scientific reputation. 
A reviewer who catches one overclaim starts doubting *everything*, and the doubt attaches to every name on the paper. 
Naming your results specifically and their limits is what makes your research have long term impact.
</div>

### 5 · Quantify your results, reported trends, and associated error

Always report sample size ($$n$$), the test, the test statistic, and the exact $$p$$-value. Be precise about which kind of uncertainty your error bars carry: biological variation, measurement noise, or numerical/model error. 
Add effect size, confidence intervals, randomization or blinding, replicate count, and inclusion/exclusion criteria where they apply.
Reproducibility is a writing requirement too: equipment, software versions, mesh and calibration details, environmental conditions. 

See [Data analysis]({{ '/lab-guide/data-analysis/' | relative_url }}#what-to-report) for
what every fitted model must report, [Error and uncertainty]({{ '/lab-guide/uncertainty-analysis/' | relative_url }})
for how we quantify it, and the [honest data checks]({{ '/lab-guide/figures/' | relative_url }}#figure-checklist)
for what the figure must show.

<div class="callout callout--warn" markdown="1">
**Lab requirement:** maintain an annotated script that traces every number in the
draft back to its source. That script is how we catch errors before reviewers do.
</div>

### 6 · Use words precisely

Load-bearing words must carry their exact meaning, consistently across sections: *significant* (only statistical, name
the test), *robust* (to what?), *converged* (what, to what value, under what
condition?), *improved* (vs. what, by how much, on what metric?). Cut *very,
obviously, extremely, actually*; prefer *use* over *utilize*; and the verb over the noun built from it 
(*we assessed*, not "we performed an assessment").

Every "this" needs a following noun. Define acronyms at first use, and don't introduce one the
reader will meet only once or twice; spell it out instead.

### 7 · Write engagingly and directly

Use active voice for what you did and what you found: "We found…", "We showed…", not "It was observed that…".
Passive voice is helpful in three spots: Methods, where the actor doesn't matter; correlations, where naming a cause would overclaim; and sentences that need to open on the idea the last one ended with.

Use past tense for what you did and found. Present tense for general facts and figure descriptions. 

### 8 · Cite figures, do not narrate

A reader looks at your figures first. How you write about them decides whether that look helps or confuses.
In the main text, lead with the finding and cite the figure in support, never the reverse:
❌ "Figure 1 shows the lift coefficient across sweep angles." →
✅ "Lift coefficient peaked near 20° of sweep and dropped sharply beyond it (Fig. 1)."
Don't narrate the plot. Say what the result means and how it changes what we knew.

See [Figures]({{ '/lab-guide/figures/' | relative_url }}) for figure design and captions.

### 9 · Write so everyone can follow you

Our work sits at the aerospace-biology interface, and your reader rarely lives in both fields.
Decide your primary audience, then write so the secondary field can still follow.
Give half a sentence of grounding the first time a term has implied or assumed meaning in one field but not the other.
Scope every claim to what you actually studied: one wingbeat, one individual, one species. Don't quietly generalize to "birds."

Choose the plain word over the impressive one. Complex ideas do not need complex vocabulary, and many of your readers work in English as a second language.

### 10 · Name the limitations and uncertainty before a reviewer does

Research always contains some limitations or assumptions. You need to state your work's directly so that readers can know when your results are relevant and when they are not.

### 11 · Label bio-inspiration by its evidence

*Bio-inspired*, *biomimetic*, and *bio-informed* hold implied meaning that varies across the fields. F
or clarity, always report the organism that is the source of inspiration, the level of design mimicry, and the strength of biological
evidence together. 
Reserve *biomimetic* for near-mimicry and *bio-informed* for designs built on a principle with at least single-species primary
evidence. 
See[Harvey (2026), *How bio-inspired is your design?*](https://doi.org/10.1038/s44172-026-00641-4)

## Journal article vs. conference paper

<aside class="marginnote" markdown="1">
**Why hold exciting results back at a conference?** A conference is a fast, lightly
reviewed checkpoint. It's the wrong venue for a major claim, and publishing early
can weaken the journal paper's novelty. Conference papers should be simple, well supported results that you would defend in
your sleep. Unknowns that benefit from conferring with the field should be presented as such in oral presentations.
</aside>

The core principles hold for both; what changes is strategy. Some conference venues do suit major results. Talk to Christina if it is unclear.

| Aspect | Journal article | Conference paper |
| --- | --- | --- |
| **Goal** | The complete, definitive account | A solid, citable checkpoint |
| **What to include** | Strongest, fully validated results | Boring-but-bulletproof results; hold exciting findings back |
| **Risk posture** | Claims fully defended; limits stated | Even more conservative |
| **Scope** | Broad enough to support the full argument | Narrow, self-contained, finishable |
| **Reuse** | Stands alone | Shouldn't "spend" results you need for the journal version |

**Null and negative results count.** A clean negative result, honestly
reported is valid for both conference and journal papers. Negative results matter just as much as the splashy ones.

## When you revise your own draft

Revision is where the writing actually happens. Read the whole draft top to bottom,
repeatedly; it's the only way to see whether the *argument* holds.

Then go paragraph by paragraph. What is the main point here, and did I say it*directly*? 
Did I explain why it matters and support it with evidence? 
Could an informed reader understand it on the first pass? 
Is this paragraph doing too much?

Apply the fix:

- Feels like a literature review: tighten it to only the most relevant sections.
- Feels like a string of facts: add synthesis and interpretation.
- Feels vague: make the claim more specific and quantified.
- Could be removed without changing the argument: remove it.

## Before you send a draft (checklist)

<aside class="marginnote" markdown="1">
**The comments Christina leaves most often:** Where are the stats? Percent relative
to what? What in the data shows this? Is this significant, or within your error
bars? Are you using this term the way the field does?
</aside>

<aside class="marginnote" markdown="1">
**Major vs. minor.** Not every item matters equally. Issues that affect whether
your *argument holds* are major; style and consistency are real but fixable. 
</aside>

Run this checklist yourself first. Most revision requests come straight off this list, so
clearing it yourself saves a full review cycle.

**Start here.** Figures stand on their own and are each cited by the claim they
support ("(Fig. 1)"), not narrated ("Figure 1 shows…"). Run the
[figure checklist]({{ '/lab-guide/figures/' | relative_url }}#figure-checklist)
before you go any further.

### Start with judgment calls

- If a reader stopped after my first two paragraphs, would they know what I'm studying and why it matters, and does every citation earn its place?
- Can I state my main point in one sentence, and does every section add support for that same point?
- What is each paragraph's one job, and does its opening sentence say so?
- Can a reader tell which statements are observations, which are inferences, and which are open questions?
- For each number I report, could a reader find where it came from and how it was tested?
- Have I used a strong-sounding word without saying exactly what I mean by it?
- Does this sentence engage directly with the science, or describe it from a distance?
- Could each figure be understood on its own, and does my text say what to look at?
- Could a reviewer from the field I am less trained in follow this, and would they feel respected?
- Where does my model or experiment stop representing real conditions, have I named that limit before a reviewer does, and have I said which kind of uncertainty my numbers carry?
- Have I named the source organism, the level of mimicry, and the strength of evidence behind every bio-inspired claim?
- When did I last read this draft all the way through, and what changed because I did?

### Tier 1 · The argument

- The main takeaway can be summarized in one to two sentences, and the same takeaway appears in the abstract, results, and conclusion. It does not drift between sections.
- The introduction makes the question and stakes clear within two paragraphs, without a jargon-heavy or review-style opening.
- All claims are proportional to the evidence; observation, inference, and uncertainty are distinguishable.
- All results are quantified: the sample size, *n*, the test, and the statistic (including the associated $$F$$-statistic where relevant) with the exact $$p$$. Error bars are named by statistic in the caption. For fitted models, also clear [Before you write it up]({{ '/lab-guide/data-analysis/' | relative_url }}#before-you-write-it-up).
- Every number is internally consistent and can be traced back to its source; see [Code]({{ '/lab-guide/code/' | relative_url }}).
- Each bio-inspired claim reports the source organism, the level of mimicry, and the strength of evidence.
- The limitations are described either in a specific section or in at least one to two paragraphs.
- The conclusion lands the existing argument and adds no new idea.
{: .checklist}

### Tier 2 · Structure and clarity

- Every paragraph has one job, its topic sentence captures that job, and it runs about four or five sentences.
- Every sentence can be read out loud in one breath.
- There are no repeated ideas that fail to advance the argument.
- Any use of the word *significant* is supported by statistics. Vague quantifiers (*some, few, many*) are replaced with numbers where you have them.
- Strong verbs are used in place of nominalizations (*we analyzed*, not *we performed an analysis of*).
- All empty intensifiers are removed.
- Every "this" has a following noun.
- Every term, especially a measurement term, means the same thing in every section.
{: .checklist}

### Tier 3 · Polish and consistency

- Verb tense matches the job of the sentence: past for what you did and found, present for established knowledge, for what the paper and figures show, and for what the results mean.
- Every equation is part of a sentence, properly punctuated, and referenced as needed. LaTeX formatting is used where appropriate, and every variable introduced in the text is in mathematical font (or italics).
- Units, spelling (US *or* UK, not a mix), hyphenation, and notation are consistent.
- Gender-neutral language is used throughout (e.g., uncrewed aerial vehicles).
{: .checklist}

### Before it leaves your hands

- All venue requirements (template, length, formatting) and disclosures are met. Ask Christina for the proper funding language.
- *Conference paper?* The headline result is one you would defend anywhere. It does not need to be life-changing.
- At least two labmate pre-reviews are done via **#phone-a-friend** on the lab Slack, Christina has the draft at least two weeks before the deadline, and all co-authors have approved.
{: .checklist}

## What happens next

Settle authorship early and write it down; see
[Authorship policy]({{ '/lab-guide/authorship-policy/' | relative_url }}).
Once the draft clears the checklist, the submission steps, reviewer responses, and
what to do on publication live in
[Submitting & publishing]({{ '/lab-guide/submitting-publishing/' | relative_url }}).

## Resources

- [Gopen & Swan, *The Science of Scientific Writing*](https://www.usenix.org/sites/default/files/gopen_and_swan_science_of_scientific_writing.pdf): topic and stress positions; still the best single read on sentence-level clarity.
- [Doumont, *Effective Writing*](https://www.nature.com/scitable/topicpage/effective-writing-13815989/): a compact reference on verb tense, subject–verb proximity, and word-level precision.
- [Nature Masterclasses, *Writing for greater impact*](https://www.nature.com/masterclasses/writing-for-greater-impact/50732650): active voice, strong verbs, conciseness, signposting.
- [Nature's summary-paragraph format](https://www.nature.com/documents/nature-summary-paragraph.pdf): the model we use for abstracts.
- [Harvey (2026), *How bio-inspired is your design?*](https://doi.org/10.1038/s44172-026-00641-4): how we label bio-inspiration claims.
- [Never on a Sunday](https://blogs.lse.ac.uk/impactofsocialsciences/2019/01/29/never-on-a-sunday-is-there-a-best-day-for-submitting-an-article-for-publication/): is there a best day to submit?


