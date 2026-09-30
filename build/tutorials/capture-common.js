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
 * What the admin-session capture scripts (capture-collections.js, capture-payments.js) share:
 * the in-page redaction and chrome-hiding pass, click-by-text, and the waits for the SPA.
 */

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const READY_TIMEOUT_MS = 40000;

const BLUR_FN = function (markerSrc, piiClass, renames) {
  const STYLE_ID = '__doc_blur_style';
  if (!document.getElementById(STYLE_ID)) {
    const st = document.createElement('style');
    st.id = STYLE_ID;
    st.textContent = `.${piiClass}{filter:blur(5px)!important;-webkit-filter:blur(5px)!important;}`;
    document.head.appendChild(st);
  }

  /*
   * The portal's own chrome — the top bar and the black footer — is hidden before the shutter.
   *
   * It is not just tidier. `fullPage` captures the whole document, and on a long settings page the
   * footer is not the last thing in the flow: the collections settings shot came out with the
   * footer lying across the middle of the page and a third of the agencies below it. With the
   * chrome gone the frame is the screen the episode is about, at any page length.
   */
  {
    const chrome = [];
    document.querySelectorAll('header, footer, nav').forEach((el) => chrome.push(el));
    // The footer is a plain <div> in this app; it is the block that carries the legal links.
    document.querySelectorAll('div').forEach((el) => {
      const t = (el.textContent || '').trim();
      if (t.length < 400 && /terms of use|privacy policy|t[ée]rminos de uso/i.test(t)
          && el.querySelectorAll('a, button').length >= 2) {
        chrome.push(el);
      }
    });
    chrome.forEach((el) => { el.style.display = 'none'; });
  }

  // The admin-mode banner ("VIEWING AS OWNER: …") and nothing else: this is an owner's screen.
  // Matching on the text alone hid the whole layout — every ancestor contains that text too, and
  // the first run came out as seven blank pages. The banner is the SMALLEST element that holds
  // the phrase and nothing much else, so it is picked by text length, not by depth.
  {
    const candidates = Array.from(document.querySelectorAll('div, section, aside'))
      .filter((el) => /viewing as owner/i.test(el.textContent || '')
        && (el.textContent || '').trim().length < 140);
    if (candidates.length) {
      candidates.sort((a, b) => (a.textContent || '').length - (b.textContent || '').length);
      candidates[0].style.visibility = 'hidden';
    }
  }

  // Rename the account on screen only — nothing is saved.
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null);
  const texts = [];
  for (let n = walker.nextNode(); n; n = walker.nextNode()) texts.push(n);
  texts.forEach((n) => {
    let v = n.nodeValue;
    renames.forEach(([from, to]) => {
      if (v && v.includes(from)) v = v.split(from).join(to);
    });
    if (v !== n.nodeValue) n.nodeValue = v;
  });

  const mark = new Function('return (' + markerSrc + ')')();
  mark();

  if (!window.__docPiiObserver) {
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
    window.__docPiiObserver = observer;
  }
};

async function clickText(page, text) {
  const ok = await page.evaluate((want) => {
    const wanted = want.trim().toLowerCase();
    const visible = (el) => el.offsetParent !== null || el.getClientRects().length > 0;
    const nodes = Array.from(document.querySelectorAll('button, a, li, span, div, th'))
      .filter((el) => visible(el) && el.children.length <= 2);
    const txt = (el) => (el.innerText || el.textContent || '').trim().toLowerCase();
    // A tab reads "Awaiting approval (2)", so an exact match is tried first and a
    // starts-with second; anything looser picks up the toast that repeats the same words.
    const pick = nodes.find((el) => txt(el) === wanted)
      || nodes.find((el) => txt(el).startsWith(wanted))
      || nodes.find((el) => txt(el).includes(wanted));
    if (!pick) return false;
    pick.scrollIntoView({ block: 'center' });
    pick.click();
    return true;
  }, text);
  if (!ok) throw new Error(`nothing on the page reads "${text}"`);
  await sleep(2000);
}

/** Wait until the app has painted something of its own, not the empty shell. */
async function waitForApp(page) {
  await page.waitForFunction(
    () => {
      const t = document.body ? document.body.innerText.trim() : '';
      return t.length > 40 && !/^\s*$/.test(t);
    },
    { timeout: READY_TIMEOUT_MS, polling: 500 },
  );
}

async function setLanguage(page, lang) {
  await page.evaluate((l) => {
    try { localStorage.setItem('aegis-language', l); } catch (e) { /* ignore */ }
  }, lang);
}

module.exports = { BLUR_FN, clickText, waitForApp, setLanguage, sleep, READY_TIMEOUT_MS };
