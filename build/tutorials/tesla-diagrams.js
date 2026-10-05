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
 * The drawn frames of the Tesla episodes (46-49).
 *
 * The steps that happen on Tesla's side — signing in at tesla.com, Tesla's approval screen, the
 * Tesla app on a phone in the car, the Tesla for Business consent page — are Tesla's screens.
 * We do not reproduce them (that would be imitating another company's interface), so they are
 * DRAWN, in the same style as the payment diagrams: three boxes and the few things to know.
 * Every box sits at a fixed fraction of the frame (BOX), which series_o.py rings.
 *
 * Output: shots/<lang>/tes-2N-*.png, 1600x1000 at deviceScaleFactor 2.
 *
 *   node tesla-diagrams.js            # en and es
 *   node tesla-diagrams.js --lang=es
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
    brand: 'MyEZToll · Tesla',
    signTitle: 'You sign in at Tesla. MyEZToll never sees your Tesla password.',
    s1: ['MyEZToll', 'Connect Tesla'],
    s2: ['tesla.com', 'sign in with the account that owns the cars'],
    s3: ['MyEZToll', 'your cars arrive by VIN'],
    sa1: 'opens Tesla', sa2: 'you approve',
    signNotes: [
      'Use the Tesla account the cars belong to. Every car in it is brought in.',
      'Tesla shows what MyEZToll asks for. Leave Vehicle Location ticked, or the connection is refused.',
      'You can withdraw the access at any time in your Tesla account.'],

    permTitle: 'What MyEZToll asks Tesla for, and what it does not',
    p1: ['1', 'Vehicle Information', 'Which car is which: VIN, model and year. That is how each Tesla finds its car in MyEZToll.', 'Needed'],
    p2: ['2', 'Vehicle Location', 'Where the car drives. Tolls are matched from the route, so this is the one that matters.', 'Keep it ticked'],
    p3: ['3', 'Nothing else', 'No unlocking, no starting, no climate, no charging. MyEZToll cannot control the car.', 'Read only'],
    permFoot: 'MyEZToll never wakes a sleeping car. Location comes in only while the car is awake and driving.',

    keyTitle: 'Add the MyEZToll key: once per car, from a phone inside it',
    k1: ['Your phone', 'signed in to the Tesla app of the car\u2019s account'],
    k2: ['In the car', 'open the link, or scan the QR code'],
    k3: ['Tesla app', 'approve the MyEZToll key'],
    ka1: 'sit in the car', ka2: 'Tesla asks',
    keyNotes: [
      'Tesla checks that the phone is in the car, so this cannot be done from the office.',
      'Back in MyEZToll, press Check cars. The car shows "key added \u2014 streaming".',
      'The key lets the car send its location to MyEZToll. It does not let anyone open or drive it.'],

    bizTitle: 'Tesla for Business: the whole fleet with one approval',
    b1: ['MyEZToll', 'sends a consent request to your fleet admin'],
    b2: ['Tesla for Business', 'your admin approves it once'],
    b3: ['MyEZToll', 'every car of the business is brought in'],
    ba1: 'email to your admin', ba2: 'a code comes back',
    bizNotes: [
      'Tell us the email of your Tesla for Business admin. We send the request from our side.',
      'After the approval, we paste the code into your account. There is nothing for you to type.',
      'Cars that need it still get the MyEZToll key added once \u2014 the QR sheet makes that quick.'],
  },
  es: {
    brand: 'MyEZToll · Tesla',
    signTitle: 'Usted inicia sesión en Tesla. MyEZToll nunca ve su contraseña de Tesla.',
    s1: ['MyEZToll', 'Conectar Tesla'],
    s2: ['tesla.com', 'inicie sesión con la cuenta dueña de los coches'],
    s3: ['MyEZToll', 'sus coches llegan por VIN'],
    sa1: 'abre Tesla', sa2: 'usted aprueba',
    signNotes: [
      'Use la cuenta de Tesla a la que pertenecen los coches. Se traen todos los coches de esa cuenta.',
      'Tesla muestra lo que pide MyEZToll. Deje marcada la ubicación del vehículo; si no, la conexión se rechaza.',
      'Puede retirar el acceso cuando quiera desde su cuenta de Tesla.'],

    permTitle: 'Lo que MyEZToll pide a Tesla, y lo que no',
    p1: ['1', 'Información del vehículo', 'Qué coche es cuál: VIN, modelo y año. Así cada Tesla encuentra su coche en MyEZToll.', 'Necesario'],
    p2: ['2', 'Ubicación del vehículo', 'Por dónde circula el coche. Los peajes salen de la ruta, así que esta es la que importa.', 'Déjela marcada'],
    p3: ['3', 'Nada más', 'Sin abrir, sin arrancar, sin climatización, sin carga. MyEZToll no puede controlar el coche.', 'Solo lectura'],
    permFoot: 'MyEZToll nunca despierta un coche dormido. La ubicación llega solo mientras el coche está despierto y en marcha.',

    keyTitle: 'Agregue la llave de MyEZToll: una vez por coche, desde un teléfono dentro',
    k1: ['Su teléfono', 'con la app de Tesla de la cuenta del coche'],
    k2: ['En el coche', 'abra el enlace o escanee el código QR'],
    k3: ['App de Tesla', 'apruebe la llave de MyEZToll'],
    ka1: 'siéntese en el coche', ka2: 'Tesla pregunta',
    keyNotes: [
      'Tesla comprueba que el teléfono está en el coche, así que no se puede hacer desde la oficina.',
      'De vuelta en MyEZToll, pulse Revisar autos. El coche muestra «llave agregada — transmitiendo».',
      'La llave permite que el coche envíe su ubicación a MyEZToll. No permite a nadie abrirlo ni conducirlo.'],

    bizTitle: 'Tesla for Business: toda la flota con una sola aprobación',
    b1: ['MyEZToll', 'envía una solicitud de consentimiento a su administrador'],
    b2: ['Tesla for Business', 'su administrador la aprueba una vez'],
    b3: ['MyEZToll', 'se traen todos los coches de la empresa'],
    ba1: 'correo a su administrador', ba2: 'vuelve un código',
    bizNotes: [
      'Díganos el correo de su administrador de Tesla for Business. Enviamos la solicitud desde nuestro lado.',
      'Tras la aprobación, pegamos el código en su cuenta. Usted no tiene que escribir nada.',
      'Los coches que lo necesiten reciben la llave de MyEZToll una vez; la hoja de códigos QR lo hace rápido.'],
  },
};

// ---------------------------------------------------------------- layout
// Fractions of the 1600x1000 frame. series_o.py rings these exact rectangles.
const BOX = {
  over: [[0.055, 0.25, 0.28, 0.50], [0.36, 0.25, 0.28, 0.50], [0.665, 0.25, 0.28, 0.50]],
  flow: [[0.05, 0.25, 0.22, 0.24], [0.39, 0.25, 0.22, 0.24], [0.73, 0.25, 0.22, 0.24]],
};

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;');
const pos = ([x, y, w, h]) => `left:${x * 100}%;top:${y * 100}%;width:${w * 100}%;height:${h * 100}%`;

const CSS = `
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1600px;height:1000px;background:#f5f6fb;font-family:Inter,'Segoe UI',Arial,sans-serif;color:#1f2433}
.frame{position:relative;width:1600px;height:1000px;overflow:hidden}
.brand{position:absolute;left:5.5%;top:5.5%;font-size:18px;letter-spacing:.14em;text-transform:uppercase;color:#5b5fc7;font-weight:700}
h1{position:absolute;left:5.5%;top:10%;right:5.5%;font-size:42px;font-weight:800;line-height:1.15}
.box{position:absolute;background:#fff;border-radius:22px;box-shadow:0 6px 24px rgba(40,44,90,.10);padding:30px 30px}
.num{width:58px;height:58px;border-radius:50%;background:#5b5fc7;color:#fff;font-size:30px;font-weight:800;display:flex;align-items:center;justify-content:center;margin-bottom:22px}
.box h2{font-size:31px;font-weight:800;margin-bottom:16px;line-height:1.15}
.box p{font-size:21px;line-height:1.45;color:#454b5e}
.tag{position:absolute;left:30px;right:30px;bottom:28px;background:#eef0ff;color:#3c40a8;border-radius:12px;padding:13px 16px;font-size:19px;font-weight:700}
.box.hl{border:3px solid #5b5fc7}
.foot{position:absolute;left:5.5%;right:5.5%;top:81%;font-size:22px;color:#4a5068;text-align:center}
.node{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:20px}
.node .icon{font-size:52px;margin-bottom:10px}
.node b{font-size:30px;font-weight:800}
.node span{font-size:19px;color:#5a6075;margin-top:6px;line-height:1.35}
.arrow{position:absolute;height:0;border-top:4px solid #5b5fc7}
.arrow:after{content:'';position:absolute;right:-4px;top:-13px;border-left:20px solid #5b5fc7;border-top:11px solid transparent;border-bottom:11px solid transparent}
.alabel{position:absolute;font-size:18px;font-weight:700;color:#3c40a8;text-align:center;line-height:1.3}
.notes{position:absolute;left:6%;right:6%;top:58%;display:flex;flex-direction:column;gap:18px}
.note{background:#fff;border-radius:16px;padding:20px 26px;font-size:22px;line-height:1.4;box-shadow:0 3px 14px rgba(40,44,90,.07);display:flex;gap:16px;align-items:flex-start}
.note i{font-style:normal;color:#5b5fc7;font-weight:800}
`;

function page(body) {
  return `<!doctype html><html><head><meta charset="utf-8"><style>${CSS}</style></head>` +
    `<body><div class="frame">${body}</div></body></html>`;
}

function node(i, icon, [title, sub], hl) {
  return `<div class="box node${hl ? ' hl' : ''}" style="${pos(BOX.flow[i])}">
    <div class="icon">${icon}</div><b>${esc(title)}</b><span>${esc(sub)}</span></div>`;
}

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

const flow = (title, a, b, c, l1, l2, list, icons, hl) => (t) => page(
  `<div class="brand">${esc(t.brand)}</div><h1>${esc(t[title])}</h1>
   ${node(0, icons[0], t[a], hl === 0)}${node(1, icons[1], t[b], hl === 1)}${node(2, icons[2], t[c], hl === 2)}
   ${arrow(0, 1, 0.37, t[l1])}${arrow(1, 2, 0.37, t[l2])}${notes(t[list])}`);

function permissions(t) {
  const col = (o, i, hl) => `<div class="box${hl ? ' hl' : ''}" style="${pos(BOX.over[i])}">
      <div class="num">${o[0]}</div><h2>${esc(o[1])}</h2><p>${esc(o[2])}</p>
      <div class="tag">${esc(o[3])}</div></div>`;
  return page(`<div class="brand">${esc(t.brand)}</div><h1>${esc(t.permTitle)}</h1>
    ${col(t.p1, 0)}${col(t.p2, 1, true)}${col(t.p3, 2)}
    <div class="foot">${esc(t.permFoot)}</div>`);
}

const DIAGRAMS = [
  ['tes-20-sign-in', flow('signTitle', 's1', 's2', 's3', 'sa1', 'sa2', 'signNotes', ['&#128273;', '&#127760;', '&#128663;'], 1)],
  ['tes-21-permissions', permissions],
  ['tes-22-phone-key', flow('keyTitle', 'k1', 'k2', 'k3', 'ka1', 'ka2', 'keyNotes', ['&#128241;', '&#128664;', '&#9989;'], 1)],
  ['tes-23-business', flow('bizTitle', 'b1', 'b2', 'b3', 'ba1', 'ba2', 'bizNotes', ['&#9993;', '&#127970;', '&#128663;'], 1)],
];

module.exports = { BOX };

if (require.main === module) {
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
}
