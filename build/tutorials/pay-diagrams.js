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
 * The money diagrams for the payment-options episodes (36-38) and the payment-options guide.
 *
 * There is no screen in the portal that shows where the money goes — only the switches that
 * decide it — so these are drawn, not captured. Every box sits at a fixed fraction of the frame
 * (BOX below), which is what the episodes' `cam` and `ring` numbers are written against: move a
 * box here and the rings in series_m.py move with it.
 *
 * Output: shots/<lang>/pay-0N-*.png, 1600x1000 at deviceScaleFactor 2 — the size of every other
 * screen in the series, so the camera treats a diagram exactly like a screenshot.
 *
 *   node pay-diagrams.js            # en and es
 *   node pay-diagrams.js --lang=es
 */

const fs = require('fs');
const path = require('path');
const puppeteer = require('C:/aegis-aa/node_modules/puppeteer-core');

const args = process.argv.slice(2);
const argVal = (name, dflt) => {
  const hit = args.find((a) => a.startsWith(`--${name}=`));
  return hit ? hit.slice(name.length + 3) : dflt;
};
const LANGS = argVal('lang', 'en,es').split(',').map((s) => s.trim()).filter(Boolean);
const OUT = argVal('out', path.join(__dirname, 'shots'));

const CHROME = [
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
].find((p) => fs.existsSync(p));

// ---------------------------------------------------------------- words

const T = {
  en: {
    brand: 'MyEZToll · Partner guide · Payment options',
    overTitle: 'Three ways to pay. Each of your clients picks one.',
    o1: ['1', 'The driver pays us', 'We charge the renter\u2019s card for tolls, fines and, if you want, the rental. The owner gets the money back and a share of our fee.', 'The owner pays nothing'],
    o2: ['2', 'The owner’s booking system collects', 'The owner\u2019s booking software (for example HQ Rental Software) charges the driver through the owner\u2019s payment gateway. We invoice only our share.', 'Weekly invoice for our share'],
    o3: ['3', 'A flat fee per car', 'One fixed price per car per day. We do not charge your drivers anything. One invoice per billing period.', '$5.00 per car per day by default'],
    overFoot: 'Tolls, fines and rentals are set separately. Tell us what each client chose \u2014 we switch it on.',

    d1Title: 'Option 1 \u2014 The driver pays us',
    driver: 'Driver', driverSub: 'card on file',
    us: 'MyEZToll', usSub: 'charges through Stripe',
    you: 'The owner', youSub: 'Banking \u2192 payout to the bank',
    a1: 'toll + fine + our fee', a2: 'the toll back + the owner\u2019s share of the fee',
    d1Notes: ['The toll agency takes the toll from the owner automatically. We win it back from the driver.',
      'A fine is shown to the owner in time to pay it without a late penalty; the driver repays it.',
      'Rentals too, if the owner wants: an agreed commission comes out of the rental payout.'],

    d2Title: 'Option 2 \u2014 The owner\u2019s booking system collects',
    plugin: 'The owner\u2019s booking system', pluginSub: 'e.g. HQ Rental Software',
    gw: 'The owner\u2019s gateway', gwSub: 'the whole amount lands with the owner',
    inv: 'Our invoice', invSub: 'only our share of the fee',
    b1: 'toll + fine + fee', b2: 'charges the driver', b3: 'card or bank, weekly by default',
    d2Alt: 'For bookings from a rental platform the owner can also choose:',
    d2AltA: ['Owner absorbs', 'the owner pays the toll \u2014 nobody is charged, no fee'],
    d2AltB: ['Platform invoice', 'we bill the rental platform, one invoice per trip'],

    d3Title: 'Option 3 \u2014 A flat fee per car',
    cars: 'The owner\u2019s cars', carsSub: 'every car in the account',
    calc: '\u00d7 $5.00 a day', calcSub: 'or the price we agree',
    bill: 'One invoice', billSub: 'every billing period, card or bank',
    d3Notes: ['Per-transaction charging is switched off: we do not charge the owner\u2019s drivers.',
      'A car is counted for every day it is in the account. Remove a car and it stops counting.',
      'The whole fee is ours: no partner share is paid on it.'],
  },
  es: {
    brand: 'MyEZToll · Guía para socios · Formas de pago',
    overTitle: 'Tres formas de pagar. Cada uno de sus clientes elige una.',
    o1: ['1', 'El conductor nos paga', 'Cobramos a la tarjeta del arrendatario los peajes, las multas y, si lo desea, el alquiler. El propietario recupera el dinero y una parte de nuestra tarifa.', 'El propietario no paga nada'],
    o2: ['2', 'Cobra el sistema de reservas del propietario', 'El software de reservas del propietario (por ejemplo HQ Rental Software) cobra al conductor por la pasarela del propietario. Facturamos solo nuestra parte.', 'Factura semanal por nuestra parte'],
    o3: ['3', 'Una tarifa fija por coche', 'Un precio fijo por coche y por día. No cobramos nada a sus conductores. Una factura por periodo.', '$5.00 por coche y día por defecto'],
    overFoot: 'Peajes, multas y alquileres se configuran por separado. Díganos qué eligió cada cliente y lo activamos.',

    d1Title: 'Opción 1 \u2014 El conductor nos paga',
    driver: 'Conductor', driverSub: 'tarjeta registrada',
    us: 'MyEZToll', usSub: 'cobra a través de Stripe',
    you: 'El propietario', youSub: 'Banca \u2192 pago a su banco',
    a1: 'peaje + multa + nuestra tarifa', a2: 'el peaje de vuelta + la parte del propietario',
    d1Notes: ['La agencia cobra el peaje al propietario automáticamente. Nosotros lo recuperamos del conductor.',
      'Mostramos la multa al propietario a tiempo para pagarla sin recargo; el conductor la devuelve.',
      'También alquileres, si el propietario quiere: una comisión acordada se descuenta del pago del alquiler.'],

    d2Title: 'Opción 2 \u2014 Cobra el sistema de reservas del propietario',
    plugin: 'El sistema de reservas', pluginSub: 'p. ej. HQ Rental Software',
    gw: 'La pasarela del propietario', gwSub: 'el importe completo llega al propietario',
    inv: 'Nuestra factura', invSub: 'solo nuestra parte de la tarifa',
    b1: 'peaje + multa + tarifa', b2: 'cobra al conductor', b3: 'tarjeta o banco, semanal por defecto',
    d2Alt: 'Para reservas de una plataforma de alquiler el propietario también puede elegir:',
    d2AltA: ['El propietario asume', 'el propietario paga el peaje — no se cobra a nadie, sin tarifa'],
    d2AltB: ['Factura de plataforma', 'facturamos a la plataforma de alquiler, una factura por viaje'],

    d3Title: 'Opción 3 \u2014 Una tarifa fija por coche',
    cars: 'Los coches del propietario', carsSub: 'cada coche de la cuenta',
    calc: '\u00d7 $5.00 al día', calcSub: 'o el precio que acordemos',
    bill: 'Una factura', billSub: 'cada periodo, con tarjeta o banco',
    d3Notes: ['El cobro por transacción queda apagado: no cobramos a los conductores del propietario.',
      'Un coche cuenta cada día que está en la cuenta. Si se quita, deja de contar.',
      'Esta tarifa es toda nuestra: no se paga parte al socio.'],
  },
};

// ---------------------------------------------------------------- layout
// Fractions of the 1600x1000 frame. series_m.py rings these exact rectangles.
const BOX = {
  over: [[0.055, 0.25, 0.28, 0.50], [0.36, 0.25, 0.28, 0.50], [0.665, 0.25, 0.28, 0.50]],
  flow: [[0.05, 0.25, 0.20, 0.24], [0.40, 0.25, 0.20, 0.24], [0.75, 0.25, 0.20, 0.24]],
};

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;');
const pos = ([x, y, w, h]) => `left:${x * 100}%;top:${y * 100}%;width:${w * 100}%;height:${h * 100}%`;

const CSS = `
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1600px;height:1000px;background:#f5f6fb;font-family:Inter,'Segoe UI',Arial,sans-serif;color:#1f2433}
.frame{position:relative;width:1600px;height:1000px;overflow:hidden}
.brand{position:absolute;left:5.5%;top:5.5%;font-size:18px;letter-spacing:.14em;text-transform:uppercase;color:#5b5fc7;font-weight:700}
h1{position:absolute;left:5.5%;top:10%;right:5.5%;font-size:44px;font-weight:800;line-height:1.15}
.box{position:absolute;background:#fff;border-radius:22px;box-shadow:0 6px 24px rgba(40,44,90,.10);padding:30px 30px}
.num{width:58px;height:58px;border-radius:50%;background:#5b5fc7;color:#fff;font-size:30px;font-weight:800;display:flex;align-items:center;justify-content:center;margin-bottom:22px}
.box h2{font-size:31px;font-weight:800;margin-bottom:16px;line-height:1.15}
.box p{font-size:21px;line-height:1.45;color:#454b5e}
.tag{position:absolute;left:30px;right:30px;bottom:28px;background:#eef0ff;color:#3c40a8;border-radius:12px;padding:13px 16px;font-size:19px;font-weight:700}
.foot{position:absolute;left:5.5%;right:5.5%;top:81%;font-size:22px;color:#4a5068;text-align:center}
.node{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:20px}
.node .icon{font-size:52px;margin-bottom:10px}
.node b{font-size:30px;font-weight:800}
.node span{font-size:19px;color:#5a6075;margin-top:6px}
.node.hl{border:3px solid #5b5fc7}
.arrow{position:absolute;height:0;border-top:4px solid #5b5fc7}
.arrow:after{content:'';position:absolute;right:-4px;top:-13px;border-left:20px solid #5b5fc7;border-top:11px solid transparent;border-bottom:11px solid transparent}
.alabel{position:absolute;font-size:18px;font-weight:700;color:#3c40a8;text-align:center;line-height:1.3}
.notes{position:absolute;left:6%;right:6%;top:58%;display:flex;flex-direction:column;gap:18px}
.note{background:#fff;border-radius:16px;padding:20px 26px;font-size:22px;line-height:1.4;box-shadow:0 3px 14px rgba(40,44,90,.07);display:flex;gap:16px;align-items:flex-start}
.note i{font-style:normal;color:#5b5fc7;font-weight:800}
.alts{position:absolute;left:6%;right:6%;top:60%}
.alts h3{font-size:24px;font-weight:700;color:#4a5068;margin-bottom:16px}
.altrow{display:flex;gap:24px}
.alt{flex:1;background:#fff;border-radius:16px;padding:22px 26px;box-shadow:0 3px 14px rgba(40,44,90,.07)}
.alt b{display:block;font-size:26px;margin-bottom:8px}
.alt span{font-size:20px;color:#50566b;line-height:1.4}
`;

function page(body) {
  return `<!doctype html><html><head><meta charset="utf-8"><style>${CSS}</style></head>` +
    `<body><div class="frame">${body}</div></body></html>`;
}

function overview(t) {
  const col = (o, i) => `<div class="box" style="${pos(BOX.over[i])}">
      <div class="num">${o[0]}</div><h2>${esc(o[1])}</h2><p>${esc(o[2])}</p>
      <div class="tag">${esc(o[3])}</div></div>`;
  return page(`<div class="brand">${esc(t.brand)}</div><h1>${esc(t.overTitle)}</h1>
    ${col(t.o1, 0)}${col(t.o2, 1)}${col(t.o3, 2)}
    <div class="foot">${esc(t.overFoot)}</div>`);
}

function node(i, icon, title, sub, hl) {
  return `<div class="box node${hl ? ' hl' : ''}" style="${pos(BOX.flow[i])}">
    <div class="icon">${icon}</div><b>${esc(title)}</b><span>${esc(sub)}</span></div>`;
}

/** An arrow between two flow boxes, with its words under it (a long label wraps downwards, never across the line). `y` is a fraction of the frame. */
function arrow(from, to, y, label) {
  const x0 = (BOX.flow[from][0] + BOX.flow[from][2]) * 1600 + 12;
  const x1 = BOX.flow[to][0] * 1600 - 20;
  const top = y * 1000;
  return `<div class="arrow" style="left:${x0}px;top:${top}px;width:${x1 - x0}px"></div>
    <div class="alabel" style="left:${x0 - 6}px;top:${top + 16}px;width:${x1 - x0 + 12}px">${esc(label)}</div>`;
}

function notes(list) {
  return `<div class="notes">${list.map((n, i) => `<div class="note"><i>${i + 1}</i><div>${esc(n)}</div></div>`).join('')}</div>`;
}

function driverFlow(t) {
  return page(`<div class="brand">${esc(t.brand)}</div><h1>${esc(t.d1Title)}</h1>
    ${node(0, '&#128663;', t.driver, t.driverSub)}${node(1, '&#128179;', t.us, t.usSub, true)}${node(2, '&#127970;', t.you, t.youSub)}
    ${arrow(0, 1, 0.37, t.a1)}${arrow(1, 2, 0.37, t.a2)}${notes(t.d1Notes)}`);
}

function pluginFlow(t) {
  return page(`<div class="brand">${esc(t.brand)}</div><h1>${esc(t.d2Title)}</h1>
    ${node(0, '&#128421;', t.plugin, t.pluginSub, true)}${node(1, '&#127974;', t.gw, t.gwSub)}${node(2, '&#129534;', t.inv, t.invSub)}
    ${arrow(0, 1, 0.37, t.b2 + ': ' + t.b1)}${arrow(1, 2, 0.37, t.b3)}
    <div class="alts"><h3>${esc(t.d2Alt)}</h3><div class="altrow">
      <div class="alt"><b>${esc(t.d2AltA[0])}</b><span>${esc(t.d2AltA[1])}</span></div>
      <div class="alt"><b>${esc(t.d2AltB[0])}</b><span>${esc(t.d2AltB[1])}</span></div></div></div>`);
}

function plateFlow(t) {
  return page(`<div class="brand">${esc(t.brand)}</div><h1>${esc(t.d3Title)}</h1>
    ${node(0, '&#128665;', t.cars, t.carsSub)}${node(1, '&#128197;', t.calc, t.calcSub, true)}${node(2, '&#129534;', t.bill, t.billSub)}
    ${arrow(0, 1, 0.37, '')}${arrow(1, 2, 0.37, '')}${notes(t.d3Notes)}`);
}

const DIAGRAMS = [
  ['pay-01-overview', overview],
  ['pay-02-driver-pays', driverFlow],
  ['pay-03-plugin-collects', pluginFlow],
  ['pay-04-per-car', plateFlow],
];

(async () => {
  const browser = await puppeteer.launch({ executablePath: CHROME, headless: 'new' });
  const tab = await browser.newPage();
  await tab.setViewport({ width: 1600, height: 1000, deviceScaleFactor: 2 });
  for (const lang of LANGS) {
    fs.mkdirSync(path.join(OUT, lang), { recursive: true });
    for (const [name, draw] of DIAGRAMS) {
      await tab.setContent(draw(T[lang]), { waitUntil: 'load' });
      const file = path.join(OUT, lang, `${name}.png`);
      await tab.screenshot({ path: file });
      console.log(file);
    }
  }
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });
