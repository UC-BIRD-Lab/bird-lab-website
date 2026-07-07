---
title: Data analysis
category: Research Workflow
order: 6
summary: "A staged approach to analysis: clean, explore, quantify, and report with uncertainty."
keywords: [analysis, statistics, R, uncertainty, error, plots, quantify, stats]
icon: "📊"
reviewed: 2026-07-05
---

So you finished your experiment or your code finally converged, congrats! Now comes
the fun part: the analysis.

<aside class="marginnote" markdown="1">
Christina strongly recommends all students get comfortable analyzing data in R.
</aside>

1. **Clean your data.** Ensure consistency and remove blanks, false recordings,
   and other artifacts. This can take about a week and needs to be clearly documented and procedural.

   <div class="callout callout--warn" markdown="1">
   Never edit your raw data. Save any cleaned data separately (see the source-file
   rule in [Data management]({{ '/lab-guide/data-management/' | relative_url }})).
   </div>

2. **Explore the data.** Make many simple (un-styled) x–y plots to get a feel for
   the trends. You should have decided what trends to quantify *before* running
   the experiment. This can take 1–2 weeks.

3. **Quantify your trends.** Use statistical approaches in R to test for
   significant effects. Keep your original
   [hypothesis]({{ '/lab-guide/research-hypotheses/' | relative_url }}) in mind and avoid
   [p-hacking](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4359000/). Dolph
   Schluter's [R tips pages](https://www.zoology.ubc.ca/~schluter/R/index.html)
   are a great resource.

4. **Calculate error and uncertainty.** All reported trends must have a quantification of their experimental uncertainty or 95% confidence intervals aligned with best scientific practices, see [below](#error-and-uncertainty).

5. **Plot your data.** See [Figures]({{ '/lab-guide/figures/' | relative_url }}).

## Error and uncertainty

There is error in everything. Recognizing this is a central value of the lab.
The methods to quantify and report the possible error that you apply depend on what you're doing. The following covers some basics. A course in experimental design and statistics can help you to build these skills.

### Power analysis

A helpful tool for initial power analyses and sample-size calculations:
[sample-size calculator](https://homepage.univie.ac.at/robin.ristl/samplesize.php?test=anova).

### Propagation of error

When you combine measured values into a derived quantity, the uncertainty in each
input carries through to the result, and errors tend to accumulate rather than
cancel. Skip this and your final numbers will look far more precise than they are.

<aside class="marginnote" markdown="1">
**Collecting the data itself?** Operating procedures for the wind tunnel, high-speed cameras, and 3D scanner are in the [member portal]({{ '/portal/' | relative_url }}).
</aside>

This comes up constantly in our wind tunnel work. The forces and moments we report
are rarely measured directly: we build them from load-cell readings, geometry, and
flow conditions, then combine those into coefficients, static margins, and
stability derivatives. Each step inherits the uncertainty of its inputs, so a small
error in a raw measurement can dominate a derived result. Two features of wind
tunnel data make this especially important:

- **Fluctuating signals.** We sample a noisy, turbulent flow over time, so the mean
  itself has an uncertainty that must be estimated, not assumed away.
- **Non-independent samples.** Consecutive high-rate samples are correlated, so the
  effective number of independent measurements is far smaller than the raw count.
  Treating every sample as independent understates the true uncertainty.

This is why every reported trend carries a quantified uncertainty (step 4): we
report an expanded uncertainty of roughly a 95% confidence interval and confirm
that independent methods agree within it.

- **The mechanics of how uncertainty propagates through arithmetic:**
  [Propagation of Error (LibreTexts)](https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Supplemental_Modules_%28Analytical_Chemistry%29/Quantifying_Nature/Significant_Digits/Propagation_of_Error).
- **The lab's approach in practice:**
  [Harvey et al. 2021, *J. R. Soc. Interface*](https://doi.org/10.1098/rsif.2021.0132),
  which reports wind tunnel force and moment uncertainty as roughly 95%
  confidence-interval error bars and checks them against numerical predictions.

### Tools

- **R:** [Dolph Schluter's guide to statistics in R](https://www.zoology.ubc.ca/~bio501/R/workshops/workshops-intro.html)
- **Python:** the [uncertainties](https://uncertainties.readthedocs.io/en/latest/) library
- **MATLAB:** [`movmean`](https://www.mathworks.com/help/matlab/ref/movmean.html) and related moving-statistics tools
