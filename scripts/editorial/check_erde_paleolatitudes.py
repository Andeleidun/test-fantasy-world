"""Probe the inherited Earth-analogue scaffold in two explicit GPlates models.

Default: replay cached responses. --fetch: obtain the defined public requests.
This checks reconstructed sample locations, not candidate crust or palaeocoasts.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/global-geography-trial'
CACHE = OUT / 'paleolocation-responses'
SAMPLES = {'C1_interior': (-100,50), 'C2_interior': (-60,-10),
           'C3_west': (25,55), 'C3_east': (110,35), 'shelf_cradle': (110,0),
           'C4_core': (30,0), 'ancestral_refuge': (-16,15),
           'ancestral_exit': (32,30), 'C5_interior': (130,-25),
           'C6_interior': (80,-75)}
MODELS = ['MERDITH2021', 'MULLER2022']
TIMES = [0, 2, 23, 66, 100, 150, 200, 250, 300, 450, 600, 1000]
ENDPOINT = 'https://gws.gplates.org/reconstruct/reconstruct_points/'


def native_latitude(lon, lat):
    return math.degrees(math.asin(max(-1, min(1,
        math.cos(math.radians(lat)) * math.cos(math.radians(lon + 150))))))


def request(model, age):
    params = {'lons': ','.join(str(p[0]) for p in SAMPLES.values()),
              'lats': ','.join(str(p[1]) for p in SAMPLES.values()),
              'time': age, 'model': model, 'anchor_plate_id': 0,
              'fc': '', 'return_null_points': ''}
    url = ENDPOINT + '?' + urllib.parse.urlencode(params)
    target = CACHE / f'{model}-{age}Ma.json'
    if args.fetch:
        with urllib.request.urlopen(url, timeout=25) as response:
            raw = response.read().decode()
        payload = {'url': url, 'retrieved_utc': datetime.now(timezone.utc).isoformat(),
                   'response_sha256': hashlib.sha256(raw.encode()).hexdigest(),
                   'raw_response': raw}
        target.write_text(json.dumps(payload, indent=2) + '\n')
    payload = json.loads(target.read_text())
    assert payload['url'] == url
    raw = payload['raw_response']
    assert hashlib.sha256(raw.encode()).hexdigest() == payload['response_sha256']
    data = json.loads(raw)
    if data.get('type') != 'FeatureCollection' or len(data['features']) != len(SAMPLES):
        raise ValueError(f'{model} {age}: response cannot be mapped safely to sample order')
    rows = []
    for (name, original), feature in zip(SAMPLES.items(), data['features']):
        geometry = feature.get('geometry') if feature else None
        coords = geometry.get('coordinates') if geometry else None
        usable = coords is not None and len(coords) == 2 and all(abs(v) <= lim for v, lim in zip(coords, [180,90]))
        if usable and age == 0:
            assert max(abs(a-b) for a,b in zip(coords,original)) < .01, (model,name,coords)
        rows.append({'sample': name, 'present_reference_lonlat': original,
                     'paleo_reference_lonlat': coords,
                     'native_paleolatitude_degrees': native_latitude(*coords) if usable else None,
                     'properties': feature.get('properties', {}) if feature else {},
                     'usable': usable})
    return {'model': model, 'age_Ma': age, 'cache_file': str(target.relative_to(OUT)), 'samples': rows}


args = argparse.ArgumentParser()
args.add_argument('--fetch', action='store_true')
args = args.parse_args()
CACHE.mkdir(exist_ok=True)
with ThreadPoolExecutor(max_workers=4) as executor:
    records = list(executor.map(lambda pair: request(*pair), [(m,t) for m in MODELS for t in TIMES]))
result = {'status': 'inherited-scaffold sample test, not a candidate plate reconstruction',
          'reference_frame': 'native north at source 0N 150W; anchor_plate_id=0 for each explicit model',
          'samples': SAMPLES, 'records': records,
          'limitations': ['Model reference-frame choice materially affects transformed palaeolatitudes.',
                          'Static plate-assigned point reconstructions do not recover elevations, shorelines, complete continental occupancy or climate.',
                          'Candidate margin changes have no assigned block motions; these probes do not validate their histories.',
                          'Agreement at sampled epochs does not establish continuous conditions between them.']}
(OUT / 'paleolatitude-checks.json').write_text(json.dumps(result, indent=2) + '\n')
for record in records:
    print(record['model'],record['age_Ma'], {r['sample']: round(r['native_paleolatitude_degrees'],1) if r['usable'] else None for r in record['samples']})

# Scientific comparison of calculated sample paths, not palaeogeographic maps.
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10, 'svg.fonttype': 'none', 'svg.hashsalt': 'erde-paleolatitude-review-v1'})
fig, axes = plt.subplots(2, 3, figsize=(15, 9), sharex=True, sharey=True, facecolor='#f7f5ef')
selected = [('C1_interior','C1 · interior'),('C2_interior','C2 · interior'),
            ('C3_east','C3 · eastern interior'),('C4_core','C4 · core'),
            ('C5_interior','C5 · interior'),('C6_interior','C6 · interior')]
for ax, (key, title) in zip(axes.flat, selected):
    ax.set_facecolor('#f7f5ef')
    ax.axhspan(-30,30,color='#e3ebdf',zorder=0)
    ax.axhline(0,color='#86918a',lw=.7)
    for model, color, style in [('MERDITH2021','#246682','-'),('MULLER2022','#a95132','--')]:
        points = [(rec['age_Ma'],next(p['native_paleolatitude_degrees'] for p in rec['samples'] if p['sample']==key))
                  for rec in records if rec['model']==model and rec['age_Ma']<=300]
        ax.plot([p[0] for p in points],[p[1] for p in points],style,marker='o',ms=3,color=color,lw=1.8,label=model)
    ax.set_title(title,loc='left',weight='bold',pad=10)
    ax.set_xlim(300,0);ax.set_ylim(-90,90)
    ax.set_yticks([-90,-60,-30,0,30,60,90],['90°S','60°S','30°S','0°','30°N','60°N','90°N'])
    ax.set_xticks([300,200,100,0]);ax.grid(axis='y',alpha=.15)
    ax.spines[['top','right']].set_visible(False)
for ax in axes[1,:]:ax.set_xlabel('Million years before present')
fig.subplots_adjust(top=.80,bottom=.15,left=.065,right=.975,hspace=.32,wspace=.18)
fig.text(.065,.955,'ERDE / GEOLOGICAL VALIDATION',size=11,weight='bold',color='#506562')
fig.text(.065,.90,'Testing inherited latitude histories',size=25,weight='bold',color='#233c43')
fig.text(.065,.855,'Reconstructed sample points in Erde’s frame. These are not reconstructions of the candidate coastlines.',size=12)
handles,labels=axes[0,0].get_legend_handles_labels()
fig.legend(handles,labels,loc='lower left',bbox_to_anchor=(.06,.055),ncol=2,frameon=False)
fig.text(.065,.035,'Shading marks 30°S–30°N, not modeled biomes. Model differences are not statistical confidence intervals. Lines join sampled epochs.',size=10,color='#506562')
for ext in ['png','svg']:
    fig.savefig(OUT/f'04-paleolatitude-checks.{ext}',dpi=140,metadata={'Date':None} if ext=='svg' else None)
plt.close(fig)
