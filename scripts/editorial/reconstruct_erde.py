"""Bounded authorial reconstruction; no network during generation.

The saved input scenario is an authored hypothesis. Numerical agreement with its
parameters is internal consistency, never independent proof of habitat or history.
"""
from pathlib import Path
import json, math, hashlib, argparse, subprocess, os
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from shapely import make_valid
from shapely.geometry import shape, mapping, Point, Polygon, LineString
from shapely.ops import unary_union, transform
from erde_geometry import FRAME, GEO, GLOBE, PROJECTION, tr, C
from pyproj import Geod
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/geological-reconstruction'
GEOD=Geod(a=6371008.8,b=6371008.8)
CENTERS={'C1':(-107,45),'C2':(-63,-15),'C3':(75,45),'C4':(15,0),'C5':(141,-25),'C6':(0,-90)}
CORE={'C1':(-100,50),'C2':(-60,-10),'C3':(110,35),'C4':(30,0),'C5':(130,-25),'C6':(80,-75)}
PID={'C1':101,'C2':201,'C3':601,'C4':712,'C5':8011,'C6':8031}

def parts(g):
 if g.is_empty:return []
 if g.geom_type=='Polygon':return [g]
 return [p for x in getattr(g,'geoms',[]) for p in parts(x)]
def area(g):return sum(abs(GEOD.geometry_area_perimeter(p)[0]) for p in parts(g))/1e6

def local_projection(refcenter):return ccrs.LambertAzimuthalEqualArea(*tr(*refcenter),globe=GLOBE)
def project(g,src,dst):
 if src != GEO:
  return make_valid(dst.project_geometry(g,src))
 def fn(x,y,z=None):
  p=dst.transform_points(src,np.asarray(x),np.asarray(y));return p[...,0],p[...,1]
 return make_valid(transform(fn,g))
def buffer(g,km,center):
 p=local_projection(center);return project(project(g,GEO,p).buffer(km*1000),p,GEO)
def circle(ref,km):return buffer(Point(tr(*ref)),km,ref)
def line(refpoints):return LineString([tr(*p) for p in refpoints])
def smooth(v):
 v=np.array(v,dtype=float)
 for _ in range(2):
  n=np.roll(v,-1,axis=0);v=np.stack([.8*v+.2*n,.2*v+.8*n],axis=1).reshape(-1,2)
 return make_valid(FRAME.project_geometry(Polygon(v),GEO))
def feature(g,**props):return {'type':'Feature','properties':props,'geometry':mapping(g)}
def writegeo(name,features):
 (OUT/name).write_text(json.dumps({'type':'FeatureCollection','features':features},separators=(',',':'))+'\n')
def writejson(name,data):(OUT/name).write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
def covers_path(land,path):return land.covers(path)
def connected(land,pts):return any(all(p.covers(Point(x)) for x in pts) for p in parts(land))

def load_components():
 tmp=Path('/tmp/erde-reconstruction-components');tmp.mkdir(exist_ok=True)
 env=dict(os.environ,ERDE_TRIAL_OUTPUT=str(tmp),ERDE_EXPORT_COMPONENTS='1',ERDE_GEOMETRY_ONLY='1')
 subprocess.run(['python',str(ROOT/'scripts/editorial/try_erde_global.py')],env=env,stdout=subprocess.DEVNULL,check=True,timeout=45)
 features=json.loads((tmp/'components.geojson').read_text())['features']
 target={f['properties']['group']:shape(f['geometry']) for f in features if f['properties']['kind']=='body'}
 old={f['properties']['group']:shape(f['geometry']) for f in features if f['properties']['kind']=='reference'}
 islands=unary_union([shape(f['geometry']) for f in features if f['properties']['kind']=='islands'])
 controls=json.loads((tmp/'design-controls.json').read_text())
 return target,old,islands,controls


def make_candidate(target,old,islands,controls,radius):
 bodies={}; domains={}
 for c in target:
  original=target[c]
  if c=='C2':original=smooth(controls['reference_frame_vertices']['C2'])
  # A proximity bound limits unassigned oceanward growth. It is explicitly NOT
  # an observed continental-crust boundary or a validated stretched margin.
  domains[c]=buffer(old[c],radius,CENTERS[c])
  bodies[c]=make_valid(original.intersection(domains[c]))
 # Preserve the actual approach sectors and both sides of their connections.
 for guard in controls['historical_control_sectors']:
  disk=circle(guard['reference_center'],guard['radius_km'])
  for c in bodies:bodies[c]=make_valid(bodies[c].difference(disk).union(old[c].intersection(disk)))
 # A western inherited arc joins the polar periphery to the western mainland.
 western=line([(-10,31),(-6,35),(-5,38),(-3,42)])
 neck=buffer(western,85,(-6,36))
 bodies['C4']=make_valid(bodies['C4'].union(neck.intersection(circle((-7,34),420))))
 bodies['C3']=make_valid(bodies['C3'].union(neck))
 # Ensure an inland coastal plain joins the old refugial sector to the neck.
 refuge_route=line([(-16,15),(-14,21),(-10,27),(-10,31),(-6,35),(-5,38),(-3,42),(8,45),(20,42)])
 plain=buffer(refuge_route,65,(-6,32))
 # This local collar is inherited/uplifted basement, not a Quaternary land fill.
 bodies['C4']=make_valid(bodies['C4'].union(plain.intersection(circle((-12,24),1450))))
 bodies['C3']=make_valid(bodies['C3'].union(plain.intersection(circle((5,42),1300))))
 # Submerged inherited basement remains crust; do not invent a circular island
 # merely to force an obsolete highland locator onto present dry land.
 land=make_valid(unary_union([*bodies.values(),islands]))
 return bodies,land,domains,refuge_route


def build_arc(land):
 # A proposed inherited continental ribbon plus accreted arc, shown at full
 # scale. Deep transverse channels divide it; they never emerge at lowstand.
 center=(128,-3);p=local_projection(center)
 path=project(line([(113,-1),(119,0),(124,1),(129,-1),(135,-3),(141,-6)]),GEO,p)
 ribbon=path.buffer(90000,cap_style=1)
 cuts=[]
 # Fixed geographic cuts are tested against the entire land mask below.
 for fraction in [.15,.30,.46,.62,.79]:
  s=path.length*fraction;q=path.interpolate(s)
  a=path.interpolate(s-1000);b=path.interpolate(s+1000)
  direction=np.array([b.x-a.x,b.y-a.y]);direction/=np.linalg.norm(direction)
  normal=np.array([-direction[1],direction[0]])
  center_xy=np.array([q.x,q.y]);section=LineString([center_xy-700000*normal,center_xy+700000*normal])
  cuts.append(section.buffer(10000,cap_style=2))
 patch=circle(center,2800)
 local_land=project(land.intersection(patch),GEO,p)
 # Cuts apply only inside the proposed ribbon; outside coastline is preserved.
 arc=ribbon.difference(unary_union(cuts))
 revised=make_valid(local_land.union(arc).difference(unary_union(cuts).intersection(ribbon.buffer(120000))))
 native=make_valid(land.difference(patch).union(project(revised,p,GEO)))
 cut_native=[project(c.intersection(ribbon.buffer(120000)),p,GEO) for c in cuts]
 return native,project(arc,p,GEO),cut_native


def rotation(lon,lat,pole):
 l,p=np.radians([np.asarray(lon),np.asarray(lat)]);v=np.stack([np.cos(p)*np.cos(l),np.cos(p)*np.sin(l),np.sin(p)],axis=-1)
 lo,la,an=np.radians(pole);k=np.array([np.cos(la)*np.cos(lo),np.cos(la)*np.sin(lo),np.sin(la)])
 w=v*np.cos(an)+np.cross(k,v)*np.sin(an)+np.sum(k*v,axis=-1)[...,None]*k*(1-np.cos(an))
 return np.degrees(np.arctan2(w[...,1],w[...,0])),np.degrees(np.arcsin(np.clip(w[...,2],-1,1)))

def core_history():
 payload=json.loads((OUT/'rotation-cache.json').read_text());raw=payload['raw_response']
 assert hashlib.sha256(raw.encode()).hexdigest()==payload['sha256']
 model=json.loads(raw);records=[]
 for t in sorted(float(x) for x in model):
  for c,present in CORE.items():
   pole=model[str(float(t))][str(PID[c])]
   if t>0 and abs(pole[2])<1e-8:raise ValueError('Unexpected identity rotation; missing plate cannot pass')
   paleo=rotation(*present,pole);native=tr(*paleo)
   records.append({'group':c,'age_Ma':t,'plate_id':PID[c],'source_lonlat':list(map(float,paleo)),'native_lonlat':list(map(float,native)),'euler_pole_source_lon_lat_angle':pole})
 # Independent cached point service checks transformation sign and frame.
 pointdata=json.loads((ROOT/'docs/global-geography-trial/paleolatitude-checks.json').read_text())
 names={'C1':'C1_interior','C2':'C2_interior','C3':'C3_east','C4':'C4_core','C5':'C5_interior','C6':'C6_interior'}
 errors=[]
 for r in records:
  prior=next((x for x in pointdata['records'] if x['model']=='MULLER2022' and x['age_Ma']==r['age_Ma']),None)
  if prior:
   pt=next(x for x in prior['samples'] if x['sample']==names[r['group']])
   if pt['usable']:errors.append(abs(r['native_lonlat'][1]-pt['native_paleolatitude_degrees']))
 assert max(errors)<.001
 return records,max(errors)


def gateway_tests(scenario):
 # Common sea-level envelope includes highstands, lowstands and vertical/local
 # uncertainty. All bounds are authorial inputs, not a fitted climate output.
 sl=scenario['sea_level_envelope_m'];out=[]
 for g in scenario['gateways']:
  tested=[]
  for age in sorted(set([0.,*g['check_ages_Ma'],*np.linspace(0,2,201)])):
   times=np.array([x[0] for x in g['sill_history_Ma_m']]);heights=np.array([x[1] for x in g['sill_history_Ma_m']]);idx=np.argsort(times)
   z=float(np.interp(age,times[idx],heights[idx]));u=g['vertical_uncertainty_m']+scenario['local_sea_level_uncertainty_m']
   tested.append({'age_Ma':float(age),'sill_m':z,'clearance_worst_highstand_m':z-u-sl[1], 'water_depth_worst_lowstand_m':sl[0]-(z+u), 'lowstand_clearance_best_m':z+u-sl[0], 'lowstand_clearance_worst_m':z-u-sl[0]})
  if g['requirement']=='permanent_land':passed=all(x['clearance_worst_highstand_m']>0 for x in tested)
  elif g['requirement']=='persistent_water':passed=all(x['water_depth_worst_lowstand_m']>0 for x in tested)
  else:passed=all(x['lowstand_clearance_worst_m']>0 and x['clearance_worst_highstand_m']<0 for x in tested)
  maxrate=max(abs((b[1]-a[1])/((b[0]-a[0])*1000)) for a,b in zip(g['sill_history_Ma_m'],g['sill_history_Ma_m'][1:]))
  oldest=max(g['check_ages_Ma']);emergence_ok=g['substrate_present_by_Ma']>=oldest
  out.append({'id':g['id'],'requirement':g['requirement'],'geometry_envelope_pass':bool(passed),'substrate_predates_requirement':emergence_ok,'max_assumed_vertical_rate_mm_year':maxrate,'minimum_highstand_clearance_m':min(x['clearance_worst_highstand_m'] for x in tested),'minimum_lowstand_water_depth_m':min(x['water_depth_worst_lowstand_m'] for x in tested),'minimum_lowstand_clearance_m':min(x['lowstand_clearance_worst_m'] for x in tested),'samples':tested,'habitat_and_demography':'not established by sill calculation'})
 return out



def crossing_audit(land,arc,cuts,lowstand=False,platform=None):
 # Exact polygon connectivity in a regional equal-area frame. This is a
 # minimum-largest-gap screen, not a navigational route or settlement model.
 from heapq import heappush,heappop
 center=(128,-5);p=local_projection(center);patch=circle(center,3200)
 local=project(land.intersection(patch),GEO,p)
 if lowstand:
  # Explicit platform hypothesis: up to 45 km of additional shallow margin.
  # Deep channels remain excluded through the same sea-level envelope.
  local=local.buffer(45000)
  if platform is not None:local=local.union(project(platform,GEO,p))
  local=local.difference(unary_union([project(g,GEO,p) for g in cuts]))
 polys=[g for g in parts(local) if g.area>1e6]
 source=project(Point(tr(110,0)),GEO,p);dest=project(Point(tr(145,-22)),GEO,p)
 starts=[i for i,g in enumerate(polys) if g.covers(source)];ends=[i for i,g in enumerate(polys) if g.covers(dest)]
 if not starts or not ends:return {'valid_endpoints':False,'lowstand':lowstand}
 scores={i:0. for i in starts};previous={};queue=[(0.,i) for i in starts]
 while queue:
  d,i=heappop(queue)
  if d!=scores[i]:continue
  if i in ends:break
  for j,g in enumerate(polys):
   if i==j:continue
   gap=polys[i].distance(g)/1000
   if gap>700:continue
   nd=max(d,gap)
   if nd<scores.get(j,float('inf')):scores[j]=nd;previous[j]=i;heappush(queue,(nd,j))
 best=min((scores.get(i,float('inf')),i) for i in ends)
 if not math.isfinite(best[0]):return {'valid_endpoints':True,'route_found_with_gaps_under_700km':False,'lowstand':lowstand}
 chain=[best[1]]
 while chain[-1] not in starts:chain.append(previous[chain[-1]])
 chain=chain[::-1]
 isolation={}
 for name,ref in {'early_island':(120.5,-8.5),'later_northern_island':(123,14)}.items():
  pt=project(Point(tr(*ref)),GEO,p);members=[i for i,g in enumerate(polys) if g.covers(pt)]
  isolation[name]={'site_on_land':bool(members),'separate_from_source':bool(members) and not any(i in starts for i in members),'separate_from_destination':bool(members) and not any(i in ends for i in members)}
 return {'valid_endpoints':True,'lowstand':lowstand,'isolation_sites':isolation,'minimum_largest_projected_water_gap_km':best[0], 'land_shortcut':best[0]==0,'component_hops':len(chain)-1,'gap_lengths_projected_km':[polys[a].distance(polys[b])/1000 for a,b in zip(chain,chain[1:])],'island_area_km2':[polys[a].area/1e6 for a in chain], 'limitation':'Distance in regional equal-area projection; route can cross arbitrary intermediate land interiors. No currents, landing, freshwater or founder test.'}


def material_blocks(records):
 # Six small inherited nucleus parcels, not substitutes for whole-plate polygons.
 from shapely.geometry import box
 from shapely.affinity import translate
 features=[];sizes={};errors=[]
 for r in records:
  lon,lat=CORE[r['group']];az=np.linspace(0,360,181)
  xx,yy,_=GEOD.fwd(np.full(len(az),lon),np.full(len(az),lat),az,np.full(len(az),200000.))
  xx,yy=rotation(xx,yy,r['euler_pole_source_lon_lat_angle'])
  q=FRAME.transform_points(GEO,np.asarray(xx),np.asarray(yy));longitude=np.degrees(np.unwrap(np.radians(q[:,0])))
  vertices=list(zip(longitude,q[:,1]))
  if abs(longitude[-1]-longitude[0])>180:
   pole_lat=90 if r['native_lonlat'][1]>0 else -90
   vertices.extend([(longitude[-1],pole_lat),(longitude[0],pole_lat)])
  raw=make_valid(Polygon(vertices));sectors=[]
  for shift in [-720,-360,0,360,720]:
   piece=translate(raw,xoff=shift).intersection(box(-180,-90,180,90))
   if not piece.is_empty:sectors.extend(parts(piece))
  g=make_valid(unary_union(sectors));a=area(g)
  if r['age_Ma']==0:sizes[r['group']]=a
  features.append(feature(g,group=r['group'],age_Ma=r['age_Ma'],plate_id=r['plate_id'],material='inherited nucleus parcel; radius 200 km',area_km2=a))
 for f in features:errors.append(abs(f['properties']['area_km2']/sizes[f['properties']['group']]-1))
 overlaps=[]
 for age in sorted({r['age_Ma'] for r in records}):
  fs=[f for f in features if f['properties']['age_Ma']==age]
  overlaps.append({'age_Ma':age,'overlap_km2':sum(area(shape(a['geometry']).intersection(shape(b['geometry']))) for i,a in enumerate(fs) for b in fs[i+1:])})
 maxerror=max(errors)
 assert maxerror<.0001
 assert max(x['overlap_km2'] for x in overlaps)<1
 writegeo('dated-nucleus-blocks.geojson',features)
 return {'maximum_fractional_area_drift':maxerror,'dated_nucleus_overlap_checks':overlaps,'scope':'Only six 200-km-radius inherited parcels; external margins and composite-continent block circuits remain unvalidated'}

def relief_paths(land):
 paths={
  'revised highland spine':{'points':[(-75,5),(-73,-7),(-67,-17),(-65,-25),(-70,-30)],'elevation_m':[2200,4000,4300,3500,2400],'established_by_Ma':5},
  'highland to basin headwaters':{'points':[(-73,-7),(-68,-8),(-64,-9),(-60,-10),(-54,-9),(-48,-7)],'elevation_m':[4000,1600,700,250,90,20],'established_by_Ma':3},
  'western ancestral route':{'points':[(-16,15),(-14,21),(-10,27),(-10,31),(-6,35),(-5,38),(-3,42),(8,45),(20,42)],'elevation_m':[120,100,150,180,250,240,300,400,350],'established_by_Ma':6}}
 results=[];features=[]
 for name,d in paths.items():
  g=line(d['points']);inside=land.covers(g);pts=np.asarray(g.coords)
  distance=sum(GEOD.inv(*a,*b)[2] for a,b in zip(pts,pts[1:]))/1000
  results.append({'name':name,'whole_polyline_on_land':inside,'length_km':distance,'maximum_absolute_native_latitude':max(abs(p[1]) for p in pts),'elevation_m':d['elevation_m'],'established_by_Ma':d['established_by_Ma'],'elevation_status':'authored profile, not terrain simulation'})
  features.append(feature(g,name=name,**{k:v for k,v in d.items() if k!='points'}))
 writegeo('relief-and-headwaters.geojson',features)
 return results

def render(target,old,bodies,land,refuge,arc,cuts,cores,gateways):
 plt.rcParams.update({'svg.hashsalt':'erde-reconstruction-v1','font.size':10})
 def save(fig,name):
  for ext in ['png','svg']:fig.savefig(OUT/f'{name}.{ext}',dpi=135,facecolor=fig.get_facecolor(),metadata={'Date':None} if ext=='svg' else None)
  plt.close(fig)
 fig=plt.figure(figsize=(16,10),facecolor=C['paper']);fig.text(.05,.945,'ERDE / REVISED CONTINENTAL TARGETS',fontsize=24,weight='bold')
 fig.text(.05,.905,'Solid green: revised body. Dark outline: prior target. Ochre dashes: original reference.',fontsize=11)
 for i,c in enumerate(CENTERS):
  p=local_projection(CENTERS[c]);ax=fig.add_axes([.055+i%3*.32,.48-i//3*.37,.28,.31],projection=p)
  geoms=[project(g,GEO,p).buffer(1).buffer(-1) for g in [old[c],target[c],bodies[c]]]
  bound=unary_union(geoms).bounds;x0,y0,x1,y1=bound;pad=max(x1-x0,y1-y0)*.06
  ax.set_xlim(x0-pad,x1+pad);ax.set_ylim(y0-pad,y1+pad);ax.set_facecolor(C['paper'])
  for g,fill,col,ls in [(geoms[0],'none','#ac754c','--'),(geoms[2],'#a6c0af','#376251','-'),(geoms[1],'none','#263e45','-')]:
   ax.add_geometries(parts(g),p,facecolor=fill,edgecolor=col,linewidth=.7,linestyle=ls)
  ax.set_title(c,loc='left',weight='bold')
 fig.text(.05,.05,'Local equal-area panels; scales differ between panels. These are authorial candidates, not adopted atlas geography.',fontsize=10)
 save(fig,'01-revised-outlines')
 fig=plt.figure(figsize=(16,10),facecolor=C['paper']);fig.text(.05,.94,'Erde: revised land and proposed passages',fontsize=25,weight='bold')
 ax=fig.add_axes([.07,.23,.86,.60],projection=PROJECTION);ax.set_global();ax.set_facecolor(C['water']);ax.add_geometries(parts(land),GEO,facecolor='#a6c0af',edgecolor='#3c6054',linewidth=.4)
 ax.gridlines(linewidth=.3,alpha=.3)
 for g,color,width in [(refuge,'#a44e33',2.5),(arc,'#a78138',.8)]:
  if g.geom_type=='LineString':ax.plot(*g.xy,transform=GEO,color=color,lw=width)
  else:ax.add_geometries(parts(g),GEO,facecolor=color,edgecolor=color,alpha=.8)
 fig.text(.05,.15,'Rust: western ancestral route, avoiding the obligatory high-latitude exit. Gold: proposed segmented shelf arc.',fontsize=11)
 fig.text(.05,.10,'Shelf depths, uplift dates and habitats are explicit scenario inputs. Geometric passage alone does not establish settlement.',fontsize=10)
 save(fig,'02-world-and-passages')
 fig,axes=plt.subplots(2,2,figsize=(14,9),facecolor=C['paper']);fig.suptitle('Gateway sensitivity to sea level and vertical motion',fontsize=20,y=.97)
 for ax,g in zip(axes.flat,[gateways[0],gateways[1],gateways[2],gateways[3]]):
  x=[r['age_Ma'] for r in g['samples']];z=[r['sill_m'] for r in g['samples']]
  ax.axhspan(-125,15,color='#d9eaf0',label='Tested sea-level envelope');ax.plot(x,z,color='#365c4b',lw=2,label='Authored sill history')
  ax.set_xlim(2,0);ax.set_title(g['id'],loc='left');ax.set_xlabel('Million years before present');ax.set_ylabel('Elevation relative to present sea level (m)');ax.grid(alpha=.15)
 axes[0,0].legend(fontsize=8);fig.tight_layout(rect=[.02,.07,.98,.92]);fig.text(.05,.025,'These curves are proposed boundary conditions, not recovered sea-level or uplift records. The JSON includes uncertainty margins.',fontsize=10)
 save(fig,'03-gateway-sections')
 # Regional map exposes the real scale and connected island components.
 fig=plt.figure(figsize=(15,10),facecolor=C['paper']);fig.text(.05,.94,'The shelf route: land, platform and deep channels',fontsize=23,weight='bold')
 p=local_projection((130,-8));ax=fig.add_axes([.07,.19,.86,.65],projection=p)
 patch=circle((130,-8),2500);local=project(land.intersection(patch),GEO,p)
 sites=[p.transform_point(*tr(*pos),GEO) for pos in [(110,0),(120.5,-8.5),(123,14),(142,-6),(145,-22)]]
 sx,sy=zip(*sites);ax.set_xlim(min(sx)-450000,max(sx)+650000);ax.set_ylim(min(sy)-450000,max(sy)+450000);ax.set_facecolor(C['water'])
 platform=shape(json.loads((OUT/'southern-shelf-platform.geojson').read_text())['features'][0]['geometry'])
 ax.add_geometries(parts(project(platform,GEO,p)),p,facecolor='#d7bc7d',edgecolor='#a0803b',alpha=.8)
 ax.add_geometries(parts(local),p,facecolor='#adc2b1',edgecolor='#3b6052',lw=.6)
 for g in cuts:ax.add_geometries(parts(project(g,GEO,p)),p,facecolor='#91b9cd',edgecolor='none')
 for name,pos in [('Shelf cradle',(110,0)),('Early island',(120.5,-8.5)),('Northern island',(123,14)),('Highlands',(142,-6)),('Shelf-human homeland',(145,-22))]:
  q=p.transform_point(*tr(*pos),GEO);ax.plot(*q,'o',color='#283f45',ms=4);ax.annotate(name,q,xytext=(-5,5) if name=='Shelf-human homeland' else (5,5),ha='right' if name=='Shelf-human homeland' else 'left',textcoords='offset points',fontsize=9)
 fig.text(.05,.115,'Gold: proposed shallow platform, underwater today. Blue cuts: channels retained through the tested lowstand.',fontsize=11)
 fig.text(.05,.065,'An approximately 20 km residual gap is a geometric result, not a finding that voyages or repeated founding were reliable.',fontsize=10)
 save(fig,'05-shelf-route')
 # A genuine dated core-position figure; avoid misleading whole paleocoasts.
 fig=plt.figure(figsize=(16,10),facecolor=C['paper']);fig.text(.05,.94,'Inherited nuclei through geological time',fontsize=25,weight='bold')
 for i,t in enumerate([150.,66.,23.,2.]):
  ax=fig.add_axes([.05+(i%2)*.47,.51-(i//2)*.38,.43,.31],projection=PROJECTION);ax.set_global();ax.set_facecolor(C['water']);ax.gridlines(linewidth=.3,alpha=.5)
  for r in cores:
   if r['age_Ma']==t:
    x,y=r['native_lonlat'];ax.plot(x,y,'o',transform=GEO,ms=5,color='#365e4b');ax.text(x+3,y+3,r['group'],transform=GEO,fontsize=9)
  ax.set_title(f'{t:g} million years ago',loc='left')
 fig.text(.05,.05,'MULLER2022 parent rotations in Erde’s frame. Nucleus points only: no implied coastlines, shelf positions, ice or habitats.',fontsize=10)
 save(fig,'04-dated-nuclei')


def main():
 OUT.mkdir(exist_ok=True);target,old,islands,controls=load_components();scenario=json.loads((OUT/'scenario.json').read_text())
 variants=[];options={}
 for radius in [250,450,700]:
  bodies,land,domains,refuge=make_candidate(target,old,islands,controls,radius)
  anchors=controls['anchors_native'];checks={
   'valid_geometry':land.is_valid,
   'paired_interiors_connected':connected(land,[tr(-162,65),tr(-94,38),tr(-75,8),tr(-60,-10)]),
   'western_refuge_route_on_land':covers_path(land,refuge),
   'mainland_shelf_approach_connected':connected(land,[tr(165,65),tr(75,40),tr(103,18)]),
   'all_core_centers_in_basement_domain':all(domains[c].covers(Point(tr(*pt))) for c,pt in CORE.items())}
  fit_target={c:(smooth(controls['reference_frame_vertices']['C2']) if c=='C2' else target[c]) for c in bodies}
  overlaps={c:area(bodies[c].intersection(fit_target[c]))/area(bodies[c].union(fit_target[c])) for c in bodies}
  row={'margin_search_radius_km':radius,'checks':checks,'target_footprint_IoU':overlaps,'minimum_target_IoU':min(overlaps.values()),'geometry_pass':all(checks.values()),'note':'Radius is a design constraint, not a geophysical measurement.'}
  variants.append(row);options[radius]=(bodies,land,domains,refuge)
 viable=[r for r in variants if r['geometry_pass'] and r['minimum_target_IoU']>=.75]
 if not viable:
  writejson('variant-results.json',variants);raise RuntimeError('No variant passes; inspect diagnostics before changing targets')
 chosen=min(viable,key=lambda x:x['margin_search_radius_km']);bodies,land,domains,refuge=options[chosen['margin_search_radius_km']]
 before_arc=land;land,arc,cuts=build_arc(land)
 # Real full-mask check for unintended continental land shortcuts after adding arc.
 arc_shortcut=connected(land,[tr(110,0),tr(142,-6)])
 if arc_shortcut:
  # Reject this layout; never promote its abstract sill table as geometry proof.
  land=before_arc;arc_status='REJECTED: full map contains a land shortcut; retain separated original islands'
 else:arc_status='passes present full-mask no-land-shortcut check; voyage and dated widths remain conditional'
 platform=buffer(line([(141,-6),(143,-10),(145,-16),(145,-22)]),90,(144,-14))
 crossings_initial=[crossing_audit(land,arc,cuts,low) for low in [False,True]]
 crossings=[crossing_audit(land,arc,cuts,low,platform) for low in [False,True]]
 writejson('crossing-retry.json',{'without_southern_platform':crossings_initial,'with_southern_platform':crossings,'platform_status':'Authored shallow continental shelf, flooded at present and exposed only at suitable lowstands; not extra present land'})
 writegeo('southern-shelf-platform.geojson',[feature(platform,id='highland to shelf-human platform',sill_m=-45,oldest_required_Ma=1.0,proposed_existing_by_Ma=5)])
 writejson('crossing-audit.json',crossings)
 cores,rotation_error=core_history();blocks=material_blocks(cores);relief=relief_paths(land);gateway=gateway_tests(scenario)
 budget=[];provinces=[]
 for c in bodies:
  retained=bodies[c].intersection(old[c]);added=bodies[c].difference(old[c]);drowned=old[c].difference(bodies[c])
  budget.append({'group':c,'emergent_land_km2':area(bodies[c]),'retained_land_km2':area(retained),'new_emergent_locations_km2':area(added),'drowned_reference_locations_km2':area(drowned),'target_IoU':chosen['target_footprint_IoU'][c],'original_reference_IoU':area(bodies[c].intersection(old[c]))/area(bodies[c].union(old[c]))})
  for g,kind in [(retained,'inherited emergent basement'),(added,'proposed marginal basement; provenance conditional'),(drowned,'proposed submerged inherited basement')]:provinces.append(feature(g,group=c,province=kind,age_framework=scenario['continental_histories'][c]))
 writejson('variant-results.json',variants);writejson('core-history.json',{'records':cores,'maximum_latitude_error_vs_independent_cached_point_service_degrees':rotation_error})
 writejson('gateway-results.json',gateway);writejson('land-accounting.json',budget)
 writegeo('revised-geography.geojson',[feature(land,status='authorial candidate; historical acceptance conditional')]);writegeo('crustal-provinces.geojson',provinces)
 writegeo('proposed-passages.geojson',[feature(refuge,id='western ancestral substitution'),feature(arc,id='northern shelf arc',status=arc_status),*[feature(g,id=f'deep-channel-{i+1}') for i,g in enumerate(cuts)]])
 results={'status':'bounded geometric and parametric validation; full historical acceptance remains conditional','chosen_margin_search_radius_km':chosen['margin_search_radius_km'],'variants':variants,'arc_status':arc_status,'full_mask_shelf_to_highland_land_shortcut':arc_shortcut,'material_block_checks':blocks,'relief_paths':relief,'crossing_audit':crossings,'sill_and_emergence_checks_pass':all(g['geometry_envelope_pass'] and g['substrate_predates_requirement'] for g in gateway),'rotation_check_max_error_degrees':rotation_error,'public_atlas_changed':False,'unresolved':['Ancient marginal crust and a globally closed plate-boundary reconstruction','Dated full-route terrain, rainfall, ice margins and freshwater','Voyage success, repeated founding and restricted gene flow','Wildlife-specific dispersal and vicariance','Timing and frequency of actual sea-level openings']}
 baseline=make_valid(FRAME.project_geometry(unary_union([shape(g) for g in json.loads((ROOT/'scripts/editorial/data/reference-land.geojson').read_text())['geometries']]),GEO))
 results['global_land_accounting']={'reference_km2':area(baseline),'revised_km2':area(land),'new_emergent_locations_km2':area(land.difference(baseline)),'drowned_reference_locations_km2':area(baseline.difference(land))}
 results['all_historical_requirements_pass']=False
 results['checks_after_all_geometry_edits']={'valid_geometry':land.is_valid,'western_refuge_route_on_land':land.covers(refuge),'all_relief_paths_on_land':all(r['whole_polyline_on_land'] for r in relief),'required_island_sites_separate_at_high_and_lowstand':all(all(y['site_on_land'] and y['separate_from_source'] and y['separate_from_destination'] for y in x['isolation_sites'].values()) for x in crossings),'residual_lowstand_water_gap_between_0_and_30_km':0<crossings[1]['minimum_largest_projected_water_gap_km']<30}
 writejson('validation.json',results)
 if not os.environ.get('ERDE_NO_RENDER'):render(target,old,bodies,land,refuge,arc,cuts,cores,gateway)
 print(json.dumps({k:v for k,v in results.items() if k!='variants'},indent=2))
if __name__=='__main__':
 from datetime import datetime,timezone
 started=datetime.now(timezone.utc).isoformat()
 writejson('run-status.json',{'status':'running','started_utc':started,'full_historical_validation':False})
 try:
  main()
 except BaseException as error:
  writejson('run-status.json',{'status':'failed','started_utc':started,'error':f'{type(error).__name__}: {error}','full_historical_validation':False})
  raise
 else:
  writejson('run-status.json',{'status':'completed','started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),'full_historical_validation':False,'meaning':'Generation and bounded checks finished; not all historical requirements pass'})
