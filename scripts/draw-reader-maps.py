"""Draw qualitative reader diagrams from the synchronized public descriptions."""
from pathlib import Path
from html import escape

OUT=Path('assets/guide-maps')
OUT.mkdir(exist_ok=True)
INK='#253932'; MUTED='#52645d'; BLUE='#467789'; LAND='#dce5cc'; GOLD='#a96f38'; PAPER='#faf7ed'
def txt(x,y,s,size=19,fill=INK,anchor='start',weight='normal'):
 return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{escape(s)}</text>'
def path(d,fill='none',stroke=INK,width=2,extra=''):
 return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" {extra}/>'
def rect(x,y,w,h,fill=LAND,rx=12):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"/>'
def line(x1,y1,x2,y2,color=INK,width=2,dash=''):
 return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}" stroke-dasharray="{dash}"/>'
def circle(x,y,r,fill,stroke='none'):
 return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
def lines(x,y,ss,size=18,step=27,fill=MUTED):
 return ''.join(txt(x,y+i*step,s,size,fill) for i,s in enumerate(ss))
def panel(x,y,w,h,title,ss,fill=LAND):
 return rect(x,y,w,h,fill)+txt(x+22,y+34,title,min(23,int((w-44)/(len(title)*.60))),weight='bold')+lines(x+22,y+67,ss)
def save(name,title,desc,body,height=720,foot='Schematic relationships; positions and distances are not surveyed.'):
 svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{height}" viewBox="0 0 1000 {height}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto-start-reverse"><path d="M0 0L8 4L0 8" fill="{BLUE}"/></marker><linearGradient id="light"><stop stop-color="#d9b26a"/><stop offset=".42" stop-color="#d9b26a"/><stop offset=".5" stop-color="#77916f"/><stop offset=".58" stop-color="#344d49"/><stop offset="1" stop-color="#192e35"/></linearGradient></defs><rect width="1000" height="{height}" fill="{PAPER}"/><g font-family="Georgia,serif">{txt(38,52,title,32)}{txt(38,84,desc,17,MUTED)}{body}{line(38,height-55,962,height-55,'#c8d0c2',1)}{txt(38,height-26,foot,16,MUTED)}</g></svg>'''
 (OUT/(name+'.svg')).write_text(svg)

# Erde: contact geography follows the documented coastal relay and headwaters.
b=rect(38,113,190,519,'#d9e7e8')+txt(62,153,'Coastal route',24)+lines(62,187,['Short voyages,','estuaries and','offshore islands.'])
b+=path('M155 275 C78 312 100 365 180 366 L270 366',stroke=BLUE,width=4,extra='stroke-dasharray="9 7" marker-end="url(#arrow)"')
b+=panel(278,116,310,128,'Coasts and mountain rim',['Early approach; later','mixed successor communities.'])
b+=panel(648,116,310,164,'Great Watersheds',['Rivers, lakes and wetlands.','Defended interior crossings;','basin councils and orders.'])
b+=line(588,177,642,177,BLUE,3,'6 5')+txt(636,310,'Coastal travel bypasses',17,MUTED)+txt(636,333,'the defended interior.',17,MUTED)
b+=panel(278,298,310,137,'Volcanic Hinge',['Highlands, islands and valleys.','Warnings and maritime refuges.'])
b+=panel(278,476,310,137,'Highland Spine',['Coasts, valleys and plateaus.','Guides and refuge houses.'])
b+=panel(648,476,310,137,'Equatorial Basin',['Headwaters, forests and rivers.','River-garden houses.'])
b+=path('M424 244 L424 291',stroke=BLUE,width=3,extra='marker-end="url(#arrow)"')
b+=path('M424 435 L424 469',stroke=BLUE,width=3,extra='marker-end="url(#arrow)"')
b+=path('M588 541 L640 541',stroke=BLUE,width=3,extra='marker-end="url(#arrow)"')+txt(618,580,'Headwater',12,MUTED,anchor='middle')+txt(618,598,'route',12,MUTED,anchor='middle')
save('erde-regions','Erde: regions and routes','Regional contact, coastal passages and the headwater approach.',b,foot='E1 · E3 · E5 | Route relationships only; arrows summarize later migration, not a single journey.')

b=panel(38,120,270,455,'Latitude',['Latitude influences light','and seasonal conditions.','','Local relief and water','also shape the landscape.'],'#e9e2c7')
for y,l in [(318,'Higher latitudes'),(390,'Middle latitudes'),(462,'Equatorial country')]:
 b+=line(65,y,280,y,'#978861',2,'5 5')+txt(65,y+26,l,17)
b+=path('M350 506 L430 390 L510 347 L600 199 L695 337 L755 415 L880 466 L960 506 Z',LAND,'#7b8b70',2)
b+=path('M558 261 L600 199 L647 270 L618 257 L599 275 L581 253 Z','#eff1e8','#eff1e8')
b+=path('M430 403 C455 435 450 477 505 519 C577 552 617 513 656 553',stroke=BLUE,width=5)
b+=txt(350,158,'Relief and water',25)+txt(628,233,'High country',19)+txt(366,580,'Valleys and rivers',19)+txt(728,412,'Sheltered slopes',18)
b+=lines(355,615,['Mountain chains divide interiors; rivers connect settlements.'],18)
save('erde-landscape','Erde: reading the landscape','Latitude, mountains and water describe different parts of a place.',b,720,'E2 | Qualitative section; no temperature, rainfall or elevation scale is assigned.')

b=panel(340,115,320,90,'Shared deep ancestry',[],fill='#e9e2c7')
b+=path('M500 205 L500 234 L230 234 L230 268',stroke=BLUE,width=3,extra='marker-end="url(#arrow)"')
b+=path('M500 234 L758 234 L758 268',stroke=BLUE,width=3,extra='marker-end="url(#arrow)"')
b+=panel(38,278,410,130,'Human branches',['Separation, migration and later contact.','Some branches exchange ancestry.'])
b+=panel(550,278,410,130,'Hobbit lineages',['Island, highland and seafaring branches.','Different histories and ways of living.'])
b+=line(448,355,550,355,BLUE,2,'5 5')+txt(500,447,'Human–hobbit interbreeding is rare and usually has low fertility.',18,MUTED,anchor='middle')
b+=panel(38,485,410,135,'The Thal departure',['Erde refugees passed through the','Otherworld about 5,000 years ago.'],'#e9e2c7')
b+=panel(550,485,410,135,'Dverghamar',['Thal descendants settled among','native peoples with separate ancestry.'],'#d9e7e8')
b+=path('M448 551 L542 551',stroke=BLUE,width=3,extra='marker-end="url(#arrow)"')
save('erde-ancestry','Erde: ancestry and the Thal migration','Broad inferred descent and a much later historical journey.',b,720,'E4 | Branching dates and a detailed family tree remain uncertain. Culture does not follow descent alone.')

b=circle(266,324,184,'url(#light)')+path('M266 140 C231 231 231 414 266 508 C301 414 301 231 266 140',fill='#9aaf80',stroke='none',extra='opacity=".55"')
b+=lines(53,551,['Sunward hemisphere'],19)+lines(308,551,['Nightward hemisphere'],17)
b+=line(266,155,352,121,'#52645d')+txt(355,126,'Twilight',20)
b+=panel(530,122,430,117,'Sunward margin',['Hot, dry ground; salt and brine basins.','Water-bearing refuges occur locally.'],'#e9d5ac')
b+=panel(530,267,430,145,'Twilight landscapes',['Lit slopes and watered valleys support','most settlements and familiar large life.','Dry divides interrupt fertile districts.'])
b+=panel(530,440,430,117,'Nightward country',['Cold and darkness; ice farther nightward.','Reports of isolated warm sites.'],'#d9e4e8')
b+=txt(64,605,'Sunlight',18,MUTED)+path('M158 598 L394 598',stroke=BLUE,width=3,extra='marker-end="url(#arrow)"')
save('dverghamar-light','Dverghamar: day, night and twilight','The inhabited country follows light and water across a varied landscape.',b,720,'D1 · D2 | Twilight is not a uniform fertile ring. Widths and continental outlines are unspecified.')

b=path('M38 482 L115 400 L189 342 L250 248 L299 322 L347 203 L435 385 L516 450 L589 425 L641 495 L962 514 L962 624 L38 624Z','#d1c7ad','#877c65',2)
b+=path('M305 265 L347 203 L393 290 L353 274 L337 291Z','#edf0e8','#edf0e8')
b+=rect(180,337,90,32,PAPER,3)+rect(307,410,83,32,PAPER,3)+rect(390,514,90,36,PAPER,3)
b+=path('M269 353 L292 353 L292 426 L306 426',stroke=PAPER,width=11)
b+=line(226,280,226,332,BLUE,2)+txt(48,244,'Little rock overhead',20)+path('M225 251 L226 276',stroke=BLUE)
b+=line(158,355,158,480,BLUE,2,'5 5')+txt(45,523,'High above',17)+txt(45,547,'the valley',17)
b+=txt(329,594,'A deeper mine',19)+line(445,554,445,570,BLUE)
b+=path('M379 280 C398 316 419 336 435 385 C447 439 544 478 660 497 C719 509 733 538 821 539',stroke=BLUE,width=7)
b+=path('M764 551 C772 510 835 491 921 513 C978 536 909 581 823 574Z','#a7c7ce','none')
b+=rect(582,442,107,28,'#9bae7d',3)+line(590,447,681,447,'#4b674b')+line(590,455,681,455,'#4b674b')+line(590,463,681,463,'#4b674b')
b+=path('M495 470 L544 443 L548 412 L569 412 L571 443 L587 453',stroke=GOLD,width=4,extra='stroke-dasharray="7 5"')
b+=circle(543,457,18,PAPER,INK)+line(526,457,560,457)+line(543,440,543,474)
b+=txt(505,181,'Mountain homes and their countryside',23)+lines(525,225,['Surface farms supply food.','Roads and rivers connect settlements.','Water drives workshops.','Homes need fresh air and drainage.'])
b+=txt(641,414,'Fields',18)+txt(830,605,'Lake',19)+txt(695,364,'Rivers and springs',18)+path('M743 374 L732 438 L689 489',stroke=BLUE)
save('dverghamar-settlement','Dverghamar: water and mountain homes','A cross-section connects chambers, valley farms and surface water.',b,720,'D4 · D5 · D7 | Illustrative section. Height above a valley differs from burial depth; no engineering scale.')

b=panel(38,121,292,204,'Warm margins',['Sunward peoples: dry heat','and water conservation.','Volcanic ranges: humid','heat, ash and local','chemical exposure.'],'#e9d5ac')
b+=panel(354,121,292,204,'Mountain interiors',['Central massif peoples.','','The deep-massif subspecies','retains connections with','shallower ecosystems.'])
b+=panel(670,121,292,204,'Cold and high country',['Cold-edge peoples near the','productive twilight region.','','High-mountain peoples face','thin air as well as cold.'],'#d9e4e8')
b+=txt(500,365,'Habitats overlap. These are not political or language borders.',19,MUTED,anchor='middle')
b+=path('M45 484 Q145 470 240 502 Q320 560 451 512 Q548 478 655 514 Q797 480 962 496 L962 616 L38 616Z',LAND,'#758870')
b+=path('M156 490 Q249 539 363 500 Q363 572 255 584 Q170 571 156 490Z','#94bcc6','none')
b+=txt(45,414,'Lakes and productive shores',22)+lines(45,448,['Some large lake animals reach several metres.','Water depth alone does not establish safe fishing.'],17)
b+=circle(796,533,42,'#b69b74')+circle(796,533,25,'#c5d8cd')+txt(590,585,'An isolated warm refuge',21)+lines(590,414,['Ice and darkness surround warm sites.','Reports describe sparse small life;','many places remain undescribed.'],17)
save('dverghamar-habitats','Dverghamar: habitats and refuges','Related peoples occupy varied ground; lakes and isolated sites support different life.',b,720,'D3 · D6 · D8 | A habitat comparison, not a species range map or a wildlife identification plate.')

b=rect(38,118,438,438,'#d9e7e8')+rect(522,118,438,438,'#e7dfcf')
b+=txt(65,158,'Merenval',29)+txt(549,158,'The inhabited companion',27)
b+=path('M60 344 Q118 321 145 339 T245 355 T353 339 T456 351 L456 407 L60 407Z','#94bcc6','none')
b+=path('M60 334 L95 261 L136 290 L191 220 L260 313 L327 271 L383 320 L456 295 L456 342 Q350 380 260 346 T60 364Z',LAND,'#7b8b70')
b+=path('M545 356 L578 356 L578 223 L611 223 L617 321 L645 321 L645 273 L683 273 L683 354 L719 354 L719 224 L752 224 L760 342 L792 342 L792 276 L918 276 L941 357Z','#c4bba0','#877c65')
b+=path('M791 357 C783 297 902 297 899 357',PAPER,'#877c65')
b+=lines(65,440,['Connected seas, forests and wetlands.','Forest and Maritime/Littoral Sylvans.','Voyaging links coasts and islands.'],19)
b+=lines(549,440,['Plateaus, pillars, caverns and separated seas.','Crystalline/High and Deep/Star Elves.','Gnome communities and living houses.'],18)
b+=path('M431 200 C486 175 513 175 565 200',stroke=BLUE,width=3,extra='marker-start="url(#arrow)" marker-end="url(#arrow)"')
b+=txt(500,599,'Travel and kinship connect the pair. Orc societies inhabit both worlds.',20,anchor='middle')
b+=txt(500,630,'Similarities of life suggest shared ancestry; the early passage remains unknown.',18,MUTED,anchor='middle')
save('merenval-pair','Merenval and its companion','Two inhabited landscapes, with continuing contact and distinct communities.',b,740,'Landscape comparison only; the drawing gives no orbital scale, fixed locations or exclusive territories.')
print('Drew seven reader maps.')
