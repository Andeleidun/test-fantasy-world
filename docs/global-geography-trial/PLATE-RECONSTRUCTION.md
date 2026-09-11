# Strategy A crustal-block reconstruction

## Status

This document records the first explicit crustal-block and time-indexed plate model for the redesigned Erde geography.

The model is a **kinematic necessary-condition reconstruction**, not a complete geodynamic simulation. It asks whether the present Strategy A design target can be represented by inherited continental nuclei, old microcontinental and shelf blocks, deforming plate-boundary provinces, moderate finite rotations, and changes in continental freeboard **without requiring impossible late continent assembly or wholesale creation of young continental crust**.

The machine-readable model is `plate-block-model.json`. Its validator is `scripts/editorial/validate_erde_plate_blocks.py`.

## Method

### Reconstruction hierarchy

The reconstruction uses three distinct layers that must not be conflated:

1. **Global reference-frame transform.** Proposal 4 is applied as a fixed global reorientation after reconstruction. It is not tectonic plate motion.
2. **Inherited rigid-block motion.** Old continental nuclei and shelf blocks use the cached MERDITH2021 GPlates point reconstructions as the primary scaffold, with MULLER2022 as an independent sensitivity scaffold.
3. **Erde-specific relative deformation.** Redesigned junctions and marginal provinces use explicit relative finite rotations and/or deforming boundary networks. These motions are complete before the 1.9 Ma human-route cutoff wherever their geometry matters to H01-H12.

This mirrors the architecture supported by GPlates: rigid plate geometries move through finite Euler rotations and rotation hierarchies, while diffuse boundaries can be represented as deforming networks containing optional interior rigid blocks and deforming triangulations.

## Critical reinterpretation from the plate-scale pass

The earlier Strategy A descriptions used the word **terrane** too broadly for several surface polygons. Their generated surface areas make a wholly juvenile interpretation untenable:

- JX1 surface province: about 2.96 million km²;
- C4 marginal corridor: about 3.75 million km²;
- C5 shelf head: about 1.15 million km².

Those are surface reconstruction envelopes, not plausible areas of continental crust generated from scratch during their late-Cenozoic assembly intervals.

The plate model therefore retains their successful surface geometry while changing the crustal interpretation:

- **JX1** is a broad C1-C2 junction province composed mainly of old microcontinental fragments and reworked C1/C2 margin crust, with a substantially narrower juvenile arc/suture contribution.
- **C4 marginal corridor** is mainly old foreland, microcontinental, and reworked C4/C3 margin crust later reorganized by the 30-8 Ma collision/suture history.
- **C5 shelf head** is mostly old C3 southeast continental-shelf/rifted-margin crust. The legacy feature name is retained for project continuity, but its kinematic parent is the C3 southeast shelf block represented by the inherited shelf-cradle control, not the C5 nucleus.
- The two small eastern stepping islands can plausibly contain much larger juvenile-arc fractions because their actual areas are only hundreds of square kilometres.

This is a semantic/crustal-provenance correction, not a coastline redesign.

## Inherited rigid-block scaffold

The cached GPlates point controls define the following Earth-analogue reconstruction IDs at the tested epochs:

| Erde block | Control | Cached plate ID |
| --- | --- | ---: |
| C1 nucleus | C1 interior | 101 |
| C2 nucleus | C2 interior | 201 |
| C3 west core | C3 west | 302 |
| C3 east core | C3 east | 601 |
| C3 southeast shelf | shelf cradle | 614 |
| C4 core | C4 core | 712 |
| C4 west foreland | ancestral refuge | 714 |
| C4 northeast platform | ancestral exit | 715 |
| C5 nucleus | C5 interior | 8011 |
| C6 nucleus | C6 interior | 8031 |

Distinct IDs do not by themselves prove distinct relative motion at every epoch. The plate validator therefore tests **pair-distance invariance**, not merely ID equality. At the 0, 2, and 23 Ma cached states, the C3 west/east controls and the three C4 controls behave as effectively co-moving late-Cenozoic clusters within the model tolerances. The C3 southeast shelf control retains modest residual motion relative to the C3 east core and is treated as a slow microplate/shelf block rather than silently welded to it.

## Deforming boundary provinces

### JX1 C1-C2 junction

JX1 is not treated as a rigid plate welded simultaneously to C1 and C2. That would conflict with continuing relative C1-C2 motion.

Instead:

- a central inherited/reworked microcontinental block finishes its major C1-relative reorientation by 12 Ma;
- continuing C1-C2 relative motion is absorbed across the southern/central deforming boundary network through transpression, strike-slip partitioning, subduction-related deformation, uplift, and local basin formation;
- complete terrestrial emergence is a later topographic/freeboard event, modeled by about 3.2 Ma;
- after 1.9 Ma, no new continent-scale motion is permitted to create the migration gateway.

The cached parent-block test limits 0-2 Ma change in C1-C2 separation to 50 km; the expected inherited-scaffold result is substantially below that limit.

### C4-C3 marginal corridor

The C4 route likewise does not require the entire ~3.75 million km² corridor to have accreted as new crust between 30 and 12 Ma.

The surface route is modeled as a broad old foreland/microcontinental province. A younger collisional suture and thrust/strike-slip network reorganizes it. Its representative foreland block reaches final C4-relative orientation by 8 Ma, while subsequent modest C3-C4 convergence can be accommodated internally without destroying land continuity.

### Northern approach

The northern American approach is deliberately **not a welded bridge plate**. It is a relationship between old opposing continental shelves and microcontinental highs separated by a shallow sill. Its migration significance therefore remains controlled by local relative sea level and bathymetry rather than by late continental assembly.

## Erde-specific finite rotations

The authored relative rotations are intentionally modest and finish before they can interfere with the human-route chronology:

| Block | Relative history | Motion complete |
| --- | --- | ---: |
| JX1 central block | +8° at 28 Ma → +3° at 18 Ma → 0° at 12 Ma | 12 Ma |
| C4 corridor foreland | +10° at 30 Ma → +4° at 18 Ma → 0° at 8 Ma | 8 Ma |
| Eastern stepping A | +4° at 5 Ma → +1.5° at 3 Ma → 0° at 2 Ma | 2 Ma |
| Eastern stepping B | -4° at 5 Ma → -1.5° at 3 Ma → 0° at 2 Ma | 2 Ma |

Representative stage velocities are approximately 1.4-2.7 cm/yr. These are not presented as measured values for Erde; they are a plausibility envelope for the authored block motions.

The eastern stepping islands are therefore placed into their final shelf-relative geometry by **2 Ma**, slightly earlier than the previous provisional 1.3 Ma statement. That is a conservative correction: the water-separated island geography already exists before H02 and remains available for H03-H05.

## Continental-crust budget and the +7.7% emerged-land increase

The previous physical pass found about 158.64 million km² of emerged Strategy A land, roughly 11.38 million km² more than the generalized reference land mask.

That number must not be interpreted as 11.38 million km² of newly generated continental crust.

Published global estimates place modern Earth continental crust, including submerged continental margins and fragments, at roughly **210.4 million km²**, about 41% of Earth's surface. On that Earth-analogue inventory:

- Strategy A emerged land: ~158.64 million km²;
- target continental-crust inventory: ~210.4 million km²;
- continental crust still submerged: ~51.76 million km²;
- fraction of target continental crust emerged: ~75.4%.

Thus the present Strategy A land fraction can close **without any net increase in continental-crust area**. The difference can instead be assigned to a different global distribution of shelf depth, rifted-margin subsidence, orogenic uplift, sediment loading, thermal history, and other freeboard controls.

This does not prove the required palaeoelevation history. It removes the specific false assumption that the extra emerged land necessarily requires implausible young crust generation.

## Crustal-provenance budget

The provisional large-province budgets intentionally require at least 80% inherited or reworked crust:

- JX1: 88% old/reworked, 10% juvenile arc, 2% young cover;
- C4 corridor: 92% old/reworked, 6% juvenile arc/suture, 2% young cover;
- C5 shelf head: 97% old/reworked, 2% juvenile arc, 1% young cover.

The combined juvenile contribution of these synthetic surface provinces must remain below 1% of the approximately 210.4 million km² continental-crust inventory. The validator computes this using the regenerated areas rather than trusting the authored percentages in isolation.

## Dated reconstruction sequence

- **66 Ma:** all six main continental nuclei and the old shelf/microcontinental blocks already exist; final coastlines do not.
- **30 Ma:** C4-C3 convergence reorganizes the old foreland; JX1 assembly is underway.
- **28 Ma:** JX1 central block remains about 8° from final C1-relative orientation.
- **23 Ma:** inherited MERDITH2021/MULLER2022 control circuits provide the first explicit late-Cenozoic cross-check.
- **18 Ma:** JX1 and C4 corridor relative motions have substantially converged toward their final orientations.
- **12 Ma:** JX1 major block reorientation is complete; later relative motion is boundary deformation.
- **8 Ma:** the C4 corridor foreland reaches final C4-relative orientation.
- **5-2 Ma:** the small eastern stepping blocks finish local shelf-margin rotations.
- **~3.2 Ma:** JX1 reaches its modeled continuous terrestrial-neck state through uplift/freeboard evolution rather than new continent assembly.
- **2 Ma:** all human-route-sensitive synthetic rigid-block rotations are complete.
- **1.9 Ma:** hard chronology gate. Continental-scale/gateway-forming geometry is frozen for H02-H12; later evolution is limited to boundary slip, uplift, subsidence, volcanism, erosion, glaciation, bathymetry, and sea-level effects.
- **0 Ma:** present Strategy A design target.

## What this pass can and cannot validate

A passing plate-block validator establishes that:

- inherited GPlates sample relations are internally compatible with the proposed rigid clusters at 0, 2, and 23 Ma;
- the proposed synthetic finite rotations do not require excessive representative block speeds;
- gateway-forming block rotations finish before the human-route cutoff;
- broad junction/corridor provinces are not being counted as millions of square kilometres of young crust;
- the global emerged-land increase can fit inside an Earth-analogue continental-crust inventory without net crust creation.

It **does not** establish:

- a unique set of plate boundaries or Euler poles;
- exact crustal thickness, stretching, or strain fields;
- exact palaeoelevation or coastline at intermediate dates;
- mantle-driven dynamic topography;
- local relative sea level or bathymetry;
- climate, ice sheets, or migration probability.

## Remaining escalation gates

If the crustal-block validator passes, U5 changes from an unstructured high-risk unknown into a bounded reconstruction with the following remaining implementation work:

1. Build spatial crustal-thickness/stretching grids for the redesigned continental margins.
2. Replace schematic JX1 and C4-C3 boundary descriptions with dynamic topological polygons/deforming meshes.
3. Build a time-indexed freeboard/palaeoelevation model capable of explaining the large gross land/water redistribution.
4. Couple the existing U1-U4 regional tests to that geometry: C4 ice/climate, northern relative sea level, eastern bathymetry/voyage, and C3 relief/drainage.
5. Invoke mantle/dynamic-topography modeling only if regional crustal thickness, isostasy, rifting, orogenic uplift, and sediment/thermal effects cannot close the required freeboard history.

A failure at any of those stages should be repaired at the responsible block or margin. Strategy B remains reserved for a genuine C1-C2 kinematic incompatibility that cannot be absorbed by the JX1 deforming network.

## Scientific grounding

- GPlates reconstruction theory: https://www.gplates.org/docs/user-manual/reconstructions/
- GPlates crustal deformation and deforming networks: https://www.gplates.org/docs/user-manual/crustaldeformation/
- pyGPlates primer, including rotation hierarchies, finite rotations, topologies, deforming networks, and rigid blocks: https://www.gplates.org/docs/pygplates/pygplates_primer
- Cogley (1984), *Continental margins and the extent and number of the continents*, Reviews of Geophysics 22:101-122, DOI 10.1029/RG022i002p00101.
- Hawkesworth et al. (2013), *The continental record and the generation of continental crust*, GSA Bulletin 125:14-32, DOI 10.1130/B30722.1.
- Cawood et al. (2018), *Continental crustal volume, thickness and area, and their geodynamic implications*, Gondwana Research 55:13-20.
- U.S. Geological Survey, *This Dynamic Planet / Rates of motion*: observed plate motions range from less than 1 to more than 15 cm/yr in the summarized global examples.

These references constrain mechanisms and broad physical scales. Erde's particular blocks, dates, Euler poles, crustal fractions, and geological narrative remain authored hypotheses subject to the explicit validators above.
