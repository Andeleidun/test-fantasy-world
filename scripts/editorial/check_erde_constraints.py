#!/usr/bin/env python3
"""Check the authored constraint model; this is not a geological simulator.

Uses exact decimal, strict difference constraints. No network or dependencies.
"""
import argparse
import copy
from decimal import Decimal
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT = ROOT / 'docs/continental-constraint-graph/graph.json'


def tighter(a, b):
    return b is None or a[0] < b[0] or (a[0] == b[0] and a[1] and not b[1])


def chronology(events, relations):
    """x = age in Ma BP. (bound, strict) means x_v - x_u <=/< bound."""
    ids = ['ZERO'] + [e['id'] for e in events]
    at = {name: i for i, name in enumerate(ids)}
    n = len(ids)
    d = [[None] * n for _ in ids]
    for i in range(n):
        d[i][i] = (Decimal(0), False)

    def edge(u, v, value, strict=False):
        pair = (Decimal(str(value)), strict)
        if tighter(pair, d[at[u]][at[v]]):
            d[at[u]][at[v]] = pair

    for e in events:
        lo, hi = e['age_Ma_BP']
        edge(e['id'], 'ZERO', -Decimal(str(lo)))
        if hi is not None:
            edge('ZERO', e['id'], hi)
    for r in relations:
        # older >= younger; no invented minimum duration for strict precedence.
        edge(r['older'], r['younger'], 0, r['strict'])
    for k in range(n):
        for i in range(n):
            if d[i][k] is None:
                continue
            for j in range(n):
                if d[k][j] is None:
                    continue
                v = (d[i][k][0] + d[k][j][0], d[i][k][1] or d[k][j][1])
                if tighter(v, d[i][j]):
                    d[i][j] = v
    conflicts = [ids[i] for i in range(n)
                 if d[i][i][0] < 0 or (d[i][i][0] == 0 and d[i][i][1])]
    if conflicts:
        return {'feasible': False, 'conflict_events': conflicts}
    windows = {}
    for name in ids[1:]:
        i = at[name]
        windows[name] = {
            'youngest_Ma_BP': float(-d[i][0][0]),
            'youngest_exclusive': d[i][0][1],
            'oldest_Ma_BP': None if d[0][i] is None else float(d[0][i][0]),
            'oldest_exclusive': False if d[0][i] is None else d[0][i][1],
        }
    return {'feasible': True, 'derived_windows': windows,
            'scope': 'Existential event chronology only; no chosen dates, durations, terrain or migration success.'}


def validate(g):
    errors = []
    groups = ['sources', 'continents', 'events', 'dependencies', 'gateways',
              'requirements', 'choices', 'evidence', 'process_constraints',
              'temporal_relations']
    indices = {}
    seen = set()
    for group in groups:
        indices[group] = {n['id']: n for n in g[group]}
        for n in g[group]:
            if n['id'] in seen:
                errors.append('Duplicate ID: ' + n['id'])
            seen.add(n['id'])
    def refs(values, group, owner):
        for v in values:
            if v not in indices[group]:
                errors.append(f'{owner}: unknown {group} reference {v}')
    for group in groups[1:]:
        for n in g[group]:
            refs(n.get('sources', []), 'sources', n['id'])
            if not n.get('sources'):
                errors.append(n['id'] + ': missing provenance')
    for c in g['continents']:
        refs(c['dependencies'], 'dependencies', c['id'])
    if set(indices['continents']) != {f'C{i}' for i in range(1, 7)}:
        errors.append('All six continental groups are mandatory')
    for e in g['events']:
        lo, hi = e['age_Ma_BP']
        if lo < 0 or (hi is not None and lo > hi):
            errors.append(e['id'] + ': reversed/negative age range')
        if e['date_status'] not in ('adopted_window', 'undated', 'adopted_deadline'):
            errors.append(e['id'] + ': authored scenario age cannot become hard chronology')
    for r in g['temporal_relations']:
        refs([r['older'], r['younger']], 'events', r['id'])
        refs(r['sources'], 'sources', r['id'])
        if not isinstance(r['strict'], bool):
            errors.append(r['id'] + ': strict must be boolean')
    for d in g['dependencies']:
        refs(d['depends_on'], 'dependencies', d['id'])
        if d['status'] not in ('unknown', 'conditional', 'validated'):
            errors.append(d['id'] + ': invalid evidence status')
        refs(d['evidence'], 'evidence', d['id'])
        if d['status'] == 'validated' and not d['evidence']:
            errors.append(d['id'] + ': validated dependency needs evidence')
    for w in g['gateways']:
        refs(w['events'], 'events', w['id'])
        refs(w['dependencies'], 'dependencies', w['id'])
        if not w['negative_test'] or not w['positive_test']:
            errors.append(w['id'] + ': needs access and barrier tests')
    if set(indices['requirements']) != {f'H{i:02}' for i in range(1, 13)}:
        errors.append('H01–H12 coverage is incomplete')
    for h in g['requirements']:
        refs(h['events'], 'events', h['id'])
        refs(h['gateways'], 'gateways', h['id'])
        refs(h['dependencies'], 'dependencies', h['id'])
        if not h['acceptance_test']:
            errors.append(h['id'] + ': missing acceptance test')
    for c in g['choices']:
        refs(c['gateways'], 'gateways', c['id'])
        if c['operator'] != 'exactly_one' or len(c['options']) < 2:
            errors.append(c['id'] + ': architecture alternatives need exclusive choice')
        if c['selected'] is not None and c['selected'] not in [o['id'] for o in c['options']]:
            errors.append(c['id'] + ': unknown selected alternative')
    if errors:
        return {'schema_pass': False, 'errors': errors, 'historical_acceptance': False}
    temporal = chronology(g['events'], g['temporal_relations'])
    def closure(start):
        result = set(start)
        todo = list(start)
        while todo:
            for parent in indices['dependencies'][todo.pop()]['depends_on']:
                if parent not in result:
                    result.add(parent)
                    todo.append(parent)
        return result
    gates = {}
    for h in g['requirements']:
        deps = set(h['dependencies'])
        for w in h['gateways']:
            deps.update(indices['gateways'][w]['dependencies'])
        all_deps = closure(deps)
        blockers = sorted(d for d in all_deps if indices['dependencies'][d]['status'] != 'validated')
        unresolved_choices = sorted(c['id'] for c in g['choices']
                                    if c['selected'] is None and set(c['gateways']) & set(h['gateways']))
        # Evidence prerequisites never substitute for an actual requirement-level review.
        accepted = (temporal['feasible'] and not blockers and not unresolved_choices
                    and h['review_status'] == 'validated')
        gates[h['id']] = {'accepted': accepted, 'blocking_dependencies': blockers,
                         'unselected_architectures': unresolved_choices,
                         'review_status': h['review_status']}
    impact = {d: [h for h, v in gates.items() if d in v['blocking_dependencies']]
              for d in indices['dependencies']}
    return {'schema_pass': True, 'errors': [], 'chronology': temporal,
            'requirements': gates, 'dependency_impact': impact,
            'historical_acceptance': all(h['accepted'] for h in gates.values()),
            'limits': ['Physical feedback cycles are allowed, not temporal precedence cycles.',
                       'Alternatives are not conjoined or certified by this validator.',
                       'Existential events do not prove repeated openings or process duration.']}


def self_test(g):
    checks = {}
    def mutated(name, change, predicate):
        other = copy.deepcopy(g)
        change(other)
        checks[name] = bool(predicate(validate(other)))
    def date(graph, node, bounds):
        next(e for e in graph['events'] if e['id'] == node)['age_Ma_BP'] = bounds
    mutated('reject_substrate_younger_than_cradle',
            lambda x: date(x, 'E_CRADLE_READY', [1.0, 1.0]),
            lambda r: not r['chronology']['feasible'])
    mutated('reject_reversed_inherited_branch_order',
            lambda x: x['temporal_relations'].append({'id': 'TEST', 'older': 'E_HA_BRANCH',
                  'younger': 'E_HE_BRANCH', 'strict': True, 'sources': ['S_CANON']}),
            lambda r: not r['chronology']['feasible'])
    mutated('reject_equal_time_for_strict_precedence',
            lambda x: (date(x, 'E_HE_BRANCH', [1.2, 1.2]), date(x, 'E_HA_BRANCH', [1.2, 1.2])),
            lambda r: not r['chronology']['feasible'])
    mutated('reject_missing_historical_requirement',
            lambda x: x['requirements'].pop(), lambda r: not r['schema_pass'])
    mutated('reject_dangling_gateway_reference',
            lambda x: x['requirements'][0]['gateways'].append('MISSING'),
            lambda r: not r['schema_pass'])
    result = validate(g)
    checks['physical_feedback_does_not_cause_temporal_failure'] = result['chronology']['feasible']
    checks['unknown_physics_never_passes_acceptance'] = not result['historical_acceptance']
    checks['unselected_or_routes_remain_unresolved'] = bool(result['requirements']['H04']['unselected_architectures'])
    checks['undated_ancient_event_keeps_unbounded_oldest_age'] = (
        result['chronology']['derived_windows']['E_CRADLE_READY']['oldest_Ma_BP'] is None)
    checks['no_fabricated_settlement_order'] = chronology([
        {'id': 'HE', 'age_Ma_BP': [.6, 1.]}, {'id': 'HA', 'age_Ma_BP': [.45, .65]}],
        [{'older': 'HA', 'younger': 'HE', 'strict': True}])['feasible']
    assert all(checks.values()), checks
    return checks


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--graph', type=Path, default=DEFAULT)
    p.add_argument('--output', type=Path)
    p.add_argument('--self-test', action='store_true')
    args = p.parse_args()
    raw = args.graph.read_bytes()
    g = json.loads(raw)
    result = validate(g)
    result['graph_sha256'] = hashlib.sha256(raw).hexdigest()
    if args.self_test:
        result['negative_and_scope_controls'] = self_test(g)
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'schema_pass': result['schema_pass'],
                      'chronology_feasible': result.get('chronology', {}).get('feasible'),
                      'historical_acceptance': result['historical_acceptance'],
                      'controls_passed': len(result.get('negative_and_scope_controls', {})),
                      'errors': result['errors']}))
    raise SystemExit(0 if result['schema_pass'] and result['chronology']['feasible'] else 1)


if __name__ == '__main__':
    main()
