---
title: "Spatial in R: sf — beginner caveats"
date: 2025-08-01
tags: [r, sf, geospatial, crs, s2]
---

**TL;DR**
- Get your **CRS** right before measuring areas/distances; reproject to an **appropriate projected CRS** first.
- Know when **sf** uses **s2** (spherical) vs **GEOS** (planar) and how that changes results.
- Keep geometries **valid** and **precise** to avoid slivers and odd overlays.

## 1. CRS & units
- Never compute area/distance/buffer in raw **EPSG:4326** (lon/lat). Transform first:
  ```r
  x_proj <- sf::st_transform(x, 3857)  # example; pick a local equal-area/UTM CRS for your region
  sf::st_area(x_proj)                  # returns units (e.g., m^2); convert with units::set_units()
  ```
- Check assumptions quickly: `sf::st_is_longlat(x)` or `sf::st_crs(x)`; print the bbox.

## 2. s2 vs GEOS in sf
- `sf` uses **s2** for geographic CRS by default. Some operations (e.g., `st_intersection`, `st_buffer`) can differ from planar GEOS.
  ```r
  sf::sf_use_s2()       # see current
  sf::sf_use_s2(TRUE)   # enable (default)
  sf::sf_use_s2(FALSE)  # force planar (after transforming to projected CRS)
  ```
- Rule of thumb: **transform + planar** for buffers/areas; **s2** is great for long-distance great-circle logic.

## 3. Validity & precision
- Invalid rings/self-intersections cause weird results; always clean:
  ```r
  x <- lwgeom::st_make_valid(x)
  x <- sf::st_set_precision(x, 1e-8) |> lwgeom::st_make_valid()
  ```
- Coerce consistent types before joins/overlays: `st_cast(x, "MULTIPOLYGON")` etc.

## 4. Performance with sf
- Prefer **GeoParquet/Feather** over GeoJSON/CSV for speed.
- Clip early with coarse **bbox** to shrink data:
  ```r
  bbox <- sf::st_as_sfc(sf::st_bbox(window_poly), crs = sf::st_crs(window_poly))
  pts_small <- sf::st_filter(pts, bbox)  # fast prefilter
  ```

## 5. Axis order & coordinates
- Be explicit when building points from columns:
  ```r
  pts <- sf::st_as_sf(df, coords = c("lon", "lat"), crs = 4326, remove = FALSE)
  ```
- If a dataset used `lat,lon` by mistake, your bbox will look flipped—always sanity-check `st_bbox(pts)`.

## 6. Buffers & distances
- Choose a CRS whose **units align** with your intent. For a 500 m buffer, use a meter-based CRS (e.g., UTM); then:
  ```r
  x_m <- sf::st_transform(x, 31983)  # example CRS; pick one that suits your region
  ring <- sf::st_buffer(x_m, dist = 500)
  ```

## 7. Simplify for plotting
- For web/plots, simplify lightly to speed rendering (don’t simplify data you’ll analyze):
  ```r
  x_simpl <- lwgeom::st_simplify(x_proj, dTolerance = 50)  # meters if CRS in meters
  ```

## 8. Joining attributes safely
- Spatial join then **select** only what you need; beware of duplicated rows after many-to-many joins:
  ```r
  joined <- sf::st_join(pts_small, polys, left = TRUE)
  dplyr::count(joined$poly_id)  # check multiplicities
  ```

**Good defaults to remember**
- Keep raw data in **EPSG:4326**, compute in a **projected CRS**, and render back in 4326 if needed.
- Validate geometries after any union/buffer/overlay.
