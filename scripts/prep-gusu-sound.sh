#!/usr/bin/env bash
# Modern ambient illustrations from existing CC0 sources, no voices or invented period music.
set -euo pipefail
cd "$(dirname "$0")/.."
workdir=$(mktemp -d)
trap 'rm -rf "$workdir"' EXIT
sox assets/sound/raw/628949_3311539-hq.ogg -r 44100 -c 2 "$workdir/gusu-birds.wav" trim 0 6 highpass 1200 lowpass 12000 gain -n -9 fade t 0.15 6 0.6
sox assets/sound/raw/318064_4457609-hq.ogg -r 44100 -c 2 "$workdir/gusu-water.wav" trim 8 6 gain -n -6 fade t 0.2 6 0.6
for name in gusu-birds gusu-water; do
 sox "$workdir/$name.wav" -C 5 "assets/sound/$name.ogg"
 sox "$workdir/$name.wav" -r 22050 -c 1 -b 16 "assets/sound/$name.wav"
done
