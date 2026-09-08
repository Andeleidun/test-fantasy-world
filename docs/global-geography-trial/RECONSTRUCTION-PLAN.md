# Erde dated continental reconstruction plan

## Current decision

Continue **Strategy A: inherited continental nuclei plus old marginal provinces and dated gateways**.

The reconstruction has now passed five coupled escalation levels:

1. H01–H12 dated constraint graph;
2. regenerated structural geometry;
3. bounded regional physical tests;
4. crustal-block / finite-rotation / continental-crust accounting;
5. **spatial crustal-thickness/stretching/freeboard existence reconstruction**.

The primary U5 existence problem is therefore **resolved**. Strategy B has not been invoked.

## What the solved state means

Strategy A no longer depends on the proposition that a visually redesigned coastline can simply be assigned a plausible history later. The current model now supplies a common sequence of:

- old rigid continental nuclei and shelf blocks;
- dated deforming junction/collision provinces;
- ordinary finite rotations completed before the human-route ledger;
- spatial crustal-thickness/stretching classes;
- post-rift thermal subsidence and older collisional thickening;
- shallow/outer continental shelves;
- local dated gateway freeboard sections.

The present Strategy A coastline remains an authorial design target, but the reconstruction demonstrates that a physically ordinary crustal/freeboard history can realize it without net continental-crust creation or late continent-scale motion.

## Why Strategy A replaced the old candidate

The rejected candidate combined a 6° C2 rigid offset with Earth-reference guard sectors. That could preserve present connectivity while providing no dated history for the preserved routes.

Strategy A instead uses:

- **0°** additional C2 rotation;
- JX1 as an old/reworked C1–C2 junction province;
- a lower-latitude C4–C3 marginal corridor;
- an old C3 southeast shelf head;
- two small eastern stepping blocks;
- a northern shelf/sill system rather than a welded bridge plate.

Modern connectivity is never accepted as historical proof by itself.

## Plate-block solution

The plate model in [`plate-block-model.json`](plate-block-model.json) passes both inherited GPlates sensitivity frames and the authored marginal-block motions.

Representative results:

- C3 west/east behave effectively rigidly through the sampled 23 Ma interval;
- C3 southeast shelf differs from C3 east by only ~43.2 km over 23 Myr;
- JX1 C1/C2 parent separation changes by ~9.3 km over 0–2 Ma;
- C4–C3 corridor parents change by ~5.5 km;
- northern shelf parents by ~1.25 km;
- authored synthetic stage speeds are ~1.4–2.7 cm/yr;
- all human-route-sensitive rigid motions finish by 2 Ma.

Broad JX1, C4 and shelf-head envelopes are mostly inherited/reworked continental substrate rather than enormous young terranes. Synthetic juvenile continental crust is only ~544,762 km², ~0.259% of the adopted continental-crust inventory.

## Freeboard solution

The machine-readable model is [`freeboard-model.json`](freeboard-model.json), the validator is `scripts/editorial/validate_erde_freeboard.py`, and the detailed interpretation is in [`FREEBOARD-RECONSTRUCTION.md`](FREEBOARD-RECONSTRUCTION.md).

The refined 1° reconstruction closes an Earth-analogue **210.4 Mkm²** continental-crust inventory around the present Strategy A land and nearby submerged margins.

Validated results:

- exact Strategy A land: **158.6366 Mkm²**;
- 1° grid Strategy A land: **158.6726 Mkm²**;
- land-grid error: **~0.023%**;
- continental-domain area: **210.4009 Mkm²**;
- crust-inventory mismatch: **~0.0004%**;
- present submerged continental crust: **24.6%**;
- maximum modeled offshore continental-margin distance: **~310 km**;
- present crust thickness: **21–42 km**;
- maximum stretching beta: **1.67**;
- required net new continental crust: **0 km²**;
- additional shallow shelf exposed at -80 m: **~16.84 Mkm²**.

### Important rejected intermediate model

The first freeboard implementation formally passed but was rejected after review because it showed no global shelf-area response from -80 to -104 m sea-level states.

Root cause: it incorrectly forced all generalized source-reference land locations to remain continental crust at the same present coordinates.

Natural repair: Strategy A land became the emergent continental core; the remaining continental-crust inventory is now filled by its nearest offshore continental margins. Explicit inner shelves sit near -54 m first-order present freeboard and outer shelves near -143 m. The source-reference mask is a provenance diagnostic rather than a previous Erde coastline.

The corrected model produces large but bounded shelf expansion during strong lowstands while leaving the required deep-water eastern channels submerged.

## Dated critical sections

### JX1

By 3.2 Ma the weakest tested land-neck node retains **+60 m** freeboard after the maximum local downward perturbation and highstand. No late continent assembly is needed.

### Northern approach

The founder-scale route contains multiple H06 openings and closures, H07 alternates between marginal exposure and inundation, and all tested H10 states expose the founder route. The same old substrate therefore supports two strong founding windows separated by restricted contact.

### Eastern shelf/islands

At the -130 m extreme lowstand, the three deep sills remain **180–290 m below sea level** while the shelf head and stepping islands remain emergent.

### C4 peripheral corridor

All seven tested corridor nodes remain above water in the bounded warm/highstand and cold/ice-loaded freeboard states. Climate productivity remains a downstream question.

## Failure history and bounded repairs

1. **C4 corridor missed C3 after equal-area resizing:** widened only the local corridor.
2. **Eastern first water leg ~188 km:** added two small old stepping blocks while preserving marine barriers.
3. **Shelf cradle was disconnected from C3:** extended only the shelf-head western root.
4. **Old validator required the rejected C2 offset:** migrated the validator instead of restoring obsolete geometry.
5. **Broad provinces implied huge young terranes:** corrected provenance to mostly inherited/reworked substrate.
6. **First freeboard model was globally shelf-insensitive:** changed the crust-domain assumption and added responsive shallow/outer shelf classes.

None required a continent-scale retry or Strategy B.

## Current validation stack

```sh
ERDE_GEOMETRY_ONLY=1 python scripts/editorial/try_erde_global.py
python scripts/editorial/validate_erde_constraint_graph.py
python scripts/editorial/validate_erde_physical_tests.py
python scripts/editorial/validate_erde_history.py
python scripts/editorial/check_erde_paleolatitudes.py
python scripts/editorial/validate_erde_plate_blocks.py
python scripts/editorial/validate_erde_freeboard.py
```

CI regenerates the Strategy A geometry before running the stack.

## Next scientific work

Another continent-outline pass is not justified by the current evidence. Work now proceeds **downstream on the solved substrate**.

### U1 — C4 climate and ice

Use the solved elevations/freeboard as the terrain boundary for a time-dependent ice/climate/refugia model. The question is habitat productivity and ice occupation, not whether the corridor has continental substrate or can stand above water.

### U2 — northern local RSL refinement

Increase bathymetric resolution and include glacio-isostasy, flexure, geoid effects and local tectonic vertical motion around the already passing sill-state sequence.

### U3 — eastern hydrodynamics and founding

Use the fixed 54.65/28.30/75.01 km geometry and deep-channel freeboard to model winds, currents, voyage durations, landings and founder demography.

### U4 — C3 relief/drainage/hydroclimate

Derive high-resolution relief and drainage from the plate/suture/freeboard substrate and verify the intermittent west/east contact state without an unintended coastal bypass.

### Cross-cutting ecology

Evaluate wildlife, freshwater lineages, ocean circulation and biotic vicariance against the same evolving surface.

## Dynamic topography policy

Mantle-driven dynamic topography is no longer needed to close the primary freeboard existence problem. Do not add it merely to increase realism. Introduce it only if a later local/regional model finds a residual vertical-motion requirement that crustal thickness, thermal subsidence, flexure, loading, orogenesis and isostasy cannot plausibly absorb.

## Retry policy

- Preserve Strategy A unless a downstream model identifies a specific contradiction in its common plate/crust/freeboard substrate.
- Repair a demonstrated local relief, shelf, sill or deformation failure at its source.
- Do not redraw continents to simplify an unconstrained downstream model.
- Invoke Strategy B only for a genuine C1–C2 deforming-mesh incompatibility that survives local JX1 repair.

## Acceptance boundary

The former primary blocker, U5 crustal/freeboard existence, is resolved. The candidate should still remain non-canonical until the most consequential downstream U1–U4 and ecological/ocean consequences have been checked against this common reconstruction. Those are now refinements and compatibility tests, not evidence that the continental design lacks a geological history.
