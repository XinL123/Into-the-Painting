Latest requested behavior: gallery background music only. Both projects suspend music on entry; only scene foley plays inside. Unmuting scene audio does not restart background music. Resume music after the leave transition has fully returned to gallery, respecting shared manual mute.

11 browser checks passed across Gusu/Qingming, including scene sound, unmute, return and manual mute. Seven Node audio/lifecycle tests passed, Vite build888ms, git diff --check clean. Prior continuous-inside-music expectation is superseded. Local only.
