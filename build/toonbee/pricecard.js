/*
 * Render pricecard.html to a six-second clip, frame by frame.
 *
 *   node pricecard.js            # both languages
 *   node pricecard.js es         # one of them
 *
 * Not a screen recording: the card paints itself as a pure function of t
 * (`window.__card.seek`), so frame n is always the same image and the labels land on
 * the exact second the narrator says them. splice_scene10.sh composites the result
 * over scene 10 of the film.
 *
 * The clip carries no audio. The narration in that scene is right and is not touched;
 * only the picture behind it is replaced.
 */
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const HERE = __dirname;
const ROOT = 'C:\\aegis-aa';
const puppeteer = require(path.join(ROOT, 'node_modules', 'puppeteer-core'));

/*
 * The browser. This machine has three and only one of them starts under puppeteer:
 * Edge exits immediately, the full Chromium beside it dies with "spawn UNKNOWN", and
 * Playwright's headless shell runs.
 */
const CHROME = 'C:\\Users\\Alexander\\AppData\\Local\\ms-playwright\\chromium_headless_shell-1208' +
  '\\chrome-headless-shell-win64\\chrome-headless-shell.exe';

// Node's spawn resolves a bare name through PATHEXT and fails with "spawn UNKNOWN"
// on this machine, so ffmpeg is named outright. FFMPEG in the environment wins.
const FFMPEG = process.env.FFMPEG ||
  ['D:\\ffmpeg\\bin\\ffmpeg.exe', 'C:\\ffmpeg\\bin\\ffmpeg.exe'].find((p) => fs.existsSync(p)) ||
  'ffmpeg.exe';

const FPS = 30;
const W = 1920;
const H = 1080;

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function render(lang) {
  const source = 'file:///' + path.join(HERE, 'pricecard.html').replace(/\\/g, '/') + '?lang=' + lang;
  const out = path.join(HERE, `pricecard.${lang}.mp4`);

  const browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: 'shell',
    args: [`--window-size=${W},${H}`, '--hide-scrollbars', '--force-color-profile=srgb',
           '--no-sandbox', '--disable-gpu'],
  });
  const page = await browser.newPage();
  await page.setViewport({ width: W, height: H, deviceScaleFactor: 1 });
  await page.goto(source, { waitUntil: 'networkidle0', timeout: 120000 });
  // The display face arrives over the network; a frame rendered before it lands is
  // the same card in the wrong typeface.
  await page.evaluate(() => document.fonts && document.fonts.ready);
  await sleep(400);

  const total = await page.evaluate(() => window.__card.total);
  const frames = Math.ceil(total * FPS);

  const ff = spawn(FFMPEG, [
    '-y', '-v', 'error',
    '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '16',
    '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
    out,
  ]);
  let ffErr = '';
  ff.stderr.on('data', (d) => { ffErr += d.toString(); });
  const done = new Promise((resolve, reject) => {
    ff.on('close', (code) => (code === 0 ? resolve() : reject(new Error('ffmpeg: ' + ffErr.slice(0, 500)))));
  });

  for (let i = 0; i < frames; i++) {
    await page.evaluate((t) => window.__card.seek(t), i / FPS);
    const png = await page.screenshot({ type: 'png' });
    if (!ff.stdin.write(png)) await new Promise((r) => ff.stdin.once('drain', r));
  }
  ff.stdin.end();
  await done;
  await browser.close();

  console.log(`  ${lang}  ${frames} frames, ${total.toFixed(1)}s  ->  ${path.basename(out)}`);
}

(async () => {
  const langs = process.argv.slice(2).filter((a) => /^[a-z]{2}$/.test(a));
  for (const lang of langs.length ? langs : ['en', 'es']) await render(lang);
})().catch((e) => {
  console.error(e.message);
  process.exit(1);
});
