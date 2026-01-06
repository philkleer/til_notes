# TIL: Point labels are often better suited for *site detection* than for segmentation

_Date: 2026-01-05_

**Today I learned** that when the only reliable labels available are **points** (for example, a CSV of school locations), framing the problem as **site detection** is often more appropriate than forcing a semantic segmentation task.

Semantic segmentation requires pixel-level ground truth masks, which point data cannot provide directly. In contrast, point labels naturally support a **binary classification** formulation:

> *Is there a school site within this surrounding area?*

By extracting **contextual image patches** around each point (e.g. covering 300–600 meters), a model can learn higher-level spatial patterns such as building clusters, courtyards, or sports fields. These contextual cues are often more informative than the appearance of individual buildings.

This approach is faster to bootstrap, more robust to label noise, and often generalizes better geographically than footprint segmentation derived from weak or inferred polygons.

See full [case study](../../../notes/case-studies/2026-01-05-school_detection_from_satellite_imagery.md).