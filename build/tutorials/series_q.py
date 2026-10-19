# -*- coding: utf-8 -*-
"""Episodes 52-53 — new on 19.10.2026.

  52  Turo: trips from emails that came earlier — "Re-read Turo emails", the progress strip, one run at a time,
      confirming the new trips; the Turo earnings CSV button on the same page
  53  Refer one booking to collections by hand — the row menu, the preview (debt, agency fee, claim, agency, where
      the driver lives), the owner's confirmation, the case in Collections already approved

The frames (`oct-NN-*`, capture-oct-features.js) are the real dev portal shown as an owner, with DEMO DATA: made-up
drivers, cars and amounts; the two writes are answered in the browser. Rings come from shots/_oct_boxes.json (measured
per language); the referral dialog sits in the middle of the frame in both languages, so its ring is a fixed fraction.

Facts the narration states, checked against the code: the re-read takes the last 30 days (PendingBookingsPage →
rereadEmails(…, 30)), runs in the background (InboundEmailReplayRunner) one run per owner at a time (409 otherwise),
and is idempotent (pending bookings keyed by reservation id). The referral invoices the driver and opens the case
Approved (CollectionsManualReferralService); the claim is grossed up so the owner nets the debt (CollectionsClaim).
"""
import io
import json
import os

from model import B, E

HERE = os.path.dirname(os.path.abspath(__file__))


def _boxes():
    try:
        return json.loads(io.open(os.path.join(HERE, 'shots', '_oct_boxes.json'), encoding='utf-8').read())
    except (OSError, ValueError):
        return {}


BOXES = _boxes()
PAD = 0.008
LANGS = ('en', 'es')


def _r(lang, shot, key):
    r = BOXES.get('%s/%s' % (lang, shot), {}).get(key)
    if not r:
        raise KeyError('no measured box %s for %s/%s — run capture-oct-features.js' % (key, lang, shot))
    return r


def ring(shot, key, pad=PAD):
    out = {}
    for lang in LANGS:
        x, y, w, h = _r(lang, shot, key)
        out[lang] = (round(x - pad, 4), round(y - pad, 4), round(w + 2 * pad, 4), round(h + 2 * pad, 4))
    return out


def at(shot, key):
    out = {}
    for lang in LANGS:
        x, y, w, h = _r(lang, shot, key)
        out[lang] = (round(x + w / 2, 4), round(y + h / 2, 4))
    return out


def look(rings, zoom):
    out = {}
    for lang, (x, y, w, h) in rings.items():
        z = max(1.0, min(zoom, 0.9 / w, 0.85 / h))
        out[lang] = (round(x + w / 2, 4), round(y + h / 2, 4), round(z, 3))
    return out


def both(r):
    return {'en': r, 'es': r}


WIDE = (0.5, 0.5, 1.0)
DIALOG = both((0.332, 0.262, 0.336, 0.476))        # the referral dialog with its preview
DIALOG_DONE = both((0.332, 0.332, 0.336, 0.336))   # the same dialog after referring


# =============================================================================== 52
EP52 = E(
    52, 'turo-reread',
    'Turo: trips from emails that came earlier',
    'Turo: viajes a partir de correos que llegaron antes',
    'Re-read Turo emails, follow its progress, confirm the new trips',
    'Releer correos de Turo, seguir el avance y confirmar los viajes nuevos',
    [
        B(en='Your Turo trips are made from the Turo emails in your My E-Z Toll mailbox. Emails that came before Turo '
             'was switched on did not become trips.',
          es='Sus viajes de Turo se crean con los correos de Turo de su buzón de My E-Z Toll. Los correos que llegaron '
             'antes de activar Turo no se convirtieron en viajes.',
          say_en='Your Turo trips are made from the Turo emails in your My E Z Toll mailbox. Emails that came before '
                 'Turo was switched on did not become trips.',
          say_es='Sus viajes de Turo se crean con los correos de Turo de su buzón de My E Z Toll. Los correos que '
                 'llegaron antes de activar Turo no se convirtieron en viajes.',
          shot='oct-01-turo-idle', url='/p2p-bookings/turo', cam=WIDE,
          label_en='Bookings · Turo', label_es='Reservas · Turo'),

        B(en='Re-read Turo emails turns the emails of the last thirty days into trips.',
          es='Releer correos de Turo convierte en viajes los correos de los últimos treinta días.',
          cam=look(ring('oct-01-turo-idle', 'reread'), 2.0), ring=ring('oct-01-turo-idle', 'reread'),
          point=at('oct-01-turo-idle', 'reread'), click=1.6),

        B(en='A blue strip shows how far it has got. Trips appear here as they are read.',
          es='Una franja azul muestra cuánto lleva. Los viajes aparecen aquí a medida que se leen.',
          shot='oct-02-turo-running', cam=look(ring('oct-02-turo-running', 'strip'), 1.4),
          ring=ring('oct-02-turo-running', 'strip')),

        B(en='While it runs, the button is locked. A new re-read can start when this one ends.',
          es='Mientras dura, el botón queda bloqueado. Se puede iniciar otra relectura cuando termine esta.',
          cam=look(ring('oct-02-turo-running', 'reread'), 2.0), ring=ring('oct-02-turo-running', 'reread')),

        B(en='Each new trip waits here. Confirm it, choose the car, and tick Remember this Turo listing, so the next '
             'trips of that car find it by themselves.',
          es='Cada viaje nuevo espera aquí. Confírmelo, elija el coche y marque Recordar este anuncio de Turo, para '
             'que los próximos viajes de ese coche lo encuentren solos.',
          shot='oct-03-turo-done', cam=look(ring('oct-03-turo-done', 'table'), 1.3),
          ring=ring('oct-03-turo-done', 'table')),

        B(en='Nothing is ever doubled. Pressing it again only updates trips that are already here.',
          es='Nada se duplica nunca. Pulsarlo otra vez solo actualiza los viajes que ya están aquí.',
          cam=look(ring('oct-03-turo-done', 'reread'), 2.0), ring=ring('oct-03-turo-done', 'reread')),

        B(en='Next to it, Turo earnings CSV links your listings to your cars from the Earnings file you download on '
             'turo.com.',
          es='A su lado, CSV de ganancias de Turo vincula sus anuncios con sus coches a partir del archivo Earnings '
             'que descarga en turo.com.',
          say_en='Next to it, Turo earnings C S V links your listings to your cars from the Earnings file you '
                 'download on turo dot com.',
          say_es='A su lado, C S V de ganancias de Turo vincula sus anuncios con sus coches a partir del archivo '
                 'Earnings que descarga en turo punto com.',
          shot='oct-01-turo-idle', cam=look(ring('oct-01-turo-idle', 'csv'), 2.0), ring=ring('oct-01-turo-idle', 'csv')),
    ])


# =============================================================================== 53
EP53 = E(
    53, 'refer-to-collections',
    'Send one booking to a collections agency',
    'Enviar una reserva a una agencia de cobranza',
    'From the booking: see the claim, confirm, and the case is ready',
    'Desde la reserva: vea el reclamo, confirme y el caso queda listo',
    [
        B(en='The driver’s card failed and the tolls on this booking are still unpaid. You can send it to a '
             'collections agency yourself.',
          es='La tarjeta del conductor falló y los peajes de esta reserva siguen sin pagar. Puede enviarla usted mismo '
             'a una agencia de cobranza.',
          shot='oct-11-bookings-menu', url='/bookings', cam=look(ring('oct-11-bookings-menu', 'row1'), 1.3),
          ring=ring('oct-11-bookings-menu', 'row1'),
          label_en='Bookings', label_es='Reservas'),

        B(en='Right-click the booking and choose Refer to collections.',
          es='Haga clic derecho en la reserva y elija Enviar a cobranza.',
          cam=look(ring('oct-11-bookings-menu', 'refer'), 2.0), ring=ring('oct-11-bookings-menu', 'refer'),
          point=at('oct-11-bookings-menu', 'refer'), click=1.4),

        B(en='Before anything happens, you see the debt, the agency fee, what the driver will be asked for, the '
             'agency, and where the driver lives.',
          es='Antes de que pase nada, ve la deuda, la comisión de la agencia, lo que se le pedirá al conductor, la '
             'agencia y dónde vive el conductor.',
          shot='oct-12-refer-preview', cam=look(DIALOG, 1.6), ring=DIALOG),

        B(en='You get the whole debt. The agency’s fee is added on top of what the driver pays.',
          es='Usted recibe la deuda completa. La comisión de la agencia se suma a lo que paga el conductor.',
          cam=look(DIALOG, 1.6)),

        B(en='Tick that you asked the driver to pay and they have not, then press Refer to collections.',
          es='Marque que le pidió el pago al conductor y que no pagó, y pulse Enviar a cobranza.',
          shot='oct-13-refer-confirmed', cam=look(DIALOG, 1.6), ring=ring('oct-13-refer-confirmed', 'checkbox', pad=0.012),
          point=at('oct-13-refer-confirmed', 'submit'), click=2.6),

        B(en='The driver gets an invoice for the debt, and the case is in Collections, already approved.',
          es='El conductor recibe una factura por la deuda, y el caso está en Cobranza, ya aprobado.',
          shot='oct-14-refer-done', cam=look(DIALOG_DONE, 1.6), ring=DIALOG_DONE),

        B(en='Here it is, under Approved. From now on it goes on like any other case.',
          es='Aquí está, en Aprobados. A partir de ahora sigue como cualquier otro caso.',
          shot='oct-15-collections-approved', url='/payments/collections',
          cam=look(ring('oct-15-collections-approved', 'row1'), 1.4), ring=ring('oct-15-collections-approved', 'row1'),
          label_en='Payments · Collections', label_es='Pagos · Cobranza'),

        B(en='For a Turo trip, ask Turo first: a reimbursement through Turo costs nothing and pays you in full.',
          es='Para un viaje de Turo, pida primero a Turo: un reembolso a través de Turo no cuesta nada y le paga el '
             'total.',
          cam=WIDE),
    ])
