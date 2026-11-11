// Edge-aware framing for the shorter Gusu scan. Bounds stay in original pixels.
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
export function sceneFrame({ box, width, height, vw, vh, rest, cardHeight = 280, cardBottom = 64, maxZoom = 1.25, share }) {
  const [x0, y0, x1, y1] = box;
  const mobile = vw <= 800;
  const top = 72;
  const bottom = mobile ? Math.max(top + 110, vh - Math.min(cardHeight, vh * 0.45) - cardBottom - 24) : vh - 65;
  const side = mobile ? 'bottom' : ((x0 + x1) / 2 * rest.s + rest.x > vw / 2 ? 'left' : 'right');
  // A wide scene may claim more of the window than the usual 43% beside the card.
  const wide = !mobile && share ? share : null;
  const availableWidth = vw * (mobile ? 0.86 : wide ?? 0.43);
  const s = Math.min(maxZoom, availableWidth / (x1 - x0), (bottom - top) * 0.88 / (y1 - y0));
  const px = mobile ? vw / 2 : wide ? vw * (side === 'right' ? wide / 2 + 0.03 : 0.97 - wide / 2)
    : vw * (side === 'right' ? 0.28 : 0.72);
  const cx = (x0 + x1) / 2, cy = (y0 + y1) / 2;
  return {
    side,
    x: clamp(px - cx * s, Math.min(0, vw - width * s), Math.max(0, vw - width * s)),
    y: clamp((top + bottom) / 2 - cy * s, Math.min(top, bottom - height * s), Math.max(top, bottom - height * s)),
    s, top, bottom,
  };
}
