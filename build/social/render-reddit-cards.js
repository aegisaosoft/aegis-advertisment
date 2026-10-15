/*
 * Render reddit-card.html to the PNGs the Reddit campaign uses:
 *   social/reddit-card-<turo|fleet>-<wide|square>.png      (English)
 *   social/reddit-card-<turo|fleet>-<wide|square>-es.png   (Spanish)
 *
 *   node render-reddit-cards.js
 *
 * Same browser as short45/render.js: Playwright's headless shell is the only one that
 * starts under puppeteer on this machine.
 */
const path = require('path');
const { pathToFileURL } = require('url');

const ROOT = 'C:\\aegis-aa';
const puppeteer = require(path.join(ROOT, 'node_modules', 'puppeteer-core'));
const CHROME = 'C:\\Users\\Alexander\\AppData\\Local\\ms-playwright\\chromium_headless_shell-1208' +
  '\\chrome-headless-shell-win64\\chrome-headless-shell.exe';

const PAGE = pathToFileURL(path.join(__dirname, 'reddit-card.html')).href;
const OUT = path.join(__dirname, '..', '..', 'social');
const SIZES = { wide: [1200, 628], square: [1080, 1080] };

(async () => {
  const browser = await puppeteer.launch({ executablePath: CHROME, headless: true });
  try {
    const page = await browser.newPage();
    for (const lang of ['en', 'es']) for (const v of ['turo', 'fleet']) {
      for (const [shape, [width, height]] of Object.entries(SIZES)) {
        await page.setViewport({ width, height, deviceScaleFactor: 1 });
        await page.goto(`${PAGE}?v=${v}&shape=${shape}&lang=${lang}`, { waitUntil: 'networkidle0' });
        await page.evaluate(() => document.fonts.ready);
        const suffix = lang === 'en' ? '' : `-${lang}`;
        const file = path.join(OUT, `reddit-card-${v}-${shape}${suffix}.png`);
        await page.screenshot({ path: file, type: 'png' });
        console.log(file);
      }
    }
  } finally {
    await browser.close();
  }
})();
