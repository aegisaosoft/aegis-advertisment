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
 * Screenshots for episode 51 (a partner turns on a booking plugin for an owner they brought) and episode 54
 * (the Partners page: the row menu and the owner's Owner Settings / Booking Plugins / Page Visibility pages),
 * from the DEV portal, with DEMO DATA.
 *
 * The frames show the portal as a PARTNER sees it. The session underneath is whatever account is signed in
 * on dev-owner (an administrator is fine): the persisted auth state is switched to partner-only in the
 * browser, so the menu, the Settings tabs and the dashboard's "Select Owner" card render as for a partner.
 * Who the partner's owners are, and which booking plugins the server has loaded, are staged here — two
 * made-up rental companies and a plugin list — so no real owner's name or email reaches a frame.
 *
 * READ-ONLY BY CONSTRUCTION. The one write episode 51 shows — "+ Add booking plugin" → Turo, a PUT — is
 * answered here with success and never reaches the server; every other request to the API that is not a
 * GET is aborted before it leaves the browser. Episode 54 shows no write at all: its Turo card (connected,
 * two accounts) and the partner's owner list are staged answers to GETs.
 *
 * Usage:
 *   node capture-partner.js --cdp=9223
 *   node capture-partner.js --cdp=9223 --only=prt-03 --lang=es
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

// ------------------------------------------------------------------ the staged partner

const PARTNER = { firstName: 'Your Company', lastName: '', email: 'yourcompany@mail.myeztoll.com' };

// The partner's owners. The first one is given the SIGNED-IN account's id at run time, so the owner-scoped
// requests the settings page makes on its own (owner settings, toll config) are answered by the server for
// an account the session may read — only its name on screen is staged.
const owners = (firstId) => [
  { id: firstId, firstName: 'Sunrise', lastName: 'Car Rental', email: 'sunrise@mail.myeztoll.com' },
  { id: 'demo-owner-2', firstName: 'Harbor', lastName: 'Rentals', email: 'harbor@mail.myeztoll.com' },
].map((o) => ({
  ...o, distributionMode: 'OwnerShare', ownerSharePercent: 0, partnerSharePercent: 20, payoutPeriodDays: 7,
  payoutThresholdAmount: 1, accumulatedPartnerShare: 0, partnerShareDurationDays: 365,
}));

const rental = (platformId, platformName, isConfigured) => ({
  family: 'rental', authMode: 'ChallengeFlow', platformId, platformName, supportedRegions: [],
  credentialFields: [], isConfigured, secretsPresent: {}, supportsManualBookingFetch: false,
  supportsPasswordLogin: false, supportsEmailOtp: true, supportsSmsOtp: false, requiresCaptcha: false,
  emailNotificationDomains: ['turo.com'], connected: false, needsReauth: false, login: null,
});
const fleet = (platformId, platformName) => ({
  family: 'fleetmgmt', authMode: 'CredentialFields', platformId, platformName, supportedRegions: [],
  credentialFields: [], isConfigured: false, secretsPresent: {}, supportsManualBookingFetch: false,
  supportsBookingSync: true, supportsFleetSync: true, supportsCustomerSync: true, supportsWebhooks: false,
  supportsBookingCreate: false, regions: [],
});
// Episode 54: Turo already connected for the owner, with two Turo accounts, so the card shows everything a
// partner can now change — the login, removing one account, Disconnect.
const TURO_LOGIN = 'sunrise.rentals@mail.myeztoll.com';
const TURO_ACCOUNTS = {
  supportsMultipleAccounts: true,
  accounts: [
    { accountKey: 'acct-1', login: TURO_LOGIN, isDefault: true, connected: true },
    { accountKey: 'acct-2', login: 'sunrise.airport@mail.myeztoll.com', isDefault: false, connected: true },
  ],
};
const PLUGINS = (turoOn) => [
  turoOn === 'connected'
    ? { ...rental('turo', 'Turo', true), connected: true, login: TURO_LOGIN }
    : rental('turo', 'Turo', turoOn),
  fleet('hq', 'HQ Rental Software'),
  fleet('fleetwire', 'Fleetwire'),
  fleet('wheelbase', 'Wheelbase'),
];

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

// ------------------------------------------------------------------ page helpers

/** Make the persisted session a partner's: isAdmin off, isPartner on, the partner's name; and pick the owner. */
const STAGE_SESSION_FN = function (partner, selected, fakeId) {
  const auth = JSON.parse(localStorage.getItem('aegis-auth-storage') || '{}');
  if (!auth.state || !auth.state.user) return null;
  auth.state.isAdmin = false;
  auth.state.isPartner = true;
  auth.state.isOwner = true;
  auth.state.user = { ...auth.state.user, isAdmin: false, isPartner: true, isOwner: true, ...partner };
  // The portal marks "viewing as owner" only when the chosen owner is NOT the signed-in user, and the first staged
  // owner borrows the signed-in id — so in those frames the partner gets a made-up id of its own.
  if (fakeId) auth.state.user.id = fakeId;
  localStorage.setItem('aegis-auth-storage', JSON.stringify(auth));
  const app = JSON.parse(localStorage.getItem('aegis-app-storage') || '{"state":{},"version":0}');
  app.state = app.state || {};
  app.state.selectedOwner = selected;
  localStorage.setItem('aegis-app-storage', JSON.stringify(app));
  return auth.state.user.id;
};

/** Hide the dev badge and GUIDs; bring the header and sidebar back (the shared blur hides them). */
const TIDY_FN = function (showBanner) {
  document.querySelectorAll('header, nav').forEach((el) => { el.style.display = ''; });
  document.querySelectorAll('.bg-amber-400.text-amber-950, .pin-action-sandbox')
    .forEach((el) => { el.style.visibility = 'hidden'; });
  Array.from(document.querySelectorAll('span, div, a, button'))
    .filter((el) => /^\s*sandbox\s*$/i.test(el.textContent || ''))
    .forEach((el) => { el.style.visibility = 'hidden'; });
  // The staged names and addresses are made up, and the viewer has to read them: un-blur those only.
  Array.from(document.querySelectorAll('*'))
    .filter((el) => /sunrise|harbor|yourcompany@/i.test(el.textContent || '') && (el.textContent || '').length < 200)
    .forEach((el) => {
      for (let n = el; n && n !== document.body; n = n.parentElement) {
        n.classList.forEach((c) => { if (/pii|blur/i.test(c)) n.classList.remove(c); });
        if (n.style && n.style.filter) n.style.filter = '';
      }
    });
  // The shared pass hides the "viewing as owner" banner; frames about choosing an owner want it seen.
  if (showBanner) {
    Array.from(document.querySelectorAll('div, section, aside'))
      .filter((el) => /viewing as owner|viendo como propietario/i.test(el.textContent || '') && (el.textContent || '').length < 160)
      .forEach((el) => { el.style.visibility = ''; });
    // Its label ("VIEWING AS OWNER") is caught by the shared blur; the banner holds only staged data.
    document.querySelectorAll('.selected-owner-banner, .selected-owner-banner *').forEach((n) => {
      n.classList.forEach((c) => { if (/pii|blur/i.test(c)) n.classList.remove(c); });
      if (n.style) { n.style.filter = ''; n.style.visibility = ''; }
    });
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

/** Where the things the episode points at landed, as fractions of the frame (see capture-tesla.js). */
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
    } else if (kind === 'row' || kind === 'rowbtn') {
      const row = Array.from(document.querySelectorAll('tr')).filter(vis).find((r) => norm(r.textContent).includes(t)) || null;
      el = row && kind === 'rowbtn' ? row.querySelector('button') : row;
    } else if (kind === 'btn') {
      el = Array.from(document.querySelectorAll('button, a, select, input'))
        .filter(vis).find((b) => norm(b.textContent).startsWith(t) || norm(b.value) === t);
    } else if (kind === 'select') {
      el = Array.from(document.querySelectorAll('select')).filter(vis)
        .find((s) => Array.from(s.options).some((o) => norm(o.textContent).startsWith(t))) || null;
    } else {
      const cands = Array.from(document.querySelectorAll('h1,h2,h3,h4,div,span,p,label,b'))
        .filter(vis).filter((n) => norm(n.textContent).startsWith(t));
      cands.sort((a, b) => (a.textContent || '').length - (b.textContent || '').length);
      el = cands[0] || null;
      if (el && kind === 'box') {
        let n = el;
        while (n && n !== document.body && !/\b(border|shadow|rounded-lg)\b/.test(n.className || '')) n = n.parentElement;
        if (n && n !== document.body) el = n;
      }
    }
    if (!el) return;
    // Clip to the scrolling box around it — a table row is wider than the list when the list scrolls sideways.
    let { left, top, right, bottom } = el.getBoundingClientRect();
    for (let a = el.parentElement; a && a !== document.body; a = a.parentElement) {
      if (!/(auto|scroll|hidden)/.test(getComputedStyle(a).overflowX)) continue;
      const c = a.getBoundingClientRect();
      left = Math.max(left, c.left); right = Math.min(right, c.right);
      top = Math.max(top, c.top); bottom = Math.min(bottom, c.bottom);
    }
    right = Math.min(right, W);
    const r = { left, top, width: right - left, height: bottom - top };
    out[key] = [r.left / W, r.top / H, r.width / W, r.height / H].map((v) => Math.round(v * 10000) / 10000);
  });
  return out;
};

/** Click a button/tab whose text starts with `text`. */
const clickButton = (text) => async (page) => {
  const ok = await page.evaluate((t) => {
    const norm = (s) => (s || '').replace(/\s+/g, ' ').trim().toLowerCase();
    const b = Array.from(document.querySelectorAll('button, a')).find((x) => norm(x.textContent).startsWith(norm(t)));
    if (b) b.click();
    return !!b;
  }, text);
  if (!ok) throw new Error(`no button "${text}"`);
  await sleep(1500);
};

/** Right-click the table row that holds `text` — the row menu of the Partners list. A real mouse click, so
 *  React's onContextMenu sees it the way a person's would. */
const rightClickRow = (text) => async (page) => {
  const at = await page.evaluate((t) => {
    const norm = (s) => (s || '').replace(/\s+/g, ' ').trim().toLowerCase();
    const vis = (e) => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
    const row = Array.from(document.querySelectorAll('tr')).filter(vis).find((r) => norm(r.textContent).includes(norm(t)));
    if (!row) return null;
    const cell = row.querySelectorAll('td')[2] || row;
    const r = cell.getBoundingClientRect();
    return { x: r.left + r.width / 2, y: r.top + r.height / 2, hit: (document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2) || {}).tagName };
  }, text);
  if (!at) throw new Error(`no row "${text}"`);
  // The list may still be re-rendering from its first fetch, which swallows an early click — try again.
  for (let i = 0; i < 4; i += 1) {
    await page.mouse.click(at.x, at.y, { button: 'right' });
    await sleep(900);
    if (await page.evaluate(() => !!document.querySelector('div.fixed.w-56'))) return;
    const diag = await page.evaluate((x, y) => {
      let fired = 0;
      const on = () => { fired += 1; };
      window.addEventListener('contextmenu', on, true);
      const el = document.elementFromPoint(x, y);
      el && el.dispatchEvent(new MouseEvent('contextmenu', { bubbles: true, cancelable: true, clientX: x, clientY: y, button: 2 }));
      window.removeEventListener('contextmenu', on, true);
      return { fired, el: el && el.outerHTML.slice(0, 120), fixed: Array.from(document.querySelectorAll('.fixed')).map((d) => d.className).slice(0, 5) };
    }, at.x, at.y);
    await sleep(700);
    if (await page.evaluate(() => !!document.querySelector('div.fixed.w-56'))) return;
    console.log(`  row menu not open (try ${i + 1})`, JSON.stringify(diag));
    await page.keyboard.press('Escape');
    await sleep(1500);
  }
  throw new Error('row menu did not open');
};

/** Choose an option in the select that offers it (the owner picker, the plugin picker). */
const choose = (optionStart) => async (page) => {
  const ok = await page.evaluate((t) => {
    const norm = (s) => (s || '').replace(/\s+/g, ' ').trim().toLowerCase();
    const sel = Array.from(document.querySelectorAll('select'))
      .find((s) => Array.from(s.options).some((o) => norm(o.textContent).startsWith(norm(t))));
    if (!sel) return false;
    const opt = Array.from(sel.options).find((o) => norm(o.textContent).startsWith(norm(t)));
    const setter = Object.getOwnPropertyDescriptor(HTMLSelectElement.prototype, 'value').set;
    setter.call(sel, opt.value);
    sel.dispatchEvent(new Event('change', { bubbles: true }));
    return true;
  }, optionStart);
  if (!ok) throw new Error(`no option "${optionStart}"`);
  await sleep(1800);
};

/** Choose the owner on the dashboard and wait for the sidebar banner; the page's own reload can undo an early pick. */
const chooseOwner = (name) => async (page) => {
  for (let i = 0; i < 4; i += 1) {
    await choose(name)(page);
    if (await page.$('.selected-owner-banner:not(.mobile)')) return;
    await sleep(1500);
  }
  throw new Error(`owner "${name}" did not stay selected`);
};

// ------------------------------------------------------------------ the screens

function screens(L) {
  // The tab label is translated since owner-web #695 ("Plugins de reservas" in Spanish).
  const pluginsLabel = L('pluginsPage.tabBooking', 'Booking Plugins');
  const pluginsTab = clickButton(pluginsLabel);
  const myAccount = L('dashboard.partnerMyAccount', 'My account');
  return [
    // Dashboard, "My account" still selected: the Select Owner card is the point.
    { name: 'prt-01-select-owner', path: '/dashboard', selected: false, steps: [],
      measure: [['card', L('dashboard.partnerSelectOwner', 'Select Owner'), 'box'], ['picker', myAccount, 'select']] },
    // The owner chosen: the sidebar says whose account is on screen.
    { name: 'prt-02-viewing-as', path: '/dashboard', selected: false, banner: true, steps: [chooseOwner('Sunrise')],
      measure: [['card', L('dashboard.partnerSelectOwner', 'Select Owner'), 'box'], ['picker', myAccount, 'select'],
        ['banner', '.selected-owner-banner', 'tag']] },
    // Settings → Booking Plugins, nothing on yet: the "+ Add booking plugin" picker.
    { name: 'prt-03-plugins-empty', path: '/admin/settings', selected: true, banner: true, turo: false, steps: [pluginsTab],
      measure: [['tab', pluginsLabel, 'btn'], ['add', L('pluginsSettings.ownerBooking.addPlugin', '+ Add booking plugin'), 'select'],
        ['banner', '.selected-owner-banner', 'tag']] },
    // Turo picked: the card appears with "Turo enabled for this owner".
    { name: 'prt-04-turo-enabled', path: '/admin/settings', selected: true, banner: true, turo: false,
      steps: [pluginsTab, choose('Turo')],
      measure: [['tab', pluginsLabel, 'btn'], ['add', L('pluginsSettings.ownerBooking.addPlugin', '+ Add booking plugin'), 'select'],
        ['card', 'Turo', 'box'], ['toast', '[role="status"]', 'tag']] },

    // ---- episode 54: Partnership → Partners, the row menu, and the three pages it opens
    { name: 'prt-05-partners-list', path: '/partners', selected: false, steps: [],
      measure: [['title', 'h1', 'tag'], ['row', 'Sunrise', 'row'], ['dots', 'Sunrise', 'rowbtn'],
        ['search', 'input[placeholder]', 'tag']] },
    { name: 'prt-06-row-menu', path: '/partners', selected: false, steps: [rightClickRow('Sunrise')],
      measure: [['row', 'Sunrise', 'row'], ['menu', 'div.fixed.w-56', 'tag'],
        ['payment', L('partnersPage.paymentSettings', 'Payment Settings'), 'btn'],
        ['owner', L('ownerSettingsPage.ownerSettingsTab', 'Owner Settings'), 'btn'],
        ['plugins', L('pluginsPage.tabBooking', 'Booking Plugins'), 'btn'],
        ['visibility', L('ownerSettingsPage.pageVisibilityTab', 'Page Visibility'), 'btn']] },
    { name: 'prt-07-owner-settings', path: '/partners', selected: false,
      steps: [rightClickRow('Sunrise'), clickButton(L('ownerSettingsPage.ownerSettingsTab', 'Owner Settings')), settle],
      measure: [['title', 'h1', 'tag'], ['owner', 'h1 + p', 'tag'], ['save', L('ownerSettingsPage.save', 'Save'), 'btn']] },
    { name: 'prt-08-owner-plugins', path: '/partners', selected: false, turo: 'connected',
      steps: [rightClickRow('Sunrise'), clickButton(L('pluginsPage.tabBooking', 'Booking Plugins')), settle,
        hideText('TuroActivator')],
      measure: [['title', 'h1', 'tag'], ['owner', 'h1 + p', 'tag'], ['card', 'Turo', 'box'],
        ['login', 'input[type="email"]', 'tag'],
        ['accounts', L('pluginsSettings.bookingCards.connectedAccounts', 'Connected Turo accounts'), 'text'],
        ['remove', `button[title="${L('pluginsSettings.bookingCards.removeAccount', 'Remove account')}"]`, 'tag'],
        ['disconnect', L('pluginsSettings.bookingCards.disconnect', 'Disconnect'), 'btn'],
        ['add', L('pluginsSettings.ownerBooking.addPlugin', '+ Add booking plugin'), 'select']] },
    { name: 'prt-09-owner-visibility', path: '/partners', selected: false,
      steps: [rightClickRow('Sunrise'), clickButton(L('ownerSettingsPage.pageVisibilityTab', 'Page Visibility')), settle],
      measure: [['title', 'h1', 'tag'], ['owner', 'h1 + p', 'tag'],
        ['preset', L('ownerSettingsPage.visibilityPresetPlaceholder', 'Choose a preset…'), 'select'],
        ['save', L('ownerSettingsPage.save', 'Save'), 'btn']] },
  ];
}

/** Drop the paragraph holding `text` — for a line only an administrator sees (the frames run as admin, the
 *  viewer is a partner). */
const hideText = (text) => async (page) => {
  await page.evaluate((t) => {
    Array.from(document.querySelectorAll('p, div')).filter((e) => e.children.length === 0 && e.textContent.includes(t))
      .forEach((e) => e.remove());
  }, text);
};

/** The owner pages load their own data after the client-side navigation. */
async function settle(page) {
  await waitForApp(page);
  await sleep(SETTLE_MS);
}

// ------------------------------------------------------------------ run

(async () => {
  const browser = await puppeteer.connect({ browserURL: `http://127.0.0.1:${CDP_PORT}`, defaultViewport: VIEWPORT, protocolTimeout: 600000 });
  const page = await browser.newPage();
  await page.setViewport(VIEWPORT);
  page.setDefaultNavigationTimeout(60000);
  page.on('dialog', (d) => d.dismiss().catch(() => {}));

  // Who is signed in: the first staged owner borrows this id (see owners()).
  await page.goto(`${BASE}/dashboard`, { waitUntil: 'domcontentloaded' });
  await sleep(1500);
  // The id comes from the token, not the stored user: an earlier run may have left a staged partner id there.
  const selfId = await page.evaluate(() => {
    const a = JSON.parse(localStorage.getItem('aegis-auth-storage') || '{}');
    const tok = a.state && a.state.token;
    if (!tok) return null;
    const p = JSON.parse(atob(tok.split('.')[1].replace(/-/g, '+').replace(/_/g, '/')));
    return p.nameid || p.sub || p['http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier'] || p.id || null;
  });
  if (!selfId) throw new Error('nobody is signed in on dev-owner in this Chrome');
  console.log(`signed-in id from token: ${selfId.slice(0, 8)}…`);
  const saved = await page.evaluate(() => ({ auth: localStorage.getItem('aegis-auth-storage'), app: localStorage.getItem('aegis-app-storage') }));
  const OWNERS = owners(selfId);
  const SELECTED = { id: selfId, email: OWNERS[0].email, firstName: OWNERS[0].firstName, lastName: OWNERS[0].lastName };

  let current = null;
  let turoOn = false;
  const blocked = [];
  await page.setRequestInterception(true);
  page.on('request', (req) => {
    const url = req.url();
    const m = req.method();
    const json = (body) => req.respond({ status: 200, contentType: 'application/json', body: JSON.stringify(body) }).catch(() => {});
    if (current && m === 'GET' && /\/OwnerTollBalance\/my-partnership-owners(\?|$)/i.test(url)) {
      return json({ result: OWNERS, reason: 0 });
    }
    if (current && m === 'GET' && /\/OwnerTollBalance\/my-partnership-owners-paged(\?|$)/i.test(url)) {
      return json({ result: { items: OWNERS, totalCount: OWNERS.length, page: 1, pageSize: 10 }, reason: 0 });
    }
    if (current && m === 'GET' && /\/api\/owners\/[^/]+\/booking-plugins\/turo\/accounts(\?|$)/.test(url)) {
      return json(turoOn === 'connected' ? TURO_ACCOUNTS : { supportsMultipleAccounts: false, accounts: [] });
    }
    if (current && m === 'GET' && /\/api\/owners\/[^/]+\/booking-plugins(\?|$)/.test(url)) {
      return json(PLUGINS(turoOn));
    }
    if (current && m === 'PUT' && /\/api\/owners\/[^/]+\/booking-plugins\/turo(\?|$)/.test(url)) {
      turoOn = true;
      return json({ success: true });
    }
    if (m !== 'GET' && m !== 'HEAD' && m !== 'OPTIONS' && /\/api\//i.test(url)) {
      blocked.push(`${m} ${url}`);
      return req.abort('blockedbyclient').catch(() => {});
    }
    return req.continue().catch(() => {});
  });

  const blurArgs = [REDACTION.markerSource(), REDACTION.PII_CLASS, RENAME];
  const failures = [];
  const boxesFile = path.join(SHOTS, '_partner_boxes.json');
  const boxes = fs.existsSync(boxesFile) ? JSON.parse(fs.readFileSync(boxesFile, 'utf8')) : {};

  for (const lang of LANGS) {
    fs.mkdirSync(path.join(SHOTS, lang), { recursive: true });
    const L = labeller(lang);
    const list = screens(L).filter((s) => !ONLY.length || ONLY.some((o) => s.name.includes(o)));
    for (const s of list) {
      process.stdout.write(`[${lang}] ${s.name}\n`);
      current = s;
      turoOn = s.turo === 'connected' ? 'connected' : !!s.turo;
      try {
        await page.goto(`${BASE}/dashboard`, { waitUntil: 'domcontentloaded' });
        await page.evaluate(STAGE_SESSION_FN, PARTNER, s.selected ? SELECTED : null, s.banner ? 'demo-partner' : null);
        await page.goto(`${BASE}${s.path}`, { waitUntil: 'domcontentloaded' });
        for (let i = 0; i < 2; i += 1) {
          await setLanguage(page, lang);
          await page.reload({ waitUntil: 'domcontentloaded' });
          await sleep(1500);
        }
        await waitForApp(page);
        await sleep(SETTLE_MS);
        for (const step of s.steps) await step(page);
        await sleep(1000);
        await page.evaluate(BLUR_FN, ...blurArgs);
        await page.evaluate(TIDY_FN, !!s.banner);
        await page.evaluate(() => window.scrollTo(0, 0));
        await sleep(600);
        boxes[`${lang}/${s.name}`] = await page.evaluate(MEASURE_FN, s.measure);
        fs.writeFileSync(path.join(SHOTS, lang, `${s.name}.png`), await page.screenshot());
      } catch (err) {
        console.log(`  FAILED: ${err.message}`);
        failures.push({ lang, name: s.name, error: err.message });
      }
    }
  }

  current = null;
  // Put the session back as it was: the staging rewrote it to a partner's.
  await page.goto(`${BASE}/dashboard`, { waitUntil: 'domcontentloaded' }).catch(() => {});
  await page.evaluate((v) => {
    const a = JSON.parse(v.auth || '{}');
    if (a.state && a.state.user) { a.state.user.id = v.id; }
    localStorage.setItem('aegis-auth-storage', JSON.stringify(a));
    localStorage.removeItem('aegis-app-storage');
  }, { ...saved, id: selfId }).catch(() => {});
  fs.writeFileSync(boxesFile, JSON.stringify(boxes, null, 2));
  if (blocked.length) console.log(`\nWrites blocked (nothing saved):\n  ${blocked.join('\n  ')}`);
  console.log(`\nDone. ${failures.length ? 'Failures: ' + JSON.stringify(failures) : 'all captured'}`);
  await page.close().catch(() => {});
  await browser.disconnect();
})().catch((e) => { console.error('FATAL', e); process.exit(1); });
