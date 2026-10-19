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
 * Screenshots for episodes 52 (Turo: trips from emails that arrived earlier — "Re-read Turo emails") and 53
 * (refer one booking to collections by hand), from the DEV portal, with DEMO DATA.
 *
 * The session is shown as an OWNER's (admin flags switched off in the browser). Everything these screens list is
 * staged: the pending Turo bookings, the re-read status, the owner's bookings, the referral preview and the case in
 * the Collections queue — made-up drivers and cars, no real person. The page is the real deployed portal.
 *
 * READ-ONLY BY CONSTRUCTION. The two writes the episodes show (start a re-read, refer a booking) are answered here;
 * every other API request that is not a GET is aborted before it leaves the browser.
 *
 * Usage:
 *   node capture-oct-features.js --cdp=9223
 *   node capture-oct-features.js --cdp=9223 --only=oct-1 --lang=es
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

if (!/^https:\/\/dev-/.test(BASE)) throw new Error(`refusing a non-dev base: ${BASE}`);

const OWNER = { firstName: 'Your Company', lastName: '', email: 'yourcompany@mail.myeztoll.com' };
const RENAME = [
  ['Aegis AG Soft LLC', 'Your Company'], ['Aegis AA Soft LLC', 'Your Company'], ['AEGIS AG SOFT', 'YOUR COMPANY'],
  ['ELIZAVETA GAEVAYA', 'YOUR COMPANY'], ['Elizaveta Gaevaya', 'Your Company'], ['Luxury Wheels Away', 'Your Company'],
  ['aegisagsoft@gmail.com', 'yourcompany@mail.myeztoll.com'], ['aegisaasoft@outlook.com', 'yourcompany@mail.myeztoll.com'],
  ['aegis admin', 'Your Company'], ['Luxury wheels away', 'Your Company'], ['luxurywheelsaway@gmail.com', 'yourcompany@mail.myeztoll.com'],
];

const day = (d, h = 15) => { const t = new Date(Date.now() + d * 86400000); t.setUTCHours(h, 0, 0, 0); return t.toISOString(); };

// ------------------------------------------------------------------ staged data

const pending = (n, make, model, year, first, last, start, days, earn, driverMatch) => ({
  id: `demo-pb-${n}`, ownerId: 'self', pluginName: 'turo', externalReservationId: `5${n}1203${n}4`,
  status: 'PendingConfirmation', lastEventType: 'Created', vehicleMakeRaw: make, vehicleModelRaw: model,
  vehicleYearRaw: year, matchedCarId: null, carMatchType: 'None', externalVehicleId: null,
  driverFirstName: first, driverLastName: last, driverPhone: '+1 555 010 0' + n + '0', driverEmail: null,
  matchedDriverUserId: null, pendingDriverId: null, driverMatchType: driverMatch, tripStartUtc: day(start, 16),
  tripEndUtc: day(start + days, 16), earnings: earn, milesIncluded: 200, locationText: 'Newark, NJ', deliveryText: null,
  rawEmailMessageId: null, created: day(0), updated: day(0), confirmedBookingId: null,
});
const PENDING_SOME = [pending(1, 'Nissan', 'Altima', 2024, 'Jordan', 'Reyes', -1, 3, 186.4, 'Exact'),
  pending(2, 'Dodge', 'Durango', 2026, 'Casey', 'Morgan', 4, 2, 241.0, 'None')];
const PENDING_ALL = [...PENDING_SOME, pending(3, 'Mazda', 'CX-5', 2026, 'Riley', 'Brooks', -3, 4, 302.15, 'None')];
const PLUGINS = [{
  family: 'rental', authMode: 'ChallengeFlow', platformId: 'turo', platformName: 'Turo', supportedRegions: [],
  credentialFields: [], isConfigured: true, secretsPresent: {}, supportsManualBookingFetch: false,
  supportsPasswordLogin: false, supportsEmailOtp: true, supportsSmsOtp: false, requiresCaptcha: false,
  emailNotificationDomains: ['turo.com'], connected: false,
}];

const booking = (n, first, last, car, model, plate, year, from, to, failed, toll) => ({
  id: `demo-bk-${n}`, bookingId: `demo-bk-${n}`, carId: `demo-car-${n}`, renterId: `demo-driver-${n}`,
  renterFirstName: first, renterLastName: last, renterPhoneNumber: '+1 555 010 0' + n + '1', renterEmail: null,
  dateFrom: day(from, 14), dateTo: day(to, 14), status: 7, price: 0, carTitle: `${car} ${model}`, carModel: model,
  carBrand: car, carPlateNumber: plate, carPlateNumberState: 'NJ', carYear: year,
  paymentStatusCode: failed ? 'failed' : 'paid', paymentStatusNote: failed ? 'Card declined' : null,
  tollAmount: toll, origin: 'manual', originName: 'MyEZToll', approvalFlags: 0,
});
const BOOKINGS = {
  items: [
    booking(1, 'Taylor', 'Quinn', 'Toyota', 'Camry', 'NJT4102', 2025, -24, -18, true, 612.5),
    booking(2, 'Avery', 'Lane', 'Honda', 'Accord', 'NJL8830', 2024, -15, -12, false, 38.2),
    booking(3, 'Drew', 'Parker', 'Hyundai', 'Sonata', 'NJP5521', 2026, -9, -7, false, 12.75),
  ],
  totalCount: 3, page: 1, pageSize: 25,
};
const PREVIEW = {
  bookingId: 'demo-bk-1', canRefer: true, blockers: [], warnings: [],
  principal: 612.5, fee: 262.5, claim: 875.0, currency: 'USD', lineCount: 14,
  agencyKey: 'debitura', agencyName: 'Debitura', commissionPercent: 30, agencyMinimum: 500,
  agencyPlacesAutomatically: true, debtorName: 'Taylor Quinn', debtorCountry: 'US', debtorRegion: 'US-NJ',
  hasEmail: true, hasPhone: true, hasAddress: true, isTuroBooking: false,
};
const CASE = {
  id: 'demo-case-1', status: 'Approved', createdAtUtc: day(0), bookingId: 'demo-bk-1', vehicleLabel: 'Toyota Camry NJT4102',
  bookingFromUtc: day(-24, 14), bookingToUtc: day(-18, 14), driverUserId: 'demo-driver-1', driverName: 'Taylor Quinn',
  driverEmail: null, driverCountry: 'US', invoiceId: 'demo-inv-1', invoiceNumber: 'INV-20261019-4F2A10',
  principalAmount: 612.5, collectionFeeAmount: 262.5, claimAmount: 875.0, currency: 'USD', daysOverdue: 18,
  lettersSent: 0, deliveryProof: 'None', deliveryUnconfirmed: true, agencyPluginKey: 'debitura',
  agencyCommissionPercent: 30, approvedAtUtc: day(0), approvedByUserId: 'self', declineReason: null, recoveredAmount: null,
};

// ------------------------------------------------------------------ helpers

function labeller(lang) {
  let bundle = {};
  try { bundle = JSON.parse(fs.readFileSync(`C:/aegis-aa/_wt-reread-ow/src/locales/${lang}/common.json`, 'utf8')); } catch (e) { /* */ }
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
  const staged = /Jordan|Casey|Riley|Taylor|Avery|Drew|Reyes|Morgan|Brooks|Quinn|Lane|Parker|NJT4102|NJL8830|NJP5521|INV-2026|yourcompany@|Your Company/;
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
const rightClickRow = (text) => async (page) => {
  const box = await page.evaluate((t) => {
    const r = Array.from(document.querySelectorAll('tbody tr')).find((x) => (x.textContent || '').includes(t));
    if (!r) return null;
    const b = r.getBoundingClientRect();
    return { x: b.left + b.width * 0.3, y: b.top + b.height / 2 };
  }, text);
  if (!box) throw new Error(`no row ${text}`);
  await page.mouse.click(box.x, box.y, { button: 'right' });
  await sleep(1000);
};
const tick = async (page) => {
  await page.evaluate(() => { const c = document.querySelector('input[type="checkbox"]'); if (c) c.click(); });
  await sleep(600);
};

// ------------------------------------------------------------------ screens

function screens(L) {
  const reread = L('pendingBookings.rereadEmails', 'Re-read {{platform}} emails').replace('{{platform}}', 'Turo');
  const refer = L('referToCollections.menu', 'Refer to collections');
  return [
    { name: 'oct-01-turo-idle', path: '/p2p-bookings/turo', pending: [], status: { running: false, total: 0, done: 0 }, steps: [],
      measure: [['reread', reread, 'btn'], ['csv', L('turoEarnings.cardTitle', 'Turo earnings CSV'), 'btn']] },
    { name: 'oct-02-turo-running', path: '/p2p-bookings/turo', pending: PENDING_SOME, status: { running: true, total: 23, done: 7 }, steps: [],
      measure: [['reread', reread, 'btn'], ['strip', '[role="status"]', 'tag'], ['row1', 'Altima', 'row']] },
    { name: 'oct-03-turo-done', path: '/p2p-bookings/turo', pending: PENDING_ALL, status: { running: false, total: 23, done: 23 }, steps: [],
      measure: [['reread', reread, 'btn'], ['row1', 'Altima', 'row'], ['row3', 'CX-5', 'row'], ['table', 'table', 'tag']] },
    { name: 'oct-11-bookings-menu', path: '/bookings', steps: [rightClickRow('Quinn')],
      measure: [['row1', 'Quinn', 'row'], ['refer', refer, 'btn']] },
    { name: 'oct-12-refer-preview', path: '/bookings', steps: [rightClickRow('Quinn'), clickButton(`^${refer}$`)],
      measure: [['modal', L('referToCollections.title', 'Refer to collections'), 'panel']] },
    { name: 'oct-13-refer-confirmed', path: '/bookings', steps: [rightClickRow('Quinn'), clickButton(`^${refer}$`), tick],
      measure: [['modal', L('referToCollections.title', 'Refer to collections'), 'panel'], ['checkbox', 'input[type="checkbox"]', 'tag'],
        ['submit', `${L('referToCollections.submit', 'Refer to collections')}`, 'btnlast']] },
    { name: 'oct-14-refer-done', path: '/bookings', steps: [rightClickRow('Quinn'), clickButton(`^${refer}$`), tick, clickButton(`^${refer}$`)],
      measure: [['modal', L('referToCollections.title', 'Refer to collections'), 'panel'], ['open', L('referToCollections.openQueue', 'Open Collections'), 'btn']] },
    { name: 'oct-15-collections-approved', path: '/payments/collections',
      steps: [clickButton(`^${L('collectionsQueue.tabApproved', 'Approved')}`)],
      measure: [['row1', 'Quinn', 'row'], ['tab', L('collectionsQueue.tabApproved', 'Approved'), 'btn']] },
  ];
}

// ------------------------------------------------------------------ run

(async () => {
  const browser = await puppeteer.connect({ browserURL: `http://127.0.0.1:${CDP_PORT}`, defaultViewport: VIEWPORT, protocolTimeout: 600000 });
  const page = await browser.newPage();
  await page.setViewport(VIEWPORT);
  page.setDefaultNavigationTimeout(60000);
  page.on('dialog', (d) => d.dismiss().catch(() => {}));

  await page.goto(`${BASE}/dashboard`, { waitUntil: 'domcontentloaded' });
  await sleep(1500);
  const saved = await page.evaluate(() => ({ auth: localStorage.getItem('aegis-auth-storage'), app: localStorage.getItem('aegis-app-storage') }));
  if (!saved.auth || !JSON.parse(saved.auth).state?.token) throw new Error('nobody is signed in on dev-owner in this Chrome');

  let current = null;
  const blocked = [];
  await page.setRequestInterception(true);
  page.on('request', (req) => {
    const url = req.url(); const m = req.method();
    const json = (body, status = 200) => req.respond({ status, contentType: 'application/json', body: JSON.stringify(body) }).catch(() => {});
    if (current) {
      if (m === 'GET' && /\/api\/OwnerPendingBookings\/bookings/i.test(url)) return json(current.pending || []);
      if (m === 'GET' && /\/api\/OwnerPendingBookings\/drivers/i.test(url)) return json([]);
      if (m === 'GET' && /\/booking-plugins\/turo\/reread-emails\/status/.test(url)) return json(current.status || { running: false, total: 0, done: 0 });
      if (m === 'GET' && /\/api\/owners\/[^/]+\/booking-plugins(\?|$)/.test(url)) return json(PLUGINS);
      if (m === 'GET' && /\/api\/Booking\/get-owner-bookings-paged/i.test(url)) return json({ result: BOOKINGS, reason: 0 });
      if (m === 'GET' && /\/api\/Collections\/manual-referral\/preview/i.test(url)) return json(PREVIEW);
      if (m === 'POST' && /\/api\/Collections\/manual-referral(\?|$)/i.test(url)) return json({ caseId: 'demo-case-1', status: 'Approved', preview: PREVIEW });
      if (m === 'GET' && /\/api\/Collections\/cases(\?|$)/i.test(url)) return json([CASE]);
    }
    if (m !== 'GET' && m !== 'HEAD' && m !== 'OPTIONS' && /\/api\//i.test(url)) {
      blocked.push(`${m} ${url}`);
      return req.abort('blockedbyclient').catch(() => {});
    }
    return req.continue().catch(() => {});
  });

  const blurArgs = [REDACTION.markerSource(), REDACTION.PII_CLASS, RENAME];
  const failures = [];
  const boxesFile = path.join(SHOTS, '_oct_boxes.json');
  const boxes = fs.existsSync(boxesFile) ? JSON.parse(fs.readFileSync(boxesFile, 'utf8')) : {};

  for (const lang of LANGS) {
    fs.mkdirSync(path.join(SHOTS, lang), { recursive: true });
    const L = labeller(lang);
    for (const s of screens(L).filter((x) => !ONLY.length || ONLY.some((o) => x.name.includes(o)))) {
      process.stdout.write(`[${lang}] ${s.name}\n`);
      current = s;
      try {
        await page.goto(`${BASE}/dashboard`, { waitUntil: 'domcontentloaded' });
        await page.evaluate(STAGE_OWNER_FN, OWNER);
        await page.goto(`${BASE}${s.path}`, { waitUntil: 'domcontentloaded' });
        for (let i = 0; i < 2; i += 1) { await setLanguage(page, lang); await page.reload({ waitUntil: 'domcontentloaded' }); await sleep(1500); }
        await waitForApp(page);
        await sleep(SETTLE_MS);
        for (const step of s.steps) await step(page);
        await sleep(1000);
        await page.evaluate(BLUR_FN, ...blurArgs);
        await page.evaluate(TIDY_FN);
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
