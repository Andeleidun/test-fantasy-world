# Erde: worldwide continental redesign and reconstruction study

Status: **Strategy A passes the current dated-geometry, bounded physical, and crustal-block necessary-condition suites. It is still a reconstruction candidate, not adopted public geography and not a complete geodynamic/climate reconstruction.**

This study replaces the earlier worldwide draft that combined a 6° C2 rigid offset with restored Earth-reference guard sectors. That approach is rejected because a modern connected coastline cannot substitute for a dated geological history. The current design preserves visibly different C1–C6 outlines while requiring every historically important route, barrier, and junction to exist at the date when the population history needs it.

The controlling files are:

- [`dated-constraint-graph.json`](dated-constraint-graph.json): H01–H12 chronology, dependencies, and negative constraints;
- [`reconstruction-model.json`](reconstruction-model.json): current Strategy A reconstruction objects and unresolved high-fidelity gates;
- [`physical-test-model.json`](physical-test-model.json): bounded sea-level, crossing, ice/refugia, and relief-state tests;
- [`plate-block-model.json`](plate-block-model.json): inherited rigid blocks, deforming boundary provinces, finite rotations, and crustal-provenance/freeboard accounting;
- [`PLATE-RECONSTRUCTION.md`](PLATE-RECONSTRUCTION.md): scientific interpretation of the plate-scale pass.

## Current Strategy A

### C1–C2: JX1 junction province

C2 receives **no additional Euler rotation**. JX1 is a broad C1–C2 junction province consisting predominantly of old microcontinental and reworked continental-margin substrate, with a narrower younger arc/suture system. Major authored block reorientation is complete by 12 Ma. A continuous terrestrial neck is modeled by about 3.2 Ma through uplift/freeboard evolution, not through late continent assembly.

Continuing small C1–C2 relative motion is absorbed inside a deforming transpressional/subduction-transform network. The geometry needed for H06, H07, H10 and H11 therefore predates the 1.9 Ma human-route cutoff.

### C4–C3: lower-latitude marginal corridor

The former ancestral-exit control near ~60°S is not retained. It is replaced by a western/northwestern C4 marginal route whose regenerated native latitude spans approximately **31.70–45.58°S**.

The ~3.75 million km² surface envelope is not interpreted as young accreted crust. It is mainly old foreland, microcontinental and reworked C4/C3 margin substrate reorganized by a younger collisional suture/thrust network. Its representative foreland-block reorientation is complete by 8 Ma.

### C3 southeast shelf and eastern islands

The legacy-named `C5_SHELF_HEAD` is kinematically assigned to the **C3 southeast shelf block**, not to the C5 nucleus. Its western root connects to C3 while its eastern edge remains separated from the island radiation.

The original ~188 km first required water leg failed the repeated-founding plausibility audit. Two small old arc/microcontinental stepping blocks were added instead of a land bridge. Regenerated coastline-to-coastline gaps are approximately:

- **54.65 km**;
- **28.30 km**;
- **75.01 km**.

The stepping islands are approximately **445.8 km²** and **582.2 km²**. Their authored relative rotations finish by 2 Ma. Deep-channel scenarios remain marine even at the bounded -130 m lowstand test, preserving H03/H09 isolation while reducing the burden on H04 repeated founding.

### Northern approach

The northern American approach is an old shelf/microcontinental-high system separated by a shallow sill, **not a newly assembled bridge plate**. Distinct H06 and H10 access episodes are produced by relative sea level and bathymetry on old substrate, with intermittent H07 access between them.

## Validation status

The current branch has five reconstruction layers. A pass means the tested necessary conditions are internally consistent; it does not mean the remaining high-fidelity physics have been solved.

| Layer | Current result | What it establishes |
| --- | --- | --- |
| Dated constraint graph | **PASS** | H01–H12 objects, dependencies, ages, negative constraints, and pre-1.9 Ma motion rule are internally consistent |
| Regenerated structural geometry | **PASS** | all 11 established anchors are on land; required land-component connections exist; eastern water barriers remain water |
| Bounded physical model | **PASS** | northern access states, eastern crossing geometry, C4 peripheral refugia scenario, and C3 contact/filter state are mutually consistent |
| Geological necessary-condition audit | **PASS** | current Strategy A geometry/provenance assumptions do not reproduce the rejected C2 offset or violate the tested land/crust/polar constraints |
| Crustal-block / plate history | **PASS** | inherited rotation circuits, authored finite rotations, gateway parent-block drift, juvenile-crust budget, and global continental-crust accounting satisfy the current bounds |

`full_geological_validation` remains **false** because spatial crustal-thickness, deformation, palaeoelevation/freeboard, local bathymetry, climate/ice, and hydrodynamic models are still incomplete.

## Plate-block reconstruction result

The main plate-scale correction was interpretive rather than geometric. JX1, the C4 corridor, and the shelf head are too large to be plausibly treated as wholly young terranes. The current provisional crustal budgets are therefore:

- **JX1:** 88% inherited/reworked crust, 10% juvenile arc crust, 2% young cover;
- **C4 corridor:** 92% inherited/reworked crust, 6% juvenile arc/suture crust, 2% young cover;
- **C3 southeast shelf head:** 97% inherited/reworked crust, 2% juvenile arc crust, 1% young cover.

Across all modeled synthetic provinces, juvenile continental crust totals approximately **544,762 km²**, about **0.259%** of the ~210.4 million km² Earth-analogue continental-crust inventory used for the accounting test.

The inherited MERDITH2021 and MULLER2022 controls also pass the late-Cenozoic rigid/slow-block tests:

- C3 west/east pair-distance drift through 23 Ma is only metre-scale in both reference models;
- C4 core/refuge/exit pair distances likewise remain effectively rigid at the sampled epochs;
- the C3 southeast shelf differs from C3 east by only about **43.2 km** over 23 Myr;
- C1/C2 parent separation changes by about **9.3 km** over 0–2 Ma;
- C4/C3 corridor parents by about **5.5 km**;
- northern-approach parents by about **1.25 km**.

The authored synthetic block rotations imply representative stage speeds of roughly **1.4–2.7 cm/yr**, below the project's conservative 5 cm/yr relative-block cap.

## Land and continental-crust accounting

The verified Cartopy regeneration gives:

| Measurement | Strategy A result |
| --- | ---: |
| Generalized reference land | **147.26 million km²** |
| Candidate emerged land | **158.64 million km²** |
| Net emerged-land change | **+7.73%** |
| Candidate planetary land fraction | **31.10%** |
| Gross changed land/water locations | **~52.1% of reference land area** |

The +7.73% emerged-land increase is **not** modeled as +11.38 million km² of newly generated continental crust. The plate audit uses an Earth-analogue total continental-crust inventory of about **210.4 million km²**. Under that accounting:

- candidate land is about **75.4%** of the target continental crust;
- about **51.76 million km²** of continental crust remains submerged;
- required net new continental crust = **0 km²**.

The unresolved problem is therefore the **freeboard history**: why these particular shelves/platforms are emergent or submerged through time, not how to manufacture enough crust.

## Failures repaired during Strategy A validation

1. **Artificial C2 rotation and guard-sector restoration.** Rejected. C2 now uses its authored silhouette without a 6° offset, and historically important regions are explicit dated reconstruction objects rather than pasted reference coastline.
2. **C4 route missed C3 after equal-area resizing.** The C4 marginal envelope was widened locally and retested; no broader silhouette retry was required.
3. **Eastern first water leg was ~188 km.** Two small old stepping blocks reduced the three actual crossings to ~54.65, 28.30 and 75.01 km while preserving deep-water isolation.
4. **Shelf cradle was on land but disconnected from the C3 eastern core.** Only the western root of the shelf head was extended into the resized C3 margin; its eastern water barriers were retained.
5. **Broad surface provinces were implicitly described as young terranes.** Their coastlines were retained, but their crustal provenance was corrected to predominantly inherited/reworked continental substrate.
6. **The old geological validator still expected the removed C2 offset.** The validator was migrated to Strategy A instead of modifying geography to satisfy obsolete code.

## Remaining high-fidelity gates

The next work is deliberately **not another silhouette pass**.

### U1 — C4 ice and climate

Build a time-dependent elevation/ice/climate solution for the bounded 32–46°S peripheral-refugia behavior. Redraw C4 only if that higher-fidelity model specifically fails the route.

### U2 — northern local relative sea level

Build local bathymetry, eustasy, glacio-isostatic adjustment, tectonic/isostatic subsidence/uplift and geoid sensitivity for H06/H07/H10. Do not add new continent-scale motion.

### U3 — eastern bathymetry and voyaging

Build dated shelf/channel cross-sections plus wind/current/voyage simulations for the 54.65/28.30/75.01 km network. Do not add more islands unless the higher-fidelity model specifically fails.

### U4 — C3 relief and drainage

Build explicit relief, deforming-suture topography, drainage and hydroclimate capable of producing intermittent west/east contact without a permanent bypass.

### U5 — spatial deformation and freeboard

The first plate-block necessary-condition test now passes. The remaining plate-scale work is to:

1. assign spatial crustal-thickness and stretching grids to redesigned margins;
2. replace schematic JX1 and C4–C3 boundaries with deforming topological meshes;
3. construct time-indexed palaeoelevation/freeboard capable of explaining roughly 44 million km² of new land locations and 33 million km² of former land locations;
4. couple U1–U4 to that common geometry;
5. invoke mantle/dynamic-topography modeling only if regional crustal thickness, rifting, isostasy, orogenic uplift, sediment loading and thermal evolution cannot close the freeboard history.

Strategy B remains reserved for a genuine C1–C2 kinematic incompatibility that survives local repair inside the JX1 deforming network.

## Reproduction

With the pinned atlas dependencies installed, from the repository root:

```sh
ERDE_GEOMETRY_ONLY=1 python scripts/editorial/try_erde_global.py
python scripts/editorial/validate_erde_constraint_graph.py
python scripts/editorial/validate_erde_physical_tests.py
python scripts/editorial/validate_erde_history.py
python scripts/editorial/check_erde_paleolatitudes.py
python scripts/editorial/validate_erde_plate_blocks.py
```

A normal `python scripts/editorial/try_erde_global.py` additionally renders the comparison maps.

The PR workflow runs the same reconstruction stack against regenerated outputs before the normal site/browser checks. Because generated map files are not automatically committed by CI, a committed `candidate-geography.geojson`, `measurements.json`, or rendered image must not be treated as branch-head evidence when `design-controls.json` marks `generated_outputs_current: false`. The successful workflow artifact is the verified generated snapshot for that run.

## Evidence boundary

The external Earth literature and GPlates models constrain mechanisms, plausible rates, continental-crust accounting, and reconstruction methodology. Erde's exact coastlines, Euler poles, block fractions, dates, palaeoelevation and migration history remain authored hypotheses. Passing the current validators means no contradiction was found at the tested level; it does not establish uniqueness or full geodynamic truth.
