/*
 * Render endcard.html to endcard.png at 1920x1080.
 *
 *   node endcard.js [source.html] [out.png]
 *
 * The closing frame is drawn rather than generated: it is the only place in the
 * ToonBee cut where the wording must be exact, and every generated frame in that film
 * has drifted — the money figure counted itself down, the price rings came out as
 * lettering that means nothing. append_endcard.js puts this on the end of the export.
 */
const path = require('path');
const puppeteer = require(path.join('C:\\aegis-aa', 'node_modules', 'puppeteer-core'));

const CHROME = 'C:\\Users\\Alexander\\AppData\\Local\\ms-playwright\\chromium_headless_shell-1208' +
  '\\chrome-headless-shell-win64\\chrome-headless-shell.exe';

const SRC = process.argv[2] || 'endcard.html';
const OUT = process.argv[3] || 'endcard.png';

(async () => {
  const browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: 'shell',
    args: ['--no-sandbox', '--disable-gpu', '--force-color-profile=srgb', '--hide-scrollbars'],
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 1 });
  await page.goto('file:///' + path.join(__dirname, SRC).replace(/\\/g, '/'),
                  { waitUntil: 'networkidle0', timeout: 120000 });
  await page.evaluate(() => document.fonts && document.fonts.ready);
  await new Promise((r) => setTimeout(r, 500));
  await page.screenshot({ path: path.join(__dirname, OUT) });
  await browser.close();
  console.log(OUT + ' rendered at 1920x1080');
})().catch((e) => { console.error(e.message); process.exit(1); });
