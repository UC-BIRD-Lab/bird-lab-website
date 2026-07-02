---
title: Analyze data
category: Research Workflow
order: 6
summary: A staged approach to analysis — clean, explore, quantify, and report with uncertainty.
---

So you finished your experiment or your code finally converged — great. Now comes
the analysis.

<div class="callout" markdown="1">
We recommend all students get comfortable analyzing data in R.
</div>

1. **Clean your data.** Ensure consistency and remove blanks, false recordings,
   and other artifacts. This can take about a week.

   <div class="callout callout--warn" markdown="1">
   Never edit your raw data. Save any cleaned data separately.
   </div>

2. **Explore the data.** Make many simple (un-styled) x–y plots to get a feel for
   the trends. You should have decided what trends to quantify *before* running
   the experiment. This can take 1–2 weeks.

3. **Quantify your trends.** Use statistical approaches in R to test for
   significant effects. Keep your original hypothesis in mind and avoid
   [p-hacking](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4359000/). Dolph
   Schluter's [R tips pages](https://www.zoology.ubc.ca/~schluter/R/index.html)
   are a great resource.

4. **Calculate error and uncertainty.** All reported trends must have 95%
   confidence intervals or a quantification of experimental uncertainty — see
   [Analyze error & uncertainty]({{ '/lab-guide/analyze-error-uncertainty/' | relative_url }}).

5. **Plot your data.** See [Design your figures]({{ '/lab-guide/design-your-figures/' | relative_url }}).
