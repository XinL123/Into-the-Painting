// The gallery's paintings. Only Along the River can be entered; the others are
// shown and credited but are not interactive yet.
// Provenance for each: assets/paintings/<id>/SOURCE.md
import stretch from '../../assets/paintings/qingming/stretch/stretch.json';
import { stories } from './qingming/stories.js';

const stretchFiles = import.meta.glob('../../assets/paintings/qingming/stretch/{web,details}/*.webp', {
  eager: true, query: '?url', import: 'default',
});
const stretchUrl = (rel) => stretchFiles[`../../assets/paintings/qingming/stretch/${rel}`];

const gallery = import.meta.glob('../../assets/paintings/*/web/*.webp', {
  eager: true, query: '?url', import: 'default',
});
const galleryUrl = (id) => gallery[`../../assets/paintings/${id}/web/${id}.webp`];

const brushes = import.meta.glob('../../assets/ui/brush/*.webp', {
  eager: true, query: '?url', import: 'default',
});
const brushUrl = (name) => brushes[`../../assets/ui/brush/${name}.webp`];

const CMA = 'The Cleveland Museum of Art';
const bridgeX = 19875;   // master x of the Rainbow Bridge's crown

export const paintings = [
  {
    id: 'muqi-dragon',
    title: { en: 'Dragon', zh: '龙图' },
    artist: { en: 'Muqi (Fachang)', zh: '牧谿' },
    period: { en: 'Southern Song, c. 1250–79', zh: '南宋' },
    collection: { en: CMA },
    credit: 'CC0',
    image: galleryUrl('muqi-dragon'),
    brush: brushUrl('brush-dragon'),
    place: { x: 13, y: 24, w: 11, h: 52, rotate: -1.2 },
    position: '50% 20%',
  },
  {
    id: 'juran-retreat',
    title: { en: 'Buddhist Retreat by Stream and Mountains', zh: '溪山兰若图' },
    artist: { en: 'Juran', zh: '巨然' },
    period: { en: 'Northern Song, 960–85', zh: '北宋' },
    collection: { en: CMA },
    credit: 'CC0',
    image: galleryUrl('juran-retreat'),
    brush: brushUrl('brush-juran'),
    place: { x: 28.2, y: 21, w: 11.4, h: 56, rotate: 1 },
    position: '50% 30%',
  },
  {
    id: 'qingming',
    live: true,
    title: { en: 'Along the River During the Qingming Festival', zh: '清明上河图' },
    artist: { en: 'Zhang Zeduan', zh: '张择端' },
    period: { en: 'Northern Song, early 12th century', zh: '北宋' },
    collection: { en: 'Palace Museum, Beijing' },
    credit: 'Image: Wikimedia Commons, public domain',
    brush: brushUrl('brush-qingming'),
    place: { x: 43.6, y: 17, w: 12.8, h: 63 },
    scene: {
      width: stretch.width,
      height: stretch.height,
      rect: stretch.rect,
      focus: { x: (bridgeX - stretch.rect.left) / stretch.width, y: 0.5 },
      flat: stretch.web.map((f) => ({ url: stretchUrl(f.file), width: f.width })),
      details: Object.fromEntries(
        Object.entries(stretch.details).map(([id, d]) => [id, { url: stretchUrl(d.file), rect: d.rect }]),
      ),
      stories,
    },
  },
  {
    id: 'cloudy-mountains',
    title: { en: 'Cloudy Mountains', zh: '云山图' },
    artist: { en: 'Mi Youren', zh: '米友仁' },
    period: { en: 'Southern Song, 1130', zh: '南宋' },
    collection: { en: CMA },
    credit: 'CC0',
    image: galleryUrl('cloudy-mountains'),
    brush: brushUrl('brush-cloudy'),
    place: { x: 60.2, y: 22.5, w: 11.2, h: 54, rotate: -1.4 },
    position: '37% 50%',
  },
  {
    id: 'peach-birds',
    title: { en: 'Birds on a Peach Branch', zh: '桃枝双鸟图' },
    artist: { en: 'Unidentified artist', zh: '佚名' },
    period: { en: 'Southern Song, 12th century', zh: '南宋' },
    collection: { en: CMA },
    credit: 'CC0',
    image: galleryUrl('peach-birds'),
    brush: brushUrl('brush-birds'),
    place: { x: 75.6, y: 20.5, w: 11.2, h: 55, rotate: 1.6 },
    position: '17% 50%',
  },
];

export const livePainting = paintings.find((p) => p.live);
