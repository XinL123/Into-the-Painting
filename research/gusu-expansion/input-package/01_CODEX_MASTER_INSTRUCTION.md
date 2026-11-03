# CODEX MASTER BRIEF — Prosperous Suzhou: Expand Discovery Hotspots

**Current task: research, verify, and propose only. Do NOT implement, edit production code/assets, commit, push, or deploy until I approve the final map and English text.**

## A. Current state / what stays unchanged

- This is the **second Painting Playground work**, *Prosperous Suzhou* (《姑苏繁华图》) by Xu Yang. The existing experience already has **13 live hotspots**.
- Goal: **~21–23 meaningful discoveries total**, by adding **8–10 verified new hotspots**. Ten candidates A–J follow below. If only 8 or 9 pass, stop at 21 or 22; no filler.
- **Keep all original 13** unless a verified factual/location problem is identified; report any proposed changes separately, do not silently change them.
- Retain the existing *Along the River During the Qingming Festival* look and UX: scroll/pan, focus and camera motion, markers, story-card hierarchy, paper/ink styling, controls, accessibility, sounds, and navigation. Keep the **currently implemented marker treatment** in this research pass; do not reopen colors or styling without a specific request.
- Existing file references within the local project may include `playground/painting/research/gusu-proposal/{hotspots.json,STORY_RESEARCH.md,PROJECT_PLAN.md,location-map.jpg,hotspot-contact-sheet.jpg}`. Locate and read the actual files first; path spelling may differ. This pack also includes `existing_13_hotspots_REFERENCE.json` as a read-only copy of the 13 previously supplied anchors. **The current live project files are the source of truth**; report differences.
- Master image: `master-research.jpg`, *exactly* **35,311 × 1,010 px**, coordinates with x increasing left-to-right, while users explore **right-to-left**. Use only this same master for final cropped artwork and coordinates. Different scans may be used for historical identification only, not coordinate transfer.

## B. Why we are doing this

Several stretches of the extremely long painting lack discovery markers. Fill meaningful *content gaps*, especially in areas already described by painting-specific historical research, while preserving visually restful landscape stretches. **Balanced density is a secondary constraint; truth and recognizability always come first.**

Keep final cards about **30–55 English words**, playful and inviting like *Did You Know?*, with an authentic, memorable fact and restrained humor. Avoid invented person identities, conversations, trades, prices, dates, procedures, unreadable sign transcriptions, and certainty where a researcher merely proposes an interpretation.

## C. Six broad visual search zones

These intervals are **approximate horizontal search bands** for candidate exploration, NOT approved bounding boxes or evidence that an object exists at a specific x coordinate.

| Search zone | Master x interval | Candidates | Nearby current route gaps |
|---|---:|---|---|
| 01 Mudu | 27,200–31,300 | A Bridge into Business; B Temple Behind the Shops | Between existing 03 and 04 |
| 02 Waterside granary | 22,000–24,800 | C A Granary with a Backup Plan | Existing 05–06 |
| 03 Stone Lake | 19,100–22,000 | D Farming on the Water's Edge? | Existing 06–07 |
| 04 City / Panmen / Xumen | 11,650–17,900 | E Street for Almost Everything; F Ruiguang Pagoda; G Xumen wharf | **Largest gap**, existing 08–09 |
| 05 Civic administration | 7,800–11,300 | H Flags Mean Official Business | Existing 09–10 |
| 06 Shantang | 1,600–5,000 | I A School with a Purpose; J Three Bridges, One Canal | Existing 12–13 |

The visual pack provides six **low-resolution locator previews** and a contact sheet cut from the previously shared, downsampled overall location map. They are **search guides only, not verified close-ups**. For accurate close-ups run `python3 crop_from_master.py --master /path/to/master-research.jpg` from this pack, then make scene-specific **unaltered** context and detail crops. Do not enlarge blurry images by hallucination, generative restoration, or OCR guesses.

## D. Exact steps (complete in this order)

1. Inspect the current source code/data, 13 existing anchors, and exact master. Record the existing route and the x gaps. Do not overwrite the existing data.
2. For A–J below, find (or fail to find) the precise identifiable object in the exact master. Cross-check painting-specific scholarship and museum/source images to validate historical labels.
3. **Keep only candidates that pass BOTH tests**: (i) visible matching object/scene in the master and (ii) reliable source supporting the claimed historical meaning. Historical evidence from a nearby neighborhood alone does not establish the identity of a chosen building.
4. For each viable new candidate export a **context crop** and a tighter **detail crop**, both from the unchanged master, plus exact `[x0,y0,x1,y1]` pixels, normalized `[x/W,y/H,w/W,h/H]`, visually appropriate marker anchor/center, source URLs and a concise explicit justification.
5. Assign confidence **High / Medium / Low** separately to the *visual identification* and *historical interpretation*. Treat Medium carefully in copy and exclude Low from the final recommendations. Clearly label observed facts vs scholarly interpretations vs contextual general history.
6. Refine all accepted **English story texts**, ~30–55 words each; make them engaging without unsupported assertions. Explain candidate rejections/replacements. Keep the ten proposed texts as editorial starting points, not guaranteed truth.
7. Produce one updated **right-to-left master location map**, plus a labeled **new-hotspots contact sheet with each proposed caption adjacent to its exact crop**. Map should distinguish **existing 13** from **new provisional** markers. Include a route-order table, minimum gaps, candidate overlaps, crop readability, and desktop/mobile potential zoom and edge clipping concerns.
8. **STOP AND WAIT FOR APPROVAL. No implementation in this pass.** Deliver a clear accept/reject/revise table; report if fewer than 8 evidence-grade points are found. The exact total is flexible.

## E. Formal acceptance test

Every new candidate must have all of these:
- actual unaltered **context crop** and **detail crop** from 35,311 × 1,010 source;
- exact original-image box and normalized box;
- clearly visible subject; at a realistic camera scale (not requiring impossible zoom);
- exact evidence URL(s) distinguishing source support from visual observation;
- final 30–55-word English tooltip, title, one useful and defensible takeaway;
- confidence, guardrails, route insertion, and reason for acceptance;
- no undesirable collision/overlap with existing hotspots and no large blank periods filled with an invented point.

If a claim relies on a museum's separate close-up, state that clearly: a tiny inscription cannot be presented as legible in the full master. Similarly, a researched pagoda, school, or granary must be linked to the correct *specific* object, not one that only resembles it.

## F. Source order and caution

- Exact image: https://commons.wikimedia.org/wiki/File:Prosperous_Suzhou.jpg
- Xu Hao, Zhao Jin, Cui Jing, landscape and site study: https://www.zgwypl.com/content/details78_48430.html
- Shanghai Museum catalogue: https://www.shanghaimuseum.net/mu/frontend/pg/m/article/id/CI00005093
- Historical background for community granaries: https://www.qinghistory.cn/c/392/392940.shtml

Use these as research starting points, verify links and relevant passages. **Do not cite a general source as proof of an exact pixel location.**

---

# APPENDIX — Ten targeted scenes and provisional English stories

The following is the editorial candidate brief. All ten are *proposals*, and every scene/location must be verified in the actual master image before it may become a hotspot.

### Candidate A — between existing #03 and #04, Mudu riverside / oblique bridge
**Title:** A Bridge into Business

**Look for:** The distinctive oblique bridge (斜桥) and the cluster of riverside shops around Mudu; do not attach this story to an arbitrary bridge.

**Draft tooltip:**
> A bridge, a river, and shops lining the waterfront: welcome to Mudu. Researchers describe the area around its oblique bridge as a busy commercial district. In this town, a trip across the water could also lead you straight into the market. Convenient, isn't it?

**Fact guardrail:** Bridge/shops and commercial identity supported by the landscape study; show actual storefronts or the bridge in the focus. Avoid claiming who owns a shop or what's being sold without supporting evidence.

### Candidate B — between existing #03 and #04, temple behind shops near Mudu
**Title:** A Temple Behind the Shops?

**Look for:** The documented temple compound behind Mudu waterfront shops, with a distinctive multi-sided, two-storey pavilion. It may fall near existing #04; only use if it fills a genuine gap and is clearly separable from the wedding scene.

**Draft tooltip:**
> The riverfront may look like one long shopping street, but there's more behind the rooftops. Researchers identify a temple complex tucked behind Mudu's shops, including a two-storey, six-sided pavilion. A busy market in front, a quieter courtyard behind: two very different sides of town.

**Fact guardrail:** Scholarly identification; write "researchers identify," not a definite temple name, deity, denomination, or specific ritual. Reject if the pavilion cannot be matched.

### Candidate C — between existing #05 and #06, waterside community granary
**Title:** A Granary with a Backup Plan

**Look for:** The rectangular waterside storehouse complex identified by researchers as a 社仓 (community granary). Avoid relying on tiny unreadable wall writing as the hotspot target.

**Draft tooltip:**
> Not every important building was a shop or a mansion. Researchers identify this waterside compound as a *shecang*, a community granary. Such granaries stored grain that could help local people through shortages or poor harvests. A rather practical way to prepare for a rainy day.

**Fact guardrail:** Verify the *building*, not invented readable characters. Distinguish this historical granary's purpose from claims about how this particular one actually operated.

### Candidate D — between existing #06 and #07, fields and fishponds around Stone Lake
**Title:** Farming on the Water's Edge?

**Look for:** Clearly visible plots of reclaimed/cultivated land or fishpond divisions around Stone Lake, not just undifferentiated open water.

**Draft tooltip:**
> At first glance, it's all water and distant hills. Look again: the landscape study describes cultivated plots and fishponds around Stone Lake. People were making room for both crops and fish. Even the quietest stretch of this scroll has someone hard at work.

**Fact guardrail:** The study verifies field/fishpond features in the broader Stone Lake scene, but Codex must match a distinctive feature in this *exact crop*. No fish species, acreage, farming techniques, or workers should be invented.

### Candidate E — between existing #08 and #09, shopping street near Huai-Xu Bridge
**Title:** A Street for Almost Everything

**Look for:** A distinct row of busy shops near 怀胥桥 (Huai-Xu Bridge) that is different from the currently selected dye-workshop hotspot.

**Draft tooltip:**
> Think Suzhou's markets were just about silk? Think again. Researchers identify rice merchants, shoe shops, wine sellers, and other businesses along the streets near Huai-Xu Bridge. The painting gives us a glimpse of a city where everyday errands could turn into quite a shopping trip.

**Fact guardrail:** These trade types are documented for the *area*, not necessarily legible on one selected storefront. Do not label any specific shop unless its trade/sign is independently matched. Avoid overlap with the original #08 dye story or #10 general-sign story.

### Candidate F — between existing #08 and #09, Panmen & Ruiguang Pagoda
**Title:** A Pagoda Above the Rooftops

**Look for:** The Panmen city-wall/gate landmark with 瑞光寺塔 (Ruiguang Pagoda) rising behind it; use the correct pagoda, not the Tiger Hill tower or Bao'en pagoda near Changmen.

**Draft tooltip:**
> Can you spot the tower rising above Suzhou's city walls? Researchers identify this stretch as the Panmen area, with Ruiguang Pagoda in the background. The painting isn't just showing a skyline—it helps us trace the city's landmarks as the scroll moves toward its busiest streets.

**Fact guardrail:** No age, floor count, reconstruction story, or claim that the pagoda was part of the defensive wall. The *landmark pairing* must be confirmed in the master.

### Candidate G — between existing #08 and #09, Xumen wharf
**Title:** Where Did All the Boats Go?

**Look for:** The Xumen waterfront landing, steps, moored boats, adjacent warehouses and/or transport businesses. Distinguish Xumen from other quays.

**Draft tooltip:**
> All those boats needed somewhere to stop. At Xumen, researchers identify a busy wharf, with stone embankments, steps down to the water, and boats gathering beside the city wall. It was a place where river traffic met the streets. Imagine the loading and unloading!

**Fact guardrail:** Do not identify a particular cargo, passenger, or person as a merchant unless visibly or independently verified. Avoid interpreting official ceremonies as certain.

### Candidate H — between existing #09 and #10, government administrative complex
**Title:** Flags Mean Official Business

**Look for:** The formal Jiangsu provincial administration compound described in the study—gates, screens/fences, and paired flagpoles. Ensure this is a separate landmark from Changmen.

**Draft tooltip:**
> Shops weren't the only busy places in Suzhou. Behind these formal gates was an administrative compound that researchers identify as the Jiangsu provincial administration office. Flags, courtyards, and carefully arranged entrances marked a very different kind of workplace. Not exactly your neighborhood market!

**Fact guardrail:** Do not transcribe small text on flags from this master if illegible. Do not call an unseen historical official by name. If this compound cannot be pinpointed, investigate the documented examination precinct as a substitute without claiming to read the tiny “状元糕” sign.

### Candidate I — between existing #12 and #13, Shantang charitable school
**Title:** A School with a Purpose

**Look for:** The specific simple three-bay charity-school building (义学) described on Shantang street, NOT the existing village school in #01. Make sure the building can be uniquely identified.

**Draft tooltip:**
> Remember the little village school near the start of the scroll? Here's another side of education. Researchers identify a *yixue*, or charitable school, near Shantang Street. Such schools were intended to make learning possible for children from poorer families. A small building with a big idea.

**Fact guardrail:** Do not claim every child could attend for free or that a named historical founder personally built this particular structure. If identification is not visually convincing, substitute a distinct verified waterside trade or architectural scene.

### Candidate J — between existing #12 and #13, Shantang canal bridges
**Title:** Three Bridges, One Canal

**Look for:** A visually unmistakable arched bridge along Shantang River, separate from the existing river-and-road hotspot #12. Source identifies Shantang Bridge, Bantang Bridge, and Puji Bridge along this stretch.

**Draft tooltip:**
> One canal, several ways across. A landscape study identifies three arched bridges along the Shantang River: Shantang, Bantang, and Puji. Boats passed beneath while people crossed overhead. The bridges connected more than two banks—they helped keep a very busy neighborhood moving.

**Fact guardrail:** Do not claim all three bridges appear inside the selected small crop or name which bridge is visible without confidently matching that specific structure.

## Source register (not all sources verify precise anchor locations)
- Primary landmark and scene research: https://www.zgwypl.com/content/details78_48430.html
- Museum catalog / scroll route: https://www.shanghaimuseum.net/mu/frontend/pg/m/article/id/CI00005093
- Community granary definition in Qing sources: https://www.qinghistory.cn/c/392/392940.shtml
- Historical discussion of granary types: https://www.chinagrain.org.cn/luntan/ff808081978ec6f90197ed4d669c0b30.html
- Public-domain original master image: https://commons.wikimedia.org/wiki/File:Prosperous_Suzhou.jpg


---

**END OF BRIEF — Do not implement until user approval.**
