// Approved master anchors; current discovery order follows master x, left-to-right.
// Research and per-claim boundaries:
// research/gusu-proposal/STORY_RESEARCH.md and FINAL_COPY.md.
// Ambient recordings are modern interpretive sound, never historical evidence.
import anchors from './anchors.json' with { type: 'json' };
import expansion from './expansion.json' with { type: 'json' };
// Screenshot-directed presentation refinements; archival research boxes remain intact.
import focus from './focus.json' with { type: 'json' };

const copy = [
  [
    "A classroom, before we even reach the city!",
    "Researchers identify this little room as a village school. The desks and figures give us a glimpse of education beyond Suzhou’s busy streets. Even a scroll about prosperity makes room for homework."
  ],
  [
    "Beautiful cloth had a quieter beginning: somebody had to make it.",
    "Researchers read this household scene as cotton-cloth production. Look at the workroom and equipment around the courtyard. Behind the shops and colorful fabrics were hours of work much closer to home."
  ],
  [
    "Pine trees, mountain air, and a little time away from town.",
    "Near Lingyan Mountain, visitors gather beneath the trees while attendants prepare food. Some travelers even have a carrying chair nearby. Apparently, a scenic day out could involve both a picnic and a ride!"
  ],
  [
    "Bright decorations and a very crowded boat—could this be a wedding?",
    "Researchers interpret the boats near Mudu as a wedding procession. In a town threaded with waterways, a celebration could travel by river."
  ],
  [
    "A garden, an elegant hall, and plenty of company.",
    "This Mudu residence has planted courtyards, ornamental rocks, and rooms where people gather. Researchers suggest it may be the historic Suichu Garden, though that identification remains uncertain.",
    "Some gardens were made for enjoying company as much as scenery."
  ],
  [
    "Nine arches—and, according to tradition, nine moons.",
    "This is Xingchun Bridge at Stone Lake. On certain autumn nights, people came to see moonlight shine through its arches and reflect on the water, a sight called *Shihu Chuanyue*.",
    "Xu Yang painted the bridge by day, but its famous spectacle belonged to the night."
  ],
  [
    "The crowd has found something more exciting than shopping.",
    "Look at the colorful stage and all the spectators gathered around it. The scene offers a glimpse of live entertainment in Qing-era Suzhou. Long before anyone could stream a show, a performance could draw quite a crowd."
  ],
  [
    "Those colorful lengths of fabric have a story behind them.",
    "Suzhou was a major textile-dyeing center, and a 2026 exhibition report notes four dye works across the entire scroll. Here, bright cloth hangs outside a workshop. The city's colorful fashions didn't dye themselves!"
  ],
  [
    "A museum close-up reveals a tiny sign: *Songluo Tea Room* (松蘿茶室).",
    "Songluo is the name of a celebrated green tea associated with the Huangshan region. Tea drinking was part of Suzhou's social life, and this little sign hints at a much bigger story of taste and trade. Fancy a cup?"
  ],
  [
    "Look at the shop signs lining this busy street near Changmen.",
    "Recent exhibition reporting counts more than 200 business signs across the *whole* scroll—not just this street.",
    "The characters may be too small to read here, but the message is clear: Suzhou's shopkeepers knew how to compete for attention."
  ],
  [
    "A city gate, a bridge, and hardly any room to stand still!",
    "This is Changmen, a major gateway along Xu Yang's painted route through Suzhou. Beyond the defensive walls, boats, shops, and pedestrians crowd together. A city gate could be a landmark—and a lively meeting place."
  ],
  [
    "Why choose between roads and canals when you can have both?",
    "Around Shantang, boats travel beside busy streets, linking shops and landing places in different ways. This side-by-side network of water routes and walkways was a defining feature of Suzhou's urban life. Two kinds of traffic, one bustling neighborhood."
  ],
  [
    "After all those markets, bridges, and boats, the scroll ends on a hill.",
    "This is Tiger Hill, where a pagoda rises above temple buildings. Xu Yang's journey has taken us from countryside to busy city streets and finally to this landmark. Quite a long walk—for your eyes, at least."
  ]
];
// All 22 discoveries have a distinct, scene-specific clip.
// Contemporary illustrative foley, not a reconstruction of Qing-era sound.
const ambience = {
  school: { file: 'gusu-balanced-school-v5', mode: 'once', gain: 0.8 },
  cloth: { file: 'gusu-balanced-cloth-v5', mode: 'once', gain: 0.8 },
  outing: { file: 'gusu-balanced-outing-v5', mode: 'once', gain: 0.8 },
  'mudu-market': { file: 'gusu-balanced-mudu-market-v5', mode: 'once', gain: 0.8 },
  temple: { file: 'gusu-balanced-temple-v5', mode: 'once', gain: 0.8 },
  wedding: { file: 'gusu-balanced-wedding-v5', mode: 'once', gain: 0.8 },
  granary: { file: 'gusu-balanced-granary-v5', mode: 'once', gain: 0.8 },
  garden: { file: 'gusu-balanced-garden-v5', mode: 'once', gain: 0.8 },
  bridge: { file: 'gusu-balanced-bridge-v5', mode: 'once', gain: 0.8 },
  'lake-plots': { file: 'gusu-balanced-lake-plots-v5', mode: 'once', gain: 0.8 },
  theatre: { file: 'gusu-balanced-theatre-v5', mode: 'once', gain: 0.8 },
  dye: { file: 'gusu-balanced-dye-v5', mode: 'once', gain: 0.8 },
  ruiguang: { file: 'gusu-balanced-ruiguang-v5', mode: 'once', gain: 0.8 },
  wharf: { file: 'gusu-balanced-wharf-v5', mode: 'once', gain: 0.8 },
  wannian: { file: 'gusu-balanced-wannian-v5', mode: 'once', gain: 0.8 },
  tea: { file: 'gusu-balanced-tea-v5', mode: 'once', gain: 0.8 },
  administration: { file: 'gusu-balanced-administration-v5', mode: 'once', gain: 0.8 },
  signs: { file: 'gusu-balanced-signs-v5', mode: 'once', gain: 0.8 },
  gate: { file: 'gusu-balanced-gate-v5', mode: 'once', gain: 0.8 },
  canal: { file: 'gusu-balanced-canal-v5', mode: 'once', gain: 0.8 },
  'shantang-arch': { file: 'gusu-balanced-shantang-arch-v5', mode: 'once', gain: 0.8 },
  pagoda: { file: 'gusu-balanced-pagoda-v5', mode: 'once', gain: 0.8 },
};
const originalIds = ["school", "cloth", "outing", "wedding", "garden", "bridge", "theatre", "dye", "tea", "signs", "gate", "canal", "pagoda"];
const originalCopy = Object.fromEntries(originalIds.map((id, i) => [id, copy[i]]));
const sourceUpdates = {
  signs: ['https://paper.people.com.cn/rmrbhwb/pc/content/202608/28/content_30177716.html'],
  tea: ['https://m.jstv.com/news/2026/7/11/1525560875541487616.html', 'https://www.huangshan.gov.cn/zwgk/public/6615714/11213401.html'],
};
// Route-dependent wording is separate from the stable object/research IDs.
const routeText = {
  school: ["A classroom, beyond the busy city!", ...originalCopy.school.slice(1)],
  pagoda: [
    "At one end of the scroll, a pagoda rises above a hill.",
    "This is Tiger Hill, where temple buildings sit among the trees. Xu Yang’s scroll connects this landmark with busy city streets and the countryside beyond. Quite a long walk—for your eyes, at least."
  ],
};
const masterX = (a) => a.anchor?.[0] ?? (a.box[0] + a.box[2]) / 2;
const orderedAnchors = anchors.map(a => ({ ...a, ...focus[a.id] })).sort((a, b) => masterX(a) - masterX(b));
export const stories = orderedAnchors.map(({ nextLabel, ...a }, i) => ({
  ...a,
  title: a.id === 'pagoda' ? 'A Tower Above the Trees' : a.title,
  text: routeText[a.id] ?? originalCopy[a.id] ?? expansion[a.id].text,
  sound: ambience[a.id],
  sources: sourceUpdates[a.id] ?? expansion[a.id]?.sources,
  ...(i === orderedAnchors.length - 1 ? { nextLabel: 'Restart the Journey' } : {}),
}));
