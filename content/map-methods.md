# Erde and the Dwarven Planet: map guide

This guide reproduces the 13 SVG sheets from the existing atlas. The original printable atlas contains 15 pages. Captions and the following methods describe the source maps and their limitations.

## Reading the maps

- **Selected geometry:** the accepted planetary orientation and the mathematical coordinate transformation.
- **Scenario target:** accepted but quantitatively unvalidated climate, ecological, or historical parameters.
- **Schematic placement:** invented locations, paths, shapes, and section dimensions used to explain established relationships.

Each map identifies its status. Regional examples do not silently create new canonical continents, settlements, rivers, species territories, or exact migrations. No political borders have been invented.

## Map index

| Sheet | World | Purpose | Source scope |
| --- | --- | --- | --- |
| E1 | Erde | Compare Earth reference coastlines with their mathematical rotation into Erde's selected spin frame. | 33; 38; Natural Earth land |
| E2 | Erde | New-latitude forcing bands with reference sites; separates geometric constraints from unmodeled regional climates. | 33; 38; Natural Earth land |
| E3 | Erde | An approximate mountain and passage scaffold for planning isolation, rain shadows, and migration. | 20; 24; 33; 38; modern reference mountain axes |
| E4 | Erde | Locate the selected African ancestry, Sunda radiation, Sahul branch, and early American migration without inventing political borders. | 33; 38 |
| E5 | Erde | Defined-epoch map of the five First American regional complexes and the northern successor outcome. | 33 paragraphs 148-178; 38 |
| D1 | Dwarven Planet | Orthographic views show that the terminator is a great circle, with the provisional habitable envelope around it. | 35 paragraphs 12-40; 38 |
| D2 | Dwarven Planet | Global target-envelope map with thermal ranges and the distinction between photic habitat and a mostly dark fringe. | 35 paragraphs 34-41, 71-78; 38 |
| D3 | Dwarven Planet | A scaled hypothetical sector showing fragmented wet provinces, mountain passes, salt barriers, terminal brines, and large lakes. | 35 paragraphs 37-48; 37 |
| D4 | Dwarven Planet | A process map connecting river catchments and lakes to evaporation, precipitation, ice storage, and conditional slow return. | 35 paragraphs 20, 23, 42-48; 38 |
| D5 | Dwarven Planet | A shared vertical datum makes mountain-city altitude distinct from rock cover and lowland mine depth. | 35 paragraphs 95-107; 38 |
| D6 | Dwarven Planet | Ecological placement of five dwarf species and the deep-massif subspecies, with no invented territorial boundaries. | 35 paragraphs 129-141; 36; 37 |
| D7 | Dwarven Planet | An illustrative site map of hydropower, agriculture, ventilation, transit, and waste flows supporting underground settlement. | 35 paragraphs 88-112; 38 |
| D8 | Dwarven Planet | Compare an oxygenated lake food web above anoxic depths with a chemically powered, isolated subglacial oasis. | 35 paragraphs 44-48, 74-87; 38 |

## Coordinate conventions

### Erde

North points toward Earth-reference latitude 0 degrees, longitude -150 degrees. South points toward its antipode at 0 degrees, +30 degrees. The new latitude is derived from:

`sin(latitude_new) = cos(latitude_old) * cos(longitude_old + 150 degrees)`

New longitude zero passes through the old geographic north pole. This longitude choice is an atlas convention, not an additional canon decision. The RotatedPole coordinate transformation supplies a consistent right-handed frame. `erde-reference-locations.csv` contains both coordinate systems for useful approximate locators.

The original authorial rectangular sheets are equidistant cylindrical in the new frame, not equal-area. The public Erde atlas now uses the Equal Earth equal-area projection; see `docs/ERDE-PROJECTION-REVIEW.md` for the implementation and validation. The following distortion description applies to the retained original sheets. Areas and distances are distorted toward the new poles. The poles themselves have no unique longitude. Modern Earth coastlines are a reference scaffold only. Sea level, erosion, ice, and the independent history would alter actual Erde shorelines. No modern national borders, modern ice-sheet layer, or Earth vegetation layer is transplanted.

E2's 30-degree bands illustrate latitude-related solar forcing under a conventional modest-obliquity scenario. They are not computed biome boundaries or selected tropical/polar circles. Orbital obliquity is separate from the map rotation. E3's mountain paths are approximate regional axes, not surveyed outlines, altitude measurements, or reconstructed plate boundaries.

### Dwarven Planet

Substellar longitude is zero; the opposite meridian is 180 degrees. At ideal zero obliquity, angular distance from the substellar point satisfies `cos(chi) = cos(latitude) * cos(longitude)`. The terminator is the great circle at `chi = 90 degrees`.

With radius 8,919.4 km, the proposed 3,900 km dayward and 600 km nightward distances correspond to about 25.05 and 3.85 degrees from the terminator. The resulting corridor is an envelope for possible habitat, not a continuous productive ring. D2's uniform fills identify broad placement zones; the quoted surface temperatures refer to the central/deep target regions rather than every location sharing a fill color.

D3 is one invented sector unrolled along the ring. Its local planar distances are illustrative and do not determine the planet's basin distribution. Example lake ellipse areas are approximately 105,558, 87,965, and 88,122 km2. D5 uses one shared vertical datum: elevation, local rock cover, and mine depth remain different measurements. Room symbols are deliberately exaggerated for visibility and are not proposed excavation spans. The deep-district example lies under a lowland flank, with about 2 km local overburden, not under the full massif.

D6 is a qualitative ecological placement map. Its horizontal spacing and vertical categories are not measured geography or height. D7 is a hypothetical 20 by 14 km catchment plan; facility symbols and flow widths are not scaled production capacities. D4 and D8 are mechanism/habitat sections without a shared spatial scale.

## Time and ancestry

E4 summarizes selected deep-history dispersal stages on one locator map. Arrows need not be contemporaneous. The early American founding interval is roughly 650-450 thousand years before Erde present. E5 is explicitly about 5,000 years before Erde present, following the later sapiens-like founding movement around 35-20 thousand years ago. These dates belong to the fictional scenario and are not claims about Earth's archaeological record.

At E5's epoch, the Great Watersheds, Volcanic Hinge, Highland Spine, and Equatorial Basin remain self-sustaining population networks. The former Boreal Rim persists through multiple mixed successor populations with substantial ancestral and cultural continuity. Its working name does not make its low-latitude Beringian approaches uniformly boreal.

The Thal catastrophe occurred on Erde. Refugees reached the Dwarven Planet through the Otherworld. No physical orbital adjacency, interplanetary distance, or specific portal location is invented in this atlas. Thals are not part of the native six-limbed dwarf radiation.

## Files in this guide

The [Erde atlas](erde-atlas.html) and [Dverghamar atlas](dverghamar-atlas.html) display the original SVG sheets with text explanations. Each map links to its full-size SVG. The original PDF pack and Python map-generation environment are separate source artifacts, not required to run this website.

[Download the paired Erde reference coordinates (CSV)](data/erde-reference-locations.csv).

## Checks performed

The new pole coordinates, the Bering and Dakar reference latitudes, the kilometer-to-angle conversion, and the map count were checked numerically. Final images were visually inspected for boundaries, clipped labels, and overlap. PNG checksums and PDF page counts were verified. The finished atlas has 15 pages and 13 maps. These checks validate the map construction, not a planetary climate model or an engineering design.

## Sources

- [33: Erde history and decision ledger](erde-reference.html)
- [35: Dwarven scientific canon](dverghamar-reference.html)
- [36: Geological, biospheric, and evolutionary synthesis](evolution-reference.html)
- [37: Open questions and wildlife branching map](wildlife-questions.html)
- 38: Scientific review and validation record (source-project reference; not reproduced here)
- 20: Historical alternate-axis framework (source-project reference; not reproduced here)
- 24: Historical Proposal 4 geology (source-project reference; not reproduced here)
- [Natural Earth 1:110m physical land](https://www.naturalearthdata.com/downloads/110m-physical-vectors/), public-domain cartographic data. Land archive: `https://naturalearth.s3.amazonaws.com/110m_physical/ne_110m_land.zip`.

The unresolved phrase "3-5% of the wet core" is not assigned a spatial layer. The source conversation did not identify its measured quantity.
