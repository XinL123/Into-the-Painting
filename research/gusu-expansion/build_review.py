from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,math,textwrap,html,csv
P=Path(__file__).resolve().parent
MASTER=P.parent/'gusu-proposal/master-research.jpg'
W,H=35311,1010
im=Image.open(MASTER).convert('RGB'); assert im.size==(W,H)
S='https://www.zgwypl.com/content/details78_48430.html'
B='https://xuebaosk.ahut.edu.cn/cn/article/pdf/preview/10.3969/j.issn.1671-9247.2021.02.013.pdf'
C='https://www.chinagrain.org.cn/luntan/ff808081978ec6f90197ed4d669c0b30.html'
M='https://commons.wikimedia.org/wiki/File:Prosperous_Suzhou.jpg'
data=[
 dict(id='A',title='A Bridge into Business',decision='revised',box=[29120,540,29870,1000],context=[28500,120,30300,1010],anchor=[29540,610],visual='High',historical='Medium',
 text="A bridge, a river, and shops almost at your feet. Researchers describe this part of Mudu as a busy commercial district. With shopfronts opening toward the waterfront, crossing the river could bring you straight into the market. A handy place to combine two errands!",
 observed='High arched bridge beside a continuous waterfront shop row; steps, pedestrians, boats and open shopfronts are visible.',
 evidence='Study: Mudu paragraph beginning 作者以木渎镇. The same market sequence contains the distinctive pavilion behind the shops and the wedding boats farther left. The commercial district is supported; the precise named bridge is not established independently.',
 guard='Removed the specific oblique-bridge identity. No shop trades, ownership, or actual errands assigned to individuals.',sources=[S],zoom='750 x 460 scene; bridge remains readable at native scale. Bottom margin only 10 px: retain full source height in context and do not force vertical centering.'),
 dict(id='B',title='A Temple Behind the Shops?',decision='revised',box=[28970,320,29240,510],context=[28680,220,29600,740],anchor=[29090,435],visual='High',historical='Medium',
 text="Shopping in front, something quieter behind. See the small, many-sided tower tucked among the roofs? Researchers identify this compound as a temple behind Mudu's waterfront shops. Its pavilion rises above an enclosed courtyard. The busy riverfront has more than one layer to explore.",
 observed='Distinct red two-level polygonal pavilion, enclosed court and aligned halls behind the commercial frontage.',
 evidence='Study: same Mudu paragraph describes a temple behind shops with a two-storey hexagonal pavilion and axial halls. Spatial configuration matches; the six sides and interior statue cannot all be independently resolved here.',
 guard='Do not name temple or deity, count six visible sides, identify monks, or claim the courtyard is actually quiet. Quiet is an editorial contrast, not an observed sound.',sources=[S],zoom='270 x 190 detail; use 920 x 520 context for camera. Pavilion remains small (~100 native px high); do not enlarge to fill a card-sized viewport.'),
 dict(id='C',title='A Granary with a Backup Plan',decision='revised',box=[24650,40,25650,460],context=[24300,0,25900,800],anchor=[25200,280],visual='High',historical='Medium',
 text="Those long roofs had a practical purpose. Researchers identify this waterside compound as a shecang, or community granary. Such granaries held grain to help communities withstand shortages. The rows of storehouses make a useful counterpoint to all those shops: prosperity needed a backup plan, too.",
 observed='Rectangular stone platform surrounded by water, four repeated roof rows, enclosed yard and long rear buildings.',
 evidence='Study: paragraph beginning 在湖对岸 describes the square community granary, stone base and four warehouse rows. Grain Economics Society research supports the general relief function, not documented transactions at this building.',
 guard='Actual compound lies beyond the pack C band. Place BEFORE existing garden #05, not between #05 and #06. No wall-warning transcription, loans, precise management system, or contents claimed visible.',sources=[S,C],zoom='1000 x 420 scene. Garden #05 is below and left; marker chosen on upper storehouse block. Green reproduction seam remains intact. Context touches top boundary; avoid cropping warehouse roofs.'),
 dict(id='D',title="Farming at the Water's Edge",decision='revised',box=[20200,350,20980,710],context=[19800,180,21500,850],anchor=[20700,590],visual='High',historical='Medium',
 text="Not quite an empty lake! Low banks divide this waterside landscape into plots. Researchers describe fields and fishponds around Stone Lake, where people adapted the watery surroundings for food production. The shoreline was a working landscape as well as a scenic one. Look between the banks.",
 observed='Repeated low embankments enclose small plots and water areas; cultivated-looking strips differ from open lake beyond.',
 evidence='Study Stone Lake paragraph explicitly identifies fields opened in water and enclosed fishponds. The crop shows the bank-divided landscape in that same lake sequence; it does not establish which individual enclosure held fish.',
 guard='No fish species, exact plot use, technique, acreage or invented worker activity. Revised away from the draft assertion someone is hard at work in this crop.',sources=[S],zoom='780 x 360 detail; relief is subtle. Context needed to distinguish plots from open lake. No extra sharpness processing or claim to see fish.'),
 dict(id='E',title='A Street for Almost Everything',decision='revised',box=[16200,750,16750,1010],context=[15900,500,17400,1010],anchor=[16430,915],visual='High',historical='Medium',
 text="Silk wasn't the whole shopping list. Researchers describe rice merchants, shoe shops, wine sellers, and other businesses near Huai-Xu Bridge. This waterfront row belongs to that bustling market area. We're not decoding every tiny sign here, but the takeaway is clear: everyday shopping had plenty of variety.",
 observed='Open two-storey shopfront row, pedestrians and hanging signs on the left approach to the large stone bridge.',
 evidence='Study city paragraph beginning 第一段远景 lists the trades around Huai-Xu Bridge. The bridge, wall and market row establish the area; trade names are regional context rather than labels for each selected facade.',
 guard='No literal sign reading or individual shop-to-trade assignment. Distinct from existing dye shop #08 (x17550..17820) and existing general advertising story #10.',sources=[S],zoom='550 x 260 detail reaches native bottom edge. Use upper street facades as marker target; responsive frame must bias upward. Context includes bridge approach without replacing artwork.'),
 dict(id='F',title='A Pagoda Above the Rooftops',decision='accepted',box=[15700,15,16780,340],detail=[16480,20,16680,190],context=[15500,0,17000,600],anchor=[16590,100],visual='High',historical='Medium',
 text="A tower makes a useful landmark in a sea of rooftops. Researchers identify this distant pairing as Panmen's city gate and Ruiguang Pagoda. Follow the wall to see how the tower sits behind it. They share the skyline, but the pagoda isn't part of the defensive wall.",
 observed='Narrow tiered tower behind crenellated city wall, with gate precinct visible to its left in wider context.',
 evidence='Study first city paragraph identifies the distant gate and tower as Panmen and Ruiguang. Relative order before Xumen matches the painting route; no coordinates copied from another scan.',
 guard='Neither Tiger Hill nor Baoen tower. No construction age, floor count, original survival claim, or pagoda-as-defensive-structure claim.',sources=[S],zoom='Tower detail is only 200 x 170. Wide 1080 x 325 scene is needed for landmark pairing; tower alone must not be zoomed to fill screen. Anchor y100 requires upper-edge framing.'),
 dict(id='G',title='Where the Boats Met the Street',decision='revised',box=[14600,360,15370,780],context=[14000,180,15500,1010],anchor=[15200,600],visual='High',historical='Medium',
 text="A river journey still needed a way ashore. Researchers identify this busy landing beside the city wall as Xumen wharf. Stone embankments and steps connect the water to the crowded shore, with boats gathered alongside. Here, Suzhou's water traffic met its streets. Quite a change of pace!",
 observed='Stone quay, descending stairs, densely gathered figures and moored boats under the wall; gate context visible to left.',
 evidence='Study second city paragraph identifies Xumen wharf through the open landing outside the gate, raised stone embankment and steps, with warehouses and boat businesses nearby.',
 guard='No ceremony/event identification, cargo, occupational identities, loading action or specific warehouse use inferred for an individual roof.',sources=[S],zoom='770 x 420 focus; crowded detail is readable as a group. Context is 1500 px wide and should be shown smaller; steps at marker remain principal visual target.'),
 dict(id='H',title='Flags Mean Official Business',decision='revised',box=[10480,370,10980,790],context=[10100,100,11200,900],anchor=[10700,600],visual='High',historical='Medium',
 text="Two tall flagpoles, a screened entrance, and gates arranged in sequence. Researchers identify this as the provincial administration compound. Its fenced forecourt separates official space from the surrounding streets. Same city, different kind of business: the architecture itself tells you this is no ordinary shop.",
 observed='Paired poles and yellow flags above fenced forecourt, screen, gatehouse and sequence of halls behind.',
 evidence='Study third city paragraph identifies Jiangsu provincial administration (布政使司) through paired poles, wooden fences, screen and axial halls opposite the temple precinct. Distinct from the Xumen examination precinct farther right.',
 guard='Use attributed provincial administration label. Do not read tiny flag text or name officials, ceremonies, examination activity or actual government functions taking place.',sources=[S],zoom='500 x 420 scene; paired poles and fence remain visible at native scale. Wider context necessary for axial compound; avoid selecting crowded street to right as focus.'),
 dict(id='J',title='Room for Boats, Too',decision='revised',box=[3780,410,4160,850],context=[3500,200,4500,1010],anchor=[3970,570],visual='High',historical='High',
 text="Up and over for people; room underneath for boats. This arched bridge belongs to the Shantang stretch of the scroll. Research on the painting explains how raised bridge openings accommodated water traffic while linking the banks. Two routes crossing in one small space. Nicely done, bridge builders.",
 observed='Large single arched bridge crossing the canal with people on steps and a boat adjacent to the opening.',
 evidence='Bridge study p50 on raised arches and navigation, p51 on Shantang bridges; museum route places Shantang between Changmen and Tiger Hill. Exact individual bridge name left unresolved.',
 guard='Replaced Three Bridges, One Canal title; no claim that three bridges appear in this crop or this one has a proven historical name. Does not reuse bridge inside existing #12 box.',sources=[B,'https://www.shanghaimuseum.net/mu/frontend/pg/m/article/id/CI00005093'],zoom='380 x 440 detail. At native scale the arched opening is clear; retain the boat and banks in context. 1255 native px from existing #12 center; story covers arch function rather than parallel streets.'),
]
(P/'crops').mkdir(exist_ok=True)
for d in data:
 d['detail']=d.get('detail',d['box'])
 for key in ['box','detail','context']:
  x0,y0,x1,y1=d[key];assert 0<=x0<x1<=W and 0<=y0<y1<=H
  d[key+'_normalized_xywh']=[round(v,8) for v in [x0/W,y0/H,(x1-x0)/W,(y1-y0)/H]]
 d['anchor_normalized']=[round(d['anchor'][0]/W,8),round(d['anchor'][1]/H,8)]
 d['word_count']=len(d['text'].split());assert 30<=d['word_count']<=55,(d['id'],d['word_count'])
 for key in ['context','detail']:
  im.crop(d[key]).save(P/'crops'/f"{d['id']}-{key}.png",optimize=True)
 d['status']='recommended_for_user_review_not_approved_for_implementation'
# Rejected evidence is deliberately not a proposed anchor.
reject=dict(id='I',title='A School with a Purpose',decision='rejected_pending_unique_match',visual='Low',historical='Medium',anchor=None,
 context=[3500,200,6100,1010],detail=[4130,620,4900,1010],
 reason='A Shantang charitable school is documented, but multiple three-bay rooms/courtyards fit loosely. The native master does not permit a unique room/sign match to the description. Do not attach the school story to a generic house.',
 sources=[S,'https://yangtze.silkroadinfo.org.cn/2016/8/8/200810271747829.pdf'])
for k in ['context','detail']:im.crop(reject[k]).save(P/'crops'/f'I-REJECTED-search-{k}.png',optimize=True)
existing=json.loads((P.parents[1]/'src/paintings/gusu/anchors.json').read_text())
for i,d in enumerate(existing,1):d.update(label=f'{i:02}',kind='existing',anchor=[(d['box'][0]+d['box'][2])/2,(d['box'][1]+d['box'][3])/2])
route=sorted(existing+[dict(d,kind='new',label=d['id']) for d in data],key=lambda d:-d['anchor'][0])
for i,d in enumerate(route,1):d['provisional_route_order']=i
for d in data:d['provisional_route_order']=next(x['provisional_route_order'] for x in route if x['label']==d['id'])
register=dict(review_date='2026-10-27',master=str(MASTER),master_sha256=hashlib.sha256(MASTER.read_bytes()).hexdigest(),width=W,height=H,coordinate_convention='Top-left origin; half-open [x0,y0,x1,y1] original pixels. Story order descending anchor x. box=scene, detail=tight evidence, context=surroundings; none is a final camera instruction.',existing_13_unchanged=existing,new_candidates=data,rejected=[reject],route=[{k:d[k] for k in ['label','kind','title','anchor','provisional_route_order']} for d in route])
(P/'proposed-hotspots.json').write_text(json.dumps(register,ensure_ascii=False,indent=2))
with (P/'proposed-hotspots.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['candidate','route_order','title','scene_box','detail_box','context_box','anchor','scene_normalized_xywh','visual','historical','decision'])
 for d in data:w.writerow([d['id'],d['provisional_route_order'],d['title'],d['box'],d['detail'],d['context'],d['anchor'],d['box_normalized_xywh'],d['visual'],d['historical'],d['decision']])
# Fonts, artwork is only cropped/downsampled, never reconstructed.
font='/System/Library/Fonts/Supplemental/Arial.ttf'
serif='/System/Library/Fonts/Supplemental/Georgia.ttf'
def F(n,b=False):return ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf' if b else font,n)
def wrap(draw,text,xy,width,font,fill='#283b42',gap=7):
 x,y=xy;words=text.split();line=''
 for word in words:
  if line and draw.textlength(line+' '+word,font=font)>width:
   draw.text((x,y),line,font=font,fill=fill);y+=font.size+gap;line=word
  else:line=(line+' '+word).strip()
 if line:draw.text((x,y),line,font=font,fill=fill);y+=font.size+gap
 return y
paper='#f1ecdf';ink='#283b42';gold='#E7B93E'
# Six sequential strips. Within each strip artwork keeps its actual left/right orientation.
canvas=Image.new('RGB',(1920,2780),paper);draw=ImageDraw.Draw(canvas)
draw.text((55,32),'PROSPEROUS SUZHOU | 13 EXISTING + 9 PROPOSED',font=F(34,True),fill=ink)
draw.text((55,85),'Research review only  /  Follow each strip RIGHT TO LEFT, then continue on the next row',font=F(22),fill=ink)
draw.text((55,120),'Slate: existing 01–13   •   Apricot: new A–H, J   •   I: withheld, no invented anchor',font=F(21),fill=ink)
for row in range(6):
 x1=round(W*(6-row)/6);x0=round(W*(5-row)/6);top=195+row*420;scale=1800/(x1-x0);ih=round(H*scale)
 strip=im.crop((x0,0,x1,H)).resize((1800,ih),Image.Resampling.LANCZOS);canvas.paste(strip,(60,top))
 draw.text((60,top-32),f'{row+1:02}   x {x1:,} → {x0:,}     ← reading direction',font=F(21,True),fill=ink)
 for d in route:
  ax,ay=d['anchor']
  b=d['box'];col=gold if d['kind']=='new' else ink
  if b[0]<x1 and b[2]>x0:
   bx=[60+(max(x0,b[0])-x0)*scale,top+b[1]*scale,60+(min(x1,b[2])-x0)*scale,top+b[3]*scale]
   draw.rectangle(bx,outline=col,width=3)
  if x0<=ax<x1 or (row==0 and ax==W):
   px=60+(ax-x0)*scale;py=top+ay*scale
   draw.ellipse((px-5,py-5,px+5,py+5),fill=col,outline='white',width=1)
   # Route label in alternating lanes, leader line preserves true anchor.
   lane=(d['provisional_route_order']%2);ly=top+ih+9+lane*26
   lw=draw.textlength(d['label'],font=F(18,True))+14
   lx=max(61,min(1850-lw,px-lw/2))
   draw.line((px,py,px,ly),fill=col,width=1)
   draw.rectangle((lx,ly,lx+lw,ly+24),fill=col)
   draw.text((lx+7,ly+1),d['label'],font=F(18,True),fill=ink if d['kind']=='new' else 'white')
canvas.save(P/'updated-master-location-map.jpg',quality=95)
# Contact sheets, three candidates per 2200-wide sheet; detail never enlarged.
for page in range(3):
 sheet=Image.new('RGB',(2200,2260),paper);ds=ImageDraw.Draw(sheet)
 ds.text((45,25),f'NEW DISCOVERIES | NATIVE-MASTER EVIDENCE | {page+1}/3',font=F(31,True),fill=ink)
 ds.text((45,69),'Context on left • native close-up in middle • proposed English copy on right • no artwork restoration',font=F(21),fill=ink)
 for r,d in enumerate(data[page*3:page*3+3]):
  y=125+r*700
  ds.line((40,y-10,2160,y-10),fill='#b9b3a3',width=2)
  ds.text((45,y),f"{d['id']}  {d['title']}  /  route {d['provisional_route_order']:02}",font=F(27,True),fill=ink)
  ds.text((45,y+42),f"{d['decision'].upper()} · visual {d['visual']} / historical {d['historical']} · {d['word_count']} words",font=F(20),fill=ink)
  for key,x,mw,mh in [('context',45,750,460),('detail',830,550,460)]:
   crop=im.crop(d[key]);sc=min(1,mw/crop.width,mh/crop.height);crop=crop.resize((round(crop.width*sc),round(crop.height*sc)),Image.Resampling.LANCZOS)
   sheet.paste(crop,(x,y+105));ds.text((x,y+80),key.upper(),font=F(17,True),fill=ink)
   wrap(ds,str(d[key])+'  px',(x,y+580),mw,F(17))
  yy=wrap(ds,d['text'],(1430,y+105),700,F(25),gap=10)
  wrap(ds,'Guardrail: '+d['guard'],(1430,yy+20),700,F(18),gap=6)
 sheet.save(P/f'contact-sheet-{page+1}.jpg',quality=96)
# Review markdown and a responsive static HTML artifact.
lines=['# 姑苏繁华图新增发现点审核稿','', '建议新增 **9 个**，总计 **22 个**。A–H 与 J 可提交审核；I（义学）暂不采用。所有新增均为待批准建议，未修改应用。','',
 '## 阅读方法','', '场景框、近景框、上下文框和标记点各有用途；JSON 逐一提供原像素和归一化数值。最终相机尚未实施，也未声称通过桌面/手机运行测试。原图像素原样保存在 PNG 裁图中；排版图只缩小、不补画。','',
 '![总位置图](updated-master-location-map.jpg)','', '## 候选取舍','', '|候选|结果|建议新顺序|标题|视觉 / 历史置信度|','|---|---|---:|---|---|']
for d in data:lines.append(f"|{d['id']}|{d['decision']}|{d['provisional_route_order']}|{d['title']}|{d['visual']} / {d['historical']}|")
lines+=['|I|暂不采用|—|A School with a Purpose|Low / Medium|','','历史 Medium 表示建筑/地名采用已发表研究的对应解释，保留 Researchers identify/describe；不是已经独立验证所有历史细节。视觉 High 评价可见形态及场景组合，不代表小字可读。','']
for d in data:
 lines += [f"## {d['id']} · {d['title']}",'',f"**建议路线位置 {d['provisional_route_order']:02} · {d['word_count']} words**",'',d['text'],'',f"![{d['id']} context](crops/{d['id']}-context.png)",'',f"![{d['id']} native close-up](crops/{d['id']}-detail.png)",'',f"- 场景框：`{d['box']}`；近景框：`{d['detail']}`；上下文框：`{d['context']}`。",f"- 标记：`{d['anchor']}`；归一化：`{d['anchor_normalized']}`。",f"- 场景归一化 xywh：`{d['box_normalized_xywh']}`。",f"- 可见事实：{d['observed']}",f"- 研究对应：{d['evidence']}",f"- 文案边界：{d['guard']}",f"- 清晰度/相机风险：{d['zoom']}",'- 来源：'+ ' · '.join(f'[证据 {i+1}]({s})' for i,s in enumerate(d['sources'])),'']
lines+=['## I · 暂不采用义学','',reject['reason'],'','原生搜索裁图如下，不是已核定的义学坐标；不提供 marker anchor、不把普通民居包装成学校。即使研究描述小门题字，当前母图也不足以作为可读招牌证据。未将北宋范仲淹创办义学的一般历史归到这间未知建筑。','','![I rejected search context](crops/I-REJECTED-search-context.png)','','![I unresolved rooms](crops/I-REJECTED-search-detail.png)','','来源：[景观研究]('+S+')；[范金民研究 PDF（搜索索引可检索正文；直接抓取502，不作为完成视觉核验）]('+reject['sources'][1]+')。','','## 更新后的右至左路线','','|新序号|稳定编号|标题|标记 x,y|','|---:|---|---|---|']
for d in route:lines.append(f"|{d['provisional_route_order']:02}|{'既有' if d['kind']=='existing' else '新增'} {d['label']}|{d['title']}|{d['anchor']}|")
oldgap=sorted([(existing[i]['anchor'][0]-existing[i+1]['anchor'][0],existing[i]['label'],existing[i+1]['label']) for i in range(12)],reverse=True)
gaps=sorted([(route[i]['anchor'][0]-route[i+1]['anchor'][0],route[i]['label'],route[i+1]['label']) for i in range(len(route)-1)],reverse=True)
lines+=['','## 空档、重叠和阅读节奏','',f"原先最大水平中心距：{oldgap[0][1]} → {oldgap[0][2]}，{oldgap[0][0]:g}px；加入候选后最大中心距：{gaps[0][1]} → {gaps[0][2]}，{gaps[0][0]:g}px。以下度量是原生 x 距离，不是浏览器中拖动的时间或像素。",'', '|相邻点|水平标记距离 px|','|---|---:|']
for gap,a,b in gaps[:7]:lines.append(f'|{a} → {b}|{gap:g}|')
lines+=['', '社仓 C 不填补 05→06 空档：其实际位置在园林 #05 之前，并与园林上下分层。05→06 的水面、岸景仍保留。J→13 的树木、寺院及虎丘过渡仍较长；不为补点而把类似民居命名为义学。G→09 仍是最长空档，但主要船运景致可作为留白；可留待下一轮有独立证据的新主题。','',
 'F 与 E 的 x 接近，但相差约815px高程，分别是远景塔/城门与前景店铺。C 与05水平接近但相差470px高程，且场景框不相交。标记在正常尺度不重合；缩到整卷鸟瞰时仍可能挤近，不据此移动原物坐标。只检查研究框：新增场景框与既有13框均无面积交叠；上下文裁图可相交，因为它们提供邻接关系。','',
 f"全路线最小水平标记距为 {min(g[0] for g in gaps):g}px。坐标点没有硬性均匀分布。必须在实施后再检查 22 个导航点的窄屏触控间距、键盘顺序及当前相机的边界限制。",'',
 '## 资料与核验限制','',
 '- 母图：35311 × 1010；SHA-256 `'+register['master_sha256']+'`。Commons 原图尺寸、作者及公共领域说明已在线核对。上海博物馆确认徐扬、1759、辽博收藏；尺寸资料不写入本轮文案。',
 '- 13个现有生产 anchor box 与资料包完全一致。旧提案 JSON 的 proposed 状态是旧记录，不能覆盖现有已实施数据。',
 '- 景观研究是定位解释的主要来源；其网页正文可访问，但图2/3链接抓取失败、图5/7链接404。我们没有把这些失效图当已看过的独立证据，也没有假称多源确认。',
 '- 清史网社仓链接连续超时；改用中国粮食经济学会穆中杰的社仓制度研究支持一般赈济功能。该来源不证明像素坐标。',
 '- 桥文化论文直接可读；只采用拱桥适应船行的论述。文中其他旧统计、尺寸及个别地名不移植到故事。',
 '- 义学研究存在，但唯一建筑识别未过关。I 不以低置信度混入22点建议。',
 '- 原图的拼接色带、柔焦、小字和裁边保持原貌；没有使用其他扫描替换最终裁图。','',
 '## 审批范围','', '本轮只审核9个候选、位置和英文；应用继续维持13点。批准后才进行相机、导航、声音及移动端集成。','']
(P/'REVIEW.md').write_text('\n'.join(lines))
# HTML is independent static review, not part of application.
parts=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Gusu · Expansion review</title><style>body{margin:0;background:#f1ecdf;color:#283b42;font:17px/1.65 Georgia,serif}main{max-width:1460px;margin:auto;padding:32px}h1,h2,h3,.meta{font-family:Arial,sans-serif}h1{font-size:32px}a{color:#315a72}img{max-width:100%;height:auto}article{border-top:1px solid #bbb4a4;padding:26px 0;margin:26px 0}.meta{font-size:14px}.grid{display:grid;grid-template-columns:1.4fr 1fr;gap:30px}figure{margin:12px 0}figure img{display:block;max-height:650px;object-fit:contain;object-position:left}figcaption{font:13px Arial}blockquote{margin:12px 0;font-size:23px;line-height:1.6}summary{cursor:pointer}code{font-size:13px;overflow-wrap:anywhere}@media(max-width:800px){.grid{display:block}main{padding:18px}blockquote{font-size:20px}}@media print{article{break-before:page}details{display:block}}</style><main><h1>Prosperous Suzhou · 9 new discoveries for review</h1><p>建议总数22：保留既有13，新增A–H与J。I义学暂不采用。<strong>Research only; application unchanged.</strong></p><p><a href="REVIEW.md">完整核验与空档分析</a> · <a href="proposed-hotspots.json">精确坐标与证据JSON</a> · <a href="proposed-hotspots.csv">CSV</a></p><p>Gold A–H/J = proposed. Slate 01–13 = existing. Read right to left within each strip.</p><a href="updated-master-location-map.jpg"><img src="updated-master-location-map.jpg" alt="Updated master location map"></a>']
for d in data:
 parts += [f'<article id="{d["id"]}"><h2>{d["id"]} · {html.escape(d["title"])}</h2><p class="meta">ROUTE {d["provisional_route_order"]:02} · {d["decision"].upper()} · Visual {d["visual"]} / historical {d["historical"]} · {d["word_count"]} words</p><div class="grid"><div>',f'<figure><a href="crops/{d["id"]}-context.png"><img src="crops/{d["id"]}-context.png"></a><figcaption>CONTEXT {d["context"]} · click for original crop</figcaption></figure>',f'<figure><a href="crops/{d["id"]}-detail.png"><img src="crops/{d["id"]}-detail.png"></a><figcaption>NATIVE DETAIL {d["detail"]} · no upscaling</figcaption></figure></div><div><blockquote>{html.escape(d["text"])}</blockquote>',f'<p><strong>Observed:</strong> {html.escape(d["observed"])}</p><p><strong>Evidence:</strong> {html.escape(d["evidence"])}</p><p><strong>Guardrail:</strong> {html.escape(d["guard"])}</p><p><strong>Framing:</strong> {html.escape(d["zoom"])}</p>',f'<p class="meta">Scene {d["box"]}<br>Normalized xywh {d["box_normalized_xywh"]}<br>Marker {d["anchor"]} / normalized {d["anchor_normalized"]}</p><p>'+ ' · '.join(f'<a href="{s}">Source {i+1}</a>' for i,s in enumerate(d['sources']))+'</p></div></div></article>']
parts+=['<article><h2>I · A School with a Purpose · WITHHELD</h2><p>'+reject['reason']+'</p><p>Search evidence only; no approved building box or anchor.</p><img src="crops/I-REJECTED-search-context.png"><img src="crops/I-REJECTED-search-detail.png"></article><p>Exact PNG crops contain unchanged decoded master pixels. All colors, controls, existing stories and application assets remain untouched.</p></main></html>']
(P/'REVIEW.html').write_text('\n'.join(parts))
print('Created review, JSON/CSV, 20 evidence crops, six-strip map, 3 contact sheets. Word counts:',[(d['id'],d['word_count']) for d in data]);print('Largest gaps',gaps[:6])
