# Erde atlas projection update

## Decision and scope

Replace the five public Erde geographic sheets with **Equal Earth**, a pseudocylindrical equal-area projection. The contact sheet uses a regional crop of the same projection. This preserves relative areas while giving a balanced global view of shapes. It does not preserve all local angles, shapes, distances or bearings. No flat projection can do all of those things simultaneously.

Technical reference: [PROJ Equal Earth documentation](https://proj.org/en/stable/operations/projections/eqearth.html). Public text calls this an “equal-area view” so the guide continues to describe Erde on its own terms. The projection’s technical name is authorial terminology, not an in-world name.

The established native coordinate frame, geographic inputs and all mapped feature locations are retained. Continental and inhabitant name proposals remain undecided. The original authorial SVGs retain their historical geometry; their old public URLs resolve to the updated public artwork. Dverghamar’s distinct geographic and process diagrams are outside this change.

## Plan and issue review

| Evaluation | Root cause and chosen fix | Re-evaluation |
| --- | --- | --- |
| High-latitude areas enlarged on the old rectangular maps | Equirectangular projection; regenerate geographic vectors with Equal Earth | Numerical area checks span the equator, poles and outer meridians; no raster stretching |
| A projection change could detach labels, routes or numeric markers from land | Several original artists relied implicitly on the old degree-valued plotting axes | Apply explicit native-coordinate transforms to markers and text; project all map layers consistently |
| Long polar lines and arrow shafts could imply incorrect connections | Connecting widely separated native longitudes with straight segments; drawing a second shaft for the final arrow | Interpolate schematic range/route segments along spherical geodesics; draw one route with a tangent-aligned arrowhead |
| Curved map boundaries lost most automatic latitude labels | Rectangular-edge grid-label placement did not suit global curved boundaries | Place global latitude labels at their projected boundary positions; retain normal grid labeling in the regional crop |
| Projection regeneration could depend on transient files or downloads | Original generator and geographic source bundle lived outside the repository | Commit renderer, pinned authoring dependencies and the original Natural Earth 110m land geometry as authorial GeoJSON |
| Existing explanatory text described the old projection | Public and authorial methods had no version distinction | Update public guidance and explicitly scope the historical authorial explanation to the original sheets |
| Reader presentation needed another check | Label positioning changes after projection | Inspect all five sheets, reposition the polar highlands label, and remove a duplicated “ancestral” label |

## Implementation

- `scripts/editorial/erde_geometry.py`: reproducible Cartopy/PROJ renderer with one spherical globe and explicit transforms. Geographic reference points remain authorial inputs. Coastlines are rotated into the established native frame before the new display projection.
- `scripts/editorial/prepare-erde-atlas.py`: public terminology, SVG accessible titles/descriptions, stable map identities and public atlas links.
- `scripts/editorial/data/reference-land.geojson`: bundled Natural Earth land v4.1.0, preserving the source used by the existing atlas. Attribution and public-domain terms are recorded alongside it.
- Generated public SVGs remain publication inputs. Normal website builds require Node only; no GIS download or map rendering occurs during deployment.

## Validation

- Three numerical test groups pass: selected poles and six independent latitude/coordinate round trips; 56 spherical rectangles preserve analytic area within 0.001%; finite polar behavior, inverse projection and curved high-latitude boundary checks.
- All five publication tests pass, including internal links, public terminology, legacy SVG parity and separation of authorial naming proposals.
- All twelve browser tests pass, including the Erde atlas in light/dark themes at 1440, 390 and 320 px, keyboard navigation and automated WCAG checks.
- All five SVGs visually reviewed for coastline continuity, map-edge clipping, legends, graticules, labels and overlays. Final arrowheads follow the plotted route rather than adding a second route line.

The remaining limits are intrinsic or already documented: global maps retain local shape distortion, schematic mountains/routes are not surveys, and the original coastline scaffold is not a reconstructed high-resolution terrain model. No additional projection-related issue remains open after these checks. Deployment is verified through the GitHub Actions run attached to this commit.
