# Master source: Spring Dawn in the Han Palace

## The work

| | |
|---|---|
| Title | 明仇英漢宮春曉 卷 / *Spring Dawn in the Han Palace* |
| Artist | Qiu Ying 仇英 (c. 1494–1552), Ming dynasty |
| Collection | National Palace Museum, Taipei, accession 故畫001038 |
| Medium and size | Handscroll, ink and colour on silk; painting 30.6 × 574.1 cm |
| Catalogue | https://digitalarchive.npm.gov.tw/Collection/Detail?dep=P&id=3672 |
| Scholarly guide | Xu Wenmei 許文美, 〈宮中行樂—仇英〈漢宮春曉〉研究〉, 故宮學術季刊 36:1, pp. 37 ff. (https://theme.npm.edu.tw/Academic/ResearchDownload.ashx?bid=5938&eid=0) |

A Ming painting that imagines a Han palace. It is not a record of Han court life.

## The master file

| | |
|---|---|
| File | `assets/paintings/han-palace/master/Spring_Morning_in_the_Han_Palace.jpg` (git-ignored by the existing `assets/paintings/*/master/*` rule, same as Qingming) |
| Size | 52,680 × 2,683 px, 280,723,350 bytes |
| SHA-256 | `556575e5ec4326bdd03efa6c7cb1545845c6511ff2333826605c5c475f33c07a` |
| SHA-1 | `e055d9f677781931d5b4b7dd95a872f57485115b` (identical to the value the Commons API reports) |
| File page | https://commons.wikimedia.org/wiki/File:Spring_Morning_in_the_Han_Palace.jpg |
| Direct URL | https://upload.wikimedia.org/wikipedia/commons/c/c3/Spring_Morning_in_the_Han_Palace.jpg |
| Downloaded | 2026-11-09 |
| Licence | Public domain per Commons (faithful reproduction of a public-domain two-dimensional work). Commons credit line: "scanned by Krause, Johansen". Not a National Palace Museum download. |
| State | Untouched. |

## Edition check (passed)

Compared the full master against the museum catalogue and Xu Wenmei's Figs. 1–3 and 12–24:

- Opens at the right with the empty swing in willow mist, then the half-open gate (Xu Fig. 12).
- Ends at the left with the signature 仇英實父謹製 and the seals 實父 and 仇英 (catalogue; Xu Fig. 2).
- The ink character 慮 is at the lower right corner of the silk (catalogue; Xu Fig. 3).
- Collector and imperial seals named in the catalogue are present (乾隆御覽之寶, 嘉慶御覽之寶, 宣統御覽之寶, 石渠寶笈, 御書房鑑藏寶, 項元汴 and 梁清標 seals).
- Every scene Xu illustrates (Figs. 13–24, 39-1, 42) was found in this file with matching figures and poses.

This is the Qiu Ying scroll, not the Qing court versions or the other attributed copies.

## What the file contains, and what it does not

- Painted silk runs from about x 2,400 to x 50,730. That is about 48,300 px for 574.1 cm, roughly 84 px per cm.
- Both strips of mounting silk (隔水) are included, left of x 2,400 and right of x 50,730.
- The tail paper (拖尾) is **not** included, so Xiang Yuanbian's price note is not in this master.

## Colour (decided 2026-11-09: match the museum)

- The JPEG is CMYK with no embedded profile, and it is a scan of a printed reproduction, so its colour is warmer and more saturated than the painting.
- Reference: 16 preview photographs from the museum's own catalogue page for 故畫001038 (several include the museum's colour chart and the accession label). Each was registered to the master by feature matching, giving about 37,000 matched pixel pairs.
- Treatment: (1) CMYK to sRGB with the macOS Generic CMYK profile; (2) one global correction, quadratic in Lab, fitted to those pairs. Median colour difference to the museum's photographs fell from ΔE 16.9 to 2.7. Coefficients and the list of reference images are in `COLOR_FIT.json` (copied to `assets/paintings/han-palace/color-fit.json`).
- The correction is global: no local retouching, sharpening or repainting. The master file is unchanged; `scripts/prep-han.py` applies the treatment each time it derives the web images.
- All crops in this package now use the matched colour.
- Limit: the museum previews are 600 px wide and come from more than one photography campaign, so this is a close match, not a calibrated one.

## Print screen

The scan shows a fine print screen at 100%. The app therefore shows tiles at 0.7x and caps zoom at native size (1.3x only for the four smallest subjects).

## Corrections to the brief

- The brief gives Xu's Fig. 23 as geese/ducks. In the article Fig. 23 is the parrot.
- The brief warns that sources disagree on the classification character and the value. They agree: 慮, and 200 gold (catalogue 價值兩百金; Xu 值價貳佰金).
- The brief says the museum's English text mentions Go. The catalogue's English text says "chess"; Go is my reading of the board.
