// Three direct gallery controls; no opener or popover.
export function createMusicPlayer(root, music) {
  const panel = root.querySelector('.music-player');
  const play = panel.querySelector('.music-play');
  function refresh() {
    const s = music.state();
    const playing = s.on && !s.blocked && !s.paused && !s.suspended;
    play.classList.toggle('is-playing', playing);
    play.setAttribute('aria-label', playing ? 'Pause music' : 'Play music');
    for (const button of panel.querySelectorAll('.music-transport button')) button.disabled = !s.count;
  }
  panel.querySelector('.music-previous').addEventListener('click', () => music.previous());
  panel.querySelector('.music-next').addEventListener('click', () => music.next());
  play.addEventListener('click', () => {
    const s = music.state();
    if (s.on && !s.blocked && !s.paused) music.pause(); else music.play();
  });
  refresh();
  return { refresh };
}
