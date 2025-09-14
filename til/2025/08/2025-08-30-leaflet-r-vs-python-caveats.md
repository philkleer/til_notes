---
title: "Leaflet in R and Python — beginner caveats"
date: 2025-08-30
tags: [leaflet, r, python, folium, maps, crs]
---

**TL;DR**
- **Coordinate order** trips everyone: Leaflet/folium use **[lat, lon]**, R `leaflet::addMarkers()` often asks for **lng, lat** arguments.
- Keep data in **EPSG:4326** for web maps; reproject from `sf` to 4326 before adding to the map.
- Many points → use **clusters** or **circles**; avoid adding thousands of individual `Marker`s.
- Always include **tile attribution**; some providers need an API key.

## Minimal examples
### R (leaflet)
```r
library(leaflet)
leaflet() |>
  addProviderTiles(providers$OpenStreetMap) |>
  addMarkers(lng = -46.63, lat = -23.55, popup = "São Paulo") |>
  setView(lng = -46.63, lat = -23.55, zoom = 10)
```
- With `sf`:
```r
library(sf); library(leaflet)
pts <- st_as_sf(data.frame(lon=-46.63, lat=-23.55), coords=c("lon","lat"), crs=4326)
leaflet(pts) |> addTiles() |> addCircleMarkers()
```

### Python (folium)
```python
import folium
m = folium.Map(location=[-23.55, -46.63], tiles="OpenStreetMap", zoom_start=10)
folium.Marker(location=[-23.55, -46.63], popup="São Paulo").add_to(m)
m.save("map.html")
```

## Caveats
- **CRS**: Transform `sf` data to 4326 before mapping; Leaflet expects WGS84 degrees.
- **Large data**: Convert polygons to **GeoJSON** and simplify geometry for display; cluster points (`leaflet::addMarkers(clusterOptions = markerClusterOptions())` or `folium.plugins.MarkerCluster`).
- **Popups**: Sanitize HTML; in Python, prefer `folium.Popup(max_width=...)` to avoid overflows.
- **Tiles**: Respect usage limits; keep an eye on dark-mode/readability and bandwidth.
