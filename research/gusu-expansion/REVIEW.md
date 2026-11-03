# 姑苏繁华图新增发现点审核稿

建议新增 **9 个**，总计 **22 个**。A–H 与 J 可提交审核；I（义学）暂不采用。所有新增均为待批准建议，未修改应用。

## 阅读方法

场景框、近景框、上下文框和标记点各有用途；JSON 逐一提供原像素和归一化数值。最终相机尚未实施，也未声称通过桌面/手机运行测试。原图像素原样保存在 PNG 裁图中；排版图只缩小、不补画。

![总位置图](updated-master-location-map.jpg)

## 候选取舍

|候选|结果|建议新顺序|标题|视觉 / 历史置信度|
|---|---|---:|---|---|
|A|revised|4|A Bridge into Business|High / Medium|
|B|revised|5|A Temple Behind the Shops?|High / Medium|
|C|revised|7|A Granary with a Backup Plan|High / Medium|
|D|revised|10|Farming at the Water's Edge|High / Medium|
|E|revised|14|A Street for Almost Everything|High / Medium|
|F|accepted|13|A Pagoda Above the Rooftops|High / Medium|
|G|revised|15|Where the Boats Met the Street|High / Medium|
|H|revised|17|Flags Mean Official Business|High / Medium|
|J|revised|21|Room for Boats, Too|High / High|
|I|暂不采用|—|A School with a Purpose|Low / Medium|

历史 Medium 表示建筑/地名采用已发表研究的对应解释，保留 Researchers identify/describe；不是已经独立验证所有历史细节。视觉 High 评价可见形态及场景组合，不代表小字可读。

## A · A Bridge into Business

**建议路线位置 04 · 44 words**

A bridge, a river, and shops almost at your feet. Researchers describe this part of Mudu as a busy commercial district. With shopfronts opening toward the waterfront, crossing the river could bring you straight into the market. A handy place to combine two errands!

![A context](crops/A-context.png)

![A native close-up](crops/A-detail.png)

- 场景框：`[29120, 540, 29870, 1000]`；近景框：`[29120, 540, 29870, 1000]`；上下文框：`[28500, 120, 30300, 1010]`。
- 标记：`[29540, 610]`；归一化：`[0.83656651, 0.6039604]`。
- 场景归一化 xywh：`[0.8246722, 0.53465347, 0.02123984, 0.45544554]`。
- 可见事实：High arched bridge beside a continuous waterfront shop row; steps, pedestrians, boats and open shopfronts are visible.
- 研究对应：Study: Mudu paragraph beginning 作者以木渎镇. The same market sequence contains the distinctive pavilion behind the shops and the wedding boats farther left. The commercial district is supported; the precise named bridge is not established independently.
- 文案边界：Removed the specific oblique-bridge identity. No shop trades, ownership, or actual errands assigned to individuals.
- 清晰度/相机风险：750 x 460 scene; bridge remains readable at native scale. Bottom margin only 10 px: retain full source height in context and do not force vertical centering.
- 来源：[证据 1](https://www.zgwypl.com/content/details78_48430.html)

## B · A Temple Behind the Shops?

**建议路线位置 05 · 43 words**

Shopping in front, something quieter behind. See the small, many-sided tower tucked among the roofs? Researchers identify this compound as a temple behind Mudu's waterfront shops. Its pavilion rises above an enclosed courtyard. The busy riverfront has more than one layer to explore.

![B context](crops/B-context.png)

![B native close-up](crops/B-detail.png)

- 场景框：`[28970, 320, 29240, 510]`；近景框：`[28970, 320, 29240, 510]`；上下文框：`[28680, 220, 29600, 740]`。
- 标记：`[29090, 435]`；归一化：`[0.8238226, 0.43069307]`。
- 场景归一化 xywh：`[0.82042423, 0.31683168, 0.00764634, 0.18811881]`。
- 可见事实：Distinct red two-level polygonal pavilion, enclosed court and aligned halls behind the commercial frontage.
- 研究对应：Study: same Mudu paragraph describes a temple behind shops with a two-storey hexagonal pavilion and axial halls. Spatial configuration matches; the six sides and interior statue cannot all be independently resolved here.
- 文案边界：Do not name temple or deity, count six visible sides, identify monks, or claim the courtyard is actually quiet. Quiet is an editorial contrast, not an observed sound.
- 清晰度/相机风险：270 x 190 detail; use 920 x 520 context for camera. Pavilion remains small (~100 native px high); do not enlarge to fill a card-sized viewport.
- 来源：[证据 1](https://www.zgwypl.com/content/details78_48430.html)

## C · A Granary with a Backup Plan

**建议路线位置 07 · 45 words**

Those long roofs had a practical purpose. Researchers identify this waterside compound as a shecang, or community granary. Such granaries held grain to help communities withstand shortages. The rows of storehouses make a useful counterpoint to all those shops: prosperity needed a backup plan, too.

![C context](crops/C-context.png)

![C native close-up](crops/C-detail.png)

- 场景框：`[24650, 40, 25650, 460]`；近景框：`[24650, 40, 25650, 460]`；上下文框：`[24300, 0, 25900, 800]`。
- 标记：`[25200, 280]`；归一化：`[0.71365863, 0.27722772]`。
- 场景归一化 xywh：`[0.69808275, 0.03960396, 0.02831979, 0.41584158]`。
- 可见事实：Rectangular stone platform surrounded by water, four repeated roof rows, enclosed yard and long rear buildings.
- 研究对应：Study: paragraph beginning 在湖对岸 describes the square community granary, stone base and four warehouse rows. Grain Economics Society research supports the general relief function, not documented transactions at this building.
- 文案边界：Actual compound lies beyond the pack C band. Place BEFORE existing garden #05, not between #05 and #06. No wall-warning transcription, loans, precise management system, or contents claimed visible.
- 清晰度/相机风险：1000 x 420 scene. Garden #05 is below and left; marker chosen on upper storehouse block. Green reproduction seam remains intact. Context touches top boundary; avoid cropping warehouse roofs.
- 来源：[证据 1](https://www.zgwypl.com/content/details78_48430.html) · [证据 2](https://www.chinagrain.org.cn/luntan/ff808081978ec6f90197ed4d669c0b30.html)

## D · Farming at the Water's Edge

**建议路线位置 10 · 46 words**

Not quite an empty lake! Low banks divide this waterside landscape into plots. Researchers describe fields and fishponds around Stone Lake, where people adapted the watery surroundings for food production. The shoreline was a working landscape as well as a scenic one. Look between the banks.

![D context](crops/D-context.png)

![D native close-up](crops/D-detail.png)

- 场景框：`[20200, 350, 20980, 710]`；近景框：`[20200, 350, 20980, 710]`；上下文框：`[19800, 180, 21500, 850]`。
- 标记：`[20700, 590]`；归一化：`[0.58621959, 0.58415842]`。
- 场景归一化 xywh：`[0.5720597, 0.34653465, 0.02208943, 0.35643564]`。
- 可见事实：Repeated low embankments enclose small plots and water areas; cultivated-looking strips differ from open lake beyond.
- 研究对应：Study Stone Lake paragraph explicitly identifies fields opened in water and enclosed fishponds. The crop shows the bank-divided landscape in that same lake sequence; it does not establish which individual enclosure held fish.
- 文案边界：No fish species, exact plot use, technique, acreage or invented worker activity. Revised away from the draft assertion someone is hard at work in this crop.
- 清晰度/相机风险：780 x 360 detail; relief is subtle. Context needed to distinguish plots from open lake. No extra sharpness processing or claim to see fish.
- 来源：[证据 1](https://www.zgwypl.com/content/details78_48430.html)

## E · A Street for Almost Everything

**建议路线位置 14 · 47 words**

Silk wasn't the whole shopping list. Researchers describe rice merchants, shoe shops, wine sellers, and other businesses near Huai-Xu Bridge. This waterfront row belongs to that bustling market area. We're not decoding every tiny sign here, but the takeaway is clear: everyday shopping had plenty of variety.

![E context](crops/E-context.png)

![E native close-up](crops/E-detail.png)

- 场景框：`[16200, 750, 16750, 1010]`；近景框：`[16200, 750, 16750, 1010]`；上下文框：`[15900, 500, 17400, 1010]`。
- 标记：`[16430, 915]`；归一化：`[0.4652941, 0.90594059]`。
- 场景归一化 xywh：`[0.45878055, 0.74257426, 0.01557588, 0.25742574]`。
- 可见事实：Open two-storey shopfront row, pedestrians and hanging signs on the left approach to the large stone bridge.
- 研究对应：Study city paragraph beginning 第一段远景 lists the trades around Huai-Xu Bridge. The bridge, wall and market row establish the area; trade names are regional context rather than labels for each selected facade.
- 文案边界：No literal sign reading or individual shop-to-trade assignment. Distinct from existing dye shop #08 (x17550..17820) and existing general advertising story #10.
- 清晰度/相机风险：550 x 260 detail reaches native bottom edge. Use upper street facades as marker target; responsive frame must bias upward. Context includes bridge approach without replacing artwork.
- 来源：[证据 1](https://www.zgwypl.com/content/details78_48430.html)

## F · A Pagoda Above the Rooftops

**建议路线位置 13 · 47 words**

A tower makes a useful landmark in a sea of rooftops. Researchers identify this distant pairing as Panmen's city gate and Ruiguang Pagoda. Follow the wall to see how the tower sits behind it. They share the skyline, but the pagoda isn't part of the defensive wall.

![F context](crops/F-context.png)

![F native close-up](crops/F-detail.png)

- 场景框：`[15700, 15, 16780, 340]`；近景框：`[16480, 20, 16680, 190]`；上下文框：`[15500, 0, 17000, 600]`。
- 标记：`[16590, 100]`；归一化：`[0.46982527, 0.0990099]`。
- 场景归一化 xywh：`[0.44462066, 0.01485149, 0.03058537, 0.32178218]`。
- 可见事实：Narrow tiered tower behind crenellated city wall, with gate precinct visible to its left in wider context.
- 研究对应：Study first city paragraph identifies the distant gate and tower as Panmen and Ruiguang. Relative order before Xumen matches the painting route; no coordinates copied from another scan.
- 文案边界：Neither Tiger Hill nor Baoen tower. No construction age, floor count, original survival claim, or pagoda-as-defensive-structure claim.
- 清晰度/相机风险：Tower detail is only 200 x 170. Wide 1080 x 325 scene is needed for landmark pairing; tower alone must not be zoomed to fill screen. Anchor y100 requires upper-edge framing.
- 来源：[证据 1](https://www.zgwypl.com/content/details78_48430.html)

## G · Where the Boats Met the Street

**建议路线位置 15 · 47 words**

A river journey still needed a way ashore. Researchers identify this busy landing beside the city wall as Xumen wharf. Stone embankments and steps connect the water to the crowded shore, with boats gathered alongside. Here, Suzhou's water traffic met its streets. Quite a change of pace!

![G context](crops/G-context.png)

![G native close-up](crops/G-detail.png)

- 场景框：`[14600, 360, 15370, 780]`；近景框：`[14600, 360, 15370, 780]`；上下文框：`[14000, 180, 15500, 1010]`。
- 标记：`[15200, 600]`；归一化：`[0.43046076, 0.59405941]`。
- 场景归一化 xywh：`[0.41346889, 0.35643564, 0.02180624, 0.41584158]`。
- 可见事实：Stone quay, descending stairs, densely gathered figures and moored boats under the wall; gate context visible to left.
- 研究对应：Study second city paragraph identifies Xumen wharf through the open landing outside the gate, raised stone embankment and steps, with warehouses and boat businesses nearby.
- 文案边界：No ceremony/event identification, cargo, occupational identities, loading action or specific warehouse use inferred for an individual roof.
- 清晰度/相机风险：770 x 420 focus; crowded detail is readable as a group. Context is 1500 px wide and should be shown smaller; steps at marker remain principal visual target.
- 来源：[证据 1](https://www.zgwypl.com/content/details78_48430.html)

## H · Flags Mean Official Business

**建议路线位置 17 · 45 words**

Two tall flagpoles, a screened entrance, and gates arranged in sequence. Researchers identify this as the provincial administration compound. Its fenced forecourt separates official space from the surrounding streets. Same city, different kind of business: the architecture itself tells you this is no ordinary shop.

![H context](crops/H-context.png)

![H native close-up](crops/H-detail.png)

- 场景框：`[10480, 370, 10980, 790]`；近景框：`[10480, 370, 10980, 790]`；上下文框：`[10100, 100, 11200, 900]`。
- 标记：`[10700, 600]`；归一化：`[0.30302172, 0.59405941]`。
- 场景归一化 xywh：`[0.29679137, 0.36633663, 0.01415989, 0.41584158]`。
- 可见事实：Paired poles and yellow flags above fenced forecourt, screen, gatehouse and sequence of halls behind.
- 研究对应：Study third city paragraph identifies Jiangsu provincial administration (布政使司) through paired poles, wooden fences, screen and axial halls opposite the temple precinct. Distinct from the Xumen examination precinct farther right.
- 文案边界：Use attributed provincial administration label. Do not read tiny flag text or name officials, ceremonies, examination activity or actual government functions taking place.
- 清晰度/相机风险：500 x 420 scene; paired poles and fence remain visible at native scale. Wider context necessary for axial compound; avoid selecting crowded street to right as focus.
- 来源：[证据 1](https://www.zgwypl.com/content/details78_48430.html)

## J · Room for Boats, Too

**建议路线位置 21 · 47 words**

Up and over for people; room underneath for boats. This arched bridge belongs to the Shantang stretch of the scroll. Research on the painting explains how raised bridge openings accommodated water traffic while linking the banks. Two routes crossing in one small space. Nicely done, bridge builders.

![J context](crops/J-context.png)

![J native close-up](crops/J-detail.png)

- 场景框：`[3780, 410, 4160, 850]`；近景框：`[3780, 410, 4160, 850]`；上下文框：`[3500, 200, 4500, 1010]`。
- 标记：`[3970, 570]`；归一化：`[0.11242955, 0.56435644]`。
- 场景归一化 xywh：`[0.10704879, 0.40594059, 0.01076152, 0.43564356]`。
- 可见事实：Large single arched bridge crossing the canal with people on steps and a boat adjacent to the opening.
- 研究对应：Bridge study p50 on raised arches and navigation, p51 on Shantang bridges; museum route places Shantang between Changmen and Tiger Hill. Exact individual bridge name left unresolved.
- 文案边界：Replaced Three Bridges, One Canal title; no claim that three bridges appear in this crop or this one has a proven historical name. Does not reuse bridge inside existing #12 box.
- 清晰度/相机风险：380 x 440 detail. At native scale the arched opening is clear; retain the boat and banks in context. 1255 native px from existing #12 center; story covers arch function rather than parallel streets.
- 来源：[证据 1](https://xuebaosk.ahut.edu.cn/cn/article/pdf/preview/10.3969/j.issn.1671-9247.2021.02.013.pdf) · [证据 2](https://www.shanghaimuseum.net/mu/frontend/pg/m/article/id/CI00005093)

## I · 暂不采用义学

A Shantang charitable school is documented, but multiple three-bay rooms/courtyards fit loosely. The native master does not permit a unique room/sign match to the description. Do not attach the school story to a generic house.

原生搜索裁图如下，不是已核定的义学坐标；不提供 marker anchor、不把普通民居包装成学校。即使研究描述小门题字，当前母图也不足以作为可读招牌证据。未将北宋范仲淹创办义学的一般历史归到这间未知建筑。

![I rejected search context](crops/I-REJECTED-search-context.png)

![I unresolved rooms](crops/I-REJECTED-search-detail.png)

来源：[景观研究](https://www.zgwypl.com/content/details78_48430.html)；[范金民研究 PDF（搜索索引可检索正文；直接抓取502，不作为完成视觉核验）](https://yangtze.silkroadinfo.org.cn/2016/8/8/200810271747829.pdf)。

## 更新后的右至左路线

|新序号|稳定编号|标题|标记 x,y|
|---:|---|---|---|
|01|既有 01|School, Scroll-Style|[33745.0, 862.5]|
|02|既有 02|Cloth Starts at Home|[32820.0, 795.0]|
|03|既有 03|A Mountain Day Out|[31305.0, 870.0]|
|04|新增 A|A Bridge into Business|[29540, 610]|
|05|新增 B|A Temple Behind the Shops?|[29090, 435]|
|06|既有 04|Wedding Traffic, On Water?|[27275.0, 705.0]|
|07|新增 C|A Granary with a Backup Plan|[25200, 280]|
|08|既有 05|A Garden Party, Qing-Style|[24905.0, 750.0]|
|09|既有 06|A Bridge with Nine Arches|[21900.0, 312.5]|
|10|新增 D|Farming at the Water's Edge|[20700, 590]|
|11|既有 07|Showtime in Old Suzhou|[19260.0, 720.0]|
|12|既有 08|A City in Full Color|[17685.0, 835.0]|
|13|新增 F|A Pagoda Above the Rooftops|[16590, 100]|
|14|新增 E|A Street for Almost Everything|[16430, 915]|
|15|新增 G|Where the Boats Met the Street|[15200, 600]|
|16|既有 09|Tea with a Name|[11390.0, 922.5]|
|17|新增 H|Flags Mean Official Business|[10700, 600]|
|18|既有 10|Signs, Signs Everywhere!|[7750.0, 387.5]|
|19|既有 11|A City Gate with a Crowd|[7275.0, 795.0]|
|20|既有 12|A City with Two Kinds of Streets|[5225.0, 610.0]|
|21|新增 J|Room for Boats, Too|[3970, 570]|
|22|既有 13|A Tower at the Finish Line|[725.0, 195.0]|

## 空档、重叠和阅读节奏

原先最大水平中心距：08 → 09，6295px；加入候选后最大中心距：G → 09，3810px。以下度量是原生 x 距离，不是浏览器中拖动的时间或像素。

|相邻点|水平标记距离 px|
|---|---:|
|G → 09|3810|
|J → 13|3245|
|05 → 06|3005|
|H → 10|2950|
|04 → C|2075|
|11 → 12|2050|
|B → 04|1815|

社仓 C 不填补 05→06 空档：其实际位置在园林 #05 之前，并与园林上下分层。05→06 的水面、岸景仍保留。J→13 的树木、寺院及虎丘过渡仍较长；不为补点而把类似民居命名为义学。G→09 仍是最长空档，但主要船运景致可作为留白；可留待下一轮有独立证据的新主题。

F 与 E 的 x 接近，但相差约815px高程，分别是远景塔/城门与前景店铺。C 与05水平接近但相差470px高程，且场景框不相交。标记在正常尺度不重合；缩到整卷鸟瞰时仍可能挤近，不据此移动原物坐标。只检查研究框：新增场景框与既有13框均无面积交叠；上下文裁图可相交，因为它们提供邻接关系。

全路线最小水平标记距为 160px。坐标点没有硬性均匀分布。必须在实施后再检查 22 个导航点的窄屏触控间距、键盘顺序及当前相机的边界限制。

## 资料与核验限制

- 母图：35311 × 1010；SHA-256 `1e56d64df733839ed8f05cb7d067ced84be6ee5b2a489d0440f6c26ef8546a80`。Commons 原图尺寸、作者及公共领域说明已在线核对。上海博物馆确认徐扬、1759、辽博收藏；尺寸资料不写入本轮文案。
- 13个现有生产 anchor box 与资料包完全一致。旧提案 JSON 的 proposed 状态是旧记录，不能覆盖现有已实施数据。
- 景观研究是定位解释的主要来源；其网页正文可访问，但图2/3链接抓取失败、图5/7链接404。我们没有把这些失效图当已看过的独立证据，也没有假称多源确认。
- 清史网社仓链接连续超时；改用中国粮食经济学会穆中杰的社仓制度研究支持一般赈济功能。该来源不证明像素坐标。
- 桥文化论文直接可读；只采用拱桥适应船行的论述。文中其他旧统计、尺寸及个别地名不移植到故事。
- 义学研究存在，但唯一建筑识别未过关。I 不以低置信度混入22点建议。
- 原图的拼接色带、柔焦、小字和裁边保持原貌；没有使用其他扫描替换最终裁图。

## 审批范围

本轮只审核9个候选、位置和英文；应用继续维持13点。批准后才进行相机、导航、声音及移动端集成。

## 当前取景函数的只读几何估算

调用现有 sceneFrame，输入研究场景框，按1440×900、390×844、844×390估算。卡片高度假设280px、最大原生缩放1.25；不是运行时或最终构图验收。27组估算都落在函数给出的图像阅读区域内。

|候选|桌面缩放|手机竖屏缩放|手机横屏缩放|
|---|---:|---:|---:|
|A|0.826|0.447|0.484|
|B|1.250|1.242|1.172|
|C|0.619|0.335|0.363|
|D|0.794|0.430|0.465|
|E|1.126|0.610|0.660|
|F|0.573|0.311|0.336|
|G|0.804|0.436|0.471|
|H|1.238|0.671|0.530|
|J|1.250|0.808|0.506|

瑞光塔的紧裁图仅200×170px；手机配合城门的场景框下，紧裁区域约62×53屏幕像素，能识别塔形，不能阅读建筑小字。E原图贴底，公式估算未越界仍不保证动态卡片布局完全不挡。实施后需以真实文案高度、实际视口和过渡逐项检查。

现有应用标记使用 story.box 的中心。本提案列出独立 anchor，使标记落在明确目标上；如果批准，需在新增数据接入时支持该字段，不能擅自平移原画或既有点。当前仅做记录。

像素校验：18张推荐候选裁图与母图解码后逐像素一致；168个现有应用源码/资产文件与本轮开始时的散列一致。新增框彼此及与既有框无面积交叠。未运行应用集成测试，因为本轮未集成任何新增点。
