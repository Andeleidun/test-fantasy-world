# Scientific basis for the Erde freeboard reconstruction

The freeboard model is a constrained **existence reconstruction**. It uses published physical ranges and standard first-order mechanisms to test whether the Strategy A coastline can arise without unexplained crust creation or late continent-scale motion. It does not claim that the selected parameter field is unique.

## Continental-crust inventory

Cogley (1984), *Continental margins and the extent and number of the continents*, Reviews of Geophysics 22(2), estimated total continental-crust area at **210.4 × 10^6 km²**, about **41%** of Earth's surface, with roughly **30.6%** of continental area submerged and average crustal thickness about 36 km. Later continental-crust syntheses reproduce the same 210.4 Mkm² inventory scale and note that approximately 31% lies below sea level.

Use on Erde: 210.4 Mkm² is an Earth-analogue **accounting target**, not a claim that Erde must copy Earth's continental margins cell-for-cell. The refined Strategy A solution places ~158.7 Mkm² of this continental domain above present sea level and ~51.7 Mkm² below it.

## Crustal thickness and submerged continents

Mortimer et al. (2017), *Zealandia: Earth's Hidden Continent*, GSA Today 27(3), documents a 4.9 Mkm² region of continental crust that is about 94% submerged. Zealandia commonly has 10–30 km crust, compared with about 30 km for extended continental crust, about 46 km beneath orogens, and about 7 km for normal oceanic crust. Widespread Late Cretaceous crustal thinning followed by thermal relaxation and isostatic balance is identified as the primary reason for its submergence.

Use on Erde: continental crust is not equated with dry land. The refined model uses 21–29.7 km for submerged continental margins/shelves, 33–36.5 km for ordinary emergent continental provinces, and 42 km for the thickest modeled orogenic crust. These remain ordinary continental values and avoid treating broad redesigned margins as new oceanic or juvenile crust.

CRUST1.0 (Laske, Masters and colleagues) is a global 1° crustal model and provides an observational analogue for large lateral variations in Moho depth and sediment thickness. Erde's 1° mesh matches its broad spatial scale but does not import CRUST1.0 regional values cell-for-cell.

## Airy isostasy and why thickness alone is insufficient

The Airy-Heiskanen approximation relates surface load and crustal-root thickness through density contrast. The Erde model uses crust density 2800 kg/m³, mantle density 3300 kg/m³ and a 30 km sea-level reference crust.

First-order structural term:

`e = (crust_thickness - 30 km) * (rho_mantle - rho_crust) / rho_crust`

This is not a deterministic elevation law. Observational studies show that crustal thickness alone does not uniquely predict surface elevation because mantle-lithosphere buoyancy, flexure and regional loading also matter. The model therefore permits a bounded residual term. The refined solution's maximum absolute residual is **1000 m**, below its 1200 m validation ceiling.

## Rifting, stretching and thermal subsidence

McKenzie (1978), *Some remarks on the development of sedimentary basins*, models continental extension as rapid lithospheric stretching followed by conductive cooling and continuing thermal subsidence. Later implementations commonly use a thermal diffusion time constant near 62.8 Myr for a ~125 km lithosphere.

Use on Erde:

- emergent inherited margins remain ~33–34 km thick;
- shallow inner shelf is modeled at 29.7 km;
- outer shelf at 29.2 km;
- deeper submerged platform at 27.5 km;
- extended continental margin at 21 km;
- maximum authored stretching beta is **1.67**;
- no late-Pleistocene continental relocation is invoked.

The model stays well below extreme hyperextension end members.

## Shortening, sutures and deformation

JX1 and the C4–C3 corridor are not rigid young terranes. They are broad inherited/reworked continental provinces containing narrower deforming arc/suture systems. Their freeboard increases through crustal shortening/thickening during the adopted 28–12 Ma and 30–8 Ma assembly intervals. This changes crustal thickness and relief without creating millions of square kilometres of juvenile continental crust.

The **1°** global mesh is a material-coordinate crust/freeboard field attached to the rotation hierarchy in `plate-block-model.json`. It is not a finite-element geodynamic simulation.

## Why the first executable freeboard pass was rejected

The initial model treated both Strategy A land and generalized source-reference land as mandatory present continental crust. Although that model passed its first formal thresholds, it produced essentially **no global shelf-area response** to -80 to -104 m sea-level states.

That is physically unsatisfactory. The refined model therefore treats Strategy A dry land as the emergent continental core and fills the remaining continental-crust inventory with its nearest offshore shelves/margins. The source-reference mask remains a provenance diagnostic rather than a previous Erde shoreline.

The refined model contains approximately 16.84 Mkm² of shallow inner shelf near -54 m first-order freeboard. A -80 m lowstand therefore exposes about 16.84 Mkm² of additional continental shelf while the deeper outer shelf and eastern deep-water channels remain submerged.

## Sea level and local relative sea level

The reconstruction does not copy Earth's deep-time eustatic curve. Deep-time snapshots use a long-term zero datum with a ±150 m shoreline-uncertainty band. Late migration-critical samples use the authored Erde sea-level states from the physical tests.

Narrow gateways are validated as local sections rather than forcing a 1° grid to resolve them:

- JX1 remains continuously emergent by 3.2 Ma;
- the northern approach produces strong H06/H10 openings and intermittent H07 contact;
- eastern deep sills remain submerged at the -130 m sensitivity lowstand while shelf/island targets remain emergent;
- the C4 peripheral corridor remains above water in the bounded warm/highstand and cold/loaded states.

## Evidence boundary

A passing freeboard reconstruction establishes that **a coherent physically ordinary crustal/freeboard history exists** for the current Strategy A geometry. It does not independently predict the present coastline, uniquely determine palaeoelevation, resolve individual valleys/straits, provide a mantle-convection solution, or prove a climate/ecological history. Those downstream models must consume this common crust/freeboard history rather than inventing incompatible local surfaces.
