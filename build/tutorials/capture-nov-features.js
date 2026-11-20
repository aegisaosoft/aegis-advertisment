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
 * Screenshots for episode 57 (a ticket that came by mail), the re-shot episode 11 (Violations) and the two new
 * screens of episode 32 (a case the agency refused, a case the agency holds), from the DEV portal, with DEMO DATA.
 *
 * The session is shown as an OWNER's (admin flags switched off in the browser). Everything listed is staged:
 * violations, cars, the ticket photo (drawn here, a made-up agency and plate) and what the API "read" off it,
 * the save result and the collections cases. The page itself is the real deployed portal.
 *
 * READ-ONLY BY CONSTRUCTION. The writes the episode shows (read the photo, save the ticket) are answered here;
 * every other API request that is not a GET is aborted before it leaves the browser.
 *
 * Usage:
 *   node capture-nov-features.js --cdp=9223
 *   node capture-nov-features.js --cdp=9223 --only=nov-0 --lang=es
 */

const fs = require('fs');
const path = require('path');
const puppeteer = require('C:/aegis-aa/node_modules/puppeteer-core');
const REDACTION = require('C:/aegis-aa/docs/tools/redaction-rules');
const { BLUR_FN, waitForApp, setLanguage, sleep } = require('./capture-common');

const args = process.argv.slice(2);
const argVal = (name, dflt) => {
  const hit = args.find((a) => a.startsWith(`--${name}=`));
  return hit ? hit.slice(name.length + 3) : dflt;
};

const BASE = argVal('base', 'https://dev-owner.myeztoll.com');
const CDP_PORT = argVal('cdp', '9223');
const LANGS = argVal('lang', 'en,es').split(',').map((s) => s.trim()).filter(Boolean);
const ONLY = argVal('only', '').split(',').map((s) => s.trim()).filter(Boolean);
const SHOTS = path.join(__dirname, 'shots');
const VIEWPORT = { width: 1600, height: 1000, deviceScaleFactor: 2 };
const SETTLE_MS = 2600;
const LOCALES = 'C:/aegis-aa/aegis-owner-web/src/locales';

if (!/^https:\/\/dev-/.test(BASE)) throw new Error(`refusing a non-dev base: ${BASE}`);

const OWNER = { firstName: 'Your Company', lastName: '', email: 'yourcompany@mail.myeztoll.com' };
const RENAME = [
  ['Aegis AG Soft LLC', 'Your Company'], ['Aegis AA Soft LLC', 'Your Company'], ['AEGIS AG SOFT', 'YOUR COMPANY'],
  ['aegisagsoft@gmail.com', 'yourcompany@mail.myeztoll.com'], ['aegisaasoft@outlook.com', 'yourcompany@mail.myeztoll.com'],
  ['aegis admin', 'Your Company'],
];
const day = (d, h = 15, m = 0) => { const t = new Date(Date.now() + d * 86400000); t.setUTCHours(h, m, 0, 0); return t.toISOString(); };

// ------------------------------------------------------------------ staged data

const car = (n, brand, model, year, plate) => ({
  id: `demo-car-${n}`, ownerId: 'self', title: `${brand} ${model}`, carBrand: brand, carModel: model, year,
  carPlateNumber: plate, carPlateNumberState: 'NJ', published: false,
});
const CARS = [car(1, 'Toyota', 'Camry', 2025, 'NJT4102'), car(2, 'Honda', 'Accord', 2024, 'NJL8830'),
  car(3, 'Hyundai', 'Sonata', 2026, 'NJP5521')];

const vio = (n, d, carN, citation, amount, agency, address, state, extra = {}) => ({
  id: `V-30${n}17`, carId: `demo-car-${carN}`, carTitle: CARS[carN - 1].title, bookingId: `BK-30${n}17`,
  licensePlate: CARS[carN - 1].carPlateNumber, state: 'NJ', citationNumber: citation, amount, issueDateUtc: d,
  address, agency, status: 'Open', chargeStatus: null, isPaid: false, payUrl: 'https://pay.example.org/ticket',
  pluginKey: 'demo-agency', endpointDisplayName: agency, firstSeenAt: day(-2), lastSeenAt: day(0), ...extra,
});
const VIOLATIONS = [
  vio(1, day(-12, 18, 42), 2, 'SC48810', 50, 'City Traffic Camera Program', 'Broad St & Market St', 'NJ'),
  vio(2, day(-15, 13, 7), 3, 'PX902216', 65, 'Downtown Parking Office', '5th Ave & 22nd St', 'NY', { isPaid: true, status: 'Paid' }),
  vio(3, day(-21, 21, 15), 1, 'RL7730214', 100, 'City Parking Authority', 'Main St & 1st Ave', 'PA'),
];
// The ticket of episode 57, as it is listed after it was saved: entered by hand, on Taylor Quinn's rental.
const MAILED = vio(9, day(-7, 19, 5), 1, 'RL1234567', 100, 'City Parking Authority', 'Main St & 1st Ave', 'PA',
  { pluginKey: 'manual-notice', endpointDisplayName: null, bookingId: 'BK-30917', firstSeenAt: day(0), payUrl: 'https://pay.example.org/ticket' });
const listOf = (rows) => ({ items: rows, totalCount: rows.length, page: 1, pageSize: 25, lastScanAt: day(0, 6), lastScanStatus: 'completed' });

const ISSUED = new Date(Date.now() - 7 * 86400000);
const p2 = (v) => String(v).padStart(2, '0');
const ISSUED_LOCAL = `${ISSUED.getUTCFullYear()}-${p2(ISSUED.getUTCMonth() + 1)}-${p2(ISSUED.getUTCDate())}T14:05`;
const READ = {
  success: true,
  data: {
    citationNumber: 'RL1234567', pin: '5821', issuedLocal: ISSUED_LOCAL, amount: 100, dueDate: null,
    licensePlate: 'NJT 4102', plateState: 'NJ', agency: 'City Parking Authority', issuingState: 'PA',
    paymentUrl: 'https://pay.example.org/ticket', violationType: 'red_light', location: 'Main St & 1st Ave',
  },
};
const SAVED = { success: true, violationId: 'V-30917', bookingId: 'BK-30917', issueDateUtc: MAILED.issueDateUtc,
  lookup: { outcome: 'found', pluginKey: 'demo-agency', amount: 100, isPaid: false } };

const kase = (n, status, first, last, carLabel, principal, extra = {}) => ({
  id: `demo-case-${n}`, status, createdAtUtc: day(-9), bookingId: `BK-40${n}11`, vehicleLabel: carLabel,
  bookingFromUtc: day(-40, 14), bookingToUtc: day(-34, 14), driverUserId: `demo-driver-${n}`, driverName: `${first} ${last}`,
  driverEmail: null, driverCountry: 'US', invoiceId: `demo-inv-${n}`, invoiceNumber: `INV-202610${n}4-4F2A1${n}`,
  principalAmount: principal, collectionFeeAmount: Math.round(principal * 0.4286 * 100) / 100,
  claimAmount: Math.round(principal * 1.4286 * 100) / 100, currency: 'USD', daysOverdue: 33 + n, lettersSent: 3,
  deliveryProof: 'Email', deliveryUnconfirmed: false, agencyPluginKey: 'debitura', agencyCommissionPercent: 30,
  approvedAtUtc: day(-8), approvedByUserId: 'self', declineReason: null, recoveredAmount: null, error: null, ...extra,
});
const CASES = [
  kase(1, 'Failed', 'Avery', 'Lane', 'Honda Accord NJL8830', 612.5, {
    error: 'The debtor address is incomplete: add a street and ZIP code at https://app.example.org/cases/DBT-50311 and send the case again.',
  }),
  kase(2, 'Placed', 'Drew', 'Parker', 'Hyundai Sonata NJP5521', 840, {
    agencyCaseNumber: 'DBT-50288', agencyCaseUrl: 'https://app.example.org/cases/DBT-50288',
  }),
];

// ------------------------------------------------------------------ the ticket "photo"

const TICKET_HTML = (issued) => `<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1600px;height:1000px;background:radial-gradient(circle at 30% 20%,#8a7a66,#4d4236);display:flex;align-items:center;justify-content:center;font-family:Arial,Helvetica,sans-serif}
.p{width:860px;background:#fbfaf6;transform:rotate(-2.2deg);box-shadow:0 30px 60px rgba(0,0,0,.45);padding:42px 52px;color:#1d1d1d}
.h{display:flex;justify-content:space-between;align-items:flex-start;border-bottom:3px solid #1d1d1d;padding-bottom:14px}
.ag{font-size:26px;font-weight:700;letter-spacing:.5px}.sub{font-size:15px;color:#444;margin-top:4px}
.t{font-size:30px;font-weight:800;color:#a01818;text-align:right}.g{display:grid;grid-template-columns:1fr 1fr;gap:16px 40px;margin-top:24px}
.l{font-size:13px;color:#666;text-transform:uppercase;letter-spacing:1px}.v{font-size:23px;font-weight:700;margin-top:3px;font-family:'Courier New',monospace}
.amt{margin-top:26px;border:2px solid #1d1d1d;padding:14px 18px;display:flex;justify-content:space-between;align-items:center}
.amt .v{font-size:34px}.f{margin-top:22px;font-size:15px;color:#333;line-height:1.5}
.ph{margin-top:22px;height:150px;background:repeating-linear-gradient(45deg,#d9d6cf,#d9d6cf 10px,#cfcbc3 10px,#cfcbc3 20px);display:flex;align-items:center;justify-content:center;color:#555;font-size:16px}
</style></head><body><div class="p">
<div class="h"><div><div class="ag">CITY PARKING AUTHORITY</div><div class="sub">Red Light Camera Program · PA</div></div>
<div class="t">NOTICE OF<br>VIOLATION</div></div>
<div class="g">
<div><div class="l">Notice number</div><div class="v">RL1234567</div></div>
<div><div class="l">PIN</div><div class="v">5821</div></div>
<div><div class="l">Date and time</div><div class="v">${issued} 2:05 PM</div></div>
<div><div class="l">License plate</div><div class="v">NJT 4102 &nbsp;NJ</div></div>
<div><div class="l">Location</div><div class="v">Main St &amp; 1st Ave</div></div>
<div><div class="l">Violation</div><div class="v">Red light</div></div>
</div>
<div class="ph">[ camera photo ]</div>
<div class="amt"><div class="l">Amount due</div><div class="v">$100.00</div></div>
<div class="f">View or pay online at <b>pay.example.org</b> with your notice number and PIN.</div>
</div></body></html>`;

function labeller(lang) {
  let bundle = {};
  try { bundle = JSON.parse(fs.readFileSync(`${LOCALES}/${lang}/common.json`, 'utf8')); } catch (e) { /* */ }
  return (key, fallback) => {
    const raw = key.split('.').reduce((acc, part) => (acc && typeof acc === 'object' ? acc[part] : undefined), bundle);
    return typeof raw === 'string' && raw.trim() ? raw : fallback;
  };
}

const STAGE_OWNER_FN = function (owner) {
  const auth = JSON.parse(localStorage.getItem('aegis-auth-storage') || '{}');
  if (!auth.state || !auth.state.user) return null;
  auth.state.isAdmin = false; auth.state.isPartner = false; auth.state.isOwner = true;
  auth.state.user = { ...auth.state.user, isAdmin: false, isPartner: false, isOwner: true, ...owner };
  localStorage.setItem('aegis-auth-storage', JSON.stringify(auth));
  const app = JSON.parse(localStorage.getItem('aegis-app-storage') || '{"state":{},"version":0}');
  app.state = app.state || {}; app.state.selectedOwner = null;
  localStorage.setItem('aegis-app-storage', JSON.stringify(app));
  return auth.state.user.id;
};

const TIDY_FN = function () {
  document.querySelectorAll('header, nav').forEach((el) => { el.style.display = ''; });
  document.querySelectorAll('.bg-amber-400.text-amber-950, .pin-action-sandbox').forEach((el) => { el.style.visibility = 'hidden'; });
  Array.from(document.querySelectorAll('span, div, a, button'))
    .filter((el) => /^\s*(⚠\s*)?(sandbox|entorno de pruebas)\s*$/i.test(el.textContent || ''))
    .forEach((el) => { el.style.visibility = 'hidden'; });
  // Staged people and plates are made up and must be read: un-blur them.
  const staged = /Taylor|Avery|Drew|Quinn|Lane|Parker|Morgan|Casey|NJT4102|NJL8830|NJP5521|RL1234567|RL7730214|SC48810|PX902216|5821|BK-|INV-2026|DBT-|City Parking|Main St|example\.org|yourcompany@|Your Company/;
  Array.from(document.querySelectorAll('*'))
    .filter((el) => staged.test(el.textContent || '') && (el.textContent || '').length < 300)
    .forEach((el) => {
      for (let n = el; n && n !== document.body; n = n.parentElement) {
        n.classList.forEach((c) => { if (/pii|blur/i.test(c)) n.classList.remove(c); });
        if (n.style && n.style.filter) n.style.filter = '';
      }
    });
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null);
  for (let n = walker.nextNode(); n; n = walker.nextNode()) {
    const v = (n.nodeValue || '').trim();
    if (v === 'AA' || v === 'LW') n.nodeValue = n.nodeValue.replace(v, 'YC');
  }
};

const MEASURE_FN = function (want) {
  const W = window.innerWidth; const H = window.innerHeight;
  const vis = (el) => el.getClientRects().length > 0 && getComputedStyle(el).visibility !== 'hidden';
  const norm = (t) => (t || '').replace(/\s+/g, ' ').trim().toLowerCase();
  const out = {};
  want.forEach(([key, text, kind]) => {
    const t = norm(text);
    let el = null;
    if (kind === 'tag') el = Array.from(document.querySelectorAll(text)).find(vis) || null;
    else if (kind === 'btnlast') el = Array.from(document.querySelectorAll('button')).filter(vis).filter((b) => norm(b.textContent) === t).pop() || null;
    else if (kind === 'btn') el = Array.from(document.querySelectorAll('button, a')).filter(vis).find((b) => norm(b.textContent).startsWith(t) || norm(b.getAttribute('title')).startsWith(t));
    else if (kind === 'panel') {
      const c = Array.from(document.querySelectorAll('h1,h2,h3,div,span')).filter(vis).filter((n) => norm(n.textContent) === t);
      el = c[0] || null;
      while (el && el !== document.body && !/shadow/.test(el.className || '')) el = el.parentElement;
      if (el === document.body) el = null;
    }
    else if (kind === 'row') el = Array.from(document.querySelectorAll('tbody tr')).filter(vis).find((r) => norm(r.textContent).includes(t)) || null;
    else {
      const c = Array.from(document.querySelectorAll('h1,h2,h3,div,span,p,label,li')).filter(vis).filter((n) => norm(n.textContent).startsWith(t));
      c.sort((a, b) => (a.textContent || '').length - (b.textContent || '').length);
      el = c[0] || null;
    }
    if (!el) return;
    const r = el.getBoundingClientRect();
    out[key] = [r.left / W, r.top / H, r.width / W, r.height / H].map((v) => Math.round(v * 10000) / 10000);
  });
  return out;
};

const clickButton = (re) => async (page) => {
  const ok = await page.evaluate((src) => {
    const rx = new RegExp(src, 'i');
    const b = Array.from(document.querySelectorAll('button, a')).find((x) => rx.test((x.textContent || '').trim()));
    if (b) b.click();
    return !!b;
  }, re);
  if (!ok) throw new Error(`no button /${re}/`);
  await sleep(1500);
};
const rowMenu = (text) => async (page) => {
  const ok = await page.evaluate((t) => {
    const r = Array.from(document.querySelectorAll('tbody tr')).find((x) => (x.textContent || '').includes(t));
    const b = r && r.querySelector('button');
    if (b) b.click();
    return !!b;
  }, text);
  if (!ok) throw new Error(`no row ${text}`);
  await sleep(1000);
};
const upload = (file) => async (page) => {
  const input = await page.$('input[type="file"]');
  if (!input) throw new Error('no file input');
  await input.uploadFile(file);
  await sleep(2500);
};
const hideToasts = async (page) => {
  await page.evaluate(() => document.querySelectorAll('[role="status"]').forEach((el) => {
    const box = el.closest('div[style]'); (box || el).style.visibility = 'hidden';
  }));
};
const waitToasts = async (page) => { await sleep(4500); await hideToasts(page); };
const tab = (label) => clickButton(`^${label}`);

// ------------------------------------------------------------------ screens

function screens(L, ticketFile) {
  const add = L('violationNotice.addButton', 'Add mailed ticket');
  const title = L('violationNotice.title', 'Add mailed ticket');
  const save = L('violationNotice.save', 'Save ticket');
  const info = L('ownerViolations.info', 'Info');
  return [
    { name: 'nov-01-violations', path: '/violations', list: VIOLATIONS,
      measure: [['add', add, 'btn'], ['find', L('ownerViolations.findViolations', 'Find Violations'), 'btn'],
        ['table', 'table', 'tag'], ['row1', 'SC48810', 'row'], ['thead', 'thead', 'tag']] },
    { name: 'nov-02-row-menu', path: '/violations', list: VIOLATIONS, steps: [rowMenu('SC48810')],
      measure: [['row1', 'SC48810', 'row'], ['info', info, 'btn'], ['bookings', L('ownerViolations.bookings', 'Bookings'), 'btn'],
        ['cash', L('ownerViolations.settleCash', 'Paid by cash'), 'btn']] },
    { name: 'nov-03-notice-empty', path: '/violations', list: VIOLATIONS, steps: [clickButton(`^${add}$`)],
      measure: [['modal', title, 'panel'], ['upload', L('violationNotice.uploadPhoto', 'Upload a photo'), 'btn'],
        ['car', 'select', 'tag'], ['save', save, 'btnlast']] },
    { name: 'nov-04-notice-read', path: '/violations', list: VIOLATIONS, steps: [clickButton(`^${add}$`), upload(ticketFile), waitToasts],
      measure: [['modal', title, 'panel'], ['car', 'select', 'tag'], ['save', save, 'btnlast'],
        ['citation', L('violationNotice.citation', 'Citation / notice number'), 'text'], ['pin', L('violationNotice.pin', 'PIN'), 'text'],
        ['issued', L('violationNotice.issued', 'Date and time on the ticket'), 'text'],
        ['state', L('violationNotice.issuingState', 'State of the agency'), 'text'],
        ['hint', L('violationNotice.timeHint', 'Enter the time exactly as printed').slice(0, 30), 'text']] },
    { name: 'nov-05-notice-saved', path: '/violations', list: VIOLATIONS, after: [MAILED, ...VIOLATIONS],
      steps: [clickButton(`^${add}$`), upload(ticketFile), hideToasts, clickButton(`^${save}$`)],
      measure: [['row1', 'RL1234567', 'row'], ['toasts', '[role="status"]', 'tag']] },
    { name: 'nov-07-notice-row', path: '/violations', list: [MAILED, ...VIOLATIONS],
      measure: [['row1', 'RL1234567', 'row'], ['thead', 'thead', 'tag']] },
    { name: 'nov-06-notice-info', path: '/violations', list: [MAILED, ...VIOLATIONS], steps: [rowMenu('RL1234567'), clickButton(`^${info}$`)],
      measure: [['modal', L('ownerViolations.violationInfo', 'Violation Info'), 'panel'],
        ['source', L('violationNotice.sourceManual', 'Mailed ticket, entered by hand'), 'text'],
        ['booking', 'BK-30917', 'text']] },
    { name: 'nov-10-col-refused', path: '/payments/collections', cases: CASES,
      steps: [tab(L('collectionsQueue.tabFailed', 'Refused'))],
      measure: [['tab', L('collectionsQueue.tabFailed', 'Refused'), 'btn'], ['row1', 'Lane', 'row'],
        ['retry', L('collectionsQueue.retryPlacement', 'Place again'), 'btn'],
        ['open', L('collectionsQueue.openAgencyStep', 'Open the agency page'), 'btn']] },
    { name: 'nov-11-col-placed', path: '/payments/collections', cases: CASES,
      steps: [tab(L('collectionsQueue.tabPlaced', 'With the agency'))],
      measure: [['tab', L('collectionsQueue.tabPlaced', 'With the agency'), 'btn'], ['row1', 'Parker', 'row'],
        ['case', 'DBT-50288', 'btn']] },
  ];
}

// ------------------------------------------------------------------ run

(async () => {
  const browser = await puppeteer.connect({ browserURL: `http://127.0.0.1:${CDP_PORT}`, defaultViewport: VIEWPORT, protocolTimeout: 600000 });
  const page = await browser.newPage();
  await page.setViewport(VIEWPORT);
  page.setDefaultNavigationTimeout(60000);
  page.on('dialog', (d) => d.dismiss().catch(() => {}));

  // The ticket: one picture for both languages (a US notice is printed in English), and the file "uploaded".
  const issuedUs = `${p2(ISSUED.getUTCMonth() + 1)}/${p2(ISSUED.getUTCDate())}/${ISSUED.getUTCFullYear()}`;
  const ticketFile = path.join(SHOTS, '_nov', 'ticket.jpg');
  fs.mkdirSync(path.dirname(ticketFile), { recursive: true });
  if (!ONLY.length || ONLY.some((o) => 'nov-00-ticket'.includes(o) || o.startsWith('nov-0'))) {
    await page.setContent(TICKET_HTML(issuedUs), { waitUntil: 'load' });
    const png = await page.screenshot();
    for (const lang of LANGS) { fs.mkdirSync(path.join(SHOTS, lang), { recursive: true }); fs.writeFileSync(path.join(SHOTS, lang, 'nov-00-ticket.png'), png); }
    await page.setViewport({ width: 1000, height: 1000, deviceScaleFactor: 1 });
    fs.writeFileSync(ticketFile, await page.screenshot({ type: 'jpeg', quality: 85, clip: { x: 300, y: 0, width: 1000, height: 1000 } }));
    await page.setViewport(VIEWPORT);
    console.log('nov-00-ticket');
  }

  await page.goto(`${BASE}/dashboard`, { waitUntil: 'domcontentloaded' });
  await sleep(1500);
  const saved = await page.evaluate(() => ({ auth: localStorage.getItem('aegis-auth-storage'), app: localStorage.getItem('aegis-app-storage') }));
  if (!saved.auth || !JSON.parse(saved.auth).state?.token) throw new Error('nobody is signed in on dev-owner in this Chrome');

  let current = null;
  let savedOnce = false;
  const blocked = [];
  await page.setRequestInterception(true);
  page.on('request', (req) => {
    const url = req.url(); const m = req.method();
    const json = (body, status = 200) => req.respond({ status, contentType: 'application/json', body: JSON.stringify(body) }).catch(() => {});
    if (current) {
      if (m === 'GET' && /\/api\/owner-violations\/plugins/i.test(url)) return json([{ key: 'demo-agency', canSearchByPlate: true, endpointCount: 3 }]);
      if (m === 'GET' && /\/api\/owner-violations\/progress\//i.test(url)) return json({ ownerId: 'self', status: 'not_found', progress: 0 });
      if (m === 'GET' && /\/api\/owner-violations(\?|$)/i.test(url)) return json(listOf(savedOnce && current.after ? current.after : current.list || []));
      if (m === 'POST' && /\/api\/owner-violations\/notice\/read/i.test(url)) return json(READ);
      if (m === 'POST' && /\/api\/owner-violations\/notice(\?|$)/i.test(url)) { savedOnce = true; return json(SAVED); }
      if (m === 'GET' && /\/api\/Cars\/AllCarList\/[^/?]+/i.test(url)) return json({ result: CARS, reason: 0 });
      if (m === 'POST' && /\/api\/Cars\/AllCarList(\?|$)/i.test(url)) return json({ result: CARS, reason: 0 });
      if (m === 'GET' && /\/api\/Collections\/cases(\?|$)/i.test(url)) {
        const st = new URL(url).searchParams.get('status');
        return json((current.cases || []).filter((c) => !st || st === 'all' || c.status === st));
      }
    }
    if (m !== 'GET' && m !== 'HEAD' && m !== 'OPTIONS' && /\/api\//i.test(url)) {
      blocked.push(`${m} ${url}`);
      return req.abort('blockedbyclient').catch(() => {});
    }
    return req.continue().catch(() => {});
  });

  const blurArgs = [REDACTION.markerSource(), REDACTION.PII_CLASS, RENAME];
  const failures = [];
  const boxesFile = path.join(SHOTS, '_nov_boxes.json');
  const boxes = fs.existsSync(boxesFile) ? JSON.parse(fs.readFileSync(boxesFile, 'utf8')) : {};

  for (const lang of LANGS) {
    fs.mkdirSync(path.join(SHOTS, lang), { recursive: true });
    const L = labeller(lang);
    for (const s of screens(L, ticketFile).filter((x) => !ONLY.length || ONLY.some((o) => x.name.includes(o)))) {
      process.stdout.write(`[${lang}] ${s.name}\n`);
      current = s; savedOnce = false;
      try {
        await page.goto(`${BASE}/dashboard`, { waitUntil: 'domcontentloaded' });
        await page.evaluate(STAGE_OWNER_FN, OWNER);
        await page.goto(`${BASE}${s.path}`, { waitUntil: 'domcontentloaded' });
        for (let i = 0; i < 2; i += 1) { await setLanguage(page, lang); await page.reload({ waitUntil: 'domcontentloaded' }); await sleep(1500); }
        await waitForApp(page);
        await sleep(SETTLE_MS);
        for (const step of s.steps || []) await step(page);
        await sleep(1000);
        await page.evaluate(BLUR_FN, ...blurArgs);
        await page.evaluate(TIDY_FN);
        // The dialog holds only the staged ticket: its date field must read.
        await page.evaluate(() => document.querySelectorAll('[role="dialog"] input, [role="dialog"] select').forEach((el) => {
          for (let n = el; n && n !== document.body; n = n.parentElement) {
            n.classList.forEach((c) => { if (/pii|blur/i.test(c)) n.classList.remove(c); });
            if (n.style && n.style.filter) n.style.filter = '';
          }
        }));
        await sleep(500);
        boxes[`${lang}/${s.name}`] = await page.evaluate(MEASURE_FN, s.measure);
        fs.writeFileSync(path.join(SHOTS, lang, `${s.name}.png`), await page.screenshot());
      } catch (err) {
        console.log(`  FAILED: ${err.message}`);
        failures.push({ lang, name: s.name, error: err.message });
      }
    }
  }

  current = null;
  await page.goto(`${BASE}/dashboard`, { waitUntil: 'domcontentloaded' }).catch(() => {});
  await page.evaluate((v) => {
    if (v.auth) localStorage.setItem('aegis-auth-storage', v.auth);
    if (v.app) localStorage.setItem('aegis-app-storage', v.app);
  }, saved).catch(() => {});
  fs.writeFileSync(boxesFile, JSON.stringify(boxes, null, 2));
  if (blocked.length) console.log(`\nWrites blocked (nothing saved):\n  ${blocked.slice(0, 20).join('\n  ')}`);
  console.log(`\nDone. ${failures.length ? 'Failures: ' + JSON.stringify(failures) : 'all captured'}`);
  await page.close().catch(() => {});
  await browser.disconnect();
})().catch((e) => { console.error('FATAL', e); process.exit(1); });
