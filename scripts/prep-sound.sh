#!/usr/bin/env bash
# Cuts and mixes the moments' sounds from the recordings in assets/sound/raw/
# (Freesound previews, CC0; see assets/sound/SOURCE.md) into assets/sound/
# as <name>.ogg (Vorbis, sox) and <name>.m4a (AAC, macOS afconvert).
#
#   scripts/prep-sound.sh            # every clip
#   scripts/prep-sound.sh donkey     # one clip
#
# Trim points were chosen by listening; adjust the TRIM_* values, not the recipe.
set -euo pipefail
cd "$(dirname "$0")/.."
RAW=assets/sound/raw
OUT=assets/sound
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

# raw files, by Freesound id
DONKEY=$RAW/705300_1661766-hq.ogg       # felix.blume, Donkey braying loud with distant village atmosphere
PANT=$RAW/395563_7386498-hq.ogg         # SoundsForHim, Panting
GRUNT=$RAW/841313_18316981-hq.ogg       # takareads, strenuous_grunts
ROPE=$RAW/231438_2016452-hq.ogg         # 6polnic, hamp rope creaks
WATER=$RAW/260263_509379-hq.ogg         # richardemoore, WavesOnTheShore
OARS=$RAW/438846_2524442-hq.ogg         # craigsmith, G54-27-Oars Rowing (wood, creak, distant voices)
PADDLE=$RAW/249707_300738-hq.ogg        # brunoboselli, Paddles rowing on a calm water stream
DINERS=$RAW/539811_2396346-hq.ogg       # denkmal, Tavern_Greece_indoor (incomprehensible murmuring)
# earlier: 82809_519220-hq.ogg, soloan, Restaurant amb1 (Hong Kong) — modern speech came through
CLANK=$RAW/209009_140737-hq.ogg         # OwlStorm, Kitchen Dish Clank
CART=$RAW/437078_2524442-hq.ogg         # craigsmith, G52-05-Ox Cart (wooden wheels: rumble, squeak, rattle)
HOOVES=$RAW/159498_1177772-hq.ogg       # davilca, sfx-horse-steps-1 (two horses walking down a dirt road)
SNORE=$RAW/500803_6652872-hq.ogg        # khenshom, Light snores of a man sleeping
SNORE2=$RAW/678573_6652872-hq.ogg       # khenshom, Male Snores - Various snores - Close Up
STICK=$RAW/593178_12589965-hq.ogg       # Stefan21100190, dropping wooden stick
SPARROWS=$RAW/628949_3311539-hq.ogg     # Kimskell, Sparrows01
CREW=$RAW/480805_2524442-hq.ogg         # craigsmith, R15-73-Small Group of Men Shouting (not in English)
BRIDGE=$RAW/480809_2524442-hq.ogg       # craigsmith, R24-01-Men Rallying
RIOT=$RAW/438414_2524442-hq.ogg         # craigsmith, G29-54-Men Yell Riot
HULL=$RAW/506688_10949426-hq.ogg        # magzlurban, Boat Gently Bumping Dock
PLANKS=$RAW/478238_9395330-hq.ogg       # Fission9, Planks Clattering (dropped onto bricks)
RIVER=$RAW/717850_97550-hq.ogg          # TRP, River, water rushing under bridge
DONKEY2=$RAW/759893_14889307-hq.ogg     # Sacha.Julien, Donkey Braying in mountain (Blumlein); a different animal from the farewell's
# fallback: 675411_2524442-hq.ogg, craigsmith, S02-01 Donkey braying (vintage optical transfer)
FLAG=$RAW/386797_7236624-hq.ogg         # RichieMcMullen, flag_flap_2
BAMBOO=$RAW/335891_2792951-hq.ogg       # Yoyodaman234, Bamboo Creaking in Wind (a single bamboo tree)
POUR=$RAW/770039_13973196-hq.ogg        # Vrymaa, Water - Pouring on the ground, in a jar (from a large ceramic pot)
JARLID=$RAW/453846_612689-hq.ogg        # kyles, cookie jar large ceramic clay pot open close lid
SANDALS=$RAW/637558_612689-hq.ogg       # kyles, footsteps walking flip flops sandals dirt
# backup: 352870_4187409-hq.ogg, PotatokingXII, Footsteps Dirt Gravel
BOWL=$RAW/209013_140737-hq.ogg          # OwlStorm, High-pitched bowl impact with vibration
ARGUE=$RAW/480804_2524442-hq.ogg        # craigsmith, R15-72-Men Talking and Arguing (not in English)
SNORT=$RAW/397236_4889106-hq.ogg        # black_trillium, Horse Snort
HOOFWOOD=$RAW/479679_2524442-hq.ogg     # craigsmith, R13-07-Horse on Wood (a man's "giddy-up" and a director earlier in it)
WIND=$RAW/109485_1213320-hq.ogg         # BudJillett, Wind-Gusts-late-autumn (pine forest, 20+ mph)
SWEEPWATER=$RAW/480855_2524442-hq.ogg   # craigsmith, R29-23-Rhythmic Movement of Water
LAPPING=$RAW/318064_4457609-hq.ogg      # ceich93, Water_Lapping_River (the Hudson on a pebbly shore at night)
FIRE=$RAW/536935_11867884-hq.ogg        # Defaultv, Campfire (calm popping and crackling)
POTLID=$RAW/732158_15889796-hq.ogg      # LewisEmmott5, Ceramic_Lid_01 (lifted and scraped)

# where each clip is cut from its recording (seconds): start, length
TRIM_DONKEY=(0.0 3.5)      # the first bray and its hee-haw pulses; village tail left out
TRIM_PANT=(0.0 11.0)       # steady breathing; the sigh at the end left out
TRIM_ROPE=(100.0 11.0)     # the busiest stretch of creaking
TRIM_WATER=(0.0 11.0)
DUR=7.5            # the towpath clip's length, seconds; it plays once and fades
# the gang heaves together, tug-of-war style: at each heave every man grunts at
# once. One recorded man becomes a gang by pitch (cents), a little slack (s) so
# they are together but not one voice, and a level (dB) so some stand nearer.
HEAVES=(0.5 1.6 2.7 3.8 4.9 6.0)                    # when they pull (s)
MEN=(
  "0 0 -14"      "-220 0.03 -15"  "130 0.05 -16"   "-370 0.015 -15"
  "-90 0.06 -17" "260 0.025 -18"  "-480 0.045 -16" "40 0.01 -19"
)
GRUNT_STARTS=(2.6 4.3 6.3 7.6 9.3)                  # distinct grunts in the recording (s)
ROPE_STRAIN=101.0                                   # a creak to land on each heave (s)
# the breathing between heaves, quieter: pitch (cents), start (s)
VOICES=("0 0" "-180 0.9" "140 1.7" "-300 0.4" "220 1.3")

# the oar: eight men on one sweep, so a bigger gang than the towpath and a
# harder pull: each man grunts on the catch and again, lower, as he leans in
OAR_DUR=7.5
STROKES=(0.6 2.0 3.4 4.8 6.2)                       # when the sweep is pulled (s)
OAR_MEN=(
  "0 0 -11"        "-220 0.03 -12"  "130 0.05 -13"   "-370 0.015 -12"
  "-90 0.07 -14"   "260 0.025 -15"  "-480 0.045 -13" "40 0.01 -16"
  "-150 0.085 -14" "320 0.06 -16"   "-600 0.02 -14"  "90 0.04 -17"
  "-280 0.1 -15"   "180 0.09 -17"   "-700 0.055 -15" "-40 0.115 -18"
  "420 0.035 -18"  "-530 0.08 -16"  "230 0.12 -19"   "-330 0.065 -17"
  "-120 0.13 -16"  "70 0.095 -18"   "-820 0.03 -16"  "360 0.11 -19"
  "-430 0.14 -17"  "-20 0.05 -19"   "200 0.15 -20"   "-660 0.075 -18"
  "110 0.125 -20"  "-250 0.145 -19" "490 0.07 -21"   "-560 0.105 -19"
)
LEAN=0.32                                           # the second, deeper grunt lands this much later (s)
GANG_LEVEL=-6                                       # the whole gang, after compression, sits here
TRIM_OARS=(5.0 7.5)                                 # wood and creak bed, from the rowing recording
PADDLE_STROKE=1.45                                  # one paddle stroke to land on each pull (s)

# the restaurant: the hubbub of the room without a single modern sentence in
# it. Four stretches of the recording are laid over each other, each nudged in
# pitch, then muffled as if heard from the stairs, so words dissolve into talk.
TABLE_DUR=5
DINER_LAYERS=("2 0" "9 -70" "16 90" "22 -140")      # start in the recording (s), pitch (cents); it is 31 s long
CLANKS=(1.2 3.1)                                    # when a bowl lands (s)

# the cart: a loaded hand-cart and a donkey walk out of the city gate. The
# wooden wheels are the ox cart's steady stretch; the hooves are the dirt-road
# horses, lifted a little so they read as a smaller animal; the load creaks.
TAXI_DUR=6
TRIM_CART=(9.0 6.0)                                 # the busiest, steadiest turning of the wheels
TRIM_HOOVES=(1.0 6.0)
HOOVES_PITCH=150                                    # cents: horse → donkey
CART_CREAKS=(0.9 2.5 4.1)                           # when the load shifts (s)
# the donkey calls twice: the start of its bray, then a couple of pulses from
# further in, so the second call is not the first repeated. start in the
# recording, length, when it lands (s), level (dB)
BRAYS=("4.75 2.0 1.0 -10" "12.5 1.3 3.9 -12")

# the relay station: nine guards, several asleep. Three sleepers at
# different pitches and distances, a spear shaft slips and knocks the ground,
# sparrows in the courtyard behind.
RELAY_DUR=7
TRIM_SPARROWS=(1.0 7.0)
SLEEPERS=("19.0 0 -17" "26.0 -250 -20")             # start in the light-snores recording (s), pitch (cents), level (dB)
SLEEPER2=("0.0 120 -22")                            # the same, in the various-snores recording
SPEAR_AT=3.4                                        # when the shaft knocks (s)
STICK_HIT=1.95                                      # where the knock sits in its recording (s)

# the close call: shouting from the crew and the bridge, the river hard
# against the pier, poles clatter, then the hull takes the timber.
CALL_DUR=7
TRIM_CREW=(4.4 7.0)                                 # the loudest stretch of the crew shouting
TRIM_BRIDGE=(3.0 7.0)                               # the crowd on the bridge
TRIM_RIOT=(11.0 7.0)                                # the far crowd, muffled
TRIM_RIVER=(5.0 7.0)
POLE_CLATTERS=("1.45 1.0 1.6" "2.95 0.9 2.3" "6.45 1.1 3.1")   # start in the planks recording, length, when it lands (s)
HIT_AT=4.2                                          # the hull meets the bridge (s)
HIT_PLANK=(0.0 1.2)                                 # the heaviest plank fall
HIT_HULL=5.2                                        # a bump from the dock recording, deepened

# the wine house: its bamboo welcoming gate sways and creaks, a banner flaps,
# the room's hubbub leaks through the door, wine is poured and a jar closed
TAVERN_DUR=6
TRIM_GATE=(85.0 6.0)                                # the creakiest stretch of the bamboo
GATE_PITCH=-200                                     # cents: a lattice tower, not a stalk
TRIM_LEAK=(9.0 6.0)                                 # the tavern murmur, as heard from the street
POUR_AT=1.4                                         # the wine (s)
TRIM_POUR=(2.0 2.4)
JAR_AT=4.3                                          # the jar closed (s)
TRIM_JARLID=(3.2 0.6)

# the delivery runner: quick steps in sandals, two bowls chattering in one
# hand, the street behind him
RUN_DUR=5
TRIM_SANDALS=(1.5 6.5)                              # the steps, a quiet recording lifted by norm
HURRY=1.3                                           # tempo: the walk becomes a hurry
# when the bowls knock, pitch (cents), level (dB)
BOWL_KNOCKS=("0.4 0 -22" "0.9 90 -25" "1.5 -60 -23" "2.2 40 -26" "2.8 -120 -24" "3.5 70 -25" "4.1 -30 -24")

# the bridge crest: two parties' attendants quarrel, the horse snorts and
# shifts on the planks, the crowd around them
ROW_DUR=6
TRIM_ARGUE=(5.0 6.0)                                # the loudest interjections
SNORT_AT=2.3
TRIM_HOOFWOOD=(24.5 6.0)                            # hooves on wood, late in the recording, after the talk
TRIM_FARCROWD=(20.0 6.0)                            # the riot recording, muffled

# the poles: wind, creaking, river below, and two brief sparrow calls
POLES_DUR=6
TRIM_WIND=(64.0 6.0)                                # the strongest gusts
TRIM_POLE=(120.0 6.0)                               # the bamboo again, deepened into a mast-high pole
POLE_PITCH=-400
POLE_CREAKS=(2.0 4.4)                               # the ornament's mount (s)
POLE_BIRDS=("0.32 0.34 1.05 -9 220" "1.02 0.38 3.45 -17 -120") # source start, length, arrival, level (dB), pitch (cents)

# the stern sweep: slow heavy strokes, the sweep groaning on its pivot, water
# pushed aside, one boatman breathing
SWEEP_DUR=7
SWEEPS=(0.5 2.5 4.5)                                # when the sweep is pulled (s)
TRIM_SWEEPWATER=(46.0 7.0)

# the moored home: water lapping at the hull, a small cooking fire, a ceramic
# lid lifted twice, the boat creaking at its mooring
HOME_DUR=7
TRIM_LAPPING=(8.0 7.0)
TRIM_FIRE=(3.0 7.0)                                 # pops at 3.5, 5, 6, 7.5, 9.5 s of the recording
LIDS=("0.8 1.2 2.6 -16" "3.9 0.8 5.0 -19")          # start in the lid recording, length, when (s), level (dB)
MOORING_CREAKS=(1.2 4.6)

encode() {          # encode <wav> <name>: both web formats
  sox "$1" -C 5 "$OUT/$2.ogg"
  afconvert -f m4af -d aac -b 64000 "$1" "$OUT/$2.m4a"
  printf '%-8s %s\n' "$2" "$(soxi -d "$1")"
}

donkey() {
  sox "$DONKEY" -r 44100 -c 1 "$TMP/donkey.wav" trim "${TRIM_DONKEY[@]}" fade t 0.05 0 0.7 norm -6
  encode "$TMP/donkey.wav" donkey
}

towpath() {
  local i=0 h m v at layers=()
  # each man's grunts, cut short and placed on every heave
  for m in "${MEN[@]}"; do
    set -- $m
    local pitch=$1 slack=$2 level=$3 k=0
    for h in "${HEAVES[@]}"; do
      local start=${GRUNT_STARTS[$(( (k + i) % ${#GRUNT_STARTS[@]} ))]}
      at=$(echo "$h + $slack" | bc)
      sox "$GRUNT" -r 44100 -c 1 "$TMP/g$i-$k.wav" trim "$start" 0.7 fade t 0.01 0 0.25 pitch "$pitch" pad "$at" 0 pad 0 "$DUR" trim 0 "$DUR" norm "$level"
      layers+=("$TMP/g$i-$k.wav"); k=$((k + 1))
    done
    i=$((i + 1))
  done
  # the rope takes the strain with them
  for h in "${HEAVES[@]}"; do
    sox "$ROPE" -r 44100 -c 1 "$TMP/strain$i.wav" trim "$ROPE_STRAIN" 0.6 fade t 0.02 0 0.3 pad "$h" 0 pad 0 "$DUR" trim 0 "$DUR" norm -16
    layers+=("$TMP/strain$i.wav"); i=$((i + 1))
  done
  # breathing underneath
  for v in "${VOICES[@]}"; do
    set -- $v
    sox "$PANT" -r 44100 -c 1 "$TMP/voice$i.wav" trim "${TRIM_PANT[@]}" pitch "$1" pad "$2" 0 trim 0 "$DUR" norm -22
    layers+=("$TMP/voice$i.wav"); i=$((i + 1))
  done
  sox "$ROPE"  -r 44100 -c 1 "$TMP/rope.wav"  trim "${TRIM_ROPE[@]}"  trim 0 "$DUR" norm -17
  sox "$WATER" -r 44100 -c 1 "$TMP/water.wav" trim "${TRIM_WATER[@]}" trim 0 "$DUR" norm -20
  sox -m "${layers[@]}" "$TMP/rope.wav" "$TMP/water.wav" "$TMP/towpath.wav" fade t 0.2 "$DUR" 1.2 norm -3
  encode "$TMP/towpath.wav" towpath
}

oar() {
  local i=0 h m at layers=()
  for m in "${OAR_MEN[@]}"; do
    set -- $m
    local pitch=$1 slack=$2 level=$3 k=0
    for h in "${STROKES[@]}"; do
      local start=${GRUNT_STARTS[$(( (k + i) % ${#GRUNT_STARTS[@]} ))]}
      local again=${GRUNT_STARTS[$(( (k + i + 2) % ${#GRUNT_STARTS[@]} ))]}
      at=$(echo "$h + $slack" | bc)
      sox "$GRUNT" -r 44100 -c 1 "$TMP/og$i-$k.wav" trim "$start" 0.7 fade t 0.01 0 0.25 pitch "$pitch" pad "$at" 0 pad 0 "$OAR_DUR" trim 0 "$OAR_DUR" norm "$level"
      layers+=("$TMP/og$i-$k.wav")
      # the lean: every man grunts a second time, lower and longer
      at=$(echo "$h + $slack + $LEAN" | bc)
      sox "$GRUNT" -r 44100 -c 1 "$TMP/ol$i-$k.wav" trim "$again" 0.9 fade t 0.02 0 0.35 pitch "$((pitch - 150))" pad "$at" 0 pad 0 "$OAR_DUR" trim 0 "$OAR_DUR" norm "$((level - 1))"
      layers+=("$TMP/ol$i-$k.wav")
      k=$((k + 1))
    done
    i=$((i + 1))
  done
  # the gang on its own bus, squeezed so every pull hits hard
  sox -m "${layers[@]}" "$TMP/gang.wav" compand 0.01,0.15 -40,-40,-25,-12,0,-4 -2 norm "$GANG_LEVEL"
  local splashes=()
  # the blade takes the water a beat after the pull
  for h in "${STROKES[@]}"; do
    at=$(echo "$h + 0.25" | bc)
    sox "$PADDLE" -r 44100 -c 1 "$TMP/splash$i.wav" trim "$PADDLE_STROKE" 1.0 fade t 0.02 0 0.4 pad "$at" 0 pad 0 "$OAR_DUR" trim 0 "$OAR_DUR" norm -13
    splashes+=("$TMP/splash$i.wav"); i=$((i + 1))
  done
  sox "$OARS"  -r 44100 -c 1 "$TMP/oars.wav"  trim "${TRIM_OARS[@]}"  trim 0 "$OAR_DUR" norm -19
  sox "$WATER" -r 44100 -c 1 "$TMP/owater.wav" trim "${TRIM_WATER[@]}" trim 0 "$OAR_DUR" norm -21
  sox -m "$TMP/gang.wav" "${splashes[@]}" "$TMP/oars.wav" "$TMP/owater.wav" "$TMP/oar.wav" fade t 0.2 "$OAR_DUR" 1.2 norm -2
  encode "$TMP/oar.wav" oar
}

table() {
  local i=0 h layers=()
  for h in "${CLANKS[@]}"; do
    sox "$CLANK" -r 44100 -c 1 "$TMP/clank$i.wav" pad "$h" 0 pad 0 "$TABLE_DUR" trim 0 "$TABLE_DUR" norm -18
    layers+=("$TMP/clank$i.wav"); i=$((i + 1))
  done
  local d rooms=()
  for d in "${DINER_LAYERS[@]}"; do
    set -- $d
    sox "$DINERS" -r 44100 -c 1 "$TMP/room$i.wav" trim "$1" "$TABLE_DUR" pitch "$2" norm -12
    rooms+=("$TMP/room$i.wav"); i=$((i + 1))
  done
  sox -m "${rooms[@]}" "$TMP/diners.wav" lowpass 2200 reverb 35 60 70 channels 1 norm -12
  sox "$WATER"  -r 44100 -c 1 "$TMP/twater.wav" trim "${TRIM_WATER[@]}" trim 0 "$TABLE_DUR" norm -24
  sox -m "${layers[@]}" "$TMP/diners.wav" "$TMP/twater.wav" "$TMP/table.wav" fade t 0.4 "$TABLE_DUR" 1.2 norm -3
  encode "$TMP/table.wav" table
}

taxi() {
  local i=0 h layers=()
  sox "$CART"   -r 44100 -c 1 "$TMP/cart.wav"   trim "${TRIM_CART[@]}"   norm -8
  sox "$HOOVES" -r 44100 -c 1 "$TMP/hooves.wav" trim "${TRIM_HOOVES[@]}" pitch "$HOOVES_PITCH" norm -14
  for h in "${CART_CREAKS[@]}"; do
    sox "$ROPE" -r 44100 -c 1 "$TMP/ccreak$i.wav" trim "$ROPE_STRAIN" 0.7 fade t 0.03 0 0.3 pitch -300 pad "$h" 0 pad 0 "$TAXI_DUR" trim 0 "$TAXI_DUR" norm -17
    layers+=("$TMP/ccreak$i.wav"); i=$((i + 1))
  done
  local b
  for b in "${BRAYS[@]}"; do
    set -- $b
    sox "$DONKEY2" -r 44100 -c 1 "$TMP/bray$i.wav" trim "$1" "$2" fade t 0.03 0 0.4 pad "$3" 0 pad 0 "$TAXI_DUR" trim 0 "$TAXI_DUR" norm "$4"
    layers+=("$TMP/bray$i.wav"); i=$((i + 1))
  done
  sox -m "$TMP/cart.wav" "$TMP/hooves.wav" "${layers[@]}" "$TMP/taxi.wav" fade t 0.3 "$TAXI_DUR" 1.3 norm -3
  encode "$TMP/taxi.wav" taxi
}

relay() {
  local i=0 s layers=()
  for s in "${SLEEPERS[@]}"; do
    set -- $s
    sox "$SNORE" -r 44100 -c 1 "$TMP/sleep$i.wav" trim "$1" "$RELAY_DUR" pitch "$2" norm "$3"
    layers+=("$TMP/sleep$i.wav"); i=$((i + 1))
  done
  for s in "${SLEEPER2[@]}"; do
    set -- $s
    sox "$SNORE2" -r 44100 -c 1 "$TMP/sleep$i.wav" trim "$1" "$RELAY_DUR" pitch "$2" lowpass 3000 norm "$3"
    layers+=("$TMP/sleep$i.wav"); i=$((i + 1))
  done
  sox "$STICK" -r 44100 -c 1 "$TMP/spear.wav" trim "$STICK_HIT" 0.8 pad "$SPEAR_AT" 0 pad 0 "$RELAY_DUR" trim 0 "$RELAY_DUR" norm -12
  sox "$SPARROWS" -r 44100 -c 1 "$TMP/yard.wav" trim "${TRIM_SPARROWS[@]}" lowpass 5000 norm -24
  sox -m "${layers[@]}" "$TMP/spear.wav" "$TMP/yard.wav" "$TMP/relay.wav" fade t 0.4 "$RELAY_DUR" 1.3 norm -3
  encode "$TMP/relay.wav" relay
}

close-call() {
  local i=0 p layers=()
  # the shouting: crew close, bridge nearer than the far crowd, which is muffled to murmur
  sox "$CREW"   -r 44100 -c 1 "$TMP/crew.wav"   trim "${TRIM_CREW[@]}"   norm -9
  sox "$CREW"   -r 44100 -c 1 "$TMP/crew2.wav"  trim "${TRIM_CREW[@]}"   pitch -180 pad 0.07 0 trim 0 "$CALL_DUR" norm -13
  sox "$BRIDGE" -r 44100 -c 1 "$TMP/bridge.wav" trim "${TRIM_BRIDGE[@]}" pitch 80 norm -12
  sox "$RIOT"   -r 44100 -c 1 "$TMP/far.wav"    trim "${TRIM_RIOT[@]}"   lowpass 1800 reverb 30 50 80 channels 1 norm -16
  for p in "${POLE_CLATTERS[@]}"; do
    set -- $p
    sox "$PLANKS" -r 44100 -c 1 "$TMP/pole$i.wav" trim "$1" "$2" fade t 0.01 0 0.3 pad "$3" 0 pad 0 "$CALL_DUR" trim 0 "$CALL_DUR" norm -15
    layers+=("$TMP/pole$i.wav"); i=$((i + 1))
  done
  # the hit: the heaviest plank fall and a deepened hull bump land together
  sox "$PLANKS" -r 44100 -c 1 "$TMP/hit.wav"  trim "${HIT_PLANK[@]}" fade t 0 0 0.5 pitch -400 pad "$HIT_AT" 0 pad 0 "$CALL_DUR" trim 0 "$CALL_DUR" norm -7
  sox "$HULL"   -r 44100 -c 1 "$TMP/hull.wav" trim "$HIT_HULL" 1.2 fade t 0.01 0 0.5 pitch -600 pad "$HIT_AT" 0 pad 0 "$CALL_DUR" trim 0 "$CALL_DUR" norm -10
  sox "$ROPE"   -r 44100 -c 1 "$TMP/lines.wav" trim "${TRIM_ROPE[@]}" trim 0 "$CALL_DUR" norm -19
  sox "$RIVER"  -r 44100 -c 1 "$TMP/river.wav" trim "${TRIM_RIVER[@]}" norm -16
  sox -m "$TMP/crew.wav" "$TMP/crew2.wav" "$TMP/bridge.wav" "$TMP/far.wav" "${layers[@]}" "$TMP/hit.wav" "$TMP/hull.wav" "$TMP/lines.wav" "$TMP/river.wav" "$TMP/close-call.wav" fade t 0.3 "$CALL_DUR" 1.4 norm -2
  encode "$TMP/close-call.wav" close-call
}

ten-thousand() {
  sox "$BAMBOO" -r 44100 -c 1 "$TMP/gate.wav" trim "${TRIM_GATE[@]}" pitch "$GATE_PITCH" norm -14
  sox "$FLAG"   -r 44100 -c 1 "$TMP/banner.wav" trim 0 5 pad 0.5 0 pad 0 "$TAVERN_DUR" trim 0 "$TAVERN_DUR" norm -18
  sox "$DINERS" -r 44100 -c 1 "$TMP/leak.wav" trim "${TRIM_LEAK[@]}" lowpass 1500 reverb 30 50 70 channels 1 norm -16
  sox "$POUR"   -r 44100 -c 1 "$TMP/pour.wav" trim "${TRIM_POUR[@]}" fade t 0.05 0 0.3 pad "$POUR_AT" 0 pad 0 "$TAVERN_DUR" trim 0 "$TAVERN_DUR" norm -14
  sox "$JARLID" -r 44100 -c 1 "$TMP/jar.wav"  trim "${TRIM_JARLID[@]}" fade t 0.01 0 0.2 pad "$JAR_AT" 0 pad 0 "$TAVERN_DUR" trim 0 "$TAVERN_DUR" norm -14
  sox -m "$TMP/gate.wav" "$TMP/banner.wav" "$TMP/leak.wav" "$TMP/pour.wav" "$TMP/jar.wav" "$TMP/ten-thousand.wav" fade t 0.3 "$TAVERN_DUR" 1.3 norm -3
  encode "$TMP/ten-thousand.wav" ten-thousand
}

delivery() {
  local i=0 k layers=()
  sox "$SANDALS" -r 44100 -c 1 "$TMP/steps.wav" trim "${TRIM_SANDALS[@]}" tempo -s "$HURRY" pad 0 "$RUN_DUR" trim 0 "$RUN_DUR" norm -12
  for k in "${BOWL_KNOCKS[@]}"; do
    set -- $k
    sox "$BOWL" -r 44100 -c 1 "$TMP/bowl$i.wav" pitch "$2" pad "$1" 0 pad 0 "$RUN_DUR" trim 0 "$RUN_DUR" norm "$3"
    layers+=("$TMP/bowl$i.wav"); i=$((i + 1))
  done
  sox "$CLANK"  -r 44100 -c 1 "$TMP/pickup.wav" pad 0.15 0 pad 0 "$RUN_DUR" trim 0 "$RUN_DUR" norm -20
  sox "$DINERS" -r 44100 -c 1 "$TMP/street.wav" trim 16.0 "$RUN_DUR" lowpass 2500 norm -22
  sox -m "$TMP/steps.wav" "${layers[@]}" "$TMP/pickup.wav" "$TMP/street.wav" "$TMP/delivery.wav" fade t 0.2 "$RUN_DUR" 1.0 norm -3
  encode "$TMP/delivery.wav" delivery
}

right-of-way() {
  sox "$ARGUE" -r 44100 -c 1 "$TMP/party1.wav" trim "${TRIM_ARGUE[@]}" norm -10
  sox "$ARGUE" -r 44100 -c 1 "$TMP/party2.wav" trim "${TRIM_ARGUE[@]}" pitch 120 pad 0.4 0 trim 0 "$ROW_DUR" norm -14
  sox "$SNORT" -r 44100 -c 1 "$TMP/snort.wav" pad "$SNORT_AT" 0 pad 0 "$ROW_DUR" trim 0 "$ROW_DUR" norm -12
  sox "$HOOFWOOD" -r 44100 -c 1 "$TMP/planks.wav" trim "${TRIM_HOOFWOOD[@]}" norm -15
  sox "$RIOT"  -r 44100 -c 1 "$TMP/onlookers.wav" trim "${TRIM_FARCROWD[@]}" lowpass 1800 reverb 30 50 80 channels 1 norm -18
  sox -m "$TMP/party1.wav" "$TMP/party2.wav" "$TMP/snort.wav" "$TMP/planks.wav" "$TMP/onlookers.wav" "$TMP/right-of-way.wav" fade t 0.3 "$ROW_DUR" 1.3 norm -3
  encode "$TMP/right-of-way.wav" right-of-way
}

poles() {
  local i=0 h b layers=()
  sox "$WIND"   -r 44100 -c 1 "$TMP/wind.wav" trim "${TRIM_WIND[@]}" norm -10
  sox "$BAMBOO" -r 44100 -c 1 "$TMP/pole.wav" trim "${TRIM_POLE[@]}" pitch "$POLE_PITCH" norm -16
  for h in "${POLE_CREAKS[@]}"; do
    sox "$ROPE" -r 44100 -c 1 "$TMP/pcreak$i.wav" trim "$ROPE_STRAIN" 0.7 fade t 0.03 0 0.3 pad "$h" 0 norm -18
    layers+=("$TMP/pcreak$i.wav"); i=$((i + 1))
  done
  for b in "${POLE_BIRDS[@]}"; do
    set -- $b
    sox "$SPARROWS" -r 44100 -c 1 "$TMP/pbird$i.wav" trim "$1" "$2" pitch "$5" highpass 1800 lowpass 12000 fade t 0.008 0 0.045 norm "$4" pad "$3" 0
    layers+=("$TMP/pbird$i.wav"); i=$((i + 1))
  done
  sox "$RIVER" -r 44100 -c 1 "$TMP/below.wav" trim 10.0 "$POLES_DUR" norm -22
  sox -m "$TMP/wind.wav" "$TMP/pole.wav" "${layers[@]}" "$TMP/below.wav" "$TMP/poles.wav" fade t 0.4 "$POLES_DUR" 1.3 norm -3
  encode "$TMP/poles.wav" poles
}

rudder() {
  local i=0 h at layers=()
  for h in "${SWEEPS[@]}"; do
    # the pivot groans first, then the blade takes the water, and the boatman breathes out
    at=$(echo "$h - 0.15" | bc)
    sox "$ROPE"   -r 44100 -c 1 "$TMP/pivot$i.wav" trim "$ROPE_STRAIN" 0.9 fade t 0.03 0 0.4 pitch -500 pad "$at" 0 pad 0 "$SWEEP_DUR" trim 0 "$SWEEP_DUR" norm -13
    sox "$PADDLE" -r 44100 -c 1 "$TMP/blade$i.wav" trim "$PADDLE_STROKE" 1.3 fade t 0.02 0 0.5 pitch -350 pad "$h" 0 pad 0 "$SWEEP_DUR" trim 0 "$SWEEP_DUR" norm -11
    sox "$GRUNT"  -r 44100 -c 1 "$TMP/man$i.wav" trim "${GRUNT_STARTS[$((i % ${#GRUNT_STARTS[@]}))]}" 0.8 fade t 0.01 0 0.3 pitch -100 pad "$h" 0 pad 0 "$SWEEP_DUR" trim 0 "$SWEEP_DUR" norm -16
    layers+=("$TMP/pivot$i.wav" "$TMP/blade$i.wav" "$TMP/man$i.wav"); i=$((i + 1))
  done
  sox "$SWEEPWATER" -r 44100 -c 1 "$TMP/swirl.wav" trim "${TRIM_SWEEPWATER[@]}" norm -15
  sox "$OARS"  -r 44100 -c 1 "$TMP/hull.wav"  trim "${TRIM_OARS[@]}" trim 0 "$SWEEP_DUR" pitch -200 norm -20
  sox "$WATER" -r 44100 -c 1 "$TMP/rwater.wav" trim "${TRIM_WATER[@]}" trim 0 "$SWEEP_DUR" norm -22
  sox -m "${layers[@]}" "$TMP/swirl.wav" "$TMP/hull.wav" "$TMP/rwater.wav" "$TMP/rudder.wav" fade t 0.3 "$SWEEP_DUR" 1.3 norm -3
  encode "$TMP/rudder.wav" rudder
}

life-aboard() {
  local i=0 l h layers=()
  sox "$LAPPING" -r 44100 -c 1 "$TMP/lap.wav"  trim "${TRIM_LAPPING[@]}" norm -14
  sox "$FIRE"    -r 44100 -c 1 "$TMP/fire.wav" trim "${TRIM_FIRE[@]}" norm -18
  for l in "${LIDS[@]}"; do
    set -- $l
    sox "$POTLID" -r 44100 -c 1 "$TMP/lid$i.wav" trim "$1" "$2" fade t 0.01 0 0.3 pad "$3" 0 pad 0 "$HOME_DUR" trim 0 "$HOME_DUR" norm "$4"
    layers+=("$TMP/lid$i.wav"); i=$((i + 1))
  done
  for h in "${MOORING_CREAKS[@]}"; do
    sox "$ROPE" -r 44100 -c 1 "$TMP/moor$i.wav" trim "$ROPE_STRAIN" 0.8 fade t 0.03 0 0.4 pitch -200 pad "$h" 0 pad 0 "$HOME_DUR" trim 0 "$HOME_DUR" norm -19
    layers+=("$TMP/moor$i.wav"); i=$((i + 1))
  done
  sox "$ROPE" -r 44100 -c 1 "$TMP/timbers.wav" trim "${TRIM_ROPE[@]}" trim 0 "$HOME_DUR" pitch -200 norm -22
  sox -m "$TMP/lap.wav" "$TMP/fire.wav" "${layers[@]}" "$TMP/timbers.wav" "$TMP/life-aboard.wav" fade t 0.5 "$HOME_DUR" 1.4 norm -3
  encode "$TMP/life-aboard.wav" life-aboard
}

mkdir -p "$OUT"
[ $# -gt 0 ] || set -- donkey towpath oar table taxi relay close-call ten-thousand delivery right-of-way poles rudder life-aboard
for clip in "$@"; do "$clip"; done
