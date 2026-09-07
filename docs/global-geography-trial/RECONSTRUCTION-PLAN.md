# Erde dated continental reconstruction plan

## Decision

Use **Strategy A: inherited continental nuclei plus old marginal terranes and dated gateways**.

This is a reconstruction framework, not a plate-dynamic simulation. It is deliberately bounded. It solves the two highest-coupling defects in the previous worldwide candidate without pretending that unresolved climate, bathymetry, paleoelevation, or deep-time plate partitioning have already been proven.

The prior candidate is not accepted as historical reconstruction because it combined a 6° rigid C2 offset with restored Earth-reference coastline inside protected guard sectors. That arrangement could pass present-day connectivity checks while providing no dated deformation history for the preserved hinge or migration corridors.

Strategy A therefore makes three geometry changes and one validation change:

1. Remove the extra 6° C2 Euler rotation. C2 remains visibly non-Earthlike because its authored silhouette is already different.
2. Replace the pasted C1-C2 hinge with **JX1**, an oblique old composite terrane/junction whose substrate is stable long before the human-route ledger.
3. Replace the old approximately 60°S C4 ancestral exit with a broad western/northwestern marginal corridor that stays approximately 32–46°S in the present reconstruction frame before entering C3.
4. Treat historical accessibility as dated state on old substrate. A connected modern land mask is no longer accepted as evidence that a route existed at H06, H10, or any other dated interval.

## Bounded analysis

### Constraints that must survive any redesign

- All six continental bodies need crustal provenance and deep-time biotic continuity or a dated vicariance mechanism.
- Shelf/karst architecture for H02 must predate 1.9 Ma.
- Persistent deep-water channels must coexist with nearby shelf exposure through H03 and H09.
- The early American-form founding window H06 (0.65–0.45 Ma) and the later principal founding window H10 (35–20 ka) must use old substrate but remain distinct accessibility episodes.
- No continent-scale motion or new junction assembly may be required after 1.9 Ma.
- C4 cannot rely on an unmodeled ice-free south-polar interior to connect its ancestral refuge to the rest of the human-form range.
- C3 must permit intermittent western/eastern contact without becoming a permanent low-friction bypass.
- C6 and remote islands remain conditional on later ecology and ocean-circulation work.

### Dependencies

The dated graph is implemented in `dated-constraint-graph.json`. The reconstruction objects and their provisional ages are in `reconstruction-model.json`.

The graph distinguishes substrate age, accessibility windows, barrier states, and unresolved physical models. Climate, ice, bathymetry, paleoelevation, and plate kinematics are not inferred from coastline geometry alone.

## Strategy A geometry

### C1-C2: JX1 old oblique junction terrane

The broad C1 and C2 silhouettes are retained, but C2 receives no additional rigid offset. JX1 crosses the old gap as a deliberately non-Panama-like oblique junction.

Provisional crustal history:

- accretion/assembly: 28–18 Ma;
- major relative assembly complete: by 12 Ma;
- later change: uplift, volcanism, erosion, local subsidence, and changing ecological passability only.

This satisfies the core historical rule that H06 and H10 cannot be produced by assembling the continents hundreds of thousands or tens of thousands of years ago.

JX1 may remain physically narrow land while still functioning as a strong demographic/ecological bottleneck. The exact H06/H07/H10 passability pattern is not yet proven and is explicitly deferred to paleotopography, hydroclimate, and local sea-level work.

### C4-C3: lower-latitude marginal substitution

The old ancestral exit locator near source coordinate `(32, 30)` falls near 60°S in the current frame and creates an unnecessary ice-history dependency.

The replacement route follows a widened C4 western/northwestern foreland into C3. Its authored control envelope is approximately 32–46°S in the current frame. The substrate is provisionally treated as an old retained/accreted foreland, stable by 8 Ma.

This is an explicit historical substitution. The old exit is not silently retained, and the new route is not claimed valid merely because the modern polygons touch.

### C3-C5: shelf head with retained marine barrier

A short continental-platform shelf head reaches the H02 shelf-cradle locator. It does **not** connect to the first deep-water island block. The current control geometry retains roughly 188 km of separation in the local geometric test, which is sufficient to keep a first-order water barrier in the design while later bathymetry determines actual crossing distances and lowstand exposure.

## Validation performed

### Dated graph

`validate_erde_constraint_graph.py` checks all H01–H12 requirements, dependency references, substrate ages, the pre-1.9 Ma motion cutoff, separate H06/H10 accessibility windows, the C4 route substitution, the H03–H09 marine barrier, and explicit unresolved high-coupling science.

Current result: **PASS for chronology and dependency logic**. This is not full geological validation.

### Present geometry controls

A source-frame/local equal-area geometry audit was used to test the new controls without restoring Earth-reference guard sectors.

The first C4 corridor control failed because the existing C3/C4 equal-area body resizing left it about 5° short of C3. The failure was diagnosed as a local envelope mismatch, not a strategy failure. The corridor was widened north/east and re-tested.

The revised controls pass the available structural checks:

- all eleven established land anchors lie on candidate land;
- C1 and C2 interiors are connected through JX1;
- the ancestral C4 refuge and C3 western contact share a connected land component through the new marginal corridor;
- the C3 eastern core and shelf-cradle locator share a connected land component;
- the C5 shelf head remains separated from the first deep-water island block;
- the new C4 corridor remains approximately 32–46°S rather than using the old approximately 60°S exit.

A local attempt to calculate the complete transformed world-area union produced a projection/seam artifact around the transformed C6 polar-source polygon, inflating union area. That result is rejected and is **not** used as evidence. Full global area/IoU metrics must be regenerated with the repository's Cartopy pipeline.

## Unresolved constraints and stop conditions

These are not reasons to keep redrawing coastlines.

1. **C4 climate/ice:** verify that productive peripheral refugia can persist without requiring an implausible ice-free polar interior. Resolve with climate, ice, and elevation modeling.
2. **Northern approach shelf:** determine sill depths and exposure thresholds that produce distinct H06 and H10 access windows. Resolve with bathymetry, eustasy, isostasy, and local tectonics.
3. **Eastern shelves/channels:** verify that H02/H04 shelf access coexists with H03/H09 deep-water isolation. Resolve with dated paleobathymetric cross-sections and crossing-distance audits.
4. **C3 internal filter:** test whether relief, drainage, and hydroclimate can permit intermittent western/eastern contact without an easy permanent bypass.
5. **Full plate reconstruction:** partition each final body into dated crustal blocks and plate boundaries and test mass-balanced kinematics. The constraint graph defines what that reconstruction must satisfy but does not simulate it.

## Retry policy

Do not iterate the silhouettes indefinitely.

- Continue with Strategy A while failures can be traced to local geometry, dated passability, relief, or bathymetry and repaired without changing its reconstruction logic.
- Use **Strategy B** only if a later dated plate/block test shows that the C1-C2 junction cannot be generated under Strategy A. Strategy B promotes the junction to a separately reconstructed microplate and permits modest pre-1.9 Ma rotations of C1 and C2 around it.
- If Strategy B also fails a high-coupling constraint, preserve the best valid Strategy A state and report the unresolved incompatibility instead of inventing further continent-scale changes.

## Next scientific work

The next useful work is no longer another silhouette pass. It is:

1. regenerate the candidate with the new controls using the repository Cartopy pipeline;
2. run the existing geometric/geological audits plus the dated graph validator;
3. add dated paleobathymetric states for the northern approach and eastern shelf/channel system;
4. add a C4 peripheral climate/ice test;
5. only after those pass, formalize crustal block polygons and time-indexed rotations/translations for a plate reconstruction.
