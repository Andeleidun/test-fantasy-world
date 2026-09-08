# Erde: worldwide continental redesign and reconstruction study

Status: **Strategy A passes dated geometry, bounded physical gateway tests, crustal-block/finite-rotation validation, and a spatial crustal-thickness/stretching/freeboard existence reconstruction. It remains a reconstruction candidate rather than adopted public geography.**

The current design replaces the rejected worldwide draft that combined a 6° C2 rigid offset with restored Earth-reference guard sectors. The controlling principle is unchanged: a modern coastline is not historical proof. Every route, barrier, shelf and junction needed by H01–H12 must exist in the correct dated state.

## Controlling reconstruction files

- [`dated-constraint-graph.json`](dated-constraint-graph.json): H01–H12 chronology, dependencies and negative constraints.
- [`reconstruction-model.json`](reconstruction-model.json): current Strategy A objects and resolution state.
- [`physical-test-model.json`](physical-test-model.json): bounded gateway, sea-level, isolation and refuge tests.
- [`plate-block-model.json`](plate-block-model.json): inherited rigid blocks, deforming boundary provinces and finite rotations.
- [`freeboard-model.json`](freeboard-model.json): spatial crustal-thickness, stretching, subsidence, uplift and shelf-freeboard model.
- [`PLATE-RECONSTRUCTION.md`](PLATE-RECONSTRUCTION.md): plate-scale interpretation.
- [`FREEBOARD-RECONSTRUCTION.md`](FREEBOARD-RECONSTRUCTION.md): solution of the primary crust/freeboard problem.

## Current geography and dated structure

**C1–C2 / JX1.** C2 has no added Euler offset. JX1 is mostly old/reworked continental substrate with a narrower younger arc/suture system. Major block reorientation is complete by 12 Ma and a continuous terrestrial neck exists by about 3.2 Ma through freeboard/relief evolution rather than late continent assembly.

**C4–C3 corridor.** The old ~60°S ancestral exit is replaced by a lower-latitude marginal corridor spanning about **31.70–45.58°S** in the regenerated frame. Its ~3.75 Mkm² envelope is old foreland/microcontinental and reworked margin crust, not newly generated Cenozoic continent.

**C3 southeast shelf and eastern islands.** The shelf head is kinematically part of the C3 southeast shelf system. The initially excessive ~188 km first water leg was replaced by two small old stepping blocks; regenerated water gaps are about **54.65, 28.30 and 75.01 km**. Deep channels remain water even in the -130 m lowstand sensitivity case.

**Northern approach.** This is an old shelf/microcontinental-high system with distinct H06 and H10 exposure windows and intermittent H07 access, not a newly assembled bridge plate.

## Validation stack

| Layer | Result | Establishes |
| --- | --- | --- |
| Dated H01–H12 graph | **PASS** | chronology, dependencies, object ages and negative constraints |
| Regenerated structural geometry | **PASS** | all protected anchors and required land-component relationships survive |
| Bounded physical model | **PASS** | gateway, isolation, C4 refuge and C3 filtering scenarios coexist |
| Geological necessary conditions | **PASS** | Strategy A does not rely on the rejected C2/guard-sector logic |
| Plate-block history | **PASS** | inherited circuits, finite rotations and crust provenance are kinematically ordinary |
| Spatial freeboard reconstruction | **PASS** | ordinary continental crust can produce the Strategy A dry/submerged partition and dated shelf responses without net crust creation |

This is not a mantle-to-climate simulation. The solved state is a coherent necessary-condition/existence reconstruction.

## Plate and crust result

JX1, the C4 corridor and the shelf head are too large to be young terranes. The plate model therefore treats them predominantly as inherited/reworked crust. Synthetic juvenile continental crust totals only about **544,762 km²**, ~**0.259%** of the 210.4 Mkm² continental-crust inventory used for the test.

Representative authored block speeds are roughly **1.4–2.7 cm/yr**. All human-route-sensitive rigid-block motion is complete by 2 Ma. Late C1/C2, C4/C3 and northern-parent separation changes remain small enough to be absorbed by their explicit deforming/shelf systems rather than requiring continent relocation.

## Solved freeboard problem

The verified Cartopy geometry contains about **158.64 Mkm²** of dry land, versus **147.26 Mkm²** in the generalized source mask. The difference is not modeled as creation of ~11.38 Mkm² of new continental crust.

The refined 1° material-coordinate freeboard model instead closes a **210.4 Mkm²** continental-crust inventory by combining Strategy A dry land with nearby submerged continental shelves and margins.

Key validated results:

- continental-domain area: **210.4009 Mkm²** versus 210.4000 Mkm² target;
- Strategy A grid land: **158.6726 Mkm²**, within ~0.023% of exact geometry;
- present modeled submerged continental crust: **24.6%**;
- maximum selected offshore continental-margin distance: **~310 km**;
- present crust-thickness range: **21–42 km**;
- maximum stretching beta: **1.67**;
- required net new continental crust: **0 km²**;
- additional global shelf exposed at a -80 m lowstand: **~16.84 Mkm²**.

The first executable freeboard pass was deliberately rejected despite passing its original thresholds because it produced essentially no global shelf response to -80 to -104 m lowstands. The corrected model no longer forces all source-reference land coordinates to remain continental crust. Strategy A land is the emergent core and the continental inventory is closed with its nearest offshore margins, including explicit shallow and outer shelves.

Critical sub-grid sections also pass:

- JX1 weakest tested 3.2 Ma freeboard after perturbations: **+60 m**;
- H06 northern founder-route samples contain multiple openings and closures;
- H07 contains both marginal exposure and inundation;
- every H10 founder-route sample is exposed;
- eastern deep-channel freeboards at the -130 m lowstand remain **-180, -290 and -230 m**;
- C4 corridor nodes remain emergent under both tested warm/highstand and cold/loaded states.

See [`FREEBOARD-RECONSTRUCTION.md`](FREEBOARD-RECONSTRUCTION.md) for the full reconstruction.

## Failure-and-repair record

1. **6° C2 offset + guard sectors:** rejected as historically ungrounded; replaced with explicit old provinces and dated states.
2. **C4 corridor missed C3 after resizing:** repaired locally by widening the corridor envelope.
3. **~188 km eastern first crossing:** repaired with two small old stepping blocks while retaining marine isolation.
4. **Shelf cradle disconnected from C3:** repaired only at the western shelf-head root.
5. **Broad provinces mislabeled as young terranes:** reinterpreted as mostly inherited/reworked continental substrate.
6. **Stale geological validator:** migrated instead of altering geography to satisfy obsolete assumptions.
7. **First freeboard model had zero lowstand shelf response:** rejected and replaced with a 1° candidate-centered continental-margin inventory with responsive inner/outer shelves.

No failure so far has required Strategy B.

## What remains downstream

The primary crust/freeboard existence problem is no longer open. Remaining work refines processes on the solved substrate:

- **U1:** time-dependent C4 climate and ice fields that determine habitat productivity, not land existence;
- **U2:** higher-resolution northern bathymetry, flexure/isostasy and geoid/local-relative-sea-level refinement;
- **U3:** eastern winds, currents, voyage durations and founder-demographic viability;
- **U4:** C3 high-resolution relief, drainage and hydroclimate producing the already bounded intermittent-contact behavior;
- wildlife, freshwater-lineage, ocean-circulation and ecological consequences across all changed margins.

These downstream models must consume the common plate/crust/freeboard history. They should not independently redraw continents merely to make a local result easier.

## Reproduction

From the repository root with pinned atlas dependencies:

```sh
ERDE_GEOMETRY_ONLY=1 python scripts/editorial/try_erde_global.py
python scripts/editorial/validate_erde_constraint_graph.py
python scripts/editorial/validate_erde_physical_tests.py
python scripts/editorial/validate_erde_history.py
python scripts/editorial/check_erde_paleolatitudes.py
python scripts/editorial/validate_erde_plate_blocks.py
python scripts/editorial/validate_erde_freeboard.py
```

CI regenerates the candidate before running this stack. Generated evidence includes `freeboard-validation-metrics.json` and `freeboard-grid.jsonl` in the workflow artifact.

## Evidence boundary

Earth literature and GPlates constrain mechanisms, rates and physically plausible ranges. Erde's exact coastlines, block fractions, local elevations, sea-level chronology and biological history remain authored hypotheses. The current suite establishes that the selected continental geometry has a coherent dated plate/crust/freeboard realization; it does not establish uniqueness or a full coupled mantle–climate–biosphere history.
