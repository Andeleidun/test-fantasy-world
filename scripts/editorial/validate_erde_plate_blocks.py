"""Validate the Strategy A crustal-block and time-indexed plate model.

This is a kinematic and crustal-accounting necessary-condition test. It checks
cached GPlates point circuits, synthetic relative rotations, the 1.9 Ma motion
cutoff, surface-crust provenance, and continental-crust/freeboard accounting.
It is not a mantle-convection, palaeoelevation, or deforming-mesh simulation.
"""
from pathlib import Path
import hashlib
import json
import math
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/global-geography-trial'
CACHE = OUT / 'paleolocation-responses'
MODEL_PATH = OUT / 'plate-block-model.json'
MEASUREMENTS_PATH = OUT / 'measurements.json'

SAMPLES = {
    'C1_interior': (-100, 50),
    'C2_interior': (-60, -10),
    'C3_west': (25, 55),
    'C3_east': (110, 35),
    'shelf_cradle': (110, 0),
    'C4_core': (30, 0),
    'ancestral_refuge': (-16, 15),
    'ancestral_exit': (32, 30),
    'C5_interior': (130, -25),
    'C6_interior': (80, -75),
}
MODELS = ('MERDITH2021', 'MULLER2022')
R_KM = 6371.0088

model = json.loads(MODEL_PATH.read_text())
measurements = json.loads(MEASUREMENTS_PATH.read_text())
errors = []
warnings = []

if measurements.get('generated_outputs_current') is False or measurements.get('status', '').startswith('STALE'):
    errors.append('Strategy A generated measurements are stale; regenerate geometry before plate-block validation.')


def angular_distance_rad(a, b):
    lon1, lat1 = map(math.radians, a)
    lon2, lat2 = map(math.radians, b)
    cos_d = (math.sin(lat1) * math.sin(lat2) +
             math.cos(lat1) * math.cos(lat2) * math.cos(lon2 - lon1))
    return math.acos(max(-1.0, min(1.0, cos_d)))


def great_circle_km(a, b):
    return R_KM * angular_distance_rad(a, b)


def cached_points(reconstruction_model, age):
    path = CACHE / f'{reconstruction_model}-{age}Ma.json'
    if not path.exists():
        errors.append(f'Missing cached GPlates response: {path.name}')
        return {}
    payload = json.loads(path.read_text())
    raw = payload.get('raw_response', '')
    if hashlib.sha256(raw.encode()).hexdigest() != payload.get('response_sha256'):
        errors.append(f'Cached response hash mismatch: {path.name}')
        return {}
    data = json.loads(raw)
    features = data.get('features', [])
    if len(features) != len(SAMPLES):
        errors.append(f'{path.name} cannot be mapped safely to the established sample order.')
        return {}
    result = {}
    for (name, present), feature in zip(SAMPLES.items(), features):
        geometry = feature.get('geometry') if feature else None
        coords = geometry.get('coordinates') if geometry else None
        if coords is None or len(coords) != 2:
            result[name] = None
            continue
        result[name] = {
            'coords': tuple(float(v) for v in coords),
            'pid': feature.get('properties', {}).get('pid'),
            'present': present,
        }
    return result


cached = {(m, age): cached_points(m, age) for m in MODELS for age in (0, 2, 23)}

# Expected plate IDs must remain those captured by the inherited Earth analogue.
for block in model['inherited_rigid_blocks']:
    sample = block['sample']
    allowed = set(block['earth_analogue_plate_ids'])
    for reconstruction_model in MODELS:
        for age in (0, 2, 23):
            row = cached[(reconstruction_model, age)].get(sample)
            if not row:
                errors.append(f'{reconstruction_model} {age} Ma lacks usable sample {sample}.')
                continue
            if row['pid'] not in allowed:
                errors.append(
                    f"{block['id']} / {sample} expected plate IDs {sorted(allowed)} but "
                    f"{reconstruction_model} {age} Ma returned {row['pid']}."
                )


def pair_distance(reconstruction_model, age, first, second):
    rows = cached[(reconstruction_model, age)]
    if not rows.get(first) or not rows.get(second):
        return None
    return great_circle_km(rows[first]['coords'], rows[second]['coords'])


rigid_results = []
for test in model['rigid_cluster_tests']:
    samples = test['samples']
    for reconstruction_model in MODELS:
        if test['id'] in ('C3_MAIN_RIGID_CIRCUIT', 'C3_SE_SLOW_MICROPLATE'):
            first, second = samples
            baseline = pair_distance(reconstruction_model, 0, first, second)
            for age_key, limit in test['max_distance_drift_km'].items():
                age = int(age_key)
                distance = pair_distance(reconstruction_model, age, first, second)
                if baseline is None or distance is None:
                    continue
                drift = abs(distance - baseline)
                rigid_results.append({
                    'test': test['id'], 'model': reconstruction_model,
                    'age_ma': age, 'pair': [first, second],
                    'distance_drift_km': drift, 'limit_km': limit,
                })
                if drift > limit:
                    errors.append(
                        f"{test['id']} {reconstruction_model} {age} Ma pair-distance drift "
                        f"{drift:.2f} km exceeds {limit:.2f} km."
                    )
        elif test['id'] == 'C4_MAIN_RIGID_CIRCUIT':
            pairs = [(samples[0], samples[1]), (samples[0], samples[2]), (samples[1], samples[2])]
            for age_key, limit in test['max_pair_distance_drift_km'].items():
                age = int(age_key)
                for first, second in pairs:
                    baseline = pair_distance(reconstruction_model, 0, first, second)
                    distance = pair_distance(reconstruction_model, age, first, second)
                    if baseline is None or distance is None:
                        continue
                    drift = abs(distance - baseline)
                    rigid_results.append({
                        'test': test['id'], 'model': reconstruction_model,
                        'age_ma': age, 'pair': [first, second],
                        'distance_drift_km': drift, 'limit_km': limit,
                    })
                    if drift > limit:
                        errors.append(
                            f"{test['id']} {reconstruction_model} {age} Ma {first}/{second} "
                            f"drift {drift:.2f} km exceeds {limit:.2f} km."
                        )

# Gateways need not be rigid, but their parent blocks cannot separate so rapidly
# after 2 Ma that the physical connection would require continent-scale repair.
gateway_pair_samples = {
    'JX1_JUNCTION_NETWORK': ('C1_interior', 'C2_interior'),
    'C4_C3_COLLISIONAL_CORRIDOR': ('C3_west', 'ancestral_refuge'),
    'NORTHERN_APPROACH_BOUNDARY': ('C1_interior', 'C3_east'),
}
gateway_results = []
for network in model['deforming_networks']:
    pair = gateway_pair_samples.get(network['id'])
    if not pair:
        continue
    for reconstruction_model in MODELS:
        d0 = pair_distance(reconstruction_model, 0, *pair)
        d2 = pair_distance(reconstruction_model, 2, *pair)
        if d0 is None or d2 is None:
            continue
        drift = abs(d2 - d0)
        limit = network['post_2ma_parent_distance_drift_limit_km']
        gateway_results.append({
            'network': network['id'], 'model': reconstruction_model,
            'pair': list(pair), 'distance_drift_0_to_2ma_km': drift,
            'limit_km': limit,
        })
        if drift > limit:
            errors.append(
                f"{network['id']} {reconstruction_model} parent-block drift over 0-2 Ma "
                f"is {drift:.2f} km, exceeding {limit:.2f} km."
            )

# Finite relative rotations are checked using a representative point and spherical
# Rodrigues rotation. Stage speeds are chord-independent great-circle displacement.
def lonlat_to_vec(lonlat):
    lon, lat = map(math.radians, lonlat)
    return [math.cos(lat) * math.cos(lon), math.cos(lat) * math.sin(lon), math.sin(lat)]


def vec_to_lonlat(v):
    x, y, z = v
    norm = math.sqrt(x*x + y*y + z*z)
    x, y, z = x/norm, y/norm, z/norm
    return (math.degrees(math.atan2(y, x)), math.degrees(math.asin(max(-1, min(1, z)))))


def rotate_point(point, pole, angle_deg):
    v = lonlat_to_vec(point)
    k = lonlat_to_vec(pole)
    a = math.radians(angle_deg)
    c, s = math.cos(a), math.sin(a)
    dot = sum(vi * ki for vi, ki in zip(v, k))
    cross = [
        k[1]*v[2] - k[2]*v[1],
        k[2]*v[0] - k[0]*v[2],
        k[0]*v[1] - k[1]*v[0],
    ]
    result = [v[i]*c + cross[i]*s + k[i]*dot*(1-c) for i in range(3)]
    return vec_to_lonlat(result)


rotation_results = []
max_relative_speed = model['scientific_constraints']['max_relative_block_speed_cm_per_year']
cutoff = model['scientific_constraints']['human_route_sensitive_continent_scale_motion_cutoff_ma']
for block in model['synthetic_relative_rotations']:
    records = sorted(block['rotations'], key=lambda r: r['age_ma'], reverse=True)
    completion = block['nonzero_motion_complete_by_ma']
    if block.get('human_route_sensitive') and completion < cutoff:
        errors.append(
            f"{block['block']} completes synthetic relative motion at {completion} Ma, "
            f"younger than the {cutoff} Ma human-route cutoff."
        )
    for record in records:
        if record['age_ma'] <= completion and abs(record['angle_deg']) > 1e-9:
            errors.append(
                f"{block['block']} retains non-zero {record['angle_deg']}° relative rotation "
                f"at {record['age_ma']} Ma after its {completion} Ma completion gate."
            )
    for older, younger in zip(records, records[1:]):
        dt_ma = older['age_ma'] - younger['age_ma']
        if dt_ma <= 0:
            errors.append(f"{block['block']} has non-descending rotation ages.")
            continue
        p_old = rotate_point(block['representative_source_lonlat'], block['euler_pole_source_lonlat'], older['angle_deg'])
        p_young = rotate_point(block['representative_source_lonlat'], block['euler_pole_source_lonlat'], younger['angle_deg'])
        displacement_km = great_circle_km(p_old, p_young)
        # 1 km/Myr = 0.1 cm/yr.
        speed_cm_yr = displacement_km / dt_ma * 0.1
        rotation_results.append({
            'block': block['block'], 'older_ma': older['age_ma'],
            'younger_ma': younger['age_ma'], 'angle_change_deg': younger['angle_deg'] - older['angle_deg'],
            'representative_displacement_km': displacement_km,
            'representative_speed_cm_per_year': speed_cm_yr,
        })
        if speed_cm_yr > max_relative_speed:
            errors.append(
                f"{block['block']} stage {older['age_ma']}-{younger['age_ma']} Ma "
                f"requires {speed_cm_yr:.2f} cm/yr, exceeding {max_relative_speed:.2f} cm/yr."
            )

# Surface-province provenance must close and broad provinces cannot be mostly young
# juvenile crust. Actual generated areas are taken from the Cartopy regeneration.
terrane_areas = measurements.get('terrane_area_km2', {})
large_min = 100000.0
inherited_threshold = model['scientific_constraints']['large_synthetic_province_min_inherited_or_reworked_fraction']
juvenile_area = 0.0
provenance_results = []
for province in model['surface_crust_provenance']:
    fractions = province['fractions']
    total_fraction = sum(fractions.values())
    if abs(total_fraction - 1.0) > 1e-9:
        errors.append(f"{province['surface_feature']} provenance fractions sum to {total_fraction:.6f}, not 1.")
    area_km2 = float(terrane_areas.get(province['surface_feature'], 0.0))
    if area_km2 <= 0:
        errors.append(f"No regenerated area available for {province['surface_feature']}.")
    inherited = sum(value for key, value in fractions.items() if ('old_' in key or 'reworked_' in key))
    juvenile = sum(value for key, value in fractions.items() if 'juvenile_' in key)
    juvenile_area += area_km2 * juvenile
    provenance_results.append({
        'surface_feature': province['surface_feature'], 'area_km2': area_km2,
        'inherited_or_reworked_fraction': inherited,
        'juvenile_fraction': juvenile,
        'juvenile_area_km2': area_km2 * juvenile,
    })
    if area_km2 >= large_min and inherited < inherited_threshold:
        errors.append(
            f"{province['surface_feature']} is {area_km2:.0f} km² but only "
            f"{inherited:.1%} inherited/reworked, below {inherited_threshold:.1%}."
        )

continental_crust_area = model['hypsometric_accounting']['reference_continental_crust_area_km2']
juvenile_fraction_global = juvenile_area / continental_crust_area
max_juvenile_global = model['scientific_constraints']['max_juvenile_area_fraction_of_total_continental_crust']
if juvenile_fraction_global > max_juvenile_global:
    errors.append(
        f'Synthetic juvenile continental-crust area is {juvenile_area:.0f} km² '
        f'({juvenile_fraction_global:.3%} of the crust inventory), exceeding '
        f'{max_juvenile_global:.3%}.'
    )

for body, fractions in model['body_surface_partition_fractions'].items():
    total = sum(fractions.values())
    if abs(total - 1.0) > 1e-9:
        errors.append(f'{body} surface partition fractions sum to {total:.6f}, not 1.')

# Hypsometric accounting: emerged land may change greatly without creating new
# continental crust, provided total emerged area remains below the continental
# crust inventory and its share is plausible.
candidate_land = measurements.get('global_land_area_km2')
if candidate_land is None:
    errors.append('Regenerated measurements lack global_land_area_km2.')
    candidate_land = 0.0
planet_area = 4 * math.pi * R_KM**2
candidate_fraction = candidate_land / planet_area if planet_area else 0
min_crust_fraction, max_crust_fraction = model['scientific_constraints']['continental_crust_fraction_plausible_range']
if candidate_fraction >= min_crust_fraction:
    errors.append(
        f'Candidate emerged land fraction {candidate_fraction:.3%} leaves insufficient '
        f'room below the minimum {min_crust_fraction:.1%} total continental-crust coverage.'
    )
emerged_share = candidate_land / continental_crust_area if continental_crust_area else 0
share_min, share_max = model['scientific_constraints']['candidate_emerged_share_of_continental_crust_plausible_range']
if not (share_min <= emerged_share <= share_max):
    errors.append(
        f'Candidate emerged share of continental crust {emerged_share:.2%} is outside '
        f'{share_min:.0%}-{share_max:.0%}.'
    )
required_new_crust = max(0.0, candidate_land - continental_crust_area)
if required_new_crust > model['hypsometric_accounting']['maximum_net_new_continental_crust_required_km2'] + 1e-6:
    errors.append(f'Candidate requires {required_new_crust:.0f} km² of net new continental crust.')
submerged_continental_crust = max(0.0, continental_crust_area - candidate_land)

# Quantify how much of each redesigned body is genuinely relocated surface area.
# For candidate area A, reference B and IoU q, intersection I=q(A+B)/(1+q).
body_relocation = {}
for body, values in measurements.get('continents', {}).items():
    a = values.get('candidate_body_area_km2')
    b = values.get('baseline_partition_area_km2')
    q = values.get('footprint_intersection_over_union')
    if a is None or b is None or q is None:
        continue
    intersection = q * (a + b) / (1 + q)
    added = max(0.0, a - intersection)
    removed = max(0.0, b - intersection)
    body_relocation[body] = {
        'candidate_area_km2': a, 'reference_partition_area_km2': b,
        'intersection_km2': intersection,
        'new_surface_land_locations_km2': added,
        'former_surface_land_locations_km2': removed,
        'gross_surface_location_change_km2': added + removed,
    }

# Timeline must be explicit, descending and include the hard human-route gate.
timeline_ages = [row['age_ma'] for row in model['timeline']]
if timeline_ages != sorted(timeline_ages, reverse=True):
    errors.append('Plate-reconstruction timeline is not in descending age order.')
for required_age in (1.9, 0):
    if required_age not in timeline_ages:
        errors.append(f'Plate-reconstruction timeline lacks required {required_age} Ma state.')

metrics = {
    'status': 'PASS' if not errors else 'FAIL',
    'scope': 'Strategy A crustal-block / finite-rotation / crustal-budget necessary conditions',
    'errors': errors,
    'warnings': warnings,
    'reference_frames_checked': list(MODELS),
    'rigid_cluster_results': rigid_results,
    'gateway_parent_drift_results': gateway_results,
    'synthetic_rotation_stage_results': rotation_results,
    'surface_provenance_results': provenance_results,
    'juvenile_synthetic_continental_crust_area_km2': juvenile_area,
    'juvenile_synthetic_fraction_of_target_continental_crust': juvenile_fraction_global,
    'hypsometric_accounting': {
        'planet_area_km2': planet_area,
        'candidate_emerged_land_area_km2': candidate_land,
        'candidate_emerged_land_fraction': candidate_fraction,
        'target_total_continental_crust_area_km2': continental_crust_area,
        'candidate_emerged_share_of_target_continental_crust': emerged_share,
        'required_submerged_continental_crust_km2': submerged_continental_crust,
        'required_net_new_continental_crust_km2': required_new_crust,
    },
    'body_surface_relocation': body_relocation,
    'human_route_sensitive_motion_cutoff_ma': cutoff,
    'full_geological_validation': False,
    'remaining_high_fidelity_requirements': model['remaining_high_fidelity_requirements'],
}
(OUT / 'plate-reconstruction-metrics.json').write_text(json.dumps(metrics, indent=2) + '\n')
print(json.dumps(metrics, indent=2))
sys.exit(0 if not errors else 1)
