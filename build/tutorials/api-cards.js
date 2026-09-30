/*
 * Copyright (c) 2025-2026 Aegis AO Soft LLC and Alexander Orlov.
 * 34 Middletown Ave, Atlantic Highlands, NJ 07716
 *
 * THIS SOFTWARE IS THE CONFIDENTIAL AND PROPRIETARY INFORMATION OF
 * Aegis AO Soft LLC and Alexander Orlov.
 *
 * This code may be used, reproduced, modified, or distributed ONLY with the
 * prior written permission of Aegis AO Soft LLC / Alexander Orlov.
 *
 * Author: Alexander Orlov
 * Aegis AO Soft LLC
 */

/*
 * The code frames for the Partner API episodes (41-45) and the Partner API quick-start guide.
 *
 * Every request and response on screen comes from the API's OWN catalog (GET /api/partner/v1/functions,
 * public, snapshotted in api/catalog.prod.json) — the same examples the API serves, so a frame cannot
 * teach a call the API does not answer. Refresh the snapshot with:
 *
 *   curl -s https://owner.myeztoll.com/api/partner/v1/functions -o api/catalog.prod.json
 *
 * Two kinds of frame: `fn` (a catalog function: its curl and its example response) and `code` (a short
 * snippet we write — the paging loop, the webhook check — which the catalog cannot carry). Lines to point
 * at are listed per frame in `hl` and drawn highlighted; their boxes, and the request and response boxes,
 * are measured in the page and written to shots/_api_boxes.json, which series_n.py rings.
 *
 * Code is code in every language, so one picture serves EN and ES: it is written to both shots/en and
 * shots/es. The Swagger UI frame is photographed from the public page (no key, no login).
 *
 *   node api-cards.js              # every frame
 *   node api-cards.js --only=api-10
 */

const fs = require('fs');
const path = require('path');
const puppeteer = require('C:/aegis-aa/node_modules/puppeteer-core');

const args = process.argv.slice(2);
const argVal = (name, dflt) => {
  const hit = args.find((a) => a.startsWith(`--${name}=`));
  return hit ? hit.slice(name.length + 3) : dflt;
};
const ONLY = argVal('only', '').split(',').filter(Boolean);
const SHOTS = path.join(__dirname, 'shots');
const CATALOG = path.join(__dirname, 'api', 'catalog.prod.json');
const SWAGGER = 'https://owner.myeztoll.com/api/partner/v1/index/index.html';

const CHROME = [
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
].find((p) => fs.existsSync(p));

// Names in the catalog examples that must not reach a public-ish frame: a real-looking customer and a
// real partner. The API's own catalog should lose them too (reported, not changed from here).
const SANITIZE = [
  ['Nancy Pridgen', 'John Doe'],
  ['FleetPilot', 'Your Platform'],
];

// ---------------------------------------------------------------- the frames

const FRAMES = [
  { name: 'api-00b-keys', code: 'http', title: 'Every call carries a key',
    text: `GET https://owner.myeztoll.com/api/partner/v1/tolls?from=2026-09-01T00:00:00Z&to=2026-10-01T00:00:00Z

# An owner key: acts for ONE owner
X-Api-Key: aegispk-••••••••••••••••

# An integration token: one token for MANY owners...
X-Api-Key: aegispi-••••••••••••••••
# ...so each call names the owner it is for (GET /owners lists them)
X-Owner-Id: 7f0c…

# Test first on the sandbox, with its own key:
#   https://dev-owner.myeztoll.com/api/partner/v1`,
    hl: { owner: 'aegispk-', integ: 'aegispi-', ownerid: 'X-Owner-Id: 7f0c', sandbox: 'dev-owner' } },
  { name: 'api-01-catalog', fn: 'GET /',
    response: { success: true, data: {
      api: 'Aegis Partner API', version: 'v1',
      baseUrl: 'https://owner.myeztoll.com/api/partner/v1',
      swaggerUi: 'https://owner.myeztoll.com/api/partner/v1/index',
      openApi: 'https://owner.myeztoll.com/api/partner/v1/openapi.json',
      auth: { header: 'X-Api-Key' },
      functions: '[ … 54 functions, each with a call and a response example … ]' }, error: null },
    hl: { base: '"baseUrl"', header: '"header"', success: '"success"', error: '"error"' } },
  { name: 'api-02-me', fn: 'GET /me', hl: { kind: '"kind"' } },
  { name: 'api-03-owners', fn: 'GET /owners?page=&pageSize=', hl: { owner: '"ownerId"', paging: '"hasMore"' } },
  { name: 'api-04-car', fn: 'POST /cars', hl: { ext: '"externalId"', id: '"id"' } },
  { name: 'api-05-transponder', fn: 'GET/POST /cars/{id}/transponders', hl: { num: '"transponderNumber"' } },
  { name: 'api-06-driver', fn: 'POST /drivers', hl: { ext: '"externalId"', dl: '"driverLicenseId"' } },
  { name: 'api-07-booking', fn: 'POST /bookings',
    hl: { car: '"carExternalId"', renter: '"renterExternalId"', status: '"statusName"' } },
  { name: 'api-08-card', fn: 'GET /drivers/{id}/card', hl: { has: '"hasCard"', valid: '"isValid"' } },
  { name: 'api-09-card-link', fn: 'POST /bookings/{id}/card-link', hl: { url: '"cardRegistrationUrl"' } },
  { name: 'api-10-tolls', fn: 'GET /tolls?from=&to=&carId=&source=all|agency|gps&page=&pageSize=',
    hl: { source: '"source": "agency"', amount: '"agencyAmount"', fee: '"serviceFee"',
      booking: '"bookingSource"', charge: '"status": "charged"', more: '"hasMore"' } },
  { name: 'api-11-car-tolls', fn: 'GET /cars/{id}/tolls?from=&to=&page=&pageSize=',
    hl: { ext: '"externalCarId"' } },
  { name: 'api-12-booking-tolls', fn: 'GET /bookings/{id}/tolls?source=&page=&pageSize=',
    hl: { gps: '"source": "gps"', ext: '"externalId": "gps:' } },
  { name: 'api-13-violations', fn: 'GET /violations?from=&to=&carId=&bookingId=&page=&pageSize=',
    hl: { amount: '"amount"', fee: '"serviceFee"', paid: '"isPaid"' } },
  { name: 'api-14-paging', code: 'javascript', title: 'Read every page',
    text: `// Every list is a page: { items, page, pageSize, total, hasMore }
const BASE = 'https://owner.myeztoll.com/api/partner/v1';

async function allTolls(key, from, to) {
  const rows = [];
  for (let page = 1; ; page++) {
    const url = \`\${BASE}/tolls?from=\${from}&to=\${to}&page=\${page}&pageSize=1000\`;
    const res = await fetch(url, { headers: { 'X-Api-Key': key } });
    const body = await res.json();              // { success, data, error }
    if (!body.success) throw new Error(body.error);
    rows.push(...body.data.items);
    if (!body.data.hasMore) return rows;       // keep asking while hasMore
  }
}`,
    hl: { page: 'page=${page}', more: 'hasMore)', env: 'body.success' } },
  { name: 'api-15-positions', fn: 'GET /gps/positions?carId=&page=&pageSize=',
    hl: { pos: '"lat"', online: '"online"', age: '"ageSeconds"' } },
  { name: 'api-16-mileage', fn: 'GET /cars/{id}/gps/mileage?from=&to=', hl: { miles: '"distanceMiles"' } },
  { name: 'api-17-webhook', fn: 'GET/POST /webhooks', hl: { secret: '"secret"', events: '"*"' } },
  { name: 'api-18-verify', code: 'javascript', title: 'Check a webhook signature (Node.js)',
    text: `// X-MyEzToll-Signature: t=<unix seconds>,v1=<hex HMAC-SHA256>
const crypto = require('crypto');

function verify(rawBody, header, secret) {
  const parts = Object.fromEntries(header.split(',').map((p) => p.split('=')));
  const signed = \`\${parts.t}.\${rawBody}\`;           // "t.body", the body exactly as received
  const expected = crypto.createHmac('sha256', secret).update(signed, 'utf8').digest('hex');
  const fresh = Math.abs(Date.now() / 1000 - Number(parts.t)) < 300;   // reject replays
  return fresh && String(parts.v1).length === expected.length
    && crypto.timingSafeEqual(Buffer.from(expected), Buffer.from(parts.v1));
}

// Also sent: X-MyEzToll-Event (the event type) and X-MyEzToll-Event-Id
// (de-duplicate on it: a delivery can be retried for up to ~1.5 days).`,
    hl: { signed: '"t.body"', hmac: "createHmac('sha256'", replay: 'reject replays', dedup: 'de-duplicate' } },
  { name: 'api-19-charge', fn: 'POST /charges', compactBody: true, hl: { items: '"items": [', warn: '"sum_mismatch"' } },
  { name: 'api-20-dispute', fn: 'POST /disputes', hl: { ev: '"evidenceStatus"' } },
  { name: 'api-21-evidence', fn: 'GET /disputes/{id}',
    hl: { rec: '"recommendation"', ev: '"evidence": {', file: '"fileId": "9f1c' } },
  { name: 'api-22-dispute-patch', fn: 'PATCH /disputes/{id}', hl: { status: '"status"' } },
];

// ---------------------------------------------------------------- rendering

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const clean = (s) => SANITIZE.reduce((v, [a, b]) => v.split(a).join(b), s);

/** A curl one-liner, broken at its options so it reads on a slide. */
function formatCurl(cmd, prettyBody = true) {
  const out = cmd.replace(/ (-X|-H|-d|-F|-o) /g, ' \\\n     $1 ')
    .replace(/ (https?:\/\/\S+|"https?:\/\/[^"]+")$/, ' \\\n     $1');
  // A JSON body on one line runs off the frame: lay it out one field per line — unless the frame
  // asks not to (compactBody): a long body AND a long response do not both fit.
  if (!prettyBody) return out;
  return out.replace(/-d '(\{.*?\})'/, (whole, json) => {
    try {
      const pretty = JSON.stringify(JSON.parse(json), null, 2).split('\n').join('\n        ');
      return `-d '${pretty}'`;
    } catch (e) {
      return whole;
    }
  });
}

// A response longer than SPLIT_AT lines is laid out in two columns (a toll row with its renterCharge is
// ~45 lines — one column would run off the frame, and a smaller font would not read in a video).
const SPLIT_AT = 26;
const MAX_LINES = 60;

function jsonLines(obj) {
  const lines = JSON.stringify(obj, null, 2).split('\n');
  if (lines.length <= MAX_LINES) return lines;
  return lines.slice(0, MAX_LINES - 1).concat(['  …']);
}

function colour(line) {
  return esc(line)
    .replace(/(&quot;|")([^"]*?)("\s*:)/g, '<span class="k">"$2"</span>:')
    .replace(/: ("[^"]*")/g, ': <span class="s">$1</span>')
    .replace(/: (-?\d+(\.\d+)?)/g, ': <span class="n">$1</span>')
    .replace(/: (true|false|null)/g, ': <span class="b">$1</span>');
}

function block(lines, hl, cls) {
  return lines.map((l) => {
    const key = Object.keys(hl).find((k) => l.includes(hl[k]));
    const body = cls === 'json' ? colour(l) : esc(l);
    return `<div class="ln${key ? ' hl' : ''}"${key ? ` data-hl="${key}"` : ''}>${body || '&nbsp;'}</div>`;
  }).join('');
}

const CSS = `
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1600px;height:1000px;background:#0f1222;font-family:Consolas,'Cascadia Mono','Courier New',monospace;color:#d7dcf5}
.frame{position:absolute;inset:0;padding:44px 64px;display:flex;flex-direction:column;justify-content:center}
.top{display:flex;align-items:center;gap:18px;margin-bottom:22px}
.brand{font-family:Inter,'Segoe UI',Arial,sans-serif;font-size:16px;letter-spacing:.14em;text-transform:uppercase;color:#8f94ff;font-weight:700}
.verb{font-weight:700;font-size:26px;padding:4px 14px;border-radius:8px;background:#2b2f63;color:#b7bbff}
.path{font-size:26px;color:#fff}
.box{background:#171b33;border:1px solid #2a2f55;border-radius:14px;padding:14px 20px;margin-bottom:18px}
.lbl{font-family:Inter,'Segoe UI',Arial,sans-serif;font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:#7c82b8;margin-bottom:6px}
.ln{font-size:15.5px;line-height:1.36;white-space:pre;border-radius:5px;padding:0 6px;margin:0 -6px}
.req .ln{color:#e8e1a8}
.ln.hl{background:rgba(255,196,64,.18);box-shadow:inset 3px 0 0 #ffc440}
.k{color:#8fd3ff}.s{color:#b5e38a}.n{color:#ffb86b}.b{color:#ff8fb1}
.code .ln{font-size:17px;line-height:1.45}
.cols{column-count:2;column-gap:40px}
.cols .ln{break-inside:avoid}
`;

function page(frame, catalog) {
  let head;
  let body;
  if (frame.code) {
    head = `<span class="verb">${esc(frame.code)}</span><span class="path">${esc(frame.title)}</span>`;
    body = `<div class="box code" data-box="res">${block(frame.text.split('\n'), frame.hl || {}, 'code')}</div>`;
  } else {
    const fn = catalog.find((f) => `${f.method} ${f.path}` === frame.fn);
    if (!fn) throw new Error(`not in the catalog: ${frame.fn}`);
    const response = frame.response || JSON.parse(clean(JSON.stringify(fn.exampleResponse)));
    const pathOnly = fn.path.split('?')[0];
    const lines = jsonLines(response);
    head = `<span class="verb">${esc(fn.method)}</span><span class="path">${esc(pathOnly)}</span>`;
    body = `<div class="box req" data-box="req"><div class="lbl">Request</div>${block(formatCurl(clean(fn.exampleRequest), !frame.compactBody).split('\n'), frame.hl || {}, 'req')}</div>`
      + `<div class="box" data-box="res"><div class="lbl">Response</div>`
      + `<div class="${lines.length > SPLIT_AT ? 'cols' : ''}">${block(lines, frame.hl || {}, 'json')}</div></div>`;
  }
  return `<!doctype html><html><head><meta charset="utf-8"><style>${CSS}</style></head><body><div class="frame">`
    + `<div class="top"><span class="brand">MyEZToll · Partner API</span></div>`
    + `<div class="top">${head}</div>${body}</div></body></html>`;
}

async function measure(tab) {
  return tab.evaluate(() => {
    const r = (el) => {
      const b = el.getBoundingClientRect();
      const f = (v) => Math.round(v * 1000) / 1000;
      return [f(b.left / 1600), f(b.top / 1000), f(b.width / 1600), f(b.height / 1000)];
    };
    const out = { hl: {} };
    document.querySelectorAll('[data-box]').forEach((el) => { out[el.dataset.box] = r(el); });
    document.querySelectorAll('[data-hl]').forEach((el) => {
      if (!out.hl[el.dataset.hl]) out.hl[el.dataset.hl] = r(el);
    });
    const tall = document.querySelector('.frame').scrollHeight > 1000;
    return Object.assign(out, { overflow: tall });
  });
}

(async () => {
  const catalog = JSON.parse(fs.readFileSync(CATALOG, 'utf8')).data.functions;
  const browser = await puppeteer.launch({ executablePath: CHROME, headless: 'new' });
  const tab = await browser.newPage();
  await tab.setViewport({ width: 1600, height: 1000, deviceScaleFactor: 2 });
  const boxesFile = path.join(SHOTS, '_api_boxes.json');
  const boxes = fs.existsSync(boxesFile) ? JSON.parse(fs.readFileSync(boxesFile, 'utf8')) : {};

  for (const frame of FRAMES.filter((f) => !ONLY.length || ONLY.some((o) => f.name.includes(o)))) {
    await tab.setContent(page(frame, catalog), { waitUntil: 'load' });
    const m = await measure(tab);
    if (m.overflow) console.log(`  WARNING ${frame.name}: taller than the frame`);
    for (const want of Object.keys(frame.hl || {})) {
      if (!m.hl[want]) console.log(`  WARNING ${frame.name}: highlight "${want}" matched no line`);
    }
    boxes[frame.name] = m;
    for (const lang of ['en', 'es']) {
      fs.mkdirSync(path.join(SHOTS, lang), { recursive: true });
      await tab.screenshot({ path: path.join(SHOTS, lang, `${frame.name}.png`) });
    }
    console.log(frame.name);
  }

  // The Swagger UI, as a partner first meets it: public, no key.
  if (!ONLY.length || ONLY.some((o) => 'api-00-swagger'.includes(o))) {
    const sw = await browser.newPage();
    await sw.setViewport({ width: 1600, height: 1000, deviceScaleFactor: 2 });
    await sw.goto(SWAGGER, { waitUntil: 'networkidle2', timeout: 60000 });
    await sw.waitForSelector('.opblock-tag', { timeout: 30000 });
    await new Promise((r) => setTimeout(r, 1500));
    const m = await sw.evaluate(() => {
      const r = (el) => {
        if (!el) return null;
        const b = el.getBoundingClientRect();
        const f = (v) => Math.round(v * 1000) / 1000;
        return [f(b.left / 1600), f(b.top / 1000), f(b.width / 1600), f(b.height / 1000)];
      };
      window.scrollTo(0, 0);
      return { hl: { authorize: r(document.querySelector('.btn.authorize')),
        tags: r(document.querySelector('.opblock-tag-section')) } };
    });
    boxes['api-00-swagger'] = m;
    for (const lang of ['en', 'es']) await sw.screenshot({ path: path.join(SHOTS, lang, 'api-00-swagger.png') });
    console.log('api-00-swagger');
  }

  fs.writeFileSync(boxesFile, JSON.stringify(boxes, null, 1));
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });
