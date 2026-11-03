#!/usr/bin/env bash
# Additional CC0 scene illustrations. Never rewrites Qingming or the original Gusu clips.
set -euo pipefail
cd "$(dirname "$0")/.."
workdir=$(mktemp -d)
trap 'rm -rf "$workdir"' EXIT
raw=assets/sound/raw
sox "$raw/637558_612689-hq.ogg" "$workdir/gusu-market-steps.wav" trim 1.5 5 highpass 100 gain -n -8 fade t .15 5 .6
sox "$raw/109485_1213320-hq.ogg" "$workdir/gusu-courtyard-wind.wav" trim 64 6 highpass 150 lowpass 5000 gain -n -14 fade t .5 6 1
sox "$raw/506688_10949426-hq.ogg" "$workdir/gusu-dock.wav" trim 1 6 highpass 80 gain -n -10 fade t .3 6 .8
sox "$raw/770039_13973196-hq.ogg" "$workdir/gusu-tea-pour.wav" trim 2 4.8 highpass 200 gain -n -9 fade t .15 4.8 .6
sox "$raw/249707_300738-hq.ogg" "$workdir/gusu-paddle.wav" trim 10 6 highpass 100 gain -n -10 fade t .3 6 .8
sox "$raw/335891_2792951-hq.ogg" "$workdir/gusu-bamboo.wav" trim 85 6 highpass 150 lowpass 6500 gain -n -12 fade t .4 6 1
for name in gusu-market-steps gusu-courtyard-wind gusu-dock gusu-tea-pour gusu-paddle gusu-bamboo; do
 sox "$workdir/$name.wav" -r 44100 -c 2 -C 5 "assets/sound/$name.ogg"
 sox "$workdir/$name.wav" -r 22050 -c 1 -b 16 "assets/sound/$name.wav"
done
