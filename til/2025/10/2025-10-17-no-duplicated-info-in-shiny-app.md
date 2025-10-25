# TIL: Avoiding duplicated information in Shiny graphics exports
_Date: 2025-10-17_

## Context
In one of our web portals, plots created in Shiny included both:
- UI selectors (e.g., Region or other aggregations)
- The same text repeated in the plot title, subtitle or caption.

This caused **information duplication** — users saw the same labels twice or even three times.

## Solution
I restructured the rendering logic so that:
- The **on-screen plot** only shows essential titles (no repeated selectors).
- When **exporting** the plot (e.g., PNG or PDF), the system dynamically adds the contextual info (subtitle + data source).

## Implementation
- Added a **JavaScript input binding** that detects when the user triggers a download.
- The backend appends only the needed info (`subtitle`, `source`) at render time.
- The live app remains clean and readable; exports stay self-contained.

## Outcome
- Cleaner on-screen visuals.
- Consistent, informative exported images.
- Improved UX — users focus on data, not repeated labels.

## Lessons Learned
- Always think about **context** vs **presentation**.
- Dynamic labeling for exports keeps both app and outputs elegant.

## Where you can see it: [Portal OBIA](https://obia.nic.br/s/indicadores)