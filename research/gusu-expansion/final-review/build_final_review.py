from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageChops
import json,math,csv,html,hashlib,zipfile
P=Path(__file__).resolve().parent
old=json.loads((P.parent/'proposed-hotspots.json').read_text());W,H=old['width'],old['height'];im=Image.open(old['master']).convert('RGB')
S={
'S1':dict(title='Xu Hao, Zhao Jin, Cui Jing — Landscape study (2016; online 2017)',url='https://www.zgwypl.com/content/details78_48430.html',role='Painting-specific scene identifications; paragraphs Mudu, granary, Stone Lake, city segments 1–3.'),
'S2':dict(title='Zhu Xinxin — Bridge culture in Prosperous Suzhou (2021), pp50–52',url='https://xuebaosk.ahut.edu.cn/cn/article/pdf/preview/10.3969/j.issn.1671-9247.2021.02.013.pdf',role='p50 Wannian bridge parapets and p50–51 bridge clearance; no statistics or disputed dimensions reused.'),
'S3':dict(title='Mu Zhongjie — Community granaries (China Grain Economics Society)',url='https://www.chinagrain.org.cn/luntan/ff808081978ec6f90197ed4d669c0b30.html',role='General relief function only; not evidence of this building location or its actual transactions.'),
'S4':dict(title='National Museum of China — 1669 provincial commissioner edict',url='https://www.chnmuseum.cn/zp/zpml/201812/t20181218_24755.shtml',role='Commissioners reported collected/remitted money and grain accounts. Jiangxi edict supports general Qing duties, not identity/activity of Suzhou figures.'),
'S5':dict(title='Suzhou government — Xumen and Wannian Bridge',url='https://english.suzhou.gov.cn/szsenglish/szcmyz/202512/da66785a602b4e6fafd5df357a4c25e3.shtml',role='Wannian outside Xumen and historical bridge construction. No transfer of coordinates from modern photographs.'),
'S6':dict(title='Panmen scenic area — Ruiguang Pagoda',url='https://www.panmen.com.cn/About/1.html',role='Buddhist temple/pagoda association only. Foundation legends, dates and height omitted.'),
}
D={d['id']:dict(d) for d in old['new_candidates'] if d['id']!='E'}
D['B'].update(box=[28850,280,29470,530],detail=[28850,280,29470,590],context=[28680,200,29600,740],
 text="Shopfronts in front, a temple tucked behind! Researchers identify this enclosed compound by its two-storey, many-sided pavilion and aligned halls. The market street wasn't the whole town: religious buildings shared the same crowded waterfront neighborhood. Look past the first row of roofs for a different story.",
 observed='Two visible levels of the red polygonal pavilion, enclosed court, and receding aligned halls behind shops.',
 evidence='S1 Mudu paragraph: temple behind shop row, a two-level polygonal pavilion, an enclosed court, and halls in sequence. All spatial features are matched in the context. Six sides, a statue and two monks are described in the study but cannot be independently resolved here.',
 guard='Temple identity is attributed, not read from an inscription. No temple name, deity, ritual or exact side count.',
 zoom='Native evidence detail 620×310; focus scene 620×250 retains pavilion and halls. Keep surrounding roofs visible for the behind-the-shops relationship.')
D['C'].update(detail=[25000,135,25600,400],evidence='S1 granary paragraph: a rectangular compound on a stone base, four repeated storehouse rows, beside water. Raw context shows the base and water; detail resolves the four foreground roof rows. S3 supplies the general relief function only.',guard='Wall signs are not transcribed. Grain storage function is a scholarly identification; no particular crop, stock amount, lending operation or worker identity is visible.')
D['D'].update(box=[20450,405,21000,685],detail=[20450,405,21000,685],evidence='S1 Stone Lake paragraph: cultivation within the waterscape and enclosed fishponds. Detail shows multiple physically divided enclosures and banks, rather than empty lake. Individual enclosure use cannot be separated confidently into field versus fishpond.',guard='Say fields and fishponds in the Stone Lake landscape; never label a specific selected cell as a fishpond, fish trap, crop species or engineering technique.',zoom='Native 550×280 detail shows bank outlines; keep 1700×670 context to explain the lake setting. Low relief remains subtle without contrast enhancement.')
D['F'].update(detail=[16450,0,16800,285],
 text="City walls and a temple tower share this skyline. Researchers identify them as Panmen and Ruiguang Pagoda. One marked the fortified city edge; the other belonged to a Buddhist temple. Follow the wall, then look up: Suzhou's religious landscape rises just behind its defenses.",
 evidence='S1 first city segment pairs Panmen and Ruiguang Pagoda in the distance, above the near Huai-Xu Bridge scene. Native context shows the gate precinct to the left, wall and tower behind; the sequence precedes Xumen. S6 independently supports the tower’s Buddhist temple association, not the pixel placement.',
 guard='Identification rests on the landmark pairing and scroll sequence, not a readable label. No age, tier count, relics, tilt, or historical construction claim.',zoom='Native tower/wall detail 350×285, no enlargement. The actual tower is narrow. Main 1080×325 scene keeps gate and tower together; on a 390px screen the detail area is about109×89px at the estimated scene scale. Inspect shape, not tiny architectural parts.')
D['H'].update(text="Those flags signal a different kind of business. Researchers identify this compound as the provincial administration office. Qing provincial commissioners had to report money and grain accounts as part of their duties. Prosperity came with paperwork, too. The fenced entrance gives official business a space of its own.",
 evidence='S1 third city segment: paired yellow flags, fenced forecourt, screen opposite the entry hall, and repeated axial halls. These features coincide in the native context/detail. S4 supplies general reporting duties of Qing provincial commissioners; its Jiangxi edict is not an account of this Suzhou scene.',
 guard='No independent reading of tiny flag lettering. No unseen document, named official, ceremony, or work taking place is asserted. Distinguish this compound from the examination precinct nearer Xumen.')
D['E2']=dict(id='E2',title='A Bridge in Two Colors',decision='replacement_for_E',box=[12720,570,13880,1010],detail=[13080,675,13580,920],context=[12250,240,14200,1010],anchor=[13240,775],visual='High',historical='High',
 text="Stone here, red-painted wood there. Researchers identify this as Wannian Bridge outside Xumen, with alternating stone and red wooden railings. Look along the parapet to spot the changing pattern. In this busy waterfront scene, even a river crossing came dressed for the occasion.",
 observed='Large stepped bridge across the moat, pale parapet sections alternating with red lattice sections, roofed pavilions and archway on approaches.',
 evidence='S1 second city segment and S2 p50 describe Wannian Bridge, approach pavilions/archways and alternating stone/red wooden parapets. The native detail resolves that alternating pattern; context fixes the bridge outside the wall beside Xumen. S5 independently confirms Wannian crosses the moat outside Xumen.',
 guard='Material identification attributed to research: pixels alone establish colors/pattern, not wood species. No need to read bridge name, count all openings in this crop, invent a festival, or reuse modern bridge images.',
 zoom='Wide 1160×440 scene reaches original lower edge; native detail 500×245 resolves railings. Context shows relation to quay and wall. Keep upper deck/pavilion visible; lower bridge continues beyond scan edge.')
texts={'A':D['A']['text'],'C':D['C']['text'],'D':D['D']['text'],'G':D['G']['text'],'J':D['J']['text']}
source_ids={'A':['S1'],'B':['S1'],'C':['S1','S3'],'D':['S1'],'F':['S1','S6'],'G':['S1'],'E2':['S1','S2','S5'],'H':['S1','S4'],'J':['S2']}
for d in D.values():
 d['source_ids']=source_ids[d['id']];d['sources']=[S[k]['url'] for k in d['source_ids']]
 d['word_count']=len(d['text'].split());assert 30<=d['word_count']<=55
 d['identification_confidence']='High' if d['id'] in ['E2','J'] else 'Medium'
 d['confidence_explanation']='High visual = real, identifiable structure/feature. Identification confidence assesses its historical label. Medium labels retain explicit research attribution; general history is separately sourced.'
 for key in ['box','detail','context']:
  x0,y0,x1,y1=d[key];d[key+'_normalized_xywh']=[round(v,8) for v in [x0/W,y0/H,(x1-x0)/W,(y1-y0)/H]]
 d['anchor_normalized']=[round(d['anchor'][0]/W,8),round(d['anchor'][1]/H,8)]
 d['status']='final_review_pending_user_approval_no_implementation'
# Existing anchors are copied exactly, never rewritten in production.
existing=old['existing_13_unchanged']
route=sorted([dict(d,label=d['id'],kind='new') for d in D.values()]+existing,key=lambda d:-d['anchor'][0])
for i,d in enumerate(route,1):d['provisional_route_order']=i
new=sorted(D.values(),key=lambda d:-d['anchor'][0])
for d in new:d['provisional_route_order']=next(x['provisional_route_order'] for x in route if x['label']==d['id'])
(P/'crops').mkdir(exist_ok=True)
for d in new:
 for key in ['context','detail']:
  im.crop(d[key]).save(P/'crops'/f'{d["id"]}-{key}.png',optimize=True)
reg=dict(master=old['master'],master_sha256=old['master_sha256'],width=W,height=H,coordinate_convention=old['coordinate_convention'],status='Final research review only; no approval for implementation yet',existing_13_unchanged=existing,new_candidates=new,retired=[dict(id='E',reason='Generic market story overlaps dye and sign themes; replaced with E2 Wannian bridge within G–09.'),dict(id='I',reason='Withheld: documented school has no unique visual match; no coordinates invented.')],sources=S,route=[{k:d[k] for k in ['label','kind','title','anchor','provisional_route_order']} for d in route])
(P/'final-hotspots.json').write_text(json.dumps(reg,ensure_ascii=False,indent=2))
with (P/'final-hotspots.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['id','route','title','scene_box','detail_box','context_box','anchor','scene_normalized_xywh','visual','identification','sources'])
 for d in new:w.writerow([d['id'],d['provisional_route_order'],d['title'],d['box'],d['detail'],d['context'],d['anchor'],d['box_normalized_xywh'],d['visual'],d['identification_confidence'],d['source_ids']])
font='/System/Library/Fonts/Supplemental/Arial.ttf';bold='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
def F(s,b=False):return ImageFont.truetype(bold if b else font,s)
def wrap(draw,t,x,y,width,s=22,fill='#293e45'):
 line='';ft=F(s)
 for word in t.split():
  if line and draw.textlength(line+' '+word,font=ft)>width:draw.text((x,y),line,font=ft,fill=fill);y+=s+8;line=word
  else:line=(line+' '+word).strip()
 if line:draw.text((x,y),line,font=ft,fill=fill);y+=s+8
 return y
paper='#f1ecdf';ink='#293e45';gold='#e7b93e'
# Three complete review sheets; both crops, exact coordinates, copy, citations and scores per row.
for pg in range(3):
 sheet=Image.new('RGB',(2400,2660),paper);dr=ImageDraw.Draw(sheet)
 dr.text((45,25),f'PROSPEROUS SUZHOU | FINAL REVIEW {pg+1}/3 | 13 + 9',font=F(34,True),fill=ink)
 dr.text((45,77),'Research only. Raw PNGs linked in FINAL_REVIEW.html retain exact native pixels. This sheet only downsamples.',font=F(22),fill=ink)
 for row,d in enumerate(new[pg*3:pg*3+3]):
  y=135+row*790;dr.line((40,y-10,2360,y-10),fill='#b9b3a3',width=2)
  dr.text((45,y),f'{d["id"]}  {d["title"]}  |  route {d["provisional_route_order"]:02}',font=F(29,True),fill=ink)
  dr.text((45,y+43),f'{d["word_count"]} words  |  visible feature: {d["visual"]}  |  historical identification: {d["identification_confidence"]}',font=F(21),fill=ink)
  for key,x,mw in [('context',45,800),('detail',885,620)]:
   crop=im.crop(d[key]);scale=min(1,mw/crop.width,470/crop.height);crop=crop.resize((round(crop.width*scale),round(crop.height*scale)),Image.Resampling.LANCZOS)
   sheet.paste(crop,(x,y+110));dr.text((x,y+82),key.upper(),font=F(18,True),fill=ink)
   wrap(dr,f'{key} box {d[key]}',(x),y+600,mw,18)
  yy=wrap(dr,d['text'],1550,y+105,805,26)
  yy=wrap(dr,'Scene '+str(d['box'])+'; marker '+str(d['anchor']),1550,yy+15,805,19)
  yy=wrap(dr,'Sources: '+', '.join(d['source_ids'])+'. '+d['guard'],1550,yy+10,805,19)
  wrap(dr,d['zoom'],1550,yy+7,805,18)
 sy=2525
 for sid in sorted({k for d in new[pg*3:pg*3+3] for k in d['source_ids']}):
  sy=wrap(dr,sid+' '+S[sid]['url'],45,sy,2310,17)
 sheet.save(P/f'final-review-sheet-{pg+1}.jpg',quality=96)
# Dedicated evidence boards for requested five candidates. Raw native close-up placed without resampling.
checks={
'B':('Pavilion and court behind the shops', ['Two visible pavilion levels; polygonal roof/body profile.','Aligned halls extend behind the court; boundary walls enclose it.','Wider crop locates this behind the commercial frontage.'],['Cannot independently count all six sides.','Buddha/statue and monk identities not resolved.','Temple identity remains an attributed scholarly reading.']),
'C':('Four roof rows on the waterside platform',['Four repeated front warehouse roofs are separable.','Wider crop shows rectangular stone base and surrounding water.','Configuration matches the specific granary description.'],['No independent transcription of wall warnings.','Storage purpose comes from the study, not visible grain.','Actual site is before #05, not in #05–06 gap.']),
'D':('Divided banks, not undifferentiated lake water',['Low banks separate multiple small plots/enclosures.','Context places them within the Stone Lake landscape.','S1 documents cultivated areas and fishponds in this scene.'],['Cannot determine each individual enclosure’s use.','No visible fish species, crop type or farming technique.','Identity of this exact cell as a fishpond remains unresolved.']),
'F':('Pagoda behind a crenellated wall',['Native detail resolves tiered tower and intervening wall.','Context includes the gate precinct to the left.','Panmen/Ruiguang pairing fits the city sequence before Xumen.'],['Landmark names are not read from labels.','Tower is small; do not enlarge beyond native cap.','No transfer of location from Tiger Hill or Baoen tower.']),
'H':('Paired flags, screen, fenced forecourt',['Two poles with yellow flags stand by the forecourt.','Fences and a screen articulate entry, with halls beyond.','Combination matches S1 provincial-administration description.'],['Flag text is not independently transcribed.','No named people or visible accounts are asserted.','General commissioner duties use S4, a separate Qing edict.']),
}
for cid,(title,yes,no) in checks.items():
 d=D[cid];board=Image.new('RGB',(1800,1230),paper);dr=ImageDraw.Draw(board)
 dr.text((40,25),cid+' | '+title,font=F(29,True),fill=ink)
 dr.text((40,70),'Native-resolution evidence: close-up at 1 image pixel = 1 board pixel; no enhancement.',font=F(21),fill=ink)
 raw=im.crop(d['detail']);board.paste(raw,(45,140));dr.text((45,110),'UNALTERED NATIVE DETAIL '+str(d['detail']),font=F(18,True),fill=ink)
 y=150
 for label,arr in [('MATCHED IN MASTER',yes),('NOT ESTABLISHED / OMITTED',no)]:
  dr.text((850,y),label,font=F(22,True),fill=ink);y+=40
  for t in arr:y=wrap(dr,'• '+t,850,y,880,22)+7
  y+=18
 context=im.crop(d['context']);context.thumbnail((760,430));board.paste(context,(45,700));dr.text((45,665),'CONTEXT (DOWNSAMPLED); raw PNG supplied separately',font=F(17,True),fill=ink)
 y=wrap(dr,d['evidence'],850,max(700,y),880,21)
 wrap(dr,'Sources: '+', '.join(d['source_ids']),850,y+20,880,19)
 board.save(P/f'{cid}-identification-evidence.jpg',quality=96)
# Updated whole-master map, same native orientation and right-to-left route.
mp=Image.new('RGB',(1920,2780),paper);dr=ImageDraw.Draw(mp)
dr.text((50,25),'FINAL REVIEW | 13 EXISTING + 9 PROPOSED',font=F(36,True),fill=ink)
dr.text((50,80),'E2 replaces old E. I withheld. Slate 01–13: existing; apricot A–H/J with E2: proposed.',font=F(22),fill=ink)
dr.text((50,120),'Each strip reads RIGHT TO LEFT, then next row. Original artwork unchanged.',font=F(22),fill=ink)
for row in range(6):
 x1=round(W*(6-row)/6);x0=round(W*(5-row)/6);top=195+row*420;s=1800/(x1-x0);hh=round(H*s)
 mp.paste(im.crop((x0,0,x1,H)).resize((1800,hh),Image.Resampling.LANCZOS),(60,top))
 dr.text((60,top-32),f'{row+1:02}  x{x1:,} → x{x0:,}   ←',font=F(21,True),fill=ink)
 for d in route:
  b=d['box'];col=gold if d['kind']=='new' else ink;ax,ay=d['anchor']
  if b[0]<x1 and b[2]>x0:dr.rectangle((60+(max(b[0],x0)-x0)*s,top+b[1]*s,60+(min(b[2],x1)-x0)*s,top+b[3]*s),outline=col,width=3)
  if x0<=ax<x1:
   xx=60+(ax-x0)*s;yy=top+ay*s;ly=top+hh+9+(d['provisional_route_order']%2)*27
   lw=dr.textlength(d['label'],font=F(18,True))+14;lx=max(61,min(1850-lw,xx-lw/2))
   dr.ellipse((xx-5,yy-5,xx+5,yy+5),fill=col,outline='white',width=1);dr.line((xx,yy,xx,ly),fill=col)
   dr.rectangle((lx,ly,lx+lw,ly+24),fill=col);dr.text((lx+7,ly+1),d['label'],font=F(18,True),fill=ink if d['kind']=='new' else 'white')
mp.save(P/'final-location-map.jpg',quality=96)
# Full review: claim-level guardrails, gap analysis and exact research geometry.
md=['# 姑苏繁华图 · 最后一轮研究审核','','**建议仍为9个新增，总计22个；未实施。原E商铺主题撤回，以E2万年桥替换。I义学继续暂缓。**','','## 本轮修订结论','',
'- E2 在G与09之间，讲万年桥的红白栏杆与建筑装饰，区别于染坊、招牌和J的通航净空。原E不保留为第十个新增点。',
'- B、C、D、F、H均重新检查原生母图；另附5张证据板，把已匹配形态与未确认信息分开。对这些具体历史身份仍采用研究者归属措辞。',
'- H保持准确位置，不为分布平衡而移动到旁边屋顶。与09主题不同、二维位置可分，不据横向距离单独判定冲突。',
'- 05–06、J–13保留景观过渡；H–10没有找到能同时通过独立识别与新叙事价值的额外目标。','','![最终位置图](final-location-map.jpg)','','## 九段最终英文','','可见形态High不等于历史名称已独立证实。下表和逐项材料另列Identification置信度；Medium标签均保留attributed research。原像素PNG不缩放、不锐化、不修补。排版表中的图片仅缩小。','']
copy=['# Nine final English tooltips — pending approval','']
for d in new:
 md += [f"## {d['id']} · {d['title']}",'',d['text'],'',f"**{d['word_count']} words · 路线{d['provisional_route_order']:02} · 可见形态{d['visual']} / 历史身份{d['identification_confidence']}**",'',f"![Context](crops/{d['id']}-context.png)",'',f"![Native detail](crops/{d['id']}-detail.png)",'',f"- 场景框 `{d['box']}`；近景框 `{d['detail']}`；上下文框 `{d['context']}`。",f"- 精确标记 `{d['anchor']}`；归一化 `{d['anchor_normalized']}`。",f"- 场景归一化xywh `{d['box_normalized_xywh']}`（所有框的归一化数值见JSON）。",f"- 可见：{d['observed']}",f"- 识别论证：{d['evidence']}",f"- 边界：{d['guard']}",f"- 取景限制：{d['zoom']}",'- 来源：'+' · '.join(f'[{sid}: {S[sid]["title"]}]({S[sid]["url"]})' for sid in d['source_ids']),'']
 if d['id'] in checks:md += [f"[额外原生证据板](./{d['id']}-identification-evidence.jpg)",'']
 copy += [f"## {d['id']}. {d['title']}",'',d['text'],'']
(P/'FINAL_ENGLISH.md').write_text('\n'.join(copy))
gaps=[dict(a=route[i]['label'],b=route[i+1]['label'],dx=route[i]['anchor'][0]-route[i+1]['anchor'][0],distance=math.dist(route[i]['anchor'],route[i+1]['anchor'])) for i in range(21)]
md+=['## 空档与聚集的复核','', '|区段|上一版水平中心距|本轮建议|','|---|---:|---|','|G–09|3810px|E2插入后：G→E2=1960px，E2→09=1850px|','|J–13|3245px|保留；寺院、园林与林木过渡，不强填|','|05–06|3005px|保留；水面、岸景及已有园林的外围|','|H–10|2950px|检查过远景建筑，但无足够独特的新增匹配，不强填|','',
'原E与F水平只相距160px（16430与16590）。撤回原E后，F与E2相距3350px，且G位于二者之间。E2没有另造第十点，总数仍为22。',
'现有09标记(11390,922.5)，H标记(10700,600)：水平690px，二维距离约762px。它们一个在贴底茶室、一个在上方衙署入口，场景框不相交。按现有竖屏静态浏览比例0.719，二维间距约548屏幕像素，明显大于12px标记。此为几何说明，不是未经实施的交互验收。',
'本轮最大的剩余水平空档是J→13=3245px；其次05→06=3005px、H→10=2950px。最小水平中心距为C→05=295px，但上下相隔470px；二维约555px。不要通过移动对象坐标制造均匀间隔。','',
'新增场景框与现有13框无面积重叠；新增场景框也互不相交。上下文框可重叠，作为邻接证据。所有距离取真实母图坐标。','',
'## 五项建筑/地貌核验表','','|点|对照研究的形态组合|仍未确认|','|---|---|---|',
'|B|两层多边形亭阁、围院、后方轴线殿宇、前方店铺|六面不可全数，佛像与人物身份不清；不命名寺院|',
'|C|临水石台、矩形围合、四排连续屋顶|不读墙上字、不见储粮实物；用途是研究解释|',
'|D|连续低岸围出的分隔地块，位于石湖水景|不能给每个小格分别确定田或鱼塘|',
'|F|墙后塔身、左侧门区及先于胥门的顺序|名称来自地标组合，不读小字；塔很小|',
'|H|双旗杆、黄旗、栅栏前院、影壁、后方多进屋宇|不抄旗文，不把一般衙署职责当画中可见活动|','',
'## 最终22点路线','','|顺序|稳定编号|标题|标记 x,y|','|---:|---|---|---|']
for d in route:md.append(f"|{d['provisional_route_order']:02}|{'既有' if d['kind']=='existing' else '新增'} {d['label']}|{d['title']}|{d['anchor']}|")
md+=['','## 来源登记与局限','']
for sid,s in S.items():md += [f"- [{sid} · {s['title']}]({s['url']})：{s['role']}"]
md+=['', 'S1的正文已重新在线核对；部分图链接此前失效，故本次不把失效配图当独立核验。所有坐标来自本地35311×1010母图。S4为其他省的清代敕谕，仅支持通用职责；S5、S6支持地标背景，不证明母图中的坐标。','', '本轮未对新点进行浏览器交互测试、相机动画测试或音频集成。只审核场景、证据、英文和坐标。应用的13点和原画均保持不变。','']
(P/'FINAL_REVIEW.md').write_text('\n'.join(md))
# HTML with native PNG links, source links and complete metadata per candidate.
out=['<!doctype html><html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Gusu final review</title><style>body{margin:0;background:#f1ecdf;color:#293e45;font:17px/1.65 Georgia,serif}main{max-width:1500px;margin:auto;padding:30px}h1,h2,.meta{font-family:Arial,sans-serif}img{max-width:100%;height:auto}a{color:#315b72}article{border-top:1px solid #b9b3a3;padding:25px 0}.grid{display:grid;grid-template-columns:1.25fr 1fr;gap:32px}blockquote{font-size:23px;line-height:1.6;margin:0}.meta{font-size:14px}figure{margin:14px 0}figure img{display:block;max-height:680px;object-fit:contain;object-position:left}figcaption{font:13px Arial}code{overflow-wrap:anywhere}@media(max-width:800px){.grid{display:block}main{padding:18px}}</style><main><h1>Final review · 13 existing + 9 proposed</h1><p>E withdrawn; E2 Wannian Bridge replaces it inside G–09. I withheld. Application unchanged.</p><p><a href="FINAL_REVIEW.md">完整研究 / gap and cluster analysis</a> · <a href="FINAL_ENGLISH.md">English only</a> · <a href="final-hotspots.json">Exact coordinates and evidence JSON</a></p><img src="final-location-map.jpg">']
for d in new:
 out += [f'<article><h2>{d["id"]} · {d["title"]}</h2><p class="meta">ROUTE {d["provisional_route_order"]:02} · {d["word_count"]} words · Visible feature {d["visual"]} / identification {d["identification_confidence"]}</p><div class="grid"><div>']
 for key in ['context','detail']:out += [f'<figure><a href="crops/{d["id"]}-{key}.png"><img src="crops/{d["id"]}-{key}.png"></a><figcaption>{key.upper()} {d[key]} · click native PNG</figcaption></figure>']
 out += [f'</div><div><blockquote>{html.escape(d["text"])}</blockquote><p><strong>Observed:</strong> {html.escape(d["observed"])}</p><p><strong>Evidence:</strong> {html.escape(d["evidence"])}</p><p><strong>Not established:</strong> {html.escape(d["guard"])}</p><p><strong>Framing:</strong> {html.escape(d["zoom"])}</p><p>Scene {d["box"]}<br>Marker {d["anchor"]}<br>Normalized scene xywh {d["box_normalized_xywh"]}</p><p>'+' · '.join(f'<a href="{S[k]["url"]}">{k}</a>' for k in d['source_ids'])+'</p>']
 if d['id'] in checks:out += [f'<p><a href="{d["id"]}-identification-evidence.jpg">Native identification evidence board</a></p>']
 out += ['</div></div></article>']
out+=['<h2>Source register</h2>']
for k,s in S.items():out += [f'<p><a href="{s["url"]}">{k}: {s["title"]}</a><br>{s["role"]}</p>']
out += ['<p>Approval pending. No implementation, commit, push or deployment.</p></main></html>']
(P/'FINAL_REVIEW.html').write_text('\n'.join(out))
print('Final stories',[(d['id'],d['word_count']) for d in new]);print('Route',[d['label'] for d in route])
