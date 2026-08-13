---
title: Data analysis
category: Research Workflow
order: 6
summary: "The statistical methods we use, what is required of every analysis, and where to learn each one."
description: "How the lab chooses, fits, checks and reports statistical models, with the required standards separated from the optional improvements."
keywords: [analysis, statistics, R, model, lmer, mixed model, AIC, effect size, p-value, replicate, pseudoreplication, phylogenetic, emmeans, DHARMa, Schluter, PCA, principal component, DMD, dynamic mode decomposition, Procrustes, geomorph, PyDMD]
icon: "📈"
reviewed: 2026-08-12
math: true
---

<div class="guide-glance">
<div><span class="k">Jump to</span><a href="#the-five-stages">The five stages</a> · <a href="#requirements">Requirements</a> · <a href="#choosing-a-model">Choosing a model</a> · <a href="#what-to-report">What to report</a> · <a href="#decomposition">PCA &amp; DMD</a> · <a href="#sharpening-the-analysis">Sharpening</a> · <a href="#where-to-learn-each-method">Where to learn it</a></div>
</div>

Once your experiment finishes or your code converges, now comes the analysis! 

This shouldn't be the first time you're thinking about this though as good experimental design involves a consideration of the analysis goals right from the outset.

This page is about how to choose a model, fit it, check it, and report what it
supports (and what it doesn't). How well you know any single number is covered in
[Error and uncertainty analysis]({{ '/lab-guide/uncertainty-analysis/' | relative_url }}).

<aside class="marginnote" markdown="1">
**Two different jobs.**

*Uncertainty* answers "how well do I know this value?"

*Statistics* answers "is this pattern across values distinguishable from noise?"

You need both, and neither substitutes for the other.
</aside>

<aside class="marginnote" markdown="1">
**Christina learned her statistics from Dolph Schluter's
[R tips pages](https://www.zoology.ubc.ca/~schluter/R/index.html).** This page is the best starting
point. Get comfortable analysing data in R.
</aside>

## The five stages {#the-five-stages}

1. **Clean.** Remove blanks, false triggers and artifacts. This process must be documented and procedural.
   Never edit raw data; save cleaned data separately (see the source-file rule in
   [Data management]({{ '/lab-guide/data-management/' | relative_url }})).
2. **Explore.** Make many ugly, unstyled x–y plots. One to two weeks. Work through the eight checks
   below.
3. **Model.** The rest of this page.
4. **Quantify uncertainty.** [Error and uncertainty analysis]({{ '/lab-guide/uncertainty-analysis/' | relative_url }}).
5. **Plot.** [Figures]({{ '/lab-guide/figures/' | relative_url }}).

<div class="callout callout--warn" markdown="1">
**Stage 2 is not stage 3.** Exploring is how you find out what the data look like. Fitting is how you
test what you claimed before you looked. Choosing your model *after* the exploratory plots is
[p-hacking](https://pmc.ncbi.nlm.nih.gov/articles/PMC4359000/), even when it does not feel like it.
</div>

### What to check before you fit

<aside class="marginnote" markdown="1">
Every one of these is a **plot**, not a test. Look at the data. A normality test on 40,000
autocorrelated samples will reject regardless, and tells you nothing a Q–Q plot would not have shown
you in a second.
</aside>

The eight checks below are the data-exploration protocol from
[Zuur, Ieno & Elphick (2010)](https://doi.org/10.1111/j.2041-210X.2009.00001.x).
Run them in order, on every dataset, before you fit anything.

<figure class="protocol-fig">
<div class="protocol">
  <div class="protocol__stage">
    <div class="protocol__num" aria-hidden="true">1</div>
    <div class="protocol__body">
      <p class="protocol__title">Formulate the hypothesis · run the experiment · collect the data</p>
    </div>
  </div>
  <div class="protocol__stage protocol__stage--main">
    <div class="protocol__num" aria-hidden="true">2</div>
    <div class="protocol__body">
      <p class="protocol__title">Data exploration</p>
      <ol class="protocol__steps">
        <li><span class="what"><b>Outliers</b> in Y and X</span><span class="tool">boxplot · Cleveland dotplot</span></li>
        <li><span class="what"><b>Homogeneity</b> of Y</span><span class="tool">conditional boxplot</span></li>
        <li><span class="what"><b>Normality</b> of Y</span><span class="tool">histogram · Q–Q plot</span></li>
        <li><span class="what"><b>Zero trouble</b> in Y</span><span class="tool">frequency plot · corrgram</span></li>
        <li><span class="what"><b>Collinearity</b> in X</span><span class="tool">VIF · scatterplots · PCA</span></li>
        <li><span class="what"><b>Relationships</b> between Y and X</span><span class="tool">multi-panel scatterplots</span></li>
        <li><span class="what"><b>Interactions</b></span><span class="tool">coplots · conditional boxplots</span></li>
        <li><span class="what"><b>Independence</b> of Y</span><span class="tool">ACF · variogram · Y against time or space</span></li>
      </ol>
    </div>
  </div>
  <div class="protocol__stage">
    <div class="protocol__num" aria-hidden="true">3</div>
    <div class="protocol__body">
      <p class="protocol__title">Apply the statistical model</p>
    </div>
  </div>
</div>
<figcaption>The data exploration protocol, after
<a href="https://doi.org/10.1111/j.2041-210X.2009.00001.x">Zuur, Ieno &amp; Elphick (2010)</a>, fig. 1.
Step 8 is the one that decides your random-effect structure below.</figcaption>
</figure>

<div class="callout" markdown="1">
**Two of these do double duty on this page.** Check 8, independence, is how you discover the
non-independence that [requirement 3](#requirements) makes you model. Check 5, collinearity, is a
common reason to reach for [PCA](#principal-component-analysis) rather than throwing every correlated
predictor into one fit.
</div>

## The requirements {#requirements}

<div class="callout callout--stop" markdown="1">
**Every analysis in this lab meets all seven. They are not negotiable and they are not ranked.**

1. The model is written down before the data are collected.
2. The replicate unit is stated in words.
3. Non-independence is in the model, not in a footnote.
4. Residuals are checked, and the check is in the repository.
5. The estimate and its interval are reported, not only the verdict.
6. The report contains enough to refit the model.
7. Uncertainty and inference are reported separately.
</div>

### 1 · Write the model down first

Before the first run, put a plain-text analysis plan in the project repository: response variable,
predictors, random effects, and what result would count as support for each
[hypothesis]({{ '/lab-guide/research-hypotheses/' | relative_url }}). One paragraph is enough.

This is the cheapest protection that exists against fitting until something is significant (i.e., [p-hacking](https://pmc.ncbi.nlm.nih.gov/articles/PMC4359000/)). 
[Makin & Orban de Xivry's (2019)](https://doi.org/10.7554/eLife.48175) lists ten of the most common
statistical mistakes, which is the shortest useful thing anyone in the lab can read on this.

### 2 · State the replicate unit

Write the sentence out: *"n = 1 hawk, 5 trials per condition, ~4000 samples per trial; inference is
about this individual."* Then check that the model's degrees of freedom agree with it.

<aside class="marginnote marginnote--stop" markdown="1">
**More rows is not more evidence.** Ten thousand frames from one bird are ten thousand measurements
of one bird. Treating them as independent inflates $$\nu$$, shrinks the interval, and produces a
$$p$$-value describing an experiment nobody ran.
</aside>

Counting correlated measurements as independent replicates is **pseudoreplication**
([Hurlbert 1984](https://doi.org/10.2307/1942661); [Lazic 2010](https://doi.org/10.1186/1471-2202-11-5)).
It remains the most common serious error in animal biomechanics, and a
[2025 review of two decades of animal studies](https://doi.org/10.1186/s13229-025-00663-3) found it
present in the majority of papers and *increasing over time*, despite statistical reporting improving
across the same period. Better reporting does not fix this one. Naming the unit does.

### 3 · Put the non-independence in the model

Once the replicate unit is named, the structure follows. Repeated trials on one animal get a random
intercept for trial. Repeated configurations of one wing specimen get a random intercept for the
specimen. Species share ancestry, so cross-species comparisons carry the phylogeny.

<aside class="marginnote" markdown="1">
Our own analyses have used `(1 | trial_id)` for repeated perching trials
([Martínez-Carmena et al. 2026](https://doi.org/10.1098/rsif.2025.1082)), `(1 | WingID)` for repeated
morphed configurations of the same specimen
([Harvey et al. 2021](https://doi.org/10.1098/rsif.2021.0132)), and a phylogenetic GLMM across 22
species ([Harvey et al. 2022](https://doi.org/10.1038/s41586-022-04477-8)).
</aside>

[Harrison et al. (2018)](https://doi.org/10.7717/peerj.4794) is the lab's default reference for how to
specify these models, and [Bolker's GLMM FAQ](https://bbolker.github.io/mixedmodels-misc/glmmFAQ.html)
is where to go when one misbehaves.

### 4 · Check the residuals, and commit the check

Run the diagnostic, look at it, and leave the code in the repository so the next person can rerun it.
Use [`DHARMa`](https://cran.r-project.org/web/packages/DHARMa/vignettes/DHARMa.html), which simulates
scaled residuals for mixed models and tests dispersion and residual temporal, spatial and phylogenetic
autocorrelation. A quantile–quantile plot you looked at once and did not save is not a check.

### 5 · Report the estimate, not only the verdict

A $$p$$-value alone says whether an effect is distinguishable from zero. It does not say how large it
is, and that is usually the actual question. Report the estimate with a 95% interval alongside every
test, and an effect size where one is meaningful.

<div class="callout" markdown="1">
This is the settled position across the field, not a stylistic preference:
[Wasserstein, Schirm & Lazar (2019)](https://doi.org/10.1080/00031305.2019.1583913) for the American
Statistical Association, and [Amrhein, Greenland & McShane (2019)](https://doi.org/10.1038/d41586-019-00857-9)
in *Nature*, co-signed by over 800 researchers. Both argue for leading with magnitude and precision.

We keep $$\alpha = 0.05$$ and two-sided tests as a convention for deciding what to *discuss*. We do not
let it decide what to *report*.
</div>

### 6 · Report enough to refit

Model formula including the random terms, package and version, the degrees-of-freedom method, exact
$$F$$ and $$p$$ (not "$$p < 0.05$$"), and the seed for anything resampled. See
[What to report](#what-to-report).

### 7 · Keep uncertainty separate

Measurement uncertainty belongs in the error bars and the text, following
[Error and uncertainty analysis]({{ '/lab-guide/uncertainty-analysis/' | relative_url }}). Model
uncertainty belongs in the confidence intervals. Do not let one stand in for the other. Where they
genuinely have to combine, see [Sharpening](#sharpening-the-analysis).

## Choosing a model {#choosing-a-model}

Find the row that describes your data. Start there; justify anything more complicated.

| Your data | Start with | Where it is explained |
|---|---|---|
| One value per condition, conditions independent | `lm()` | Schluter, *Fit model* → **Simple linear regression** |
| Repeated measurements on the same bird, specimen or model | `lmer(y ~ x + (1 \| ID))` | Schluter, *Fit model* → **Mixed models**; [Coding Club](https://ourcodingclub.github.io/tutorials/mixed-models/) |
| Several individuals, generalising to the species | `lmer()`, individual as random intercept | [Harrison et al. 2018](https://doi.org/10.7717/peerj.4794) |
| Multiple species | `gls(..., correlation = corPagel())`, or PGLMM in `MCMCglmm` | Schluter, *Phylogenetic comparison*; [Hadfield's course notes](https://cran.r-project.org/web/packages/MCMCglmm/vignettes/CourseNotes.pdf) |
| Counts, proportions, binary outcomes | `glmer()` or `glmmTMB()` | [Bolker's GLMM FAQ](https://bbolker.github.io/mixedmodels-misc/glmmFAQ.html) |
| Two candidate functional forms (e.g. linear vs quadratic) | Fit both, compare AIC — see warning below | [Harrison et al. 2018](https://doi.org/10.7717/peerj.4794), §multi-model inference |
| Real uncertainty on **both** axes | Major-axis or standardised major-axis regression (`smatr`) | Schluter, *Fit model* → **Correct for body size** |
| A deterministic sweep with no sampling noise | No test. Run a sensitivity study instead | [Harvey 2024](https://doi.org/10.1098/rsif.2023.0734) |
| Many correlated shape or morphology variables, no single response | [Principal component analysis](#principal-component-analysis) | Schluter, *Multivariate methods* |
| A time series of coordinates with rhythmic structure | [Dynamic mode decomposition](#dynamic-mode-decomposition) | [BirdDMD](https://lydiafrance.github.io/BirdDMD/) |

<aside class="marginnote marginnote--warn" markdown="1">
**AIC on REML fits is wrong when the fixed effects differ.** `lmer()` defaults to `REML = TRUE`, and
`AIC()` will happily return a REML-based value. Models with different fixed effects do not have
comparable REML likelihoods. Refit the candidate set with `REML = FALSE` to compare, then refit the
winner with REML for the estimates. This one is silent: nothing warns you.
</aside>

<div class="callout" markdown="1">
**Keep the candidate set small and justified.** Every model in the set should correspond to a
hypothesis you can state. Enumerating fifty polynomial combinations and taking the lowest AIC is a
search, not an inference, and it will find structure in noise.

When the set is a genuine comparison, report **Akaike weights** as well as $$\Delta$$AIC: they say how
much better, not just which.
</div>

## What to report {#what-to-report}

Every fitted model in a paper, thesis chapter or committee meeting reports all of
these. For how to word the result once you have the numbers, see
[Writing papers]({{ '/lab-guide/writing-papers/' | relative_url }}#core-principles).

| Item | Example |
|---|---|
| Full model formula, random terms included | `avg_lift ~ state + perch_height + (1 \| trial_id)` |
| Replicate structure in words | "1 individual, 5 trials per condition" |
| Software and package versions | R 4.4.1; `lmerTest` 3.1-3 |
| Estimation and df method | REML, Kenward–Roger |
| Test statistic with **both** degrees of freedom | $$F_{1,17.06} = 42.43$$ |
| Exact $$p$$ | $$p = 0.002$$, or "$$p < 0.001$$" only below that |
| Estimate with a 95% interval | $$-0.14$$ [$$-0.21$$, $$-0.07$$] |
| Effect size, where meaningful | partial $$\eta^2 = 0.51$$ |
| Model fit | marginal and conditional $$R^2$$ |
| Seed, for anything resampled | `set.seed(42)` |
{: .table-budget}

<aside class="marginnote" markdown="1">
**Marginal vs conditional $$R^2$$.** Marginal is the variance explained by the fixed effects alone;
conditional includes the random effects
([Nakagawa & Schielzeth 2013](https://doi.org/10.1111/j.2041-210x.2012.00261.x)). Report both, or the
reader cannot tell whether your predictors did the work or the grouping did. `performance::r2()`
returns both.
</aside>

<details class="guide-details" markdown="1">
<summary>Worked example: repeated measures on one animal</summary>

One bird, two feather conditions, three perch heights, several trials per combination. The design
behind [Martínez-Carmena et al. (2026)](https://doi.org/10.1098/rsif.2025.1082), written out as a
template you can adapt.

```r
library(lmerTest)     # lmer with Kenward-Roger tests
library(DHARMa)       # residual diagnostics
library(performance)  # marginal / conditional R2
library(emmeans)      # marginal means

# 1. Fit. Fixed effects are the two designed factors;
#    the random intercept carries the repeated measures.
model_A <- lmer(avg_lift ~ factor_state + factor_perch + (1 | trial_id), data = data)

# 2. Check before you read anything off it.
res <- simulateResiduals(model_A)
plot(res)

# 3. Test. Kenward-Roger, because the sample is small.
anova(model_A, ddf = "Kenward-Roger")

# 4. Fit quality, both flavours.
r2(model_A)

# 5. Magnitudes and direction, on the response scale.
emmeans(model_A, ~ factor_state)

# 6. Intervals on the fixed effects.
confint(model_A, method = "profile")
```

Steps 4–6 are what turn a verdict into a result. They are the reason this analysis satisfies
requirement 5 without any extra work.

**Why Kenward–Roger.** [Luke (2017)](https://doi.org/10.3758/s13428-016-0809-y) showed that REML with
$$F$$-tests using Kenward–Roger or Satterthwaite degrees of freedom gives the most accurate inference
for fixed effects in linear mixed models. `lmerTest` defaults to Satterthwaite; Kenward–Roger is the
more conservative choice at small $$n$$ and is what we use.
</details>

## Decomposition: finding structure in many variables {#decomposition}

Sometimes there is no single response variable. A wing outline is fifty correlated coordinates; a
motion-capture trial is twenty-four coordinates evolving in time. Decomposition methods turn that into
a handful of axes or modes you can plot, interpret, and put into the models above.

<div class="callout" markdown="1">
**The two we use, and how to tell them apart.**

**PCA** finds the directions of greatest variance. It has no concept of time: shuffle the rows and you
get the same answer.

**DMD** finds modes that each carry one frequency and one growth rate. Shuffle the rows and it is
meaningless.

If your question contains *"how much does shape vary, and along what axes"*, you want PCA. If it
contains *"how fast"*, *"in what order"*, or *"what would the next wingbeat look like"*, PCA cannot
answer it and DMD can.
</div>

### Principal component analysis {#principal-component-analysis}

<aside class="marginnote" markdown="1">
**For the engineers.** PCA is the singular value decomposition of the mean-centred data matrix. The
components are the right singular vectors, and each component's variance is its squared singular value
divided by $$n-1$$. It is the same computation as **proper orthogonal decomposition** in fluids, under
a different name and a different normalisation convention.
</aside>

Schluter's [Multivariate methods](https://www.zoology.ubc.ca/~schluter/R/Multivariate.html) page has
the mechanics: `prcomp()`, scaling, scree plots, biplots, loadings and scores. Read that first. What
follows is the part specific to how we use it.

**1 · Get the variables onto a common scale before you start.** `prcomp()` defaults to the covariance
matrix (`scale. = FALSE`), which is right when everything shares units and has a comparable variance:
usually after log-transforming a set of lengths. Mixing linear, area and mass measurements without
correcting first will let whichever variable happens to have the largest numbers dominate PC1. Use
`scale. = TRUE` (the correlation matrix) when the units genuinely differ. Schluter's *Preparing
variables* section gives the rule, including dividing logged areas by 2 and volumes by 3.

**2 · If the variables are landmark coordinates, superimpose first.** Raw digitised coordinates carry
position, orientation and size, which will otherwise appear as the first few components. A generalised
Procrustes superimposition removes all three and leaves shape. Use
[`geomorph::gpagen()`](https://doi.org/10.1111/2041-210X.12035); it also handles sliding
semi-landmarks along curves, which is what you want for a wing outline or a trailing edge.

**3 · Decide how many components to keep, and decide it by a stated rule.** Cumulative variance
threshold, a break in the scree plot, whatever you like — but write the rule down before you look at
the plot, and report it.

**4 · Interpret by drawing, not by reading coefficients.** Reconstruct and plot the shape at plus and
minus a few standard deviations along each retained axis. A loadings table tells you almost nothing
about what a wing is doing; two overlaid outlines tell you immediately.

<aside class="marginnote marginnote--warn" markdown="1">
**The sign of a component is arbitrary.** `prcomp()` can hand you PC1 or its negative depending on
trivia. "PC1 increased" means nothing on its own. Always say which shape the positive direction
corresponds to, and keep the convention fixed across every figure in the paper.
</aside>

<aside class="marginnote marginnote--stop" markdown="1">
**The axes belong to your sample, not to the animal.** Add a specimen and the axes rotate. So:

- Never compare PC scores between two separately-run analyses.
- Never treat a component as a biological or physical quantity. It is a direction that happened to
  explain variance in the specimens you measured.
</aside>

**5 · Using scores downstream is fine, with one caveat.** PC scores make good response or predictor
variables in the models above. But the model treats them as if they were measured, when they were
estimated — the uncertainty in the components themselves is not carried through. Say so in the methods.

<div class="callout callout--warn" markdown="1">
**A small percentage is not automatically a small effect.** In
[Gamble et al. (2020)](https://doi.org/10.1088/1748-3190/ab9b6f), PCA on 57 landmarks along a
compliant trailing edge gave PC1 = 99.7% of shape change (driven by Reynolds number) and PC2 = 0.3%
(driven by angle of attack). The second axis was 0.3% of the variance and still a real, interpretable,
significant effect. Percentage of variance ranks the axes. It does not rank their importance to your
question.
</div>

**Report:** how many variables and how many specimens went in, whether you used the covariance or
correlation matrix, whether landmarks were Procrustes-aligned, variance explained by each retained
component, the retention rule, and the sign convention.

### Dynamic mode decomposition {#dynamic-mode-decomposition}

DMD approximates a time series as a sum of modes, each with its own spatial shape, frequency and
growth or decay rate:

$$\mathbf{x}(t) = \sum_{k=1}^{r} b_k\,\boldsymbol{\varphi}_k\, e^{\omega_k t}$$

<aside class="marginnote" markdown="1">
$$\boldsymbol{\varphi}_k$$ is the spatial mode: here, a wing–tail shape. $$\omega_k$$ is **complex**, so
one mode carries both a frequency, $$\mathrm{Im}(\omega_k)/2\pi$$ in Hz, and a growth or decay rate,
$$\mathrm{Re}(\omega_k)$$. $$b_k$$ is how much of that mode is present.
</aside>

That gives you something PCA cannot: a **generative** model. Because each mode carries a frequency,
you can run it forward, synthesise a wingbeat that was never recorded, or reconstruct a trial from a
chosen subset of modes and see what each one contributes.

**Where to start.** Our collaborator Lydia France has written
[**BirdDMD**](https://lydiafrance.github.io/BirdDMD/), which wraps
[PyDMD](https://mathlab.github.io/PyDMD/) with defaults chosen for biological motion-capture data. Work
through the [notebook gallery](https://lydiafrance.github.io/BirdDMD/notebooks/index.html) in order: it
starts from a synthetic sum of two sinusoids where you can check DMD recovers the frequencies you put
in, then moves to hawk flapping modes, turning manoeuvres, reconstruction error, and a generative
model. The underlying study is [France, Lapo & Kutz (2026)](https://arxiv.org/abs/2602.19196), which
decomposes flapping, turning, landing and gliding into a shared, low-order set of modes.

**The knobs, and why they matter.**

| Setting | What it does |
|---|---|
| `n_modes` (rank $$r$$) | How many modes to keep. Too few and you lose real dynamics; too many and you fit noise |
| `d` (time-delay embedding) | Stacks lagged copies of the data. Needed when you have fewer spatial channels than dynamics |
| `eig_constraints` | `conjugate_pairs` forces eigenvalues into complex-conjugate pairs, which keeps the reconstruction real-valued and the modes interpretable as oscillations |

<div class="callout callout--stop" markdown="1">
**Reconstruction error on the data you fitted proves nothing.** Enough modes will reproduce any
record. The number that means something is the error on a segment or a trial the fit never saw. Report
that one.
</div>

**Report:** number of modes, delay embedding, any eigenvalue constraints, the frequency and growth rate
of each retained mode, and held-out reconstruction error.

<div class="callout" markdown="1">
**What DMD is and is not.** It is a linear fit in a coordinate system chosen from the data. That is a
strength when physics-based models rest on assumptions that do not survive real flight, and it is the
limitation when you want a mechanism rather than a description. A DMD mode tells you the motion
contains a coherent oscillation at that frequency and shape. It does not tell you why.
</div>

## Sharpening the analysis {#sharpening-the-analysis}

Everything above is required. Everything below is worth reaching for, and none of it is a prerequisite
for a good paper. Pick what your question needs.

<aside class="marginnote" markdown="1">
Talk to Christina before adding any of these to a manuscript. Most cost a day; a couple cost a month.
</aside>

**Say what you could have detected.** With one or two animals, "power" is the wrong output. Simulate
from a pilot fit ([`simr`](https://cran.r-project.org/package=simr)) and report the *smallest effect
the design could resolve*. Do it before you collect, and the limitation becomes a stated scope rather
than a caveat. Schluter's *Planning tools* page covers the simpler `pwr` and `power.t.test` cases.

**Answer the comparative question directly.** [`emmeans`](https://cran.r-project.org/web/packages/emmeans/vignettes/basics.html)
and [`marginaleffects`](https://cran.r-project.org/package=marginaleffects) give contrasts on the
response scale with intervals, and handle multiplicity adjustment when you are making many
comparisons. Far more informative than a table of $$p$$-values.

**Declare which tests are exploratory.** When one study fits many models across many response
variables at $$\alpha = 0.05$$, some will clear the bar by chance. Either pre-specify a primary
response, adjust, or label the rest exploratory in the text. Any of the three is defensible; silence
is not.

**Plot the fit, not just the data.** [`visreg`](https://pbreheny.github.io/visreg/) shows partial
residuals against one predictor with the others accounted for, so a multi-predictor fit becomes
something you can actually look at. It works with `lmer` fits.

**Push measurement error through to the conclusion.** *This is the one place the two pages meet.*
Resample each point within its uncertainty range, refit, and check the conclusion still holds.
[Harvey et al. (2022)](https://doi.org/10.1038/s41586-022-04477-8) did this with 5,000 bootstrap draws
over the centre-of-gravity error range, refitting the evolutionary model each time. Schluter's
*Resample, bootstrap* page has the mechanics, including `boot` and BCa intervals.

**Show you had the power to choose the model.** Selecting by AIC assumes the candidates are
distinguishable at your sample size. Simulating under each and comparing likelihood-ratio distributions
demonstrates it. [Harvey et al. (2022)](https://doi.org/10.1038/s41586-022-04477-8) used `pmc` this way
for the Ornstein–Uhlenbeck versus Brownian motion choice.

**Consider a Bayesian fit when $$n$$ is tiny.** At two or three replicates an $$F$$-test is working
with almost no degrees of freedom. A weakly informative prior gives a better-behaved interval.
`brms` ([Coding Club tutorial](https://ourcodingclub.github.io/tutorials/brms/)) or `MCMCglmm`. Optional,
and never a way to rescue an analysis that failed frequentist assumptions.

## Where to learn each method {#where-to-learn-each-method}

Start with Dolph. The rest fill specific gaps he does not cover.

**Dolph Schluter's [R tips pages](https://www.zoology.ubc.ca/~schluter/R/index.html)** — the lab's
default reference. Written for biologists, worked examples throughout.

| If you need | Go to |
|---|---|
| Linear models, ANOVA, mixed models, ML vs REML, singular fits | [Fit model](https://www.zoology.ubc.ca/~schluter/R/Model.html) → *Read me*, then *Mixed models* |
| Marginal means, post-hoc tests, visualising fits | [Fit model](https://www.zoology.ubc.ca/~schluter/R/Model.html) → *Estimate magnitudes of effect* |
| Body-size correction, errors in x, MA and SMA regression | [Fit model](https://www.zoology.ubc.ca/~schluter/R/Model.html) → *Correct for body size* |
| Simulating a design; power and sample size | [Planning tools](https://www.zoology.ubc.ca/~schluter/R/Plan.html) |
| Bootstrap standard errors, BCa intervals, permutation tests | [Resample, bootstrap](https://www.zoology.ubc.ca/~schluter/R/Resample.html) |
| Independent contrasts, phylogenetic GLS, Pagel's $$\lambda$$, OU | [Phylogenetic comparison](https://www.zoology.ubc.ca/~schluter/R/Phylogenetic.html) |
| PCA, discriminant analysis, multidimensional scaling | [Multivariate methods](https://www.zoology.ubc.ca/~schluter/R/Multivariate.html) |
| Worked R for every example in *The Analysis of Biological Data* | [Whitlock & Schluter examples](https://whitlockschluter3e.zoology.ubc.ca/RExamples/) |

**Filling the gaps.**

- **Mixed models, from scratch.** [Coding Club: Introduction to linear mixed models](https://ourcodingclub.github.io/tutorials/mixed-models/)
  (Hajduk & Gallois). The gentlest on-ramp; do this before Harrison et al.
- **Mixed models, as a standard.** [Harrison et al. (2018), *PeerJ*](https://doi.org/10.7717/peerj.4794).
  A code of best practice for random-effect structure and multi-model inference. Read once properly,
  then keep for reference.
- **When a model misbehaves.** [Bolker's GLMM FAQ](https://bbolker.github.io/mixedmodels-misc/glmmFAQ.html).
  Convergence warnings, singular fits, which degrees of freedom, whether to use a GLMM at all.
- **Bayesian and phylogenetic mixed models.** [Coding Club: MCMCglmm](https://ourcodingclub.github.io/tutorials/mcmcglmm/)
  for priors, chain convergence and building measurement error into a model, then
  [Hadfield's course notes](https://cran.r-project.org/web/packages/MCMCglmm/vignettes/CourseNotes.pdf)
  for the statistics underneath.
- **Phylogenetic comparative methods.** Revell & Harmon (2022), *Phylogenetic Comparative Methods in R*,
  and [`phytools` 2.0](https://doi.org/10.7717/peerj.16505). Where to go past Schluter's page.
- **Exploring data before modelling.** [Zuur, Ieno & Elphick (2010)](https://doi.org/10.1111/j.2041-210X.2009.00001.x).
- **PCA in depth.** [Jolliffe & Cadima (2016)](https://doi.org/10.1098/rsta.2015.0202), the standard
  review: what PCA does, what the choices are, and where it breaks.
- **Landmark shape data.** [`geomorph`](https://doi.org/10.1111/2041-210X.12035) (Adams &
  Otárola-Castillo 2013) for Procrustes superimposition and shape PCA.
- **DMD, start here.** [BirdDMD](https://lydiafrance.github.io/BirdDMD/) (France) — motion-capture
  defaults and a notebook gallery. Then [France, Lapo & Kutz (2026)](https://arxiv.org/abs/2602.19196)
  for the hawk study behind it.
- **DMD, the theory.** [Schmid (2010)](https://doi.org/10.1017/S0022112010001217), the original ·
  [Kutz, Brunton, Brunton & Proctor (2016)](https://doi.org/10.1137/1.9781611974508), the book ·
  [Brunton & Kutz (2022)](https://doi.org/10.1017/9781009089517), *Data-Driven Science and
  Engineering*, which puts SVD, PCA/POD and DMD in one place and is the best single source if you want
  to see how they connect · [PyDMD](https://doi.org/10.21105/joss.00530).
- **What goes wrong.** [Makin & Orban de Xivry (2019), *eLife*](https://doi.org/10.7554/eLife.48175).
  Ten mistakes, each in a page. Read before your first submission and again before every review you write.
- **Why we report intervals.** [Wasserstein, Schirm & Lazar (2019)](https://doi.org/10.1080/00031305.2019.1583913) ·
  [Amrhein, Greenland & McShane (2019)](https://doi.org/10.1038/d41586-019-00857-9).
- **Package documentation.** [`DHARMa`](https://cran.r-project.org/web/packages/DHARMa/vignettes/DHARMa.html) ·
  [`emmeans`](https://cran.r-project.org/web/packages/emmeans/vignettes/basics.html) ·
  [`performance::r2()`](https://easystats.github.io/performance/reference/r2_nakagawa.html) ·
  [`marginaleffects`](https://cran.r-project.org/package=marginaleffects)

## Before you write it up

- Analysis plan was written before data collection, and is in the repository
- Replicate unit stated in words, and the model's degrees of freedom agree with it
- Non-independence is in the model
- Residual diagnostic run, and the code committed
- Candidate model set is small, and each model answers a stated question
- Any AIC comparison of differing fixed effects used `REML = FALSE`
- Estimate and 95% interval reported alongside every test
- Effect size and both $$R^2$$ values reported
- Exact $$F$$, both degrees of freedom, and exact $$p$$
- Seed set and recorded for every resampling step
- Package versions recorded
- Any PCA states scaling, retention rule, variance per axis, and the sign convention
- Any DMD reports rank, delay embedding, and error on data it did not fit
- Measurement uncertainty reported separately, per [Error and uncertainty analysis]({{ '/lab-guide/uncertainty-analysis/' | relative_url }})
{: .checklist}
