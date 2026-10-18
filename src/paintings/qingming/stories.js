// Small stories hidden in the chosen stretch of 清明上河图.
// box = [left, top, right, bottom] in master pixels of the Song scroll
// (assets/paintings/qingming/master). An optional `spot` shapes the spotlight:
// { angle } in degrees (clockwise on screen), { rx, ry } radii in master px.
// An optional `sound` plays while the moment is looked at: { file } names a
// clip in assets/sound/, mode 'once' (plays through) or 'loop' (until closed).
// Readings that scholars dispute are phrased as readings, not facts.
export const stories = [
  {
    id: 'taxi',
    title: 'A Song-Dynasty \u201cTaxi\u201d?',
    box: [7960, 1050, 9060, 1320],
    sound: { file: 'taxi', mode: 'once', gain: 0.8 },
    text: [
      'A young woman in a veiled hat rides out of the city while a heavily loaded chuanche travels ahead of her.',
      'One interpretation suggests these hired carts worked near the docks, carrying travelers\u2019 luggage \u2014 a little like an early urban transport service.',
    ],
  },
  {
    id: 'relay',
    title: 'Waiting for the Next Dispatch?',
    box: [11330, 300, 11980, 720],
    sound: { file: 'relay', mode: 'once', gain: 0.8 },
    text: [
      'Outside this official compound, nine uniformed men wait with spears nearby \u2014 and several appear to have fallen asleep.',
      'One interpretation identifies the site as a relay station, part of the Song government\u2019s system for carrying official messages by foot and horse.',
    ],
  },
  {
    id: 'farewell',
    title: 'Seeing a Friend Off',
    box: [13230, 820, 13660, 1050],
    sound: { file: 'donkey', mode: 'once' },
    text: [
      'Outside a shop near the edge of town, a saddled donkey waits while a group of men bow their goodbyes. One of them is about to mount and go.',
      'Donkeys could be hired in Song Kaifeng much as taxis are today, so the scene reads as a farewell at the start of a journey.',
      'It fits a scroll whose far end opens onto open country.',
    ],
  },
  {
    id: 'ten-thousand',
    title: 'The Ten-Thousand-Cash Tavern',
    box: [16980, 1420, 17230, 1745],
    sound: { file: 'ten-thousand', mode: 'once', gain: 0.7 },
    text: [
      'The sign reads 十千脚店, “Ten Thousand Jiaodian”. It is not an address, and not a price.',
      'A jiaodian was a licensed tavern that bought its wine from one of the capital’s great breweries, and “ten thousand cash” was a poet’s phrase for wine too fine to afford.',
      'The tower of bamboo lattice over the door is a “welcoming gate”, the way a Kaifeng wine house announced itself from streets away.',
    ],
  },
  {
    id: 'delivery',
    title: 'A Song-Dynasty Delivery Runner?',
    box: [17380, 1540, 17560, 1745],
    sound: { file: 'delivery', mode: 'once', gain: 0.8 },
    text: [
      'Outside the tavern a waiter in an apron hurries off with two bowls balanced in one hand and a food box in the other.',
      'Twelfth-century accounts of Kaifeng describe restaurants that would send dishes out to homes and offices on request.',
      'Whether this man is on such an errand the painter does not say, but modern viewers have claimed him as the scroll’s delivery rider.',
    ],
  },
  {
    id: 'right-of-way',
    title: 'Who Gets to Cross First?',
    box: [18620, 160, 19250, 590],
    sound: { file: 'right-of-way', mode: 'once', gain: 0.8 },
    spot: { angle: -31, rx: 470, ry: 170 },
    text: [
      'At the crest of Rainbow Bridge, a rider and a sedan-chair party meet head-on. Their attendants appear to be arguing over who should give way.',
      'One common interpretation identifies them as a military official on horseback and a civil official in the chair \u2014 turning a tiny traffic jam into one of the scroll’s liveliest confrontations.',
    ],
  },
  {
    id: 'poles',
    title: 'What Were These Bridge Poles For?',
    box: [18960, 610, 19050, 970],
    sound: { file: 'poles', mode: 'once', gain: 0.7 },
    text: [
      'At the ends of Rainbow Bridge stand tall poles topped with small bird-shaped ornaments.',
      'Their purpose is still debated. They have often been interpreted as wind indicators for boatmen, while another interpretation suggests they were huabiao \u2014 architectural markers associated with the bridge. Their exact function remains uncertain.',
    ],
  },
  {
    id: 'close-call',
    title: 'Close Call Under the Bridge',
    box: [19520, 300, 20420, 640],
    sound: { file: 'close-call', mode: 'once', gain: 0.8 },
    text: [
      'The scroll’s most dramatic moment is a traffic accident. A heavy barge has been caught by the current with its mast still raised.',
      'Men on deck strain to lower it, a sailor leans out with a pole, and the crowd on the bridge shouts and throws down ropes.',
      'Some historians read scenes like this as the painter’s quiet warning: a prosperous capital whose river traffic had outgrown its care.',
    ],
  },
  {
    id: 'towpath',
    title: 'Five Men and a Rope',
    box: [21750, 110, 22300, 360],
    sound: { file: 'towpath', mode: 'once', gain: 0.8 },
    text: [
      'Upstream of the bridge five men lean into a long rope, hauling a loaded boat against the current from the towpath.',
      'On the Bian River, which carried grain to the capital from the south, boats were towed for miles this way.',
      'Each man is drawn with a few lines, yet you can feel the weight on the rope.',
    ],
  },
  {
    id: 'rudder',
    title: 'A Giant Oar at the Stern?',
    box: [22290, 450, 22560, 630],
    sound: { file: 'rudder', mode: 'once', gain: 0.8 },
    text: [
      'This long sweep at the stern was worked by a boatman to help maneuver the vessel.',
      'The scroll records boat technology in remarkable detail \u2014 including both large stern sweeps like this and more compact rudders on other vessels.',
    ],
  },
  {
    id: 'oar',
    title: 'Eight Men, One Oar',
    box: [21970, 790, 22430, 975],
    sound: { file: 'oar', mode: 'once', gain: 0.8 },
    text: [
      'A small boat at the bank carries eight men crowded onto a single great sweep oar.',
      'Oars like this, worked by a team, steered and drove boats on stretches of river where sails were no use.',
      'It is one of the scroll’s many group portraits: eight faces, eight postures, nobody standing still.',
    ],
  },
  {
    id: 'table',
    title: 'Dinner Above the River?',
    box: [22840, 240, 23540, 600],
    sound: { file: 'table', mode: 'once', gain: 0.7 },
    text: [
      'Near the river, this open-sided restaurant sits on a raised platform above the bank. Diners can be seen upstairs, looking out over the busy waterfront.',
      'Riverside restaurants like this turned the riverfront into more than a transport hub — it was also a place to eat, rest, and watch the city go by.',
    ],
  },
  {
    id: 'life-aboard',
    title: 'A Home on the River?',
    box: [23780, 790, 24580, 1050],
    sound: { file: 'life-aboard', mode: 'once', gain: 0.7 },
    text: [
      'On this moored boat, one person leans from the cabin while another sits above among baskets and bedding.',
      'For crews traveling long distances along the Bian River, a boat could be more than transportation — it could also be a place to cook, rest, and sleep.',
      'For some, life on the river was also life at home.',
    ],
  },
];
