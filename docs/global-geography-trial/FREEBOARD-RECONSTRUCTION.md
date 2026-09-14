# Erde spatial crustal freeboard reconstruction

## Result

The primary crustal/freeboard existence problem is **solved at the required necessary-condition level** for Strategy A.

A 1° material-coordinate crustal mesh can reproduce the present Strategy A land/water partition while:

- closing an Earth-analogue **210.4 million km²** continental-crust inventory without net new continental crust;
- keeping present modeled continental crust between **21 and 42 km** thick;
- keeping maximum authored stretching at **beta = 1.67**;
- reproducing the present land/water sign for all sampled candidate-land and submerged-continental grid cells;
- retaining about **24.6%** of modeled continental crust below present sea level;
- exposing about **16.84 million km²** of additional shallow continental shelf at a -80 m lowstand;
- preserving the required deep-water eastern channels under the -130 m extreme lowstand sensitivity test;
- reproducing distinct H06, H07 and H10 northern-approach states;
- keeping the C4 peripheral corridor and JX1 neck above water in their required states.

No continental silhouette change, Strategy B plate motion, or late continent-scale displacement is required.

This is an **existence reconstruction**, not a unique global palaeogeographic solution and not a high-resolution DEM.

## The problem that was actually solved

The previous plate-block pass established that the six continental bodies and gateway provinces could be assembled with ordinary plate-motion rates, old continental substrate, and no post-1.9 Ma continent-scale repair. It did not establish why roughly 158.6 million km² of the adopted continental crust should be dry land while the rest is submerged, or how shelves should respond through the migration-critical sea-level states.

The freeboard problem therefore had four simultaneous constraints:

1. The current coastline must be reachable with ordinary continental crustal thickness and deformation.
2. The +7.73% dry-land area relative to the bundled generalized reference cannot be explained by creating ~11 million km² of young continental crust.
3. Removed reference-land locations do not automatically have to remain dry or even remain continental at the same coordinates; Erde's breakup and margin history is allowed to differ.
4. Shelf/freeboard states must vary through time. A model in which a -80 to -104 m lowstand produces no additional shelf exposure is not physically adequate even if it matches the present coastline.

## Rejected first freeboard pass

The first executable freeboard model passed its formal thresholds but was rejected during review.

It treated the union of Strategy A land and the generalized source-reference land mask as mandatory present continental crust, then added a small offshore halo to reach the continental-crust inventory. This produced an apparently clean present match but made almost every submerged grid cell too deep. From approximately 18 Ma onward, global emerged area remained unchanged even under -80 to -104 m sea-level states.

That was a **real physical-model failure**: broad continental shelves should respond to a strong lowstand.

The root cause was not the Strategy A coastline. It was a faulty provenance assumption: reference-Earth land had been treated as crust that must remain at the same present coordinate on Erde.

## Natural repair

The corrected model uses the physically appropriate material accounting:

- **Strategy A present land** is the emergent continental core.
- The continental domain is expanded offshore from that core, in projected distance order, until the total reaches **210.4 million km²**.
- The generalized source-reference land mask is retained as a diagnostic of inherited ancestry, not as a mandatory previous Erde coastline or fixed crust coordinate.
- The nearest submerged margins are divided into shallow and outer shelves before deeper extended continental margin.

This permits a changed breakup geometry to redistribute continental crust rather than pretending that candidate and source coastlines are two successive shoreline snapshots of the same stationary crust.

### Present submerged provinces

The final 1° reconstruction contains approximately:

- **16.84 million km²** inner continental shelf, first-order present freeboard about -54 m;
- **13.61 million km²** outer continental shelf, first-order present freeboard about -143 m;
- **14.80 million km²** extended continental margin;
- **6.47 million km²** additional submerged reference-derived platform retained where it naturally overlaps the Erde continental halo.

Total submerged modeled continental crust is about **51.73 million km²**, or **24.6%** of the adopted continental-crust area.

The outer edge of the selected continental domain is at most about **310 km** from Strategy A dry land in the 1° distance representation. This is a continental-margin scale, not an ocean-basin-spanning artificial shelf.

## Crustal provinces

The spatial reconstruction uses ordinary continental end members rather than one universal crustal thickness.

| Province | Present crust | Function |
| --- | ---: | --- |
| Stable interior | 36.5 km | Old craton/platform interiors |
| Stable margin | 33 km | Moderately stretched but emergent margin |
| Old divergent platform | 34 km | Broad Erde-specific inherited platform |
| Reworked margin land | 34 km | Older convergent/reworked continental margin |
| Orogenic belt | 42 km | Shortened/thickened inherited crust |
| JX1 junction | 35 km | Reworked junction province plus later volcanic relief |
| C4 corridor | 34 km | Thickened old foreland/microcontinental substrate |
| C3 southeast shelf head | 31 km | Shallow continental shelf block |
| Inner continental shelf | 29.7 km | Present shallow shelf responsive to late lowstands |
| Outer continental shelf | 29.2 km | Deeper shelf normally flooded during tested lowstands |
| Submerged platform | 27.5 km | Stretched continental platform |
| Extended continental margin | 21 km | Thin continental/transitional margin |
| Small eastern arc blocks | 24 km | Old arc/microcontinental substrate plus volcanic construction |

The range **21–42 km** lies within ordinary extended-to-orogenic continental values and remains distinctly thicker than normal oceanic crust. The maximum stretching factor is **1.67**, well below extreme hyperextension values.

## First-order freeboard physics

The global mesh uses an Airy buoyancy term around a 30 km sea-level reference crust:

`e_Airy = (Tcrust - 30 km) * (rho_mantle - rho_crust) / rho_crust`

with crust density 2800 kg/m³ and mantle density 3300 kg/m³.

This is not treated as a complete elevation law. A bounded residual represents lithospheric mantle buoyancy, flexure, regional loading and other long-wavelength terms because real continental elevation is not uniquely determined by Moho depth. The maximum absolute residual in the authored province set is 1000 m.

Rifted provinces may additionally receive McKenzie-style post-rift thermal subsidence, while collisional provinces thicken inherited crust and the small eastern arc blocks add volcanic construction.

## Time-indexed freeboard behavior

The reconstructed global emerged continental area is not forced to equal the present value through deep time.

The current model gives approximately:

| Epoch | Emerged continental crust | Interpretation |
| --- | ---: | --- |
| 150 Ma | 188.8 Mkm² | Pre-/early-rift higher freeboard; exact shoreline remains highly uncertain |
| 100–30 Ma | 151.9 Mkm² | Major differentiated rift/subsidence configuration |
| 18 Ma | 158.7 Mkm² | Older collision/reworking has raised the required later-emergent provinces |
| 2 Ma | 158.7 Mkm² | Human-route-sensitive rigid geometry complete |
| H06-type -80 m state | 175.5 Mkm² | Inner shelves emerge globally |
| H06-type -90 m state | 175.5 Mkm² | Same resolved inner-shelf class remains exposed |
| H10-type -82 to -104 m states | 175.5 Mkm² | Strong later shelf exposure |
| Present | 158.7 Mkm² on the grid | Matches exact Strategy A land of 158.64 Mkm² to ~0.023% |

The deep-time values are **not precise palaeocoastlines**. The model deliberately does not invent an Erde global eustatic curve for 150–2 Ma. Cells within ±150 m of the long-term datum remain shoreline-uncertain. The important result is that the thickness/deformation history has physically ordinary signs and magnitudes and becomes consistent with the migration-critical late states.

## Critical sub-grid sections

A 1° mesh cannot validate the narrow passages that matter most, so four sections remain explicit.

### JX1

At 3.2 Ma the tested structural ground nodes are 180–320 m above datum. After a 60 m maximum local downward perturbation and +20 m highstand, the weakest tested node retains **60 m** freeboard.

Result: **pass**. Continuous land does not require late continent assembly.

### Northern approach

Founder-scale sill: -70 m plus a -5 m local offset.

H06 tested freeboards: **+5, +30, -30, -45, -10, +15 m**. Multiple founder-scale openings occur, but the full interval is not a permanent bridge.

A slightly shallower -60 m small-contact route gives H07 freeboards: **-70, +3, -3, -73, -10, 0 m**, producing intermittent marginal exposure rather than a continuous highway.

H10 founder-route freeboards: **+7, +21, +33, +29 m**.

Result: **pass**. H06 and H10 remain distinct strong accessibility episodes and H07 remains restricted/intermittent.

### Eastern shelf and islands

At the -130 m extreme lowstand sensitivity test, channel freeboards are still **-180, -290 and -230 m**. The shelf head and stepping islands remain above water.

Result: **pass**. Global shelf expansion does not erase the persistent marine selective environment.

### C4 peripheral corridor

Warm-phase route-node freeboards are **70–310 m**. Under the modeled cold-state sea level plus maximum 60 m local ice-isostatic depression, the seven nodes remain **120–360 m** above water.

Result: **pass** for freeboard. Whether those nodes are climatically productive is a downstream ice/climate question, not an unresolved crust/freeboard question.

## Crustal accounting

The 1° mesh produces:

- continental-domain area: **210.4009 million km²**;
- target: **210.4000 million km²**;
- relative mismatch: approximately **0.0004%**;
- exact Strategy A land: **158.6366 million km²**;
- 1° grid Strategy A land: **158.6726 million km²**;
- grid land-area error: approximately **0.023%**;
- required net new continental crust: **0 km²**.

The +7.73% present dry-land difference from the generalized source mask is therefore a **freeboard and margin-provenance difference**, not evidence of wholesale crust generation.

## Scientific interpretation

The solution uses ordinary mechanisms:

- different inherited breakup geometry;
- crustal stretching and thinning;
- post-rift thermal subsidence;
- collisional shortening/thickening;
- isostatic and lithospheric buoyancy differences;
- sediment accumulation;
- localized volcanic construction;
- glacial/isostatic perturbations;
- eustatic exposure of shallow shelves.

Real Earth analogues establish the available physical space. Published continental-crust inventories place about 210.4 million km², roughly 41% of Earth, over continental crust, with about 31% submerged. Zealandia demonstrates that millions of square kilometres of continental crust can remain submerged following thinning and isostatic adjustment.

## What is now resolved versus downstream

### Resolved

- Is there enough inherited continental crust? **Yes.**
- Does Strategy A require creation of ~11 million km² of new continent? **No.**
- Can ordinary crustal thickness and stretching reproduce dry versus submerged continental provinces? **Yes.**
- Can the surface respond realistically to strong late lowstands? **Yes.**
- Can the response coexist with the required persistent eastern water barriers? **Yes.**
- Can the dated JX1, northern, eastern and C4 freeboard requirements coexist in one model? **Yes.**
- Is another silhouette change or Strategy B required by freeboard? **No.**

### Still downstream, but no longer blockers to crust/freeboard existence

- high-resolution palaeorelief and drainage;
- local backstripping/flexure and geoid corrections;
- explicit C4 ice/climate fields;
- currents, winds and voyage/founder probabilities;
- C3 hydroclimate/contact ecology;
- wildlife and freshwater-clade histories;
- full mantle/dynamic-topography calculation if later regional models expose a residual that ordinary lithospheric mechanisms cannot absorb.

Those models must use this solved plate/crust/freeboard state as their common substrate. They should not independently reshape continents to make a local biological or climatic requirement easier.

## Reproducibility

Primary inputs:

- `plate-block-model.json`
- `freeboard-model.json`
- regenerated `candidate-geography.geojson`
- regenerated `design-controls.json`
- regenerated `measurements.json`

Validator:

`python scripts/editorial/validate_erde_freeboard.py`

Generated evidence:

- `freeboard-validation-metrics.json`
- `freeboard-grid.jsonl`

The validation is run after Strategy A regeneration, dated constraints, physical tests, geological audit, paleolatitude replay and plate-block validation in the repository CI workflow.
