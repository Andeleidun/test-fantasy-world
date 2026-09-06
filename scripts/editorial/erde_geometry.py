"""Authorial geographic inputs for the public atlas; all positions use one projection.

Reference coordinates locate established features, not public place names.
Called by prepare-erde-atlas.py, which supplies the reader-facing terminology.
"""
from pathlib import Path
import json, textwrap
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from pyproj import Geod
import cartopy.crs as ccrs
from shapely.geometry import shape

GLOBE=ccrs.Globe(ellipse=None,semimajor_axis=6371008.8,semiminor_axis=6371008.8)
GEO=ccrs.PlateCarree(globe=GLOBE)
FRAME=ccrs.RotatedPole(pole_longitude=-150,pole_latitude=0,globe=GLOBE)
GEODESIC=ccrs.Geodetic(globe=GLOBE)
ROT=GEO  # Plot in native Erde longitude/latitude after the coordinate rotation.
PROJECTION=ccrs.EqualEarth(globe=GLOBE)
# Fine projection subdivision keeps seam/pole geometry and overlays smooth.
PROJECTION.threshold=1000
LAND=[FRAME.project_geometry(shape(g),GEO) for g in json.loads(
    (Path(__file__).parent/'data/reference-land.geojson').read_text())['geometries']]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.labelcolor':'#243c43',
    'text.color':'#243c43','xtick.color':'#435b60','ytick.color':'#435b60',
    'svg.fonttype':'none','svg.hashsalt':'erde-equal-area-v1',
    'axes.spines.top':False,'axes.spines.right':False})
C={'ink':'#233c43','muted':'#536a6e','paper':'#f7f5ef','land':'#e0ddce','water':'#d9eaf0','blue':'#247fa1','green':'#558c64','lightgreen':'#cddfc9','amber':'#c17c36','hot':'#b45939','cold':'#52738e','ice':'#ddebf0','purple':'#836d9a','rock':'#bcb6a8','dark':'#182f44'}

def figmap(code,world,title,subtitle,status):
    f=plt.figure(figsize=(16,10),facecolor=C['paper'])
    f.text(.045,.951,"ANDEL'S SONG / FIELD ATLAS",size=11,weight='bold',color=C['muted'])
    f.text(.955,.951,f'{world.upper()}  /  {code}',size=11,ha='right',weight='bold')
    f.text(.045,.894,title,size=27,weight='bold')
    f.text(.045,.855,subtitle,size=12,color=C['muted'])
    f.text(.045,.034,status,size=9,color=C['muted'])
    f.text(.955,.034,code,size=10,ha='right',weight='bold')
    return f

def note(f,x,y,title,body,width=47):
    f.text(x,y,title,size=11,weight='bold',va='top')
    f.text(x,y-.029,'\n'.join(textwrap.wrap(body,width)),size=10.5,va='top',linespacing=1.45,color=C['muted'])

def earth(f,rect=(.055,.27,.69,.55),land=C['land'],grid=True,regional=False):
    ax=f.add_axes(rect,projection=PROJECTION)
    ax.set_global();ax.set_facecolor(C['water'])
    ax.add_geometries(LAND,GEO,facecolor=land,edgecolor='#637575',linewidth=.55,zorder=2)
    if grid:
        gl=ax.gridlines(crs=GEO,draw_labels={'bottom':'x',**({'left':'y'} if regional else {})},
            xlocs=np.arange(-180,181,60),ylocs=np.arange(-60,61,30),
            linewidth=.4,color='#78908e',alpha=.55,zorder=3,
            x_inline=False,y_inline=False,rotate_labels=False)
        gl.xlabel_style={'size':8};gl.ylabel_style={'size':8}
        if not regional:
            for latitude in [-60,-30,0,30,60]:
                label=f'{abs(latitude)}°'+('N' if latitude>0 else 'S' if latitude<0 else '')
                ax.annotate(label,xy=(-180,latitude),xycoords=GEO._as_mpl_transform(ax),
                    xytext=(-5,0),textcoords='offset points',ha='right',va='center',size=8)
    return ax

def tr(lon,lat):return FRAME.transform_point(lon,lat,GEO)

def elabel(ax,lon,lat,label,dx=0,dy=0,size=10,color=None,marker=False):
    x,y=tr(lon,lat)
    if marker:ax.plot(x,y,'o',color=color or C['ink'],ms=4,transform=ROT,zorder=7)
    if marker and (dx or dy):ax.plot([x,x+dx],[y,y+dy],color=color or C['muted'],lw=.6,transform=ROT,zorder=7)
    return ax.text(x+dx,y+dy,label,transform=ROT,size=size,ha='center',va='center',color=color or C['ink'],zorder=8,bbox={'facecolor':C['paper'],'alpha':.83,'edgecolor':'none','pad':1.5})

def route(ax,coords,color,label=None,ls='--',lw=2):
    pts=np.array([tr(*p) for p in coords]);ax.plot(pts[:,0],pts[:,1],color=color,lw=lw,ls=ls,zorder=6,transform=GEODESIC)
    # One path per route; an un-stroked arrowhead follows its final geodesic tangent.
    geod=Geod(a=6371008.8,b=6371008.8)
    start,end=pts[-2],pts[-1]
    azimuth,_,distance=geod.inv(*start,*end)
    tangent=geod.fwd(*start,azimuth,distance*.95)[:2]
    tip=PROJECTION.transform_point(*end,GEO)
    tail=PROJECTION.transform_point(*tangent,GEO)
    ax.annotate('',xy=tip,xytext=tail,zorder=7,arrowprops={
        'arrowstyle':'-|>','color':color,'lw':0,'mutation_scale':12,'shrinkA':0,'shrinkB':0})
    if label:
        mid=pts[len(pts)//2];ax.text(*mid,label,size=9,color=color,zorder=8,transform=ROT)

def save(f,code,title,world,description,provenance):
    stem=f'{code}-{title.lower().replace(" / ","-").replace(" ","-")}'
    for ch in ['?',':',',','(',')']:stem=stem.replace(ch,'')
    f.savefig(MAPS/(stem+'.svg'),format='svg',facecolor=f.get_facecolor(),metadata={'Date':None})
    plt.close(f)

def render_erde_maps(output):
    global MAPS
    MAPS=Path(output)
    # E1 is a single native-coordinate overview; reference crosswalks remain authorial.
    f=figmap('E1','Erde','Lands and seas','Continental geography and the seas connecting its shores.','Equal-area view. Coastlines are broad outlines; no political borders are shown.')
    a=earth(f,(.085,.16,.83,.65))
    save(f,'E1','Orientation comparison','Erde','','')

    # E2: insolation bands, deliberately not a purported GCM biome map.
    f=figmap('E2','Erde','Latitude and climate potential','A map of solar forcing zones, not a forecast of rainfall, ice, or vegetation.','DERIVED: transformed latitude. SCHEMATIC: forcing bands. No Earth ice sheet or biome map has been transplanted. [33, 38, NE]')
    a=earth(f,land='none')
    bands=[(-90,-60,C['ice']),(-60,-30,'#d5dfcf'),(-30,30,'#e6d7ad'),(30,60,'#d5dfcf'),(60,90,C['ice'])]
    for lo,hi,col in bands:a.add_patch(Rectangle((-180,lo),360,hi-lo,transform=ROT,fc=col,ec='none',zorder=1))
    a.add_geometries(LAND,GEO,facecolor='none',edgecolor='#566a66',lw=.8,zorder=4)
    for y in [-60,-30,0,30,60]:a.plot(np.linspace(-180,180,361),np.full(361,y),transform=ROT,color=C['muted'],lw=1 if y==0 else .5,zorder=5)
    elabel(a,-169,65,'Bering: 23.6N',10,9,marker=True)
    elabel(a,-17.4,14.7,'Dakar reference: 40.9S',-5,10,marker=True)
    elabel(a,110,0,'Sunda: about 10S',5,-14,marker=True)
    elabel(a,0,-80,'Antarctic landmass\nat low latitude',32,11)
    note(f,.775,.77,'Low latitude | within 30 degrees','Stronger average solar input. Wet forests, seasonal vegetation, or dry interiors depend on circulation and relief.',29)
    note(f,.775,.56,'Middle latitude | 30-60 degrees','Potentially large seasonality and maritime/interior contrasts. Latitude alone does not determine habitat.',29)
    note(f,.775,.35,'High latitude | beyond 60 degrees','Low annual solar input. Ice extent depends on elevation, greenhouse forcing, ocean transport, and orbital seasonality.',29)
    note(f,.055,.19,'African refugia remain conditional','The selected African ancestral network belongs on productive ice-free peripheral routes, not automatically inside the south-polar interior.',73)
    note(f,.54,.19,'Do not read the color as a biome','Band edges are explanatory 30-degree intervals, not tropical or polar circles derived from a selected obliquity.',65)
    save(f,'E2','Latitude and climate potential','Erde','New-latitude forcing bands with reference sites; separates geometric constraints from unmodeled regional climates.','33; 38; Natural Earth land')

    # E3: relief and biogeographic barriers as a spatial scaffold.
    f=figmap('E3','Erde','Relief, barriers, and passages','Inherited mountain systems provide a geographic scaffold; their mapped axes are approximate.','SCHEMATIC RELIEF: no elevations or plate-boundary predictions. Modern shorelines are a locator backdrop. [20, 24, 33, 38, NE]')
    a=earth(f)
    ranges=[('Andean spine',[(-75,5),(-76,-10),(-69,-30),(-72,-50)]),('Western cordillera',[(-145,61),(-124,48),(-112,35),(-103,22)]),('Alpine-Himalayan system',[(0,43),(25,39),(45,35),(70,34),(88,29),(100,27)]),('East African highlands',[(35,12),(37,0),(33,-15)]),('New Guinea highlands',[(132,-4),(141,-5),(149,-7)])]
    for label,pts in ranges:
        q=np.array([tr(*p) for p in pts]);a.plot(q[:,0],q[:,1],color=C['amber'],lw=3.3,transform=GEODESIC,zorder=6)
    for lon,lat,label,dx,dy in [(-73,-22,'Andean spine',20,-8),(-119,42,'Western\ncordillera',-25,9),(65,32,'Alpine-Himalayan\nbarrier system',-10,13),(140,-5,'New Guinea\nhighlands',-3,-15),(36,0,'African\nhighlands',-21,18)]:elabel(a,lon,lat,label,dx,dy,size=9)
    for lon,lat,label,dx,dy in [(-169,65,'1',0,0),(-83,10,'2',0,0),(112,-2,'3',0,0)]:
        x,y=tr(lon,lat);a.scatter([x],[y],s=190,c=C['paper'],edgecolors=C['blue'],linewidths=2,transform=ROT,zorder=8);a.text(x,y,label,ha='center',va='center',weight='bold',zorder=9,transform=ROT)
    note(f,.775,.76,'1  Beringian approaches','A low-to-subtropical connection. Sea level, food, terrain, and climate govern passage, not a copied Arctic ice barrier.',29)
    note(f,.775,.54,'2  American hinge','Central American valleys and coasts connect the continents. Mountains and regional habitats create bottlenecks.',29)
    note(f,.775,.32,'3  Sunda and island passages','Shelf exposure reconnects some lands; deep-water straits still isolate others. Modern coastlines do not show past crossings.',29)
    note(f,.055,.19,'Continental topography is not a finished terrain model','Use this map to place candidate rain shadows, refuges, and contact zones. Mountain extent, elevation, rivers, and paleocoasts need their own reconstruction.',110)
    save(f,'E3','Relief and passages','Erde','An approximate mountain and passage scaffold for planning isolation, rain shadows, and migration.','20; 24; 33; 38; modern reference mountain axes')

    # E4: selected ancestry routes, no contemporary sovereign territories.
    f=figmap('E4','Erde','Ancestral centers and dispersal','The selected evolutionary narrative, located approximately on the reference world.','HISTORY: selected scenario. DOTS: approximate region locators. DASHES: route sketches, not excavated tracks or range borders. [33, 38, NE]')
    a=earth(f)
    route(a,[(-17,15),(-6,35),(30,40),(65,28),(100,20)],C['hot'])
    route(a,[(108,1),(118,-5),(135,-5),(145,-15)],C['purple'])
    route(a,[(112,0),(122,8),(122,18)],C['purple'])
    route(a,[(110,-2),(120,-8)],C['purple'])
    route(a,[(130,35),(155,55),(-169,65),(-135,58),(-116,42)],C['blue'])
    points=[(-17,20,'African\nancestral network',-24,11,C['hot']), (109,1,'Sunda-mainland\ndivergence',-32,-4,C['purple']), (122,18,'Luzon-like',12,8,C['purple']), (120,-8,'Flores-like',12,-23,C['purple']), (143,-6,'Papuan-highland',23,-12,C['purple']), (145,-22,'Sahul H-E',12,12,C['blue']),(-160,64,'American founders',0,13,C['blue']), (15,45,'Western archaics',-18,-9,C['hot']), (75,40,'Eastern archaics',-4,-12,C['hot'])]
    for lon,lat,label,dx,dy,col in points:elabel(a,lon,lat,label,dx,dy,size=9,color=col,marker=True)
    note(f,.775,.77,'Human-form ancestry','African sapiens-like population network; Eurasian Neanderthal-like and Denisovan-like sister branches; deeper Sahul and American continuities.',29)
    note(f,.775,.53,'Hobbit-form radiation','Sunda trunk and successive Flores-like, Luzon-like, Papuan-highland, and pelagic branches. Maritime networks are not bounded ethnic states.',29)
    note(f,.775,.28,'American founding interval','Erectus-derived founders arrive about 650-450 thousand years before Erde present. This is fictional history, not an Earth archaeological claim.',29)
    note(f,.055,.17,'Different dates share this locator map','Arrows summarize branching and movement across deep time. Their overlap does not imply simultaneous populations or uninterrupted access.',112)
    save(f,'E4','Ancestry and dispersal','Erde','Locate the selected African ancestry, Sunda radiation, Sahul branch, and early American migration without inventing political borders.','33; 38')

    # E5: American complexes and contact status at a defined date.
    f=figmap('E5','Erde','The American contact landscape','Regional complexes and mixed successors around 5,000 years before Erde present.','EPOCH: about 5 kya. SYMBOLS indicate core regions, not exclusive ranges. Modern coastlines are reference geometry. [33, 38, NE]')
    a=earth(f,(.055,.275,.69,.54),regional=True);a.set_extent([-155,65,-45,75],crs=ROT)
    complexes=[(-133,55,'1'),(-94,38,'2'),(-84,13,'3'),(-73,-22,'4'),(-58,-6,'5')]
    cols=[C['purple'],C['green'],C['amber'],C['hot'],C['blue']]
    for (lon,lat,n),co in zip(complexes,cols):
        x,y=tr(lon,lat);a.scatter(x,y,s=700,facecolors=co,edgecolors=C['paper'],lw=2,alpha=.9,transform=ROT,zorder=7);a.text(x,y,n,ha='center',va='center',color='white',size=14,weight='bold',zorder=8,transform=ROT)
    route(a,[(150,58),(-169,65),(-140,58),(-122,43),(-97,32),(-83,12)],C['ink'])
    elabel(a,-169,65,'Later sapiens-like entry\n35-20 kya',16,19,size=9,marker=True)
    items=[('1  Boreal Rim successors','Several mixed regional networks; ancestral continuity remains.'),('2  Great Watersheds','Interior and Atlantic-facing river, lake, and lowland systems.'),('3  Volcanic Hinge','Central American-Caribbean highlands, valleys, coasts, and islands.'),('4  Highland Spine','Andean-Pacific highlands, intermontane valleys, and coastal routes.'),('5  Equatorial Basin','South American river-forest, wetland, and savanna networks.')]
    for i,(title,body) in enumerate(items):note(f,.775,.79-i*.12,title,body,30)
    note(f,.055,.19,'Four self-sustaining First American complexes','At this epoch, complexes 2-5 retain independent population networks. The former Boreal Rim is represented by connected mixed successors, not disappearance of its people or cultures.',108)
    save(f,'E5','American contact landscape','Erde','Defined-epoch map of the five First American regional complexes and the northern successor outcome.','33 paragraphs 148-178; 38')
