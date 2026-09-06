# Atlas geometry inputs (authorial)

`reference-land.geojson` is the unmodified Natural Earth 1:110m land geometry (version 4.1.0), converted from the shapefile in the original atlas source bundle. Natural Earth data is public domain: https://www.naturalearthdata.com/about/terms-of-use/ . These reference coordinates are authorial inputs, not public Erde names or countries.

`erde_geometry.py` rotates these inputs into the established Erde frame before projecting them. The rotation is unchanged: north pole at reference 0°, −150°; native longitude zero follows the original atlas convention. The public render keeps all points, mountain lines, routes, and numeric markers in this same native coordinate system.

The source dataset is intentionally bundled: regeneration does not fetch new coastlines or silently change the geography. Shorelines remain the established broad scaffold, not surveyed final regional geography.
