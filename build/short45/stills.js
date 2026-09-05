/*
 * Grab a handful of frames instead of a whole film.
 *
 *   node stills.js en 1x1 3 12 25 36 44 54
 *
 * A full render is twenty-odd minutes; judging a change to the look does not need
 * one. Same browser, same viewport, same seek — so what comes out is exactly the
 * frame the mp4 would hold at that second.
 */
const fs = require('fs');
const path = require('path');

const HERE = __dirname;
const puppeteer = require(path.join('C:\\aegis-aa', 'node_modules', 'puppeteer-core'));
const CHROME = 'C:\\Users\\Alexander\\AppData\\Local\\ms-playwright\\chromium_headless_shell-1208' +
  '\\chrome-headless-shell-win64\\chrome-headless-shell.exe';

const SHAPES = { '16x9': { w: 1920, h: 1080, square: false }, '1x1': { w: 1080, h: 1080, square: true } };

(async () => {
  const args = process.argv.slice(2);
  const lang = args.find((a) => /^[a-z]{2}$/.test(a)) || 'en';
  const shapeName = args.find((a) => SHAPES[a]) || '1x1';
  const times = args.filter((a) => /^[\d.]+$/.test(a)).map(Number);
  const shape = SHAPES[shapeName];
  const out = path.join(HERE, 'stills');
  fs.mkdirSync(out, { recursive: true });

  const browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: 'shell',
    args: [`--window-size=${shape.w},${shape.h}`, '--hide-scrollbars', '--force-color-profile=srgb',
           '--no-sandbox', '--disable-gpu'],
  });
  const page = await browser.newPage();
  await page.setViewport({ width: shape.w, height: shape.h, deviceScaleFactor: 1 });
  await page.goto('file:///' + path.join(HERE, `film.${lang}.html`).replace(/\\/g, '/'),
                  { waitUntil: 'networkidle0', timeout: 120000 });
  if (shape.square) await page.evaluate(() => document.body.classList.add('square'));
  await page.evaluate(() => document.fonts && document.fonts.ready);
  await new Promise((r) => setTimeout(r, 400));

  for (const t of times) {
    await page.evaluate((time) => window.__film.seek(time), t);
    const file = path.join(out, `${lang}-${shapeName}-${String(t).replace('.', '_')}s.png`);
    await page.screenshot({ path: file });
    console.log(path.basename(file));
  }
  await browser.close();
})().catch((e) => { console.error(e.message); process.exit(1); });
