Completed local-only changes.
- 90 normal-motion lifecycle browser checks; 2350 sampled entrance/inside frames; zero inactive-painting visibility incidents. Desktop 1440x900 and mobile390x844, alternating paintings and interrupted entry.
- 682 current real-app UI/audio checks passed: all22 playback starts, cards, navigation, positions, desktop/mobile320/390/1440, touch and keyboard event logic, cleanup, mute and Qingming regressions. Physical-device/audio-speaker listening is separate.
- 14 Node checks passed, including deferred-image completion after interrupted entry.
- 22 Ogg assets: mono gated loudness -24.97..-24.44 LUFS including .8 playback; all WAV fallbacks matched within .2 LU, peaks below -3dBFS at playback, <=8s.
- Original artwork/audio binary hash verification passed (excluding the intentionally updated source-credit document).
- Build and git diff --check passed. Final localhost gallery and office screenshots inspected.
Errors resolved: initial audio mix mismatched source sample rates; convert both stems to48k mono. First fallback codec comparison exceeded .8LU; add format-specific gain matching. Async test read initially placed in a synchronous callback; marked callback async. Hash check initially included intentionally modified SOURCE.md; scoped preservation check to original binaries.
