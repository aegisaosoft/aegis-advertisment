/*
 * Render film.<lang>.html to mp4, frame by frame.
 *
 *   node render.js                 # every language x every shape
 *   node render.js en 1x1          # one of them
 *
 * Not a screen recording. The film exposes `window.__film.seek(t)` and paints
 * itself as a pure function of t, so this asks for frame 512 at t = 17.0666s,
 * screenshots it, and pipes the PNG straight into ffmpeg. Nothing is dropped when
 * the machine is busy and nothing drifts: frame n is always the same image.
 *
 * The audio is muxed from `audio/<lang>/track.mp3` — the clips at the exact seconds
 * the timeline placed them — rather than captured from the browser's speakers, so
 * picture and voice cannot disagree.
 */
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const HERE = __dirname;
const ROOT = 'C:\\aegis-aa';
// puppeteer-core lives in the workspace root's node_modules, not next to this file.
const puppeteer = require(path.join(ROOT, 'node_modules', 'puppeteer-core'));

/*
 * The browser. This machine has three and only one of them starts under puppeteer:
 * Edge exits immediately, the full Chromium next to this one dies with "spawn
 * UNKNOWN", and Playwright's headless shell runs. It is also the right tool —
 * a headless shell is a renderer without a window, which is all this needs.
 */
const CHROME = 'C:\\Users\\Alexander\\AppData\\Local\\ms-playwright\\chromium_headless_shell-1208' +
  '\\chrome-headless-shell-win64\\chrome-headless-shell.exe';
const FPS = 30;

// Node's spawn resolves a bare name through PATHEXT and fails with "spawn UNKNOWN"
// on this machine, so ffmpeg is named outright. FFMPEG in the environment wins.
const FFMPEG = process.env.FFMPEG ||
  ['D:\\ffmpeg\\bin\\ffmpeg.exe', 'C:\\ffmpeg\\bin\\ffmpeg.exe'].find((p) => fs.existsSync(p)) ||
  'ffmpeg.exe';

// LinkedIn's feed gives a square far more screen than a widescreen frame; the 16:9
// is for YouTube, the site and email. Both are the same layout — the film's content
// column is square in either, which is why one design serves both.
const SHAPES = {
  '16x9': { w: 1920, h: 1080, square: false },
  '1x1': { w: 1080, h: 1080, square: true },
};

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function render(lang, shapeName) {
  const shape = SHAPES[shapeName];
  const film = path.join(HERE, `film.${lang}.html`);
  const audio = path.join(HERE, 'audio', lang, 'track.mp3');
  const out = path.join(HERE, 'mp4', `myeztoll-four-twelve-${lang}-${shapeName}.mp4`);
  if (!fs.existsSync(film)) throw new Error(`no ${path.basename(film)} — run build.py first`);
  if (!fs.existsSync(audio)) throw new Error(`no track for ${lang} — run build.py first`);
  fs.mkdirSync(path.dirname(out), { recursive: true });

  const browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: 'shell',
    args: [`--window-size=${shape.w},${shape.h}`, '--hide-scrollbars', '--force-color-profile=srgb',
           '--no-sandbox', '--disable-gpu'],
  });
  const page = await browser.newPage();
  await page.setViewport({ width: shape.w, height: shape.h, deviceScaleFactor: 1 });
  await page.goto('file:///' + film.replace(/\\/g, '/'), { waitUntil: 'networkidle0', timeout: 120000 });
  if (shape.square) await page.evaluate(() => document.body.classList.add('square'));
  // The display face arrives over the network; a frame rendered before it lands is
  // the same film in the wrong typeface.
  await page.evaluate(() => document.fonts && document.fonts.ready);
  await sleep(400);

  const total = await page.evaluate(() => window.__film.total);
  const frames = Math.ceil(total * FPS);

  const ff = spawn(FFMPEG, [
    '-y', '-v', 'error',
    '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
    '-i', audio,
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
    '-pix_fmt', 'yuv420p',            // what every platform can actually decode
    '-movflags', '+faststart',        // so it starts playing before it has downloaded
    '-c:a', 'aac', '-b:a', '192k',
    '-shortest', out,
  ]);
  let ffErr = '';
  ff.stderr.on('data', (d) => { ffErr += d.toString(); });
  const done = new Promise((resolve, reject) => {
    ff.on('close', (code) => (code === 0 ? resolve() : reject(new Error('ffmpeg: ' + ffErr.slice(0, 500)))));
  });

  const started = Date.now();
  for (let i = 0; i < frames; i++) {
    await page.evaluate((t) => window.__film.seek(t), i / FPS);
    const png = await page.screenshot({ type: 'png' });
    if (!ff.stdin.write(png)) await new Promise((r) => ff.stdin.once('drain', r));
    if (i % 150 === 0) {
      process.stdout.write(
        `\r  ${lang} ${shapeName}  frame ${i}/${frames}  ${((Date.now() - started) / 1000).toFixed(0)}s`
      );
    }
  }
  ff.stdin.end();
  await done;
  await browser.close();

  const mb = fs.statSync(out).size / 1048576;
  process.stdout.write(
    `\r  ${lang} ${shapeName}  ${frames} frames, ${total.toFixed(1)}s, ${mb.toFixed(1)} MB` +
    `  →  ${path.basename(out)}          \n`
  );
}

(async () => {
  const args = process.argv.slice(2);
  const langs = args.filter((a) => /^[a-z]{2}$/.test(a));
  const shapes = args.filter((a) => SHAPES[a]);
  for (const lang of langs.length ? langs : ['en', 'es']) {
    for (const shape of shapes.length ? shapes : Object.keys(SHAPES)) {
      await render(lang, shape);
    }
  }
})().catch((e) => {
  console.error('\n' + e.message);
  process.exit(1);
});
