---
title: Research hypotheses
category: Research Workflow
order: 2
summary: How to write clear, testable hypotheses for your thesis or project.
keywords: [hypothesis, research question, prediction, testable, aims, hypotheses]
icon: "💡"
reviewed: 2026-07-05
---

A research hypothesis is a **concise, testable statement** about how a system
behaves or why a phenomenon occurs. It should propose an explanation, lead to specific, observable predictions; and be possible to accept
or reject with attainable data.

## What makes a good hypothesis

<aside class="marginnote" markdown="1">
Christina always spends a long time on developing a good hypothesis, as it's one of the hardest and most confusing parts. Once done right, the time will feel well spent!
</aside>

A strong hypothesis in the BIRD Lab is:

1. **Grounded in prior work.** Based on
   [literature]({{ '/lab-guide/literature-reviews/' | relative_url }}), theory, or
   existing data and models, so you can point to *why* the expectation is reasonable.
2. **Explicit about how expectation leads to predictions.** It states what you expect (a
   relationship, pattern, or mechanism), and that expectation implies measurable
   predictions.
3. **Testable and falsifiable.** Some conceivable data would count *against* it,
   and you can distinguish it from competing hypotheses.

## Common hypothesis forms

Use whichever best matches your question.

**Relationship-based.** *If X changes, Y will change in [direction], because [reason].*
Example: "If gust intensity increases, peak roll rate during recovery will
increase because larger corrective torques are required."

**Pattern-based.** *[Behavior or field] will show [specific pattern] under [conditions], consistent with [reason].*
Example: "In formation flight, follower positions will cluster near the leader's
upwash region."

**Mechanism-based.** *[Phenomenon] occurs because [mechanism], leading to [observable consequence].*
Example: "Rapid yaw turns are generated primarily by asymmetric wingbeat
kinematics, leading to characteristic asymmetries in wingtip paths."

## What is not a hypothesis

Some statements sound research-y but are not hypotheses:

- **Goals**, not expectations: "We want to understand how birds steer in clutter."
- **Methods**, not predictions: "We will use high-speed cameras to record wing motion."
- **Descriptive plans**: "We will measure wingbeat frequency at different speeds."
  A hypothesis must add an expectation about how the measurements will differ.
- **Vague or unfalsifiable claims**: "Birds use complex strategies to fly
  efficiently." Nothing would clearly show it wrong.
- **Bare predictions with no context**: "Wingbeat frequency will increase."
  A hypothesis needs conditions and reasoning.
- **Tautologies**: "Higher lift allows the bird to stay aloft." A definition, not
  an explanation.
- **Design wishes**: "Our controller should be robust across all conditions."
  A goal, not a testable claim.

<aside class="marginnote" markdown="1">
**When in doubt, ask:** does this make a specific, testable claim about how the
system behaves under identifiable conditions, in a way that could turn out to be
wrong? If not, it's probably not a hypothesis yet.
</aside>

## From question to hypotheses

1. **Define the phenomenon.** What exactly are you trying to explain or predict?
2. **Summarize what's known.** A short paragraph or bullet list from the
   literature and prior data.
3. **List plausible explanations.** Morphology, aerodynamics, control, sensing,
   environment, task demands.
4. **Write competing hypotheses.** H₀ (null), then H₁, H₂ as alternative
   mechanisms or relationships.
5. **Derive discriminating predictions.** For each, "if this is true, we should
   see ___," focusing on predictions that *differ* across hypotheses.
6. **Check feasibility.** Can you measure what you need with available tools and time? Plan how you'll test each prediction; see [Data analysis]({{ '/lab-guide/data-analysis/' | relative_url }}).

## Hypothesis checklist

Before you commit a hypothesis to your thesis or proposal:

- Grounded in literature, data, or theory
- States a clear expectation (relationship, pattern, or mechanism)
- Implies specific, measurable predictions
- Is falsifiable (you can say what would contradict it)
- Has at least one competing hypothesis, plus a null
- Your planned experiment or analysis can distinguish between hypotheses
- Wording is precise, neutral, and concise
- You can state the core hypothesis in one or two presentation-ready sentences
{: .checklist}

## Worked example: what predicts flight behavior?

A competing-hypotheses example based on
[Altshuler et al. (2025)](https://doi.org/10.1242/jeb.247992).

**Question:** which traits best predict variation in flight behavior across bird
species? Framed as competing hypotheses:

- **H₀ (null):** flight behavior is not meaningfully associated with the measured
  traits; classification accuracy is similar to shuffled data.
- **H₁ (wing shape):** static wing shape is the main predictor, and shape-based
  models classify behavior better than chance.
- **H₂ (range of motion):** wing range of motion is the main predictor, and
  ROM-based models outperform shape- and mass-based models.
- **H₃ (body mass):** body mass is the main predictor, and mass-based models show
  the highest accuracy.

Each hypothesis implies different predictions about classification accuracy, how
each trait compares against a shuffled null, and relative importance. If ROM-based
models beat shape- and mass-based models and their shuffled controls, that
supports H₂ over H₁ and H₃.
