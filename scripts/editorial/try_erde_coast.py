"""Second authorial trial: one rift embayment on the medium-offset continent.
The first trial remains an immutable input; no adopted map is overwritten.
"""
from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import shape, mapping, Point, LineString, Polygon, box
from shapely.ops import transform
from pyproj import Transformer, Geod
import cartopy.crs as ccrs
from erde_geometry import FRAME,GEO,GLOBE,PROJECTION,C,tr

ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/coast-trial';OUT.mkdir(exist_ok=True)
base=shape(json.loads((ROOT/'docs/geography-trial/candidate-land.geojson').read_text())['features'][0]['geometry'])
prior=json.loads((ROOT/'docs/geography-trial/measurements.json').read_text())['medium']
overlays=json.loads((ROOT/'docs/geography-trial/candidate-overlays.geojson').read_text())['features']
hinge=shape(next(f['geometry'] for f in overlays if f['properties']['role']=='schematic accreted hinge'))
R=6371008.8;geod=Geod(a=R,b=R)
pole=np.radians(prior['euler_pole_native_lon_lat']);k=np.array([np.cos(pole[1])*np.cos(pole[0]),np.cos(pole[1])*np.sin(pole[0]),np.sin(pole[1])]);a=np.radians(prior['angle_degrees'])
def rotate(x,y,z=None):
    l,p=np.radians([np.asarray(x),np.asarray(y)]);v=np.stack([np.cos(p)*np.cos(l),np.cos(p)*np.sin(l),np.sin(p)],axis=-1)
    w=v*np.cos(a)+np.cross(k,v)*np.sin(a)+np.sum(k*v,axis=-1)[...,None]*k*(1-np.cos(a))
    return np.degrees(np.arctan2(w[...,1],w[...,0])),np.degrees(np.arcsin(np.clip(w[...,2],-1,1)))
def point(p):return tuple(float(v) for v in rotate(*tr(*p)))
def parts(g):
    if g.is_empty:return []
    if g.geom_type=='Polygon':return [g]
    return [p for c in g.geoms for p in parts(c)]
def area(g):return sum(abs(geod.geometry_area_perimeter(p)[0]) for p in parts(g))/1e6
center=point((-45,-21))
crs=f'+proj=laea +lon_0={center[0]} +lat_0={center[1]} +R={R} +units=m'
fwd=Transformer.from_crs(f'+proj=longlat +R={R}',crs,always_xy=True).transform
inv=Transformer.from_crs(crs,f'+proj=longlat +R={R}',always_xy=True).transform
local=lambda g:transform(fwd,g)
native=lambda g:transform(inv,g)
coast_projection=ccrs.LambertAzimuthalEqualArea(*center,globe=GLOBE)
regional_projection=ccrs.EqualEarth(central_longitude=-90,globe=GLOBE)
basin=transform(rotate,FRAME.project_geometry(Polygon([(-70,-10),(-62,-15),(-52,-8),(-52,-2),(-59,3),(-68,-1)]),GEO))
spine=LineString([point(p) for p in [(-74,5),(-75,-10),(-68,-22),(-69,-35),(-72,-49)]])
# These are design centers, not a claim that the reference terrain was already below sea level.
ends={'small':(-44.8,-21.5),'moderate':(-46.5,-20),'deep':(-48.5,-18)}
cases={}
for name,end in ends.items():
    nodes=np.array([fwd(*point(p)) for p in [(-38,-25),(-42,-23),end]])
    axis=LineString(nodes)
    samples=np.linspace(0,axis.length,250)
    q=np.array([axis.interpolate(d).coords[0] for d in samples]);t=np.gradient(q,axis=0);t/=np.linalg.norm(t,axis=1)[:,None];n=np.column_stack([-t[:,1],t[:,0]])
    fraction=samples/axis.length
    width={'small':48000,'moderate':76000,'deep':105000}[name]*(1-.45*fraction)
    left=width*(1+.12*np.sin(fraction*17*np.pi));right=width*(1+.15*np.cos(fraction*13*np.pi))
    cut=Polygon(np.vstack([q+n*left[:,None],(q-n*right[:,None])[::-1]]))
    cut=cut.union(Point(q[-1]).buffer(width[-1])).union(Point(q[0]).buffer(width[0]))
    sea=native(cut);land=base.difference(sea);lost=base.intersection(sea)
    connected=any(all(p.covers(Point(v)) for v in prior['population_locators_native'].values()) for p in parts(land))
    actual_penetration=local(base.intersection(native(axis))).length/1000
    metrics={'removed_land_km2':area(lost),'removed_fraction_of_prior_global_land_percent':100*area(lost)/area(base),
        'axis_length_over_previously_exposed_land_km':actual_penetration,
        'valid_geometry':land.is_valid,'all_four_region_locators_same_land_component':connected,
        'hinge_unchanged':hinge.intersection(sea).is_empty,
        'sampled_basin_core_loss_km2':area(basin.intersection(sea)),
        'minimum_distance_to_sampled_basin_core_km_local_projection':local(basin).distance(cut)/1000,
        'minimum_distance_to_schematic_highland_axis_km_local_projection':local(spine).distance(cut)/1000,
        'new_sea_is_one_connected_shape':len(parts(sea))==1,
        'mouth_center_was_water':not base.covers(Point(point((-38,-25)))),
        'inland_head_was_land':base.covers(Point(point(end)))}
    assert land.is_valid and connected and metrics['hinge_unchanged']
    assert metrics['sampled_basin_core_loss_km2']<.01
    assert metrics['new_sea_is_one_connected_shape'] and metrics['mouth_center_was_water'] and metrics['inland_head_was_land']
    cases[name]={'land':land,'lost':lost,'sea':sea,'axis':native(axis),'metrics':metrics}
selected=cases['moderate']
(OUT/'measurements.json').write_text(json.dumps({n:c['metrics'] for n,c in cases.items()},indent=2)+'\n')
(OUT/'candidate-land.geojson').write_text(json.dumps({'type':'FeatureCollection','features':[{'type':'Feature','properties':{'status':'authorial trial','variant':'medium offset plus moderate gulf'},'geometry':mapping(selected['land'])}]},separators=(',',':'))+'\n')
(OUT/'gulf.geojson').write_text(json.dumps({'type':'Feature','properties':{'status':'assumed rift-basin outline, not bathymetry'},'geometry':mapping(selected['sea'])},separators=(',',':'))+'\n')
plt.rcParams.update({'svg.hashsalt':'erde-coast-trial-v1','font.size':11})
def save(f,name):
    for ext in ['png','svg']:f.savefig(OUT/f'{name}.{ext}',dpi=135,facecolor=f.get_facecolor(),metadata={'Date':None} if ext=='svg' else None)
    plt.close(f)
def draw(ax,g):
    if ax.projection==coast_projection:g=g.intersection(box(center[0]-20,center[1]-20,center[0]+20,center[1]+20))
    ax.set_facecolor(C['water']);ax.add_geometries(parts(g),GEO,facecolor=C['land'],edgecolor='#576c69',lw=.7)
    ax.gridlines(crs=GEO,color='#809491',alpha=.55,lw=.45)

f=plt.figure(figsize=(16,9),facecolor=C['paper'])
f.text(.045,.94,'ERDE / SECOND GEOGRAPHY TRIAL',size=12,weight='bold',color=C['muted']);f.text(.045,.875,'An embayment changes the continental outline',size=25,weight='bold')
f.text(.045,.83,'The medium continental offset and relocated hinge are retained; one coastal rift basin is added.',size=12)
for rect,g,title in [([.04,.26,.44,.51],base,'Previous candidate'),([.52,.26,.44,.51],selected['land'],'Candidate with coastal embayment')]:
    ax=f.add_axes(rect,projection=regional_projection);ax.set_extent([-163,-55,-28,42],crs=GEO);draw(ax,g);ax.set_title(title,size=14,pad=15)
    if title.startswith('Candidate'):
        ax.add_geometries(parts(selected['lost']),GEO,facecolor='none',edgecolor='#9c5e42',linestyle='--',lw=.9)
        ax.add_geometries(parts(basin),GEO,facecolor='#b1c7a6',edgecolor='#557448',alpha=.7,lw=.6)
f.text(.055,.19,'Dashed outline: former coastline in the edited area. Green: representative protected basin interior.',size=11)
f.text(.055,.135,'This changes the shape of the mainland without cutting its land connection or the protected basin sample.',size=12)
f.text(.055,.08,'Trial only. Flooded terrain is an assumed geological difference; drainage, elevation and marine depth are not simulated.',size=10,color=C['muted'])
save(f,'01-coast-comparison')

f=plt.figure(figsize=(16,9),facecolor=C['paper']);f.text(.045,.94,'ERDE / SECOND GEOGRAPHY TRIAL',size=12,weight='bold',color=C['muted']);f.text(.045,.88,'Testing the size of the gulf',size=26,weight='bold')
f.text(.045,.835,'Three cuts into the same coastal sector, shown at the same scale in a local equal-area projection.',size=12)
for i,(name,c) in enumerate(cases.items()):
    ax=f.add_axes([.035+i*.325,.3,.29,.47],projection=coast_projection);cx,cy=fwd(*center);ax.set_xlim(cx-900000,cx+900000);ax.set_ylim(cy-900000,cy+900000);draw(ax,c['land']);ax.set_title(name.capitalize(),size=14,pad=12)
    ax.add_geometries(parts(c['lost']),GEO,facecolor='none',edgecolor='#a36d4d',ls='--',lw=.8)
    m=c['metrics'];f.text(.045+i*.325,.23,f"Newly marine area: {m['removed_land_km2']:,.0f} km²\nAxis over former land: {m['axis_length_over_previously_exposed_land_km']:.0f} km",size=11,linespacing=1.6)
f.text(.055,.13,'Moderate is the comparison specimen. Visual review finds limited continental-scale benefit; adoption is deferred.',size=12)
f.text(.055,.075,'Marine intrusion requires sustained basin accommodation. Sediment supply and subsidence may instead fill or restrict the gulf.',size=10,color=C['muted'])
save(f,'02-gulf-options')
print(json.dumps({n:c['metrics'] for n,c in cases.items()},indent=2))
