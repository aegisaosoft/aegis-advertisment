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
 * Screenshot harness for the HQ Rental Software side of the tutorial series.
 *
 * The HQ episodes (27-30) show two systems: our portal, captured by
 * docs/tools/capture-screenshots.js, and HQ itself — where the owner picks up the two
 * API tokens and where our tolls land as external charges. This file captures the HQ
 * half, into the same shots/<lang>/ folder build.py reads first.
 *
 * It is a separate file rather than a mode of the portal harness because nothing is
 * shared: a different sign-in, a sidebar that is not links, and its own idea of what
 * has to be blurred. What IS the same is the shape — a real Chrome on a persistent
 * profile, the operator signs in once, then every screen is walked and written at
 * 1600x1000 with deviceScaleFactor 2, because the films magnify a screenshot up to 1.5x.
 *
 * HQ renders in English for both languages of the series (the user's call): the Spanish
 * narration names each control in English with the Spanish meaning beside it. So one
 * capture run is copied to every language folder — --lang=en,es by default.
 *
 * Usage:
 *   node capture-hq.js
 *   node capture-hq.js --only=tenant-token,user-token
 *   node capture-hq.js --base=https://myeztoll.staging-1.hqrentalsoftware.com --lang=en,es
 */

const fs = require('fs');
const path = require('path');
const puppeteer = require('C:/aegis-aa/node_modules/puppeteer-core');

// ---------------------------------------------------------------- config

const args = process.argv.slice(2);
const argVal = (name, dflt) => {
  const hit = args.find((a) => a.startsWith(`--${name}=`));
  return hit ? hit.slice(name.length + 3) : dflt;
};
const hasFlag = (name) => args.includes(`--${name}`);

const BASE = argVal('base', 'https://myeztoll.staging-1.hqrentalsoftware.com');
const LANGS = argVal('lang', 'en,es').split(',').map((s) => s.trim()).filter(Boolean);
const ONLY = argVal('only', '').split(',').map((s) => s.trim()).filter(Boolean);
const NO_BLUR = hasFlag('no-blur');
const CDP_PORT = argVal('cdp', '');
const SHOTS = path.join(__dirname, 'shots');

const CHROME = [
  'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
].find((p) => fs.existsSync(p));

// Its own profile: the portal profile holds an owner session for a different product and
// signing into HQ there would make each run fight the other for whatever was left behind.
const PROFILE = argVal('profile', 'C:/Users/Alexander/AppData/Local/Temp/claude/hq-doc-profile');

const VIEWPORT = { width: 1600, height: 1000, deviceScaleFactor: 2 };
const SETTLE_MS = 2600;

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// ---------------------------------------------------------------- redaction
//
// The portal's rules (docs/tools/redaction-rules.js) are built around owner-web's own
// column headers and are no use here. HQ needs four things hidden, and all four have
// shipped legible somewhere in this industry before:
//
//  1. The two API tokens. They are the subject of episode 27 — the viewer has to see
//     WHERE they are, never WHAT they are. A staging token is still a live credential.
//  2. Email addresses and phone numbers, wherever they sit.
//  3. Customer names. HQ writes them into the Reservation cell as "76 - Abbey Kub", so
//     a whole-cell "is this a name" test never fires; the rule strips the number and
//     blurs what is left.
//  4. Colleagues in HQ's own user list — every row but the integration user itself.
//
// Vehicles are NOT hidden: this tenant is a sandbox whose entire fleet is test data, and the
// owner has cleared plates and VINs for publication. Earlier runs blurred them, which is why
// the already-rendered episodes 28-30 still show them blurred.
//
// Everything is marked by class and blurred in CSS, and re-marked on every DOM change,
// because HQ fills its tables after the first paint.

const HQ_BLUR_FN = function (blurClass) {
  const STYLE_ID = '__hq_blur_style';
  if (!document.getElementById(STYLE_ID)) {
    const st = document.createElement('style');
    st.id = STYLE_ID;
    st.textContent = `.${blurClass}{filter:blur(5px)!important;-webkit-filter:blur(5px)!important;}`;
    document.head.appendChild(st);
  }

  const EMAIL = /[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/;
  const PHONE = /(\+?\d[\d\s().-]{7,}\d)/;
  // "76 - Abbey Kub", "8 - Lucio Jast": an HQ reservation cell is an id, a dash and a person.
  const RESERVATION_PERSON = /^\s*\d+\s*-\s*[A-Za-z][\w'’.-]*(\s+[A-Za-z][\w'’.-]*)+\s*$/;
  // Both tokens are long opaque strings; the labels beside them are what the film points at.
  const TOKEN_LABEL = /(tenant api token|user api token|api token)/i;
  // The label-then-value rule below missed the tenant token outright: HQ renders the caption as a
  // plain div, not a <label>, so nothing anchored it and the token shipped legible in the first
  // capture. A token also looks like nothing else on these screens — one long unbroken run of
  // letters and digits — so it is matched on its own shape as well.
  const TOKENISH = /^[A-Za-z0-9_-]{20,}$/;

  const mark = () => {
    const hit = (el) => el.classList.add(blurClass);

    // 1. token values — the text node that follows the labelled control
    document.querySelectorAll('label, .control-label, strong, b, th, dt').forEach((lab) => {
      if (!TOKEN_LABEL.test((lab.textContent || '').trim())) return;
      const holder = lab.closest('.form-group, .col, .field, div') || lab.parentElement;
      if (!holder) return;
      Array.from(holder.querySelectorAll('div, span, p, code, input, textarea'))
        .filter((n) => {
          const t = (n.value !== undefined && n.value !== null && n.value !== '')
            ? String(n.value) : (n.textContent || '');
          return t.trim().length >= 12 && !TOKEN_LABEL.test(t) && n.children.length === 0;
        })
        .forEach(hit);
    });

    // 1b. a token that is a BARE TEXT NODE. HQ writes the user token as loose text inside the
    // same div as its caption and its Generate/Delete links, so no element holds the token
    // alone and every element-level rule steps over it — which is exactly how it came out
    // legible on the modal. Wrapping the text node is the only way to reach it.
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
      acceptNode: (n) => {
        const p = n.parentElement;
        if (!p || p.classList.contains(blurClass)) return NodeFilter.FILTER_REJECT;
        if (/^(SCRIPT|STYLE|TEXTAREA)$/.test(p.tagName)) return NodeFilter.FILTER_REJECT;
        return TOKENISH.test((n.nodeValue || '').trim())
          ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
      },
    });
    const loose = [];
    for (let n = walker.nextNode(); n; n = walker.nextNode()) loose.push(n);
    loose.forEach((n) => {
      const span = document.createElement('span');
      span.className = blurClass;
      span.textContent = n.nodeValue;
      n.parentNode.replaceChild(span, n);
    });

    // 2-4. cell- and node-level identifiers
    const LEAF = 'td, th, span, div, p, a, option, input';
    document.querySelectorAll(LEAF).forEach((el) => {
      if (el.children.length > 1) return;
      if (el.classList.contains(blurClass)) return;
      const raw = (el.tagName === 'INPUT' ? (el.value || '') : (el.textContent || '')).trim();
      if (!raw || raw.length > 120) return;
      // Plates and VINs are deliberately NOT redacted here: the HQ tenant is a sandbox whose
      // whole fleet is test data, and the user has cleared it for publication. People and keys
      // are a different matter and stay hidden.
      if (EMAIL.test(raw) || PHONE.test(raw)
          || RESERVATION_PERSON.test(raw) || TOKENISH.test(raw)) {
        hit(el);
        return;
      }

    });
  };

  mark();

  if (!window.__hqBlurObserver) {
    let queued = false;
    const observer = new MutationObserver(() => {
      if (queued) return;
      queued = true;
      Promise.resolve().then(() => {
        queued = false;
        try { mark(); } catch (e) { /* the next mutation tries again */ }
      });
    });
    observer.observe(document.documentElement, { childList: true, subtree: true });
    window.__hqBlurObserver = observer;
  }
};

// ---------------------------------------------------------------- driver helpers

/**
 * Click whatever reads like `text`. HQ's sidebar and its section headers are not links —
 * they are divs with handlers — so nothing here can be a selector; the element is found
 * by its own text and ranked, exact matches first, so "Settings" does not land on
 * "Settings Order".
 */
async function clickText(page, text, opts) {
  const ok = await page.evaluate((want, minLeft) => {
    const wanted = want.toLowerCase();
    const visible = (el) => el.offsetParent !== null || el.getClientRects().length > 0;
    // The left navigation repeats half the words the content uses — "Integrations" is both a
    // sidebar entry and a collapsed section of the settings form, and taking the first match
    // navigated away instead of opening the section, leaving the run to shoot the page it was
    // already on. Anything left of `minLeft` is the navigation and is not a candidate.
    const nodes = Array.from(document.querySelectorAll(
      'a, button, li, span, div, h1, h2, h3, h4, label, th, td',
    )).filter((el) => visible(el) && el.children.length <= 2
      && el.getBoundingClientRect().left >= minLeft);
    const txt = (el) => (el.innerText || el.textContent || '').trim().toLowerCase();
    // A row's <td> holds the same text as the <a> inside it and comes first in document order,
    // so clicking the cell did nothing and the modal never opened: controls rank above containers.
    const isControl = (el) => el.tagName === 'A' || el.tagName === 'BUTTON';
    const exact = nodes.filter((el) => txt(el) === wanted)
      .sort((a, b) => (isControl(b) ? 1 : 0) - (isControl(a) ? 1 : 0));
    const starts = nodes.filter((el) => txt(el).startsWith(wanted));
    const holds = nodes.filter((el) => txt(el).includes(wanted));
    const pick = exact[0] || starts[0] || holds[0];
    if (!pick) return false;
    pick.scrollIntoView({ block: 'center' });
    pick.click();
    return true;
  }, text, (opts && opts.minLeft) !== undefined ? opts.minLeft : 260);
  if (!ok) throw new Error(`nothing in the content area reads "${text}"`);
  await sleep(1800);
}

/** Wait until a table on the page has rows — HQ paints the frame first and fills it later. */
async function waitForRows(page, min = 1) {
  const deadline = Date.now() + 25000;
  while (Date.now() < deadline) {
    const n = await page.evaluate(() => document.querySelectorAll('table tbody tr').length);
    if (n >= min) { await sleep(900); return; }
    await sleep(600);
  }
}

/** Scroll so that the element reading `text` sits in the upper third of a non-full-page shot. */
async function scrollTo(page, text) {
  await page.evaluate((want) => {
    const wanted = want.toLowerCase();
    const el = Array.from(document.querySelectorAll('label, h1, h2, h3, h4, div, span'))
      .find((n) => (n.innerText || '').trim().toLowerCase() === wanted);
    if (el) el.scrollIntoView({ block: 'center' });
  }, text);
  await sleep(800);
}

/** Scroll the widest horizontally-scrolling box on the page fully to the right. */
async function scrollTableRight(page) {
  await page.evaluate(() => {
    const boxes = Array.from(document.querySelectorAll('div, section, table'))
      .filter((el) => el.scrollWidth - el.clientWidth > 40);
    if (!boxes.length) return;
    boxes.sort((a, b) => (b.scrollWidth - b.clientWidth) - (a.scrollWidth - a.clientWidth));
    boxes[0].scrollLeft = boxes[0].scrollWidth;
  });
  await sleep(900);
}

async function goTo(page, url) {
  await page.goto(url, { waitUntil: 'domcontentloaded' });
  await sleep(SETTLE_MS);
}

// ---------------------------------------------------------------- the screens

const SCREENS = [
  {
    name: 'hq-10-integrations',
    route: '/settings/car-rental/integrations/marketplace',
    fullPage: false,
    steps: [],
  },
  // The Tolls tab of the marketplace is deliberately NOT captured: HQ still lists us there
  // under the retired brand "Huur", linking to huur-us.com. Until HQ renames the card, a frame
  // of that tab would teach viewers a name we no longer use.
  {
    // The tenant token lives in a collapsed section of the general settings page.
    name: 'hq-12-tenant-token',
    route: '/settings',
    fullPage: false,
    steps: [
      // The section header, not the sidebar entry of the same name. The content column starts
      // at x=215 and the navigation ends around x=160, so 200 separates them.
      async (p) => clickText(p, 'Integrations', { minLeft: 200 }),
      async (p) => sleep(1200),
      async (p) => scrollTo(p, 'Tenant API Token'),
    ],
  },
  {
    name: 'hq-13-users',
    route: '/settings/users',
    steps: [async (p) => waitForRows(p)],
  },
  {
    // The user token is on the user itself: Users -> Custom Integration -> User API Token.
    name: 'hq-14-user-token',
    route: '/settings/users',
    fullPage: false,
    steps: [
      async (p) => waitForRows(p),
      async (p) => clickText(p, 'Custom Integration'),
      async (p) => sleep(1500),
    ],
  },
  {
    // Toll Tag is the last column of a table far wider than the window: at 1600 the shot stopped
    // four columns short of it, and that column is what this episode is about.
    name: 'hq-15-vehicles',
    route: '/fleets/vehicles',
    steps: [async (p) => waitForRows(p), async (p) => scrollTableRight(p)],
  },
  {
    name: 'hq-16-external-charges',
    route: '/car-rental/external-charges',
    steps: [async (p) => waitForRows(p)],
  },
  {
    name: 'hq-17-reservations',
    route: '/car-rental/reservations',
    steps: [async (p) => waitForRows(p)],
  },
];

// ---------------------------------------------------------------- main

(async () => {
  if (!CHROME && !CDP_PORT) throw new Error('Chrome not found');
  for (const lang of LANGS) fs.mkdirSync(path.join(SHOTS, lang), { recursive: true });
  fs.mkdirSync(PROFILE, { recursive: true });

  console.log(CDP_PORT ? `Attach:  127.0.0.1:${CDP_PORT}` : `Chrome:  ${CHROME}`);
  if (!CDP_PORT) console.log(`Profile: ${PROFILE}`);
  console.log(`Base:    ${BASE}`);
  console.log(`Out:     ${LANGS.map((l) => path.join(SHOTS, l)).join(', ')}`);
  console.log(`Blur:    ${!NO_BLUR}`);

    // --cdp=<port> attaches to a Chrome the operator is ALREADY signed in to, started with
  // --remote-debugging-port=<port>. That is the cheap path: their HQ session is already
  // there, so nothing has to be typed again, and a tab of our own still gets the 2x
  // viewport the films need. Without it, a dedicated profile is launched and the operator
  // signs in once, which is what every earlier capture run did.
  const browser = CDP_PORT
    ? await puppeteer.connect({
      browserURL: `http://127.0.0.1:${CDP_PORT}`,
      defaultViewport: VIEWPORT,
      protocolTimeout: 600000,
    })
    : await puppeteer.launch({
      executablePath: CHROME,
      userDataDir: PROFILE,
      headless: false,
      defaultViewport: VIEWPORT,
      protocolTimeout: 600000,
      args: [
        `--window-size=${VIEWPORT.width},${VIEWPORT.height + 120}`,
        '--disable-features=Translate',
        '--no-first-run',
        '--no-default-browser-check',
      ],
    });

  // Attached: work in a tab of our own and leave every tab the operator had open alone.
  const page = CDP_PORT
    ? await browser.newPage()
    : ((await browser.pages())[0] || (await browser.newPage()));
  await page.setViewport(VIEWPORT);
  page.setDefaultNavigationTimeout(60000);
  page.on('dialog', (d) => d.accept().catch(() => {}));

  await page.goto(BASE, { waitUntil: 'domcontentloaded' });

  // --- wait for the operator to sign in. Credentials are never typed on their behalf.
  console.log('\n>>> Sign in to HQ inside the opened Chrome window. Waiting up to 15 minutes...');
  const deadline = Date.now() + 15 * 60 * 1000;
  let signedIn = false;
  while (Date.now() < deadline) {
    await sleep(3000);
    try {
      const state = await page.evaluate(() => ({
        url: location.pathname,
        hasPassword: !!document.querySelector('input[type="password"]'),
        // The signed-in shell always carries the left navigation with Car Rental in it.
        hasShell: /car rental/i.test(document.body.innerText || ''),
      }));
      if (state.hasPassword || /login|signin/i.test(state.url) || !state.hasShell) continue;
      signedIn = true;
      break;
    } catch (e) { /* page navigating */ }
  }
  if (!signedIn) throw new Error('No HQ session detected in time');
  console.log('>>> Signed in. Capturing...\n');

  const screens = SCREENS.filter((s) => !ONLY.length || ONLY.some((p) => s.name.includes(p)));
  const failures = [];

  for (const s of screens) {
    process.stdout.write(`[${s.name}] ${s.route}\n`);
    try {
      await goTo(page, `${BASE}${s.route}`);
      for (const step of s.steps || []) await step(page);
      if (!NO_BLUR) await page.evaluate(HQ_BLUR_FN, '__hq_pii');
      await sleep(900);
      const buf = await page.screenshot({ fullPage: s.fullPage !== false });
      for (const lang of LANGS) {
        fs.writeFileSync(path.join(SHOTS, lang, `${s.name}.png`), buf);
      }
    } catch (err) {
      console.log(`  FAILED: ${err.message}`);
      failures.push({ name: s.name, error: err.message });
    }
  }

  fs.writeFileSync(
    path.join(SHOTS, '_hq_manifest.json'),
    JSON.stringify({ base: BASE, langs: LANGS, blurred: !NO_BLUR, failures }, null, 2),
  );

  console.log(`\nDone. ${screens.length - failures.length}/${screens.length} captured.`);
  if (failures.length) console.log('Failures:', failures);
  if (CDP_PORT) {
    // Attached to somebody else's browser: park our tab and let go. Closing the browser here
    // took the operator's signed-in window down with it, and the next run found a dead port.
    await page.goto('about:blank').catch(() => {});
    await browser.disconnect();
  } else {
    await browser.close();
  }
})().catch((e) => {
  console.error('FATAL', e);
  process.exit(1);
});
