#!/bin/sh
# Gallery music: the audio of the videos in music/ (local only) as 96 kbps AAC.
set -e
cd "$(dirname "$0")/.."
mkdir -p assets/music
afconvert -f m4af -d aac -b 96000 -q 127 "music/琵琶语.MP4"   assets/music/pipa-yu.m4a
afconvert -f m4af -d aac -b 96000 -q 127 "music/双面燕询.mov" assets/music/shuangmian-yanxun.m4a
afconvert -f m4af -d aac -b 96000 -q 127 "music/苏州听雨.MP4" assets/music/suzhou-tingyu.m4a
# Optional fourth source: scripts/prep-music.sh /path/to/望月之城.mov
if [ -n "${1:-}" ]; then
  afconvert -f m4af -d aac -b 96000 -q 127 "$1" assets/music/wangyue-zhi-cheng.m4a
fi
ls -la assets/music
