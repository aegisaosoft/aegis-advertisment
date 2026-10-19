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
 * Screenshots for the Tesla episodes (46-50), from the DEV portal, with DEMO DATA.
 *
 * No Tesla is connected to any of our accounts yet, so the Tesla card, its cars and their key states
 * are supplied here: the GPS Systems tab's own API answers are replaced in the browser with a made-up
 * fleet (the VINs below end in 0001xx and belong to no real car). The page itself is the real,
 * deployed owner portal — only the data under it is staged. Episode 50 (the Supercharger page, `tes-1N-*`)
 * stages the page's /api/supercharger-sessions answer the same way: six made-up sessions on the same VINs.
 *
 * READ-ONLY BY CONSTRUCTION. Every request to the API that is not a GET is aborted before it leaves
 * the browser, except the "Check cars" and "Import from Tesla" calls, which are answered here with staged
 * results and never reach the server.
 *
 * Like capture-payments.js this runs against an administrator session in a Chrome started with
 * --remote-debugging-port, signed in on dev-owner. The admin-only "Tesla for Business" card is hidden
 * in every frame except the business ones (episode 49 is the one that shows it).
 *
 * Usage:
 *   node capture-tesla.js --cdp=9223
 *   node capture-tesla.js --cdp=9223 --only=tes-05 --lang=es
 */

const fs = require('fs');
const path = require('path');
const puppeteer = require('C:/aegis-aa/node_modules/puppeteer-core');
const REDACTION = require('C:/aegis-aa/docs/tools/redaction-rules');
const { BLUR_FN, clickText, waitForApp, setLanguage, sleep } = require('./capture-common');

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

const RENAME = [
  ['Aegis AG Soft LLC', 'Your Company'],
  ['Aegis AA Soft LLC', 'Your Company'],
  ['ELIZAVETA GAEVAYA', 'YOUR COMPANY'],
  ['Elizaveta Gaevaya', 'Your Company'],
  ['Luxury Wheels Away', 'Your Company'],
  ['aegisagsoft@gmail.com', 'yourcompany@mail.myeztoll.com'],
  ['aegisaasoft@outlook.com', 'yourcompany@mail.myeztoll.com'],
  ['aegis admin', 'Your Company'],
];

// ------------------------------------------------------------------ the staged fleet

const VIN = {
  y23: '7SAYGDEE0PA000101',   // Model Y 2023
  m322: '5YJ3E1EB8NF000102',  // Model 3 2022
  y24: '7SAYGDEE6RF000103',   // Model Y 2024
  s20: '5YJSA1E40LF000104',   // Model S 2020 (old firmware in the mixed state)
};
const ALL = [VIN.y23, VIN.m322, VIN.y24, VIN.s20];
const PAIRING = 'https://tesla.com/_ak/owner.myeztoll.com';

const PROVIDERS = [
  ['bouncie', 'Bouncie', 'oauth'], ['geotab', 'Geotab', 'credentials'], ['samsara', 'Samsara', 'oauth'],
  ['tesla', 'Tesla', 'oauth'], ['tracki', 'Tracki', 'credentials'], ['zubie', 'Zubie', 'oauth'],
].map(([providerId, providerName, authKind]) => ({ providerId, providerName, authKind, credentialFields: [] }));

const teslaAccount = (nickname) => ({
  providerId: 'tesla', nickname: nickname || null, isActive: true, isConfigured: true, secretsPresent: {},
  lastScrapeAtUtc: new Date(Date.now() - 4 * 60 * 1000).toISOString(), lastScrapeStatus: 'ok', consecutiveFailures: 0,
});

const STATUS = {
  mixed: {
    vins: ALL, keyPairedVins: [VIN.y23, VIN.y24, VIN.s20], keyMissingVins: [VIN.m322], configuredVehicles: 2,
    skipped: { unsupported_firmware: [VIN.s20] }, pairingUrl: PAIRING, problem: null,
  },
  sheet: {
    vins: ALL, keyPairedVins: [VIN.y23], keyMissingVins: [VIN.m322, VIN.y24, VIN.s20], configuredVehicles: 1,
    skipped: {}, pairingUrl: PAIRING, problem: null,
  },
  all: {
    vins: ALL, keyPairedVins: ALL, keyMissingVins: [], configuredVehicles: 4,
    skipped: {}, pairingUrl: PAIRING, problem: null,
  },
};

const PENDING = {
  pending: [{
    id: 'demo-pending-1', providerId: 'tesla', imei: VIN.m322, vin: VIN.m322, plate: null, plateState: null,
    make: 'Tesla', model: 'Model 3', year: 2022, title: 'Model 3', reason: 'unmatched',
    createdAt: new Date().toISOString(),
  }],
  linkableCars: [
    { id: 'demo-car-1', make: 'Tesla', model: 'Model 3', year: 2022, plate: 'KRT4102', vin: null, title: null },
    { id: 'demo-car-2', make: 'Toyota', model: 'Camry', year: 2021, plate: 'NJL8830', vin: null, title: null },
  ],
};

// The Supercharger page (episode 50): one session per state the "Renter charge" chip can show, newest first.
const daysAgo = (d, h) => {
  const t = new Date(Date.now() - d * 86400000);
  t.setUTCHours(h, 12, 0, 0);
  return t.toISOString();
};
const session = (n, vin, car, plate, site, start, energy, idle, extra) => ({
  id: `demo-sc-${n}`, sessionId: `DEMO-${4810 + n}`, vin, carId: `demo-car-${n}`, carTitle: car,
  licensePlate: plate, state: 'NJ', siteName: site, countryCode: 'US',
  chargeStartUtc: start, chargeStopUtc: new Date(Date.parse(start) + 38 * 60000).toISOString(),
  energyKwh: Math.round((energy / 0.48) * 10) / 10, energyAmount: energy, idleFeeAmount: idle,
  amount: Math.round((energy + idle) * 100) / 100, currency: 'USD', ownerPaid: true, hasInvoice: true,
  source: 'history', bookingId: null, renterName: null, chargeStatus: 'NotCharged', chargeError: null,
  chargedAt: null, ...extra,
});
// Dashless: TIDY_FN strips anything shaped like a GUID, which would leave the Info line empty.
const booked = (n, renter) => ({ bookingId: `5e1d0c${n}a7b2f4c119d3e00000000000${n}`, renterName: renter });
const SESSIONS = [
  session(1, VIN.y23, 'Tesla Model Y 2023', 'KRT4102', 'Secaucus, NJ', daysAgo(1, 15), 18.4, 0,
    { ...booked(1, 'Jamie Carter') }),
  session(2, VIN.m322, 'Tesla Model 3 2022', 'NJL8830', 'Newark Airport, NJ', daysAgo(3, 21), 22.75, 6,
    { ...booked(2, 'Morgan Lee'), chargeStatus: 'Charged', chargedAt: daysAgo(3, 23) }),
  session(3, VIN.y24, 'Tesla Model Y 2024', 'PTX5521', 'Edison, NJ', daysAgo(5, 13), 15.1, 0,
    { ...booked(3, 'Riley Brooks'), ownerPaid: false }),
  session(4, VIN.s20, 'Tesla Model S 2020', 'HVW2093', 'Paramus, NJ', daysAgo(8, 17), 31.2, 0, {}),
  session(5, VIN.m322, 'Tesla Model 3 2022', 'NJL8830', 'Woodbridge, NJ', daysAgo(11, 19), 12.6, 0,
    { ...booked(5, 'Casey Nguyen'), chargeStatus: 'ChargeFailed', chargeError: 'No payment method on file for renter' }),
  session(6, VIN.y23, 'Tesla Model Y 2023', 'KRT4102', 'Clinton, NJ', daysAgo(14, 12), 19.8, 0,
    { ...booked(6, 'Jordan Patel'), chargeStatus: 'Charged', chargedAt: daysAgo(14, 14) }),
];
// With rebilling off nothing has been charged, so every session is still waiting.
const SC = {
  on: { items: SESSIONS, totalCount: SESSIONS.length, chargingEnabled: true, feeMode: 'Percent', fee: 10 },
  off: {
    items: SESSIONS.map((r) => ({ ...r, chargeStatus: 'NotCharged', chargedAt: null, chargeError: null })),
    totalCount: SESSIONS.length, chargingEnabled: false, feeMode: 'Percent', fee: 10,
  },
};
const SC_IMPORT = { ownerId: 'demo', fetched: 6, inserted: 1, updated: 5, withBooking: 5, problem: null };

// ------------------------------------------------------------------ helpers

function labeller(lang) {
  let bundle = {};
  try {
    bundle = JSON.parse(fs.readFileSync(`C:/aegis-aa/aegis-owner-web/src/locales/${lang}/common.json`, 'utf8'));
  } catch (e) { /* English fallbacks */ }
  return (key, fallback) => {
    const raw = key.split('.').reduce((acc, part) => (acc && typeof acc === 'object' ? acc[part] : undefined), bundle);
    return typeof raw === 'string' && raw.trim() ? raw : fallback;
  };
}

/** Hide what an owner's frame never shows: the admin business card, the sandbox badge, GUIDs, "AA". */
const TIDY_FN = function (showBusiness) {
  document.querySelectorAll('.bg-amber-400.text-amber-950, .pin-action-sandbox')
    .forEach((el) => { el.style.visibility = 'hidden'; });
  // The dev environment's badge: the smallest element reading just "SANDBOX".
  Array.from(document.querySelectorAll('span, div, a, button'))
    .filter((el) => /^\s*sandbox\s*$/i.test(el.textContent || ''))
    .forEach((el) => { el.style.visibility = 'hidden'; });
  // The staged VINs (ending 0001xx) are made up, and the viewer has to read them: un-blur those only.
  Array.from(document.querySelectorAll('*'))
    .filter((el) => el.children.length === 0 && /[A-HJ-NPR-Z0-9]{11}0001\d\d/.test(el.textContent || ''))
    .forEach((el) => {
      for (let n = el; n && n !== document.body; n = n.parentElement) {
        n.classList.forEach((c) => { if (/pii|blur/i.test(c)) n.classList.remove(c); });
        if (n.style && n.style.filter) n.style.filter = '';
      }
    });
  if (!showBusiness) {
    Array.from(document.querySelectorAll('div'))
      .filter((d) => /^tesla for business/i.test((d.textContent || '').trim()) && d.className.includes('border'))
      .forEach((d) => { (d.parentElement || d).style.display = 'none'; });
  }
  const GUID = /\s*\(?[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\)?/gi;
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null);
  for (let n = walker.nextNode(); n; n = walker.nextNode()) {
    const v = n.nodeValue || '';
    if (GUID.test(v)) n.nodeValue = v.replace(GUID, '');
    GUID.lastIndex = 0;
    if (v.trim() === 'AA') n.nodeValue = v.replace('AA', 'YC');
  }
};

/**
 * The shared redaction pass hides header, nav and footer — right for the isolated admin cards it was
 * written for, wrong here: the Settings tabs and the sidebar are <nav>, and these frames are meant to
 * look like the portal (the written guide's GPS screens show header and sidebar). Bring back header
 * and nav; the footer, which carries contact details, stays hidden.
 */
const RESTORE_CHROME_FN = function () {
  document.querySelectorAll('header, nav').forEach((el) => { el.style.display = ''; });
};

/**
 * Where the things an episode points at landed, as fractions of the 1600x1000 frame — what series_o.py
 * rings and points the cursor at, measured instead of guessed (and re-measured per language, where a
 * longer label moves a button). `want` is [key, text, kind]: kind 'btn' = a button/link starting with
 * text, 'box' = the bordered card around the element starting with text, 'el' = that element itself.
 */
const MEASURE_FN = function (want) {
  const W = window.innerWidth;
  const H = window.innerHeight;
  const vis = (el) => el.getClientRects().length > 0 && getComputedStyle(el).visibility !== 'hidden';
  const norm = (t) => (t || '').replace(/\s+/g, ' ').trim().toLowerCase();
  const out = {};
  want.forEach(([key, text, kind]) => {
    const t = norm(text);
    let el = null;
    if (kind === 'tag') {
      el = Array.from(document.querySelectorAll(text)).find(vis) || null;
    } else if (kind === 'row') {
      el = Array.from(document.querySelectorAll('tbody tr')).filter(vis)
        .find((r) => norm(r.textContent).includes(t)) || null;
    } else if (kind === 'dl') {
      const dt = Array.from(document.querySelectorAll('dt')).filter(vis).find((d) => norm(d.textContent).startsWith(t));
      el = dt ? dt.parentElement : null;
    } else if (kind === 'btn') {
      el = Array.from(document.querySelectorAll('button, a, select, input'))
        .filter(vis).find((b) => norm(b.textContent).startsWith(t) || norm(b.value) === t || norm(b.getAttribute('aria-label')) === t);
    } else {
      const cands = Array.from(document.querySelectorAll('h1,h2,h3,h4,div,span,li,p,label,b,select'))
        .filter(vis).filter((n) => norm(n.textContent).startsWith(t));
      cands.sort((a, b) => (a.textContent || '').length - (b.textContent || '').length);
      el = cands[0] || null;
      if (el && kind === 'box') {
        let n = el;
        while (n && n !== document.body && !/\b(border|shadow-xl)\b/.test(n.className || '')) n = n.parentElement;
        if (n && n !== document.body) el = n;
      }
    }
    if (!el) return;
    const r = el.getBoundingClientRect();
    out[key] = [r.left / W, r.top / H, r.width / W, r.height / H].map((v) => Math.round(v * 10000) / 10000);
  });
  return out;
};

const click = (text) => async (page) => clickText(page, text);

/** Open the Review imports modal by clicking the BUTTON itself, and wait until the modal is there. */
const openReview = (label, title) => async (page) => {
  const ok = await page.evaluate((want) => {
    const btn = Array.from(document.querySelectorAll('button'))
      .find((b) => (b.textContent || '').trim().toLowerCase().startsWith(want.toLowerCase()));
    if (!btn) return false;
    btn.click();
    return true;
  }, label);
  if (!ok) throw new Error(`no button reading "${label}"`);
  await page.waitForFunction((t) => document.body.innerText.includes(t), { timeout: 10000 }, title);
  await sleep(800);
};

const selectTesla = async (page) => {
  const ok = await page.evaluate(() => {
    const sel = Array.from(document.querySelectorAll('select'))
      .find((s) => Array.from(s.options).some((o) => o.value === 'tesla'));
    if (!sel) return false;
    const setter = Object.getOwnPropertyDescriptor(HTMLSelectElement.prototype, 'value').set;
    setter.call(sel, 'tesla');
    sel.dispatchEvent(new Event('change', { bubbles: true }));
    return true;
  });
  if (!ok) throw new Error('no provider dropdown offering Tesla');
  await sleep(1200);
};

const typeBusinessCode = async (page) => {
  const input = await page.$('input[aria-label]:not([type=password])');
  const ok = await page.evaluate(() => {
    const el = Array.from(document.querySelectorAll('input')).find((i) => i.className.includes('font-mono'));
    if (!el) return false;
    el.scrollIntoView({ block: 'center' });
    el.focus();
    return true;
  });
  if (!ok || !input) throw new Error('no Tesla for Business code field (is this an admin session?)');
  await page.keyboard.type('TFB-7Q2K-93XD-DEMO', { delay: 20 });
  await sleep(600);
};

/** Click "Print QR sheet" with window.open caught, and photograph the sheet it would have printed. */
const captureSheet = async (page) => {
  await page.evaluate(() => {
    window.__sheetHtml = '';
    // One print = one document: keep the LAST one written, never a concatenation.
    window.open = () => ({ document: { open() {}, write(h) { window.__sheetHtml = h; }, close() {} } });
  });
  return async (L) => {
    await clickText(page, L('ownerGps.teslaPrintSheet', 'Print QR sheet'));
    const html = await page.evaluate(() => window.__sheetHtml);
    if (!html) throw new Error('the QR sheet was not produced');
    return html.replace(/<script>[\s\S]*?<\/script>/g, '');
  };
};

/** The Supercharger frames: the banner, the buttons, the table and one row per staged session. */
function scMeasures(L) {
  const P = (k, d) => L(`superchargerPage.${k}`, d);
  const page = [
    ['title', P('title', 'Supercharger'), 'el'],
    ['banner', P('rebillingOn', 'Supercharger sessions').slice(0, 20), 'el'],
    ['bannerOff', P('rebillingOff', 'Rebilling is off').slice(0, 16), 'el'],
    ['import', P('importNow', 'Import from Tesla'), 'btn'],
    ['excel', 'Excel', 'btn'],
    ['pdf', 'PDF', 'btn'],
    ['summary', P('summary', '{{count}}').split('{{')[0] || '6', 'el'],
    ['table', 'table', 'tag'],
    ['statusHead', P('chargeStatus', 'Renter charge'), 'el'],
    ['idleHead', P('idleFee', 'Idle fee'), 'el'],
    ...['Secaucus', 'Newark Airport', 'Edison', 'Paramus', 'Woodbridge', 'Clinton']
      .map((site, i) => [`row${i + 1}`, site, 'row']),
  ];
  return {
    'tes-10-sc-list': page,
    'tes-11-sc-off': page,
    'tes-12-sc-menu': [...page, ['menuInfo', P('info', 'Info'), 'btn'], ['menuBookings', P('bookings', 'Bookings'), 'btn'],
      ['menuInvoice', P('teslaInvoice', 'Tesla invoice (PDF)'), 'btn']],
    'tes-13-sc-info': [['modal', P('sessionInfo', 'Supercharger session'), 'box'],
      ['ourFee', P('ourFee', 'Our fee'), 'dl'], ['infoTotal', P('amount', 'Total'), 'dl'],
      ['infoStatus', P('chargeStatus', 'Renter charge'), 'dl'],
      ['infoInvoice', P('teslaInvoice', 'Tesla invoice (PDF)'), 'btn']],
  };
}

/** What to measure on each screen (see MEASURE_FN). */
function measures(L, name) {
  const common = [
    ['tab', 'GPS Systems', 'btn'],
    ['addProvider', L('ownerGps.addProvider', 'Add GPS provider'), 'btn'],
    ['teslaCard', 'tesla', 'box'],
    ['panel', L('ownerGps.teslaTitle', 'Tesla live tracking'), 'box'],
    ['addKey', L('ownerGps.teslaAddKey', 'Add key to car'), 'btn'],
    ['check', L('ownerGps.teslaCheck', 'Check cars'), 'btn'],
    ['print', L('ownerGps.teslaPrintSheet', 'Print QR sheet'), 'btn'],
    ['summary', L('ownerGps.teslaSummary', '{{paired}}').split('{{')[0] || 'x', 'el'],
    ['reconnect', L('ownerGps.reconnect', 'Reconnect'), 'btn'],
    ['review', L('ownerGps.reviewImports', 'Review imports'), 'btn'],
  ];
  const per = {
    'tes-01-gps-add': [['addBox', L('ownerGps.addTitle', 'Add GPS provider'), 'box'], ['select', 'tesla', 'el']],
    'tes-02-add-tesla': [['addBox', L('ownerGps.addTitle', 'Add GPS provider'), 'box'],
      ['connect', L('ownerGps.connect', 'Connect') + ' Tesla', 'btn'],
      ['help', L('ownerGps.oauthConnectHelp', 'You').slice(0, 12), 'el']],
    'tes-04-review': [['modalTitle', L('ownerGps.pendingTitle', 'Review GPS vehicles'), 'el'],
      ['row', 'Tesla Model 3 2022', 'box'], ['writeDb', L('ownerGps.writeToDb', 'Write to DB'), 'btn'],
      ['discard', L('ownerGps.discard', 'Discard'), 'btn']],
    ...scMeasures(L),
    'tes-08-business': [['biz', L('ownerGps.teslaBusinessTitle', 'Tesla for Business (admin)'), 'box'],
      ['bizConnect', L('ownerGps.teslaBusinessConnect', 'Connect fleet'), 'btn']],
  };
  const rows = ['7SAYGDEE0PA000101', '5YJ3E1EB8NF000102', '7SAYGDEE6RF000103', '5YJSA1E40LF000104']
    .map((v, i) => [`vin${i + 1}`, v, 'el']);
  return [...common, ...(per[name] || []), ...rows];
}

/** Open the row menu (the button at the start of the row) of the session at `site`, as the owner would. */
const openRowMenu = (site) => async (page) => {
  const ok = await page.evaluate((want) => {
    const tr = Array.from(document.querySelectorAll('tbody tr')).find((r) => (r.textContent || '').includes(want));
    const btn = tr && tr.querySelector('button');
    if (!btn) return false;
    btn.click();
    return true;
  }, site);
  if (!ok) throw new Error(`no row menu for "${site}"`);
  await sleep(700);
};

function screens(L) {
  const gpsTab = [click('GPS Systems')];
  const addOpen = [...gpsTab, click(L('ownerGps.addProvider', 'Add GPS provider'))];
  const check = click(L('ownerGps.teslaCheck', 'Check cars'));
  return [
    { name: 'tes-01-gps-add', accounts: [], steps: addOpen },
    { name: 'tes-02-add-tesla', accounts: [], steps: [...addOpen, selectTesla] },
    { name: 'tes-03-connected', accounts: [teslaAccount()], steps: gpsTab },
    { name: 'tes-04-review', accounts: [teslaAccount()], pending: PENDING,
      steps: [...gpsTab, openReview(L('ownerGps.reviewImports', 'Review imports'), L('ownerGps.pendingTitle', 'Review GPS vehicles'))] },
    { name: 'tes-05-check-mixed', accounts: [teslaAccount()], status: STATUS.mixed, steps: [...gpsTab, check] },
    { name: 'tes-06-check-all', accounts: [teslaAccount()], status: STATUS.all, steps: [...gpsTab, check] },
    { name: 'tes-07-qr-sheet', accounts: [teslaAccount()], status: STATUS.sheet, sheet: true, steps: [...gpsTab, check] },
    { name: 'tes-08-business', accounts: [], business: true, steps: [...gpsTab, typeBusinessCode] },
    { name: 'tes-10-sc-list', path: '/supercharger', sc: SC.on, steps: [] },
    { name: 'tes-11-sc-off', path: '/supercharger', sc: SC.off, steps: [] },
    { name: 'tes-12-sc-menu', path: '/supercharger', sc: SC.on, steps: [openRowMenu('Newark Airport')] },
    { name: 'tes-13-sc-info', path: '/supercharger', sc: SC.on,
      steps: [openRowMenu('Newark Airport'), click(L('superchargerPage.info', 'Info'))] },
    { name: 'tes-09-business-fleet', accounts: [teslaAccount('Tesla for Business')], status: STATUS.all,
      steps: [...gpsTab, check] },
  ];
}

// ------------------------------------------------------------------ run

(async () => {
  const browser = await puppeteer.connect({ browserURL: `http://127.0.0.1:${CDP_PORT}`, defaultViewport: VIEWPORT, protocolTimeout: 600000 });
  const page = await browser.newPage();
  await page.setViewport(VIEWPORT);
  page.setDefaultNavigationTimeout(60000);
  page.on('dialog', (d) => d.dismiss().catch(() => {}));

  let current = null;   // the screen being captured: what the staged API answers
  const blocked = [];
  await page.setRequestInterception(true);
  page.on('request', (req) => {
    const url = req.url();
    const m = req.method();
    const json = (body) => req.respond({ status: 200, contentType: 'application/json', body: JSON.stringify(body) }).catch(() => {});
    if (current && m === 'GET' && /\/api\/owners\/[^/]+\/gps-plugins\/pending-imports(\?|$)/.test(url)) {
      return json(current.pending || { pending: [], linkableCars: [] });
    }
    if (current && m === 'GET' && /\/api\/owners\/[^/]+\/gps-plugins(\?|$)/.test(url)) {
      return json({ providers: PROVIDERS, accounts: current.accounts || [] });
    }
    if (current && m === 'GET' && /\/api\/supercharger-sessions(\?|$)/.test(url)) {
      return json(current.sc || SC.on);
    }
    if (current && m === 'POST' && /\/api\/supercharger-sessions\/import(\?|$)/.test(url)) {
      return json(SC_IMPORT);
    }
    if (current && m === 'POST' && /\/api\/gps\/tesla\/telemetry\/refresh/.test(url)) {
      return json(current.status || STATUS.all);
    }
    if (m !== 'GET' && m !== 'HEAD' && m !== 'OPTIONS' && /\/api\//i.test(url)) {
      blocked.push(`${m} ${url}`);
      return req.abort('blockedbyclient').catch(() => {});
    }
    return req.continue().catch(() => {});
  });

  const blurArgs = [REDACTION.markerSource(), REDACTION.PII_CLASS, RENAME];
  const failures = [];
  const boxesFile = path.join(SHOTS, '_tesla_boxes.json');
  const boxes = fs.existsSync(boxesFile) ? JSON.parse(fs.readFileSync(boxesFile, 'utf8')) : {};

  for (const lang of LANGS) {
    fs.mkdirSync(path.join(SHOTS, lang), { recursive: true });
    const L = labeller(lang);
    const list = screens(L).filter((s) => !ONLY.length || ONLY.some((o) => s.name.includes(o)));
    for (const s of list) {
      process.stdout.write(`[${lang}] ${s.name}\n`);
      current = s;
      try {
        await page.goto(`${BASE}${s.path || '/settings'}`, { waitUntil: 'domcontentloaded' });
        for (let i = 0; i < 2; i += 1) {
          await setLanguage(page, lang);
          await page.reload({ waitUntil: 'domcontentloaded' });
          await sleep(1500);
        }
        await waitForApp(page);
        await sleep(SETTLE_MS);
        await page.evaluate(BLUR_FN, ...blurArgs);
        await page.evaluate(RESTORE_CHROME_FN);
        const sheet = s.sheet ? await captureSheet(page) : null;
        for (const step of s.steps) await step(page);
        await sleep(1200);
        await page.evaluate(BLUR_FN, ...blurArgs);
        await page.evaluate(RESTORE_CHROME_FN);
        await page.evaluate(TIDY_FN, !!s.business);
        await page.evaluate(() => window.scrollTo(0, 0));
        await sleep(800);
        const out = path.join(SHOTS, lang, `${s.name}.png`);
        if (!s.sheet) boxes[`${lang}/${s.name}`] = await page.evaluate(MEASURE_FN, measures(L, s.name));
        if (sheet) {
          // In THIS tab: a second tab is a background tab, and Chrome painted it as a tiled mess.
          // The next screen navigates back to the portal anyway.
          const html = await sheet(L);
          await page.setContent(html, { waitUntil: 'load' });
          await sleep(800);
          boxes[`${lang}/${s.name}`] = await page.evaluate(() => {
            const W = window.innerWidth; const H = window.innerHeight;
            const f = (el) => { const r = el.getBoundingClientRect(); return [r.left / W, r.top / H, r.width / W, r.height / H].map((v) => Math.round(v * 10000) / 10000); };
            const card = document.querySelector('.card');
            return card ? { card: f(card), qr: f(card.querySelector('.qr')), tail: f(card.querySelector('.tail')),
              done: f(card.querySelector('.done')), title: f(document.querySelector('h1')) } : {};
          });
          fs.writeFileSync(out, await page.screenshot());
        } else {
          fs.writeFileSync(out, await page.screenshot());
        }
      } catch (err) {
        console.log(`  FAILED: ${err.message}`);
        failures.push({ lang, name: s.name, error: err.message });
      }
    }
  }

  current = null;
  fs.writeFileSync(boxesFile, JSON.stringify(boxes, null, 2));
  if (blocked.length) console.log(`\nWrites blocked (nothing saved):\n  ${blocked.join('\n  ')}`);
  console.log(`\nDone. ${failures.length ? 'Failures: ' + JSON.stringify(failures) : 'all captured'}`);
  await page.close().catch(() => {});
  await browser.disconnect();
})().catch((e) => { console.error('FATAL', e); process.exit(1); });
