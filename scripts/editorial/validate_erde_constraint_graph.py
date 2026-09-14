"""Validate the dated Erde reconstruction constraint graph.

This bounded validator checks chronology, dependency references, substrate ages,
accessibility ordering, negative constraints, and explicit resolved/unresolved
high-coupling science. Plate motion and freeboard have their own validators.
"""
from __future__ import annotations
from pathlib import Path
import json, sys

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/global-geography-trial'
graph=json.loads((OUT/'dated-constraint-graph.json').read_text())
model=json.loads((OUT/'reconstruction-model.json').read_text())
errors=[]; warnings=[]

requirements={r['id']:r for r in graph['requirements']}
expected={f'H{i:02d}' for i in range(1,13)}
if set(requirements)!=expected:
    errors.append(f"Requirement ledger mismatch: missing={sorted(expected-set(requirements))}, extra={sorted(set(requirements)-expected)}")

objects={}
for collection in ('crustal_units','features'):
    for item in model.get(collection,[]):
        if item['id'] in objects: errors.append(f"Duplicate reconstruction object id: {item['id']}")
        objects[item['id']]=item

for dep in graph.get('dependencies',[]):
    if dep['from'] not in requirements or dep['to'] not in requirements:
        errors.append(f'Dependency references unknown requirement: {dep}')
for req in requirements.values():
    for object_id in req.get('requires',[]):
        if object_id not in objects: errors.append(f"{req['id']} requires unknown object {object_id}")

def established_age(obj):
    for key in ('stable_by_ma','established_by_ma'):
        if key in obj: return float(obj[key])
    substrate=obj.get('substrate')
    return established_age(objects[substrate]) if substrate in objects else None

def interval_covers(feature_interval, requirement_interval):
    f_old,f_young=map(float,feature_interval); r_old,r_young=map(float,requirement_interval)
    return f_old>=r_old and f_young<=r_young

for req in requirements.values():
    window=req.get('window_ma')
    if not window: continue
    req_old=float(window[0])
    for object_id in req.get('requires',[]):
        obj=objects.get(object_id)
        if not obj: continue
        if 'active_interval_ma' in obj:
            if not interval_covers(obj['active_interval_ma'],window):
                errors.append(f"{object_id} active interval {obj['active_interval_ma']} does not cover {req['id']} {window}")
            continue
        age=established_age(obj)
        if age is not None and age<req_old:
            errors.append(f'{object_id} is not established early enough for {req["id"]}: {age} Ma < required {req_old} Ma')

cutoff=float(model['motion_policy']['human_route_sensitive_motion_cutoff_ma'])
for obj in objects.values():
    if not obj.get('human_route_sensitive'): continue
    age=established_age(obj)
    if age is not None and age<cutoff:
        errors.append(f"N01 violation: {obj['id']} stabilizes at {age} Ma, younger than {cutoff} Ma human-route cutoff")
if float(model['motion_policy'].get('c2_extra_euler_rotation_degrees',0))!=0:
    errors.append('Strategy A requires zero extra C2 Euler rotation.')

states={s['id']:s for s in model.get('accessibility_states',[])}
for state_id in ('H06_EARLY_AMERICAN_ACCESS','H10_LATE_AMERICAN_ACCESS'):
    if state_id not in states: errors.append(f'Missing accessibility state {state_id}')
if all(x in states for x in ('H06_EARLY_AMERICAN_ACCESS','H10_LATE_AMERICAN_ACCESS')):
    early=states['H06_EARLY_AMERICAN_ACCESS']['active_interval_ma']; late=states['H10_LATE_AMERICAN_ACCESS']['active_interval_ma']
    if float(early[1])<float(late[0]): errors.append(f'H06/H10 access windows overlap or are reversed: {early}, {late}')
    if states['H06_EARLY_AMERICAN_ACCESS']['substrates']!=states['H10_LATE_AMERICAN_ACCESS']['substrates']:
        warnings.append('H06 and H10 do not use exactly the same old substrate set.')

c4=objects.get('C4_MARGINAL_CORRIDOR',{}); lat_target=c4.get('native_latitude_target_deg_s')
if not lat_target or max(map(float,lat_target))>50: errors.append('C4 marginal corridor must stay within the provisional <=50S peripheral target.')
if 'replaces_reference_route' not in c4: errors.append('C4 route substitution must record which previous route it replaces.')
channels=objects.get('DEEP_WATER_ISLAND_CHANNELS',{})
if channels.get('must_remain_water_through_ma')!=[1.4,0.15]: errors.append('Deep-water island barrier interval must span H03 through H09.')

unresolved={u['id'] for u in model.get('unresolved_constraints',[])}
resolved={u['id']:u for u in model.get('resolved_constraints',[])}
for required_unknown in ('U1','U2','U3','U4'):
    if required_unknown not in unresolved: errors.append(f'Missing explicit unresolved downstream constraint {required_unknown}')
if 'U5' in unresolved: errors.append('U5 freeboard/crustal existence constraint must no longer be listed as unresolved after the passing spatial reconstruction.')
if 'U5' not in resolved: errors.append('Resolved constraint U5 is missing.')
elif resolved['U5'].get('status')!='spatial_freeboard_existence_pass': errors.append('U5 does not record the required spatial freeboard existence pass.')
if model['motion_policy'].get('freeboard_model')!='freeboard-model.json': errors.append('Reconstruction model is not bound to the freeboard model.')

result={
    'status':'PASS' if not errors else 'FAIL',
    'scope':'dated graph / dependency / resolution-state logic',
    'requirements_checked':len(requirements),
    'reconstruction_objects_checked':len(objects),
    'errors':errors,'warnings':warnings,
    'unresolved_constraints':sorted(unresolved),
    'resolved_constraints':sorted(resolved),
    'full_mantle_to_climate_validation':False}
print(json.dumps(result,indent=2)); sys.exit(0 if not errors else 1)
