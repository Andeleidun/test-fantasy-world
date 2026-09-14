"""Validate the bounded physical-test model against regenerated Strategy A geometry.

This checks scenario consistency plus the geometry measurements that the scenarios
actually depend on. It does not replace a GCM, ice-sheet model, hydrodynamic model,
local relative-sea-level model, or plate reconstruction.
"""
from pathlib import Path
import json, sys

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/global-geography-trial'
m=json.loads((OUT/'physical-test-model.json').read_text())
measurements=json.loads((OUT/'measurements.json').read_text())
controls=json.loads((OUT/'design-controls.json').read_text())
errors=[]

if not controls.get('generated_outputs_current'):
    errors.append('Regenerated geometry is stale; run try_erde_global.py before physical validation.')
if not measurements.get('valid_land'):
    errors.append('Regenerated candidate land is invalid.')
if not all(measurements.get('anchors_on_land',{}).values()):
    errors.append('At least one required land anchor is off the regenerated geometry.')
if not all(measurements.get('structural_connectivity',{}).values()):
    errors.append(f"Required structural connection missing: {measurements.get('structural_connectivity')}")

# JX1 must be dry land before the earliest route-sensitive interval.
j=m['tests']['JX1_emergence']
if j['continuous_terrestrial_neck_by_ma'] < j['required_before_ma']:
    errors.append('JX1 terrestrial neck emerges too late.')

# Northern shelf: H06 needs multiple robust windows, H10 a robust later window,
# and H07 must remain intermittent rather than permanently exposed.
n=m['tests']['northern_approach']; s=n['erde_sea_level_scenarios_m']
h06=[v for k,v in s.items() if k.startswith('H06_')]
h07=[v for k,v in s.items() if k.startswith('H07_')]
h10=[v for k,v in s.items() if k.startswith('H10_')]
if sum(v<=n['founder_scale_exposure_threshold_m'] for v in h06)<2:
    errors.append('H06 lacks at least two founder-scale exposure samples.')
if not all(v<=n['founder_scale_exposure_threshold_m'] for v in h10):
    errors.append('H10 is not robustly exposed across sampled states.')
if not (any(v<=n['small_contact_exposure_threshold_m'] for v in h07) and any(v>n['small_contact_exposure_threshold_m'] for v in h07)):
    errors.append('H07 is not intermittent.')

# Eastern route: compare scenario requirements to actual regenerated coastline gaps
# and actual regenerated island area rather than validating JSON in isolation.
e=m['tests']['eastern_shelf_repaired']
actual_gaps=measurements.get('eastern_repaired_water_gaps_km',[])
if len(actual_gaps)!=3 or not all(0 < gap < e['project_max_individual_water_leg_km'] for gap in actual_gaps):
    errors.append(f'Eastern regenerated water gaps fail the physical target: {actual_gaps}')
if any(depth>=e['maximum_tested_lowstand_m'] for depth in e['channel_sill_depths_m']):
    errors.append('An eastern deep-water channel becomes emergent at the tested lowstand.')
if not e['freshwater_catchment_present']:
    errors.append('Eastern stepping terranes lack freshwater catchments.')
areas=measurements.get('terrane_area_km2',{})
for name,target in zip(('EASTERN_STEPPING_TERRANE_A','EASTERN_STEPPING_TERRANE_B'),e['terrane_min_area_km2']):
    if areas.get(name,0)<target:
        errors.append(f'{name} regenerated area {areas.get(name,0):.1f} km2 < target {target:.1f} km2.')

# The second local repair must remain present: C3 east core and shelf cradle are one
# connected land component, without converting the three later water gaps to land.
if not measurements.get('structural_connectivity',{}).get('c3_eastern_core_to_shelf_cradle'):
    errors.append('C5 shelf-head western-root repair no longer connects the shelf cradle to C3.')

# C4: route must remain a peripheral, fragmented-but-surviving network and the
# generated corridor must remain inside the same band used by the physical model.
c4=m['tests']['C4_peripheral_refugia']
actual_c4=measurements.get('c4_marginal_corridor_native_latitude_deg',[])
if len(actual_c4)!=2 or min(actual_c4)<-50 or max(actual_c4)>-25:
    errors.append(f'C4 regenerated corridor left the permitted peripheral band: {actual_c4}')
if max(c4['corridor_native_latitude_deg_s'])>50:
    errors.append('C4 scenario corridor intrudes too far into the polar interior target.')
if c4['warm_phase_connected_habitat_fraction']<0.70:
    errors.append('C4 warm-phase route is too fragmented for H02.')
if c4['cold_phase_refugia_count']<2:
    errors.append('C4 cold-phase refugial network collapses below two refugia.')
if c4['maximum_contiguous_lowland_ice_occupation_fraction']>=0.50:
    errors.append('C4 lowland ice occupation removes too much peripheral habitat.')

# C3 needs both contact and restriction states, without an easy universal bypass.
c3=m['tests']['C3_internal_filter']; states=c3['states']
contact=any(x['lower_pass'] in ('open','seasonal','restricted') for x in states)
strong_filter=any(x['upper_pass']=='closed' and x['lower_pass']!='open' for x in states)
easy_bypass=any(x['lower_pass']=='open' and x['coastal_bypass'] in ('easy','open') for x in states)
if not contact or not strong_filter or easy_bypass:
    errors.append('C3 contact/filter state machine does not satisfy intermittent-contact constraints.')

# Both observed failures and their bounded repairs must stay documented.
if m['tests']['eastern_shelf_initial']['result']!='fail' or m['tests']['eastern_shelf_repaired']['result']!='pass':
    errors.append('Eastern initial failure/repair history is incomplete.')
if m['tests']['shelf_head_root_initial']['result']!='fail' or m['tests']['shelf_head_root_repaired']['result']!='pass':
    errors.append('Shelf-head structural failure/repair history is incomplete.')
if m['overall']['continental_silhouette_or_junction_strategy_change_required']:
    errors.append('Repair scope drifted into a continent-scale strategy change.')

result={
    'status':'PASS' if not errors else 'FAIL',
    'errors':errors,
    'scope':'bounded physical scenario plus regenerated-geometry consistency',
    'actual_eastern_water_gaps_km':actual_gaps,
    'actual_stepping_terrane_area_km2':{k:areas.get(k) for k in ('EASTERN_STEPPING_TERRANE_A','EASTERN_STEPPING_TERRANE_B')},
    'actual_c4_corridor_native_latitude_deg':actual_c4,
    'full_geological_validation':False}
print(json.dumps(result,indent=2))
sys.exit(0 if not errors else 1)
