---
title: Analyze error & uncertainty
category: Research Workflow
order: 7
summary: The basics of error propagation, plus power-analysis and uncertainty tooling.
---

There is error in everything — in measurement tools, in averages, in propagation.
The methods you apply depend on what you're doing. The following covers the
basics.

## Power analysis

A helpful tool for initial power analyses and sample-size calculations:
[sample-size calculator](https://homepage.univie.ac.at/robin.ristl/samplesize.php?test=anova).

## Propagation of errors (for standard deviations)

If you have errors and are doing arithmetic with the values, you must propagate
the errors. Let `Δx` and `Δy` be the errors on measured variables `x` and `y`.

**Addition / subtraction** — for `z = x ± y`:

```
Δz = sqrt( (Δx)² + (Δy)² )
```

**Multiplication / division** — for `z = x·y` or `z = x/y`:

```
Δz / |z| = sqrt( (Δx/x)² + (Δy/y)² )
```

**Power** — for `z = xⁿ`:

```
Δz / |z| = |n| · (Δx / |x|)
```

**Measured quantity times a constant** — for `z = A·x`:

```
Δz = |A| · Δx
```

## Resources

- **R:** [Dolph Schluter's guide to statistics in R](https://www.zoology.ubc.ca/~bio501/R/workshops/workshops-intro.html)
- **Python:** the [uncertainties](https://uncertainties.readthedocs.io/en/latest/) library
- **MATLAB:** [`movmean`](https://www.mathworks.com/help/matlab/ref/movmean.html) and related moving-statistics tools
