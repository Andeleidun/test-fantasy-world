"""Build and validate the Strategy A spatial crustal freeboard reconstruction.

This is a multiscale existence model. The present Strategy A coastline is a boundary
condition. A 1-degree material-coordinate grid tests whether ordinary continental
crustal thickness, stretching, shortening, thermal subsidence, bounded isostatic/
lithospheric residuals, sediment fill and volcanic construction can reproduce that
boundary while conserving the adopted continental-crust inventory. Critical narrow
gateways are tested separately at local-section scale because even a 1-degree grid
cannot resolve them.

The generalized Earth-reference land mask is a provenance diagnostic only. It is not
forced to remain continental crust at the same present coordinates. The model does not
claim a unique palaeotopography, GCM, mantle-convection solution, or exact deep-time
eustatic curve.
"""
from __future__ import annotations

from pathlib import Path
import json
import math
import sys

from pyproj import Geod
from shapely import make_valid
from shapely.geometry import LineString, Point, Polygon, shape
from shapely.ops import unary_union

from erde_geometry import FRAME, GEO, PROJECTION, tr

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs" / "global-geography-trial"
MODEL = json.loads((OUT / "freeboard-model.json").read_text())
CONTROLS = json.loads((OUT / "design-controls.json").read_text())
MEASUREMENTS = json.loads((OUT / "measurements.json").read_text())

R = float(MODEL["physical_constants"]["planet_radius_m"])
GEOD = Geod(a=R, b=R)
ERRORS: list[str] = []
WARNINGS: list[str] = []


def polys(g):
    if g.is_empty:
        return []
    if g.geom_type == "Polygon":
        return [g]
    return [p for child in getattr(g, "geoms", []) for p in polys(child)]


def cell_area_km2(lat_center: float, resolution: float) -> float:
    half = resolution / 2
    lat1 = math.radians(max(-90, lat_center - half))
    lat2 = math.radians(min(90, lat_center + half))
    dlon = math.radians(resolution)
    return R * R * dlon * (math.sin(lat2) - math.sin(lat1)) / 1e6


def interp_history(points, age):
    if not points:
        return 0.0
    pts = sorted(((float(a), float(v)) for a, v in points), reverse=True)
    if age >= pts[0][0]:
        return pts[0][1]
    if age <= pts[-1][0]:
        return pts[-1][1]
    for (older, vo), (younger, vy) in zip(pts, pts[1:]):
        if older >= age >= younger:
            f = (older - age) / (older - younger)
            return vo + f * (vy - vo)
    raise RuntimeError((points, age))


def thermal_subsidence_m(params, age):
    end = params.get("rift_end_ma")
    asym = float(params.get("thermal_asymptotic_subsidence_m", 0))
    if end is None or asym == 0 or age >= float(end):
        return 0.0
    dt = float(end) - age
    tau = float(MODEL["physical_constants"]["thermal_time_constant_ma"])
    return -asym * (1 - math.exp(-dt / tau))


def structural_elevation(params, age):
    pc = MODEL["physical_constants"]
    crust = interp_history(params["crust_history_km"], age)
    airy = ((crust - float(pc["sea_level_reference_crust_thickness_km"])) * 1000
            * (float(pc["mantle_density_kg_m3"]) - float(pc["crust_density_kg_m3"]))
            / float(pc["crust_density_kg_m3"]))
    residual = interp_history(params.get("lithosphere_residual_history_m", []), age)
    volcanic = interp_history(params.get("volcanic_surface_build_history_m", []), age)
    sediment = interp_history(params.get("sedimentary_surface_fill_history_m", []), age)
    thermal = thermal_subsidence_m(params, age)
    return {
        "crust_km": crust,
        "airy_m": airy,
        "thermal_m": thermal,
        "residual_m": residual,
        "volcanic_m": volcanic,
        "sediment_fill_m": sediment,
        "structural_elevation_m": airy + thermal + residual + volcanic + sediment,
    }


def sea_level(age):
    table = {float(k): float(v) for k, v in MODEL["eustatic_sea_level_m"].items()}
    if age not in table:
        raise KeyError(age)
    return table[age]


# --- Present candidate/reference geometry ---
candidate = make_valid(unary_union([
    shape(f["geometry"]) for f in json.loads((OUT / "candidate-geography.geojson").read_text())["features"]
]))
reference_source = unary_union([
    shape(g) for g in json.loads((ROOT / "scripts/editorial/data/reference-land.geojson").read_text())["geometries"]
])
reference = make_valid(FRAME.project_geometry(reference_source, GEO))

if not candidate.is_valid or not reference.is_valid:
    ERRORS.append("Candidate or reference geometry is invalid.")
if not CONTROLS.get("generated_outputs_current"):
    ERRORS.append("Strategy A geometry must be regenerated before freeboard validation.")

# Equal Earth is used for spatial distance ordering/classification. Cell area is
# calculated analytically on the sphere.
candidate_proj = make_valid(PROJECTION.project_geometry(candidate, GEO))
candidate_boundary_proj = candidate_proj.boundary

# Recreate named marginal surface envelopes from generator controls.
feature_native = {}
for name, vertices in CONTROLS.get("terrane_reference_frame_vertices", {}).items():
    poly = make_valid(Polygon(vertices))
    feature_native[name] = make_valid(FRAME.project_geometry(poly, GEO))

# Orogenic axes are thickness/freeboard proxies, not finished mountain polygons.
orogen_buffers = []
for axis in MODEL["spatial_rules"]["orogenic_axes_source_lonlat"]:
    native_line = FRAME.project_geometry(LineString(axis), GEO)
    projected = PROJECTION.project_geometry(native_line, GEO)
    orogen_buffers.append(projected.buffer(float(MODEL["spatial_rules"]["orogenic_buffer_km"]) * 1000))
orogen_union = unary_union(orogen_buffers)

body_centers_native = {
    body: tuple(map(float, tr(*source)))
    for body, source in MODEL["spatial_rules"]["body_center_source_lonlat"].items()
}


def nearest_body(lon, lat):
    best = None
    for body, center in body_centers_native.items():
        _, _, distance = GEOD.inv(lon, lat, center[0], center[1])
        if best is None or distance < best[0]:
            best = (distance, body)
    return best[1]


def feature_at(pt):
    order = [
        "EASTERN_STEPPING_TERRANE_A", "EASTERN_STEPPING_TERRANE_B",
        "C5_SHELF_HEAD", "JX1_ISTHMIAN_TERRANE", "C4_MARGINAL_CORRIDOR"
    ]
    for name in order:
        g = feature_native.get(name)
        if g is not None and g.covers(pt):
            return name
    return None


def classify(cell):
    pt = Point(cell["lon"], cell["lat"])
    feat = feature_at(pt)
    if feat == "JX1_ISTHMIAN_TERRANE":
        return "jx1_junction"
    if feat == "C4_MARGINAL_CORRIDOR":
        return "c4_corridor"
    if feat == "C5_SHELF_HEAD":
        return "c3_se_shelf_head"
    if feat in ("EASTERN_STEPPING_TERRANE_A", "EASTERN_STEPPING_TERRANE_B"):
        return "arc_stepping_island"

    pxy = Point(cell["x"], cell["y"])
    if cell["candidate_land"]:
        if orogen_union.covers(pxy):
            return "orogenic_belt"
        coast_km = candidate_boundary_proj.distance(pxy) / 1000
        if cell["reference_land"]:
            return ("stable_interior" if coast_km >= float(MODEL["spatial_rules"]["interior_distance_from_candidate_coast_km"])
                    else "stable_margin")
        if coast_km >= float(MODEL["spatial_rules"]["candidate_only_interior_distance_km"]):
            return "old_divergent_platform"
        return "reworked_margin_land" if cell["body"] in ("C3", "C4") else "stable_margin"

    offshore_km = cell["distance_to_candidate_km"]
    if offshore_km <= float(MODEL["spatial_rules"]["inner_shelf_distance_km"]):
        return "inner_continental_shelf"
    if offshore_km <= float(MODEL["spatial_rules"]["outer_shelf_distance_km"]):
        return "outer_continental_shelf"
    if cell["reference_land"]:
        return "submerged_reference_platform"
    return "extended_continental_margin"


# --- Build global material grid and mass-balanced submerged continental halo ---
res = float(MODEL["scope"]["global_material_grid_resolution_deg"])
latitudes = [(-90 + res / 2) + i * res for i in range(int(180 / res))]
longitudes = [(-180 + res / 2) + i * res for i in range(int(360 / res))]
all_cells = []
for lat in latitudes:
    area = cell_area_km2(lat, res)
    for lon in longitudes:
        pt = Point(lon, lat)
        cand = candidate.covers(pt)
        ref = reference.covers(pt)
        x, y = PROJECTION.transform_point(lon, lat, GEO)
        pxy = Point(float(x), float(y))
        all_cells.append({
            "lon": lon, "lat": lat, "x": float(x), "y": float(y), "area_km2": area,
            "candidate_land": bool(cand), "reference_land": bool(ref),
            "distance_to_candidate_km": 0.0 if cand else candidate_proj.distance(pxy) / 1000,
        })

# Candidate land is the emergent continental core. Add nearest offshore cells until
# the adopted total continental-crust inventory closes. This is materially more
# natural than forcing every removed Earth-reference land location to remain crust.
core = [c for c in all_cells if c["candidate_land"]]
water = [c for c in all_cells if not c["candidate_land"]]
water.sort(key=lambda c: c["distance_to_candidate_km"])

target = float(MODEL["scope"]["continental_crust_target_area_km2"])
domain = list(core)
domain_area = sum(c["area_km2"] for c in domain)
for c in water:
    if domain_area >= target:
        break
    domain.append(c)
    domain_area += c["area_km2"]

if domain_area < target:
    ERRORS.append("Could not allocate the continental-crust target area on the grid.")

for c in domain:
    c["body"] = nearest_body(c["lon"], c["lat"])
    c["province"] = classify(c)

province_params = MODEL["province_models"]
unknown = sorted({c["province"] for c in domain if c["province"] not in province_params})
if unknown:
    ERRORS.append(f"Unknown freeboard provinces: {unknown}")

# --- Physical parameter checks ---
validation = MODEL["validation"]
all_present_thickness = []
max_beta = 0.0
max_residual = 0.0
for name, params in province_params.items():
    present = structural_elevation(params, 0)
    all_present_thickness.append(present["crust_km"])
    initial = max(float(v) for _, v in params["crust_history_km"])
    if present["crust_km"] > 0:
        max_beta = max(max_beta, initial / present["crust_km"])
    for _, v in params.get("lithosphere_residual_history_m", []):
        max_residual = max(max_residual, abs(float(v)))

if min(all_present_thickness) < float(validation["present_crust_thickness_min_km"]):
    ERRORS.append("A province is thinner than the permitted continental/arc crust floor.")
if max(all_present_thickness) > float(validation["present_crust_thickness_max_km"]):
    ERRORS.append("A province exceeds the permitted crust-thickness ceiling.")
if max_beta > float(validation["maximum_stretching_beta"]):
    ERRORS.append(f"Stretching beta {max_beta:.2f} exceeds model limit.")
if max_residual > float(validation["maximum_absolute_lithosphere_residual_m"]):
    ERRORS.append(f"Lithospheric residual {max_residual:.0f} m exceeds model limit.")

# --- Time-indexed freeboard and area accounting ---
epochs = [float(a) for a in MODEL["epochs_ma"]]
snapshots = {}
rows = []
positive_candidate_area = 0.0
candidate_grid_area = 0.0
negative_non_candidate_area = 0.0
non_candidate_domain_area = 0.0
reference_only_domain_area = 0.0

for c in domain:
    params = province_params[c["province"]]
    history = {}
    for age in epochs:
        state = structural_elevation(params, age)
        level = sea_level(age)
        freeboard = state["structural_elevation_m"] - level
        key = str(age).rstrip("0").rstrip(".") if age else "0"
        history[key] = round(freeboard, 1)
    present_fb = structural_elevation(params, 0)["structural_elevation_m"]
    if c["candidate_land"]:
        candidate_grid_area += c["area_km2"]
        if present_fb > 0:
            positive_candidate_area += c["area_km2"]
    else:
        non_candidate_domain_area += c["area_km2"]
        if c["reference_land"]:
            reference_only_domain_area += c["area_km2"]
        if present_fb < 0:
            negative_non_candidate_area += c["area_km2"]
    rows.append({
        "lon": c["lon"], "lat": c["lat"], "area_km2": round(c["area_km2"], 3),
        "body": c["body"], "province": c["province"],
        "candidate_land": c["candidate_land"], "reference_land": c["reference_land"],
        "distance_to_candidate_km": round(c["distance_to_candidate_km"], 2),
        "freeboard_m": history,
    })

uncertainty = float(MODEL["scope"]["deep_time_shoreline_uncertainty_m"])
for age in epochs:
    emerged = robust_land = uncertain = submerged = 0.0
    for c in domain:
        state = structural_elevation(province_params[c["province"]], age)
        fb = state["structural_elevation_m"] - sea_level(age)
        a = c["area_km2"]
        if fb > 0:
            emerged += a
        else:
            submerged += a
        if fb > uncertainty:
            robust_land += a
        elif abs(fb) <= uncertainty:
            uncertain += a
    snapshots[str(age).rstrip("0").rstrip(".") if age else "0"] = {
        "sea_level_m": sea_level(age),
        "emerged_continental_crust_km2": emerged,
        "submerged_continental_crust_km2": submerged,
        "robust_land_gt_plus_150m_km2": robust_land,
        "shoreline_uncertain_plus_minus_150m_km2": uncertain,
        "emerged_planet_fraction": emerged / (4 * math.pi * R * R / 1e6),
    }

exact_candidate_area = float(MEASUREMENTS["global_land_area_km2"])
grid_candidate_error = abs(candidate_grid_area - exact_candidate_area) / exact_candidate_area
crust_area_error = abs(domain_area - target) / target
candidate_positive_fraction = positive_candidate_area / candidate_grid_area if candidate_grid_area else 0
water_negative_fraction = negative_non_candidate_area / non_candidate_domain_area if non_candidate_domain_area else 0
submerged_fraction = non_candidate_domain_area / domain_area if domain_area else 1

if grid_candidate_error > float(validation["grid_candidate_area_relative_error_max"]):
    ERRORS.append(f"1-degree candidate grid area error {grid_candidate_error:.3%} exceeds tolerance.")
if crust_area_error > float(validation["continental_crust_area_relative_tolerance"]):
    ERRORS.append(f"Continental-domain area error {crust_area_error:.3%} exceeds tolerance.")
if candidate_positive_fraction < float(validation["present_candidate_land_positive_fraction_min"]):
    ERRORS.append(f"Only {candidate_positive_fraction:.2%} of candidate grid land is positive freeboard.")
if water_negative_fraction < float(validation["present_non_candidate_continental_water_negative_fraction_min"]):
    ERRORS.append(f"Only {water_negative_fraction:.2%} of non-candidate continental substrate is submerged.")
if not (float(validation["minimum_present_submerged_continental_fraction"]) <= submerged_fraction <= float(validation["maximum_present_submerged_continental_fraction"])):
    ERRORS.append(f"Present submerged continental fraction {submerged_fraction:.2%} falls outside the plausibility band.")
if validation.get("require_zero_net_new_continental_crust") and exact_candidate_area > target:
    ERRORS.append("Candidate emerged land exceeds the total continental-crust inventory.")

# A physically useful shelf model must respond globally to an ordinary strong lowstand.
present_emerged = snapshots["0"]["emerged_continental_crust_km2"]
minus80_emerged = snapshots["0.65"]["emerged_continental_crust_km2"]
global_shelf_response = minus80_emerged - present_emerged
if global_shelf_response < float(validation["minimum_global_shelf_response_km2_at_minus_80m"]):
    ERRORS.append(f"Global shelf response at -80 m is only {global_shelf_response:.0f} km2; shelf field is too rigid/deep.")

# --- Critical local sections below the global-grid resolution ---
sections = MODEL["critical_sections"]
section_results = {}

j = sections["JX1_land_neck"]
j_margin = min(float(v) for v in j["structural_ground_elevation_m_at_3_2ma"]) - float(j["max_local_downward_perturbation_m"]) - float(j["max_tested_highstand_m"])
section_results["JX1_land_neck"] = {"minimum_tested_freeboard_m": j_margin, "pass": j_margin >= float(validation["minimum_human_route_critical_structural_margin_m"])}
if not section_results["JX1_land_neck"]["pass"]:
    ERRORS.append("JX1 land-neck freeboard fails by 3.2 Ma.")

n = sections["NORTHERN_APPROACH_SHELF"]
founder_sill = float(n["critical_sill_elevation_m"])
contact_sill = float(n["small_contact_sill_elevation_m"])
offset = float(n["local_vertical_offset_m"])
def fb_samples(sill, levels):
    return [sill + offset - float(sl) for sl in levels]
h06 = fb_samples(founder_sill, n["H06_sea_level_samples_m"])
h07 = fb_samples(contact_sill, n["H07_sea_level_samples_m"])
h10 = fb_samples(founder_sill, n["H10_sea_level_samples_m"])
n_pass = sum(v >= 0 for v in h06) >= 2 and any(v >= 0 for v in h07) and any(v < 0 for v in h07) and all(v >= 0 for v in h10)
section_results["NORTHERN_APPROACH_SHELF"] = {"H06_freeboard_m": h06, "H07_freeboard_m": h07, "H10_freeboard_m": h10, "pass": n_pass}
if not n_pass:
    ERRORS.append("Northern shelf does not reproduce distinct H06/H07/H10 accessibility states.")

e = sections["EASTERN_SHELF_CHANNELS"]
low = float(e["maximum_tested_lowstand_m"])
channel_fb = [float(v) - low for v in e["channel_sill_elevation_m"]]
e_pass = (float(e["shelf_head_structural_elevation_m"]) > 0
          and all(float(v) > 0 for v in e["stepping_island_structural_elevation_m"])
          and all(v < 0 for v in channel_fb))
section_results["EASTERN_SHELF_CHANNELS"] = {"channel_freeboard_at_lowstand_m": channel_fb, "pass": e_pass}
if not e_pass:
    ERRORS.append("Eastern shelf/channel freeboard fails persistent-water or island-emergence requirements.")

c4 = sections["C4_PERIPHERAL_CORRIDOR"]
warm = [float(v) - float(c4["warm_phase_sea_level_m"]) for v in c4["lowland_structural_elevation_m"]]
cold = [float(v) - float(c4["cold_phase_sea_level_m"]) - float(c4["maximum_local_ice_isostatic_depression_m"]) for v in c4["lowland_structural_elevation_m"]]
c4_pass = all(v > 0 for v in warm) and sum(v > 0 for v in cold) >= 5
section_results["C4_PERIPHERAL_CORRIDOR"] = {"warm_freeboard_m": warm, "cold_loaded_freeboard_m": cold, "pass": c4_pass}
if not c4_pass:
    ERRORS.append("C4 peripheral corridor freeboard fails warm/cold-phase emergence test.")

# Save generated evidence for CI artifact inspection.
with (OUT / "freeboard-grid.jsonl").open("w") as f:
    for row in rows:
        f.write(json.dumps(row, separators=(",", ":")) + "\n")

province_area = {}
for c in domain:
    province_area[c["province"]] = province_area.get(c["province"], 0.0) + c["area_km2"]

summary = {
    "status": "PASS" if not ERRORS else "FAIL",
    "scope": "spatial crustal-thickness/stretching/freeboard existence reconstruction",
    "errors": ERRORS,
    "warnings": WARNINGS,
    "grid_resolution_deg": res,
    "grid_cells_in_continental_domain": len(domain),
    "candidate_exact_area_km2": exact_candidate_area,
    "candidate_grid_area_km2": candidate_grid_area,
    "candidate_grid_area_relative_error": grid_candidate_error,
    "continental_domain_area_km2": domain_area,
    "continental_domain_target_km2": target,
    "continental_domain_relative_error": crust_area_error,
    "maximum_selected_offshore_distance_km": max((c["distance_to_candidate_km"] for c in domain if not c["candidate_land"]), default=0),
    "present_submerged_continental_fraction": submerged_fraction,
    "reference_only_area_retained_inside_erde_continental_domain_km2": reference_only_domain_area,
    "present_candidate_land_positive_fraction": candidate_positive_fraction,
    "present_non_candidate_continental_water_negative_fraction": water_negative_fraction,
    "present_crust_thickness_range_km": [min(all_present_thickness), max(all_present_thickness)],
    "maximum_stretching_beta": max_beta,
    "maximum_absolute_lithosphere_residual_m": max_residual,
    "global_shelf_area_exposed_at_minus_80m_km2": global_shelf_response,
    "province_area_km2": province_area,
    "snapshots": snapshots,
    "critical_section_results": section_results,
    "required_net_new_continental_crust_km2": max(0, exact_candidate_area - target),
    "interpretation": "The present land/water pattern is reproduced by freeboard redistribution within an Earth-scale continental-crust inventory. The source-reference mask is not treated as a prior Erde coastline or as crust that must remain at the same coordinate. The responsive inner-shelf field produces lowstand emergence without turning persistent deep-water channels into land.",
    "remaining_limits": [
        "The 1-degree global mesh is not a DEM and cannot resolve narrow straits, river valleys or individual fault blocks; those are represented by critical sections.",
        "Deep-time eustatic sea level is intentionally not invented. Cells within +/-150 m of the long-term datum remain shoreline-uncertain.",
        "Airy buoyancy is only a first-order term; bounded residuals represent mantle-lithosphere buoyancy, flexure and unresolved regional effects.",
        "Sediment fill is represented as a surface-elevation contribution rather than a full compaction/backstripping calculation.",
        "The model proves a coherent physically ordinary solution exists; it does not establish that this is the unique geological history."
    ],
    "full_mantle_to_climate_validation": False,
}
(OUT / "freeboard-validation-metrics.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary, indent=2))
sys.exit(0 if not ERRORS else 1)
