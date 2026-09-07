# Erde dated continental reconstruction plan

## Current decision

Continue **Strategy A: inherited continental nuclei plus old marginal provinces and dated gateways**.

The bounded analysis has now progressed through four increasingly strict levels:

1. dated historical constraint graph;
2. regenerated structural geometry;
3. regional physical plausibility scenarios;
4. explicit crustal-block / finite-rotation / continental-crust accounting.

All four currently pass their necessary-condition validators. Strategy B has therefore **not** been invoked.

This remains a reconstruction framework rather than a completed geodynamic model. The next escalation is spatial deformation, crustal thickness, and time-indexed palaeoelevation/freeboard, not another coastline redesign.

## Why Strategy A replaced the earlier candidate

The rejected worldwide draft combined a 6° C2 rigid offset with Earth-reference guard sectors. That could preserve a modern route while saying nothing about whether the route existed at H02, H06, H10, or another required historical interval.

Strategy A removed both failure mechanisms:

- C2's extra rigid offset is **0°**;
- sensitive routes are explicit dated reconstruction objects rather than restored reference coastline.

The current model distinguishes old crustal substrate, block motion, deforming boundaries, emergence/submergence, passability, and ecological filtering.

## Geometry retained after validation

### JX1 C1–C2 junction

JX1 remains the preferred C1–C2 solution. The plate-scale pass changes its interpretation, not its visible envelope.

The ~2.96 million km² JX1 surface province is mainly old microcontinental and reworked C1/C2 margin crust. A narrower younger arc/suture system records the 28–12 Ma assembly/reorientation interval. A representative central block reaches its final C1-relative orientation by 12 Ma, while later C1–C2 relative motion is absorbed through an internal deforming transpressional/subduction-transform network.

Continuous terrestrial emergence is modeled by about 3.2 Ma. This separates crustal assembly from later topographic/freeboard closure and keeps H06/H07/H10/H11 independent of late continent assembly.

### C4–C3 marginal corridor

The replacement C4 route remains approximately 31.70–45.58°S in the regenerated native frame. Its ~3.75 million km² surface envelope is now treated predominantly as inherited foreland/microcontinental and reworked margin crust rather than wholly young accretion.

A representative corridor block reaches final C4-relative orientation by 8 Ma. Later modest C4–C3 convergence may continue inside the collisional/thrust/strike-slip network without requiring the land route to be assembled during human evolution.

### C3 southeast shelf and eastern stepping blocks

The shelf head's western root remains connected to C3. The legacy `C5_SHELF_HEAD` identifier is retained only for project continuity; plate parentage is the C3 southeast shelf block.

The two small eastern stepping blocks remain the local repair to the failed ~188 km crossing. Regenerated water gaps are approximately 54.65, 28.30 and 75.01 km. Their authored local rotations finish by 2 Ma, before the 1.9 Ma human-route motion cutoff.

### Northern approach

The northern route remains a shallow-sill relationship between old continental shelves and microcontinental highs. It is not a welded bridge plate. H06/H07/H10 accessibility remains a local relative-sea-level and bathymetric problem on old substrate.

## Plate-block reconstruction result

The machine-readable model is [`plate-block-model.json`](plate-block-model.json), with methodology in [`PLATE-RECONSTRUCTION.md`](PLATE-RECONSTRUCTION.md).

The plate audit checks both MERDITH2021 and MULLER2022 at 0, 2 and 23 Ma plus the authored synthetic rotations.

Key results:

- C3 west/east pair-distance drift through 23 Ma is metre-scale in both reference models;
- C4 core/refuge/exit pair distances are likewise effectively rigid at the tested epochs;
- C3 east versus the southeast shelf changes by about 43.2 km over 23 Myr, supporting a slow shelf microplate rather than mandatory rigid welding;
- C1/C2 separation changes by about 9.3 km over the last 2 Myr;
- C4–C3 corridor parent separation changes by about 5.5 km over 0–2 Ma;
- northern shelf parents change by about 1.25 km over 0–2 Ma;
- authored synthetic block motions imply representative stage speeds of roughly 1.4–2.7 cm/yr;
- every authored human-route-sensitive rigid motion is complete by 2 Ma or earlier.

No test approaches the current failure thresholds closely enough to justify a silhouette or Strategy-B change.

## Crustal-provenance correction

The broad JX1, C4 corridor, and shelf-head polygons cannot reasonably mean that millions of square kilometres of continental crust formed during their late-Cenozoic assembly intervals.

Their provisional substrate fractions are now:

- JX1: 88% old/reworked, 10% juvenile arc, 2% young cover;
- C4 corridor: 92% old/reworked, 6% juvenile arc/suture, 2% young cover;
- C3 southeast shelf head: 97% old/reworked, 2% juvenile arc, 1% young cover.

Combined synthetic juvenile continental crust is about 544,762 km², or about 0.259% of the ~210.4 million km² Earth-analogue continental-crust inventory used by the test.

This correction is now part of Strategy A. The word “terrane” in legacy object identifiers should not be read to mean wholly juvenile crust.

## Global freeboard consequence

The current Cartopy regeneration contains about 158.64 million km² of emerged land, +7.73% relative to the generalized 147.26 million km² reference mask.

The plate-scale accounting demonstrates that this does **not** require net continental-crust creation. With an Earth-analogue ~210.4 million km² continental-crust inventory:

- about 75.4% is emergent in Strategy A;
- about 51.76 million km² remains submerged;
- required net new continental crust is 0 km².

The hard unsolved question is therefore how uplift, subsidence, stretching, crustal thickness, sediment loading, thermal history and isostasy produce the required **freeboard distribution through time**.

## Failure history and bounded repairs

The reconstruction has encountered several real failures. Each was repaired at the failure point rather than by restarting the world design:

1. **C4 corridor missed C3 after equal-area resizing.** Widened only the local corridor envelope.
2. **Eastern first water leg ~188 km.** Added two small old stepping blocks while preserving deep channels.
3. **Shelf cradle remained on land but disconnected from C3.** Extended only the shelf-head western root.
4. **Old geological validator required the rejected C2 offset.** Migrated the validator instead of restoring obsolete geometry.
5. **Broad provinces implied implausibly huge young terranes.** Reclassified their crustal provenance to mostly inherited/reworked substrate without changing coastlines.

The first explicit plate-block audit then passed without another geometric repair.

## Current validation stack

From the repository root:

```sh
ERDE_GEOMETRY_ONLY=1 python scripts/editorial/try_erde_global.py
python scripts/editorial/validate_erde_constraint_graph.py
python scripts/editorial/validate_erde_physical_tests.py
python scripts/editorial/validate_erde_history.py
python scripts/editorial/check_erde_paleolatitudes.py
python scripts/editorial/validate_erde_plate_blocks.py
```

The pull-request CI runs this stack from regenerated geometry before the normal site and browser/accessibility tests.

## Next escalation: spatial deformation and freeboard

### Phase 1 — crustal-thickness and stretching fields

Construct spatial grids or polygon attributes for:

- inherited cratonic/platform crust;
- rifted continental margins;
- stretched/transitional crust;
- microcontinental fragments;
- juvenile arc/suture crust;
- sedimentary basins.

The purpose is to convert the current area fractions into a mass- and buoyancy-aware crustal inventory.

### Phase 2 — deforming topological networks

Replace schematic boundary descriptions with spatial deformation models for:

- JX1 internal transpressional/subduction-transform network;
- C4–C3 collisional/thrust/strike-slip network;
- C3 southeast shelf microplate boundary where required.

The model should preserve rigid interiors while distributing strain across physically plausible widths and rates.

### Phase 3 — time-indexed palaeoelevation/freeboard

Reconstruct enough elevation/subsidence history to explain the large gross redistribution of emerged land:

- approximately 44 million km² of current land located where the generalized reference has water;
- approximately 33 million km² of reference land locations submerged in Strategy A.

This is not one uniform sea-level offset. It requires regional tectonic/freeboard histories tied to crustal thickness, stretching, thermal subsidence, orogenic uplift, sediment loading and isostatic response.

### Phase 4 — couple U1–U4

Once the common freeboard geometry exists:

- U1: run C4 ice/climate/refugia against explicit elevations;
- U2: run northern local relative sea level and sill exposure;
- U3: run eastern bathymetry, currents and voyage states;
- U4: run C3 relief, drainage and hydroclimate connectivity.

### Phase 5 — mantle/dynamic topography only if needed

Do not invoke unconstrained mantle-driven dynamic topography merely to force coastlines to fit. Use it only if regional crustal thickness, rifting, orogenesis, thermal evolution, sediment loading and isostasy cannot close the required freeboard history within plausible ranges.

## Retry policy

- Preserve Strategy A while a failure can be repaired at its responsible margin, block, deformation zone, bathymetric sill or elevation field.
- Do not redraw continents merely to simplify a model that has not demonstrated a contradiction.
- Invoke Strategy B only if a spatial deforming-mesh reconstruction shows a genuine C1–C2 incompatibility that cannot be absorbed inside JX1.
- If Strategy B is ever invoked and also fails, preserve the best validated Strategy A state and report the irreducible incompatibility rather than entering an open-ended redesign loop.

## Acceptance boundary

The plate-block pass materially reduces the uncertainty in U5, but `full_geological_validation` remains false. Strategy A should not be promoted to canonical planetary geography until the spatial deformation/freeboard model and the coupled U1–U4 regional tests are complete enough to show that the present design can arise through a coherent time history rather than only satisfy independent necessary conditions.
