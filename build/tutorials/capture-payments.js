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
 * Screenshots for the payment-options episodes (36-38), from the DEV portal.
 *
 * The switches that choose a payment option are admin-only: the "Who collects payments" card
 * (Administration -> Settings, for the owner being viewed) and "Charge Target" (the owner's toll
 * settings page). So, like capture-collections.js, this runs against an administrator session in
 * a Chrome started with --remote-debugging-port, viewing the test owner.
 *
 * READ-ONLY BY CONSTRUCTION. Showing the "Pay per plate" state means pressing its button, and that
 * button saves at once (it turns all three collectors off for the owner). Every request to the API
 * that is not a GET is therefore aborted before it leaves the browser: the card redraws in its new
 * state from local React state, and nothing on the server changes. The aborts are logged.
 *
 * Usage:
 *   node capture-payments.js --cdp=9223 --owner=<ownerId>
 *   node capture-payments.js --cdp=9223 --owner=<ownerId> --only=pay-12 --lang=es
 */

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
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
const OWNER = argVal('owner', '');
const LANGS = argVal('lang', 'en,es').split(',').map((s) => s.trim()).filter(Boolean);
const ONLY = argVal('only', '').split(',').map((s) => s.trim()).filter(Boolean);
const SHOTS = path.join(__dirname, 'shots');

const VIEWPORT = { width: 1600, height: 1000, deviceScaleFactor: 2 };
const SETTLE_MS = 2600;

if (!OWNER) throw new Error('--owner=<ownerId> is required (the test owner the episodes show)');
if (!/^https:\/\/dev-/.test(BASE)) throw new Error(`refusing a non-dev base: ${BASE}`);

// The account on dev is ours; the series shows a neutral company throughout.
const RENAME = [
  ['Aegis AG Soft LLC', 'Your Company'],
  ['Aegis AA Soft LLC', 'Your Company'],
  ['ELIZAVETA GAEVAYA', 'YOUR COMPANY'],
  ['Elizaveta Gaevaya', 'Your Company'],
  ['aegisagsoft@gmail.com', 'yourcompany@mail.myeztoll.com'],
  ['aegisaasoft@outlook.com', 'yourcompany@mail.myeztoll.com'],
  ['aegis admin', 'Your Company'],
];

/*
 * What an owner's screen in this series never shows, removed after the shared redaction pass:
 * the dev sandbox badge, the owner's GUID beside "Settings for", the admin account's initials in
 * the avatar (the series says YC), the Turo-lock hint of OUR test account (it would tell every
 * viewer that Aegis always collects), and — with `isolate` — every other admin card on the page,
 * one of which carries a masked API key.
 */
const TIDY_FN = function (isolateTitle, hideExample) {
  // The live calculator on the Distribution Settings card hard-codes the service fee at $0.50 a
  // toll, whatever the owner's real fee is — a frame of it would teach a wrong number.
  if (hideExample) {
    const ex = Array.from(document.querySelectorAll('div'))
      .filter((d) => /^(example|ejemplo)\b/i.test((d.textContent || '').trim()) && /stripe/i.test(d.textContent || ''));
    ex.sort((x, y) => (x.textContent || '').length - (y.textContent || '').length);
    // The smallest match is the lines under the heading; the box around them starts with the same
    // words, so climb while it does and hide the whole box, heading and frame included.
    let box = ex[0];
    const starts = (el) => /^(example|ejemplo)/i.test((el.textContent || '').trim());
    while (box && box.parentElement && starts(box.parentElement)) box = box.parentElement;
    if (box) box.style.display = 'none';
  }
  document.querySelectorAll('.bg-amber-400.text-amber-950, .pin-action-sandbox')
    .forEach((el) => { el.style.visibility = 'hidden'; });
  const GUID = /\s*\(?[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\)?/gi;
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null);
  for (let n = walker.nextNode(); n; n = walker.nextNode()) {
    const v = n.nodeValue || '';
    if (GUID.test(v)) n.nodeValue = v.replace(GUID, '');
    GUID.lastIndex = 0;
    if (v.trim() === 'AA') n.nodeValue = v.replace('AA', 'YC');
  }
  document.querySelectorAll('p, div, span').forEach((el) => {
    if (el.children.length === 0 && /no payment gateway of its own|no tiene pasarela de pago propia/i
      .test(el.textContent || '')) el.style.display = 'none';
  });
  // The card the frame is about: the nearest box around its title that is taller than a
  // heading row. Marked, not hidden around — the capture then photographs the element alone.
  document.querySelectorAll('[data-pay-card]').forEach((el) => el.removeAttribute('data-pay-card'));
  if (isolateTitle) {
    const want = isolateTitle.trim().toLowerCase();
    const head = Array.from(document.querySelectorAll('h1,h2,h3,h4,h5,h6,span,div'))
      .find((n) => n.children.length <= 1 && (n.textContent || '').trim().toLowerCase() === want);
    let card = head;
    while (card && card.getBoundingClientRect().height < 120) card = card.parentElement;
    if (card) card.setAttribute('data-pay-card', '1');
  }
};

function labeller(lang) {
  let bundle = {};
  try {
    bundle = JSON.parse(fs.readFileSync(
      `C:/aegis-aa/aegis-owner-web/src/locales/${lang}/common.json`, 'utf8'));
  } catch (e) { /* English fallbacks */ }
  return (key, fallback) => {
    const raw = key.split('.').reduce(
      (acc, part) => (acc && typeof acc === 'object' ? acc[part] : undefined), bundle);
    return typeof raw === 'string' && raw.trim() ? raw : fallback;
  };
}

/**
 * Scroll the element that carries `text` (or matches `selector`) to a fixed height in the window,
 * so the frame is a 1600x1000 view like every other screen and the coordinates in series_m.py
 * stay put between runs. `at` is where its top lands, as a fraction of the window.
 */
function scrollTo({ text, selector, at = 0.18 }) {
  return async (page) => {
    // A card that loads its own data paints a beat after the page; one second chance.
    let ok = false;
    for (let attempt = 0; attempt < 2 && !ok; attempt += 1) {
      if (attempt) await sleep(3500);
      ok = await page.evaluate((want, sel, frac) => {
      let el = sel ? document.querySelector(sel) : null;
      if (!el && want) {
        const w = want.toLowerCase();
        el = Array.from(document.querySelectorAll('h1,h2,h3,h4,h5,h6,label,div,span'))
          .filter((n) => n.children.length <= 2)
          .find((n) => (n.textContent || '').trim().toLowerCase() === w);
      }
      if (!el) return false;
      const top = el.getBoundingClientRect().top + window.scrollY;
      window.scrollTo(0, Math.max(0, top - window.innerHeight * frac));
      return true;
    }, text || '', selector || '', at);
    }
    if (!ok) throw new Error(`nothing to scroll to: ${text || selector}`);
    await sleep(900);
  };
}

/*
 * Lay one card on a plain 1600x1000 frame (compose_card.py does the pixels: a second browser tab
 * would be a background tab, and Chrome throttles those to minutes per screenshot). The card is
 * centred and scaled down only when it would not fit; where it landed, as fractions of the frame,
 * goes to shots/_pay_boxes.json — the numbers series_m.py rings are measured from.
 */
function compose(png, out) {
  const raw = out.replace(/\.png$/, '.card.png');
  fs.writeFileSync(raw, png);
  const res = spawnSync('python', [path.join(__dirname, 'compose_card.py'), raw, out], { encoding: 'utf8' });
  if (res.status !== 0) throw new Error(`compose_card.py: ${res.stderr || res.stdout}`);
  fs.unlinkSync(raw);
  return JSON.parse(res.stdout);
}

function screens(L) {
  const card = L('pluginsSettings.collector.title', 'Who collects payments');
  const plate = L('pluginsSettings.collector.modePerPlate', 'Pay per plate');
  return [
    { name: 'pay-10-collector', route: '/admin/settings', isolate: card, steps: [scrollTo({ text: card })] },
    {
      name: 'pay-11-collector-per-plate',
      route: '/admin/settings',
      isolate: card,
      steps: [scrollTo({ text: card }), async (p) => clickText(p, plate), scrollTo({ text: card })],
    },
    {
      name: 'pay-12-charge-target',
      route: `/owners/${OWNER}`,
      isolate: L('ownerTollSettings.settings.title', 'Distribution Settings'),
      hideExample: true,
      steps: [scrollTo({ selector: '#chargeTarget', at: 0.45 })],
    },
    // The amounts (episodes 39-40): one admin card of the owner's toll settings page per frame.
    ...[
      ['pay-13-toll-service', 'ownerTollSettings.tollService.title', 'Toll Service Settings (Admin)'],
      ['pay-14-violation-fee', 'ownerTollSettings.violationFee.title', 'Violation Fee Settings (Admin)'],
      ['pay-15-booking-settings', 'ownerTollSettings.bookingSettings.title', 'Booking Settings (Admin)'],
      ['pay-16-gps-fee', 'ownerTollSettings.gpsNavigatorFee.title', 'GPS Navigator Billing (Admin)'],
      ['pay-17-partner-share', 'ownerTollSettings.partner.title', 'Partner Assignment'],
    ].map(([name, key, fallback]) => ({
      name,
      route: `/owners/${OWNER}`,
      isolate: L(key, fallback),
      steps: [scrollTo({ text: L(key, fallback) })],
    })),
  ];
}

(async () => {
  const browser = await puppeteer.connect({
    browserURL: `http://127.0.0.1:${CDP_PORT}`,
    defaultViewport: VIEWPORT,
    protocolTimeout: 600000,
  });
  const page = await browser.newPage();
  await page.setViewport(VIEWPORT);
  page.setDefaultNavigationTimeout(60000);
  // "Leave the page? Changes you made may not be saved" follows the Pay-per-plate press: leaving
  // is exactly right (nothing is to be saved), and dismissing it cancels the next navigation.
  // Any other dialog is dismissed.
  page.on('dialog', (d) => (d.type() === 'beforeunload' ? d.accept() : d.dismiss()).catch(() => {}));

  // Nothing but reads reaches the server — see the header.
  const blocked = [];
  await page.setRequestInterception(true);
  page.on('request', (req) => {
    const m = req.method();
    if (m !== 'GET' && m !== 'HEAD' && m !== 'OPTIONS' && /\/api\//i.test(req.url())) {
      blocked.push(`${m} ${req.url()}`);
      req.abort('blockedbyclient').catch(() => {});
    } else {
      req.continue().catch(() => {});
    }
  });

  const blurArgs = [REDACTION.markerSource(), REDACTION.PII_CLASS, RENAME];
  const boxesFile = path.join(SHOTS, '_pay_boxes.json');
  const boxes = fs.existsSync(boxesFile) ? JSON.parse(fs.readFileSync(boxesFile, 'utf8')) : {};
  const failures = [];

  for (const lang of LANGS) {
    fs.mkdirSync(path.join(SHOTS, lang), { recursive: true });
    const list = screens(labeller(lang)).filter((s) => !ONLY.length || ONLY.some((o) => s.name.includes(o)));
    for (const s of list) {
      process.stdout.write(`[${lang}] ${s.name} ${s.route}\n`);
      try {
        // The app writes its current language back on the way out, so a page left in the previous
        // run's language overwrites a switch made from inside it. Switch, reload, then switch and
        // reload again on the screen itself.
        await page.goto(`${BASE}${s.route}`, { waitUntil: 'domcontentloaded' });
        for (let i = 0; i < 2; i += 1) {
          await setLanguage(page, lang);
          await page.reload({ waitUntil: 'domcontentloaded' });
          await sleep(1500);
        }
        await waitForApp(page);
        await sleep(SETTLE_MS);
        await page.evaluate(BLUR_FN, ...blurArgs);
        for (const step of s.steps) await step(page);
        await page.evaluate(BLUR_FN, ...blurArgs);
        await page.evaluate(TIDY_FN, s.isolate || '', !!s.hideExample);
        await sleep(900);
        const out = path.join(SHOTS, lang, `${s.name}.png`);
        let cardEl = s.isolate ? await page.$('[data-pay-card]') : null;
        if (s.isolate && !cardEl) {                  // still painting: one more pass
          await sleep(4000);
          await page.evaluate(TIDY_FN, s.isolate, !!s.hideExample);
          cardEl = await page.$('[data-pay-card]');
        }
        if (s.isolate && !cardEl) {
          const seen = await page.evaluate(() => Array.from(document.querySelectorAll('h1,h2,h3,h4,h5,h6'))
            .map((h) => (h.textContent || '').trim()).filter(Boolean).slice(0, 25).join(' | '));
          throw new Error(`no card titled "${s.isolate}" — headings on the page: ${seen}`);
        }
        if (cardEl) {
          await cardEl.scrollIntoView();
          boxes[`${lang}/${s.name}`] = compose(await cardEl.screenshot(), out);
        } else {
          fs.writeFileSync(out, await page.screenshot());
        }
      } catch (err) {
        console.log(`  FAILED: ${err.message}`);
        failures.push({ lang, name: s.name, error: err.message });
      }
    }
  }

  fs.writeFileSync(boxesFile, JSON.stringify(boxes, null, 2));
  if (blocked.length) console.log(`\nWrites blocked (nothing saved):\n  ${blocked.join('\n  ')}`);
  console.log(`\nDone. ${failures.length ? 'Failures: ' + JSON.stringify(failures) : 'all captured'}`);
  await page.close().catch(() => {});
  await browser.disconnect();
})().catch((e) => {
  console.error('FATAL', e);
  process.exit(1);
});
