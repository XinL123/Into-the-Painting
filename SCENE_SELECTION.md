# Scene selection — 清明上河图 (Song original, Zhang Zeduan)

## How the scroll was inspected

I viewed the Song original section by section in the browser (Wikimedia Commons copies of the Palace
Museum scroll, 1800 px tall), zooming into each area. Nothing was saved into the project. The scroll
reads right to left:

```
 LEFT (end)                                                                      RIGHT (start)
┌──────────────┬───────────────┬──────────────────────────┬─────────────────┬───────────────┐
│ city streets │  city gate    │   RAINBOW BRIDGE  虹桥    │  wharf, moored  │ rural         │
│ shops, wells │  camels       │   boat in trouble         │  grain boats,   │ outskirts,    │
│ clinic       │  tower        │   crowd, stalls, 脚店     │  willows        │ donkeys, mist │
└──────────────┴───────────────┴──────────────────────────┴─────────────────┴───────────────┘
        D                              A        B                   C
```

What makes a section suitable for 2.5D here:

- The painter's high oblique viewpoint means **near = low in the frame, far = high**. A section whose
  content falls into clear horizontal-ish bands separates into layers naturally.
- **Open water or bare silk behind a foreground form** makes separation cheap: when the foreground
  shifts, what is revealed is plain silk tone, easy to fill honestly.
- **Crowds are fine if they stay baked into one layer.** They become a problem only if figures straddle
  layer boundaries.

---

## Candidate A — The Rainbow Bridge and the boat (虹桥)

The frame runs from the near (left) abutment of the bridge, across the arch and the boat fighting the
current beneath it, to the great willow on the near bank at the right.

```
┌──────────────────────────────────────────────────────────────────────────┐
│ far bank: houses, moored boats, small trees                      (L0)    │
│      ╭───────── bridge arch + crowd ─────────╮      ~~ river ~~  (L2)    │
│  street│                     ⛵ boat, lowering mast, crew        (L1)    │
│  stalls│         ~~~~~~ open water ~~~~~~              ❦ willow  (L4)    │
│ ▟▀▀▀▀▀▙  rooftops along the bottom edge  ▟▀▀▀▀▙ ▟▀▀▀▀▙            (L3)    │
└──────────────────────────────────────────────────────────────────────────┘
```

- **Visually strong:** the single most recognisable passage of the scroll and its dramatic centre; the
  arch gives a large clear shape; the boat gives the scene a story (mast coming down, crew shouting,
  onlookers leaning over the rail).
- **Feasible:** a band of dark rooftops runs along the bottom edge as a ready-made foreground; the far
  bank is a ready-made background; the middle is mostly open water. Full scroll height is used, so we
  get every available pixel (about 4,000 × 1,800 px from the best open source).
- **Depth layers (5):** L0 far bank · L1 river surface + boat · L2 bridge with its crowd and the
  left-bank street · L3 foreground rooftops · L4 front-most willow crown.
- **Motion:** slow water shimmer on the river; the boat rocking and drifting a few pixels; willow twigs
  swaying. Optional later: the hanging banner by the 彩楼 scaffold.
- **Difficulty: medium–high.**
  - The bridge spans from the near bank to the far bank, so it crosses depth. As one flat layer it is a
    compromise; it needs a soft depth gradient (near end closer than far end) rather than a single depth.
  - The bridge and the left-bank street are dense with figures; the mask edge along the bridge rail
    must be clean.
  - River behind the bridge and boat needs a small amount of fill where parallax reveals it.

## Candidate B — The river bend and the great willow (just right of the bridge)

Foreground rooftops and one large old willow silhouetted against open water; a boat with eight men on
a long sweep oar mid-river; a small covered boat at the near bank; far bank with a moored barge.

- **Visually strong:** calm, very "ink" in feeling; the willow against empty water is beautiful. Less
  iconic than the bridge; a viewer may not recognise it as *the* Qingming scroll.
- **Feasible:** the easiest of the three. Almost everything in front sits on plain water, so cut-outs
  and fills are simple. Few figures.
- **Depth layers (4):** far bank · river + sweep-oar boat · near bank, roofs and small boat · willow.
- **Motion:** water, willow twigs, the oar boat drifting. All gentle and easy.
- **Difficulty: low–medium.** Main work is a fine mask for the willow's twigs.

## Candidate C — The wharf with moored grain boats (further right)

Large cargo boats tied along the bank, shops and porters behind, wide open water in front.

- **Visually strong:** superb boat drawing; quiet working-harbour mood.
- **Feasible:** yes, but depth is shallow: there is no real foreground (the bottom of the frame is
  empty water), so the scene would feel like two layers, boats and bank.
- **Depth layers (3):** bank and buildings · boats · water.
- **Motion:** water, mooring ropes, boats bobbing.
- **Difficulty: low,** but the payoff is the weakest "stepping in" effect.

## (Considered and set aside) D — City gate and camel caravan

Strong architecture, but no water and almost no natural motion; the gate tower's own perspective makes
flat layers look wrong quickly. Better kept for a later version.

---

## Recommendation: Candidate A, framed wide enough to include B's willow

Build **the Rainbow Bridge and the boat**, with the frame extended to the right so that it ends on the
great willow. This is one scene, one crop:

- It is the image people think of when they hear 清明上河图, so the pilot immediately reads as this
  painting and not as a generic ink scene.
- It has all five depth bands and three natural, quiet motion sources.
- The wide frame (about 2.2 : 1) is wider than a screen, which is exactly what makes the "look
  left / look right" interaction meaningful: bridge on one side, willow and open river on the other.
- The willow end is the easy part and gives the scene a calm side to balance the busy bridge.

The cost is the bridge mask and its depth gradient. To keep that risk contained, the build order in
[TASKS.md](TASKS.md) does the easy layers first (rooftops, willow, far bank) so the scene already has
depth before the bridge is separated; if the bridge separation turns out badly, it can stay attached
to the river layer and the scene still works.

**Fallback:** if the bridge proves too costly, narrow the same crop to Candidate B. No new source,
no new pipeline, only a different crop rectangle.

Exact crop coordinates are fixed in Phase 0 once the master image is approved (approximately the
central third of the scroll, full height).
