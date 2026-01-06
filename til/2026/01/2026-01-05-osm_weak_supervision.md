# TIL: OpenStreetMap is powerful weak supervision—but it teaches what is *mapped*, not what *exists*

_Date: 2026-01-05_

**Today I learned** that training models with OpenStreetMap (OSM) data introduces an important and often overlooked bias: models tend to learn **what humans have mapped**, not necessarily **what is present in the real world**.

For example:
- roads and buildings are usually well covered and geometrically reliable,
- schools (`amenity=school`) are often incomplete, inconsistently tagged, or represented only as points.

As a result, OSM works best as **weak supervision**:
- excellent for infrastructure geometry and context,
- risky as a sole semantic authority for point-of-interest classes.

The most effective strategy is to combine OSM with **authoritative datasets** (such as official school registries) and treat OSM as contextual guidance rather than ground truth.

See full [case study](../../../notes/case-studies/2026-01-05-school_detection_from_satellite_imagery.md).