// Approved anchors, numbered left to right across the scroll as it lies on screen:
// 1 is the leftmost discovery, the last is the rightmost (the user's choice, 2026-11-10;
// anchors.json itself is stored right to left, the way a handscroll is read).
// Evidence, sources and per-claim limits: research/han-palace-proposal/STORY_REVIEW.md.
// A Ming painting of an imagined Han palace: the cards describe the picture,
// attribute interpretations, and keep legend labelled as legend.
import anchors from './anchors.json' with { type: 'json' };

const copy = {
  "shelf-mark": [
    "In the bottom corner, beside the red seals, sits one small ink character: 慮.",
    "The museum reads it as collector Xiang Yuanbian's inventory number, counted off from the Thousand Character Classic. Even a painted palace, it seems, needed a shelf mark."
  ],
  "swing": [
    "Before any palace lady appears, a red swing stands empty in the morning mist.",
    "Scholar Xu Wenmei links it to old palace poems, where swings belong to the spring festival season. The scroll announces spring without showing a single person."
  ],
  "rock": [
    "Outside the wall stands a tall grey rock, full of holes and hollows, with pink blossoms growing around it.",
    "Rocks like this were prized in Chinese gardens for their strange shapes. The stranger the stone, the better the view."
  ],
  "gate": [
    "A red gate stands ajar, and behind it roofs, walls and railings run on in perfectly straight lines.",
    "This ruled-line style is called jiehua, and Qiu Ying was a master of it. The palace is imaginary; the geometry is exact."
  ],
  "mandarin-duck": [
    "One small bird perches on the stone railing above the pond, with a red bill and a sweep of orange and white.",
    "The museum's catalogue names mandarin ducks among the painting's birds. Easy to miss; hard to forget once found."
  ],
  "peacocks": [
    "Two peacocks stroll across the courtyard while ladies lean from a window to watch.",
    "Peacocks turn up in old palace poetry, kept for their dazzling feathers; one verse even imagines the plumes sewn into a dance costume."
  ],
  "watering": [
    "Beside the great rock, a woman tips a long-necked vessel over the flowering shrubs.",
    "Others in this courtyard pick blossoms and admire them; she is the one keeping them alive. The museum's catalogue even lists her tool: a flower-watering vessel."
  ],
  "flowers": [
    "A lady reaches up to break off a flowering branch while her attendant waits with a tray.",
    "Flower-viewing is one of the palace pastimes Xu Wenmei traces through the scroll and through the poems behind it. Somebody, of course, has to carry the flowers."
  ],
  "toilette": [
    "Under a leafy tree, a woman lifts both hands to fix her hair before a mirror on a red table.",
    "'Morning adornment' is a favourite scene in palace poetry, and it gives the scroll its mood: spring, dawn, and not quite ready yet."
  ],
  "dance": [
    "Two dancers turn toward each other, long blue sleeves flying, while the musicians play a few steps away.",
    "Music and dance fill the old palace poems, which praised court women for their talents. Here the poem becomes a performance."
  ],
  "ensemble": [
    "Two string instruments, two shapes.",
    "The pear-shaped one held upright is a pipa. The long one on the red stand, with a row of small bridges under its strings, is a zheng. Behind it, a woman seems to be pulling a string tight."
  ],
  "cat": [
    "Above the musicians, on a round stool with a red cushion, something small and fluffy is curled up fast asleep.",
    "A cat? A lapdog? The museum's catalogue lists a cat among this painting's subjects, so that is our best guess. Concert or no concert, it is not getting up."
  ],
  "qin": [
    "Two women slide a long black instrument out of its patterned cloth cover.",
    "It is a qin, the zither of Chinese scholars; the museum notes that this scroll gives its palace ladies the scholar's pastimes of qin, chess, calligraphy and painting."
  ],
  "doucao": [
    "A small group sits in a circle on the ground, holding out sprigs and flowers; more lie scattered beside them.",
    "Xu Wenmei identifies the game as doucao, a springtime contest played with plants. Who is winning? The painting is not telling."
  ],
  "reading": [
    "Two women lie side by side on a flowered rug, chins on their arms, sharing one open book.",
    "A long zither rests beside them. Xu Wenmei counts reading among the scroll's palace pastimes: learning, pictured as pure leisure."
  ],
  "parrot": [
    "On the red railing sits a small green parrot, and two women have stopped to look.",
    "Parrots turn up again and again in palace poems; one famous line says the ladies dare not gossip in front of the bird."
  ],
  "go": [
    "Around a low table, players lean over a gridded board dotted with black and white stones while friends crowd in to watch.",
    "The game is weiqi, known in English as Go. An attendant with a tall fan stands by."
  ],
  "infants": [
    "A woman lifts a baby in a red jacket while a toddler crawls at her knees, and another lady looks on from the stairs.",
    "'Playing with infants' is one of the pastimes scholars list in this scroll, with roots in much older paintings of court women."
  ],
  "embroidery": [
    "One woman pulls a thread high, another bends close over a long embroidery frame, and a third rests her chin on her hand.",
    "Needlework is on the museum's list of subjects for this scroll, tools included. Patience, apparently, came in different amounts."
  ],
  "ironing": [
    "Women stretch a length of white silk between them while one presses it with a pan of glowing coals: an iron.",
    "Xu Wenmei notes that the group closely echoes a famous older painting of court ladies preparing silk. Qiu Ying knew his classics."
  ],
  "harp": [
    "A lady plucks a tall, bow-shaped harp, the konghou, while her companion marks time with red clappers.",
    "Xu Wenmei shows that this pair was borrowed from a much older court painting. Qiu Ying was quoting a classic, almost figure for figure."
  ],
  "portrait": [
    "A painter leans toward his picture; his sitter, in red, holds perfectly still.",
    "The museum has long linked the scene to the legend of Mao Yanshou painting the beauty Wang Zhaojun. Scholars have questioned that reading, and the museum's own notes admit the theme has no single fixed story. So who is she?"
  ],
  "fan-chase": [
    "A woman in red steps forward with a round fan raised high above her head, sleeves and sash flying.",
    "The museum's catalogue lists butterflies in this scroll, and two rest in the willows further left, but none is near her. What caught her eye? The painting leaves it open."
  ],
};

const ordered = [...anchors].sort((a, b) => a.anchor[0] - b.anchor[0]);
export const stories = ordered.map((a, i) => ({
  ...a,
  text: copy[a.id],
  // Modern recordings chosen to suit each scene; illustration, not evidence of
  // how a Ming or Han palace sounded. Recipes: scripts/prep-han-sound.py.
  sound: { file: `han-${a.id}`, mode: 'once', gain: 0.8 },
  ...(i === anchors.length - 1 ? { nextLabel: 'Restart the Journey' } : {}),
}));
