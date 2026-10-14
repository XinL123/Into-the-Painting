// The gallery: paintings seen through brushed openings. The artwork is the navigation.
const el = (tag, cls, text) => {
  const n = document.createElement(tag);
  if (cls) n.className = cls;
  if (text != null) n.textContent = text;
  return n;
};

// Smallest file that still covers `cssWidth` at this screen density.
export function pickFile(files, cssWidth) {
  const need = cssWidth * Math.min(devicePixelRatio, 2);
  const sorted = [...files].sort((a, b) => a.width - b.width);
  return sorted.find((f) => f.width >= need) ?? sorted.at(-1);
}

export function createGallery(root, paintings, { onEnter }) {
  const sheet = root.querySelector('.sheet');
  let live;

  paintings.forEach((p, i) => {
    const opening = el(p.live ? 'button' : 'div', `opening ${p.live ? 'opening--live' : 'opening--locked'}`);
    if (p.live) {
      opening.type = 'button';
      opening.setAttribute('aria-label', `${p.title.en}: enter the painting`);
    } else {
      opening.setAttribute('aria-label', `${p.title.en}: not yet open`);
    }
    const { x, y, w, h, rotate = 0 } = p.place;
    opening.style.cssText = `left:${x}%;top:${y}%;width:${w}%;height:${h}%;--rotate:${rotate}deg;--i:${i}`;

    const ink = el('span', 'opening-ink');
    ink.style.setProperty('--brush', `url("${p.brush}")`);
    const img = el('img', 'opening-image');
    img.alt = '';
    img.draggable = false;
    img.decoding = 'async';
    if (p.live) {
      img.src = pickFile(p.scene.flat, innerWidth * 1.2).url; // also serves the expand
    } else {
      img.src = p.image;
      img.style.objectPosition = p.position ?? '50% 50%';
    }
    ink.append(img);

    // the painting's name, shown beneath its stroke while it is being looked at
    const name = el('span', 'opening-name');
    name.append(
      el('span', 'opening-name-zh', p.title.zh),
      el('span', 'opening-name-by', `${p.period.zh} · ${p.artist.zh}`),
      el('span', 'opening-name-en', p.title.en),
    );
    opening.append(ink, name);
    if (!p.live) {
      const lock = el('span', 'opening-lock');
      lock.setAttribute('aria-hidden', 'true');
      lock.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.15" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="10.5" width="14" height="10" rx="1.4"/><path d="M8.2 10.5V7.6a3.8 3.8 0 0 1 7.6 0v2.9"/><circle cx="12" cy="15.3" r="1" fill="currentColor" stroke="none"/></svg>';
      opening.append(lock);
    }
    sheet.append(opening);
    if (p.live) live = { opening, ink, img, painting: p };
  });

  // The live opening shows the scene itself, framed on the bridge. Its image is
  // laid out here (not with object-fit) so the enter transition can carry the
  // very same element from this frame to the full view.
  function layoutLive() {
    const { ink, img, painting } = live;
    const { width: W, height: H, focus } = painting.scene;
    const bw = ink.clientWidth;
    const bh = ink.clientHeight;
    const s = Math.max(bw / W, bh / H) * 1.04;
    const w = W * s;
    const h = H * s;
    const left = Math.min(0, Math.max(bw - w, bw / 2 - focus.x * w));
    const top = Math.min(0, Math.max(bh - h, (bh - h) / 2));
    Object.assign(img.style, { left: `${left}px`, top: `${top}px`, width: `${w}px`, height: `${h}px` });
  }

  live.opening.addEventListener('click', () => onEnter(live));
  addEventListener('resize', () => {
    if (!root.classList.contains('is-inside')) layoutLive();
  });

  layoutLive();
  requestAnimationFrame(() => root.classList.add('is-ready'));

  return { live, layoutLive };
}
