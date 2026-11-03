# Sounds

Each moment's sound ships as `<name>.m4a` (AAC, Safari) and `<name>.ogg` (Vorbis), cut and mixed by
`scripts/prep-sound.sh` from the recordings in `raw/` (local only, see `.gitignore`). Which story uses
which file is set in `src/paintings/qingming/stories.js`.

The recordings are Freesound's public player previews (128 kbps Vorbis) of these CC0 sounds, saved
as `raw/<id>_<uploader>-hq.ogg`:

| File | Used by | Recordings (Freesound, CC0) |
|---|---|---|
| `donkey` (3.5 s, once) | farewell | [705300](https://freesound.org/people/felix.blume/sounds/705300/) felix.blume, *Donkey braying loud with distant village atmosphere* — first 3.5 s, the village tail left out |
| `towpath` (7.5 s, once) | towpath | Six heaves 1.1 s apart, tug-of-war style. On each heave eight "men" grunt together: [841313](https://freesound.org/people/takareads/sounds/841313/) takareads, *strenuous_grunts*, eight pitch-shifted copies at different levels with up to 60 ms of slack · a creak from [231438](https://freesound.org/people/6polnic/sounds/231438/) 6polnic, *hamp rope creaks* lands on each heave, the same recording (100–107 s) is the bed · [395563](https://freesound.org/people/SoundsForHim/sounds/395563/) SoundsForHim, *Panting*, five quiet copies between heaves · [260263](https://freesound.org/people/richardemoore/sounds/260263/) richardemoore, *WavesOnTheShore* |

| `oar` (7.5 s, once) | oar | Five strokes 1.4 s apart; on each a 32-copy grunt gang ([841313](https://freesound.org/people/takareads/sounds/841313/), pitch −820…+490 cents, ≤150 ms slack, compressed as one bus) pulls, every man grunting a second time, lower, as he leans in; a paddle stroke from [249707](https://freesound.org/people/brunoboselli/sounds/249707/) brunoboselli, *Paddles rowing on a calm water stream* (1.45 s) takes the water a beat later · bed: [438846](https://freesound.org/people/craigsmith/sounds/438846/) craigsmith, *G54-27-Oars Rowing* (5–12.5 s) and [260263](https://freesound.org/people/richardemoore/sounds/260263/) river |
| `table` (5 s, once) | table | [539811](https://freesound.org/people/denkmal/sounds/539811/) denkmal, *Tavern_Greece_indoor* ("incomprehensible murmuring"): four 5-s stretches (from 2, 9, 16, 22 s) laid over each other at slightly different pitches, low-passed at 2.2 kHz and given room reverb, so it is hubbub with no words in it; two bowls set down from [209009](https://freesound.org/people/OwlStorm/sounds/209009/) OwlStorm, *Kitchen Dish Clank*, and the river faint underneath |
| `taxi` (6 s, once) | taxi | [437078](https://freesound.org/people/craigsmith/sounds/437078/) craigsmith, *G52-05-Ox Cart* (wooden wheels: rumble, squeak, rattle), 9–15 s · [159498](https://freesound.org/people/davilca/sounds/159498/) davilca, *sfx-horse-steps-1* (horses walking down a dirt road), 1–7 s, lifted 150 cents to read as a smaller animal · three creaks from [231438](https://freesound.org/people/6polnic/sounds/231438/) 6polnic, *hamp rope creaks*, dropped 300 cents, as the load shifts · the donkey calls twice, at 1.0 and 3.9 s, from [759893](https://freesound.org/people/Sacha.Julien/sounds/759893/) Sacha.Julien, *Donkey Braying in mountain* (the start of its bray, then two pulses from 12.5 s), a different animal from the farewell's |
| `relay` (7 s, once) | relay | Three sleepers: [500803](https://freesound.org/people/khenshom/sounds/500803/) khenshom, *Light snores of a man sleeping*, two stretches (from 19 and 26 s) at different pitches and distances, and [678573](https://freesound.org/people/khenshom/sounds/678573/) khenshom, *Male Snores - Various snores - Close Up*, its quiet opening, muffled · a spear shaft slips: [593178](https://freesound.org/people/Stefan21100190/sounds/593178/) Stefan21100190, *dropping wooden stick* at 3.4 s · the courtyard behind: [628949](https://freesound.org/people/Kimskell/sounds/628949/) Kimskell, *Sparrows01* |
| `close-call` (7 s, once) | close-call | The crew: [480805](https://freesound.org/people/craigsmith/sounds/480805/) craigsmith, *R15-73-Small Group of Men Shouting* (not in English), 4.4–11.4 s, with a second copy 180 cents lower and 70 ms late · the bridge: [480809](https://freesound.org/people/craigsmith/sounds/480809/) craigsmith, *R24-01-Men Rallying*, 3–10 s · the far crowd: [438414](https://freesound.org/people/craigsmith/sounds/438414/) craigsmith, *G29-54-Men Yell Riot*, 11–18 s, low-passed at 1.8 kHz with reverb so no words survive · poles clatter at 1.6, 2.3 and 3.1 s and the hull takes the timber at 4.2 s: [478238](https://freesound.org/people/Fission9/sounds/478238/) Fission9, *Planks Clattering*, the heaviest fall dropped 400 cents, together with a bump from [506688](https://freesound.org/people/magzlurban/sounds/506688/) magzlurban, *Boat Gently Bumping Dock*, dropped 600 cents · under it the lines from [231438](https://freesound.org/people/6polnic/sounds/231438/) and [717850](https://freesound.org/people/TRP/sounds/717850/) TRP, *River, water rushing under bridge* |
| `ten-thousand` (6 s, once) | ten-thousand | The welcoming gate: [335891](https://freesound.org/people/Yoyodaman234/sounds/335891/) Yoyodaman234, *Bamboo Creaking in Wind*, 85–91 s, dropped 200 cents into a lattice tower · a banner: [386797](https://freesound.org/people/RichieMcMullen/sounds/386797/) RichieMcMullen, *flag_flap_2* · the room through the door: [539811](https://freesound.org/people/denkmal/sounds/539811/) tavern murmur low-passed at 1.5 kHz with reverb · wine poured at 1.4 s: [770039](https://freesound.org/people/Vrymaa/sounds/770039/) Vrymaa, *Water - Pouring on the ground, in a jar* (from a large ceramic pot), 2–4.4 s · the jar closed at 4.3 s: [453846](https://freesound.org/people/kyles/sounds/453846/) kyles, *cookie jar large ceramic clay pot open close lid*, 3.2–3.8 s |
| `delivery` (5 s, once) | delivery | [637558](https://freesound.org/people/kyles/sounds/637558/) kyles, *footsteps walking flip flops sandals dirt*, 1.5–8 s, sped to 1.3× so the walk is a hurry · seven bowl knocks from [209013](https://freesound.org/people/OwlStorm/sounds/209013/) OwlStorm, *High-pitched bowl impact with vibration*, at different pitches and levels, and the dish clank [209009](https://freesound.org/people/OwlStorm/sounds/209009/) as he picks them up · the street: [539811](https://freesound.org/people/denkmal/sounds/539811/) murmur, faint |
| `right-of-way` (6 s, once) | right-of-way | Two parties: [480804](https://freesound.org/people/craigsmith/sounds/480804/) craigsmith, *R15-72-Men Talking and Arguing* ("not in English"), 5–11 s, and a second copy 120 cents up and 0.4 s late · the horse: [397236](https://freesound.org/people/black_trillium/sounds/397236/) black_trillium, *Horse Snort* at 2.3 s, and hooves shifting on planks from [479679](https://freesound.org/people/craigsmith/sounds/479679/) craigsmith, *R13-07-Horse on Wood*, 24.5–30.5 s (after the voices in that recording) · onlookers: [438414](https://freesound.org/people/craigsmith/sounds/438414/) riot, 20–26 s, muffled |
| `poles` (6 s, once) | poles | [109485](https://freesound.org/people/BudJillett/sounds/109485/) BudJillett, *Wind-Gusts-late-autumn*, 64–70 s · the pole swaying: [335891](https://freesound.org/people/Yoyodaman234/sounds/335891/) bamboo, 120–126 s, dropped 400 cents · the ornament's mount creaks at 2.0 and 4.4 s: [231438](https://freesound.org/people/6polnic/sounds/231438/) · the river below: [717850](https://freesound.org/people/TRP/sounds/717850/), 10–16 s · two brief sparrow calls from [628949](https://freesound.org/people/Kimskell/sounds/628949/) Kimskell, *Sparrows01* (existing CC0 source): 0.32–0.66 s placed at 1.05 s (+220 cents, −9 dB peak), 1.02–1.40 s placed at 3.45 s (−120 cents, −17 dB peak); high-passed at 1.8 kHz, low-passed at 12 kHz, 8 ms attack/45 ms release fades. First call brighter and stronger; second lower and 8 dB quieter before the shared mix normalization |
| `rudder` (7 s, once) | rudder | Three strokes at 0.5, 2.5 and 4.5 s; on each the pivot groans ([231438](https://freesound.org/people/6polnic/sounds/231438/) creak, dropped 500 cents, 0.15 s early), the blade takes the water ([249707](https://freesound.org/people/brunoboselli/sounds/249707/) paddle stroke, dropped 350 cents) and the boatman breathes out (one [841313](https://freesound.org/people/takareads/sounds/841313/) grunt, dropped 100 cents) · water pushed aside: [480855](https://freesound.org/people/craigsmith/sounds/480855/) craigsmith, *R29-23-Rhythmic Movement of Water*, 46–53 s · bed: [438846](https://freesound.org/people/craigsmith/sounds/438846/) oars, dropped 200 cents, and [260263](https://freesound.org/people/richardemoore/sounds/260263/) waves |
| `life-aboard` (7 s, once) | life-aboard | [318064](https://freesound.org/people/ceich93/sounds/318064/) ceich93, *Water_Lapping_River* (the Hudson on a pebbly shore at night), 8–15 s · a small fire: [536935](https://freesound.org/people/Defaultv/sounds/536935/) Defaultv, *Campfire*, 3–10 s · a lid lifted at 2.6 and 5.0 s: [732158](https://freesound.org/people/LewisEmmott5/sounds/732158/) LewisEmmott5, *Ceramic_Lid_01* · the boat at its mooring: [231438](https://freesound.org/people/6polnic/sounds/231438/) rope creaks, dropped 200 cents, as a bed and at 1.2 and 4.6 s |

CC0 needs no attribution; the recordists are credited on the gallery page regardless.

## Prosperous Suzhou ambience

`gusu-birds` and `gusu-water` are **modern ambient illustrations**, not recordings of historical Suzhou. No new sources or unidentified voices are added. `scripts/prep-gusu-sound.sh` generates them from the existing raw recordings:

- `gusu-birds` (6 s): Kimskell, [628949, Sparrows01](https://freesound.org/people/Kimskell/sounds/628949/), CC0. First 6 seconds, high-pass 1.2kHz, low-pass 12kHz, peak −9dB, gentle fades.
- `gusu-water` (6 s): ceich93, [318064, Water_Lapping_River](https://freesound.org/people/ceich93/sounds/318064/), CC0. Seconds 8–14, peak −6dB, gentle fades.

Vorbis plus compact 22.05kHz mono PCM WAV fallback (the local OS AAC encoder is unavailable). Playback selects a supported format present for that recording. Qingming's existing clips are unchanged.

### Spatial-navigation audio trial — 2026-10-28

Eight sounding Gusu scenes now have **eight unique clips**. Other scenes are intentionally quiet; the former repeated assignments have been removed. Original `gusu-birds` is used only by 03 and `gusu-water` only by 09. This is modern illustrative ambience/foley, not evidence of the sounds of historical Suzhou, depicted bird species, or building materials. No voices or period music are added.

Additional clips from the existing CC0 raw archive, built reproducibly with `scripts/prep-gusu-audio-trial.sh` (Vorbis + mono PCM WAV fallback):

| Discovery | Clip | CC0 source and treatment |
|---|---|---|
| 04 Mudu market | `gusu-market-steps` | [637558, kyles, footsteps walking flip flops sandals dirt](https://freesound.org/people/kyles/sounds/637558/), 1.5–6.5s; high-pass100Hz; peak−8dB |
| 05 Temple compound | `gusu-courtyard-wind` | [109485, BudJillett, Wind-Gusts-late-autumn](https://freesound.org/people/BudJillett/sounds/109485/), 64–70s; band150Hz–5kHz; peak−14dB |
| 14 Wharf | `gusu-dock` | [506688, magzlurban, Boat Gently Bumping Dock](https://freesound.org/people/magzlurban/sounds/506688/), 1–7s; high-pass80Hz; peak−10dB |
| 16 Tea room | `gusu-tea-pour` | [770039, Vrymaa, Water - Pouring on the ground, in a jar](https://freesound.org/people/Vrymaa/sounds/770039/), 2–6.8s; high-pass200Hz; peak−9dB. Water-pouring foley, not a recording of a historical tea ceremony. |
| 20 Shantang canal | `gusu-paddle` | [249707, brunoboselli, Paddles rowing on a calm water stream](https://freesound.org/people/brunoboselli/sounds/249707/), 10–16s; high-pass100Hz; peak−10dB |
| 22 Tiger Hill | `gusu-bamboo` | [335891, Yoyodaman234, Bamboo Creaking in Wind](https://freesound.org/people/Yoyodaman234/sounds/335891/), 85–91s; band150Hz–6.5kHz; peak−12dB; wind/vegetation texture, not an assertion about the pagoda. |

All clips have short attack/release fades; per-scene playback gains are in Gusu `stories.js`. Recordings are each used by one Gusu scene only. Qingming's recordings and assignments are unchanged.

### Full 22-scene coverage — 2026-10-28

Supersedes the eight-scene trial above: all 22 Gusu discoveries now have audio. The previous eight files and gains are preserved; fourteen distinct clips are added. No Gusu scenes share a final clip, and no Qingming audio or story assignments are changed.

New sources were verified against the recordists’ Freesound pages for CC0 1.0, with page snapshots, preview URLs and SHA256s in `research/gusu-all-scenes-audio-2026-10-28/new-sources.json`. The downloaded public player previews are HQ MP3; output is Vorbis and compact mono PCM WAV fallback.

All are modern sound illustrations. Foreign recording locations, instruments and species are not presented as evidence about historical Suzhou. Scene texts/identifications are unchanged.

| Discovery | Clip | CC0 source and processing |
|---|---|---|
| 01 | `gusu-school-pages` | [860360, sokworks](https://freesound.org/people/sokworks/sounds/860360/). Two page turns at 0.55s and 2.8s; second quieter. |
| 02 | `gusu-cloth-loom` | [582994, snapcam](https://freesound.org/people/snapcam/sounds/582994/). Wooden hand-loom recording, 3–9s. The source is a modern Irish hand loom, not the depicted machine. |
| 06 | `gusu-wedding-gong` | [76886, airtaxi](https://freesound.org/people/airtaxi/sounds/76886/). Single gong with decay, 0–6s. Atmosphere, not a claim that musicians are visible. |
| 07 | `gusu-granary-grain` | [464005, juanforeromusic](https://freesound.org/people/juanforeromusic/sounds/464005/). Rice falling into a bowl, 0.2–6.2s; grain-handling foley. |
| 08 | `gusu-garden-ceramics` | [732158, LewisEmmott5](https://freesound.org/people/LewisEmmott5/sounds/732158/). Ceramic lid 2–3.4s and two quiet dish clanks from OwlStorm 209009 at 2.6 and 4s. [209009, OwlStorm](https://freesound.org/people/OwlStorm/sounds/209009/). |
| 10 | `gusu-pond-frogs` | [868875, sokworks](https://freesound.org/people/sokworks/sounds/868875/). Pond frogs, 5–11s. Source recorded at night in Australia; illustrative wetland ambience only, with no claim about depicted species, locality, season or time of day. |
| 11 | `gusu-theatre-drum` | [856550, sazanami12](https://freesound.org/people/sazanami12/sounds/856550/). Four soft dagu strokes at 0.35, 1.55, 2.15 and 3.65s with varied levels. An editorial rhythm, not a reconstruction of a Qing theatre score. |
| 12 | `gusu-dye-fabric` | [624477, ValentinPetiteau](https://freesound.org/people/ValentinPetiteau/sounds/624477/). Cloth movements, 2–8s; no machine sound. |
| 13 | `gusu-ruiguang-bell` | [668647, tec_studio](https://freesound.org/people/tec_studio/sounds/668647/). Bronze bell, 0–7s. Source is a Japanese bell recorded in San Francisco; illustrative tone, not the sound of Ruiguang Pagoda or evidence of a bell depicted there. |
| 15 | `gusu-wannian-steps` | [813622, SecureSubset](https://freesound.org/people/SecureSubset/sounds/813622/). Stone footsteps, 0.1–6.1s. Modern concrete-slab foley, not historical footwear. |
| 17 | `gusu-official-flags` | [386797, RichieMcMullen](https://freesound.org/people/RichieMcMullen/sounds/386797/). Flag cloth, first 4.9s, delayed0.4s. |
| 18 | `gusu-signs-market` | [539811, denkmal](https://freesound.org/people/denkmal/sounds/539811/). Tavern murmur 2–8s and16–22s layered, pitch−90/+110c, low-pass1.2kHz and room reverb. No invented dialogue or identities. |
| 19 | `gusu-gate-hooves` | [159498, davilca](https://freesound.org/people/davilca/sounds/159498/). Horse walking1–7s plus one quiet snort from black_trillium397236 at2.4s; generic gate-traffic atmosphere. [397236, black_trillium](https://freesound.org/people/black_trillium/sounds/397236/). |
| 21 | `gusu-shantang-rope` | [231438, 6polnic](https://freesound.org/people/6polnic/sounds/231438/). Mooring-rope creaks,100–106s. Boat-passage foley, not an assertion about a particular painted rope. |

Build recipe: `scripts/prep-gusu-all-scenes.py`. All fourteen are5–7seconds, non-looping, normalized to peaks between−10 and−14dB before scene gain, with attack/release fades. School and theatre use spaced one-shots; garden and gate layer distinct object/animal recordings. Output levels are measured in the QA record. None is an authentic historical performance claim.

### Requested nine-scene refinement, v2 — 2026-10-29

Supersedes first sound drafts for01,05,06,07,08,11,14,15,19 only. All22 scenes have sound. All original assets are preserved byte-for-byte. New v2 files allow rollback. Other13 clips/gains and all story copy, anchors, artwork and Qingming files unchanged.

New recordings verified CC0 1.0 on recordist pages; page snapshots, preview URLs and SHA256s in `research/gusu-audio-refinement-2026-10-29/new-sources.json`.

- [607215, jonopodmore](https://freesound.org/people/jonopodmore/sounds/607215/) — wooden-fish; HQ public player preview, CC0.
- [199930, thedapperdan](https://freesound.org/people/thedapperdan/sounds/199930/) — bulk-grain; HQ public player preview, CC0.
- [60470, thumpmonk](https://freesound.org/people/thumpmonk/sounds/60470/) — cup; HQ public player preview, CC0.
- [60476, thumpmonk](https://freesound.org/people/thumpmonk/sounds/60476/) — saucer; HQ public player preview, CC0.
- [545756, SamuelGremaud](https://freesound.org/people/SamuelGremaud/sounds/545756/) — gate-crowd; HQ public player preview, CC0.
- [806522, marc.om](https://freesound.org/people/marc.om/sounds/806522/) — dock-crowd; HQ public player preview, CC0.
- [365414, RutgerMuller](https://freesound.org/people/RutgerMuller/sounds/365414/) — cymbals; HQ public player preview, CC0.
- [856558, sazanami12](https://freesound.org/people/sazanami12/sounds/856558/) — drum-rim; HQ public player preview, CC0.

Mix design, reproducible via `scripts/prep-gusu-refinement-v2.py`; exact cues and relative gains in `mix-recipes.json`:

|Scene|Treatment|
|---|---|
|01 School|Three slower softened page turns, quiet courtyard air. Peak about9.5dB below previous draft before unchanged scene gain. No invented lesson or text.|
|05 Temple|Five spaced wooden-fish strikes, distant bronze bell and quiet air, mild room decay.|
|06 Wedding|Four gong strikes at0.4/2.7/5.1/7.35s; twelve softer drum beats and two small-cymbal accents,10s.|
|07 Granary|9s continuous bag-of-rice pour, source15–24s. Replaces sparse bowl grains. Original recording uses a plastic bucket: grain-handling foley, not a historical container claim.|
|08 Garden|Naturally gentle tea-set recordings at irregular intervals with very low distant guests. Heavy lid scrape/dish impacts removed.|
|11 Theatre|Two brisk drum phrases, contrasting rim strokes, short fill and cymbal accents;32 cues over10s.|
|14 Wharf|Three different Chinatown market passages, hull contact and low water. Separate crowd source from city gate.|
|15 Bridge|Existing stone-step texture plus continuous quiet river water, using a different segment from scene09.|
|19 City gate|Outdoor market crowd in three passages, hooves and one restrained snort.|

These are contemporary editorial sound illustrations, not reconstructed Qing performances or evidence of depicted instruments. Wooden fish and small cymbals were recorded outside China; crowd beds are modern foreign markets. No invented dialogue or attributed speakers. Crowd passages overlap with slight pitch differences and a230Hz–1.5kHz band to keep them distant. Final peaks−11 to−19dBFS before gains, short fades, non-looping playback.

### Third audition — 2026-10-29

User requested brighter wedding sound, discrete dry grain gestures, quiet plucked strings in the garden, and no9–10s clips. Source workflow follows Qingming scene effects: short CC0 Freesound recordings layered with individual cue levels/fades. Gallery music is separate: user-supplied videos (assets/music/SOURCE.md); none of those pieces was sampled for this revision.

- [847157, nanliu_music](https://freesound.org/people/nanliu_music/sounds/847157/) — guzheng, CC0 verified on recordist page; HQ preview with SHA256 and page snapshot in dated review folder.
- [799515, Throndronis](https://freesound.org/people/Throndronis/sounds/799515/) — dry-rice, CC0 verified on recordist page; HQ preview with SHA256 and page snapshot in dated review folder.

- 06 `gusu-wedding-festive-v3`:7.8s. Replaces long low gong with four short bright damped accents, buoyant paired drum strokes, rim responses and short cymbals. No temple bell/wooden fish; no suona excerpt from an unidentified performance. Contemporary editorial rhythm, not a reconstructed wedding score.
- 07 `gusu-granary-dry-rice-v3`:7.5s. Three discrete dry-rice gestures using actual rice shaken in a container, plus small falling-grain tails. Old continuous bulk-pour layer removed. There are pauses between gestures; no water source is used. Modern grain-handling foley, not a literal historical container claim.
- 08 `gusu-garden-guzheng-v3`:7.8s. Retains gentle cups/guests and adds two soft recorded guzheng plucks at0.55/4.15s. String sources normalize−24/−26dBFS before layering; no full music bed. No claim that a specific instrument is visibly depicted.
- 11 `gusu-theatre-short-v3`:7.8s. Condenses earlier drum/rim/cymbal pattern and preserves a final accent and decay, rather than cutting off the10s phrase.
- 05/14/19: native-speed7.8s edits with650ms release; no tempo changes. All existing shorter effects remain at their natural lengths. Current22 clips range4.8–8s, none exceed8s.

Recipes: `scripts/prep-gusu-refinement-v3.py`; exact cues and duration decisions: `research/gusu-audio-v3-2026-10-29/mix-recipes.json`. Original audio, artwork, approved copy and all Qingming assets unchanged. Earlier recordings remain available for rollback.

### Fourth audition — 2026-10-29

Five requested revisions only:01/06/17/20/21, all<=8s. Current and prior assets remain available for comparison. All17 other sound assignments, artwork and story copy unchanged.

## CC BY4.0 excerpts (new)

- [161905, xserra](https://freesound.org/people/xserra/sounds/161905/) — guqin; [CC BY4.0](https://creativecommons.org/licenses/by/4.0/). Source page snapshot, public preview URL and hash in the dated source manifest. Edited as noted below.
- [162035, xserra](https://freesound.org/people/xserra/sounds/162035/) — ensemble; [CC BY4.0](https://creativecommons.org/licenses/by/4.0/). Source page snapshot, public preview URL and hash in the dated source manifest. Edited as noted below.

- 01 `gusu-school-guqin-v4`,8s: retains soft pages/air, adds18–25.8s of *Guqin-4.wav* by xserra at low level (guqin layer peak−28dBFS before final mix). This is independent from nanliu_music’s guzheng recording in garden08.
- 06 `gusu-wedding-ensemble-v4`,7.8s:0.3–8.1s of *beijing-opera-7.wav* by xserra. A real modern performance with suona and percussion, retaining natural phrasing/timbre instead of constructing a chopped cymbal wash.65Hz high-pass, fades, normalization. The source is a Beijing Opera performance in2012, not a wedding recording or evidence about the painted celebration. Used as editorial festive atmosphere; no claim to reconstruct a Qing wedding score.

Both original works recorded by xserra are CC BY4.0. Required titles, recordist, source links, licence and edit notices are provided in app About/Sources and audition/compare pages. Clips were trimmed, faded and mixed; source recordings retain their licence.

## Existing CC0 sources

- 17 `gusu-official-courtyard-v4`,7.8s: BudJillett109485 wind34–41.8s and distant SecureSubset813622 steps2–5s. The previous heavy flag-slap layer is removed. No claim of a depicted action.
- 20 `gusu-canal-clear-paddle-v4`,7.8s: brunoboselli249707 actual paddle strokes10–17.8s; mild dynamics and90Hz–10kHz band, peak−8dBFS and scene gain0.8. Clearer/louder native-water texture, not a different river reconstruction.
- 21 `gusu-bridge-boats-ambience-v4`,7.8s: existing rope texture with low river lapping (ceich93318064,31–38.8s) and two very distant crowd passages (SamuelGremaud545756,111–118.8/140–147.8s), beneath primary rope. No invented speech or speakers.

Recipes: `scripts/prep-gusu-refinement-v4.py`. Selected duration/levels/cues: `research/gusu-audio-v4-2026-10-29/mix-recipes.json`; measurements: `audio-checks.json`.


## 2026-11-01 — Gusu balanced v5

All 22 current Gusu files use the `gusu-balanced-<stable-scene-id>-v5` prefix, with Ogg and mono WAV versions. Earlier source files remain unchanged for rollback. These are modern illustrative soundscapes.

Loudness uses 48 kHz mono BS.1770 K weighting, 400 ms windows / 100 ms hops, -70 LUFS absolute and -10 LU relative gates. Values are mono estimates, including the 0.8 playback gain, not stereo programme certification. Target approximately -24.5 LUFS, near the existing Qingming median (-22.92). Selective transient compression preserves headroom; final Ogg measurements in `research/gusu-smooth-audio-2026-11-01/after-levels.json`. Reproducible script: `scripts/prep-gusu-balanced-v5.py`.

School: same licensed xserra Guqin-4.wav (161905, CC BY 4.0), 18–25.8s, brought forward against the existing soft-page mix. Credit and licence links above and in About remain applicable. Administration: existing courtyard breeze/steps plus a different, indistinct crowd passage, 66–73.8s, from SamuelGremaud's CC0 market recording 545756 (https://freesound.org/people/SamuelGremaud/sounds/545756/). Filtered, faded and mixed to suggest quiet activity, not intelligible invented dialogue. All other scenes retain their approved source mixes, with loudness/dynamics adjustments only.
