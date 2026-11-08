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
 * Episodes 55-56: FleetBold and Fleetwire.
 *
 * FleetBold frames (int-01..04): the dev portal, signed in as the empty test owner of
 * _secrets/FleetBold__ReviewerOwner_dev.txt. Every non-GET request is blocked. The connected card is staged:
 * the owner's own GET gps-plugins answer gets one FleetBold account added in the browser, nothing is written.
 * Fleetwire frames (int-20, int-21): drawn, because the path through Fleetwire happens on Fleetwire's site.
 *
 *   node capture-integrations.js
 *   node capture-integrations.js --lang=es
 */
const fs = require('fs');
const os = require('os');
const path = require('path');
const puppeteer = require('C:/aegis-aa/node_modules/puppeteer-core');
const { BLUR_FN, waitForApp, setLanguage, sleep } = require('./capture-common');
const REDACTION = require('C:/aegis-aa/docs/tools/redaction-rules');

const args = process.argv.slice(2);
const LANGS = (args.find((a) => a.startsWith('--lang=')) || '--lang=en,es').slice(7).split(',');
const BASE = 'https://dev-owner.myeztoll.com';
const SHOTS = path.join(__dirname, 'shots');
const VIEWPORT = { width: 1600, height: 1000, deviceScaleFactor: 2 };
const CHROME = ['C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'].find((p) => fs.existsSync(p));
const SECRET = fs.readFileSync('C:/aegis-aa/_secrets/FleetBold__ReviewerOwner_dev.txt', 'utf8');
const EMAIL = /Email: (.+)/.exec(SECRET)[1].trim();
const PASSWORD = /Password: (.+)/.exec(SECRET)[1].trim();
const RENAME = [['FleetBold Review', 'Your Company'], ['FleetBold Reviewer', 'Your Company'], [EMAIL, 'yourcompany@mail.myeztoll.com']];

const T = {
  en: {
    flowA: 'Toll agencies', flowAs: 'and parking and camera violations',
    flowB: 'MyEZToll', flowBs: 'finds each charge and gets it ready',
    flowC: 'Fleetwire', flowCs: 'finds the rental and bills the renter on its invoice',
    sTitle: 'In your Fleetwire account',
    s1: 'Open Connections', s2: 'Open Toll and violation partners', s3: 'Turn on MyEZToll',
    s4: 'Watch for the invitation email from MyEZToll',
  },
  es: {
    flowA: 'Agencias de peaje', flowAs: 'y multas de estacionamiento y de cámara',
    flowB: 'MyEZToll', flowBs: 'encuentra cada cargo y lo prepara',
    flowC: 'Fleetwire', flowCs: 'encuentra el alquiler y lo cobra al arrendatario en su factura',
    sTitle: 'En su cuenta de Fleetwire',
    s1: 'Abra Connections', s2: 'Abra Toll and violation partners', s3: 'Active MyEZToll',
    s4: 'Espere el correo de invitación de MyEZToll',
  },
};

const PAGE = (body) => `<!doctype html><html><head><meta charset="utf-8"><style>
  body{margin:0;width:1600px;height:1000px;background:#f8fafc;font-family:Inter,Segoe UI,Arial,sans-serif;color:#0f172a}
  .row{position:absolute;left:100px;right:100px;top:330px;display:flex;align-items:stretch;gap:0}
  .box{flex:1;background:#fff;border:2px solid #cbd5e1;border-radius:18px;padding:44px 30px;text-align:center}
  .box.mid{border-color:#2563eb;background:#eff6ff}
  .box h2{margin:0 0 16px;font-size:38px}.box p{margin:0;font-size:25px;line-height:1.35;color:#475569}
  .arrow{width:90px;display:flex;align-items:center;justify-content:center;font-size:52px;color:#2563eb}
  .card{position:absolute;left:330px;top:200px;width:940px;background:#fff;border:2px solid #cbd5e1;border-radius:18px;padding:50px 60px;box-sizing:border-box}
  .card h2{margin:0 0 34px;font-size:40px}.st{display:flex;gap:24px;align-items:center;margin:26px 0;font-size:31px}
  .n{width:58px;height:58px;flex:none;border-radius:50%;background:#2563eb;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700}
</style></head><body>${body}</body></html>`;

async function drawings(browser, lang) {
  const t = T[lang];
  const page = await browser.newPage();
  await page.setViewport(VIEWPORT);
  await page.setContent(PAGE(`<div class="row">
    <div class="box"><h2>${t.flowA}</h2><p>${t.flowAs}</p></div><div class="arrow">→</div>
    <div class="box mid"><h2>${t.flowB}</h2><p>${t.flowBs}</p></div><div class="arrow">→</div>
    <div class="box"><h2>${t.flowC}</h2><p>${t.flowCs}</p></div></div>`));
  await page.screenshot({ path: path.join(SHOTS, lang, 'int-20-fw-flow.png') });
  await page.setContent(PAGE(`<div class="card"><h2>${t.sTitle}</h2>
    ${[t.s1, t.s2, t.s3, t.s4].map((s, i) => `<div class="st"><div class="n">${i + 1}</div><div>${s}</div></div>`).join('')}</div>`));
  await page.screenshot({ path: path.join(SHOTS, lang, 'int-21-fw-steps.png') });
  await page.close();
}

const HIDE_SANDBOX = () => {
  // YC_AVATAR: the avatar's initials come from the real test name, the rename above only covers full text.
  [...document.querySelectorAll('div,span')].filter((el) => !el.children.length && (el.textContent || '').trim() === 'FR')
    .forEach((el) => { el.textContent = 'YC'; });
  document.querySelectorAll('.bg-amber-400.text-amber-950, .pin-action-sandbox').forEach((el) => { el.style.display = 'none'; });
  [...document.querySelectorAll('span,div,button')].filter((el) => /^\s*sandbox\s*$/i.test(el.textContent || ''))
    .forEach((el) => { el.style.display = 'none'; });
};

async function shot(page, lang, key) {
  await page.evaluate(BLUR_FN, REDACTION.markerSource(), REDACTION.PII_CLASS, RENAME);
  await page.evaluate(HIDE_SANDBOX);
  await sleep(300);
  await page.screenshot({ path: path.join(SHOTS, lang, `${key}.png`) });
  console.log(`  ${lang}/${key}`);
}

const openGpsTab = (page) => page.evaluate(() => {
  const b = [...document.querySelectorAll('button,[role=tab],a')]
    .find((x) => /GPS/.test(x.innerText || '') && !/Alert/i.test(x.innerText || '') && (x.innerText || '').length < 30 && x.offsetParent);
  if (b) b.click();
  return b ? b.innerText : null;
});

(async () => {
  const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'cap-int-'));
  const browser = await puppeteer.launch({ executablePath: CHROME, userDataDir: profile, headless: 'new',
    defaultViewport: VIEWPORT, protocolTimeout: 300000, args: ['--no-first-run', '--no-default-browser-check'] });
  const page = await browser.newPage();
  let gpsJson = null;
  let stage = false;
  await page.setRequestInterception(true);
  page.on('request', (req) => {
    const u = req.url();
    const login = /signin/i.test(u);
    if (req.method() !== 'GET' && req.method() !== 'OPTIONS' && !login) {
      return req.respond({ status: 200, contentType: 'application/json', body: '{}' });
    }
    if (stage && gpsJson && req.method() === 'GET' && /\/gps-plugins(\?|$)/.test(u)) {
      const body = { ...gpsJson, accounts: [{ id: 'demo-fleetbold', providerId: 'fleetbold', nickname: null, isActive: true,
        isConfigured: true, secretsPresent: {}, lastScrapeAtUtc: new Date().toISOString(), lastScrapeStatus: 'ok', consecutiveFailures: 0 }] };
      return req.respond({ status: 200, contentType: 'application/json', body: JSON.stringify(body) });
    }
    req.continue();
  });
  page.on('response', async (res) => {
    if (!stage && res.request().method() === 'GET' && /\/gps-plugins(\?|$)/.test(res.url()) && res.ok()) {
      try { gpsJson = await res.json(); } catch (e) { /* keep waiting */ }
    }
  });

  await page.goto(`${BASE}/login`, { waitUntil: 'networkidle2' });
  await page.type('input[type=email], input[name=email], input[type=text]', EMAIL);
  await page.type('input[type=password]', PASSWORD);
  await page.keyboard.press('Enter');
  await page.waitForFunction(() => !/\/login/.test(location.pathname), { timeout: 40000 });

  for (const lang of LANGS) {
    fs.mkdirSync(path.join(SHOTS, lang), { recursive: true });
    await drawings(browser, lang);
    stage = false;
    await setLanguage(page, lang);
    await page.goto(`${BASE}/settings`, { waitUntil: 'networkidle2' });
    await waitForApp(page);
    await sleep(2500);
    console.log('  tab:', await openGpsTab(page));
    await sleep(2500);
    await shot(page, lang, 'int-01-gps-tab');
    const added = await page.evaluate(() => {
      const b = [...document.querySelectorAll('main button, button')]
        .find((x) => x.offsetParent && /GPS/.test(x.innerText || '') && /(Add|Agregar|Añadir)/i.test(x.innerText || ''));
      if (b) b.click();
      return b ? b.innerText : null;
    });
    console.log('  add:', added);
    await sleep(800);
    await shot(page, lang, 'int-02-add');
    await page.evaluate(() => {
      const s = [...document.querySelectorAll('select')].find((x) => [...x.options].some((o) => /fleetbold/i.test(o.text + o.value)));
      const o = [...s.options].find((x) => /fleetbold/i.test(x.text + x.value));
      Object.getOwnPropertyDescriptor(HTMLSelectElement.prototype, 'value').set.call(s, o.value);
      s.dispatchEvent(new Event('change', { bubbles: true }));
    });
    await sleep(800);
    await shot(page, lang, 'int-03-connect');

    stage = true;
    await page.goto(`${BASE}/settings?connected=fleetbold`, { waitUntil: 'domcontentloaded' });
    await waitForApp(page);
    await sleep(1500);
    await shot(page, lang, 'int-04-connected');
  }
  await browser.close();
  try { fs.rmSync(profile, { recursive: true, force: true }); } catch (e) { /* a locked temp profile is harmless */ }
})().catch((e) => { console.error(e); process.exit(1); });
