"""Necessary-condition audit for the current dated Erde reconstruction.

This consumes regenerated Strategy A geometry. It checks land/crust accounting
proxies, polar land sensitivity, retained relief samples, and consistency between
the generated geometry and the dated physical model. It is not a plate, climate,
ice-sheet, sea-level, or migration simulation.
"""
from pathlib import Path
import hashlib
import json
import math
import sys

import numpy as np
from pyproj import Geod
from shapely import make_valid
from shapely.geometry import Polygon, Point, shape, mapping
from shapely.ops import unary_union
from erde_geometry import FRAME, GEO, tr

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/global-geography-trial'
R = 6371008.8
GEOD = Geod(a=R, b=R)


def polygons(g):
    if g.is_empty:
        return []
    if g.geom_type == 'Polygon':
        return [g]
    return [p for c in getattr(g, 'geoms', []) for p in polygons(c)]


def area(g):
    return sum(abs(GEOD.geometry_area_perimeter(p)[0]) for p in polygons(g)) / 1e6


candidate_path = OUT / 'candidate-geography.geojson'
reference_source = ROOT / 'scripts/editorial/data/reference-land.geojson'
controls_path = OUT / 'design-controls.json'
measurements_path = OUT / 'measurements.json'
physical_path = OUT / 'physical-test-model.json'

candidate = unary_union([shape(f['geometry']) for f in json.loads(candidate_path.read_text())['features']])
reference = make_valid(FRAME.project_geometry(unary_union([
    shape(g) for g in json.loads(reference_source.read_text())['geometries']
]), GEO))
controls = json.loads(controls_path.read_text())
measurements = json.loads(measurements_path.read_text())
physical = json.loads(physical_path.read_text())

errors = []
if not controls.get('generated_outputs_current'):
    errors.append('Generated Strategy A outputs are stale; run try_erde_global.py first.')
if not candidate.is_valid:
    errors.append('Candidate land mask is invalid.')
if float(controls.get('paired_offset', {}).get('angle_degrees', 999)) != 0:
    errors.append('Strategy A must not reintroduce the removed C2 rigid offset.')
if not all(measurements.get('anchors_on_land', {}).values()):
    errors.append('At least one established land anchor is off the regenerated candidate.')
if not all(measurements.get('structural_connectivity', {}).values()):
    errors.append('At least one required present structural connection is missing.')

eastern_gaps = measurements.get('eastern_repaired_water_gaps_km', [])
if len(eastern_gaps) != 3 or not all(0 < g < 80 for g in eastern_gaps):
    errors.append(f'Eastern repaired water gaps do not satisfy the bounded geometry test: {eastern_gaps}')

c4_lats = measurements.get('c4_marginal_corridor_native_latitude_deg', [])
if len(c4_lats) != 2 or min(c4_lats) < -50 or max(c4_lats) > -25:
    errors.append(f'C4 marginal corridor left the intended midlatitude peripheral band: {c4_lats}')

# The physical model asks for freshwater-capable stepping islands of at least the
# recorded target areas. Compare that model against actual regenerated geometry.
terrane_area = measurements.get('terrane_area_km2', {})
stepping_targets = physical['tests']['eastern_shelf_repaired']['terrane_min_area_km2']
for name, target in zip(('EASTERN_STEPPING_TERRANE_A', 'EASTERN_STEPPING_TERRANE_B'), stepping_targets):
    actual = terrane_area.get(name, 0)
    if actual < target:
        errors.append(f'{name} area {actual:.1f} km2 is below physical-model target {target:.1f} km2.')

added = candidate.difference(reference)
removed = reference.difference(candidate)
retained = candidate.intersection(reference)

# Sampled latitude parallels avoid representing a cap rim as one long geodesic edge.
def south_cap(limit):
    return Polygon([*[(float(x), -limit) for x in np.linspace(-180, 180, 1441)],
                    (180, -90), (-180, -90)])


caps = {}
for limit in [50, 60, 70]:
    cap = south_cap(limit)
    caps[str(limit)] = {'reference_land_km2': area(reference.intersection(cap)),
                        'candidate_land_km2': area(candidate.intersection(cap))}

# Existing atlas relief lines remain reuse diagnostics, not reconstructed ranges.
relief_source = {
    'paired_southern_spine': [(-75,5),(-76,-10),(-69,-30),(-72,-50)],
    'paired_northern_cordillera': [(-145,61),(-124,48),(-112,35),(-103,22)],
    'continental_collision_belt': [(0,43),(25,39),(45,35),(70,34),(88,29),(100,27)],
    'polar_continent_highlands': [(35,12),(37,0),(33,-15)],
    'island_highlands': [(132,-4),(141,-5),(149,-7)]}
relief = {name: [{'reference_coordinates': p, 'native_coordinates': tr(*p),
                 'reference_on_land': reference.covers(Point(tr(*p))),
                 'candidate_on_land_without_remapping': candidate.covers(Point(tr(*p)))}
                for p in points] for name, points in relief_source.items()}

planet_area = 4 * math.pi * R**2 / 1e6
water_area = planet_area - area(candidate)
ice_budget = [{'sea_level_fall_m': h,
    'water_removed_km3_fixed_ocean_area': water_area * h / 1000,
    'ice_volume_change_km3_density_917': water_area * h / 1000 * 1000 / 917,
    'mean_ice_thickness_change_km_over_candidate_land_south_60':
       water_area * h / 1000 * 1000 / 917 / caps['60']['candidate_land_km2']}
    for h in [50, 100, 150]]

result = {
    'status': 'PASS' if not errors else 'FAIL',
    'scope': 'Strategy A necessary conditions; full geological validity not established',
    'errors': errors,
    'candidate_sha256': hashlib.sha256(candidate_path.read_bytes()).hexdigest(),
    'reference_sha256': hashlib.sha256(reference_source.read_bytes()).hexdigest(),
    'candidate_valid': candidate.is_valid,
    'strategy_A': {
        'c2_extra_offset_degrees': controls.get('paired_offset', {}).get('angle_degrees'),
        'structural_connectivity': measurements.get('structural_connectivity'),
        'eastern_repaired_water_gaps_km': eastern_gaps,
        'c4_marginal_corridor_native_latitude_deg': c4_lats,
        'terrane_area_km2': terrane_area,
    },
    'world_mask_area_km2': {'reference': area(reference), 'candidate': area(candidate),
        'new_land_locations': area(added), 'former_land_locations': area(removed),
        'retained_land_locations': area(retained),
        'gross_location_change': area(added) + area(removed),
        'area_partition_residual_km2': area(added)-area(removed)-(area(candidate)-area(reference))},
    'gross_change_percent_of_reference_land_area':
        100 * (area(added) + area(removed)) / area(reference),
    'southern_latitude_cap_land': caps,
    'unremapped_atlas_relief_vertices': relief,
    'ice_volume_sensitivity_not_prediction': ice_budget,
    'vertical_motion_sensitivity_m': [
        {'rate_mm_year': rate, 'duration_Myr': duration,
         'vertical_change_m': rate * duration * 1000}
        for rate in [.05, .1, .5] for duration in [.65, 1.9]],
    'limitations': [
        'Land-mask changes are locations, not volumes of continental crust created or destroyed.',
        'The JX1 and C4 corridor polygons are surface design envelopes; a full block inventory and crustal budget remain required.',
        'No time-indexed plate boundaries, deformed crustal mesh, palaeoelevation raster, local relative sea-level solution, or GCM is supplied.',
        'Relief samples check reuse of an old overlay only; they do not prove physical mountain continuity.',
        'Latitude caps measure possible land substrate, not ice-covered or habitable area.',
        'Ice budgets neglect changing ocean area, isostasy, geoid, seawater density, thermal expansion and floating-ice effects.',
        'The bounded physical model tests consistency of selected scenarios, not likelihood or uniqueness.'
    ]
}
(OUT / 'geological-validation-metrics.json').write_text(json.dumps(result, indent=2) + '\n')
features = [{'type': 'Feature', 'properties': {'role': role, 'status': 'static difference, not crust provenance'},
             'geometry': mapping(g)} for role, g in [('new_land_locations', added), ('former_land_locations', removed)]]
(OUT / 'land-mask-differences.geojson').write_text(json.dumps({'type': 'FeatureCollection', 'features': features}, separators=(',', ':')) + '\n')
print(json.dumps({k: v for k, v in result.items() if k not in ['unremapped_atlas_relief_vertices', 'limitations']}, indent=2))
sys.exit(0 if not errors else 1)
