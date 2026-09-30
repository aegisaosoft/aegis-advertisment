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
 * Screenshots for the registration episodes (34-35): /create-owner and /create-partner.
 *
 * Both pages are public, so unlike every other capture in this folder nothing has to be
 * signed in to. They are walked on the DEV portal — the public sandbox, where an account is
 * not real and no payment is ever charged — with a made-up person typed into the form. The
 * only real thing the run creates is one sandbox owner, because the agreement page that
 * follows the wizard exists only for a submitted registration. That happens once: the
 * agreement's key is written to `shots/_reg_manifest.json`, and the Spanish run (and every
 * later run) revisits the same agreement in its own language instead of registering again.
 *
 * The sandbox marks itself — an amber banner on the wizard, a chip in the header — and
 * those are hidden before the shutter: the episode teaches the production page, which does
 * not have them.
 *
 * Same frame as the rest of the series: 1600x1000 at deviceScaleFactor 2, the UI language
 * forced through localStorage, into shots/<lang>/ which build.py reads first.
 *
 * Usage:
 *   node capture-register.js                  # en then es
 *   node capture-register.js --lang=es --only=reg-2
 *   node capture-register.js --base=https://dev-owner.myeztoll.com
 */

const fs = require('fs');
const path = require('path');

// The sandbox test account's password is not in git: env TUTORIAL_SANDBOX_PASSWORD, else the
// gitignored _sandbox_password.txt next to this script (the same arrangement as the ElevenLabs key).
function sandboxPassword() {
  if (process.env.TUTORIAL_SANDBOX_PASSWORD) return process.env.TUTORIAL_SANDBOX_PASSWORD;
  const file = path.join(__dirname, '_sandbox_password.txt');
  if (fs.existsSync(file)) return fs.readFileSync(file, 'utf8').trim();
  throw new Error('no sandbox password: set TUTORIAL_SANDBOX_PASSWORD or create _sandbox_password.txt');
}
const puppeteer = require('C:/aegis-aa/node_modules/puppeteer-core');

const args = process.argv.slice(2);
const argVal = (name, dflt) => {
  const hit = args.find((a) => a.startsWith(`--${name}=`));
  return hit ? hit.slice(name.length + 3) : dflt;
};

const BASE = argVal('base', 'https://dev-owner.myeztoll.com');
const LANGS = argVal('lang', 'en,es').split(',').map((s) => s.trim()).filter(Boolean);
const ONLY = argVal('only', '').split(',').map((s) => s.trim()).filter(Boolean);
const SHOTS = path.join(__dirname, 'shots');
const MANIFEST = path.join(SHOTS, '_reg_manifest.json');
const PROFILE = argVal('profile', 'C:/Users/Alexander/AppData/Local/Temp/claude/reg-doc-profile');

const CHROME = [
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
].find((p) => fs.existsSync(p));

const VIEWPORT = { width: 1600, height: 1000, deviceScaleFactor: 2 };
const SETTLE_MS = 2200;
const READY_TIMEOUT_MS = 40000;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// The person on the form. Nobody: the company is the neutral one the whole series shows,
// the phone is in the 555-01xx block reserved for fiction, and the mailbox is on our own
// relay domain so nothing can be delivered to a stranger.
const PERSON = {
  companyName: 'Your Company',
  firstName: 'Jamie',
  lastName: 'Carter',
  email: argVal('email', ''),   // per language, see emailFor()
  phoneNumber: '2015550123',
  birth: { month: '6', day: '15', year: '1985' },
  password: sandboxPassword(),
  addressLine1: '100 Main Street',
  city: 'Red Bank',
  state: 'NJ',
  zipCode: '07701',
};

// ---------------------------------------------------------------- helpers

/**
 * The address typed into the form. The English run registers it, and from then on the sandbox
 * refuses the same address ("already registered", Next disabled) — so every other language
 * types a variant of it and never submits.
 */
function emailFor(lang) {
  if (PERSON.email) return PERSON.email;
  return lang === 'en' ? 'yourcompany@mail.myeztoll.com' : `yourcompany.${lang}@mail.myeztoll.com`;
}

const HIDE_SANDBOX_CSS = `
  .bg-amber-400.text-amber-950, .pin-action-sandbox { display: none !important; }
`;

async function hideSandbox(page) {
  await page.evaluate((css) => {
    if (document.getElementById('__reg_hide')) return;
    const st = document.createElement('style');
    st.id = '__reg_hide';
    st.textContent = css;
    document.head.appendChild(st);
  }, HIDE_SANDBOX_CSS);
}

async function waitForApp(page) {
  await page.waitForFunction(
    () => (document.body ? document.body.innerText.trim().length > 40 : false),
    { timeout: READY_TIMEOUT_MS, polling: 500 },
  );
}

async function setLanguage(page, lang) {
  await page.evaluate((l) => {
    try { localStorage.setItem('aegis-language', l); } catch (e) { /* ignore */ }
  }, lang);
}

async function goTo(page, route, lang) {
  const url = route.startsWith('http') ? route : `${BASE}${route}`;
  await page.goto(url, { waitUntil: 'domcontentloaded' });
  await waitForApp(page);
  // The language lives in localStorage of this origin; the first visit sets it and reloads.
  const current = await page.evaluate(() => localStorage.getItem('aegis-language'));
  if (current !== lang) {
    await setLanguage(page, lang);
    await page.reload({ waitUntil: 'domcontentloaded' });
    await waitForApp(page);
  }
  await hideSandbox(page);
  await sleep(SETTLE_MS);
}

/** Click the last visible, enabled button whose text reads like `text` (exact first). */
async function clickButton(page, text) {
  const ok = await page.evaluate((want) => {
    const w = want.toLowerCase();
    const visible = (el) => el.getClientRects().length > 0;
    const btns = Array.from(document.querySelectorAll('button, a'))
      .filter((el) => visible(el) && !el.disabled);
    const txt = (el) => (el.innerText || el.textContent || '').trim().toLowerCase();
    const exact = btns.filter((el) => txt(el) === w);
    const holds = btns.filter((el) => txt(el).includes(w));
    const pick = (exact.length ? exact : holds).pop();
    if (!pick) return false;
    pick.scrollIntoView({ block: 'center' });
    pick.click();
    return true;
  }, text);
  if (!ok) throw new Error(`no enabled button reads "${text}"`);
  await sleep(1500);
}

async function typeInto(page, selector, value) {
  await page.waitForSelector(selector, { visible: true, timeout: 15000 });
  await page.click(selector, { clickCount: 3 });
  await page.type(selector, value, { delay: 15 });
}

async function fillInfo(page, lang) {
  await typeInto(page, 'input[name="companyName"]', PERSON.companyName);
  await typeInto(page, 'input[name="firstName"]', PERSON.firstName);
  await typeInto(page, 'input[name="lastName"]', PERSON.lastName);
  await typeInto(page, 'input[name="email"]', emailFor(lang));
  await typeInto(page, 'input[name="phoneNumber"]', PERSON.phoneNumber);
  await page.select('select[name="birthMonth"]', PERSON.birth.month);
  await page.select('select[name="birthDay"]', PERSON.birth.day);
  await page.select('select[name="birthYear"]', PERSON.birth.year);
  const pw = await page.$$('input[type="password"]');
  if (pw.length < 2) throw new Error('password fields not found');
  await pw[0].type(PERSON.password, { delay: 15 });
  await pw[1].type(PERSON.password, { delay: 15 });
  // The email is checked against existing accounts on blur; Next stays disabled until then.
  await page.evaluate(() => document.activeElement && document.activeElement.blur());
  await sleep(2500);
  const taken = await page.evaluate(() => /already|ya est|taken/i.test(document.body.innerText)
    && !!document.querySelector('.text-red-500, .text-red-600'));
  if (taken) throw new Error(`email ${emailFor(lang)} is already registered on ${BASE} — pass --email=`);
}

async function fillLocation(page) {
  await typeInto(page, 'input[name="addressLine1"]', PERSON.addressLine1);
  await typeInto(page, 'input[name="city"]', PERSON.city);
  await typeInto(page, 'input[name="state"]', PERSON.state);
  await typeInto(page, 'input[name="zipCode"]', PERSON.zipCode);
  await page.evaluate(() => document.activeElement && document.activeElement.blur());
  await sleep(600);
}

const NEXT = { en: 'Next', es: 'Siguiente' };
const START = { en: 'Get Started', es: 'Comenzar' };
const ACCEPT = { en: 'Accept Agreement', es: 'Aceptar' };
const REDACTION = require('C:/aegis-aa/docs/tools/redaction-rules');

/** Blur what the shared rules call personal data — the portal's own footer contacts, mostly. */
async function blurPortal(page) {
  await page.evaluate((markerSrc, piiClass) => {
    if (!document.getElementById('__doc_blur_style')) {
      const st = document.createElement('style');
      st.id = '__doc_blur_style';
      st.textContent = `.${piiClass}{filter:blur(5px)!important;-webkit-filter:blur(5px)!important;}`;
      document.head.appendChild(st);
    }
    // eslint-disable-next-line no-eval
    const mark = eval(markerSrc);
    mark();
  }, REDACTION.markerSource(), REDACTION.PII_CLASS);
  await sleep(400);
}

/** Tick every acknowledgement in the agreement and draw a signature; nothing is submitted. */
async function tickAndSign(page) {
  await scrollAgreementToEnd(page);
  const n = await page.evaluate(() => {
    const boxes = Array.from(document.querySelectorAll(
      'input.owner-ack-checkbox, input.owner-ack-checkbox-master',
    ));
    boxes.forEach((b) => { b.scrollIntoView({ block: 'center' }); if (!b.checked) b.click(); });
    return boxes.length;
  });
  if (n < 3) throw new Error(`only ${n} acknowledgement boxes found`);
  await sleep(600);
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await sleep(400);
  const canvas = await page.$('canvas');
  if (!canvas) throw new Error('signature canvas not found');
  const box = await canvas.boundingBox();
  // A handwritten-looking stroke: two loops across the pad.
  const x0 = box.x + box.width * 0.25;
  const y0 = box.y + box.height * 0.55;
  await page.mouse.move(x0, y0);
  await page.mouse.down();
  const pts = 60;
  for (let i = 1; i <= pts; i++) {
    const u = i / pts;
    const x = x0 + box.width * 0.5 * u;
    const y = y0 + Math.sin(u * Math.PI * 4) * box.height * 0.22 - u * box.height * 0.1;
    await page.mouse.move(x, y, { steps: 2 });
  }
  await page.mouse.up();
  await sleep(600);
}

/** Sign in as the sandbox person the English run registered, unless a session already exists. */
async function ensureSignedIn(page, lang) {
  await goTo(page, '/login', lang);
  const needs = await page.$('input[type="password"]');
  if (needs) {
    await typeInto(page, 'input[type="email"]', emailFor('en'));
    await page.type('input[type="password"]', PERSON.password, { delay: 15 });
    await page.click('button[type="submit"]');
    await page.waitForFunction(() => !/\/login/.test(location.pathname), { timeout: 60000, polling: 500 });
    await waitForApp(page);
    await sleep(SETTLE_MS);
  }
}

/**
 * Stripe's page names the sandbox ("My E-Z Toll sandbox") and offers test shortcuts; the episode
 * teaches the production page, so those are rewritten and hidden before the shutter. Its language
 * follows the footer selector rather than the browser, so Spanish is chosen there.
 */
async function dressStripe(page) {
  await page.evaluate(() => {
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    const nodes = [];
    for (let n = walker.nextNode(); n; n = walker.nextNode()) nodes.push(n);
    nodes.forEach((n) => {
      if (/My E-Z Toll sandbox/i.test(n.nodeValue)) n.nodeValue = n.nodeValue.replace(/My E-Z Toll sandbox/gi, 'My E-Z Toll');
    });
    const TEST = /(test (phone|code|account|bank)|is not needed for test|for test accounts|de prueba)/i;
    // The "Skip this with a test phone number" box: the shortcut button and the block around
    // it, up to the first ancestor that holds a real field.
    Array.from(document.querySelectorAll('button, a, [role="button"]')).forEach((btn) => {
      if (!TEST.test((btn.innerText || btn.textContent || '').trim())) return;
      let block = btn;
      while (block.parentElement && block.parentElement !== document.body
             && !block.parentElement.querySelector('input, select, textarea')
             && (block.parentElement.textContent || '').trim().length < 200) {
        block = block.parentElement;
      }
      block.style.display = 'none';
    });
    // A hint line under a field is a leaf: only the line goes, the field stays.
    Array.from(document.querySelectorAll('p, span, div, label')).forEach((el) => {
      if (el.children.length) return;
      const txt = (el.textContent || '').trim();
      if (txt.length < 120 && TEST.test(txt)) el.style.visibility = 'hidden';
    });
  });
  await sleep(300);
}

/** Wait until the tab has left the portal for Stripe's hosted onboarding. */
async function waitForStripe(page) {
  await page.waitForFunction(() => /stripe\.com/.test(location.hostname), { timeout: 90000, polling: 500 });
  await sleep(SETTLE_MS + 2500);
}


/** Scroll the agreement to its end so the acknowledgements and the signature pad appear. */
async function scrollAgreementToEnd(page) {
  await page.evaluate(() => {
    const boxes = Array.from(document.querySelectorAll('div, section, article'))
      .filter((el) => el.scrollHeight - el.clientHeight > 200
        && /(auto|scroll)/.test(getComputedStyle(el).overflowY));
    boxes.forEach((b) => { b.scrollTop = b.scrollHeight; });
    window.scrollTo(0, document.body.scrollHeight);
  });
  await sleep(1500);
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await sleep(800);
}

function readManifest() {
  try { return JSON.parse(fs.readFileSync(MANIFEST, 'utf8')); } catch (e) { return {}; }
}

function writeManifest(m) {
  fs.writeFileSync(MANIFEST, JSON.stringify(m, null, 2));
}

// ---------------------------------------------------------------- screens
//
// A "screen" is a name and the steps that reach it from the previous one; the wizard is
// walked once per language, in order, and shot at every step. A screen with a `route`
// starts from a new navigation, so it can be captured on its own with --only.
//
// The agreement exists once the English run has registered, and it can be shown unsigned
// only until somebody signs it. So the order across runs matters:
//   1. every language walks the wizard and shoots the agreement unsigned, ticked and signed;
//   2. one run passes --sign: it presses Accept, lands on Stripe, shoots it, and then the
//      portal's Banking page with onboarding pending;
//   3. every other language signs in as that person and shoots Banking and Stripe again.

function screens(lang) {
  const manifest = readManifest();
  const agreement = () => `/owner-agreement/${readManifest().agreementKey}`;
  const stripeFromBanking = async (p) => {
    // Stripe's hosted page speaks the language the browser asks for; the portal has its own.
    await p.setExtraHTTPHeaders({ 'Accept-Language': lang === 'en' ? 'en-US,en' : `${lang},${lang}-419,en;q=0.5` });
    await ensureSignedIn(p, lang);
    await goTo(p, '/stripe-cards', lang);
    // "Connect Stripe Account" before the first attempt, "Complete Onboarding" after it.
    try { await clickButton(p, lang === 'en' ? 'Complete Onboarding' : 'Completar'); }
    catch (e) { await clickButton(p, lang === 'en' ? 'Connect Stripe Account' : 'Conectar'); }
    try {
      await waitForStripe(p);
    } catch (e) {
      const toast = await p.evaluate(() => document.body.innerText.slice(0, 400));
      throw new Error(`Stripe did not open; page says: ${toast.replace(/\s+/g, ' ')}`);
    }
    await dressStripe(p);
  };
  return [
    { name: 'reg-11-owner-welcome', route: '/create-owner', fullPage: false },
    { name: 'reg-12-owner-info', steps: [(p) => clickButton(p, START[lang]), (p) => fillInfo(p, lang)], fullPage: true },
    { name: 'reg-13-owner-location', steps: [(p) => clickButton(p, NEXT[lang]), fillLocation], fullPage: true },
    { name: 'reg-14-owner-review', steps: [(p) => clickButton(p, NEXT[lang])], fullPage: true },
    {
      // Only the first language submits; the manifest remembers the agreement for the rest.
      name: 'reg-15-agreement',
      fullPage: false,
      skip: manifest.signed,
      steps: [async (p) => {
        const m = readManifest();
        if (m.agreementKey) {
          await goTo(p, agreement(), lang);
          return;
        }
        await clickButton(p, NEXT[lang]);
        await p.waitForFunction(() => /\/owner-agreement\//.test(location.pathname),
          { timeout: 60000, polling: 500 });
        await waitForApp(p);
        await hideSandbox(p);
        await sleep(SETTLE_MS + 1500);
        m.agreementKey = (await p.evaluate(() => location.pathname)).split('/owner-agreement/')[1];
        m.email = emailFor(lang);
        m.base = BASE;
        m.createdAt = new Date().toISOString();
        writeManifest(m);
        console.log(`  registered ${m.email}; agreement ${m.agreementKey}`);
      }],
    },
    { name: 'reg-16-agreement-sign', skip: manifest.signed, steps: [scrollAgreementToEnd], fullPage: false },
    {
      name: 'reg-17-agreement-signed',
      skip: manifest.signed,
      fullPage: false,
      steps: [async (p) => { await goTo(p, agreement(), lang); await tickAndSign(p); }],
    },
    {
      // Stripe's hosted onboarding, where the bank account is entered. Reached by pressing
      // Accept once (--sign), and afterwards from Banking > Complete Onboarding.
      name: 'reg-18-stripe-onboarding',
      fullPage: false,
      steps: [async (p) => {
        const m = readManifest();
        if (SIGN && !m.signed) {
          await goTo(p, agreement(), lang);
          await tickAndSign(p);
          await clickButton(p, ACCEPT[lang]);
          await waitForStripe(p);
          m.signed = true;
          m.signedAt = new Date().toISOString();
          writeManifest(m);
          console.log('  agreement accepted; Stripe onboarding opened');
          return;
        }
        if (!m.signed) throw new Error('agreement not signed yet — run once with --sign');
        await stripeFromBanking(p);
      }],
    },
    {
      name: 'reg-19-banking-pending',
      fullPage: false,
      steps: [async (p) => { await ensureSignedIn(p, lang); await goTo(p, '/stripe-cards', lang); await blurPortal(p); }],
    },
    { name: 'reg-21-partner-welcome', route: '/create-partner', fullPage: false },
    { name: 'reg-22-partner-info', steps: [(p) => clickButton(p, START[lang]), (p) => fillInfo(p, lang)], fullPage: true },
  ];
}

const SIGN = args.includes('--sign');

// ---------------------------------------------------------------- main

async function launch(lang) {
  return puppeteer.launch({
    executablePath: CHROME,
    userDataDir: PROFILE,
    headless: false,
    defaultViewport: VIEWPORT,
    protocolTimeout: 600000,
    args: [
      `--window-size=${VIEWPORT.width},${VIEWPORT.height + 120}`,
      // Stripe's hosted pages speak the browser's language; the portal's is forced separately.
      `--lang=${lang}`,
      '--disable-features=Translate',
      '--no-first-run',
      '--no-default-browser-check',
    ],
  });
}

(async () => {
  if (!CHROME) throw new Error('Chrome not found');
  for (const lang of LANGS) fs.mkdirSync(path.join(SHOTS, lang), { recursive: true });
  fs.mkdirSync(PROFILE, { recursive: true });

  console.log(`Chrome:  ${CHROME}\nBase:    ${BASE}\nLangs:   ${LANGS.join(', ')}\nSign:    ${SIGN}`);

  const failures = [];
  for (const lang of LANGS) {
    const browser = await launch(lang);
    try {
      const page = await browser.newPage();
      await page.setViewport(VIEWPORT);
      page.setDefaultNavigationTimeout(60000);
      page.on('dialog', (d) => d.accept().catch(() => {}));

      for (const s of screens(lang)) {
        if (ONLY.length && !ONLY.some((p) => s.name.includes(p))) continue;
        if (s.skip) { console.log(`[${lang}] ${s.name} — skipped (agreement already signed)`); continue; }
        process.stdout.write(`[${lang}] ${s.name}\n`);
        try {
          if (s.route) await goTo(page, s.route, lang);
          for (const step of s.steps || []) await step(page);
          await hideSandbox(page);
          await sleep(900);
          const buf = await page.screenshot({ fullPage: s.fullPage !== false });
          fs.writeFileSync(path.join(SHOTS, lang, `${s.name}.png`), buf);
        } catch (err) {
          console.log(`  FAILED: ${err.message}`);
          failures.push({ lang, name: s.name, error: err.message });
          // The wizard cannot continue past a failed step; the next screen with a route restarts it.
        }
      }
      await page.close();
    } finally {
      await browser.close();
    }
  }

  const m = readManifest();
  m.failures = failures;
  writeManifest(m);
  console.log(`\nDone. ${failures.length ? `Failures: ${JSON.stringify(failures)}` : 'All captured.'}`);
})().catch((e) => {
  console.error('FATAL', e);
  process.exit(1);
});
