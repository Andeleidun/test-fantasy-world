"""Worldwide silhouette design constrained by the dated Erde reconstruction graph.

The geometry is authorial. Historical routes are accepted only when the dated
constraint model supplies an old substrate and an appropriate accessibility state.
"""
from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from shapely import make_valid
from shapely.affinity import scale
from shapely.geometry import Polygon, Point, shape, mapping, box
from shapely.ops import unary_union, transform, nearest_points
from pyproj import Geod
from erde_geometry import FRAME,GEO,GLOBE,PROJECTION,C,tr

ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/global-geography-trial';OUT.mkdir(exist_ok=True)
R=6371008.8;GEOD=Geod(a=R,b=R)
def parts(g):
    if g.is_empty:return []
    if g.geom_type=='Polygon':return [g]
    return [p for c in getattr(g,"geoms",[]) for p in parts(c)]
def area(g):return sum(abs(GEOD.geometry_area_perimeter(p)[0]) for p in parts(g))/1e6

controls={
'C1':[(-168,66),(-158,59),(-141,59),(-133,51),(-128,42),(-122,34),(-120,25),(-110,19),(-99,17),(-93,16),(-86,20),(-84,27),(-88,32),(-77,34),(-66,31),(-60,38),(-64,46),(-56,54),(-63,62),(-79,66),(-95,64),(-100,58),(-110,60),(-116,67),(-128,73),(-147,70),(-162,72)],
'C2':[(-79,7),(-74,12),(-66,8),(-60,4),(-52,7),(-44,0),(-43,-9),(-49,-15),(-45,-24),(-53,-31),(-65,-31),(-72,-39),(-83,-38),(-91,-30),(-89,-18),(-82,-8),(-85,0)],
'C3':[(-11,36),(-18,45),(-6,53),(-14,63),(4,72),(25,68),(42,76),(72,74),(92,65),(110,67),(130,74),(154,71),(166,63),(179,64),(179,55),(166,49),(152,44),(144,30),(130,25),(123,11),(115,5),(110,-2),(102,1),(99,16),(83,19),(73,13),(60,15),(50,24),(34,28),(32,33),(22,35),(15,40),(3,37)],
'C4':[(-6,35),(9,34),(20,30),(32,32),(38,23),(34,13),(45,7),(50,-7),(40,-15),(44,-26),(34,-33),(23,-25),(16,-14),(5,-18),(-9,-11),(-20,1),(-24,18),(-17,29)],
'C5':[(123,-12),(136,-13),(145,-17),(154,-14),(166,-22),(160,-31),(148,-30),(142,-37),(132,-43),(122,-39),(118,-26)]}

def outline(vertices,iterations=2):
    v=np.array(vertices,dtype=float)
    for _ in range(iterations):
        nxt=np.roll(v,-1,axis=0);v=np.stack([.8*v+.2*nxt,.2*v+.8*nxt],axis=1).reshape(-1,2)
    return Polygon(v)

reference=unary_union([shape(g) for g in json.loads((ROOT/'scripts/editorial/data/reference-land.geojson').read_text())['geometries']])
source={k:outline(v) for k,v in controls.items()}
longitudes=np.linspace(-180,180,241);phase=np.radians(longitudes)
coast=-90+(17+5*np.cos(2*phase+.4)+3*np.sin(3*phase-1)+1.3*np.cos(7*phase))
source['C6']=Polygon([*zip(longitudes,coast),(180,-90),(-180,-90)])

# C2 no longer receives the prior extra 6-degree Euler offset. Its authored
# silhouette supplies the visible difference without creating a false hinge history.
native={code:FRAME.project_geometry(g,GEO) for code,g in source.items()}

island_sources=[
 outline([(-55,62),(-44,65),(-37,72),(-44,77),(-54,73),(-60,68)]),
 outline([(114,-2),(119,2),(124,-1),(122,-7),(117,-9),(113,-6)]),
 outline([(119,13),(124,18),(128,15),(126,9),(122,8)]),
 outline([(119,-10),(124,-9),(129,-12),(127,-14),(122,-14)]),
 outline([(130,-4),(137,-2),(147,-5),(153,-10),(145,-12),(137,-8),(131,-9)]),
 outline([(136,31),(140,35),(145,34),(150,39),(151,43),(147,44),(140,39)]),
 outline([(158,-39),(164,-38),(170,-43),(167,-47),(160,-46)]),
 outline([(46,-13),(52,-16),(54,-25),(50,-28),(46,-22)])]
islands=[FRAME.project_geometry(g,GEO) for g in island_sources]
baseline=FRAME.project_geometry(reference,GEO)

anchors_ref={'paired_north':(-94,18),'paired_south':(-75,8),'watersheds':(-94,38),'equatorial_basin':(-58,-6),'highland_spine':(-78,-22),'ancestral_refuge':(-16,15),'west_contact':(20,42),'east_contact':(75,40),'shelf_cradle':(112,0),'shelf_humans':(145,-22),'highland_islanders':(142,-6)}
anchors={name:tuple(float(v) for v in tr(*p)) for name,p in anchors_ref.items()}
join_names=['paired_north','paired_south','watersheds','equatorial_basin','highland_spine']

# Diagnostic Earth-reference partitions are area/IoU comparators only.
sa_mask=Polygon([(-82,7),(-78,7),(-77,9.5),(-73,12.8),(-30,15),(-30,-60),(-85,-60)])
base_ref={'C2':reference.intersection(sa_mask),'C1':reference.intersection(box(-180,7,-30,86)).difference(sa_mask),'C4':reference.intersection(Polygon([(-26,37),(10,37),(32,32),(44,11),(60,7),(52,-40),(-26,-40)])),'C5':reference.intersection(box(110,-47,155,-10)),'C6':reference.intersection(box(-180,-90,180,-60))}
base_ref['C3']=reference.intersection(box(-25,0,180,86)).difference(base_ref['C4'])
old={c:make_valid(FRAME.project_geometry(g,GEO)) for c,g in base_ref.items()}

sizing={'C3':((75,45),.88),'C4':((15,0),.9),'C5':((141,-25),.89)}
for c,(center,factor) in sizing.items():
    local=ccrs.LambertAzimuthalEqualArea(*center,globe=GLOBE)
    projected=local.project_geometry(source[c],GEO)
    resized=GEO.project_geometry(scale(projected,xfact=factor,yfact=factor,origin=(0,0)),local)
    native[c]=make_valid(FRAME.project_geometry(resized,GEO))

# Explicit old marginal terranes replace the former Earth-reference guard patches.
# Their chronology and physical roles are defined in reconstruction-model.json and
# physical-test-model.json.
terrane_sources={
 'JX1_ISTHMIAN_TERRANE':outline([(-99,19),(-94,23),(-87,22),(-81,18),(-76,13),(-71,10),(-72,5),(-77,4),(-82,7),(-86,11),(-92,13),(-98,15)],1),
 'C4_MARGINAL_CORRIDOR':outline([(-24,14),(-26,20),(-23,28),(-18,35),(-12,40),(-6,43),(0,44),(8,43),(5,38),(-2,35),(-8,31),(-13,27),(-16,21),(-17,16)],1),
 # The shelf head's western root intentionally overlaps the resized C3 margin.
 # Its eastern nose is unchanged so the deep-water stepping route remains intact.
 'C5_SHELF_HEAD':outline([(98,7),(104,6),(109,4),(113,2),(113,-1),(111,-4),(106,-3),(101,0)],1),
 # Small old terrane islands shorten repeated founder crossings without creating
 # a lowstand land bridge. B is slightly larger to support a stronger catchment.
 'EASTERN_STEPPING_TERRANE_A':outline([(113.19,-1.33),(113.33,-1.19),(113.47,-1.33),(113.33,-1.47)],1),
 'EASTERN_STEPPING_TERRANE_B':outline([(113.50,-1.66),(113.66,-1.50),(113.82,-1.66),(113.66,-1.82)],1)}
terranes={name:make_valid(FRAME.project_geometry(g,GEO)) for name,g in terrane_sources.items()}
land=make_valid(unary_union([*native.values(),*islands,*terranes.values()]))

checks={name:land.covers(Point(pos)) for name,pos in anchors.items()}
def connected(points):
    return any(all(p.covers(Point(xy)) for xy in points) for p in parts(land))
structural_connectivity={
 'paired_continent_interiors_via_JX1':connected([anchors[n] for n in join_names]),
 'c4_refuge_to_c3_western_core':connected([anchors['ancestral_refuge'],anchors['west_contact']]),
 'c3_eastern_core_to_shelf_cradle':connected([anchors['east_contact'],anchors['shelf_cradle']])}

# Measure the repaired eastern water route as actual coastline-to-coastline gaps.
eastern_chain=[terranes['C5_SHELF_HEAD'],terranes['EASTERN_STEPPING_TERRANE_A'],terranes['EASTERN_STEPPING_TERRANE_B'],islands[1]]
eastern_water_gaps_km=[]
for left,right in zip(eastern_chain,eastern_chain[1:]):
    p1,p2=nearest_points(left,right);_,_,d=GEOD.inv(p1.x,p1.y,p2.x,p2.y);eastern_water_gaps_km.append(d/1000)
c4_lats=[tr(*p)[1] for p in [(-24,14),(-26,20),(-23,28),(-18,35),(-12,40),(-6,43),(0,44),(8,43),(5,38),(-2,35),(-8,31),(-13,27),(-16,21),(-17,16)]]
assert land.is_valid and all(checks.values()) and all(structural_connectivity.values())
assert all(gap>0 for gap in eastern_water_gaps_km) and max(eastern_water_gaps_km)<80

metrics={
 'status':'dated reconstruction Strategy A; geometry and bounded physical checks integrated',
 'global_land_area_km2':area(land),
 'baseline_land_area_km2':area(baseline),
 'land_area_change_percent':100*(area(land)/area(baseline)-1),
 'candidate_land_fraction_percent':100*area(land)/(4*np.pi*R**2/1e6),
 'valid_land':land.is_valid,
 'anchors_on_land':checks,
 'structural_connectivity':structural_connectivity,
 'eastern_repaired_water_gaps_km':eastern_water_gaps_km,
 'c4_marginal_corridor_native_latitude_deg':[min(c4_lats),max(c4_lats)],
 'dated_graph':'dated-constraint-graph.json',
 'reconstruction_model':'reconstruction-model.json',
 'physical_test_model':'physical-test-model.json',
 'historical_warning':'present-day connectivity is not evidence of dated passability; run both dated validators and the remaining high-fidelity physical-model audits',
 'terrane_area_km2':{name:area(g) for name,g in terranes.items()},
 'continents':{}}
for c in native:
    both=native[c].intersection(old[c]);union=native[c].union(old[c])
    metrics['continents'][c]={'candidate_body_area_km2':area(native[c]),'baseline_partition_area_km2':area(old[c]),'footprint_intersection_over_union':area(both)/area(union)}
(OUT/'measurements.json').write_text(json.dumps(metrics,indent=2)+'\n')
(OUT/'design-controls.json').write_text(json.dumps({
 'status':'authorial design controls constrained by dated reconstruction and bounded physical tests; not a plate/GCM simulation',
 'generated_outputs_current':True,
 'reference_frame_vertices':controls,
 'sixth_continent_polar_radius_degrees':'17 + 5 cos(2λ+0.4) + 3 sin(3λ−1) + 1.3 cos(7λ)',
 'paired_offset':{'angle_degrees':0,'reason':'removed; visible C2 redesign retained without artificial late-looking displacement'},
 'new_outline_sizing':sizing,
 'anchors_native':anchors,
 'terrane_reference_frame_vertices':{k:list(map(list,g.exterior.coords[:-1])) for k,g in terrane_sources.items()},
 'dated_non_land_substrates':['NORTHERN_APPROACH_SHELF'],
 'validators':['scripts/editorial/validate_erde_constraint_graph.py','scripts/editorial/validate_erde_physical_tests.py']},indent=2)+'\n')
features=[{'type':'Feature','properties':{'group':'worldwide candidate','status':'Strategy A; dated-history validity conditional on remaining high-fidelity physical models'},'geometry':mapping(land)}]
(OUT/'candidate-geography.geojson').write_text(json.dumps({'type':'FeatureCollection','features':features},separators=(',',':'))+'\n')
if __import__('os').environ.get('ERDE_GEOMETRY_ONLY'):
    print(json.dumps(metrics,indent=2));raise SystemExit

plt.rcParams.update({'svg.hashsalt':'erde-worldwide-v3','font.size':11})
def save(f,name):
    for ext in ['png','svg']:f.savefig(OUT/f'{name}.{ext}',dpi=150,facecolor=f.get_facecolor(),metadata={'Date':None} if ext=='svg' else None)
    plt.close(f)
def world(ax,g):
    ax.set_global();ax.set_facecolor('#e1ebed');ax.add_geometries(parts(g),GEO,facecolor='#526b65',edgecolor='#344c48',lw=.4)
    ax.gridlines(crs=GEO,linewidth=.3,color='#82918e',alpha=.35)

f=plt.figure(figsize=(16,12),facecolor=C['paper']);f.text(.045,.955,'ERDE / WORLDWIDE GEOGRAPHY STUDY',size=12,color=C['muted'],weight='bold');f.text(.045,.91,'Dated reconstruction candidate',size=26,weight='bold')
for rect,g,title in [([.08,.51,.84,.34],baseline,'Previous atlas silhouette'),([.08,.10,.84,.34],land,'Strategy A silhouette')]:
    ax=f.add_axes(rect,projection=PROJECTION);world(ax,g);ax.set_title(title,size=14,pad=14)
f.text(.055,.047,'Identical projection and scale. Junction, marginal corridor and eastern stepping terranes are explicit old reconstruction objects.',size=11)
save(f,'01-world-silhouettes')

f=plt.figure(figsize=(16,10),facecolor=C['paper']);f.text(.045,.95,'ERDE / WORLDWIDE GEOGRAPHY STUDY',size=12,color=C['muted'],weight='bold');f.text(.045,.895,'A change to every continental body',size=27,weight='bold')
centers={'C1':(-107,45),'C2':(-63,-15),'C3':(75,45),'C4':(15,0),'C5':(141,-25),'C6':(0,-90)}
for idx,c in enumerate(['C1','C2','C3','C4','C5','C6']):
    lon,lat=tr(*centers[c]);projection=ccrs.LambertAzimuthalEqualArea(lon,lat,globe=GLOBE)
    ax=f.add_axes([.055+(idx%3)*.32,.47-(idx//3)*.37,.28,.31],projection=projection);ax.set_facecolor(C['paper'])
    def local_vertices(x,y,z=None):
        pts=projection.transform_points(GEO,np.asarray(x),np.asarray(y));return pts[...,0],pts[...,1]
    candidate_projected=transform(local_vertices,native[c]);old_projected=transform(local_vertices,old[c]);b1=candidate_projected.bounds;b2=old_projected.bounds;bounds=(min(b1[0],b2[0]),min(b1[1],b2[1]),max(b1[2],b2[2]),max(b1[3],b2[3]))
    x0,y0,x1,y1=bounds;pad=max(x1-x0,y1-y0)*.08;ax.set_xlim(x0-pad,x1+pad);ax.set_ylim(y0-pad,y1+pad)
    clean_old=unary_union(parts(make_valid(old_projected))).buffer(1).buffer(-1);clean_candidate=unary_union(parts(make_valid(candidate_projected))).buffer(1).buffer(-1)
    ax.add_geometries(parts(clean_old),projection,facecolor='none',edgecolor='#b07750',lw=1,linestyle='--');ax.add_geometries(parts(clean_candidate),projection,facecolor='#a7bcb0',edgecolor='#345448',lw=.7,alpha=.85);ax.set_title(c+' · redesigned body',size=12,pad=10)
f.text(.055,.06,'Green: new body. Dashed ochre: original reference partition. Local terranes are tracked separately in the dated model.',size=10)
save(f,'02-six-body-comparison')

f=plt.figure(figsize=(16,10),facecolor=C['paper']);f.text(.045,.95,'ERDE / WORLDWIDE GEOGRAPHY STUDY',size=12,color=C['muted'],weight='bold');f.text(.045,.89,'The new world and its dated requirements',size=25,weight='bold')
ax=f.add_axes([.07,.24,.86,.57],projection=PROJECTION);world(ax,land)
for number,(name,p) in enumerate(anchors.items(),1):
    ax.plot(*p,'o',transform=GEO,ms=3,color='#faf3d9');ax.annotate(str(number),xy=p,xycoords=GEO._as_mpl_transform(ax),xytext=(4,4),textcoords='offset points',color='#273b40',size=9,weight='bold',bbox={'facecolor':C['paper'],'alpha':.8,'edgecolor':'none','pad':.4})
f.text(.055,.15,'1–5: paired-continent interiors. 6–8: C4 refuge and continental contact cores. 9–11: shelf and island lineage controls.',size=11)
f.text(.055,.10,'JX1, C4 marginal corridor, C5 shelf head and two eastern stepping terranes are old-substrate hypotheses with dated tests.',size=11)
f.text(.055,.06,'Migration windows, ice, bathymetry, relief and ecology remain separate validation layers; modern connectivity is not historical proof.',size=10,color=C['muted'])
save(f,'03-world-constraints')
print(json.dumps(metrics,indent=2))
