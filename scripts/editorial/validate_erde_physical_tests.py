"""Validate the bounded physical-test model for Erde Strategy A.

This checks internal consistency of the authored physical scenarios. It does not
replace a GCM, ice-sheet model, hydrodynamic model, or plate reconstruction.
"""
from pathlib import Path
import json, sys

ROOT=Path(__file__).resolve().parents[2]
PATH=ROOT/'docs/global-geography-trial/physical-test-model.json'
m=json.loads(PATH.read_text())
errors=[]

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

# Eastern route: repaired crossings stay bounded and the deep channels never dry.
e=m['tests']['eastern_shelf_repaired']
if max(e['approx_center_to_center_legs_km'])>80:
    errors.append('Eastern repaired route still has an excessive individual crossing leg.')
if any(depth>=e['maximum_tested_lowstand_m'] for depth in e['channel_sill_depths_m']):
    errors.append('An eastern deep-water channel becomes emergent at the tested lowstand.')
if not e['freshwater_catchment_present']:
    errors.append('Eastern stepping terranes lack freshwater catchments.')

# C4: route must remain a peripheral, fragmented-but-surviving network.
c4=m['tests']['C4_peripheral_refugia']
if max(c4['corridor_native_latitude_deg_s'])>50:
    errors.append('C4 corridor intrudes too far into the polar interior target.')
if c4['warm_phase_connected_habitat_fraction']<0.70:
    errors.append('C4 warm-phase route is too fragmented for H02.')
if c4['cold_phase_refugia_count']<2:
    errors.append('C4 cold-phase refugial network collapses below two refugia.')
if c4['maximum_contiguous_lowland_ice_occupation_fraction']>=0.50:
    errors.append('C4 lowland ice occupation removes too much peripheral habitat.')

# C3 needs both contact and restriction states, without an easy universal bypass.
c3=m['tests']['C3_internal_filter']
states=c3['states']
contact=any(x['lower_pass'] in ('open','seasonal','restricted') for x in states)
strong_filter=any(x['upper_pass']=='closed' and x['lower_pass']!='open' for x in states)
easy_bypass=any(x['lower_pass']=='open' and x['coastal_bypass'] in ('easy','open') for x in states)
if not contact or not strong_filter or easy_bypass:
    errors.append('C3 contact/filter state machine does not satisfy intermittent-contact constraints.')

# The intentional initial eastern failure must be documented and repaired locally.
if m['tests']['eastern_shelf_initial']['result']!='fail':
    errors.append('Expected initial eastern failure is not recorded.')
if m['overall']['geometry_change_required']!='add two old eastern stepping terranes; no continental silhouette or junction redesign required':
    errors.append('Repair scope drifted beyond the bounded local correction.')

result={'status':'PASS' if not errors else 'FAIL','errors':errors,'scope':'bounded physical scenario consistency only','full_geological_validation':False}
print(json.dumps(result,indent=2))
sys.exit(0 if not errors else 1)
