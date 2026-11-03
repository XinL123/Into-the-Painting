from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json,csv,hashlib
P=Path(__file__).parent
W,H=35311,1010
sources={
 'museum':'https://www.shanghaimuseum.net/mu/frontend/pg/m/article/id/CI00005093',
 'master':'https://commons.wikimedia.org/wiki/File:Prosperous_Suzhou.jpg',
 'study':'https://www.zgwypl.com/content/details78_48430.html',
 'clarification':'https://whly.ln.gov.cn/whly/mtjj/2026072413474910348/index.shtml',
 'dye':'https://www.suzhou.gov.cn/szsrmzf/szyw/202607/7fac602898bd4b60a664eba6b46ffb76.shtml',
 'tea':'https://m.jstv.com/news/2026/7/11/1525560875541487616.html',
 'school':'https://commons.wikimedia.org/wiki/File:Xu_Yang_-_Village_school.jpg',
 'textiles':'https://commons.wikimedia.org/wiki/File:Xu_Yang_-_Women_of_the_village_working.jpg',
 'theatre':'https://commons.wikimedia.org/wiki/File:Xu_Yang_-_Theatre_play.jpg',
 'penjing':'https://paper.people.com.cn/rmrbhwb/pc/content/202608/28/content_30177716.html'}
# Existing package IDs retained; display route follows actual master x descending.
rows=[
('02','School, Scroll-Style',(33590,790,33900,935),'Opening village','Open-front room, desks, seated and standing figures.','School identification supported; avoid asserting an exact conversation or pupil count.',['school','study'],'Matched scene; figures small.'),
('03','Cloth Starts at Home',(32540,610,33100,980),'Opening village','Long workshop room, courtyard equipment and household activity.','Cotton-production identification supported; no invented tool mechanism.',['textiles','study'],'Separate textile scan matches this courtyard.'),
('01','A Mountain Day Out',(30990,750,31620,990),'Lingyan foothills','Seated groups beneath pines, containers and a resting carrying chair.','Describe a mountain outing; do not invent names, verses or a menu.',['study'],'Visible gathering and equipment.'),
('04','Wedding Traffic, On Water?',(26980,600,27570,810),'Mudu, near the oblique bridge','Decorated boat with a crowded party on deck.','Wedding procession is a scholarly reading; use “Researchers identify…”; couple unknown.',['study'],'Boat real and distinct; event interpretation attributed.'),
('05','A Garden Party, Qing-Style',(24730,650,25080,850),'Mudu garden residence','Open red-trimmed hall with tables and guests, planted courtyards around it.','Describe a garden gathering; omit settled Suichu Garden identity.',['study'],'Visible hall and gathering.'),
('06','A Bridge with Nine Arches',(21740,235,22060,390),'Stone Lake','Small repeated arches of the long bridge behind the large single arch.','Identify Xingchun Bridge; moon-viewing tradition is background, not visible moonlight.',['study'],'Select rear nine-arch span, not foreground Yuecheng Bridge.'),
('10','Showtime in Old Suzhou',(18950,560,19570,880),'Between Stone Lake and the city','Bright temporary-looking stage, performers and dense audience.','A performance; no named play, opera genre or ticket price.',['theatre'],'Stage and audience unmistakable.'),
('07','A City in Full Color',(17550,710,17820,960),'Near Huai-Xu Bridge','Long colored lengths draped over rails outside a shop.','Dye works contextualized by report; four refers to the whole scroll, never this crop.',['dye','study'],'Colored fabric and shop visible.'),
('09','Tea with a Name',(11180,835,11600,1010),'North of Wannian Bridge','Upper-floor window groups above a street with a carried dark sedan.','Songluo Tea Room identified through museum-supplied close-up; no tea order or invented dialogue.',['tea'],'Exact facade/window/sedan sequence matched; master lettering too small to read independently.'),
('12','Signs, Signs Everywhere!',(7500,300,8000,475),'Street within Changmen','Continuous shopfronts with repeated hanging/vertical signs.','Point to visible signboards; avoid literal transcriptions here; optional total must be whole-scroll attributed.',['clarification'],'Sign objects visible, individual lettering small.'),
('08','A City Gate with a Crowd',(6900,600,7650,990),'Changmen','Labeled gate opening, fortified wall, bridge and crowd.','Reserve replacement for exam-snack slot; no invented queue rules or crowd identities.',['museum'],'Gate and crowd clearly visible; label can be matched.'),
('11','A City with Two Kinds of Streets',(4850,420,5600,800),'Shantang','Canal, vessels, waterside buildings and adjacent street/bridge.','Describe water and road routes side by side; no claimed precise city map.',['museum','study'],'Both route types visible in one context crop.'),
('13','A Tower at the Finish Line',(500,0,950,390),'Tiger Hill','Pagoda and hillside temple buildings near the scroll ending.','Reserve replacement for penjing; no claimed tilt, exact height, age or reconstruction history.',['museum'],'Tower conspicuous; top edge is as supplied in master.')]
out=[]
for order,(id,title,b,zone,anchor,guard,refs,confidence) in enumerate(rows,1):
 x0,y0,x1,y1=b
 out.append(dict(package_id=id,route_order=order,title=title,zone=zone,box=list(b),normalized_xywh=[round(x0/W,7),round(y0/H,7),round((x1-x0)/W,7),round((y1-y0)/H,7)],anchor=anchor,copy_guardrails=guard,verification=confidence,sources=[sources[k] for k in refs],status='proposed_verified_anchor_not_implemented'))
(P/'hotspots.json').write_text(json.dumps(dict(master='master-research.jpg',width=W,height=H,origin='top-left; x increases left-to-right',box_format='[x0,y0,x1,y1] in original master pixels',normalized_format='[x/W,y/H,width/W,height/H]',notes='Boxes are research scene bounds, not final click hit areas. Production camera padding and marker position require local viewport QA. All crops use exact master; no alternate scan substituted.',hotspots=out),ensure_ascii=False,indent=2))
with (P/'hotspots.csv').open('w') as f:
 wr=csv.writer(f);wr.writerow(['route','package_id','title','x','y','width','height','nx','ny','nw','nh']);
 for r in out:
  x,y,x1,y1=r['box'];wr.writerow([r['route_order'],r['package_id'],r['title'],x,y,x1-x,y1-y,*r['normalized_xywh']])
im=Image.open(P/'master-research.jpg'); (P/'hotspots').mkdir(exist_ok=True)
try: font=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',20);small=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',15)
except: font=small=ImageFont.load_default()
contact=Image.new('RGB',(1560,5*320+70),'#efe8d8');d=ImageDraw.Draw(contact);d.text((20,18),'PROSPEROUS SUZHOU | 13 proposed discoveries | exact-master crops',fill='#2b2723',font=font)
for i,r in enumerate(out):
 x0,y0,x1,y1=r['box'];margin=40
 cr=im.crop((max(0,x0-margin),max(0,y0-margin),min(W,x1+margin),min(H,y1+margin)))
 cr.save(P/'hotspots'/f"{r['route_order']:02d}-{r['package_id']}.jpg",quality=95)
 col=i%3;row=i//3;xx=col*520+12;yy=row*320+70
 d.text((xx,yy),f"{r['route_order']:02d}  {r['title']}",fill='#2b2723',font=font)
 cr.thumbnail((495,245));contact.paste(cr,(xx+(495-cr.width)//2,yy+29+(245-cr.height)//2));d.text((xx,yy+279),f"Package {r['package_id']} | {r['zone']}",fill='#6f675c',font=small)
contact.save(P/'hotspot-contact-sheet.jpg',quality=94)
# Six readable strips; displayed in reading order, each retains normal left/right direction.
mp=Image.new('RGB',(1700,6*360+65),'#efe8d8');md=ImageDraw.Draw(mp);md.text((20,18),'MASTER LOCATION MAP | Read each strip from RIGHT to LEFT; then move down',font=font,fill='#2b2723')
for n,(a,b) in enumerate([(30000,W),(24000,30000),(18000,24000),(12000,18000),(6000,12000),(0,6000)]):
 yy=65+n*360;scale=1660/(b-a);band=im.crop((a,0,b,H)).resize((1660,round(H*scale)));mp.paste(band,(20,yy+25));md.text((20,yy+2),f'x={a}..{b}',font=small,fill='#2b2723')
 for r in out:
  x0,y0,x1,y1=r['box'];cx=(x0+x1)/2;cy=(y0+y1)/2
  if a<=cx<b:
   left=20+(x0-a)*scale;top=yy+25+y0*scale;right=20+(x1-a)*scale;bottom=yy+25+y1*scale
   md.rectangle((left,top,right,bottom),outline='#a8382b',width=3);cxp=(left+right)/2;cyp=max(yy+42,top-12)
   md.ellipse((cxp-14,cyp-14,cxp+14,cyp+14),fill='#a8382b');md.text((cxp-10,cyp-10),f"{r['route_order']:02d}",font=small,fill='white')
mp.save(P/'location-map.jpg',quality=95)
lines=['# Story research and exact-master register','', 'Status: proposal only; all 13 retained anchors visually inspected. Two package topics replaced with its listed reserves. Route order follows x descending; original package IDs remain stable.','', '![Contact sheet](hotspot-contact-sheet.jpg)','', '| Route | Package ID | Title | Native box x0,y0,x1,y1 | Visual verification / copy constraint |','|---|---|---|---|---|']
for r in out:lines.append(f"| {r['route_order']:02d} | {r['package_id']} | {r['title']} | {','.join(map(str,r['box']))} | {r['verification']} {r['copy_guardrails']} |")
lines+=['','Coordinates: `hotspots.json` contains normalized x/y/width/height and per-scene evidence URLs. The visible objects are observations from the public-domain master; historical identities require the linked source.','', '## Unretained candidates','- Package 08: exam precinct and shopfronts found; exact 状元糕 / 状元考具 lettering not independently resolved on this master. Do not keep the snack claim attached to generic shops. Replaced by Changmen gate.','- Package 13: reporting mentions Tiger Hill penjing, but no confidently matched potted specimen here. Replaced by the visible pagoda.','- Granary warning remains reserve only: facade visible; warning transcription should not become a reading task on this scan.','', '## Text pass after approval','Keep English around 30–55 words per card: observation, one verified insight, optional light punchline. School wording hedged; wedding attributed; garden unnamed; moonlight contextual; no invented identities, species, conversations or exact count of visitors. Tea sign comes from matched museum detail, not independent OCR of master. Final microcopy still requires editorial review.','', '## Source register']
for k,u in sources.items():lines.append(f'- {k}: {u}')
(P/'STORY_RESEARCH.md').write_text('\n'.join(lines)+'\n')
