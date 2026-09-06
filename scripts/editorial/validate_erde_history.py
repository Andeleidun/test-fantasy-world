"""Independent necessary-condition checks on the exported Erde candidate.

This is a geometry and scale audit, not a plate, climate or migration simulation.
Run from any directory with the optional atlas dependencies installed.
"""
from pathlib import Path
import hashlib
import json
import math

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
candidate = unary_union([shape(f['geometry']) for f in json.loads(candidate_path.read_text())['features']])
reference_source = ROOT / 'scripts/editorial/data/reference-land.geojson'
reference = make_valid(FRAME.project_geometry(unary_union([
    shape(g) for g in json.loads(reference_source.read_text())['geometries']
]), GEO))
controls = json.loads((OUT / 'design-controls.json').read_text())
added = candidate.difference(reference)
removed = reference.difference(candidate)
retained = candidate.intersection(reference)

# Sampled latitude parallels avoid modeling a cap rim as one long geodesic edge.
def south_cap(limit):
    return Polygon([*[(float(x), -limit) for x in np.linspace(-180, 180, 1441)],
                    (180, -90), (-180, -90)])


caps = {}
for limit in [50, 60, 70]:
    cap = south_cap(limit)
    caps[str(limit)] = {'reference_land_km2': area(reference.intersection(cap)),
                        'candidate_land_km2': area(candidate.intersection(cap))}

# For a rigid Euler offset: d = 2R asin(sin(angle/2) sin(distance_to_pole)).
def rotation_displacement(native_xy):
    pole = controls['paired_offset']['pole_native']
    alpha = GEOD.inv(*pole, *native_xy)[2] / R
    angle = math.radians(abs(controls['paired_offset']['angle_degrees']))
    return 2 * R * math.asin(math.sin(angle / 2) * math.sin(alpha)) / 1000


rotation = {}
for label, source_xy in {'basin': (-58, -6), 'old_hinge_south': (-75, 8),
                         'southern_body': (-70, -35)}.items():
    distance = rotation_displacement(tr(*source_xy))
    rotation[label] = {'offset_km': distance,
        'mean_rate_cm_year_if_20_Myr': distance / (10 * 20),
        'mean_rate_cm_year_if_40_Myr': distance / (10 * 40),
        'mean_rate_cm_year_if_650_kyr': distance / (10 * .65)}

# These are existing atlas line vertices, not a new mapped mountain inventory.
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
# Diagnostic freshwater-equivalent budget only. No sea-level chronology is inferred.
ice_budget = [{'sea_level_fall_m': h,
    'water_removed_km3_fixed_ocean_area': water_area * h / 1000,
    'ice_volume_change_km3_density_917': water_area * h / 1000 * 1000 / 917,
    'mean_ice_thickness_change_km_over_candidate_land_south_60':
       water_area * h / 1000 * 1000 / 917 / caps['60']['candidate_land_km2']}
    for h in [50, 100, 150]]

# The candidate uses overlapping authorial continental partitions internally.
# Audit the exported world instead of treating those partitions as crustal plates.
result = {
    'status': 'necessary conditions only; historical validity not established',
    'candidate_sha256': hashlib.sha256(candidate_path.read_bytes()).hexdigest(),
    'reference_sha256': hashlib.sha256(reference_source.read_bytes()).hexdigest(),
    'candidate_valid': candidate.is_valid,
    'world_mask_area_km2': {'reference': area(reference), 'candidate': area(candidate),
        'new_land_locations': area(added), 'former_land_locations': area(removed),
        'retained_land_locations': area(retained),
        'gross_location_change': area(added) + area(removed),
        'area_partition_residual_km2': area(added)-area(removed)-(area(candidate)-area(reference))},
    'gross_change_percent_of_reference_land_area':
        100 * (area(added) + area(removed)) / area(reference),
    'southern_latitude_cap_land': caps,
    'C2_finite_offset_scale_test': rotation,
    'unremapped_atlas_relief_vertices': relief,
    'ice_volume_sensitivity_not_prediction': ice_budget,
    'vertical_motion_sensitivity_m': [
        {'rate_mm_year': rate, 'duration_Myr': duration,
         'vertical_change_m': rate * duration * 1000}
        for rate in [.05, .1, .5] for duration in [.65, 1.9]],
    'limitations': [
        'Land-mask changes are locations, not volumes of continental crust created or destroyed.',
        'Planar clipping inserts vertices on longitude/latitude segments; subsequent geodesic area accounting has a small nonzero partition residual. Round gross areas to 0.1 million km2.',
        'No time-indexed plate boundaries, block rotations, palaeoelevations or sea levels are supplied.',
        'Relief samples check reuse of an old overlay only; they do not prove loss of a physical mountain range.',
        'Latitude caps measure possible land substrate, not ice-covered area or habitable area.',
        'Ice budgets neglect changing ocean area, isostasy, geoid, seawater density, thermal expansion and floating-ice effects.',
        'Vertical-motion rates and sea-level scenarios are sensitivity inputs, not selected Erde parameters.'
    ]
}
(OUT / 'geological-validation-metrics.json').write_text(json.dumps(result, indent=2) + '\n')
features = [{'type': 'Feature', 'properties': {'role': role, 'status': 'static difference, not crust provenance'},
             'geometry': mapping(g)} for role, g in [('new_land_locations', added), ('former_land_locations', removed)]]
(OUT / 'land-mask-differences.geojson').write_text(json.dumps({'type': 'FeatureCollection', 'features': features}, separators=(',', ':')) + '\n')
print(json.dumps({k: v for k, v in result.items() if k not in ['unremapped_atlas_relief_vertices', 'limitations']}, indent=2))
