---
title: Statistical analysis
category: Research Workflow
order: 6
summary: "What every analysis in the lab needs, how to choose and report a statistical model, and where to learn more."
description: "How the lab plans, fits, checks and reports statistical models: the fixed requirements first, the method choices second."
keywords: [analysis, data analysis, statistics, R, model, lmer, mixed model, AIC, effect size, p-value, replicate, pseudoreplication, degrees of freedom, phylogenetic, emmeans, DHARMa, Schluter, PCA, principal component, Procrustes, geomorph]
icon: "📈"
reviewed: 2026-10-29
math: true
---

<div class="guide-glance">
<div><span class="k">Jump to</span><a href="#requirements">Requirements</a> · <a href="#plan">Plan</a> · <a href="#explore">Explore</a> · <a href="#choosing-a-model">Choose</a> · <a href="#check">Check</a> · <a href="#what-to-report">Report</a> · <a href="#situation-dependent-checks">Situation-dependent checks</a></div>
</div>

Choose the simplest analysis that answers your scientific question. It usually doesn't need to be
complicated. Then:

- Justify the choices that affect the result.
- Quantify its uncertainty, and check it against independent evidence where you can.
- Explain what it means physically.

This page covers the statistics. How well you know each measured value is covered in
[Error and uncertainty analysis]({{ '/lab-guide/uncertainty-analysis/' | relative_url }}). Most
results need both, because neither stands in for the other:

- A tight confidence interval won't reveal a calibration offset shared by every point.
- Small error bars don't make a difference significant.

Methods in the field change quickly and every project is different, so treat the methods here as
starting points. If a newer method is more appropriate for your question, use it and share what you
learn. The requirements stay fixed.

<aside class="marginnote" markdown="1">
**Start with Dolph Schluter's [R tips pages](https://www.zoology.ubc.ca/~schluter/R/index.html).**
Christina learned her statistics from his pages, which explain most methods on this page with
worked examples for biologists.
</aside>

<aside class="marginnote" markdown="1">
**Listen to [Normal Curves](https://podcasts.apple.com/us/podcast/normal-curves-sexy-science-serious-statistics/id1796408698).**
Christina is a big fan. Statisticians Regina Nuzzo and Kristin Sainani take apart real studies and
end each episode with a methodological moral. Listen to build your intuition, and if an episode
changes how you would analyse something, suggest an edit to this page.
</aside>

## The requirements {#requirements}

<div class="callout callout--stop" markdown="1">
**Every analysis meets the ones that apply to it.**

1. Write down your analysis plan before you collect data, so your test answers your question rather
   than a pattern you happened to spot. ([Plan](#plan))
2. The model counts independent repeats (trials, birds, specimens), not data points, so results
   don't look more certain than they are. ([Plan](#plan))
3. The model accounts for linked measurements, such as repeated trials on one bird or related
   species, because they tend to resemble each other. ([Plan](#plan))
4. Check how well the model fits, and save that check with your code so anyone can rerun it.
   ([Check](#check))
5. Report every test, significant or not, with its estimate and 95% interval. The size of an effect
   usually matters most, and null results count. ([Report](#what-to-report))
6. Report enough for someone to rerun the analysis, and share the data and code when the paper is
   published. ([Report](#what-to-report))
7. Report measurement uncertainty separately from the statistical results, because they answer
   different questions. ([Report](#what-to-report))
</div>

Some situations add to this list: many comparisons, large measurement uncertainty, or very few
samples. See [Situation-dependent checks](#situation-dependent-checks).

## Plan before you collect {#plan}

<aside class="marginnote" markdown="1">
**Before your first analysis,** read [Makin & Orban de Xivry (2019)](https://doi.org/10.7554/eLife.48175):
ten common statistical mistakes, a page each.
</aside>

None of this needs to be elaborate. A few clear, thoughtful sentences now will save weeks later.

1. **Decide what to quantify.** Turn each prediction from your
   [hypothesis]({{ '/lab-guide/research-hypotheses/' | relative_url }}) into a quantity you can
   measure and compare.
    - If you expect a vortex to be "more developed", name the measure that would show it, what you
      will compare it with, and how large a difference would matter physically.
    - If you expect no difference, decide how similar counts as the same.
    - Settle this before choosing a model. A correct model cannot rescue a vague comparison.
2. **Write a short plan** and save it in the project repository before the first trial or simulation
   run.
    - Say what you will measure, what you will compare, and what result would support or count
      against each hypothesis.
    - One rough paragraph is enough. Plans often change once data arrive; just note what changed and
      why.
    - Writing it first protects you from trying analyses until something looks significant
      ([p-hacking](https://pmc.ncbi.nlm.nih.gov/articles/PMC4359000/)).
3. **Name what counts as one repeat** in your plan, and what the results apply to.
    - One hawk with ten trials sampled 4000 times each is ten repeats, and the results apply to that
      hawk.
    - Check: the model's reported degrees of freedom should be near your number of repeats, not your
      number of data points.
    - Treating data points as repeats is **pseudoreplication**
      ([Hurlbert 1984](https://doi.org/10.2307/1942661); [Lazic 2010](https://doi.org/10.1186/1471-2202-11-5)).
4. **Account for linked measurements.** Common starting points:
    - Repeated trials on one bird: give each trial its own baseline (a random intercept for trial).
    - Repeated configurations of one specimen: the same, for the specimen.
    - Several species: include their family tree (the phylogeny).
    - Then check for links the model missed, such as samples close in time that resemble each other.

<aside class="marginnote marginnote--stop" markdown="1">
**Ten thousand frames from one bird are still measurements of one bird.** Treating them as
independent inflates the degrees of freedom (how many independent pieces of information the model
thinks it has), narrows the interval, and gives a $$p$$-value for an experiment nobody ran.
</aside>

<aside class="marginnote" markdown="1">
Our own analyses have used `(1 | trial_id)` for repeated perching trials
([Martínez-Carmena et al. 2026](https://doi.org/10.1098/rsif.2025.1082)), `(1 | WingID)` for repeated
morphed configurations of the same specimen
([Harvey et al. 2021](https://doi.org/10.1098/rsif.2021.0132)), and a phylogenetic generalised
linear mixed model across 22 species ([Harvey et al. 2022](https://doi.org/10.1038/s41586-022-04477-8)).
</aside>

For help setting up these models, see [Harrison et al. (2018)](https://doi.org/10.7717/peerj.4794).
If one won't fit or gives warnings, see
[Bolker's FAQ on generalised linear mixed models (GLMMs)](https://bbolker.github.io/mixedmodels-misc/glmmFAQ.html).

## Explore before you fit {#explore}
<span id="the-five-stages"></span>

- Clean the data with code and leave the raw files untouched
  ([Data management]({{ '/lab-guide/data-management/' | relative_url }})).
- Make lots of quick, rough plots, working through the eight checks of
  [Zuur, Ieno & Elphick (2010)](https://doi.org/10.1111/j.2041-210X.2009.00001.x).
- Use plots for these checks. With thousands of samples, a formal test flags almost everything.

<details class="guide-details" markdown="1">
<summary>The eight exploration checks</summary>

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
VIF is the variance inflation factor; ACF, the autocorrelation function. Check 8 tells you which
measurements are linked. Check 5 is a common reason to reach for
<a href="#principal-component-analysis">principal component analysis (PCA)</a>.</figcaption>
</figure>
</details>

<div class="callout callout--warn" markdown="1">
**Exploring can shape how you model the data, but your plan sets what you test.**

- What you see can guide choices such as a transformation, or which measurements are linked.
- It can also raise new questions worth following.
- If you test something you only noticed after seeing the data, call it exploratory. Presenting it
  as planned (called HARKing, Hypothesizing After the Results are Known) overstates the evidence.
</div>

## Choose a model {#choosing-a-model}

Start simple. The simplest model that fits your design is usually enough, and you can add to it if
the checks show you need to. Your plan should say why the model answers your question.

<details class="guide-details" markdown="1">
<summary>Starting models for common kinds of data</summary>

| Your data | Start with | Where it is explained |
|---|---|---|
| One value per condition, conditions independent | `lm()` | [Schluter, *Fit model*](https://www.zoology.ubc.ca/~schluter/R/Model.html) → Simple linear regression |
| Repeated measurements on the same bird, specimen or model | `lmer(y ~ x + (1 \| ID))` | [Schluter, *Fit model*](https://www.zoology.ubc.ca/~schluter/R/Model.html) → Mixed models; [Coding Club](https://ourcodingclub.github.io/tutorials/mixed-models/) |
| Several individuals, generalising to the species | `lmer()`, individual as random intercept | [Harrison et al. 2018](https://doi.org/10.7717/peerj.4794) |
| Multiple species | `gls(..., correlation = corPagel())`, or PGLMM in `MCMCglmm` | [Schluter, *Phylogenetic comparison*](https://www.zoology.ubc.ca/~schluter/R/Phylogenetic.html); [Hadfield's course notes](https://cran.r-project.org/web/packages/MCMCglmm/vignettes/CourseNotes.pdf) |
| Counts, proportions, binary outcomes | `glmer()` or `glmmTMB()` | [Bolker's GLMM FAQ](https://bbolker.github.io/mixedmodels-misc/glmmFAQ.html) |
| Competing functional forms (e.g. linear vs quadratic) | Fit each, compare by Akaike information criterion (AIC) | [Harrison et al. 2018](https://doi.org/10.7717/peerj.4794), multi-model inference |
| Real uncertainty on **both** axes | Major-axis or standardised major-axis regression (`smatr`) | [Schluter, *Fit model*](https://www.zoology.ubc.ca/~schluter/R/Model.html) → Correct for body size |
| A deterministic sweep with no sampling noise | No test. Run a sensitivity study instead | [Harvey 2024](https://doi.org/10.1098/rsif.2023.0734) |
| Many correlated shape or morphology variables, no single response | [PCA](#principal-component-analysis) | [Schluter, *Multivariate methods*](https://www.zoology.ubc.ca/~schluter/R/Multivariate.html) |

If you compare models, keep the set small, with each model answering a hypothesis you can state.
Fifty combinations ranked by AIC will find patterns in noise.
</details>

## Check the fit {#check}

- Plot the residuals (what is left after the model's prediction) and look for patterns.
  [`DHARMa`](https://cran.r-project.org/web/packages/DHARMa/vignettes/DHARMa.html) works for most
  models.
- Save the code and plots with your analysis, so anyone can rerun the check when the data change.
- Check that the conclusion still holds under other reasonable choices, such as how you handle
  outliers or set up the model, and report how much it changes
  ([Writing papers]({{ '/lab-guide/writing-papers/' | relative_url }}#methods)).

## Report {#what-to-report}

- **Lead with the size of the effect and its 95% interval.** A $$p$$-value only tells you how
  surprising your data would be if there were no effect, not how big the effect is
  ([Wasserstein, Schirm & Lazar 2019](https://doi.org/10.1080/00031305.2019.1583913);
  [Amrhein, Greenland & McShane 2019](https://doi.org/10.1038/d41586-019-00857-9)).
- **Report every planned test,** whatever its $$p$$-value. Our field's default is $$\alpha = 0.05$$,
  two-sided.
- **Treat null results as results.** If the interval is narrow, a non-significant result shows any
  effect is small, and that deserves the same care as a positive result. If it is wide, say the data
  can't tell yet rather than "no effect".
- **Discuss results by how big and how certain they are,** and what they mean for your question.
- **Say what the result means physically** and how it compares with independent evidence.
  [Writing papers]({{ '/lab-guide/writing-papers/' | relative_url }}#quantify) covers the wording.
- **Keep measurement uncertainty separate.** It goes in the error bars and text, following
  [Error and uncertainty analysis]({{ '/lab-guide/uncertainty-analysis/' | relative_url }}).
  Statistical uncertainty goes in the confidence intervals.
  [Figures]({{ '/lab-guide/figures/' | relative_url }}) covers labelling which is which.
- **Share the data and analysis code** when the paper is published, following
  [Data management]({{ '/lab-guide/data-management/' | relative_url }}#share-and-archive-on-publication).

Include enough for someone to rerun the analysis:

| Item | Example |
|---|---|
| Model formula, random terms included | `lift ~ condition + (1 \| trial)` |
| What counts as one repeat, in words | "1 hawk, 5 trials per condition, ~4000 samples per trial" |
| Software and package versions | R 4.4.1; `lmerTest` 3.1-3 |
| Estimation and degrees-of-freedom method | Restricted maximum likelihood (REML), Kenward–Roger |
| Test statistic, degrees of freedom and exact $$p$$ | $$F_{1,17.06} = 13.28$$, $$p = 0.002$$ ("$$p < 0.001$$" only below that) |
| Estimate with a 95% interval | $$-0.14$$ [$$-0.21$$, $$-0.07$$] |
| Effect size and model fit, where meaningful | partial $$\eta^2 = 0.51$$; marginal and conditional $$R^2$$ |
| Seed, for anything resampled | `set.seed(42)` |
{: .table-budget}

<aside class="marginnote" markdown="1">
**Two kinds of $$R^2$$** ([Nakagawa & Schielzeth 2013](https://doi.org/10.1111/j.2041-210x.2012.00261.x)):
marginal $$R^2$$ is what your predictors explain; conditional $$R^2$$ adds what the grouping (trials,
birds) explains. `performance::r2()` gives both.
</aside>

## Situation-dependent checks {#situation-dependent-checks}
<span id="when-you-need-more"></span><span id="going-further"></span><span id="sharpening-the-analysis"></span>

Not every project needs these. If one fits your situation, it becomes part of your analysis. Some
are harder than others, so look for them while you plan and talk them through with Christina. Open
the ones that apply to you.

<details class="guide-details" markdown="1">
<summary>When you fit many models or test many responses</summary>

- Some will look significant by chance.
- Choose one main measurement in advance, correct for multiple comparisons, or label the rest
  exploratory.
- Say which you did.
</details>

<details class="guide-details" markdown="1">
<summary>When measurement uncertainty is large relative to the effect</summary>

- Rerun the analysis many times with each point shifted at random within its uncertainty, and check
  the conclusion holds (method in
  [Error and uncertainty analysis]({{ '/lab-guide/uncertainty-analysis/' | relative_url }})).
- [Harvey et al. (2022)](https://doi.org/10.1038/s41586-022-04477-8) used 5,000 reruns across the
  centre-of-gravity error range.
</details>

<details class="guide-details" markdown="1">
<summary>When you have one or two animals or specimens</summary>

- Significant results from small samples tend to overstate the effect, because only large estimates
  reach significance.
- Report the smallest effect your design could have detected. You can simulate this with
  [`simr`](https://cran.r-project.org/package=simr), using the variability from pilot data and the
  smallest effect that would matter physically.
- Schluter's [Planning tools](https://www.zoology.ubc.ca/~schluter/R/Plan.html) page covers simpler
  cases.
</details>

<details class="guide-details" markdown="1">
<summary>When your question compares conditions</summary>

- Report the difference itself, in the original units, with its interval.
- [`emmeans`](https://cran.r-project.org/web/packages/emmeans/vignettes/basics.html) and
  [`marginaleffects`](https://cran.r-project.org/package=marginaleffects) do this, and correct for
  multiple comparisons.
</details>

<details class="guide-details" markdown="1">
<summary>When the model has several predictors</summary>

- Plot what the model predicts as well as the raw data.
- [`visreg`](https://pbreheny.github.io/visreg/) shows the effect of one predictor with the others
  held fixed, and works with `lmer` fits.
</details>

<details class="guide-details" id="principal-component-analysis" markdown="1">
<summary>When you have many correlated variables and no single response (PCA)</summary>
<span id="decomposition"></span><span id="dynamic-mode-decomposition"></span>

Principal component analysis (PCA) suits data such as a wing outline described by fifty correlated
coordinates. Schluter's [Multivariate methods](https://www.zoology.ubc.ca/~schluter/R/Multivariate.html)
page covers the mechanics.

- **Scale first.** If variables have different units, use `scale. = TRUE` so no single variable
  dominates. Align landmark coordinates first with
  [`geomorph::gpagen()`](https://doi.org/10.1111/2041-210X.12035), so position and size don't
  become the first components.
- **Decide in advance how many components to keep.**
- **Interpret by drawing** the shape at each end of a component. Two outlines show what it means
  more clearly than a table of numbers.
- **Treat components as specific to your sample.** They shift when specimens are added. Scores used
  in later models are estimates, so say so in the methods.
- **A small percentage can still matter.** In
  [Gamble et al. (2020)](https://doi.org/10.1088/1748-3190/ab9b6f), PC2 explained only 0.3% of
  trailing-edge shape change, yet captured a real angle-of-attack effect.
- **Signs are arbitrary.** State which shape each positive direction represents, and keep it the
  same across every figure.
- **Report** the number of variables and specimens, the scaling and alignment, the variance
  explained by each component you kept, how you chose how many to keep, and the sign convention.
- **For motion over time,** note that PCA ignores time. Dynamic mode decomposition (DMD) finds
  patterns that each carry a frequency and growth rate; Lydia France's
  [BirdDMD](https://lydiafrance.github.io/BirdDMD/) is the place to start. If you use it, check how
  well it reproduces data it wasn't fitted to.
</details>

<details class="guide-details" markdown="1">
<summary>When you have only two or three replicates</summary>

- A Bayesian fit is an option: see the [`brms` tutorial](https://ourcodingclub.github.io/tutorials/brms/)
  or the [`MCMCglmm` tutorial](https://ourcodingclub.github.io/tutorials/mcmcglmm/).
- With so little data, your prior assumptions strongly shape the result. Choose them before you see
  the data, and report how much the conclusion depends on them.
</details>

## Where to learn more {#where-to-learn}
<span id="where-to-learn-each-method"></span>

- **Everything on this page:** Schluter's pages, plus the worked R for every example in
  [*The Analysis of Biological Data*](https://whitlockschluter3e.zoology.ubc.ca/RExamples/).
- **Phylogenetic comparative methods:** Revell & Harmon (2022), *Phylogenetic Comparative Methods
  in R*, and [`phytools` 2.0](https://doi.org/10.7717/peerj.16505).
- **PCA in depth:** [Jolliffe & Cadima (2016)](https://doi.org/10.1098/rsta.2015.0202).
