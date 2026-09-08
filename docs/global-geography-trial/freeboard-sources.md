# Scientific basis for the Erde freeboard reconstruction

The freeboard model is a constrained **existence reconstruction**. It uses published physical ranges and standard first-order mechanisms to test whether the Strategy A coastline can arise without unexplained crust creation or late continent-scale motion. It does not claim that the selected parameter field is unique.

## Crustal thickness and submerged continents

Mortimer et al. (2017), *Zealandia: Earth's Hidden Continent*, GSA Today 27(3), documents a 4.9 million km² region of continental crust that is about 94% submerged. Zealandia commonly has 10–30 km crust, compared with about 30 km for extended continental crust, about 46 km beneath orogens, and about 7 km for normal oceanic crust. Widespread Late Cretaceous crustal thinning followed by thermal relaxation and isostatic balance is identified as the primary reason for its submergence.

Use on Erde: continental crust is not equated with dry land. Strategy A may therefore contain roughly 51.8 million km² of submerged continental crust while about 158.6 million km² is emergent. Extended margins in the model use 21–27.5 km crust; stable interiors use 33–36.5 km; orogenic crust reaches 42 km. These values remain inside ordinary continental ranges and avoid treating broad redesigned margins as new oceanic or juvenile crust.

CRUST1.0 (Laske, Masters and colleagues) is the global 1° crustal model used as an observational analogue for large lateral variations in Moho depth and sediment thickness. The Erde mesh does not import its regional values cell-for-cell.

## Airy isostasy and why thickness alone is insufficient

The Airy-Heiskanen approximation relates surface load and crustal-root thickness through density contrast. USGS applications commonly use a sea-level reference crust around 30 km and crust/mantle density contrasts of a few hundred kg/m³. The Erde model uses crust density 2800 kg/m³ and mantle density 3300 kg/m³, consistent with values used in lithospheric and basin studies.

The model's first-order structural term is:

`e = (crust_thickness - 30 km) * (rho_mantle - rho_crust) / rho_crust`

This is not used as a deterministic elevation law. Mooney/Lachenbruch-style USGS analyses show that regions near sea level can have crust roughly 25–55 km thick and that crustal thickness alone does not predict elevation because mantle-lithosphere buoyancy also matters. The model therefore permits a bounded residual term (maximum absolute value 1200 m) for mantle-lid buoyancy, flexure, regional loading and other unresolved long-wavelength effects.

## Rifting, stretching and thermal subsidence

McKenzie (1978), *Some remarks on the development of sedimentary basins*, models continental extension as rapid lithospheric stretching followed by conductive cooling and thermal subsidence. Later implementations commonly use stretching factor beta and a thermal diffusion time constant near 62.8 Myr for a ~125 km lithosphere.

Use on Erde:

- ordinary emergent margins end near 33–34 km crust;
- submerged platforms end near 27.5 km;
- extended continental margins end near 21 km;
- maximum beta in the authored province set remains well below 3;
- thermal subsidence follows `1 - exp(-t/62.8 Myr)` after rifting;
- no late-Pleistocene continental relocation is invoked.

The model intentionally stays below the beta ~3–4 hyperextension end member discussed for the thinnest parts of Zealandia.

## Shortening, sutures and deformation

JX1 and the C4–C3 corridor are not treated as rigid young terranes. They are broad inherited/reworked continental provinces containing narrower deforming arc/suture systems. Their freeboard increases through crustal shortening/thickening during the already adopted 28–12 Ma and 30–8 Ma assembly intervals. This changes crustal thickness and relief without creating millions of square kilometres of juvenile continental crust.

The 2° global mesh is a material-coordinate deformation/freeboard field attached to the rotation hierarchy in `plate-block-model.json`. It is not a substitute for a finite-element geodynamic model; it is sufficient to test whether required thickness changes, deformation ages and freeboard signs are physically ordinary.

## Sea level and local relative sea level

The reconstruction does not copy Earth's deep-time eustatic curve. Deep-time snapshots use a long-term zero datum and preserve a ±150 m shoreline-uncertainty band. Late migration-critical samples use the already authored Erde sea-level states from the physical tests.

Narrow gateways are validated as local sections instead of forcing a 2° global grid to resolve them:

- JX1 must be continuously emergent by 3.2 Ma;
- the northern approach has a deeper founder sill and a slightly shallower small-contact route, allowing strong H06/H10 openings but intermittent H07 contact;
- eastern deep sills remain submerged at a -130 m lowstand while the shelf head and stepping islands remain emergent;
- the C4 peripheral lowland remains above water under bounded warm/highstand and cold/loaded states.

## Evidence boundary

A passing freeboard reconstruction establishes that **a coherent physically ordinary crustal/freeboard history exists** for the current Strategy A geometry. It does not independently predict the present coastline, uniquely determine palaeoelevation, resolve individual valleys/straits, provide a mantle-convection solution, or prove a climate/ecological history. Those downstream models must consume this common crustal/freeboard history rather than inventing incompatible local surfaces.
