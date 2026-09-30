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
 * Screenshots for the collections episodes (31-33), from the DEV portal.
 *
 * Why not docs/tools/capture-screenshots.js: that harness refuses an admin session on purpose,
 * because an owner's guide captured under an admin documents a portal the reader does not have.
 * Here the only session available is an administrator VIEWING AS the owner who holds the test
 * cases, which is the same data an owner sees on this page — so the refusal is not useful and
 * this file does the narrow job instead. The admin banner is hidden before the shutter for the
 * same reason: it is not part of what the episode is teaching.
 *
 * Everything else follows the harness: 1600x1000 at deviceScaleFactor 2, the UI language forced
 * through localStorage, personal data blurred in-page by the SHARED rules in
 * docs/tools/redaction-rules.js — the queue lists real drivers, and dev shares production's
 * people — and the account renamed to the neutral company the rest of the series uses.
 *
 * Usage:
 *   node capture-collections.js --cdp=9223
 *   node capture-collections.js --cdp=9223 --only=col-10 --lang=en
 */

const fs = require('fs');
const path = require('path');
const puppeteer = require('C:/aegis-aa/node_modules/puppeteer-core');
const REDACTION = require('C:/aegis-aa/docs/tools/redaction-rules');
const { BLUR_FN, clickText, waitForApp, setLanguage } = require('./capture-common');

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
// The portal is a single-page app: a `domcontentloaded` navigation returns an empty shell, and
// the first run shot seven all-white frames because of it. Every screen waits for its own
// content to exist (waitForApp, capture-common.js) before the settle delay starts.
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// The account on dev is ours; the series shows a neutral company throughout.
const RENAME = [
  ['Aegis AG Soft LLC', 'Your Company'],
  ['Aegis AA Soft LLC', 'Your Company'],
  ['ELIZAVETA GAEVAYA', 'YOUR COMPANY'],
  ['Elizaveta Gaevaya', 'Your Company'],
  ['aegisagsoft@gmail.com', 'yourcompany@mail.myeztoll.com'],
  ['aegisaasoft@outlook.com', 'yourcompany@mail.myeztoll.com'],
];

// ---------------------------------------------------------------- labels

/** Resolve the label the UI renders, in the language being captured. */
function labeller(lang) {
  let bundle = {};
  try {
    bundle = JSON.parse(fs.readFileSync(
      `C:/aegis-aa/aegis-owner-web/src/locales/${lang}/common.json`, 'utf8'));
  } catch (e) {
    console.log(`(no locale bundle for ${lang} — clicking English labels)`);
  }
  return (key, fallback) => {
    const raw = key.split('.').reduce(
      (acc, part) => (acc && typeof acc === 'object' ? acc[part] : undefined), bundle);
    return typeof raw === 'string' && raw.trim() ? raw : fallback;
  };
}

// ---------------------------------------------------------------- in-page work

/** Expand the first case in the table: the driver's name in each row is the toggle. */
async function openFirstEvidence(page) {
  const ok = await page.evaluate(() => {
    const row = document.querySelector('table tbody tr');
    if (!row) return false;
    const btn = row.querySelector('button');
    if (!btn) return false;
    btn.scrollIntoView({ block: 'center' });
    btn.click();
    return true;
  });
  if (!ok) throw new Error('no case row to expand');
  await sleep(2500);
}

// ---------------------------------------------------------------- screens

function screens(L) {
  const tab = (key, fallback) => async (p) => clickText(p, L(key, fallback));
  return [
    {
      name: 'col-10-queue',
      route: '/payments/collections',
      steps: [tab('collectionsQueue.tabPending', 'Awaiting approval')],
    },
    {
      name: 'col-11-evidence',
      route: '/payments/collections',
      steps: [tab('collectionsQueue.tabPending', 'Awaiting approval'), openFirstEvidence],
    },
    {
      name: 'col-12-approved',
      route: '/payments/collections',
      steps: [tab('collectionsQueue.tabApproved', 'Approved')],
    },
    {
      name: 'col-13-placed',
      route: '/payments/collections',
      steps: [tab('collectionsQueue.tabPlaced', 'With the agency')],
    },
    {
      name: 'col-14-partial',
      route: '/payments/collections',
      steps: [tab('collectionsQueue.tabPartial', 'Part-recovered')],
    },
    {
      name: 'col-15-declined',
      route: '/payments/collections',
      steps: [tab('collectionsQueue.tabDeclined', 'Declined')],
    },
    {
      name: 'col-16-settings-agencies',
      route: '/settings',
      steps: [tab('ownerSettingsPage.collectionsTab', 'Collections')],
    },
  ];
}

// ---------------------------------------------------------------- main

(async () => {
  const browser = await puppeteer.connect({
    browserURL: `http://127.0.0.1:${CDP_PORT}`,
    defaultViewport: VIEWPORT,
    protocolTimeout: 600000,
  });
  const page = await browser.newPage();
  await page.setViewport(VIEWPORT);
  page.setDefaultNavigationTimeout(60000);
  page.on('dialog', (d) => d.accept().catch(() => {}));

  const blurArgs = [REDACTION.markerSource(), REDACTION.PII_CLASS, RENAME];
  const failures = [];

  for (const lang of LANGS) {
    fs.mkdirSync(path.join(SHOTS, lang), { recursive: true });
    const L = labeller(lang);
    const list = screens(L).filter((s) => !ONLY.length || ONLY.some((o) => s.name.includes(o)));

    await page.goto(BASE, { waitUntil: 'domcontentloaded' });
    await setLanguage(page, lang);
    await waitForApp(page).catch(() => {});

    for (const s of list) {
      process.stdout.write(`[${lang}] ${s.name} ${s.route}\n`);
      try {
        await page.goto(`${BASE}${s.route}`, { waitUntil: 'domcontentloaded' });
        // Set the language, then RELOAD: the app reads it at start-up, so a page already painted
        // in the previous run's language keeps its labels and every click-by-text misses.
        await setLanguage(page, lang);
        await page.reload({ waitUntil: 'domcontentloaded' });
        await waitForApp(page);
        await sleep(SETTLE_MS);
        for (const step of s.steps || []) await step(page);
        await page.evaluate(BLUR_FN, ...blurArgs);
        await sleep(900);
        const buf = await page.screenshot({ fullPage: true });
        fs.writeFileSync(path.join(SHOTS, lang, `${s.name}.png`), buf);
      } catch (err) {
        console.log(`  FAILED: ${err.message}`);
        failures.push({ lang, name: s.name, error: err.message });
      }
    }
  }

  fs.writeFileSync(path.join(SHOTS, '_collections_manifest.json'),
    JSON.stringify({ base: BASE, langs: LANGS, failures }, null, 2));
  console.log(`\nDone. ${failures.length ? 'Failures: ' + JSON.stringify(failures) : 'all captured'}`);
  await page.goto('about:blank').catch(() => {});
  await browser.disconnect();
})().catch((e) => {
  console.error('FATAL', e);
  process.exit(1);
});
