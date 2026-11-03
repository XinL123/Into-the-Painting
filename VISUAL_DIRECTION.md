# Visual direction — gallery / homepage

## How I read the reference

The reference shows a row of paintings, each seen through a tall brushstroke-shaped window on a pale
ground, with a brushed title above and a caption under the selected piece.

What it does well, and what we keep as *ideas*:

- Artworks are not in boxes. The picture's edge is a painted edge.
- Each window has its own silhouette, so the row feels made by hand.
- The art is the interface: you choose by touching a painting, not a button.
- Information appears only for the piece you are attending to.
- A lot of empty, quiet ground.

What belongs to the reference and is **not** taken:

| Reference | Ours |
|---|---|
| Even row of same-size vertical strokes | Windows whose shapes come from Chinese mounting formats, of different sizes, placed asymmetrically |
| Oil-impasto stroke edges (Western brush) | Ink behaviour on paper: dry-brush streaks (飞白), wet bleed, pooled edge |
| Brushed display lettering as the title | Quiet typeset title, a vertical Chinese line, one seal |
| Smoke/shadow drifting behind | Nothing behind; negative space (留白) is left empty on purpose |
| Centred, symmetric composition | Off-centre, weighted to one side, like a painting with its inscription |
| Bright cool-white ground | Warm, slightly uneven paper |

## Our language

**Ground.** Warm xuan-paper tone with fine fibre grain and very slight unevenness, like a mounted
sheet. No gradients, no shadows under things.

**Windows.** Each painting is revealed through an ink-shaped mask. The silhouettes echo the real
formats in which Chinese paintings are mounted, so shape carries meaning:

```
  手卷 handscroll      立轴 hanging scroll     扇面 fan        册页 album leaf     团扇 round fan
  ▁▂▃▃▃▃▃▃▃▃▃▂▁          ▂▃▂                 ▁▃▅▅▅▃▁           ▃▃▃▃▃              ▂▄▄▂
  ▀▀▀▀▀▀▀▀▀▀▀▀▀          ███                ▀▀▃▃▃▃▀▀           █████             ██████
                         ███                                   ▀▀▀▀▀              ▀▀▀▀
   long, low             ▀▀▀  tall, narrow
```

The edges are irregular: one side dry and streaked, another soft where the ink "bled". 清明上河图,
a handscroll, gets the long low window, which also foreshadows the overview that follows.

**Composition (low-fidelity sketch).**

```
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                        入   │
│                                                                        画   │
│   ▁▂▃▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▃▂▁                                                 │
│   █ 清明上河图 (live, faint motion) █          ▒▒▒                 small    │
│   ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀                    ▒▒▒  forthcoming     intro    │
│    清明上河图 · 张择端 · 北宋                   ▒▒▒                 text     │
│    Along the River During the                                      ▣ seal  │
│    Qingming Festival                ░░░░░░                                 │
│                                     ░░░░░░ forthcoming                     │
│              ░░░░                                                          │
│              ░░░░ forthcoming                          ░▒░ forthcoming     │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
   one live window, large; four pale ink-wash shapes; more than half the page empty
```

**Colour.** Paper (warm off-white), ink (soft black, never pure #000), two ink-wash greys, and one
accent: cinnabar seal red, used once per screen (the seal, or the "enter" mark). No other colours;
the paintings supply the rest.

**Typography.**

- Chinese: a Song/Ming-style serif (e.g. Source Han Serif / Noto Serif SC), light to regular weights.
  Titles may be set vertically, right to left, as in an inscription.
- Latin: a calm old-style serif (e.g. EB Garamond or Cormorant), small sizes, generous letter-spacing
  for labels, italic for English titles.
- No brush-script display fonts: imitation calligraphy next to real brushwork looks cheap. The
  typography stays typeset and lets the paintings carry the hand.
- Small text, few words. Title, artist, dynasty, collection; one line of intro.

**Layout principles.**

- Asymmetry and 留白: content occupies less than half the page.
- No grid lines, cards, borders, drop shadows, pills or rounded rectangles.
- Things align to an invisible vertical rhythm, like columns of an inscription.
- Horizontal emphasis for this pilot (a handscroll is read sideways).

**Motion.** Slow and eased; nothing bounces. Windows arrive as if ink were soaking in (the mask grows
from its wet edge), not sliding or popping.

## Hover and selected states

| State | Behaviour |
|---|---|
| Rest | Live window shows the painting through its brushed mask, slightly desaturated toward paper; an almost imperceptible drift inside the window |
| Hover (live) | Mask spreads a little, as if more ink were laid down; the image comes to full tone; title line, artist/dynasty and a small "入画 · Enter" appear beside it |
| Hover (forthcoming) | The wash darkens very slightly; a small label "待展 · forthcoming" appears; cursor stays default; nothing else |
| Selected | The window's mask opens out along its length into the full scroll, which becomes the overview. The other shapes fade into the paper |
| Keyboard focus | Same as hover, with a thin ink underline on the title for visible focus |

## Gallery decision (approved 2026-10-02)

The section below is superseded where it differs: there are **no "forthcoming" labels and no named or
implied specific future works**. 清明上河图 is the only selectable artwork. Abstract brush / ink
silhouettes may appear purely as quiet compositional elements, without labels or hover states. The
page must read as intentional and complete with one painting.

## A gallery with only one real painting (original proposal)

- The live painting is given clear primacy in size and position, so the page reads as a composed
  sheet with one subject, not a shelf with gaps.
- The four future works appear as empty ink-wash shapes in their format silhouettes, labelled only
  "待展 · forthcoming". No stand-in images and no named titles until a work is chosen and sourced
  properly.
- The shapes are positioned so that removing or filling one later does not require re-composing the
  page.
- If placeholders feel like clutter when we see it in the browser, the fallback is a single-work page
  with the same language and no placeholders.

## Overview and scene UI (brief)

- Overview: the scroll lies on the paper ground at full width, with soft edges where it meets the
  paper. The enterable scene is marked by a thin brushed bracket and a small cinnabar dot; no boxes
  or pulsing hotspots.
- Scene: almost no interface. A small back mark in a corner, a one-line caption that fades after a
  few seconds, a credit line available on request. The painting fills the view.

## Avoiding a "generic AI site" look

No glass, glow, neon, gradient meshes, floating particles, ink-splash stock effects, dragon/cloud
ornaments or fake-calligraphy fonts. If an element is not paper, ink, seal or the painting itself,
it needs a reason to be there.
