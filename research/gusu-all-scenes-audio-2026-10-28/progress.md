Completed locally: 22/22 Gusu scenes have sound, with22 unique audio files and14 new clips.
- Prior8 clips/gains, painting assets, scene anchors, spatial navigation, all approved stories and all Qingming files unchanged.
- 9 additional CC0 recordings verified on recordist pages; source URL, preview URL, license and SHA256 stored. Existing CC0 archive supplies the remaining foley.
- Reproducible processing in scripts/prep-gusu-all-scenes.py. All22 WAVs verified unique,5–7seconds, nonzero RMS and ample peak headroom. New clips have conservative scene gains and fades.
- 84 real-browser interaction checks passed: all22 AudioBufferSource starts/decode paths, all22 Gusu cards and13 Qingming cards, spatial navigation, touch/pinch/wheel, mute, card-close stopping and exit cleanup.
- 5 core tests passed. Build and git diff --check passed.
- Updated audition page has22 native audio controls, one-at-a-time playback, stop, and sequential audition. Direct UI test progressed automatically from01 to05; stop paused all22 players. Preview screenshot visually checked.
- Historical boundaries documented: modern hand-loom, instrument, nature and object recordings are illustrative, not claims about exact Qing-era sounds, species or specific instruments in the painting. In particular pond frogs and temple bell originate outside China, explicitly documented.
- All previously hashed asset/source files unchanged except expected Gusu stories.js sound mappings and sound/SOURCE.md provenance.
- No commit, push, publish or deployment.
