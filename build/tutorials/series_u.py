# -*- coding: utf-8 -*-
"""Episode 58 — new on 19.11.2026: pass a toll notice or a fine on to the renter.

  58  Violations → row menu → Transfer to renter: the issuer rule, the law, the deadline, where to send it;
      Download package → sign and send it → Mark as sent (the renter's card is no longer charged) → the
      issuer's answer; and the same button after Add mailed ticket saves a ticket onto a rental

Frames (`lt-NN-*`, capture-liability.js) are the real dev portal shown as an owner, with DEMO DATA: a made-up
renter (Riley Morgan), company, plate and amounts. The issuer rule on screen is the real `pa-turnpike-tbp`
plugin's text (aegis-ao-liability, PaTurnpikeLiabilityProvider.cs: 74 Pa.C.S. § 8117(b)(3), 30 days, mail or
fax, owner signs, no notary). The letter (`lt-06-letter`) is drawn after the plugin base's BuildLetter. The
writes are answered in the browser; nothing was saved.

Facts the narration states, checked against the code (owner-web origin/main #800-#805, aegis-ao-api 3.0.358,
aegis-ao-liability Core 1.0.3): the menu item shows only when the row has a bookingId (OwnerViolationsPage);
the best-matching rule is preselected and the select lists the others (TransferLiabilityModal); missing facts
are listed in red before the package can be prepared; the PDF is the letter plus the signed agreement when on
file (LiabilityTransferService); Mark as sent sets ChargeStatus = TransferredToRenter, which the charging loop,
card retries, reminders and collections skip; Issuer refused restores it ("The renter is charged again as
usual"); Cancel transfer is offered while the transfer is only prepared; Add mailed ticket keeps its window
open with Transfer to renter when the ticket landed on a rental, and Add many tickets shows the same link on
each saved row with a rental (AddViolationNoticeModal / BatchViolationNoticeModal, #804). 60 plugins in 30
states are loaded on dev and prod (/api/liability-transfer/providers, 19.11).

Rings are the capture's own measurements (shots/_lt_boxes.json), padded; the Spanish screen differs only where
a longer label moves a button, so those carry {'en', 'es'}.
"""
import io
import json
import os

from model import B, E
import series_u_langs

HERE = os.path.dirname(os.path.abspath(__file__))


def both(r):
    return {'en': r, 'es': r}


def pad(rings, px=0.010, py=0.008):
    out = {}
    for lang, (x, y, w, h) in rings.items():
        nx, ny = max(0.0, x - px), max(0.0, y - py)
        out[lang] = (round(nx, 4), round(ny, 4),
                     round(min(1.0 - nx, w + 2 * px), 4), round(min(1.0 - ny, h + 2 * py), 4))
    return out


def look(rings, zoom):
    out = {}
    for lang, (x, y, w, h) in rings.items():
        z = max(1.0, min(zoom, 0.9 / w, 0.85 / h))
        out[lang] = (round(x + w / 2, 4), round(y + h / 2, 4), round(z, 3))
    return out


def mid(rings):
    return {lang: (round(x + w / 2, 4), round(y + h / 2, 4)) for lang, (x, y, w, h) in rings.items()}


WIDE = (0.5, 0.5, 1.0)

# The pilot languages take every ring from the capture's own measurements (shots/_lt_boxes.json), because
# Persian and Urdu lay the page out right to left. English and Spanish keep the numbers written below.
NEW = tuple(series_u_langs.LANGS)


def _boxes():
    try:
        return json.loads(io.open(os.path.join(HERE, 'shots', '_lt_boxes.json'), encoding='utf-8').read())
    except (IOError, ValueError):
        return {}


BOXES = _boxes()


def _clip(r):
    x, y, w, h = r
    x0, y0 = max(0.0, x), max(0.0, y)
    x1, y1 = min(1.0, x + w), min(1.0, y + h)
    return (round(x0, 4), round(y0, 4), round(x1 - x0, 4), round(y1 - y0, 4))


class _Box(object):
    """One measured frame of one language."""

    def __init__(self, d):
        self.d = d

    def __getitem__(self, key):
        return self.d[key]

    def content(self, key, h=None):
        """The text column of the transfer window, at the height of a measured element."""
        m, r = self.d['modal'], self.d[key]
        return (m[0] + 0.03, r[1], m[2] - 0.065, r[3] if h is None else h)


def more(shot, fn):
    """{lang: rect} for every pilot language whose `shot` was measured; English stands in for the rest."""
    out = {}
    for lang in NEW:
        try:
            out[lang] = _clip(fn(_Box(BOXES['%s/%s' % (lang, shot)])))
        except KeyError:
            pass
    return out


def span(a, b):
    """The rectangle from the top-left of a to the bottom-right of b, whichever side each is on."""
    x0, y0 = min(a[0], b[0]), min(a[1], b[1])
    x1, y1 = max(a[0] + a[2], b[0] + b[2]), max(a[1] + a[3], b[1] + b[3])
    return (x0, y0, x1 - x0, y1 - y0)

# lt-01 / lt-02: the list and the row menu
ROW1 = pad(dict({'en': (0.2031, 0.3595, 0.780, 0.042), 'es': (0.2031, 0.3755, 0.780, 0.042)},
                **more('lt-01-violations', lambda b: b['row1'])), 0.0, 0.004)
MENU_TRANSFER = pad(dict({'en': (0.2188, 0.533, 0.0988, 0.056), 'es': (0.2188, 0.569, 0.0988, 0.056)},
                         **more('lt-02-row-menu', lambda b: b['transfer'])))
# lt-03: the top of the window
RENTER = pad(dict(both((0.32, 0.258, 0.355, 0.017)), **more('lt-03-transfer', lambda b: b.content('renter'))))
ISSUER = pad(dict(both((0.32, 0.293, 0.355, 0.044)), **more('lt-03-transfer', lambda b: b['issuer'])))
LAW = pad(dict(both((0.32, 0.354, 0.355, 0.017)), **more(
    'lt-03-transfer', lambda b: b.content('legal', b['sign'][1] - b['legal'][1] - 0.006))))  # a long label wraps the value
STEPS = pad(dict(both((0.32, 0.385, 0.355, 0.235)), **more(
    'lt-03-transfer', lambda b: b.content('sign', b['where'][1] - b['sign'][1] - 0.005))))
# lt-04: the bottom of the window
WHERE = pad(dict(both((0.32, 0.383, 0.355, 0.270)), **more(
    'lt-04-transfer-bottom', lambda b: b.content('where', b['outcome'][1] - b['where'][1] - 0.006))))
SIGN_DOWNLOAD = pad(dict(both((0.32, 0.735, 0.355, 0.179)), **more(
    'lt-04-transfer-bottom', lambda b: span(b.content('signer'), b['download']))))
DOWNLOAD = dict({'en': (0.5511, 0.876, 0.1239, 0.038), 'es': (0.5513, 0.876, 0.1237, 0.038)},
                **more('lt-04-transfer-bottom', lambda b: b['download']))
# lt-05: what is missing
MISSING = pad(dict(both((0.32, 0.645, 0.355, 0.074)), **more('lt-05-missing', lambda b: b['missing'])))
# lt-07: prepared — the toast, how it went, Mark as sent, Cancel transfer
# Toast boxes are found in the frames by their dark fill (the measured [role=status] is only the text).
TOAST_PREPARED = pad(dict({'en': (0.3531, 0.259, 0.2941, 0.0595), 'es': (0.3638, 0.259, 0.2722, 0.0595)},
                          **more('lt-07-prepared', lambda b: b['toastbox'])), 0.006, 0.006)
SENT_FIELDS = pad({'en': (0.32, 0.735, 0.355, 0.044), 'es': (0.32, 0.691, 0.355, 0.044)})
MARK_SENT = dict({'en': (0.5787, 0.876, 0.0963, 0.038), 'es': (0.5416, 0.878, 0.1334, 0.036)},
                 **more('lt-07-prepared', lambda b: b['markSent']))
SENT_AND_BUTTON = pad(dict({'en': (0.32, 0.735, 0.355, 0.179), 'es': (0.32, 0.691, 0.355, 0.223)}, **more(
    'lt-07-prepared', lambda b: span(b.content('sentBy'), span(b['markSent'], b['cancel'])))))
CANCEL = pad(dict({'en': (0.3623, 0.876, 0.0955, 0.038), 'es': (0.4158, 0.832, 0.1263, 0.038)},
                  **more('lt-07-prepared', lambda b: b['cancel'])))
# lt-08: sent
TOAST_SENT = pad(dict(both((0.3444, 0.259, 0.3109, 0.0785)), **more('lt-08-sent', lambda b: b['toastbox'])), 0.006, 0.006)
# lt-08b: the issuer's answer
ANSWER = pad(dict({'en': (0.4566, 0.876, 0.2184, 0.038), 'es': (0.421, 0.876, 0.254, 0.038)},
                  **more('lt-08b-sent-bottom', lambda b: span(b['refused'], b['accepted']))))
# lt-09: the list after Mark as sent
ROW_T = pad(dict({'en': (0.2031, 0.3595, 0.780, 0.062), 'es': (0.2031, 0.3755, 0.780, 0.062)},
                 **more('lt-09-row-transferred', lambda b: b['row1'])), 0.0, 0.004)
BADGE = pad(dict({'en': (0.8024, 0.393, 0.0845, 0.02), 'es': (0.7826, 0.409, 0.1054, 0.02)},
                 **more('lt-09-row-transferred', lambda b: b['badge'])))
# lt-10: refused
TOAST_REFUSED = pad(dict({'en': (0.3744, 0.259, 0.2509, 0.0595), 'es': (0.3444, 0.259, 0.3109, 0.0785)},
                         **more('lt-10-refused', lambda b: b['toastbox'])), 0.006, 0.006)
# lt-11: a mailed ticket saved onto a rental
SAVED = pad(dict(both((0.34, 0.385, 0.32, 0.254)), **more('lt-11-notice-saved', lambda b: b['modal'])), 0.004, 0.004)
SAVED_TRANSFER = dict({'en': (0.512, 0.587, 0.118, 0.036), 'es': (0.481, 0.587, 0.149, 0.036)},
                      **more('lt-11-notice-saved', lambda b: b['transfer']))
ADD_MANY = pad(dict({'en': (0.2025, 0.156, 0.119, 0.036), 'es': (0.2025, 0.156, 0.132, 0.036)},
                    **more('lt-11-notice-saved', lambda b: b['addMany'])))


# =============================================================================== 58
EP58 = E(
    58, 'transfer-to-renter',
    'Transfer a toll notice or a fine to the renter',
    'Transfiera un aviso de peaje o una multa al arrendatario',
    'The portal writes the letter to the issuer — you sign it, send it, and the renter\'s card is left alone',
    'El portal escribe la carta al emisor: usted la firma, la envía y no se cobra en la tarjeta del arrendatario',
    [
        B(en='In many US states, a toll notice or a fine can be passed on to the renter. You send the issuer a '
             'signed letter with the renter\'s details.',
          es='En muchos estados de EE. UU., un aviso de peaje o una multa se puede pasar al arrendatario. Usted '
             'envía al emisor una carta firmada con los datos del arrendatario.',
          shot='lt-01-violations', url='/violations', cam=WIDE,
          label_en='Transfer to renter', label_es='Transferir al arrendatario'),

        B(en='The portal prepares that letter for you. It knows the rules of about 60 issuers in 30 states.',
          es='El portal le prepara esa carta. Conoce las reglas de unos 60 emisores en 30 estados.',
          say_en='The portal prepares that letter for you. It knows the rules of about sixty issuers in thirty states.',
          say_es='El portal le prepara esa carta. Conoce las reglas de unos sesenta emisores en treinta estados.',
          cam=look(ROW1, 1.2), ring=ROW1),

        B(en='Open Tolls and Violations, then Violations. Open the row menu, or right-click the row, and press '
             'Transfer to renter. It is there only when the notice is on a rental.',
          es='Abra Peajes e infracciones, luego Infracciones. Abra el menú de la fila, o haga clic derecho en '
             'ella, y pulse Transferir al arrendatario. Solo aparece si el aviso está en un alquiler.',
          shot='lt-02-row-menu', cam=dict({'en': (0.35, 0.45, 1.6), 'es': (0.35, 0.47, 1.6)}, **{
              k: (round(r[0] + r[2] / 2, 4), round(max(0.3, r[1] + r[3] / 2 - 0.1), 4), 1.6)
              for k, r in MENU_TRANSFER.items() if k in NEW}),
          ring=MENU_TRANSFER, point=mid(MENU_TRANSFER), click=3.2),

        B(en='At the top: the renter, and whether you have their signed agreement.',
          es='Arriba: el arrendatario, y si tiene su contrato firmado.',
          shot='lt-03-transfer', cam=look(RENTER, 1.6), ring=RENTER,
          label_en='The issuer rule', label_es='La regla del emisor'),

        B(en='Under Issuer rule, the best match is already chosen. You can pick another one from the list.',
          es='En Regla del emisor ya está elegida la que mejor encaja. Puede elegir otra de la lista.',
          cam=look(ISSUER, 1.6), ring=ISSUER),

        B(en='Below it: the law that allows it, and the date to send it by.',
          es='Debajo: la ley que lo permite y la fecha límite para enviarlo.',
          cam=look(LAW, 1.6), ring=LAW),

        B(en='Then the steps for this issuer, and whether you sign it in front of a notary or just sign it.',
          es='Luego los pasos para este emisor, y si se firma ante notario o basta con su firma.',
          cam=look(STEPS, 1.4), ring=STEPS),

        B(en='And where to send it: the mailing address, the fax, or a website.',
          es='Y dónde enviarlo: la dirección postal, el fax o una página web.',
          shot='lt-04-transfer-bottom', cam=look(WHERE, 1.4), ring=WHERE),

        B(en='If something is missing, like the renter\'s address or the signed agreement, it is listed here in '
             'red. Add it first, then come back.',
          es='Si falta algo, como la dirección del arrendatario o el contrato firmado, aparece aquí en rojo. '
             'Añádalo primero y vuelva.',
          shot='lt-05-missing', cam=look(MISSING, 1.5), ring=MISSING,
          label_en='Missing something?', label_es='¿Falta algo?'),

        B(en='Type who signs and their title, then press Download package.',
          es='Escriba quién firma y su cargo, y pulse Descargar paquete.',
          shot='lt-04-transfer-bottom', cam=look(SIGN_DOWNLOAD, 1.5), ring=SIGN_DOWNLOAD,
          point=mid(DOWNLOAD), click=2.6,
          label_en='Download package', label_es='Descargar paquete'),

        B(en='You get a letter as a PDF: your company, the issuer\'s address, the notice, and the law.',
          es='Recibe una carta en PDF: su empresa, la dirección del emisor, el aviso y la ley.',
          shot='lt-06-letter', cam=(0.5, 0.33, 1.45),
          label_en='The letter', label_es='La carta'),

        B(en='Then the renter\'s name and address, and a place for your signature. If the signed rental '
             'agreement is on file, it is added at the end.',
          es='Después, el nombre y la dirección del arrendatario, y el lugar para su firma. Si el contrato '
             'firmado está guardado, se añade al final.',
          cam=(0.5, 0.74, 1.45)),

        B(en='Sign it and send it to the issuer yourself.',
          es='Fírmela y envíela usted mismo al emisor.',
          shot='lt-07-prepared', cam=look(TOAST_PREPARED, 1.4), ring=TOAST_PREPARED,
          label_en='Sign and send', label_es='Firme y envíe'),

        B(en='Changed your mind before sending it? Press Cancel transfer.',
          es='¿Cambió de idea antes de enviarla? Pulse Cancelar transferencia.',
          cam=dict({'en': (0.5, 0.82, 1.5), 'es': (0.5, 0.8, 1.5)}, **{
              k: (0.5, round(min(0.82, r[1] + r[3] / 2 - 0.075), 4), 1.5) for k, r in CANCEL.items() if k in NEW}),
          ring=CANCEL),

        B(en='Once it is sent, choose how you sent it, add the tracking number, and press Mark as sent.',
          es='Cuando la haya enviado, elija cómo la envió, añada el número de seguimiento y pulse Marcar como '
             'enviado.',
          cam=look(SENT_AND_BUTTON, 1.5), ring=SENT_AND_BUTTON, point=mid(MARK_SENT), click=4.0,
          label_en='Mark as sent', label_es='Marcar como enviado'),

        B(en='From now on, the renter\'s card is not charged for this notice. No retries, no reminders, no '
             'collections.',
          es='Desde ahora, este aviso no se cobra en la tarjeta del arrendatario. Ni reintentos, ni '
             'recordatorios, ni agencia de cobros.',
          shot='lt-08-sent', cam=look(TOAST_SENT, 1.4), ring=TOAST_SENT),

        B(en='In the list, the notice now reads Transferred to renter.',
          es='En la lista, el aviso ahora dice Transferido al arrendatario.',
          shot='lt-09-row-transferred', cam=look(BADGE, 1.6), ring=BADGE,
          label_en='Transferred to renter', label_es='Transferido al arrendatario'),

        B(en='When the issuer answers, press Issuer accepted or Issuer refused.',
          es='Cuando el emisor responda, pulse El emisor la aceptó o El emisor la rechazó.',
          shot='lt-08b-sent-bottom', cam=look(ANSWER, 1.5), ring=ANSWER,
          label_en='The issuer\'s answer', label_es='La respuesta del emisor'),

        B(en='If it was refused, the renter is charged again as usual.',
          es='Si la rechazó, se vuelve a cobrar al arrendatario como de costumbre.',
          shot='lt-10-refused', cam=look(TOAST_REFUSED, 1.4), ring=TOAST_REFUSED),

        B(en='One more way in. When Add mailed ticket saves a ticket onto a rental, the window offers Transfer '
             'to renter right away.',
          es='Otra forma de llegar. Cuando Añadir multa recibida guarda una multa en un alquiler, la ventana '
             'ofrece Transferir al arrendatario en ese momento.',
          shot='lt-11-notice-saved', cam=look(SAVED, 1.4), ring=SAVED,
          point=mid(SAVED_TRANSFER), click=4.5,
          label_en='From a mailed ticket', label_es='Desde una multa por correo'),

        B(en='In Add many tickets, each saved row on a rental gets the same link.',
          es='En Añadir varias multas, cada fila guardada en un alquiler tiene el mismo enlace.',
          cam=WIDE, ring=ADD_MANY),
    ])

# The pilot languages (series_u_langs.py).
for _lang, _t in series_u_langs.LANGS.items():
    EP58.translate(_lang, _t['title'], _t['sub'], _t['lines'])
