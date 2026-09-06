"""Redraw public Erde sheets in an equal-area projection with public terminology."""
from pathlib import Path
from tempfile import TemporaryDirectory
from erde_geometry import render_erde_maps
import json
import xml.etree.ElementTree as ET

SVG='http://www.w3.org/2000/svg'
ET.register_namespace('', SVG)
ET.register_namespace('xlink','http://www.w3.org/1999/xlink')
ns={'s':SVG}
folder=Path('assets/maps')
captions=[
 ('E1','erde-lands-and-seas','Lands and seas','A broad view of Erde’s continental land, seas and coordinate grid.','The view shows the distribution of land and water. Local shorelines and geographic boundaries require more detailed regional maps.'),
 ('E2','erde-latitude-zones','Latitude zones','Latitude bands show differences in solar input across Erde.','Latitude helps explain climatic contrasts, but rainfall, vegetation and ice also depend on relief, circulation and local conditions.'),
 ('E3','erde-relief-and-passages','Relief and passages','Mountain barriers, coastal approaches and island passages shape movement.','Mountain lines locate broad barriers and connections. They do not supply surveyed elevations or the detailed course of every valley.'),
 ('E4','erde-ancestry-and-dispersal','Ancestry and dispersal','Ancient human and hobbit populations branch and move between continental and island habitats.','Arrows combine movements from different periods. Shared ancestry and overlapping routes do not establish one culture or a political boundary.'),
 ('E5','erde-regional-contact','Regional contact','Five regional population complexes and their successor communities about five thousand years before the present.','The Great Watersheds, Volcanic Hinge, Highland Spine and Equatorial Basin retain self-sustaining networks. Coastal and mountain-rim communities continue through mixed successors.')]
replacements={
 'ancestral network':'population network',
 'ANDEL\'S SONG / FIELD ATLAS':'ERDE / WORLD ATLAS',
 'Bering: 23.6N':'Approach: 23.6N','Dakar reference: 40.9S':'Coastal site: 40.9S','Sunda: about 10S':'Island shelf: about 10S','Antarctic landmass':'Continental land',
 'A map of solar forcing zones, not a forecast of rainfall, ice, or vegetation.':'Latitude, solar input and the local conditions that shape habitats.',
 'DERIVED: transformed latitude. SCHEMATIC: forcing bands. No Earth ice sheet or biome map has been transplanted. [33, 38, NE]':'Latitude bands are schematic. Local rainfall, vegetation and ice require more detailed regional maps.',
 'African refugia remain conditional':'Ancestral habitats and refuges',
 'The selected African ancestral network belongs on productive ice-free':'The early ancestral network occupies productive ice-free',
 'peripheral routes, not automatically inside the south-polar interior.':'routes around harsher interiors. Productive ground is unevenly distributed.',
 'polar circles derived from a selected obliquity.':'polar circles. Local conditions vary within every band.',
 'Andean spine':'Highland spine','Western':'Coastal','Alpine-Himalayan':'Interior mountain','New Guinea':'Island','African':'Ancestral',
 'Inherited mountain systems provide a geographic scaffold; their mapped axes are approximate.':'Mountain chains divide the interiors and shape routes between communities.',
 'SCHEMATIC RELIEF: no elevations or plate-boundary predictions. Modern shorelines are a locator backdrop. [20, 24, 33, 38, NE]':'Schematic relief: lines mark broad mountain belts, not surveyed elevations or detailed valley boundaries.',
 '1  Beringian approaches':'1  Continental approaches','passage, not a copied Arctic':'passage. Conditions vary','ice barrier.':'along each route.',
 '2  American hinge':'2  Intercontinental hinge','Central American valleys and':'Valleys through the hinge and',
 '3  Sunda and island passages':'3  Shelf and island passages','Modern coastlines do not show':'Present shorelines do not show',
 'Continental topography is not a finished terrain model':'Mountains, refuges and movement',
 'Use this map to place candidate rain shadows, refuges, and contact zones. Mountain extent, elevation, rivers,':'Broad mountain belts create rain shadows, refuges and contact zones. Local elevation, river courses',
 'and paleocoasts need their own reconstruction.':'and former coastlines vary across the regions shown.',
 'Sunda-mainland':'Island-mainland','Luzon-like':'Isle A','Flores-like':'Isle B','Papuan-highland':'Highlanders','Sahul H-E':'Shelf human branch','American founders':'Continental founders',
 'Western archaics':'Related human branch','Eastern archaics':'Related human branch',
 'The selected evolutionary narrative, located approximately on the reference world.':'Ancestral populations and long routes through Erde’s history.',
 'HISTORY: selected scenario. DOTS: approximate region locators. DASHES: route sketches, not excavated tracks or range borders. [33, 38, NE]':'Dots locate broad ancestral regions. Dashed routes summarize movement across different periods.',
 'African sapiens-like':'Ancestral human','population network; Eurasian':'populations and several','Neanderthal-like and':'related continental','Denisovan-like sister':'human branches; island',
 'branches; deeper Sahul and':'settlement and early','American continuities.':'continental continuities.',
 'Sunda trunk and successive':'Island trunk and successive','Flores-like, Luzon-like,':'divergent island branches,','Papuan-highland, and pelagic':'highland and pelagic',
 'American founding interval':'Continental founding interval','Erectus-derived founders':'Early human founders','This is fictional history,':'Movement occurs across','not an Earth archaeological':'many generations and','claim.':'changing landscapes.',
 'Different dates share this locator map':'Routes across deep time',
 'Later sapiens-like entry':'Later human entry','The American contact landscape':'Regional contact and continuity',
 'EPOCH: about 5 kya. SYMBOLS indicate core regions, not exclusive ranges. Modern coastlines are reference geometry. [33, 38, NE]':'About five thousand years before the present. Symbols locate core regions, not exclusive ranges or political borders.',
 '1  Boreal Rim successors':'1  Coastal-rim successors','Interior and Atlantic-facing':'Interior and coastal',
 'Central American-Caribbean':'Intercontinental hinge','Andean-Pacific highlands,':'Mountain-chain highlands,','South American river-forest,':'Continental river-forest,',
 'Four self-sustaining First American complexes':'Four self-sustaining regional complexes',
 'At this epoch, complexes 2-5 retain independent population networks. The former Boreal Rim is represented by':'At this epoch, complexes 2-5 retain independent population networks. The coastal and mountain rim continues through',
}
generated=TemporaryDirectory(prefix='erde-atlas-')
render_erde_maps(generated.name)
originals=json.loads(Path('content/maps.json').read_text())
public=json.loads(Path('content/public/maps.json').read_text())
for code,stem,title,description,reading in captions:
 old=next(m for m in originals if m['code']==code)
 source=ET.parse(Path(generated.name)/(old['stem']+'.svg')).getroot()
 root=source
 for t in root.findall('.//s:text',ns):
  if t.text in replacements:t.text=replacements[t.text]
 root.set('role','img');root.set('aria-labelledby','map-title map-description')
 ET.SubElement(root,'{'+SVG+'}title',{'id':'map-title'}).text=title+' of Erde'
 ET.SubElement(root,'{'+SVG+'}desc',{'id':'map-description'}).text=description+' Equal-area view. '+reading
 ET.ElementTree(root).write(folder/(stem+'.svg'),encoding='utf-8',xml_declaration=True)
 item=next(m for m in public if m['code']==code)
 item.update(stem=stem,title=title,description=description,reading=reading,legacyStem=old['stem'])
Path('content/public/maps.json').write_text(json.dumps(public,ensure_ascii=False,indent=2)+'\n')
p=Path('content/public/erde-atlas.md');s=p.read_text().split('\n## Map sheets')[0]+'\n## Map sheets\n\n'
for m in public:
 if m['world']=='Erde':s+='- ['+m['code']+' · '+m['title']+'](../../assets/maps/'+m['stem']+'.svg): '+m['reading']+'\n'
p.write_text(s)
print('Prepared five public atlas variants')

generated.cleanup()
