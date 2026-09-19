/*
 * Render the tutorial episodes to mp4, frame by frame.
 *
 *   node render.js                 # every episode built, both languages
 *   node render.js 1 en            # one of them
 *   node render.js --stills 4 30 61   # a few frames of it as PNGs, to judge the look
 *
 * Not a screen recording of a browser playing a film. The page exposes
 * `window.__film.seek(t)` and paints itself as a pure function of t, so this asks for
 * frame 512 at t = 17.0666s, screenshots it, and pipes the PNG straight into ffmpeg.
 * Nothing is dropped when the machine is busy and nothing drifts: frame n is always
 * the same image.
 *
 * The audio is muxed from the track build.py wrote — the clips at the exact seconds
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

// Of the browsers on this machine only Playwright's headless shell starts under
// puppeteer, and it is also the right tool: a renderer without a window.
const CHROME = 'C:\\Users\\Alexander\\AppData\\Local\\ms-playwright\\chromium_headless_shell-1208' +
  '\\chrome-headless-shell-win64\\chrome-headless-shell.exe';

// Node's spawn resolves a bare name through PATHEXT and fails with "spawn UNKNOWN"
// on this machine, so ffmpeg is named outright. FFMPEG in the environment wins.
const FFMPEG = process.env.FFMPEG ||
  ['D:\\ffmpeg\\bin\\ffmpeg.exe', 'C:\\ffmpeg\\bin\\ffmpeg.exe'].find((p) => fs.existsSync(p)) ||
  'ffmpeg.exe';

const FPS = 30;
const W = 1920, H = 1080;

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

/** Every ep<NN>.<lang>.html build.py has written, as {num, lang, slug}. */
function built() {
  return fs.readdirSync(HERE)
    .map((f) => /^ep(\d\d)\.(en|es)\.html$/.exec(f))
    .filter(Boolean)
    .map((m) => ({ num: Number(m[1]), lang: m[2], file: m[0] }))
    .sort((a, b) => a.num - b.num || a.lang.localeCompare(b.lang));
}

async function open(entry) {
  const browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: 'shell',
    args: [`--window-size=${W},${H}`, '--hide-scrollbars', '--force-color-profile=srgb',
           '--no-sandbox', '--disable-gpu', '--allow-file-access-from-files'],
  });
  const page = await browser.newPage();
  await page.setViewport({ width: W, height: H, deviceScaleFactor: 1 });
  const file = path.join(HERE, entry.file);
  await page.goto('file:///' + file.replace(/\\/g, '/'), { waitUntil: 'networkidle0', timeout: 180000 });
  // A frame rendered before the screenshots decode is the right layout over a blank
  // window; before the face lands, the right film in the wrong typeface.
  await page.evaluate(() => Promise.all(
    Array.from(document.images).map((i) => (i.complete ? 0 : new Promise((r) => { i.onload = i.onerror = r; })))
  ));
  await page.evaluate(() => document.fonts && document.fonts.ready);
  await sleep(500);
  return { browser, page };
}

/** The name both the mp4 and the subtitle files carry. */
async function stem(page, entry) {
  const slug = await page.evaluate(() => window.__film.film.card.title);
  void slug;
  const found = fs.readdirSync(path.join(HERE, 'mp4'))
    .find((f) => f.startsWith(`myeztoll-tutorial-${String(entry.num).padStart(2, '0')}-`) &&
                 f.endsWith(`-${entry.lang}.srt`));
  return found ? found.slice(0, -4) : `myeztoll-tutorial-${entry.num}-${entry.lang}`;
}

async function render(entry) {
  const { browser, page } = await open(entry);
  const name = await stem(page, entry);
  const audio = path.join(HERE, 'audio', entry.lang, `ep${String(entry.num).padStart(2, '0')}`, 'track.mp3');
  const out = path.join(HERE, 'mp4', name + '.mp4');
  if (!fs.existsSync(audio)) throw new Error(`no track for ep${entry.num} ${entry.lang} — run build.py`);

  const total = await page.evaluate(() => window.__film.total);
  const frames = Math.ceil(total * FPS);

  const ff = spawn(FFMPEG, [
    '-y', '-v', 'error',
    '-f', 'image2pipe', '-c:v', 'mjpeg', '-framerate', String(FPS), '-i', '-',
    '-i', audio,
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '19',
    '-pix_fmt', 'yuv420p',            // what every platform can actually decode
    '-movflags', '+faststart',        // so it starts playing before it has downloaded
    '-c:a', 'aac', '-b:a', '192k',
    '-shortest', out,
  ]);
  let ffErr = '';
  ff.stderr.on('data', (d) => { ffErr += d.toString(); });
  const done = new Promise((resolve, reject) => {
    ff.on('close', (code) => (code === 0 ? resolve() : reject(new Error('ffmpeg: ' + ffErr.slice(0, 600)))));
  });

  const started = Date.now();
  for (let i = 0; i < frames; i++) {
    await page.evaluate((t) => window.__film.seek(t), i / FPS);
    // JPEG rather than PNG. The screenshot, not the encode, is what a render waits on,
    // and PNG's lossless compression of a 1920x1080 frame costs more than twice what
    // quality-96 JPEG does. It is re-encoded by x264 at crf 19 immediately afterwards,
    // where the difference does not survive to the file.
    const frame = await page.screenshot({ type: 'jpeg', quality: 96, optimizeForSpeed: true });
    if (!ff.stdin.write(frame)) await new Promise((r) => ff.stdin.once('drain', r));
    if (i % 150 === 0) {
      process.stdout.write(`\r  ep${entry.num} ${entry.lang}  frame ${i}/${frames}  ` +
        `${((Date.now() - started) / 1000).toFixed(0)}s   `);
    }
  }
  ff.stdin.end();
  await done;
  await browser.close();

  const mb = fs.statSync(out).size / 1048576;
  process.stdout.write(`\r  ep${entry.num} ${entry.lang}  ${total.toFixed(1)}s  ${mb.toFixed(1)} MB` +
    `  →  ${name}.mp4                    \n`);
}

/** A handful of frames instead of a whole film — a render is minutes, judging is not. */
async function stills(entry, seconds) {
  const { browser, page } = await open(entry);
  const dir = path.join(HERE, 'stills');
  fs.mkdirSync(dir, { recursive: true });
  for (const t of seconds) {
    await page.evaluate((s) => window.__film.seek(s), t);
    const out = path.join(dir, `ep${String(entry.num).padStart(2, '0')}-${entry.lang}-${t}s.png`);
    await page.screenshot({ path: out });
    console.log('  ' + path.basename(out));
  }
  await browser.close();
}

(async () => {
  const args = process.argv.slice(2);
  const wantStills = args.includes('--stills');
  const nums = args.filter((a) => /^\d+$/.test(a)).map(Number);
  const langs = args.filter((a) => a === 'en' || a === 'es');

  if (wantStills) {
    const entries = built().filter((e) => (!langs.length || langs.includes(e.lang)));
    const entry = entries.find((e) => nums.length && e.num === nums[0]) || entries[0];
    const seconds = nums.slice(entry.num === nums[0] ? 1 : 0);
    await stills(entry, seconds.length ? seconds : [1, 6, 14, 22, 30]);
    return;
  }

  for (const entry of built()) {
    if (nums.length && !nums.includes(entry.num)) continue;
    if (langs.length && !langs.includes(entry.lang)) continue;
    await render(entry);
  }
})().catch((e) => {
  console.error('\n' + e.message);
  process.exit(1);
});
