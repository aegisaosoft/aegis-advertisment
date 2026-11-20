# -*- coding: utf-8 -*-
"""Episode 57 — new on 07.11.2026: a ticket that came by mail.

  57  Violations → Add mailed ticket: a photo or PDF fills the form, check it, Save; the ticket lands on the rental
      that had the car, the agency's website is asked for it, and it is checked again by itself while unpaid

Frames (`nov-NN-*`, capture-nov-features.js) are the real dev portal shown as an owner, with DEMO DATA: made-up cars,
amounts and the ticket itself (`nov-00-ticket`, drawn by the script — a made-up agency, plate and pay site). The two
writes (read the photo, save) are answered in the browser. Rings are fixed fractions read off the frames; the dialog
sits a little higher in Spanish, so those carry {'en', 'es'}.

Facts the narration states, checked against the code (aegis-ao-api 3.0.308-311, owner-web #719/#721):
photo or PDF up to 10 MB, nothing is saved by reading (POST owner-violations/notice/read); the car is chosen by plate,
spaces and hyphens ignored, only when exactly one car matches (matchCarByPlate); the time is the agency's wall clock,
converted with the agency's state (ViolationNoticeEntryService); the ticket goes to the rental that had the car then
(ViolationBookingWindow); the PIN is stored encrypted and the agency's site is asked by number + PIN within 60 s
(ViolationCitationLookupService); a hit updates amount and status; a ticket already on the list is refused as a
duplicate; unpaid entered tickets are re-checked every 6 h, once a day each, up to 180 days
(BackgroundService.ViolationNoticeRecheck); a later scan takes the entered row over instead of adding a second one
(fix 931a4f93, build 311).
"""
from model import B, E


def both(r):
    return {'en': r, 'es': r}


ADD = {'en': (0.776, 0.098, 0.131, 0.048), 'es': (0.798, 0.098, 0.147, 0.048)}
DIALOG = both((0.336, 0.120, 0.328, 0.786))
UPLOAD = {'en': (0.376, 0.222, 0.248, 0.060), 'es': (0.376, 0.214, 0.248, 0.060)}
CAR = {'en': (0.366, 0.316, 0.268, 0.064), 'es': (0.366, 0.308, 0.268, 0.064)}
NUM_PIN = {'en': (0.366, 0.395, 0.268, 0.062), 'es': (0.366, 0.387, 0.268, 0.062)}
DATE_AMT = {'en': (0.366, 0.471, 0.268, 0.062), 'es': (0.366, 0.463, 0.268, 0.062)}
AGENCY = {'en': (0.366, 0.547, 0.268, 0.062), 'es': (0.366, 0.539, 0.268, 0.062)}
HINT = {'en': (0.366, 0.770, 0.268, 0.040), 'es': (0.366, 0.762, 0.268, 0.056)}
SAVE = {'en': (0.550, 0.842, 0.084, 0.044), 'es': (0.536, 0.850, 0.098, 0.044)}
TOASTS = both((0.340, 0.252, 0.322, 0.162))
ROW1 = both((0.205, 0.374, 0.780, 0.046))
INFO = both((0.356, 0.250, 0.288, 0.524))
SOURCE = both((0.370, 0.576, 0.260, 0.060))

TICKET_NUM = both((0.222, 0.318, 0.400, 0.070))
TICKET_WHEN = both((0.222, 0.390, 0.420, 0.064))
TICKET_AMT = both((0.232, 0.664, 0.548, 0.116))


def look(rings, zoom):
    out = {}
    for lang, (x, y, w, h) in rings.items():
        z = max(1.0, min(zoom, 0.9 / w, 0.85 / h))
        out[lang] = (round(x + w / 2, 4), round(y + h / 2, 4), round(z, 3))
    return out


def mid(rings):
    return {lang: (round(x + w / 2, 4), round(y + h / 2, 4)) for lang, (x, y, w, h) in rings.items()}


WIDE = (0.5, 0.5, 1.0)


# =============================================================================== 57
EP57 = E(
    57, 'mailed-ticket',
    'A ticket that came by mail: add it from a photo',
    'Una multa que llegó por correo: añádala con una foto',
    'Take a picture, check the fields, save — the ticket finds its rental by itself',
    'Haga una foto, revise los campos, guarde: la multa encuentra su alquiler sola',
    [
        B(en='Some tickets never show up online. They come in the mail, weeks later, addressed to you as '
             'the owner of the car.',
          es='Algunas multas nunca aparecen en internet. Llegan por correo, semanas después, a su nombre '
             'como dueño del coche.',
          shot='nov-00-ticket', cam=WIDE,
          label_en='A ticket by mail', label_es='Una multa por correo'),

        B(en='Everything we need is printed on it: the notice number, the PIN if there is one, the date and '
             'time, the plate, and the amount.',
          es='Todo lo que hace falta viene impreso: el número de la multa, el PIN si lo hay, la fecha y la '
             'hora, la matrícula y el importe.',
          cam=look(TICKET_NUM, 1.6), ring=TICKET_NUM),

        B(en='Open Tolls and Violations, then Violations, and press Add mailed ticket.',
          es='Abra Peajes e infracciones, luego Infracciones, y pulse Añadir multa recibida.',
          shot='nov-01-violations', url='/violations', cam=look(ADD, 1.5),
          ring=ADD, point=mid(ADD), click=1.6,
          label_en='Add mailed ticket', label_es='Añadir multa recibida'),

        B(en='You can type it all in. Or press the button at the top and give it a photo or a PDF of the '
             'ticket — a phone picture is enough.',
          es='Puede escribirlo todo a mano. O pulse el botón de arriba y dele una foto o un PDF de la '
             'multa: basta con una foto del teléfono.',
          shot='nov-03-notice-empty', cam=look(DIALOG, 1.15),
          ring=UPLOAD, point=mid(UPLOAD), click=2.0),

        B(en='A few seconds later the form is filled in. Nothing is saved yet: this is for you to check.',
          es='Unos segundos después el formulario está lleno. Todavía no se guarda nada: es para que usted '
             'lo revise.',
          shot='nov-04-notice-read', cam=look(DIALOG, 1.15),
          label_en='Check the fields', label_es='Revise los campos'),

        B(en='The car is picked by its plate. If two of your cars could match, or none does, choose it '
             'yourself from the list.',
          es='El coche se elige por la matrícula. Si pueden coincidir dos coches suyos, o ninguno, elíjalo '
             'usted de la lista.',
          cam=look(CAR, 1.5), ring=CAR),

        B(en='The notice number and the PIN. The PIN lets us open the ticket on the agency\'s own website, '
             'so keep it if the ticket has one.',
          es='El número de la multa y el PIN. El PIN nos permite abrir la multa en la web de la propia '
             'agencia, así que déjelo si la multa lo trae.',
          cam=look(NUM_PIN, 1.5), ring=NUM_PIN),

        B(en='The date and time exactly as printed — do not convert anything. We read it in the agency\'s '
             'time zone, and that moment decides which rental the ticket belongs to.',
          es='La fecha y la hora tal como vienen impresas, sin convertir nada. La leemos en la zona horaria '
             'de la agencia, y ese momento decide a qué alquiler pertenece la multa.',
          cam=look(DATE_AMT, 1.5), ring=DATE_AMT),

        B(en='Who issued it and their state. The same rule is written at the bottom of the form.',
          es='Quién la emitió y su estado. La misma regla está escrita al pie del formulario.',
          cam=look(HINT, 1.4), ring=HINT),

        B(en='Everything right? Save ticket.',
          es='¿Todo bien? Guardar multa.',
          cam=look(DIALOG, 1.15), ring=SAVE, point=mid(SAVE), click=1.0,
          label_en='Save ticket', label_es='Guardar multa'),

        B(en='Two things happen. The ticket is attached to the rental that had the car at that moment, '
             'and we ask the agency\'s website for it. If it is there, the amount and the status are '
             'updated from the agency.',
          es='Pasan dos cosas. La multa se une al alquiler que tenía el coche en ese momento, y la buscamos '
             'en la web de la agencia. Si está, el importe y el estado se actualizan desde la agencia.',
          shot='nov-05-notice-saved', cam=look(TOASTS, 1.5), ring=TOASTS),

        B(en='Now it is an ordinary row in the list, charged to the driver like any other violation.',
          es='Ahora es una fila normal de la lista, y se cobra al conductor como cualquier otra multa.',
          shot='nov-07-notice-row', cam=look(ROW1, 1.25), ring=ROW1),

        B(en='Info on the row menu shows the rental it went to and where it came from: a mailed ticket, '
             'entered by hand.',
          es='Información, en el menú de la fila, muestra el alquiler al que fue y de dónde vino: una multa por '
             'correo, introducida a mano.',
          shot='nov-06-notice-info', cam=look(INFO, 1.3), ring=SOURCE),

        B(en='While it stays unpaid, we check it on the agency\'s website again by ourselves, once a day. '
             'And when our own search finds the same ticket later, it updates this row — it never adds a '
             'second one.',
          es='Mientras siga sin pagar, la volvemos a comprobar en la web de la agencia nosotros solos, una '
             'vez al día. Y si nuestra búsqueda encuentra después la misma multa, actualiza esta fila: '
             'nunca añade otra.',
          shot='nov-07-notice-row', cam=WIDE),

        B(en='The same ticket entered twice is refused, so nobody pays it twice.',
          es='La misma multa introducida dos veces se rechaza, para que nadie la pague dos veces.',
          cam=WIDE,
          label_en='Never twice', label_es='Nunca dos veces'),
    ])
