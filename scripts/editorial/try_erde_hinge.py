"""Reproducible authorial trial, separate from the published atlas geometry.

The rigid continental offset is spherical. Hinge/island geometry is a schematic
construction in a local equal-area CRS, not a solved tectonic or terrain model.
"""
from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import shape, mapping, Polygon, Point, LineString, box
from shapely.ops import unary_union, transform
from pyproj import CRS, Transformer, Geod
import cartopy.crs as ccrs
from erde_geometry import FRAME, GEO, GLOBE, PROJECTION, C, tr

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/geography-trial'
OUT.mkdir(exist_ok=True)
GEOD=Geod(a=6371008.8,b=6371008.8)
LOCAL=CRS.from_proj4('+proj=laea +lon_0=-83 +lat_0=24 +R=6371008.8 +units=m')
FWD=Transformer.from_crs('+proj=longlat +R=6371008.8',LOCAL,always_xy=True).transform
INV=Transformer.from_crs(LOCAL,'+proj=longlat +R=6371008.8',always_xy=True).transform
PLOT=ccrs.LambertAzimuthalEqualArea(-83,24,globe=GLOBE)
PLOT.threshold=1000
POLE=(-100,60)

def parts(g):
    if g.is_empty:return []
    if g.geom_type=='Polygon':return [g]
    return [p for child in g.geoms for p in parts(child)]

def rotate_xy(x,y,angle):
    lon,lat=np.radians([np.asarray(x),np.asarray(y)])
    v=np.stack([np.cos(lat)*np.cos(lon),np.cos(lat)*np.sin(lon),np.sin(lat)],axis=-1)
    l,p=np.radians(POLE);k=np.array([np.cos(p)*np.cos(l),np.cos(p)*np.sin(l),np.sin(p)])
    a=np.radians(angle)
    w=v*np.cos(a)+np.cross(k,v)*np.sin(a)+np.sum(k*v,axis=-1)[...,None]*k*(1-np.cos(a))
    return np.degrees(np.arctan2(w[...,1],w[...,0])),np.degrees(np.arcsin(np.clip(w[...,2],-1,1)))

def rotate(g,angle):return transform(lambda x,y,z=None:rotate_xy(x,y,angle),g)
def local(g):return transform(FWD,g)
def native(g):return transform(INV,g)
def area(g):
    return sum(abs(GEOD.geometry_area_perimeter(p)[0]) for p in parts(g))/1e6

def feature(g,role):return {'type':'Feature','properties':{'role':role,'status':'authorial trial'},'geometry':mapping(g)}

reference=unary_union([shape(g) for g in json.loads((ROOT/'scripts/editorial/data/reference-land.geojson').read_text())['geometries']])
# Approximate source-block partition at the old hinge, not a claim about actual plate boundaries.
sa_mask=Polygon([(-82,7),(-78,7),(-77,9.5),(-73,12.8),(-30,15),(-30,-60),(-85,-60)])
sa_ref=reference.intersection(sa_mask)
old_margin=Polygon([(-96,14),(-94,16),(-91,16.8),(-89,17.2),(-87,16.6),(-84,17),(-76,10),(-76,5),(-96,5)])
removed_ref=reference.intersection(old_margin).difference(sa_ref)
fixed_ref=reference.difference(sa_ref).difference(removed_ref)
sa=FRAME.project_geometry(sa_ref,GEO)
fixed=FRAME.project_geometry(fixed_ref,GEO)
removed=FRAME.project_geometry(removed_ref,GEO)
baseline=FRAME.project_geometry(reference,GEO)
source_points={'Coastal rim':(-126,55),'Great Watersheds':(-94,38),'Highland Spine':(-68,-22),'Equatorial Basin':(-58,-6)}
anchor_na=tr(-94,18)
anchor_sa=tr(-75,8)

# Old upland fragments survive partial subsidence. Their shapes inherit the former coast.
islands=[]
for pos,radius in [((-91,15),65000),((-88,14.8),75000),((-85.5,12.7),65000),((-83.7,10.2),55000),((-80.5,8.3),45000)]:
    center=np.array(FWD(*tr(*pos)))
    theta=np.linspace(0,2*np.pi,121)
    r=radius*(1+.18*np.sin(3*theta)+.12*np.cos(5*theta)+.07*np.sin(9*theta))
    outline=Polygon(np.column_stack([center[0]+1.25*r*np.cos(theta),center[1]+.8*r*np.sin(theta)]))
    island=local(removed).intersection(outline)
    if not island.is_empty:islands.append(island)

def candidate(angle):
    shifted=rotate(sa,angle)
    end=np.array(rotate_xy(*anchor_sa,angle),dtype=float)
    # A broad curved accreted belt docks farther along the northern margin.
    controls=[anchor_na,(-74,32),(-80,29),(-85,25),(-88,21),(-88,17),tuple(end)]
    # Chaikin subdivision softens the schematic arc without a plotting spline dependency.
    pts=np.array([FWD(*p) for p in controls])
    for _ in range(3):
        q=np.stack([.75*pts[:-1]+.25*pts[1:],.25*pts[:-1]+.75*pts[1:]],axis=1).reshape(-1,2)
        pts=np.vstack([pts[0],q,pts[-1]])
    spine=LineString(pts)
    samples=np.linspace(0,spine.length,600)
    center=np.array([spine.interpolate(s).coords[0] for s in samples])
    tangents=np.gradient(center,axis=0);tangents/=np.linalg.norm(tangents,axis=1)[:,None]
    normals=np.column_stack([-tangents[:,1],tangents[:,0]])
    phase=samples/spine.length
    left=105000+28000*np.sin(phase*5*np.pi)+18000*np.sin(phase*17*np.pi)+7000*np.cos(phase*53*np.pi)
    right=110000+33000*np.sin(phase*4*np.pi+.7)+16000*np.cos(phase*19*np.pi)+6000*np.sin(phase*49*np.pi)
    hinge=Polygon(np.vstack([center+normals*left[:,None],(center-normals*right[:,None])[::-1]]))
    hinge=hinge.union(Point(pts[0]).buffer(100000)).union(Point(pts[-1]).buffer(100000))
    # Retain offshore fragments only; all land components are unioned to remove overlaps.
    hinged_native=native(hinge)
    current=unary_union([fixed,shifted,hinged_native,*[native(i) for i in islands]])
    target_native=[anchor_na,tuple(end),tuple(rotate_xy(*tr(-58,-6),angle))]
    joined=any(all(p.buffer(1e-7).covers(Point(v)) for v in target_native) for p in parts(current))
    relocated={name:np.array(rotate_xy(*tr(*pos),angle) if name in ['Highland Spine','Equatorial Basin'] else tr(*pos),dtype=float).tolist() for name,pos in source_points.items()}
    coords=np.concatenate([np.array(p.exterior.coords) for p in parts(sa)])
    rx,ry=rotate_xy(coords[:,0],coords[:,1],angle)
    distances=GEOD.inv(coords[:,0],coords[:,1],rx,ry)[2]/1000
    metrics={'angle_degrees':angle,'euler_pole_native_lon_lat':POLE,
      'basin_displacement_km':GEOD.inv(*tr(-58,-6),*relocated['Equatorial Basin'])[2]/1000,
      'coastal_vertex_displacement_km_min_max':[float(min(distances)),float(max(distances))],
      'max_coastal_latitude_change_degrees':float(max(abs(ry-coords[:,1]))),
      'south_block_area_km2':area(shifted),'south_block_area_change_percent':100*(area(shifted)/area(sa)-1),
      'all_land_valid':current.is_valid,'north_to_south_land_component':joined,
      'hinge_axis_length_km':spine.length/1000,'constructed_belt_width_km_min_max':[float(min(left+right)/1000),float(max(left+right)/1000)],
      'old_margin_removed_km2':area(removed),'surviving_fragment_area_km2':sum(i.area for i in islands)/1e6,
      'new_belt_gross_area_km2':hinge.area/1e6,
      'global_mapped_land_area_change_percent':100*(area(current)/area(baseline)-1),
      'population_locators_native':relocated,
      'locators_on_land':{name:current.buffer(1e-6).covers(Point(p)) for name,p in relocated.items()}}
    watershed=FRAME.project_geometry(reference.intersection(Polygon([(-100,32),(-99,45),(-86,43),(-86,33)])),GEO)
    basin=rotate(FRAME.project_geometry(sa_ref.intersection(Polygon([(-70,-10),(-62,-15),(-52,-8),(-52,-2),(-59,3),(-68,-1)])),GEO),angle)
    metrics['protected_land_footprints_retained']={
        'watershed_core':area(watershed.difference(current))<.01,
        'basin_core':area(basin.difference(current))<.01}
    metrics['island_to_island_shortest_outline_gaps_km']=[
        islands[i].distance(islands[i+1])/1000 for i in range(len(islands)-1)]
    metrics['new_belt_width_is_not_usable_habitat_width']=True
    assert joined and current.is_valid
    assert all(metrics['locators_on_land'].values()),metrics['locators_on_land']
    assert all(metrics['protected_land_footprints_retained'].values())
    assert abs(metrics['south_block_area_change_percent'])<1e-8
    assert metrics['max_coastal_latitude_change_degrees']<4

    # Outline connectivity is necessary, not proof of traversable terrain or water/food supply.
    return {'land':current,'shifted':shifted,'hinge':hinged_native,'axis':native(spine),'basin':basin,'watershed':watershed,'metrics':metrics}

cases={name:candidate(angle) for name,angle in [('modest',-4),('medium',-6),('stronger',-8)]}
(OUT/'measurements.json').write_text(json.dumps({name:c['metrics'] for name,c in cases.items()},indent=2)+'\n')
selected=cases['medium']
(OUT/'candidate-land.geojson').write_text(json.dumps({'type':'FeatureCollection','features':[feature(selected['land'],'candidate land')]},separators=(',',':'))+'\n')
(OUT/'candidate-overlays.geojson').write_text(json.dumps({'type':'FeatureCollection','features':[feature(selected['hinge'],'schematic accreted hinge'),feature(selected['axis'],'land corridor axis'),*[feature(native(i),'inherited upland island') for i in islands]]},separators=(',',':'))+'\n')

plt.rcParams.update({'svg.hashsalt':'erde-hinge-trial-v1','font.size':11})

def base_axes(f,rect,geom,global_view=False):
    ax=f.add_axes(rect,projection=PROJECTION if global_view else PLOT)
    if global_view:ax.set_global()
    else:ax.set_extent([-163,8,-27,68],crs=GEO)
    ax.set_facecolor(C['water'])
    ax.add_geometries(parts(geom),GEO,facecolor=C['land'],edgecolor='#637575',lw=.5)
    ax.gridlines(crs=GEO,xlocs=np.arange(-180,181,30),ylocs=np.arange(-60,91,15),linewidth=.4,color='#78908e',alpha=.6)
    return ax

def save(f,name):
    for ext in ['svg','png']:
        f.savefig(OUT/(name+'.'+ext),dpi=135,facecolor=f.get_facecolor(),metadata={'Date':None} if ext=='svg' else None)
    plt.close(f)

f=plt.figure(figsize=(16,9),facecolor=C['paper'])
f.text(.045,.94,'ERDE / GEOGRAPHY TRIAL',size=12,weight='bold',color=C['muted'])
f.text(.045,.884,'An offset pair of continents',size=27,weight='bold')
f.text(.045,.842,'The same equal-area world view; the candidate changes one continental block and its connecting margin.',size=12)
for rect,geom,title in [((.035,.26,.455,.54),baseline,'Current atlas'),((.51,.26,.455,.54),selected['land'],'Candidate: medium offset')]:
    ax=base_axes(f,rect,geom,True);ax.set_title(title,size=15,pad=16)
    if title.startswith('Candidate'):
        ax.add_geometries(parts(selected['shifted']),GEO,facecolor='#c7d8be',edgecolor='#536e56',lw=.6)
        ax.add_geometries(parts(selected['hinge']),GEO,facecolor='#c68b4e',edgecolor='#855425',lw=.5)
        ax.add_geometries(parts(sa),GEO,facecolor='none',edgecolor='#88677e',lw=.75,linestyle='--')
f.text(.055,.2,'Green: displaced continental block    Ochre: new connecting belt    Dashed: previous block outline',size=11)
f.text(.055,.145,'The basin locator shifts about 589 km, while remaining near 2°S. The distant continental entry is unchanged.',size=12)
f.text(.055,.093,'Trial geometry, not adopted canon. Coastlines are a broad design; terrain, bathymetry and climate remain to be tested.',size=10,color=C['muted'])
save(f,'01-world-comparison')

f=plt.figure(figsize=(15,11),facecolor=C['paper'])
f.text(.055,.945,'ERDE / GEOGRAPHY TRIAL',size=12,weight='bold',color=C['muted'])
f.text(.055,.89,'The relocated volcanic hinge',size=27,weight='bold')
f.text(.055,.85,'A continuous land connection with offshore remnants of the older coastal margin.',size=12)
ax=f.add_axes([.08,.23,.62,.57],projection=PLOT);ax.set_extent([-99,-62,8,38],crs=GEO);ax.set_facecolor(C['water'])
ax.add_geometries(parts(selected['land']),GEO,facecolor=C['land'],edgecolor='#536565',lw=.7)
ax.add_geometries(parts(selected['hinge']),GEO,facecolor='#cfaa78',edgecolor='#855425',lw=.6)
ax.add_geometries([native(i) for i in islands],GEO,facecolor='#9bb9a0',edgecolor='#466a50',lw=.7)
axis=np.array(selected['axis'].coords);ax.plot(axis[:,0],axis[:,1],transform=GEO,color='#6f3e1e',lw=1.7,ls='--')
gl=ax.gridlines(draw_labels={'bottom':'x','left':'y'},crs=GEO,xlocs=np.arange(-100,-59,10),ylocs=np.arange(0,46,10),x_inline=False,y_inline=False,rotate_labels=False,linewidth=.45,color='#78908e');gl.xlabel_style={'size':9};gl.ylabel_style={'size':9}
labels=[(anchor_na,'1'),(tuple(rotate_xy(*anchor_sa,-6)),'2')]
for pos,label in labels:
    ax.plot(*pos,'o',transform=GEO,color='#243c43',ms=9,zorder=8)
    ax.annotate(label,xy=pos,xycoords=GEO._as_mpl_transform(ax),xytext=(9,7),textcoords='offset points',size=13,weight='bold')
for y,title,body in [(.74,'1  Northern attachment','Docks farther along the coast.\nThe old narrow waist becomes\na broad, bent land belt.'),(.59,'2  Southern attachment','Joins the displaced continent\naway from the basin interior.\nThe highland core moves with it.'),(.44,'Offshore remnants','Assumed old uplands survive\nas islands. Water gaps can filter\nwildlife and later travel.'),(.29,'Land and ocean routes','The new belt joins the continents.\nIt does not introduce a direct\ninter-ocean seaway here.')]:
    f.text(.735,y,title,size=12,weight='bold');f.text(.735,y-.026,body,size=11,va='top',linespacing=1.5)
f.text(.075,.13,'The dashed line shows geometric land continuity, not a surveyed pass, road or guaranteed habitable route.',size=11)
f.text(.075,.085,'Local equal-area view. Island survival, freshwater, relief and sea-level histories are design requirements, not measured results.',size=10,color=C['muted'])
save(f,'02-hinge-detail')

f=plt.figure(figsize=(16,10),facecolor=C['paper'])
f.text(.045,.95,'ERDE / GEOGRAPHY TRIAL',size=12,weight='bold',color=C['muted'])
f.text(.045,.90,'How much displacement helps?',size=27,weight='bold')
f.text(.045,.855,'Three spherical offsets around one native-coordinate Euler pole. The northern continent stays fixed in this comparison.',size=12)
for i,(name,case) in enumerate(cases.items()):
    ax=base_axes(f,[.03+i*.325,.33,.3,.46],case['land']);ax.set_title(name.capitalize(),size=15,pad=15)
    ax.add_geometries(parts(case['shifted']),GEO,facecolor='#c7d8be',edgecolor='#536e56',lw=.5)
    ax.add_geometries(parts(case['hinge']),GEO,facecolor='#c68b4e',edgecolor='#855425',lw=.5)
    m=case['metrics'];f.text(.05+i*.325,.26,f"Basin displacement: {m['basin_displacement_km']:.0f} km\nMaximum coastal latitude change: {m['max_coastal_latitude_change_degrees']:.1f}°\nLand connection: {'joined' if m['north_to_south_land_component'] else 'BROKEN'}",size=11,linespacing=1.6)
f.text(.055,.13,'Medium is the working candidate: visible separation without the stronger trial’s extra displacement.',size=12)
f.text(.055,.075,'This compares geometry and protected locations. It does not solve neighboring plate motions or predict regional rainfall.',size=10,color=C['muted'])
save(f,'03-offset-options')
print(json.dumps({name:c['metrics'] for name,c in cases.items()},indent=2))

f=plt.figure(figsize=(16,10),facecolor=C['paper'])
f.text(.045,.95,'ERDE / GEOGRAPHY TRIAL',size=12,weight='bold',color=C['muted'])
f.text(.045,.90,'Protected habitats and population regions',size=26,weight='bold')
f.text(.045,.855,'Representative land footprints and region locators move consistently with the candidate geography.',size=12)
ax=base_axes(f,[.055,.24,.66,.56],selected['land'])
for geom in [selected['basin'],selected['watershed']]:ax.add_geometries(parts(geom),GEO,facecolor='#a8c7a0',edgecolor='#496b4b',lw=.8,alpha=.9)
ax.add_geometries(parts(selected['hinge']),GEO,facecolor='#cfaa78',edgecolor='#855425',lw=.5)
for number,(name,pos) in zip([1,2,4,5],selected['metrics']['population_locators_native'].items()):
    ax.plot(*pos,'o',transform=GEO,color='#243c43',ms=9)
    ax.annotate(str(number),xy=pos,xycoords=GEO._as_mpl_transform(ax),xytext=(8,6),textcoords='offset points',size=13,weight='bold')
for row,(number,(name,pos)) in enumerate(zip([1,2,4,5],selected['metrics']['population_locators_native'].items())):
    f.text(.755,.76-row*.10,f'{number}  {name}',size=12,weight='bold')
    f.text(.755,.735-row*.10,f'{abs(pos[1]):.1f}°'+('N' if pos[1]>=0 else 'S'),size=11)
f.text(.755,.30,'3  Volcanic Hinge',size=12,weight='bold');f.text(.755,.272,'Ochre land belt between\nthe two continents.',size=11,linespacing=1.5,va='top')
f.text(.055,.15,'Green patches are protected interior land samples, not watershed boundaries or predictions of forest cover.',size=11)
f.text(.055,.105,'Geometric retention passes. Rainfall, catchment divides, elevation, productive area and viable travel remain conditional.',size=11)
f.text(.055,.06,'Two legacy offshore locators are replaced with on-land trial locators for the same broad coastal-rim and highland regions.',size=10,color=C['muted'])
save(f,'04-habitat-constraints')
