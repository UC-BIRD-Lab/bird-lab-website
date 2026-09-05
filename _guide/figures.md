---
title: Figures
category: Writing & Dissemination
order: 3
summary: The lab's figure standards, a self-diagnosis checklist, and tools and palettes.
description: "Why a figure has to stand on its own, how to tell when yours doesn't, and the tools and palettes we use."
keywords: [figures, plots, graphics, illustrator, ggplot, visualization, charts, color]
icon: "🎨"
reviewed: 2026-08-13
math: true
---

<aside class="marginnote" markdown="1">
This is the figure-side companion to
[Writing papers]({{ '/lab-guide/writing-papers/' | relative_url }}).
</aside>

<div class="guide-glance">
<div><span class="k">Jump to</span><a href="#non-negotiables">The non-negotiables</a> · <a href="#the-figure-development-cycle">The development cycle</a> · <a href="#core-principles">Core principles</a> · <a href="#figure-checklist">Figure checklist</a> · <a href="#tools">Tools</a></div>
</div>

A figure is usually the first thing a reviewer looks at and the thing a reader
remembers. The lab's [communication framework]({{ '/lab-guide/presentations/' | relative_url }}#core-principles)
requires that we maximize the signal-to-noise in every figure.

<div class="callout callout--stop" markdown="1" id="non-negotiables">
**Lab policy: the non-negotiables**

- Every figure is generated end-to-end from code (R or Python). No data manipulation or axis alignment in Illustrator.
- The generation script lives in the manuscript repository, clearly named per figure, with raw data versioned.
- All figures are vector (PDF / EPS / SVG) or ≥500 DPI PNG.
- All figures use a consistent, colorblind-safe palette.
- Final figures meet the target journal's requirements (size, fonts, DPI, panel-label style).

The rules exist so any figure can be checked and rebuilt, by reviewers, collaborators, or you.
</div>

## The figure development cycle

<aside class="marginnote" markdown="1">
**Clarity beats prettiness.** A figure that lands its takeaway in three seconds
with ugly defaults beats a beautiful one whose point you have to hunt for. Do the
styling last.
</aside>

1. **Storyboard:** decide the goals and rough layouts of all figures before any software.
2. **Rough plot:** ugly but functional.
3. **Refine structure:** lock layout, panel order, axis ranges, labeling.
4. **Apply styling:** colors, typography, annotation (the fun part, but *last*).
5. **Review and revise:** show it to a colleague *without* the caption and ask their three-second takeaway. If it doesn't match yours, it isn't done. (On asking for and taking critique, see [giving and receiving feedback]({{ '/lab-guide/communication/' | relative_url }}#giving-and-receiving-feedback).)

Most "beautiful" published figures go through 10–20 iterations (not an exaggeration).

## Core principles {#core-principles}

### 1 · Plan the figure before you open software

Before plotting, think about: what is the major point, who is the audience, what figure
*type* fits, and which elements are essential vs. optional. For major journal
articles and any complex multi-panel figures, run a storyboard session with
Christina before you write plotting code.

### 2 · One message per figure

Each figure needs to convey something clearly to the audience.
Multi-panel figures are good when panels build a single argument together. 
Avoid bundling unrelated results into subpanels to save space.

### 3 · Generate every figure from code

The figure is built end-to-end in R or Python. The script outputs the *final* figure file. Name it clearly per figure (e.g., `fig2_lift_vs_alpha.R`). Start from the [lab R theme](#tools).

All raw data used in the figure generation is versioned and lives in FigShare on publication.  

### 4 · Show the data honestly

Your figure is part of the evidence record. Always err towards showing the real, raw data. 
Axes are honest, never truncated or stretched to amplify or flatten an effect, and never touched with another editor. 
Panels sharing an axis share its range. No 3D charts for 2D data. Be wary of bar charts, pie charts and heat maps for continuous data. 

Two ways to quantify integrity:

**Lie factor.** How much the graphic exaggerates or hides the real effect:

$$\text{lie factor} = \frac{\text{size of effect shown in the graphic}}{\text{size of effect shown in the data}}$$

An honest figure has $$\text{lie factor} \approx 1$$. Heatmaps are a common offender: a color scale can magnify differences. See [how a heat map can fool you](https://tywkiwdbi.blogspot.com/2013/02/how-you-can-be-fooled-by-heat-map.html?m=0).

**Data-to-ink ratio.** What fraction of the graphic is actually carrying information:

$$\text{data-to-ink} = \frac{\text{ink used to convey data}}{\text{total ink used in the graphic}}$$

Ink that isn't carrying information is noise, push this ratio toward 1. Cut the chart junk; spend ink deliberately to raise the signal. See [this data-ink ratio explainer](https://medium.com/@vaniv7397/data-ink-ratio-fcad209ef425).

### 5 · Every figure stands on its own

Axes carry quantity *and* units. Sample size and test appear on the figure or in the caption. 

The caption's first sentence states the figure's core takeaway. 
Then it describes what each panel shows, what symbols and colors encode, *n*, test. You must name the error bars by statistic: SD, SEM, 95% CI, combined measurement uncertainty, or spread across individuals. 

### 6 · Use color intentionally, consistently, and accessibly

<aside class="marginnote marginnote--warn" markdown="1">
[8% of men and 0.5% of women are colorblind](https://www.colourblindawareness.org/colour-blindness/).
In a male-dominated field, assume a meaningful share of your audience is colorblind.
</aside>

Default to colorblind-safe palettes and verify with a simulator.
Viridis, Okabe-Ito, and ColorBrewer safe sets all work. 
Colors must be consistently used across all figures in a paper.

### 7 · Keep typography and layout calm

Use one clean sans-serif font; consistent hierarchy; clean axes. Whitespace is structural. Align panels on organized grids. This
[multi-panel module from UBC](https://github.com/flightlab/MultiPanelPlotsWithR) helps with aligned multi-panel layouts in R.

## Figure checklist

### Start with judgment calls

- What is the one sentence I'd want a reader to say after three seconds with this figure?
- Does every panel contribute to that same takeaway? Could I delete one without weakening it?
- Would a reader who only looked at the figure draw the same conclusion as one who only read the result?
- If a reviewer flipped here first, would they know what was measured, how, and what happened?
- Does the caption's first sentence say what my abstract says about this result?
- In grayscale, or a red-green colorblind simulation, can every distinction still be read?
- Does any visual element pull my eye somewhere that doesn't serve the takeaway?
- If I lost the figure file tomorrow, could I rebuild it by running one script on the raw data?

### Tier 1 · The figure does its job

- There is one takeaway in the figure and the caption's first sentence states it.
- The figure can be understood without the main text.
- The figure is referenced in the main text beside the claim it supports. It is not narrated (see [how to write about figures]({{ '/lab-guide/writing-papers/' | relative_url }}#core-principles)).
- All axes are labeled with quantity and units; ticks are readable at print size.
- Shared axes use the same range and ticks; the axis label and numbers are not repeated unnecessarily.
- No axis is truncated or stretched in a way that changes how the trend reads.
- The sample size, *n*, and test are listed on the figure or in the caption.
- The caption names the error bars by statistic (SD, SEM, 95% CI, measurement uncertainty, biological spread).
- The legend(s) explain all encoded meaning in colors, shapes, sizes, or transparencies.
- Raw data is shown for continuous variables. 
- Bar charts, pie charts, and heat maps are well justified; no 3D plots for 2D data.
- No decorative chart junk unless it is conveying useful information (no full box, verify cross-hatching or shadows).
{: .checklist}

### Tier 2 · Readable by everyone

- Colorblind-safe palette, verified with a simulator.
- Color carries information, avoid using for decoration.
- Color is used consistently throughout all figures.
- Contrast checked, especially for printed figures.
- One sans-serif font throughout; text size consistent across figures and readable at print size.
- Significant digits in labels match the precision of the underlying data.
{: .checklist}

### Before it leaves your hands

- Generated entirely from code, with no manual edits hidden in Illustrator (unless they are minor decorative changes that do not touch the data).
- Panels aligned programmatically (do not align by hand); no misaligned labels or axes.
- Raw data versioned; script in the repo, named per figure.
- Journal requirements met; final file vector or ≥500 DPI PNG.
{: .checklist}

## Tools {#tools}

### Adobe Illustrator (or similar open source tools)

Use it for manuscript-final layout only: assembling non-axis based code-output panels, nudging
alignments, resizing to journal requirements. Lock aspect ratio when resizing and don't ungroup data elements.
**Never** adjust axes, labels, or data values in Illustrator.

### Lab R theme (ggplot2)

This theme sets up your canvas for plotting with ggplot2. It requires the
[`ggthemes`](https://jrnold.github.io/ggthemes/) package for `geom_rangeframe()`.

<div class="callout callout--warn" markdown="1">
This theme removes the axis lines (`axis.line = element_blank()`), so you must add
them back per plot with five extra lines: `geom_rangeframe()` plus two `annotate()`
segments, and the four axis-limit variables they use. Without them your plot will
have no axes.
</div>

<details class="guide-details" markdown="1">
<summary>Show the ggplot2 theme code and a worked example</summary>

```r
library(ggplot2)
library(ggthemes)   # provides geom_rangeframe()

th <- theme_classic() +
  theme(
    axis.title = element_text(size = 10),
    axis.text  = element_text(size = 10, colour = "black"),
    axis.text.x = element_text(margin = margin(t = 10, unit = "pt")),
    axis.text.y = element_text(margin = margin(r = 10)),
    axis.line = element_blank(),
    axis.ticks.length = unit(-5, "pt"),
    legend.position = "none",
    panel.background = element_rect(fill = "transparent"),
    plot.background  = element_rect(fill = "transparent", color = NA)
  )
```

```r
min_x_axis <- 0
max_x_axis <- 100
min_y_axis <- 0
max_y_axis <- 100

plot_example <- ggplot() +
  geom_point(data = dat_example, aes(x = testx, y = testy)) +
  th +
  scale_x_continuous(name = "Test (unit)") +
  scale_y_continuous(name = "Test (unit)") +
  geom_rangeframe() +
  annotate(geom = "segment", x = min_x_axis, xend = min_x_axis, y = min_y_axis, yend = max_y_axis) +
  annotate(geom = "segment", x = min_x_axis, xend = max_x_axis, y = min_y_axis, yend = min_y_axis)
```
</details>

If you improve the theme, share your update with the lab.

## Resources

- [Ten Simple Rules for Better Figures](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003833): the standard reference.
- Tools: [BioRender (UC Davis)](https://app.biorender.com/portal/uc-davis), [ggplot2](https://ggplot2.tidyverse.org/).
- Color: [Datawrapper on color](https://www.datawrapper.de/blog/colors), [Coblis simulator](https://www.color-blindness.com/coblis-color-blindness-simulator/), [WhoCanUse](https://whocanuse.com/).
- Inspiration: [What's Going On in This Graph? (NYT)](https://www.nytimes.com/column/whats-going-on-in-this-graph), [FlowingData](https://flowingdata.com/).
