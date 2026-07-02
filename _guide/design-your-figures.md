---
title: Design your figures
category: Writing & Dissemination
order: 2
summary: The lab's figure standards, a self-diagnosis checklist, and tools and palettes.
---

A figure is usually the first thing a reviewer sees and the last thing a reader
remembers. A figure that needs the body text to be understood has failed; one that
lands its takeaway at a glance does most of your argument's work for you. Good
figure design isn't decoration — it's part of being precise about what your data
show. This is the figure-side companion to
[Write a first draft]({{ '/lab-guide/write-a-first-draft/' | relative_url }}).

<div class="callout callout--warn" markdown="1">
**Lab policy — the non-negotiables**

- Every figure is generated end-to-end from code (R or Python). No data manipulation in Illustrator.
- The generation script lives in the manuscript repository, clearly named per figure, with raw data versioned.
- All figures are vector (PDF / EPS / SVG) or ≥500 DPI PNG.
- All figures use a consistent, colorblind-safe palette.
- Final figures meet the target journal's requirements (size, fonts, DPI, panel-label style).
</div>

<div class="callout" markdown="1">
**Clarity beats prettiness.** A figure that lands its takeaway in three seconds
with ugly defaults beats a beautiful one whose point you have to hunt for. Style is
the last pass, not the first.
</div>

## The figure development cycle

1. **Sketch** — decide the takeaway and rough layout before any software.
2. **Rough plot** — ugly but functional; look at the data every reasonable way.
3. **Refine structure** — lock layout, panel order, axis ranges, labeling.
4. **Apply styling** — colors, typography, annotation (the fun part, but *last*).
5. **Review and revise** — show it to a colleague *without* the caption and ask their three-second takeaway. If it doesn't match yours, it isn't done.

Most "beautiful" published figures go through 10–20 iterations.

## Core principles

**1 · Plan the figure before you open software.** Decide what the figure must say
first, then choose the format that says it. Before plotting, answer: what is the
major point, who is the audience, what figure *type* fits, and which elements are
essential vs. optional.

**2 · One message per figure.** A figure with two takeaways usually delivers
neither. Multi-panel figures are good when panels build a single argument together;
not when they bundle unrelated results to save space.

**3 · Every figure stands on its own.** The first sentence of the caption restates
the takeaway, not the chart type. Axes are labeled with quantity *and* units;
sample size, test, and error-bar meaning appear on the figure or caption.

**4 · Show the data honestly.** Prefer raw points (with a spread summary) over bar
charts for continuous data. Axes are honest — never truncated or stretched to
amplify or flatten an effect, and never adjusted by dragging in Illustrator.
Panels sharing an axis share its range. Define what error bars represent. No 3D
charts for 2D data.

**5 · Use color intentionally, consistently, and accessibly.** Default to
colorblind-safe palettes (viridis, Okabe-Ito, ColorBrewer safe sets) and verify
with a simulator. Don't rely on color alone — pair with shape or line style.
Categorical colors must match across all figures in a paper.

<div class="callout callout--warn" markdown="1">
[8% of men and 0.5% of women are colorblind](https://www.colourblindawareness.org/colour-blindness/).
In a male-dominated field, assume a large portion of your audience is colorblind.
</div>

**6 · Keep typography and layout calm.** One clean sans-serif font; consistent
hierarchy; clean axes (no full box, no cross-hatching, no shadows). Whitespace is
structural. Minimize chart junk — if there's ink on your chart, it should convey
information.

**7 · Generate every figure from code.** The figure is built end-to-end in R or
Python; raw data is versioned (FigShare on publication); preprocessing lives in
scripts. The script outputs the *final* figure file. Name it clearly per figure
(e.g., `fig2_lift_vs_alpha.R`).

**8 · The caption carries the takeaway.** Its first sentence states the takeaway in
the same words as the abstract; then the mechanics (what each panel shows, what
symbols/colors encode, error bars, *n*, test). Keep mechanics out of the body text.

## Working in Adobe Illustrator

Manuscript-final layout touch-ups (assembling code-output panels) are fine if used
carefully. Lock aspect ratio when resizing; don't ungroup data elements; **never**
adjust axes, labels, or data values in Illustrator — those changes go back to the
script. Restrict edits to layout only.

## Figure checklist

**The takeaway**
- [ ] One takeaway, statable in one sentence; caption's first sentence states it.
- [ ] Referenced in the body text with a note on *what to notice*.

**Standing alone**
- [ ] Axes labeled with quantity and units; ticks readable at print size.
- [ ] *n*, test, and error-bar meaning on the figure or in the caption.
- [ ] Legend wherever the encoding isn't self-evident.

**Data integrity**
- [ ] Axes honest; shared axes use the same range and ticks.
- [ ] Error bars defined; raw data shown for continuous variables.
- [ ] No 3D plots for 2D data; no decorative chart junk.

**Color and accessibility**
- [ ] Colorblind-safe palette, verified with a simulator.
- [ ] No information encoded by color alone.
- [ ] Categorical colors match across all figures.

**Reproducibility and compliance**
- [ ] Generated entirely from code; raw data versioned; script in the repo, named per figure.
- [ ] Journal requirements met; final file vector or ≥500 DPI PNG.

## Lab R theme (ggplot2)

```r
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

If you improve the theme, share your update with the lab.

## Resources

- [Ten Simple Rules for Better Figures](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003833) — the standard reference.
- Tools: [BioRender (UC Davis)](https://app.biorender.com/portal/uc-davis), [ggplot2](https://ggplot2.tidyverse.org/).
- Color: [Datawrapper on color](https://www.datawrapper.de/blog/colors), [Coblis simulator](https://www.color-blindness.com/coblis-color-blindness-simulator/), [WhoCanUse](https://whocanuse.com/).
- Inspiration: [What's Going On in This Graph? (NYT)](https://www.nytimes.com/column/whats-going-on-in-this-graph), [FlowingData](https://flowingdata.com/).
