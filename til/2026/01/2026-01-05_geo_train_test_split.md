# TIL: Geographic train/test splits are essential for honest geospatial ML evaluation

_Date: 2025-01-05_


**Today I learned** that random train/test splits can significantly overestimate performance in geospatial machine learning tasks.

Nearby locations often share:
- similar land-use patterns,
- similar building styles,
- similar imaging conditions.

Random splits therefore allow spatial leakage between training and test data. Models appear to perform well, but fail when applied to new regions.

A more realistic evaluation strategy is to:
- train on some municipalities or regions,
- test on different municipalities or regions.

Although this usually lowers headline metrics, it provides a much more honest assessment of **spatial generalization**, which is critical for real-world deployment.

See full [case study](../../../notes/case-studies/2026-01-05-school_detection_from_satellite_imagery.md).