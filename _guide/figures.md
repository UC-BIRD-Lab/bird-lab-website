---
title: Figures
category: Writing & Dissemination
order: 4
summary: The lab's figure standards, a self-diagnosis checklist, and tools and palettes.
keywords: [figures, plots, graphics, illustrator, ggplot, visualization, charts, color]
icon: "🎨"
reviewed: 2026-07-05
---

<aside class="marginnote" markdown="1">
This is the figure-side companion to
[First drafts]({{ '/lab-guide/first-drafts/' | relative_url }}).
This page is continually evolving; please suggest new resources or tips.
</aside>

<div class="guide-glance">
<div><span class="k">Jump to</span><a href="#non-negotiables">The non-negotiables</a> · <a href="#core-principles">Core principles</a> · <a href="#figure-checklist">Figure checklist</a> · <a href="#lab-r-theme-ggplot2">Lab R theme</a></div>
</div>

A figure is usually the first thing a reviewer sees and the last thing a reader
remembers. A figure that needs the body text to be understood has failed; one that
lands its takeaway at a glance does most of your argument's work for you. The lab's
[communication framework]({{ '/lab-guide/presentations/' | relative_url }}#core-principles)
applies at the level of a single graphic: maximize signal-to-noise in every figure.

Good figure design isn't decoration, it's part of being precise about what your data
show. Plus, graphic design is pretty fun and a good way to bring creativity into
academia.

<div class="callout callout--stop" markdown="1" id="non-negotiables">
**Lab policy, the non-negotiables**

- Every figure is generated end-to-end from code (R or Python). No data manipulation in Illustrator.
- The generation script lives in the manuscript repository, clearly named per figure, with raw data versioned.
- All figures are vector (PDF / EPS / SVG) or ≥500 DPI PNG.
- All figures use a consistent, colorblind-safe palette.
- Final figures meet the target journal's requirements (size, fonts, DPI, panel-label style).

These exist so any figure can be checked and rebuilt, by reviewers, collaborators,
or future you.
</div>

## The figure development cycle

<aside class="marginnote" markdown="1">
**Clarity beats prettiness.** A figure that lands its takeaway in three seconds
with ugly defaults beats a beautiful one whose point you have to hunt for. Style is
the last pass, not the first.
</aside>

1. **Sketch:** decide the takeaway and rough layout before any software.
2. **Rough plot:** ugly but functional; look at the data every reasonable way.
3. **Refine structure:** lock layout, panel order, axis ranges, labeling.
4. **Apply styling:** colors, typography, annotation (the fun part, but *last*).
5. **Review and revise:** show it to a colleague *without* the caption and ask their three-second takeaway. If it doesn't match yours, it isn't done. (On asking for and taking critique, see [giving and receiving feedback]({{ '/lab-guide/communication/' | relative_url }}#giving-and-receiving-feedback).)

Most "beautiful" published figures go through 10–20 iterations. (No, Christina is not exaggerating.)

## Core principles {#core-principles}

### 1 · Plan the figure before you open software

<aside class="marginnote" markdown="1">
🔍 **Ask yourself:** what is the one sentence I'd want the reader to say after looking at this figure for three seconds?
</aside>

Decide what the figure must say
first, then choose the format that says it. Before plotting, answer: what is the
major point, who is the audience, what figure *type* fits, and which elements are
essential vs. optional. For major journal articles and any complex multi-panel
figures, run a storyboard session with Christina before you write plotting code.

### 2 · One message per figure

<aside class="marginnote" markdown="1">
🔍 **Ask yourself:** does every panel contribute to the same takeaway? Could I delete a panel without weakening the main point?
</aside>

A figure with two takeaways usually delivers
neither. Multi-panel figures are good when panels build a single argument together;
not when they bundle unrelated results to save space.

### 3 · Every figure stands on its own

<aside class="marginnote" markdown="1">
🔍 **Ask yourself:** if a reviewer flipped to this figure first, would they know what was measured, how, and what the result is, without the body text?
</aside>

The first sentence of the caption restates
the takeaway, not the chart type. Axes are labeled with quantity *and* units;
sample size, test, and error-bar meaning appear on the figure or caption.

### 4 · Show the data honestly

<aside class="marginnote" markdown="1">
🔍 **Ask yourself:** would a reader who only looked at the figure draw the same conclusion as a reader who only read the result?
</aside>

The figure is part of the evidence record, not a
sales pitch. Prefer raw points (with a spread summary) over bar charts for
continuous data. Axes are honest, never truncated or stretched to amplify or
flatten an effect, and never adjusted by dragging in Illustrator. Panels sharing an
axis share its range. Define what error bars represent. No 3D charts for 2D data.

Two ways to quantify integrity:

- **Lie factor** = size of effect shown in the graphic ÷ size of effect shown in the data. A value far from 1 means the graphic exaggerates (or hides) the real effect. Heatmaps are a common offender: a color scale can invent a difference the data don't support. See [how a heat map can fool you](https://tywkiwdbi.blogspot.com/2013/02/how-you-can-be-fooled-by-heat-map.html?m=0).
- **Data-to-ink ratio** = ink used to convey data ÷ total ink used in the graphic. Ink that isn't carrying information is noise. Cut the chart junk; spend ink deliberately to raise the signal. See [this data-ink ratio explainer](https://medium.com/@vaniv7397/data-ink-ratio-fcad209ef425).

> *Example:*
> ❌ A bar chart of group means with no error bars, y-axis from 9.8 to 10.1.
> ✅ A strip plot of all data points overlaid with mean ± 95% CI; full y-axis range from 0.

### 5 · Use color intentionally, consistently, and accessibly

<aside class="marginnote marginnote--warn" markdown="1">
[8% of men and 0.5% of women are colorblind](https://www.colourblindawareness.org/colour-blindness/).
In a male-dominated field, assume a meaningful share of your audience is colorblind.
</aside>

<aside class="marginnote" markdown="1">
🔍 **Ask yourself:** in greyscale or a red-green colorblind simulation, could the reader still read every distinction?
</aside>

Default to
colorblind-safe palettes (viridis, Okabe-Ito, ColorBrewer safe sets) and verify
with a simulator. Don't rely on color alone; pair with shape or line style.
Categorical colors must match across all figures in a paper.

### 6 · Keep typography and layout calm

<aside class="marginnote" markdown="1">
🔍 **Ask yourself:** does any visual element pull my eye somewhere that doesn't serve the takeaway?
</aside>

One clean sans-serif font; consistent
hierarchy; clean axes (no full box, no cross-hatching, no shadows). Whitespace is
structural. Align panels on a grid. Minimize chart junk (see principle 4). This
[multi-panel module from UBC](https://github.com/flightlab/MultiPanelPlotsWithR)
helps with aligned multi-panel layouts in R.

### 7 · Generate every figure from code

<aside class="marginnote" markdown="1">
🔍 **Ask yourself:** if I lost the figure PDF tomorrow, could I rebuild it identically by running one script on the raw data?
</aside>

The figure is built end-to-end in R or
Python; raw data is versioned (FigShare on publication); preprocessing lives in
scripts. The script outputs the *final* figure file. Name it clearly per figure
(e.g., `fig2_lift_vs_alpha.R`).

### 8 · The caption carries the takeaway

<aside class="marginnote" markdown="1">
🔍 **Ask yourself:** does the caption's first sentence say the same thing my abstract says about this result?
</aside>

Its first sentence states the takeaway in
the same words as the abstract; then the mechanics (what each panel shows, what
symbols/colors encode, error bars, *n*, test). Keep mechanics out of the body text.

## Working in Adobe Illustrator

Manuscript-final layout touch-ups (assembling code-output panels) are fine if used
carefully. Lock aspect ratio when resizing; don't ungroup data elements; **never**
adjust axes, labels, or data values in Illustrator; those changes go back to the
script. Restrict edits to layout only.

## Figure checklist

### The takeaway

- One takeaway, statable in one sentence; caption's first sentence states it.
- Referenced in the body text with a note on *what to notice*.
{: .checklist}

### Standing alone

- Axes labeled with quantity and units; ticks readable at print size.
- *n*, test, and error-bar meaning on the figure or in the caption.
- Legend wherever the encoding isn't self-evident.
{: .checklist}

### Data integrity

- Axes honest; shared axes use the same range and ticks.
- Error bars defined; raw data shown for continuous variables.
- No 3D plots for 2D data; no decorative chart junk.
{: .checklist}

### Color and accessibility

- Colorblind-safe palette, verified with a simulator.
- No information encoded by color alone.
- Categorical colors match across all figures.
- Contrast checked, especially for printed figures.
{: .checklist}

### Typography and consistency

- One sans-serif font throughout; consistent hierarchy across all figures.
- Panels align on a grid; no misaligned labels or axes.
- Significant digits in labels match the precision of the underlying data, no more.
{: .checklist}

### Reproducibility and compliance

- Generated entirely from code; raw data versioned; script in the repo, named per figure.
- Journal requirements met; final file vector or ≥500 DPI PNG.
{: .checklist}

## Signs your figure will come back

The first four are **major**; they affect whether the figure does its job. The rest
are **fixable style issues**: clean them up, but don't mistake them for the hard part.

<div class="callout callout--stop" markdown="1">
**Major, fix before sending**

- The figure has more than one takeaway, or no clear takeaway at all.
- The figure cannot be understood without the body text.
- Axes are truncated, stretched, or otherwise distorted in a way that changes how the reader reads the trend.
- The figure is not reproducible from code (manual edits hidden in Illustrator).
</div>

<div class="callout" markdown="1">
**Style-level**

- Color used decoratively or inconsistently across figures.
- Categorical colors that don't match the grouping used in the body text.
- Text too small or varying across figures.
- Inconsistent axis ranges across panels that should share a scale.
- Too many significant digits in tick labels.
- Misaligned panels.
- Bar charts where points-with-spread would tell the story better.
- No annotation guiding the reader to the key point.
</div>

## Lab R theme (ggplot2)

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
