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
 * Screenshots for episode 58 (Transfer to renter), from the DEV portal, with DEMO DATA.
 *
 * The session is shown as an OWNER's (admin flags switched off in the browser). Everything listed is staged:
 * the violations, the cars, the renter, what the liability-transfer API answers (the issuer rule is the real
 * pa-turnpike-tbp plugin's text, copied from aegis-ao-liability), and the letter (`lt-06-letter`, drawn here
 * after the plugin's BuildLetter, with a made-up company, renter and plate). The page itself is the real
 * deployed portal.
 *
 * READ-ONLY BY CONSTRUCTION. The writes the episode shows (download package, mark as sent, issuer refused,
 * save a mailed ticket) are answered here; every other API request that is not a GET is aborted before it
 * leaves the browser. Downloads are denied, so the staged "PDF" never lands on disk.
 *
 * Usage:
 *   node capture-liability.js --cdp=9223
 *   node capture-liability.js --cdp=9223 --only=lt-03 --lang=es
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
const p2 = (v) => String(v).padStart(2, '0');
const usDate = (iso) => { const t = new Date(iso); return `${p2(t.getUTCMonth() + 1)}/${p2(t.getUTCDate())}/${t.getUTCFullYear()}`; };

// ------------------------------------------------------------------ staged data

const car = (n, brand, model, year, plate) => ({
  id: `demo-car-${n}`, ownerId: 'self', title: `${brand} ${model}`, carBrand: brand, carModel: model, year,
  carPlateNumber: plate, plateNumber: plate, carPlateNumberState: 'NJ', published: false,
});
const CARS = [car(1, 'Toyota', 'Camry', 2025, 'NJT4102'), car(2, 'Honda', 'Accord', 2024, 'NJL8830'),
  car(3, 'Hyundai', 'Sonata', 2026, 'NJP5521')];

const vio = (n, d, carN, citation, amount, agency, address, extra = {}) => ({
  id: `V-58${n}17`, carId: `demo-car-${carN}`, carTitle: CARS[carN - 1].title, bookingId: `BK-58${n}17`,
  licensePlate: CARS[carN - 1].carPlateNumber, state: 'NJ', citationNumber: citation, amount, issueDateUtc: d,
  address, agency, status: 'Open', chargeStatus: 'NotCharged', isPaid: false, payUrl: 'https://pay.example.org/ticket',
  pluginKey: 'demo-agency', endpointDisplayName: agency, firstSeenAt: day(-2), lastSeenAt: day(0), ...extra,
});
// The PA Turnpike toll-by-plate invoice the episode transfers: on Riley Morgan's rental of the Camry.
const PA_ISSUED = day(-6, 14, 20);
const PA = vio(1, PA_ISSUED, 1, 'TBP0041772219', 14.85, 'Pennsylvania Turnpike', 'I-76 Valley Forge');
const OTHERS = [
  vio(2, day(-12, 18, 42), 2, 'SC48810', 50, 'City Traffic Camera Program', 'Broad St & Market St'),
  vio(3, day(-15, 13, 7), 3, 'PX902216', 65, 'Downtown Parking Office', '5th Ave & 22nd St', { isPaid: true, status: 'Paid', chargeStatus: 'Charged' }),
  vio(4, day(-21, 21, 15), 2, 'RL7730214', 100, 'City Parking Authority', 'Main St & 1st Ave'),
];
const listOf = (rows) => ({ items: rows, totalCount: rows.length, page: 1, pageSize: 25, lastScanAt: day(0, 6), lastScanStatus: 'completed' });

// The real pa-turnpike-tbp plugin's rules (aegis-ao-liability, PaTurnpikeLiabilityProvider.cs).
const PA_RULES = {
  legalBasis: '74 Pa.C.S. § 8117(b)(3)',
  noticeStage: 'Toll By Plate invoice (the first, original invoice)',
  appliesTo: 'Toll', deadlineDays: 30, requiresOwnerSignature: true, requiresNotarization: false,
  channels: [
    { kind: 'Mail', label: 'Toll By Plate Appeal (mail)', value: 'PA Turnpike Toll By Plate Appeal\n300 East Park Drive\nHarrisburg, PA 17111-2729', acceptsDocuments: true, note: 'Not the payment box in Pittsburgh — appeals go to Harrisburg.' },
    { kind: 'Fax', label: 'Toll By Plate Appeal (fax)', value: '717-565-4312', acceptsDocuments: true, note: null },
    { kind: 'Phone', label: 'Toll By Plate customer service', value: '877-736-6727', acceptsDocuments: false, note: null },
  ],
  instructions: [
    'On page 3 of the invoice (TOLL BY PLATE APPEAL FORM), Section B "Certification of Non-Liability", tick "Leased or Rented".',
    "Fill in the lessee's name, address and the date the lease was executed — they are printed in this letter.",
    'Sign the certification. Unsigned appeals are not processed.',
    'Send the appeal form, this letter and the rental agreement copy together, by mail or fax.',
    'Do it on the FIRST invoice: the Turnpike may not process appeals on past-due tolls.',
  ],
  outcome: 'The Commission treats the lessee as the owner and invoices the lessee for the tolls and fees. '
    + 'Unpaid invoices get a late fee of $5 or 1.5% and go to collections after 60 days.',
  sourceUrls: ['https://www.paturnpike.com/toll-by-plate'],
};
const NJ_RULES = {
  legalBasis: 'N.J.S.A. 27:23-34.3(b), 27:25A-21.3(b); N.J.A.C. 19:9-9.2(f)', noticeStage: 'Violation notice',
  appliesTo: 'Toll', deadlineDays: 60, requiresOwnerSignature: true, requiresNotarization: false,
  channels: [], instructions: [], outcome: null, sourceUrls: [],
};
const DEADLINE = day(24, 4, 0);
const PA_CAND = (missing = []) => ({ providerKey: 'pa-turnpike-tbp', providerName: 'Pennsylvania Turnpike — Toll By Plate',
  matchScore: 100, rules: PA_RULES, deadlineUtc: DEADLINE, missingFields: missing, problem: null });
const NJ_CAND = { providerKey: 'nj-ezpass-violations', providerName: 'New Jersey E-ZPass violations (NJ Turnpike, Garden State Parkway, Atlantic City Expressway)',
  matchScore: 20, rules: NJ_RULES, deadlineUtc: day(54, 4, 0), missingFields: [], problem: null };

const record = (status) => ({
  id: 'demo-lt-1', violationId: PA.id, providerKey: 'pa-turnpike-tbp', status, noticeKind: 'Toll', deadlineUtc: DEADLINE,
  preparedAtUtc: day(0, 13), sentAtUtc: status === 'Sent' || status === 'Rejected' || status === 'Accepted' ? day(0, 14) : null,
  sentChannel: status === 'Sent' || status === 'Rejected' || status === 'Accepted' ? 'Mail' : null,
  sentReference: status === 'Sent' ? '9400 1000 0000 5812 3456 78' : null, outcomeAtUtc: null, note: null,
});
const options = (state, variant) => ({
  violationId: PA.id, noticeKind: 'Toll', bookingId: PA.bookingId, renterName: 'Riley Morgan',
  agreementOnFile: variant !== 'missing', vehicleIsTrailer: false, blocker: null,
  candidates: [PA_CAND(variant === 'missing' ? ['LesseeAddress', 'AgreementCopy'] : []), NJ_CAND],
  current: state ? record(state) : null,
});
const PACKAGE = { transferId: 'demo-lt-1', deadlineUtc: DEADLINE, fileName: 'transfer-TBP0041772219.pdf',
  pdfBase64: 'JVBERi0xLjQKJSVFT0YK', notes: [] };

// The mailed ticket of episode 57, saved onto Taylor Quinn's rental — the single-ticket entry point.
const ISSUED = new Date(Date.now() - 7 * 86400000);
const ISSUED_LOCAL = `${ISSUED.getUTCFullYear()}-${p2(ISSUED.getUTCMonth() + 1)}-${p2(ISSUED.getUTCDate())}T14:05`;
const READ = {
  success: true,
  data: {
    citationNumber: 'RL1234567', pin: '5821', issuedLocal: ISSUED_LOCAL, amount: 100, dueDate: null,
    licensePlate: 'NJT 4102', plateState: 'NJ', agency: 'City Parking Authority', issuingState: 'PA',
    paymentUrl: 'https://pay.example.org/ticket', violationType: 'red_light', location: 'Main St & 1st Ave',
  },
};
const SAVED = { success: true, violationId: 'V-58917', bookingId: 'BK-58917', issueDateUtc: day(-7, 19, 5),
  lookup: { outcome: 'not_found', pluginKey: null, amount: null, isPaid: false } };

// ------------------------------------------------------------------ the letter (after BuildLetter)

const LETTER_HTML = (today, travel) => `<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1600px;height:1000px;background:radial-gradient(circle at 30% 20%,#6f7f8f,#36414c);display:flex;align-items:center;justify-content:center;font-family:Georgia,'Times New Roman',serif}
.p{width:760px;height:930px;overflow:hidden;background:#fdfdfb;transform:rotate(-1.4deg);box-shadow:0 30px 60px rgba(0,0,0,.45);padding:38px 56px;color:#1d1d1d;font-size:14.5px;line-height:1.42;box-sizing:border-box}
.from{font-size:14px}.b{font-weight:700}.sp{height:12px}.h{font-weight:700;font-size:16px;margin:4px 0 6px}
.f{display:flex;gap:10px}.f .l{width:200px;color:#555}.sig{margin-top:22px;border-top:1px solid #1d1d1d;width:300px;padding-top:3px;font-size:12px;color:#555}
.enc{margin-top:12px;font-style:italic}
</style></head><body><div class="p">
<div class="from"><div class="b">Your Company</div><div>100 Example Avenue</div><div>Newark, NJ 07102</div><div>yourcompany@mail.myeztoll.com</div></div>
<div class="sp"></div><div>${today}</div><div class="sp"></div>
<div>Pennsylvania Turnpike Commission<br>Toll By Plate Appeal<br>300 East Park Drive<br>Harrisburg, PA 17111-2729</div>
<div class="sp"></div>
<div class="h">Toll By Plate appeal — leased / rented vehicle (74 Pa.C.S. § 8117(b)(3))</div>
<div class="f"><div class="l">Notice / invoice number</div><div>TBP0041772219</div></div>
<div class="f"><div class="l">License plate</div><div>NJT4102 NJ</div></div>
<div class="f"><div class="l">Date of travel</div><div>${travel}</div></div>
<div class="f"><div class="l">Amount</div><div>$14.85</div></div>
<div class="f"><div class="l">Vehicle</div><div>2025 Toyota Camry</div></div>
<div class="sp"></div>
<div>Your Company is the registered owner of the vehicle bearing plate NJT4102 NJ. On the date of this toll notice the vehicle was rented to the lessee named below under a written rental agreement and was in the lessee's possession and control, not ours.</div>
<div class="sp"></div>
<div>Under 74 Pa.C.S. § 8117(b)(3) we enclose a copy of the rental agreement covering the vehicle on the date of travel, with the lessee's name and address. The lessee is therefore deemed the owner for this invoice and is liable for its tolls and fees. Please reissue the invoice to the lessee.</div>
<div class="sp"></div>
<div class="h">Lessee (renter)</div>
<div class="f"><div class="l">Name</div><div>Riley Morgan</div></div>
<div class="f"><div class="l">Address</div><div>25 Sample Road, Trenton, NJ 08608</div></div>
<div class="f"><div class="l">Rental agreement / reference</div><div>BK-58117</div></div>
<div class="enc">Enclosed: a copy of the signed rental agreement covering the vehicle on the date of the notice.</div>
<div class="sig">Signature</div>
<div class="f"><div class="l">Name</div><div>Sam Rivera, Manager</div></div>
<div class="f"><div class="l">Date</div><div>${today}</div></div>
</div></body></html>`;

function labeller(lang) {
  let bundle = {};
  // The deployed labels: origin/main, not the working copy (which may be on an older branch).
  try {
    const raw = require('child_process').execFileSync('git', ['-C', LOCALES.replace(/\/src\/locales$/, ''), 'show', `origin/main:src/locales/${lang}/common.json`], { encoding: 'utf8', maxBuffer: 64 << 20 });
    bundle = JSON.parse(raw);
  } catch (e) {
    try { bundle = JSON.parse(fs.readFileSync(`${LOCALES}/${lang}/common.json`, 'utf8')); } catch (e2) { /* */ }
  }
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
  const staged = /Riley|Morgan|Taylor|Quinn|Sam Rivera|NJT4102|NJL8830|NJP5521|TBP0041772219|RL1234567|RL7730214|SC48810|PX902216|5821|BK-|9400 1000|Pennsylvania Turnpike|City Parking|Main St|I-76|Toll By Plate|Harrisburg|300 East Park|717-565|877-736|appeals go|example\.org|yourcompany@|Your Company/;
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
      while (el && el !== document.body && !/shadow/.test(el.className || '')) el = el.parentElement;
      if (el === document.body) el = null;
    }
    else if (kind === 'label') {
      // The <label> whose caption starts with the text: the caption and its field together.
      el = Array.from(document.querySelectorAll('label')).filter(vis).find((n) => norm(n.textContent).startsWith(t)) || null;
    }
    else if (kind === 'row') el = Array.from(document.querySelectorAll('tbody tr')).filter(vis).find((r) => norm(r.textContent).includes(t)) || null;
    else {
      const c = Array.from(document.querySelectorAll('h1,h2,h3,div,span,p,label,li,ol,ul')).filter(vis).filter((n) => norm(n.textContent).startsWith(t));
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
    const b = Array.from(document.querySelectorAll('button, a')).filter((x) => x.getClientRects().length)
      .find((x) => rx.test((x.textContent || '').trim()));
    if (b) b.click();
    return !!b;
  }, re);
  if (!ok) throw new Error(`no button /${re}/`);
  await sleep(1500);
};
const rowMenu = (text) => async (page) => {
  // Right to left, the ⋮ menu opens under the sidebar (a portal bug, seen 19.11): there the row is
  // right-clicked in its middle instead, which opens the same menu where the pointer is.
  const rtl = await page.evaluate(() => getComputedStyle(document.documentElement).direction === 'rtl' || document.dir === 'rtl');
  if (rtl) {
    const box = await page.evaluate((t) => {
      const r = Array.from(document.querySelectorAll('tbody tr')).find((x) => (x.textContent || '').includes(t));
      if (!r) return null;
      r.scrollIntoView({ block: 'center' });
      const b = r.getBoundingClientRect();
      return { x: b.left + b.width * 0.45, y: b.top + b.height / 2 };
    }, text);
    if (!box) throw new Error(`no row ${text}`);
    await page.mouse.click(box.x, box.y, { button: 'right' });
    await sleep(1000);
    return;
  }
  const ok = await page.evaluate((t) => {
    const r = Array.from(document.querySelectorAll('tbody tr')).find((x) => (x.textContent || '').includes(t));
    const b = r && r.querySelector('button');
    if (b) b.click();
    return !!b;
  }, text);
  if (!ok) throw new Error(`no row ${text}`);
  await sleep(1000);
};
// Types into the <input> of the <label> whose caption starts with `caption`.
const typeInto = (caption, value) => async (page) => {
  const handle = await page.evaluateHandle((c) => {
    const norm = (t) => (t || '').replace(/\s+/g, ' ').trim().toLowerCase();
    const l = Array.from(document.querySelectorAll('label')).find((n) => norm(n.textContent).startsWith(norm(c)));
    return l ? l.querySelector('input') : null;
  }, caption);
  const el = handle.asElement();
  if (!el) throw new Error(`no field "${caption}"`);
  await el.click({ clickCount: 3 });
  await el.type(value, { delay: 10 });
  await sleep(300);
};
// Scrolls the open dialog: 'top', 'bottom', or the element whose text starts with the given string, centred.
const scrollModal = (where) => async (page) => {
  await page.evaluate((w) => {
    const boxes = Array.from(document.querySelectorAll('div')).filter((d) => /overflow-y-auto/.test(d.className || '') && /max-h/.test(d.className || '') && d.getClientRects().length);
    const box = boxes[boxes.length - 1];
    if (!box) return;
    if (w === 'top') box.scrollTop = 0;
    else if (w === 'bottom') box.scrollTop = box.scrollHeight;
    else {
      const norm = (t) => (t || '').replace(/\s+/g, ' ').trim().toLowerCase();
      const hit = Array.from(box.querySelectorAll('div, p, label')).find((n) => norm(n.textContent).startsWith(norm(w)));
      if (hit) hit.scrollIntoView({ block: 'center' });
    }
  }, where);
  await sleep(600);
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
// Scrolls the list sideways to its last columns, where Paid and its "Transferred to renter" badge are.
const scrollTableRight = async (page) => {
  await page.evaluate(() => {
    const t = document.querySelector('table');
    for (let n = t && t.parentElement; n && n !== document.body; n = n.parentElement) {
      // In a right-to-left page the far end of the row is a negative scrollLeft.
      if (n.scrollWidth > n.clientWidth + 4) { n.scrollLeft = getComputedStyle(n).direction === 'rtl' ? -n.scrollWidth : n.scrollWidth; break; }
    }
  });
  await sleep(500);
};
const settle = (ms) => async () => { await sleep(ms); };
// A success toast lasts two seconds, less than the redaction pass takes: copy it into a fixed, still box.
const freezeToast = async (page) => {
  await sleep(450);
  const n = await page.evaluate(() => {
    const live = Array.from(document.querySelectorAll('[role="status"]')).filter((el) => el.getClientRects().length);
    live.forEach((el) => {
      const box = el.closest('div[style]') || el;
      const r = box.getBoundingClientRect();
      const c = box.cloneNode(true);
      c.setAttribute('data-frozen-toast', '1');
      Object.assign(c.style, { position: 'fixed', left: `${r.left}px`, top: `${r.top}px`, width: `${r.width}px`,
        zIndex: '99999', transform: 'none', animation: 'none', opacity: '1' });
      c.querySelectorAll('*').forEach((x) => { x.style.animation = 'none'; x.style.opacity = '1'; x.style.transform = 'none'; });
      box.style.visibility = 'hidden';
      document.body.appendChild(c);
    });
    return live.length;
  });
  if (!n) throw new Error('no toast to freeze');
};

// ------------------------------------------------------------------ screens

function screens(L) {
  const transfer = L('ownerViolations.transferToRenter', 'Transfer to renter');
  const title = L('liabilityTransfer.title', 'Transfer to renter');
  const add = L('violationNotice.addButton', 'Add mailed ticket');
  const save = L('violationNotice.save', 'Save ticket');
  const download = L('liabilityTransfer.download', 'Download package');
  const markSent = L('liabilityTransfer.markSent', 'Mark as sent');
  const refused = L('liabilityTransfer.rejected', 'Issuer refused');
  const signer = L('liabilityTransfer.signerName', 'Signed by (name)');
  const signerTitle = L('liabilityTransfer.signerTitle', 'Title');
  const reference = L('liabilityTransfer.reference', 'Tracking / confirmation no.');
  const open = [rowMenu('TBP0041772219'), clickButton(`^${transfer}$`), settle(800)];
  const modalTop = [
    ['modal', title, 'panel'], ['renter', L('liabilityTransfer.renter', 'Renter'), 'text'],
    ['agreement', L('liabilityTransfer.agreement', 'Signed agreement'), 'text'],
    ['issuer', L('liabilityTransfer.issuer', 'Issuer rule'), 'label'],
    ['legal', L('liabilityTransfer.legalBasis', 'Legal basis'), 'text'],
    ['deadline', L('liabilityTransfer.deadline', 'Send by'), 'text'],
    ['sign', L('liabilityTransfer.sign', 'Sign the letter before sending it.'), 'text'],
    ['steps', 'On page 3', 'text'], ['where', L('liabilityTransfer.whereToSend', 'Where to send it'), 'text'],
    ['mail', 'Toll By Plate Appeal (mail)', 'text'],
  ];
  const modalBottom = [
    ['modal', title, 'panel'], ['where', L('liabilityTransfer.whereToSend', 'Where to send it'), 'text'],
    ['mail', 'Toll By Plate Appeal (mail)', 'text'], ['outcome', 'The Commission treats', 'text'],
    ['signer', signer, 'label'], ['signerTitle', signerTitle, 'label'],
    ['download', download, 'btn'], ['downloadAgain', L('liabilityTransfer.downloadAgain', 'Download again'), 'btn'],
    ['status', L('liabilityTransfer.status.Prepared', 'Prepared, not sent yet'), 'text'],
    ['sentBy', L('liabilityTransfer.sentBy', 'Sent by'), 'label'], ['reference', reference, 'label'],
    ['markSent', markSent, 'btn'], ['cancel', L('liabilityTransfer.cancel', 'Cancel transfer'), 'btn'],
    ['refused', refused, 'btn'], ['accepted', L('liabilityTransfer.accepted', 'Issuer accepted'), 'btn'],
    ['toasts', '[role="status"]', 'tag'], ['toastbox', '[data-frozen-toast]', 'tag'], ['missing', L('liabilityTransfer.missing', 'Missing before'), 'text'],
  ];
  return [
    { name: 'lt-01-violations', path: '/violations', list: [PA, ...OTHERS],
      measure: [['row1', 'TBP0041772219', 'row'], ['thead', 'thead', 'tag'], ['add', add, 'btn']] },
    { name: 'lt-02-row-menu', path: '/violations', list: [PA, ...OTHERS], steps: [rowMenu('TBP0041772219')],
      measure: [['row1', 'TBP0041772219', 'row'], ['transfer', transfer, 'btn'], ['info', L('ownerViolations.info', 'Info'), 'btn']] },
    { name: 'lt-03-transfer', path: '/violations', list: [PA, ...OTHERS], steps: [...open, scrollModal('top')], measure: modalTop },
    { name: 'lt-04-transfer-bottom', path: '/violations', list: [PA, ...OTHERS],
      steps: [...open, typeInto(signer, 'Sam Rivera'), typeInto(signerTitle, 'Manager'), scrollModal('bottom')], measure: modalBottom },
    { name: 'lt-05-missing', path: '/violations', list: [PA, ...OTHERS], variant: 'missing',
      steps: [...open, scrollModal(L('liabilityTransfer.missing', 'Missing before'))], measure: [...modalTop, ...modalBottom] },
    { name: 'lt-07-prepared', path: '/violations', list: [PA, ...OTHERS],
      steps: [...open, typeInto(signer, 'Sam Rivera'), typeInto(signerTitle, 'Manager'), scrollModal('bottom'), clickButton(`${download}$`), freezeToast, scrollModal('bottom')],
      measure: modalBottom },
    { name: 'lt-08-sent', path: '/violations', list: [PA, ...OTHERS], initial: 'Prepared',
      steps: [...open, scrollModal('bottom'), typeInto(reference, '9400 1000 0000 5812 3456 78'), scrollModal('top'), clickButton(`${markSent}$`), freezeToast, scrollModal('top')],
      measure: [...modalTop, ...modalBottom] },
    { name: 'lt-08b-sent-bottom', path: '/violations', list: [PA, ...OTHERS], initial: 'Sent',
      steps: [...open, scrollModal('bottom')], measure: modalBottom },
    { name: 'lt-09-row-transferred', path: '/violations', list: [PA, ...OTHERS], initial: 'Sent', steps: [scrollTableRight],
      measure: [['row1', 'TBP0041772219', 'row'], ['badge', L('ownerViolations.transferredToRenter', 'Transferred to renter'), 'text'], ['thead', 'thead', 'tag']] },
    { name: 'lt-10-refused', path: '/violations', list: [PA, ...OTHERS], initial: 'Sent',
      steps: [...open, scrollModal('top'), clickButton(`${refused}$`), freezeToast, scrollModal('top')],
      measure: [...modalTop, ['toasts', '[role="status"]', 'tag'], ['toastbox', '[data-frozen-toast]', 'tag'], ['status', L('liabilityTransfer.status.Rejected', 'Refused by the issuer'), 'text']] },
    { name: 'lt-11-notice-saved', path: '/violations', list: [PA, ...OTHERS], ticket: true,
      steps: [clickButton(`^${add}$`), 'UPLOAD', hideToasts, clickButton(`^${save}$`), settle(800)],
      measure: [['modal', L('violationNotice.title', 'Add mailed ticket'), 'panel'],
        ['saved', L('violationNotice.savedOnBooking', 'Ticket saved and attached to the rental'), 'text'],
        ['hint', L('violationNotice.transferHint', 'You can transfer this ticket to the renter now.'), 'text'],
        ['transfer', transfer, 'btnlast'], ['toasts', '[role="status"]', 'tag'],
        ['addMany', L('violationNotice.batch.addButton', 'Add many tickets'), 'btn']] },
  ];
}

// ------------------------------------------------------------------ run

(async () => {
  const browser = await puppeteer.connect({ browserURL: `http://127.0.0.1:${CDP_PORT}`, defaultViewport: VIEWPORT, protocolTimeout: 600000 });
  const page = await browser.newPage();
  await page.setViewport(VIEWPORT);
  page.setDefaultNavigationTimeout(60000);
  page.on('dialog', (d) => d.dismiss().catch(() => {}));
  const cdp = await page.target().createCDPSession();
  await cdp.send('Browser.setDownloadBehavior', { behavior: 'deny' }).catch(() =>
    cdp.send('Page.setDownloadBehavior', { behavior: 'deny' }));

  // The letter: one picture for both languages (it goes to a US issuer, in English).
  if (!ONLY.length || ONLY.some((o) => 'lt-06-letter'.includes(o))) {
    await page.setContent(LETTER_HTML(usDate(day(0)), usDate(day(-9, 16))), { waitUntil: 'load' });
    const png = await page.screenshot();
    for (const lang of LANGS) { fs.mkdirSync(path.join(SHOTS, lang), { recursive: true }); fs.writeFileSync(path.join(SHOTS, lang, 'lt-06-letter.png'), png); }
    console.log('lt-06-letter');
  }

  const ticketFile = path.join(SHOTS, '_nov', 'ticket.jpg');
  if (!fs.existsSync(ticketFile)) throw new Error(`no ticket picture ${ticketFile} (run capture-nov-features.js --only=nov-00 first)`);

  await page.goto(`${BASE}/dashboard`, { waitUntil: 'domcontentloaded' });
  await sleep(1500);
  const saved = await page.evaluate(() => ({ auth: localStorage.getItem('aegis-auth-storage'), app: localStorage.getItem('aegis-app-storage') }));
  if (!saved.auth || !JSON.parse(saved.auth).state?.token) throw new Error('nobody is signed in on dev-owner in this Chrome');

  let current = null;
  let tstate = null;
  let ticketSaved = false;
  const blocked = [];
  await page.setRequestInterception(true);
  page.on('request', (req) => {
    const url = req.url(); const m = req.method();
    const json = (body, status = 200) => req.respond({ status, contentType: 'application/json', body: JSON.stringify(body) }).catch(() => {});
    if (current) {
      if (m === 'GET' && /\/api\/owner-violations\/plugins/i.test(url)) return json([{ key: 'demo-agency', canSearchByPlate: true, endpointCount: 3 }]);
      if (m === 'GET' && /\/api\/owner-violations\/progress\//i.test(url)) return json({ ownerId: 'self', status: 'not_found', progress: 0 });
      if (m === 'GET' && /\/api\/owner-violations(\?|$)/i.test(url)) {
        const rows = (current.list || []).map((v) => (v.id === PA.id && tstate === 'Sent' ? { ...v, chargeStatus: 'TransferredToRenter' } : v));
        return json(listOf(rows));
      }
      if (m === 'GET' && /\/api\/liability-transfer\/violations\/[^/]+\/options/i.test(url)) return json(options(tstate, current.variant));
      if (m === 'POST' && /\/api\/liability-transfer\/violations\/[^/]+\/package/i.test(url)) { tstate = 'Prepared'; return json(PACKAGE); }
      if (m === 'POST' && /\/api\/liability-transfer\/[^/]+\/sent/i.test(url)) { tstate = 'Sent'; return json({ record: record('Sent') }); }
      if (m === 'POST' && /\/api\/liability-transfer\/[^/]+\/outcome/i.test(url)) {
        let accepted = false; try { accepted = !!JSON.parse(req.postData() || '{}').accepted; } catch (e) { /* */ }
        tstate = accepted ? 'Accepted' : 'Rejected'; return json({ record: record(tstate) });
      }
      if (m === 'POST' && /\/api\/liability-transfer\/[^/]+\/cancel/i.test(url)) { tstate = 'Cancelled'; return json({ record: record('Cancelled') }); }
      if (m === 'POST' && /\/api\/owner-violations\/notice\/read/i.test(url)) return json(READ);
      if (m === 'POST' && /\/api\/owner-violations\/notice(\?|$)/i.test(url)) { ticketSaved = true; return json(SAVED); }
      if (m === 'GET' && /\/api\/Cars\/AllCarList\/[^/?]+/i.test(url)) return json({ result: CARS, reason: 0 });
      if (m === 'POST' && /\/api\/Cars\/AllCarList(\?|$)/i.test(url)) return json({ result: CARS, reason: 0 });
    }
    if (m !== 'GET' && m !== 'HEAD' && m !== 'OPTIONS' && /\/api\//i.test(url)) {
      blocked.push(`${m} ${url}`);
      return req.abort('blockedbyclient').catch(() => {});
    }
    return req.continue().catch(() => {});
  });

  const blurArgs = [REDACTION.markerSource(), REDACTION.PII_CLASS, RENAME];
  const failures = [];
  const boxesFile = path.join(SHOTS, '_lt_boxes.json');
  const boxes = fs.existsSync(boxesFile) ? JSON.parse(fs.readFileSync(boxesFile, 'utf8')) : {};

  for (const lang of LANGS) {
    fs.mkdirSync(path.join(SHOTS, lang), { recursive: true });
    const L = labeller(lang);
    for (const s of screens(L).filter((x) => !ONLY.length || ONLY.some((o) => x.name.includes(o)))) {
      process.stdout.write(`[${lang}] ${s.name}\n`);
      current = s; tstate = s.initial || null; ticketSaved = false;
      try {
        await page.goto(`${BASE}/dashboard`, { waitUntil: 'domcontentloaded' });
        await page.evaluate(STAGE_OWNER_FN, OWNER);
        await page.goto(`${BASE}${s.path}`, { waitUntil: 'domcontentloaded' });
        for (let i = 0; i < 2; i += 1) { await setLanguage(page, lang); await page.reload({ waitUntil: 'domcontentloaded' }); await sleep(1500); }
        await waitForApp(page);
        await sleep(SETTLE_MS);
        for (const step of s.steps || []) {
          if (step === 'UPLOAD') await upload(ticketFile)(page); else await step(page);
        }
        await sleep(1000);
        await page.evaluate(BLUR_FN, ...blurArgs);
        await page.evaluate(TIDY_FN);
        // The dialog holds only staged data: its fields must read.
        await page.evaluate(() => document.querySelectorAll('.fixed input, .fixed select, [role="dialog"] input, [role="dialog"] select').forEach((el) => {
          for (let n = el; n && n !== document.body; n = n.parentElement) {
            n.classList.forEach((c) => { if (/pii|blur/i.test(c)) n.classList.remove(c); });
            if (n.style && n.style.filter) n.style.filter = '';
          }
        }));
        await page.evaluate(() => { if (document.activeElement && document.activeElement.blur) document.activeElement.blur(); });
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
