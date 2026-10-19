// A hanging scroll over the gallery: why the work exists, what it is made of,
// whose it is. It unrolls from its top rod, and rolls back up when closed.
export function createAbout(root) {
  const about = root.querySelector('.about');
  const opener = root.querySelector('.about-open');
  const paper = about.querySelector('.scroll-paper');
  let open = false;
  let hideTimer = 0;

  function show() {
    if (open) return;
    open = true;
    clearTimeout(hideTimer);
    about.hidden = false;
    paper.scrollTop = 0;
    // next frame, so the unroll transitions from the rolled-up state
    requestAnimationFrame(() => requestAnimationFrame(() => {
      about.classList.add('is-open');
      about.querySelector('.about-close').focus({ preventScroll: true });
    }));
  }

  function hide() {
    if (!open) return;
    open = false;
    about.classList.remove('is-open');
    hideTimer = setTimeout(() => { if (!open) about.hidden = true; }, 900);
    opener.focus({ preventScroll: true });
  }

  opener.addEventListener('click', show);
  about.querySelector('.about-close').addEventListener('click', hide);
  about.querySelector('.about-veil').addEventListener('click', hide);

  return { show, hide, get open() { return open; } };
}
