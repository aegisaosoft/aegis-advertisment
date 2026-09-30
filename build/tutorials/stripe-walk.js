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
 * Walk Stripe's hosted Connect onboarding for the registration episode, one screen at a
 * time, from the sandbox owner that capture-register.js created.
 *
 * Stripe's pages are not ours: their fields have no stable names and their order changes
 * with the account's country and type. So this file does not know the flow — it is given
 * the flow as a list of actions, shoots every screen it reaches, and writes what it can see
 * (buttons, labels, inputs) so the next action can be chosen from the previous run's output.
 *
 *   node stripe-walk.js --lang=en --steps=steps.en.json
 *
 * steps.json: [ {"click":"Use test phone number"}, {"click":"Submit"}, {"type":{"label":"Routing number","value":"110000000"}}, ... ]
 * Each entry may also carry "shot":"reg-18b-stripe-code" to keep that screen as an episode
 * frame in shots/<lang>/ (sandbox marks scrubbed); otherwise the frame goes to the scratch dir.
 *
 * The sandbox names itself on Stripe's page ("My E-Z Toll sandbox", "Use test phone number");
 * before a kept frame those are rewritten to what the production page shows, and the test
 * shortcuts are hidden. Nothing else on the page is touched.
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
const LANG = argVal('lang', 'en');
const STEPS = JSON.parse(fs.readFileSync(argVal('steps', 'steps.json'), 'utf8'));
const OUT = argVal('out', path.join(process.env.TEMP || __dirname, 'stripe-walk'));
const SHOTS = path.join(__dirname, 'shots');
const PROFILE = argVal('profile', 'C:/Users/Alexander/AppData/Local/Temp/claude/reg-doc-profile');
const CHROME = [
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
].find((p) => fs.existsSync(p));
const VIEWPORT = { width: 1600, height: 1000, deviceScaleFactor: 2 };
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const PERSON = {
  email: 'yourcompany@mail.myeztoll.com',
  password: sandboxPassword(),
};

async function waitForApp(page) {
  await page.waitForFunction(() => (document.body ? document.body.innerText.trim().length > 40 : false),
    { timeout: 40000, polling: 500 });
}

async function goTo(page, route) {
  await page.goto(`${BASE}${route}`, { waitUntil: 'domcontentloaded' });
  await waitForApp(page);
  const cur = await page.evaluate(() => localStorage.getItem('aegis-language'));
  if (cur !== LANG) {
    await page.evaluate((l) => localStorage.setItem('aegis-language', l), LANG);
    await page.reload({ waitUntil: 'domcontentloaded' });
    await waitForApp(page);
  }
  await sleep(2200);
}

async function clickText(page, text) {
  const ok = await page.evaluate((want) => {
    const w = want.toLowerCase();
    const visible = (el) => el.getClientRects().length > 0;
    // Controls first, and the last of them: a page's own hint text repeats the button's words
    // above it, and the portal's sidebar repeats them left of it.
    const controls = Array.from(document.querySelectorAll('button, a, [role="button"]'))
      .filter((el) => visible(el) && !el.disabled);
    const others = Array.from(document.querySelectorAll('label, span, div'))
      .filter((el) => visible(el) && el.children.length <= 3);
    const txt = (el) => (el.innerText || el.textContent || '').trim().toLowerCase();
    const find = (els) => {
      const exact = els.filter((el) => txt(el) === w);
      const holds = els.filter((el) => txt(el).includes(w) && txt(el).length < w.length + 40);
      return (exact.length ? exact : holds).pop();
    };
    const pick = find(controls) || find(others);
    if (!pick) return false;
    pick.scrollIntoView({ block: 'center' });
    const r = pick.getBoundingClientRect();
    return { x: r.left + r.width / 2, y: r.top + r.height / 2 };
  }, text);
  if (!ok) throw new Error(`nothing reads "${text}"`);
  // A real pointer, not element.click(): Stripe's controls ignore the synthetic event.
  await page.mouse.move(ok.x, ok.y);
  await page.mouse.click(ok.x, ok.y);
  await sleep(2500);
}

/** Type into the input that a label (or placeholder, or aria-label) names. */
async function typeByLabel(page, label, value) {
  const handle = await page.evaluateHandle((want) => {
    const w = want.toLowerCase();
    const inputs = Array.from(document.querySelectorAll('input, select, textarea'))
      .filter((el) => el.getClientRects().length > 0);
    const nameOf = (el) => {
      const bits = [el.getAttribute('aria-label'), el.placeholder, el.name, el.id];
      if (el.id) {
        const lab = document.querySelector(`label[for="${CSS.escape(el.id)}"]`);
        if (lab) bits.push(lab.innerText);
      }
      const lab2 = el.closest('label');
      if (lab2) bits.push(lab2.innerText);
      const by = el.getAttribute('aria-labelledby');
      if (by) by.split(/\s+/).forEach((id) => { const n = document.getElementById(id); if (n) bits.push(n.innerText); });
      return bits.filter(Boolean).join(' | ').toLowerCase();
    };
    return inputs.find((el) => nameOf(el).includes(w)) || null;
  }, label);
  const el = handle.asElement();
  if (!el) throw new Error(`no input labelled "${label}"`);
  const tag = await el.evaluate((e) => e.tagName);
  if (tag === 'SELECT') {
    await el.select(value);
  } else {
    await el.click({ clickCount: 3 });
    await el.type(value, { delay: 20 });
  }
  await sleep(600);
}

/** What is on the screen, for choosing the next action. */
async function describe(page) {
  return page.evaluate(() => {
    const visible = (el) => el.getClientRects().length > 0;
    const t = (el) => (el.innerText || el.textContent || el.value || '').trim().replace(/\s+/g, ' ');
    const buttons = Array.from(document.querySelectorAll('button, a, [role="button"]')).filter(visible).map(t).filter(Boolean);
    const inputs = Array.from(document.querySelectorAll('input, select, textarea')).filter(visible).map((el) => ({
      tag: el.tagName, type: el.type, name: el.name, id: el.id, placeholder: el.placeholder,
      aria: el.getAttribute('aria-label'), value: el.type === 'password' ? '***' : el.value,
    }));
    const labels = Array.from(document.querySelectorAll('label, h1, h2, h3, legend')).filter(visible).map(t).filter(Boolean);
    return { url: location.href, title: document.title, buttons, inputs, labels, text: document.body.innerText.slice(0, 1500) };
  });
}

/** Rewrite the sandbox's own marks on Stripe's page to what production shows. */
async function scrubSandbox(page) {
  await page.evaluate(() => {
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    const nodes = [];
    for (let n = walker.nextNode(); n; n = walker.nextNode()) nodes.push(n);
    nodes.forEach((n) => {
      if (/My E-Z Toll sandbox/i.test(n.nodeValue)) n.nodeValue = n.nodeValue.replace(/My E-Z Toll sandbox/gi, 'My E-Z Toll');
    });
    // The "skip this with a test ..." box and any "use test ..." shortcut.
    Array.from(document.querySelectorAll('div, section, p, button')).forEach((el) => {
      const txt = (el.innerText || '').trim();
      if (el.children.length <= 4 && txt.length < 160 && /(test (phone|code|account|bank)|is not needed for test|for test accounts)/i.test(txt)) {
        el.style.visibility = 'hidden';
      }
    });
  });
  await sleep(300);
}

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  fs.mkdirSync(path.join(SHOTS, LANG), { recursive: true });
  const browser = await puppeteer.launch({
    executablePath: CHROME, userDataDir: PROFILE, headless: false, defaultViewport: VIEWPORT,
    protocolTimeout: 600000,
    args: [`--window-size=${VIEWPORT.width},${VIEWPORT.height + 120}`, `--lang=${LANG}`,
      '--disable-features=Translate', '--no-first-run', '--no-default-browser-check'],
  });
  const log = [];
  try {
    const page = await browser.newPage();
    await page.setViewport(VIEWPORT);
    page.setDefaultNavigationTimeout(60000);

    // Sign in as the sandbox person, if the profile has forgotten the session.
    await goTo(page, '/login');
    if (await page.$('input[type="password"]')) {
      await page.type('input[type="email"]', PERSON.email, { delay: 15 });
      await page.type('input[type="password"]', PERSON.password, { delay: 15 });
      await page.click('button[type="submit"]');
      await page.waitForFunction(() => !/\/login/.test(location.pathname), { timeout: 60000, polling: 500 });
      await waitForApp(page);
    }
    await goTo(page, '/stripe-cards');
    try { await clickText(page, LANG === 'en' ? 'Complete Onboarding' : 'Completar'); }
    catch (e) { await clickText(page, LANG === 'en' ? 'Connect Stripe Account' : 'Conectar'); }
    try {
      await page.waitForFunction(() => /stripe\.com/.test(location.hostname), { timeout: 90000, polling: 500 });
    } catch (e) {
      const seen = await page.evaluate(() => document.body.innerText.slice(0, 600).replace(/\s+/g, ' '));
      throw new Error(`Stripe did not open; page says: ${seen}`);
    }
    await sleep(5000);

    const shoot = async (i, keep) => {
      if (keep) await scrubSandbox(page);
      const buf = await page.screenshot({ fullPage: false });
      const file = keep ? path.join(SHOTS, LANG, `${keep}.png`) : path.join(OUT, `${LANG}-step-${String(i).padStart(2, '0')}.png`);
      fs.writeFileSync(file, buf);
      const d = await describe(page);
      log.push({ step: i, file, ...d });
      console.log(`[${i}] ${d.url}\n     buttons: ${d.buttons.slice(0, 12).join(' | ')}\n     inputs:  ${d.inputs.map((x) => x.aria || x.placeholder || x.name || x.id || x.type).join(' | ')}`);
    };

    await shoot(0, STEPS.length && STEPS[0].shotBefore ? STEPS[0].shotBefore : null);
    for (let i = 0; i < STEPS.length; i++) {
      const s = STEPS[i];
      try {
        if (s.click) await clickText(page, s.click);
        if (s.type) await typeByLabel(page, s.type.label, s.type.value);
        if (s.select) await typeByLabel(page, s.select.label, s.select.value);
        if (s.key) { await page.keyboard.press(s.key); await sleep(1500); }
        if (s.wait) await sleep(s.wait);
      } catch (err) {
        console.log(`  step ${i} FAILED: ${err.message}`);
        await shoot(i + 1, null);
        break;
      }
      await shoot(i + 1, s.shot || null);
    }
  } finally {
    fs.writeFileSync(path.join(OUT, `${LANG}-walk.json`), JSON.stringify(log, null, 2));
    await browser.close();
  }
})().catch((e) => { console.error('FATAL', e); process.exit(1); });
