# Case Study: School Detection from Satellite Imagery

## Context and Motivation

Educational infrastructure mapping is a recurring challenge in geospatial analysis, particularly in regions where authoritative spatial datasets are incomplete, outdated, or inconsistent. While some information exists in volunteered geographic information sources (e.g., OpenStreetMap) or administrative records (e.g., school registries), these sources rarely provide complete, spatially precise footprints.

This project explores **school detection from satellite imagery** using a combination of:
- weak supervision from OpenStreetMap (OSM),
- authoritative but sparse point data (CSV of school locations), and
- modern foundation models (GeoSAM) for geometry extraction.

The goal is not only to build a model, but to reason carefully about **problem formulation, label engineering, and trade-offs** in geospatial machine learning.

## Problem Framing

Two related but distinct tasks were considered:

1. **School site detection** (binary classification)
   - *Question:* “Is there a school site at or near this location?”
   - Output: probability surface or candidate locations

2. **School footprint segmentation** (semantic segmentation)
   - *Question:* “Which pixels belong to a school campus or buildings?”
   - Output: raster mask with per-pixel class labels

After evaluating data availability and task complexity, **school site detection** was chosen as the primary task, with footprint segmentation treated as a potential downstream refinement.

**Rationale:**
- Available labels are point-based (CSV), not polygons
- School identity is often contextual (buildings + yards + sports fields)
- Detection is faster to bootstrap and more robust across regions

## Data Sources

### Satellite Imagery
- High-resolution satellite imagery
- Used as the sole model input

### School Registry (CSV)
- Point locations (latitude/longitude)
- High semantic confidence ("this is a school")
- No geometric footprint information

### OpenStreetMap (OSM)
- Roads (`highway=*`)
- Buildings (`building=*`)
- Occasionally schools (`amenity=school`)

OSM is treated as **weak supervision**: useful at scale, but incomplete and biased.

## Workflow A: School Site Detection (Binary Classification)

### 1. Dataset Construction

**Positive samples**
- All known school points
- Extract image patches centered on each point

**Negative samples**
- 3–5× as many as positives
- Sampled away from known schools
- Avoid areas near OSM `amenity=school` to reduce label noise

**Patch size**
- Designed to capture *context*, not just buildings
- Target coverage: ~300–600 meters
- Example: 3 m/pixel imagery → 128×128 to 256×256 patches

### Optional: Contextual Features via GeoSAM

GeoSAM is used as a **feature generator**, not a label source:
- number of segments in a patch
- segment size distribution
- presence of large rectangular open areas (sports fields)
- building-like segment density

These features encode spatial structure that may be difficult for shallow models to learn from raw pixels alone.

### 2. Model Training

- CNN-based image classifier (Python)
- Pretrained backbone (e.g., ResNet / EfficientNet)
- Binary output: school vs non-school

### 3. Geographic Evaluation

Instead of random splits:
- Train on some municipalities
- Test on different municipalities

This explicitly tests **spatial generalization**, which is critical in geospatial ML.

### 4. Inference

- Sliding window prediction across imagery
  *or*
- Candidate-based sampling (e.g., near settlements)

Output:
- school likelihood map
- ranked candidate locations for validation

### 5. OSM-based Post-processing

To reduce false positives:
- filter detections far from roads
- filter areas with very low building density

These heuristics encode simple real-world constraints.

## Workflow B: School Footprint Segmentation (Alternative / Extension)

For cases where pixel-level footprints are required, a supervised segmentation workflow was designed.

### Label Engineering

1. **Base layers**
   - OSM roads → raster mask
   - OSM buildings → raster mask

2. **CSV-guided GeoSAM labeling**
   - Crop windows around school points
   - Run GeoSAM within each window
   - Select and label segments as `school`

3. **Mask merging with priority rules**

```
Priority: school > building > road > background

0 = background
1 = road
2 = building
3 = school
```

The result is a standard semantic segmentation label raster aligned to the imagery.

## Key Design Decisions and Trade-offs

| Decision                  | Rationale                                                           |
|---------------------------|---------------------------------------------------------------------|
| Detection vs segmentation | Detection better matches point labels and contextual semantics      |
| OSM as labels             | Scalable but noisy; used as weak supervision                        |
| GeoSAM usage              | Geometry extraction and feature generation, not automatic semantics |
| Geographic splits         | Prevents over-optimistic evaluation                                 |

## Lessons Learned

- Label engineering is often the hardest part of geospatial ML
- Points, polygons, and pixels serve very different roles
- Weak supervision (OSM) can be extremely powerful when used carefully
- Context often matters more than object appearance for place-based classes like schools

## Possible Extensions

- Active learning: label only high-uncertainty regions
- Semi-supervised refinement using model predictions
- Campus footprint refinement using GeoSAM on detected sites

## Summary

This case study demonstrates how combining **authoritative point data**, **volunteered geographic information**, and **foundation models** can produce practical, scalable solutions for real-world geospatial problems — while keeping model assumptions explicit and testable.
