# How I build data-driven presentations with Quarto + revealjs (a real-world example)
_Date: 2025-12-17_

I like to treat presentations as **reproducible artifacts**: text and figures come from the same pipeline, numbers are updated automatically, and *storytelling* is guided by a clear structure.

A good example of this is the presentation **Satellite access technologies in Brazilian schools: Distribution, performance, and inequalities** (in portuguese), where I combined **Quarto + revealjs** with graphics and maps generated in R. You can find the presentation (15 minutes) [here](https://philkleer. quarto.pub/ix_forum_2025).

##  What I want to achieve with this style

- **Automatic updating**: numbers and indicators appear on the slide via inline code (`r ...`), avoiding *copying and pasting* statistics
- **Separation of responsibilities**: a script prepares data/figures and the `.qmd` focuses on narrative
- **Visual progression**: I reveal information in stages (*fragments*, *stacks*), keeping the audience with me
- **Reproducibility and traceability**: references, sources, and criteria are documented (bibliography + CSL)

## Narrative structure I use

I almost always organize the deck into four blocks:

1. **Objective**: what question am I answering and why does it matter
2. **Data**: where does it come from, what filters do I apply, and what limitations exist
3. **Analysis**: what metrics, how do I compare, and how do I interpret
4. **Lessons learned / Results**: what can be concluded *today* and what is still missing

This structure appears in revealjs with `data-stack-name` (fourth add-on [simplemenu](https://github.com/martinomagnifico/quarto-simplemenu)), which also helps with navigation (and in the menu when I use plugins).

## Implementation pattern: a script generates the figures, the slide just calls them

In the setup, I prefer to load everything that is necessary and produce the objects (plots/tables) in a separate file:

```r
#| label: setup-libraries-data
#| include: false
#| message: false
#| eval: true
#| cache: true

source("src/visualizations_slides.R")
```

The advantage is that:
- the slide file is cleaner;
- I can reuse visualizations in future versions;
- it is easy to test and review the figures as a separate *product*.

## Visual construction: `columns`, `fragments`, and `r-stack`

### 1) `.columns` for comparison and comfortable reading  
When I need to balance text and figures (or two ideas side by side), I use columns.

### 2) `.fragment` to *reveal* the message  
I use fragments to:
- present context → evidence → implication;
- avoid “crowded” slides;
- control the pace.

### 3) `.r-stack` to show *steps* in the same space  

Perfect for:
- filtering pipeline (before/after),
- variations of the same graph (histogram → density → highlights),
- maps with different layers.

Typical example:

```markdown
:::{.r-stack}
![](imgs/filtering0.png){.fragment .fade-out fragment-index=1}
![](imgs/filtering1.png){.fragment .fade-in-then-out fragment-index=1}
![](imgs/filtering2.png){.fragment .fade-in-then-out fragment-index=2}
:::
```

##  Interactivity when it makes sense (and when it doesn't)

I like to use `{ggiraph}` for maps and explorable graphs during presentations, for example:

- zoom and pan;
- tooltips for areas/locations/values;
- highlight patterns without having to clutter the slide with labels.

**But**: it is always worth having a static *fallback* (PNG) ready, in case the environment/lock/rendering time gets in the way.

**Mas**: sempre vale ter um *fallback* estático (PNG) pronto, caso o ambiente/trava/tempo de render atrapalhe.

## Quality checklist (quick and practical)

Before presenting, I go over these points:

- [ ] **Spelling and consistency**
- [ ] **Consistent units** (e.g., prefer `Mbps` and maintain the same standard throughout the deck)
- [ ] **Visible definitions** (e.g., RTT, limits, MEC rule)
- [ ] **One message per slide** (one slide = one main statement)
- [ ] **Source + method** (explain filters, sample, and decisions such as outlier removal)
- [ ] **Plan B for interactivity** (static image if necessary)
- [ ] Create a *shareable* PDF version with less interactivity and more offline readability

## Why this deck is a good example of my style

It has several elements that I consider fundamental:

- **well-defined history** (Objective → Data → Analysis → Results),
- **data and evidence at the center** (metrics and maps),
- **organized code** (figures centralized in `src/visualizations_slides.R`),
- **controlled progression** (fragments + stacks),
- **formal references** (BibTeX + CSL).
