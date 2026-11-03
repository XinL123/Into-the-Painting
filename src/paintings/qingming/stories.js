// User-approved copy, 2026-10-26; earlier claim audit recorded below.
// Per-claim evidence and original wording: research/qingming-audit/AUDIT.md.
// box = [left, top, right, bottom] in pixels of the unaltered Song-scroll master.
// Optional spot shapes the spotlight; sound names a modern interpretive audio clip.
// Visual observations, historical context and attributed readings are kept distinct.
export const stories = [
  {
    id: 'taxi',
    title: 'One Wheel, Quite a Load',
    box: [7960, 1050, 9060, 1320],
    sound: { file: 'taxi', mode: 'once', gain: 0.8 },
    text: [
      'One wheel, one donkey, and two people working together to move a very heavy load!',
      'This is a *chuanche* (串车), a type of single-wheeled cart used in Song-era China. And here\'s a little detail: can you spot the large handwritten characters on its cover?',
    ],
  },
  {
    id: 'relay',
    title: 'Taking a Break on Official Business?',
    box: [11330, 300, 11980, 720],
    sound: { file: 'relay', mode: 'once', gain: 0.8 },
    text: [
      'These men are lounging beside boxes and weapons. Not exactly a picture of urgency, is it?',
      'Art historian Yu Hui interprets this as a government relay post, where official documents were passed along. If he\'s right, the paperwork seems to be moving rather slowly.',
    ],
  },
  {
    id: 'farewell',
    title: 'A Long Goodbye?',
    box: [13230, 820, 13660, 1050],
    sound: { file: 'donkey', mode: 'once' },
    text: [
      'A saddled donkey is waiting, but the people beside it are still exchanging farewell-like gestures.',
      'Could someone be leaving on a journey? The donkey seems ready to go. The humans, perhaps not quite yet.',
    ],
  },
  {
    id: 'ten-thousand',
    title: 'Poetry on a Wine Shop Sign?',
    box: [16980, 1420, 17230, 1745],
    sound: { file: 'ten-thousand', mode: 'once', gain: 0.7 },
    text: [
      'Look for the characters 十千脚店 (*Shiqian Jiaodian*). The words *shiqian*, meaning "ten thousand," echo an old poetic expression for fine wine—not necessarily a price tag!',
      'And that fancy entrance? It\'s a *huanmen*, a decorative gateway. Even Song-era wine shops knew how to catch your eye.',
    ],
  },
  {
    id: 'delivery',
    title: 'Takeout, Song-Style?',
    box: [17380, 1540, 17560, 1745],
    sound: { file: 'delivery', mode: 'once', gain: 0.8 },
    text: [
      'Small dishes in one hand, a container in the other. This man looks like he\'s on a mission!',
      'Here\'s a fun fact: according to the *Dongjing Meng Hua Lu*, some Kaifeng residents regularly bought prepared meals instead of cooking at home.',
      'Early takeout vibes? Perhaps. Where this man is heading, though, remains a mystery.',
    ],
  },
  {
    id: 'right-of-way',
    title: 'Who Gets to Cross First?',
    box: [18620, 160, 19250, 590],
    sound: { file: 'right-of-way', mode: 'once', gain: 0.8 },
    spot: { angle: -31, rx: 470, ry: 170 },
    text: [
      'A rider and a sedan-chair party meet on the busy bridge. Judging by the gestures, neither side seems eager to give way.',
      'Art historian Yu Hui interprets this as a dispute between military and civil officials. Traffic drama, long before cars!',
    ],
  },
  {
    id: 'poles',
    title: 'A Bird with a Job?',
    box: [18960, 610, 19050, 970],
    sound: { file: 'poles', mode: 'once', gain: 0.7 },
    text: [
      'See that bird perched on top of a tall pole?',
      'Some researchers believe the structure helped boatmen read the wind. Others identify it as a *huabiao*, an architectural marker for the bridge.',
      'One little bird, two very different job descriptions. Scholars are still debating which is right!',
    ],
  },
  {
    id: 'close-call',
    title: 'Mind the Mast!',
    box: [19520, 300, 20420, 640],
    sound: { file: 'close-call', mode: 'once', gain: 0.8 },
    text: [
      'A big boat, a low bridge, and one rather inconvenient mast.',
      'The crew is lowering the mast to squeeze beneath Rainbow Bridge, while curious spectators lean over the railings to watch.',
      'The mast can come down. The bridge? Not so much.',
    ],
  },
  {
    id: 'towpath',
    title: 'Five Men and a Rope',
    box: [21750, 110, 22300, 360],
    sound: { file: 'towpath', mode: 'once', gain: 0.8 },
    text: [
      'Did you know boats could be pulled from the riverbank?',
      'These five men are hauling a *towline*, using their own strength to move a vessel through the water.',
      'No engine, just a rope and some serious teamwork. Quite the workout!',
    ],
  },
  {
    id: 'rudder',
    title: 'A Rudder That Can Rise',
    box: [22290, 450, 22560, 630],
    sound: { file: 'rudder', mode: 'once', gain: 0.8 },
    text: [
      'Here\'s some clever Song-era engineering!',
      'The boats in this scroll feature *balanced rudders*, designed to make steering easier. They could also be raised when the water became too shallow.',
      'A handy way to avoid an unfortunate meeting with the riverbed!',
    ],
  },
  {
    id: 'oar',
    title: 'Eight Men, One Giant Oar',
    box: [21970, 790, 22430, 975],
    sound: { file: 'oar', mode: 'once', gain: 0.8 },
    text: [
      'Count the men working around this enormous *sweep oar*. There are eight!',
      'Large sweeps like this could require six to eight people to operate, helping propel a boat through the water.',
      'Apparently, rowing wasn\'t always a solo activity. This was a group project.',
    ],
  },
  {
    id: 'table',
    title: 'A Table with a River View',
    box: [22840, 240, 23540, 600],
    sound: { file: 'table', mode: 'once', gain: 0.7 },
    text: [
      'A few tables, some seated guests, and boats passing just below.',
      'This raised, open-sided building may have been a place to eat or drink beside the river.',
      'If so, the waterfront view came with a little live entertainment: all that passing boat traffic!',
    ],
  },
  {
    id: 'life-aboard',
    title: 'A Little Downtime Afloat',
    box: [23780, 790, 24580, 1050],
    sound: { file: 'life-aboard', mode: 'once', gain: 0.7 },
    text: [
      'The Bian River was a major transportation route serving the Song capital. But not every moment aboard was about moving cargo.',
      'Look closely: someone peers out from the cabin while others pause among baskets and bundles.',
      'Even one of the busiest waterways had its quieter corners.',
    ],
  },
];
