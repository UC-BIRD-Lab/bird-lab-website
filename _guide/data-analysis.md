---
title: Data analysis
category: Research Workflow
order: 6
summary: "A staged approach to analysis: clean, explore, quantify, and report with uncertainty."
keywords: [analysis, statistics, R, uncertainty, error, plots, quantify, stats, wind tunnel, GUM, autocorrelation, error propagation, effective sample size, Zieba, Type A, Type B, bootstrap, static margin]
icon: "📊"
reviewed: 2026-07-11
math: true
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
   [p-hacking](https://pmc.ncbi.nlm.nih.gov/articles/PMC4359000/). Dolph
   Schluter's [R tips pages](https://www.zoology.ubc.ca/~schluter/R/index.html)
   are a great resource.

4. **Calculate error and uncertainty.** Every reported value carries a quantified
   uncertainty, see [below](#error-and-uncertainty).

5. **Plot your data.** See [Figures]({{ '/lab-guide/figures/' | relative_url }}).

## Error and uncertainty

<div class="callout" markdown="1">
**The whole thing, at a glance.** Work down this list. Each number is a step below, and the steps say why. We follow the [GUM](https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf).

1. Cut each run down to the settled, stationary window.
2. Plot and visualize the autocorrelation. Estimate $$N_\text{eff}$$, then
   $$u_A = s_\text{corr}/\sqrt{N_\text{eff}}$$.
3. If the autocorrelation rings, skip $$N_\text{eff}$$ and bootstrap instead.
4. Build a Type B budget. 
5. Assemble the full budget to compute the combined uncertainty.
6. Propagate with `errors` / `uncertainties`. Expand with Student-$$t$$.
7. For slopes, use Monte Carlo for the systematic terms.
8. Replicate runs, and cross-check against something independent.
</div>

### Two numbers come out of a signal

<div class="callout callout--stop" markdown="1">
**Spread, $$s_\text{corr}$$.** How much the signal moves. Buffeting is physics; this measures it.

**Uncertainty of the mean, $$u_A = s_\text{corr}/\sqrt{N_\text{eff}}$$.** How well this record pins down its own mean. The statistical (Type A) ingredient of the error bar, not the whole bar.

**Report both, labelled.** The error bar on a reported mean is the expanded combined uncertainty $$U = k\,u_c$$ from Step 6, which carries $$u_A$$ inside it. The fluctuation gets its own band.
</div>

<details class="guide-details" markdown="1">
<summary>Glossary: every term used on this page</summary>

| Term | Plain words |
|---|---|
| **Measurand** | The thing you want. Usually a mean: "average lift at 5 degrees." |
| **Error** | How far you are from the truth. Unknowable. |
| **Uncertainty** | The size of the range the truth plausibly sits in. Estimable. |
| **Standard uncertainty**, $$u$$ | An uncertainty written as one standard deviation. |
| **Type A** | From the statistics of recorded data. |
| **Type B** | From anything else: a cert, spec sheet, tolerances, or judgment. Never measured. |
| **Random error** | Changes reading to reading. Averaging reduces it. |
| **Systematic error** | The same on every reading. Averaging does nothing to it. |
| **Autocorrelation**, $$\hat\rho_j$$ | How much a sample resembles the one $$j$$ steps earlier. |
| **Integral time scale**, $$T_u$$ | How long the signal stays correlated with itself. |
| **Effective sample size**, $$N_\text{eff}$$ | How many independent samples the dataset includes. |
| **Degrees of freedom**, $$\nu$$ | How well you know your own uncertainty. Small $$\nu$$ means poorly. |
| **Combined uncertainty**, $$u_c$$ | Everything added in quadrature. |
| **Coverage factor**, $$k$$ | What you multiply $$u_c$$ by to reach a stated confidence. |
| **Expanded uncertainty**, $$U$$ | $$U = k\,u_c$$. The number on your plot. |
| **Sting** | The arm holding the model in the flow. Rings like a tuning fork after any move. |
| **Tare** | The reading with no flow or no load, subtracted from every measurement. |

Type A and Type B describe **how you found the number**, not whether the error is random or systematic ([GUM](https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf), 3.3.4). Both go into the final answer.
</details>


<aside class="marginnote" markdown="1">
**Stationary** means the average and spread are not drifting. 

- Running mean should flatten, not trend.
- Window halves should have similar mean and spread.
- The autocorrelation should decay.

**Still trending? Adjust window.** If no window passes, report the condition as unsteady. 
</aside>

### Step 1. Cut the record to the steady part

The DAQ records continuously. Only part of each run is your test state.
- **Start-up.** The flow takes time to reach the desired speed.
- **Change-over.** Step to a new angle or speed and the sting rings, the flow re-establishes. Those samples belong to the *move*.

Plot the raw trace. Keep the settled window. Its mean is the value you report.

### Step 2. Find how many independent samples you have

100,000 correlated samples are not worth 100,000 independent ones. This step determines how many samples you have that are independent, $$N_\text{eff}$$.

<aside class="marginnote marginnote--warn" markdown="1">
**Ignore the dashed lines.** R's `acf()` draws a band at $$\pm 2/\sqrt{N}$$. That band assumes *white* noise, so a healthy decaying autocorrelation sits outside it constantly. 
</aside>

**a. Compute the autocorrelation.** `acf()` in R, `statsmodels.tsa.stattools.acf()` in Python. One number per lag.

<aside class="marginnote" markdown="1">
**You are not trimming your data.** You are choosing how many autocorrelation values go into one sum. The "cut" is the upper limit of a summation.
</aside>

**b. Plot the autocorrelation. Decide where to truncate the sum.** The only judgment call here. Every real autocorrelation wobbles across zero once it decays. That jitter is estimation noise. Judge whether the negative part is only jitter.

<aside class="marginnote marginnote--warn" markdown="1">
**Never sum every lag of a single record.** With the record's own mean subtracted, the sum of *all* the values is exactly $$-\tfrac{1}{2}$$ for any data, so the denominator collapses to zero ([Percival 1993](https://doi.org/10.1080/00031305.1993.10475997)).

**Start the sum at lag 1, never lag 0.** Routines hand you lag 0 first and it is always exactly one. Including it is the most common bug here, and it is silent.
</aside>

- **Decays, negative part small and brief.** → Cut-off at the first zero crossing. The standard single-record choice ([Smith et al. 2018](https://doi.org/10.1088/1361-6501/aae91d)).
- **Persistently negative, swinging back on a period.** Do not pick a cutoff,
  [bootstrap](#step-3-if-the-autocorrelation-rings-bootstrap-instead). The zero crossing overestimates $$T_u$$ here (Smith et al.), and a truncated sum can even go negative, making $$N_\text{eff}$$ meaningless.

<div class="callout" markdown="1">
**No numeric threshold exists** to tell the two cases apart. It is a judgment about your own signal (Smith et al.).

**Unsure? Bootstrap (Step 3).** Correct either way, one function call.
</div>

**c. Compute these three**, summing lag 1 to your stopping lag $$k$$:

$$N_\text{eff} = \frac{N}{1 + 2\sum_{j=1}^{k}\hat\rho_j}
\qquad
s_\text{corr}^2 = C\,s^2 ,\quad C = \frac{N_\text{eff}(N-1)}{N(N_\text{eff}-1)}
\qquad
u_A = \frac{s_\text{corr}}{\sqrt{N_\text{eff}}}$$

<small>[Zięba 2010](http://www.metrology.pg.gda.pl/full/2010/M&MS_2010_003.pdf), Eqns. 12
($$N_\text{eff}$$), 24b ($$C$$), 25 ($$u_A$$) ·
[Smith et al. 2018](https://doi.org/10.1088/1361-6501/aae91d), Eqns. 4 and 18</small>

$$u_A$$ is the Type A uncertainty, which is used to compute the combined uncertainty in Step 5.

<div class="callout callout--warn" markdown="1">
**Record for at least $$20\,T_u$$** ([Smith et al. 2018](https://doi.org/10.1088/1361-6501/aae91d)). Record **longer**, do not sample **faster**: faster sampling only adds near-copies of samples you already have.
</div>

<details class="guide-details" markdown="1">
<summary>Why this is right, and why the full sum fails</summary>

**Checked against reality.** [Smith et al. 2018](https://doi.org/10.1088/1361-6501/aae91d) took five long experimental records (hot-wire jet, pressure in a cylinder array, hot-wire airfoil boundary layer) and asked how often the reported error bar actually contains the true mean. A one-sigma band should contain it 68% of the time.

- Bars from $$s/\sqrt{N}$$: **almost never** contained it.
- Bars from $$s/\sqrt{N_\text{eff}}$$: contained it **very close to 68% of the time.**

**Where $$N_\text{eff}$$ comes from.** The denominator is $$2T_u/\Delta t$$. Tennekes and Lumley showed two samples are independent only when more than $$2T_u$$ apart, so you are counting independence windows. Zięba derives the same quantity in metrology language.

**Why our formula has no $$(1 - j/N)$$ and Zięba's Eqn. 12 does.** `acf()` in R and
`acf(adjusted=False)` in Python divide by $$N$$ at every lag, which already bakes that weight in. 

**$$N_\text{eff} > N$$ is not automatically a bug.** Anti-correlated samples converge faster than independent ones, so a ringing signal can have more effective samples than samples ([Smith et al. 2018](https://doi.org/10.1088/1361-6501/aae91d)).

**With many records, Smith et al.'s first choice is different.** Given a record long enough to split into many segments, they recommend computing each segment's autocorrelation with the *parent* mean and variance, ensemble-averaging, and summing **all** lags. The zero-crossing cut is the single-record fallback, and even there they judge the bootstrap more robust. Our recipe assumes the usual tunnel case: one record per condition.
</details>

### Step 3. If the autocorrelation rings, bootstrap instead

A ringing autocorrelation, or a short record, gives $$N_\text{eff}$$ no reliable answer. Use a **block bootstrap** ([Künsch 1989](https://doi.org/10.1214/aos/1176347265); brought to fluids by
[Theunissen et al. 2008](https://doi.org/10.1007/s00348-007-0421-0)).

Cut the record into sections long enough to hold the correlation. Draw blocks at random with replacement, concatenate into a new dataset, then take its mean. Repeat a few thousand times. The middle 95% of those means **is** your confidence interval. The correlation survives inside each block, so it is never measured.  In R, `boot::tsboot`.

**To feed the budget in Step 5**, use the standard deviation of the bootstrap means as $$u_A$$.

Requires one setting choice, the block length: see
[Politis & White 2004](https://doi.org/10.1081/ETC-120028836).

<div class="callout" markdown="1">
**Run both and compare.** They should agree where the autocorrelation is well behaved.
Bad disagreement usually means the record is not stationary.
</div>

<aside class="marginnote marginnote--stop" markdown="1">
**A term you cannot measure is not a term you may set to zero.** Setting a calibration uncertainty to zero in code claims, in print, that the instrument is perfect. Knowingly leave a systematic effect uncorrected and the GUM requires you to carry it as an uncertainty (Note to 6.3.1, and F.2.4.5).
</aside>

### Step 4. Build a Type B budget

Type B is based on calibration certificates, spec sheets, machining tolerances, or previous experiments
([GUM](https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf), 4.3.1). Note that Type B does not shrink with sample size.

To turn a specification into a standard uncertainty use the
[GUM](https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf):

| You are given | Assume | $$u$$ | GUM |
|---|---|---|---|
| Certificate quoting $$U$$ **and** a coverage factor $$k$$ | | $$U/k$$ | 4.3.3 |
| Certificate quoting a **confidence level**, no $$k$$ | Normal | $$U/1.64$$ (90%) · $$U/1.96$$ (95%) · $$U/2.58$$ (99%) | 4.3.4 |
| Bounds $$\pm a$$, nothing else known | Rectangular | $$a/\sqrt{3}$$ | 4.3.7 |
| Bounds $$\pm a$$, middle values likelier | Triangular | $$a/\sqrt{6}$$ | 4.3.9 |
| Digital readout, resolution $$q$$ | Rectangular | $$q/\sqrt{12}$$ | F.2.2.1 |

<aside class="marginnote" markdown="1">
**The two rows people get wrong.**

**Angle of attack.** Not encoder resolution. Tunnels are typically quoted at around 0.1 degrees of flow angularity (Barlow, Rae & Pope, sec. 3.3), orders of magnitude above an encoder step, and AoA feeds the stability slopes directly.

**Balance calibration.** Routinely one of the largest systematic terms in any force measurement
([NASA](https://ntrs.nasa.gov/api/citations/20160009122/downloads/20160009122.pdf)).
</aside>

Fill in the budget before you write any propagation code:

| Source | | Comes from |
|---|---|---|
| Balance calibration | B | Calibration certificate, full-scale accuracy |
| Pressure transducer | B | Transducer certificate |
| Atmospheric pressure | B | Barometer resolution |
| Angle of attack | B | Mount alignment and flow angularity |
| Moment arm | B | Machining tolerance |
| Reference area, chord | B | 3D scan or CAD repeatability. Change per configuration on a morphing wing, and scale the static margin |
| Wall and blockage | B | Left uncorrected, bounded by model sizing (details below) |
{: .table-budget}

Sum all contributions in this table in quadrature: $$u_B = \sqrt{u_B1^2 + u_B2^2}$$ ([GUM](https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf), 5.1.2), but only once every term is expressed in the units of the result. For example, do not add Newtons to degrees. The sensitivity factors used for propagation are dealt with in packages in Step 6. Your job in this step is to make sure every row exists, as a standard uncertainty. 

$$u_B$$ is the Type B uncertainty, which is used to compute the combined uncertainty in Step 5.

<details class="guide-details" markdown="1">
<summary>Worked example: our ATI Mini40 load cell</summary>

The certificate quotes **"Measurement Uncertainty (95% confidence level, percent of full-scale load)"**. A confidence level with no coverage factor is the second row of the table above, so divide by 1.96 (GUM 4.3.4). The values below are from our current certificate — **recheck them after every recalibration**.

| Axis | Full scale | Certificate | $$U$$ (95%) | $$u = U/1.96$$ |
|---|---|---|---|---|
| Fx | 80 N | 1.50% FS | 1.20 N | **0.61 N** |
| Fy | 80 N | 1.25% FS | 1.00 N | **0.51 N** |
| Fz | 240 N | 1.50% FS | 3.60 N | **1.84 N** |
| Tx | 4 N·m | 1.25% FS | 0.050 N·m | **0.026 N·m** |
| Ty | 4 N·m | 1.75% FS | 0.070 N·m | **0.036 N·m** |
| Tz | 4 N·m | 1.25% FS | 0.050 N·m | **0.026 N·m** |

<div class="callout callout--stop" markdown="1">
**Percent of full scale, not percent of reading.** $$u$$ is a fixed number of newtons no matter how small your load is. On the 80 N axes that is **0.61 N, permanently.**

A gliding bird wing makes lift of order a few newtons. So the balance alone contributes:
| If lift is | $$u_B$$ as a fraction of your signal |
|---|---|
| 1 N | **61%** |
| 2 N | 31% |
| 5 N | 12% |
| 10 N | 6% |

On a low-load run this single term can outweigh every Type A term put together. **Never let lift land on Fz**: the 240 N range carries 1.84 N. Mount so the aerodynamic forces sit on the 80 N axes.
</div>

**No temperature compensation, and no mounting error.** The certificate is issued at 22.2 ± 1.1 °C and conditions its accuracy on loads being "correctly aligned to the transducer origin". Thermal drift and mount alignment are *additional* Type B terms that you own.
</details>

<details class="guide-details" markdown="1">
<summary>Why we do not apply wall and blockage corrections</summary>

The standard corrections (Barlow, Rae & Pope, ch. 10) are derived for conventional shapes. A morphing bird wing is not one, so the model error they import is plausibly larger than the effect they remove.
We attack the problem at the source: small model, low blockage ratio, reflection-plane mount.

**Not correcting is not the same as claiming the effect is zero.** State your solid blockage ratio in the paper, bound the residual effect, and enter it as a Type B term. The GUM requires this (Note to 6.3.1, and F.2.4.5), and it is what makes the decision defensible to a reviewer.
</details>

### Step 5. Assemble the full budget

Type A and B uncertainties add in quadrature to compute the combined uncertainty: $$u_c = \sqrt{u_A^2 + u_B^2}$$.

### Step 6. Propagate, then expand to about 95%

Do not hand-write a propagation formula. Carry the uncertainty inside the numbers, with R
[`errors`](https://cran.r-project.org/package=errors) or Python
[`uncertainties`](https://uncertainties.readthedocs.io/). Push it through the calibration matrix, density, airspeed, the coefficients, and the stability metrics.

<div class="callout" markdown="1">
**The packages need to know how your data is correlated.** They propagate correlation through an *expression*, so one airspeed feeding many coefficients is automatic. Correlations *between separate measured inputs* are not: declare them with `correl()` / `covar()` in R ([Ucar et al. 2018](https://journal.r-project.org/articles/RJ-2018-075/RJ-2018-075.pdf)) or
`correlated_values()` in Python. Undeclared means silently assumed independent. For example, load-cell channels are read at the same instant and are correlated. And one calibration, one tare, one dynamic pressure are shared by **every point in a sweep**, so their errors are systematic and correlated across the whole curve. Those off-diagonal terms can *increase or decrease* your final variance (Barlow, Rae & Pope, sec. 12.2), so independence is not a safe default.
</div>

Then expand to 95%: $$U = 1.96\,u_c$$. **State $$k$$ and the confidence level.** An interval without them cannot be checked by anyone, including you.

<details class="guide-details" markdown="1">
<summary>Why we use $$k=1.96$$ for wind tunnel data</summary>

$$k$$ is the Student-$$t$$ value at the Welch-Satterthwaite degrees of freedom
([GUM](https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf), Eqn. G.2b):

$$\nu_\text{eff} = \frac{u_c^4}{\sum_i u_i^4/\nu_i}$$

**$$\nu$$ is not how big an uncertainty is. It is how well you know that uncertainty.** A Type A term is computed from noisy data, so it wobbles: few samples, poor estimate, large $$t$$, wider bar. That is the entire job of $$\nu$$. (If you ever need it, the Type A value is $$\nu_\text{eff} \approx N/(1 + 2\sum_j \hat\rho_j^2) - 1$$, Zięba Eqn. 30.)

A certificate is different. ATI states 1.5% of full scale. You are not estimating that from data, you are reading it off a document, so it has no scatter. The GUM sets $$\nu = \infty$$ for exactly this (G.4.3) and the term drops out of the sum above.

So $$\nu = \infty$$ says **"I am certain the uncertainty is 0.61 N."** It does not say 0.61 N is small.

A wind tunnel uncertainty budget is dominated by certificate terms, so $$\nu_\text{eff}$$ runs very large and $$t \to 1.96$$. It stays close to 1.96 until a Type A term with few effective samples carries a large share of the variance — compute $$\nu_\text{eff}$$ and look up $$t$$ when in doubt.

**To hedge**, GUM G.4.2 sets $$\nu$$ from how far you trust the certificate:
$$\nu \approx \tfrac12 [\Delta u / u]^{-2}$$. Trusting ATI to ±10% barely moves the final bar. Do not go lower without a reason: doubting the certificate by ±50% gives $$\nu = 2$$ and roughly doubles your uncertainty on a guess.
</details>

### Step 7. Uncertainty of experimentally computed slopes

**Know what `confint()` on an OLS fit does and does not capture.** It captures the scatter of the points about the line, and that is often a reasonable error bar. What it cannot see: uncertainty on the x-axis, and errors shared across the sweep. When those terms matter, the fit's interval under-reports.

To include them, propagate the slope by Monte Carlo. Draw the systematic terms **once per synthetic sweep**, the random terms **once per point**, refit, take the spread of the slopes. If the two intervals agree, the fit's was fine all along ([JCGM 101](https://www.bipm.org/documents/20126/2071204/JCGM_101_2008_E.pdf);
[AIAA G-160-2025](https://arc.aiaa.org/doi/book/10.2514/4.107450)). 

### Step 8. Replicate, then cross-check

One record cannot see whether the tunnel returns to the same speed tomorrow, or the model to the same angle when you re-clamp it. Random uncertainty comes from **replicate runs**: back-to-back repeats, and where affordable, repeats after removing and reinstalling the model ([AIAA S-071A](https://arc.aiaa.org/doi/book/10.2514/4.473647);
[G-160-2025](https://arc.aiaa.org/doi/book/10.2514/4.107450)). Within-run Type A alone under-reports.

Then check that an independent estimate lands inside your interval. Disagreement beyond the combined uncertainty means your budget is missing a term.
[Harvey et al. 2021](https://doi.org/10.1098/rsif.2021.0132) checks tunnel forces against a lifting-line model.

<details class="guide-details" markdown="1">
<summary>Design the runs so the replicates are worth something</summary>

Three principles from Barlow, Rae & Pope (sec. 12.3), worth knowing by name:

- **Replication.** Repeat the run and measure the variability instead of inferring it.
- **Randomization.** Vary the order you set conditions in. Order can affect the result, and
  randomizing averages out what you are not tracking.
- **Blocking.** Measure an *increment* by adding and removing one part while everything else stays installed. A tail-on minus tail-off increment is far more precise than either measurement alone, because the shared systematics cancel in the difference. If your question is comparative, design it as a block to improve the measurement precision.
</details>

### Further reading

**Correlated data.**
- [Smith, Neal, Feero & Richards (2018)](https://doi.org/10.1088/1361-6501/aae91d).
- [Belanger, Lavoie & Zingg (2023)](https://doi.org/10.1007/s00348-023-03704-w) ·
  [Benedict & Gould (1996)](https://doi.org/10.1007/s003480050030) ·
  [Theunissen et al. (2008)](https://doi.org/10.1007/s00348-007-0421-0) ·
  [Politis & White (2004)](https://doi.org/10.1081/ETC-120028836) ·
  [Percival (1993)](https://doi.org/10.1080/00031305.1993.10475997) · Tennekes & Lumley (1972).

**Standards.** 

- [AIAA G-160-2025](https://arc.aiaa.org/doi/book/10.2514/4.107450) ·
  [S-071A-1999](https://arc.aiaa.org/doi/book/10.2514/4.473647) ·
  [ASME PTC 19.1](https://www.asme.org/codes-standards/find-codes-standards/test-uncertainty) ·
  Coleman & Steele (4th ed.).
- Barlow, Rae & Pope (1999), secs. 12.2–12.3. The clearest tunnel-side account of random versus
  systematic error, and of replication, randomization and blocking. **Predates the GUM in
  aerodynamics** and does not correct for autocorrelation: use it for the reasoning, not the recipe.
- [GUM](https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf) ·
  [JCGM 101](https://www.bipm.org/documents/20126/2071204/JCGM_101_2008_E.pdf) (Monte Carlo) ·
  [Zięba (2010)](http://www.metrology.pg.gda.pl/full/2010/M&MS_2010_003.pdf) ·
  [York et al. (2004)](https://doi.org/10.1119/1.1632486) ·
  [`errors` (R)](https://cran.r-project.org/package=errors) ·
  [`uncertainties` (Python)](https://uncertainties.readthedocs.io/)
