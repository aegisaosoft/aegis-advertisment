# -*- coding: utf-8 -*-
"""Episodes 46-49 — Tesla.

  46  connect your Tesla           — GPS Systems, Connect Tesla, sign in at Tesla, what is asked, cars by VIN
  47  the key and the check        — the panel, Add key to car from a phone in the car, Check cars, the states
  48  a QR sheet for the lot       — Print QR sheet, one card per car still missing the key, the walk
  49  Tesla for Business           — FOR PARTNERS/ADMINS: consent request, the code, Connect fleet

The portal frames (`tes-0N-*`, capture-tesla.js) are the real dev portal with DEMO DATA: no Tesla is
connected to any of our accounts yet, so the GPS tab's API answers were staged in the browser — four
made-up VINs ending 0001xx. Where those frames put each button and row was MEASURED during the capture
(shots/_tesla_boxes.json, per language), so the rings follow a Spanish label that is longer than the
English one. Tesla's own screens are not reproduced: those steps are drawn (`tes-2N-*`,
tesla-diagrams.js), and their boxes are the fixed fractions written in that script.

Facts the narration states, checked against the code: the connect asks only openid/offline_access/
vehicle_device_data/vehicle_location (TeslaOAuth.Scopes) and a grant without vehicle_location is refused;
the plugin never wakes a car (TeslaProvider: only cars Tesla lists as online are read); the telemetry config
is re-pushed every 6 hours (Startup: "Tesla telemetry config - every 6 hours").
"""
import io
import json
import os

from model import B, E

HERE = os.path.dirname(os.path.abspath(__file__))


def _boxes():
    try:
        return json.loads(io.open(os.path.join(HERE, 'shots', '_tesla_boxes.json'), encoding='utf-8').read())
    except (OSError, ValueError):
        return {}


BOXES = _boxes()
PAD = 0.008
LANGS = ('en', 'es')


def _r(lang, shot, key):
    r = BOXES.get('%s/%s' % (lang, shot), {}).get(key)
    if not r:
        raise KeyError('no measured box %s for %s/%s — run capture-tesla.js' % (key, lang, shot))
    return r


def ring(shot, key, pad=PAD):
    """The measured rectangle of `key` on `shot`, padded, per language."""
    out = {}
    for lang in LANGS:
        x, y, w, h = _r(lang, shot, key)
        out[lang] = (round(x - pad, 4), round(y - pad, 4), round(w + 2 * pad, 4), round(h + 2 * pad, 4))
    return out


def span(shot, *keys):
    """One ring around several measured boxes."""
    out = {}
    for lang in LANGS:
        rs = [_r(lang, shot, k) for k in keys]
        x = min(r[0] for r in rs) - PAD
        y = min(r[1] for r in rs) - PAD
        out[lang] = (round(x, 4), round(y, 4),
                     round(max(r[0] + r[2] for r in rs) + PAD - x, 4),
                     round(max(r[1] + r[3] for r in rs) + PAD - y, 4))
    return out


def row(shot, vin_key, panel_key='panel'):
    """A car's whole line in the panel: from its VIN to the panel's right edge, status included."""
    out = {}
    for lang in LANGS:
        x, y, w, h = _r(lang, shot, vin_key)
        px, _, pw, _ = _r(lang, shot, panel_key)
        right = px + pw - 0.012
        left = x - 0.016   # the status icon sits just left of the VIN
        out[lang] = (round(left, 4), round(y - 0.004, 4), round(right - left, 4), round(h + 0.008, 4))
    return out


def at(shot, key):
    """The cursor on the middle of a measured box."""
    return dict((lang, (round(_r(lang, shot, key)[0] + _r(lang, shot, key)[2] / 2, 4),
                        round(_r(lang, shot, key)[1] + _r(lang, shot, key)[3] / 2, 4))) for lang in LANGS)


def look(rings, zoom):
    """The camera on a ring (per language), zoomed no further than lets the whole ring fit."""
    out = {}
    for lang, (x, y, w, h) in rings.items():
        z = max(1.0, min(zoom, 0.9 / w, 0.85 / h))
        out[lang] = (round(x + w / 2, 4), round(y + h / 2, 4), round(z, 3))
    return out


# Drawn frames (tesla-diagrams.js BOX): the same picture geometry in both languages.
FLOW = [(0.042, 0.242, 0.236, 0.256), (0.382, 0.242, 0.236, 0.256), (0.722, 0.242, 0.236, 0.256)]
OVER = [(0.047, 0.242, 0.296, 0.516), (0.352, 0.242, 0.296, 0.516), (0.657, 0.242, 0.296, 0.516)]
NOTE = [(0.052, 0.572, 0.896, 0.082), (0.052, 0.661, 0.896, 0.082), (0.052, 0.75, 0.896, 0.082)]
WIDE = (0.5, 0.5, 1.0)


# =============================================================================== 46
EP46 = E(
    46, 'tesla-connect',
    'Tesla: connect your Tesla account',
    'Tesla: conecte su cuenta de Tesla',
    'Your Teslas report their own route — no tracker to install',
    'Sus Tesla informan su propia ruta, sin instalar ningún rastreador',
    [
        B(en='A Tesla already knows where it drives. Connect your Tesla account, and MyEZToll finds the '
             'tolls on each trip with no tracker to install.',
          es='Un Tesla ya sabe por dónde circula. Conecte su cuenta de Tesla, y MyEZToll encuentra los '
             'peajes de cada viaje sin instalar ningún rastreador.',
          shot='tes-01-gps-add', url='/settings', cam=WIDE,
          label_en='Settings · GPS Systems', label_es='Configuración · GPS Systems'),

        B(en='Open Settings, then the GPS Systems tab, and press Add GPS provider.',
          es='Abra Configuración, luego la pestaña GPS Systems, y pulse Añadir proveedor GPS.',
          cam=look(ring('tes-01-gps-add', 'addBox'), 1.5),
          ring=ring('tes-01-gps-add', 'addBox')),

        B(en='Choose Tesla. There is nothing to type: press Connect Tesla.',
          es='Elija Tesla. No hay nada que escribir: pulse Conectar Tesla.',
          shot='tes-02-add-tesla', cam=look(ring('tes-02-add-tesla', 'addBox'), 1.5),
          point=at('tes-02-add-tesla', 'connect'), click=1.8,
          ring=ring('tes-02-add-tesla', 'connect')),

        B(en='Tesla’s own page opens. Sign in with the Tesla account the cars belong to. MyEZToll never '
             'sees your Tesla password.',
          es='Se abre la página de Tesla. Inicie sesión con la cuenta de Tesla dueña de los coches. MyEZToll '
             'nunca ve su contraseña de Tesla.',
          shot='tes-20-sign-in', url='@tesla.com', cam=WIDE, ring=FLOW[1],
          label_en='On Tesla’s side', label_es='Del lado de Tesla'),

        B(en='Every car in that account is brought in.',
          es='Se traen todos los coches de esa cuenta.',
          cam=look({'en': NOTE[0], 'es': NOTE[0]}, 1.3), ring=NOTE[0]),

        B(en='Tesla shows what MyEZToll asks for. Leave Vehicle Location ticked: tolls come from the route. '
             'Without it, the connection is refused.',
          es='Tesla muestra lo que pide MyEZToll. Deje marcada la ubicación del vehículo: los peajes salen de '
             'la ruta. Sin ella, la conexión se rechaza.',
          shot='tes-21-permissions', cam=WIDE, ring=OVER[1],
          label_en='What is asked', label_es='Lo que se pide'),

        B(en='Nothing else is asked. MyEZToll cannot unlock, start or control the car, and it never wakes a '
             'sleeping one.',
          es='No se pide nada más. MyEZToll no puede abrir, arrancar ni controlar el coche, y nunca despierta '
             'uno dormido.',
          ring=OVER[2]),

        B(en='Approve, and you are back here. Tesla is connected, and your cars arrive by VIN within a minute '
             'or two.',
          es='Apruebe, y vuelve aquí. Tesla queda conectada, y sus coches llegan por VIN en uno o dos minutos.',
          shot='tes-03-connected', url='/settings', cam=look(ring('tes-03-connected', 'teslaCard'), 1.5),
          ring=ring('tes-03-connected', 'teslaCard'),
          label_en='Settings · GPS Systems', label_es='Configuración · GPS Systems'),

        B(en='A car whose VIN is not in MyEZToll yet waits under Review imports.',
          es='Un coche cuyo VIN aún no está en MyEZToll espera en Revisar importaciones.',
          shot='tes-04-review', cam=look(ring('tes-04-review', 'row'), 1.4),
          point=at('tes-04-review', 'review'), ring=ring('tes-04-review', 'row')),

        B(en='Link it to one of your cars, or choose to create it as a new car, and press Write to DB.',
          es='Vincúlelo a uno de sus coches, o elija crearlo como coche nuevo, y pulse Guardar en la BD.',
          cam=look(ring('tes-04-review', 'row'), 1.4),
          point=at('tes-04-review', 'writeDb'), ring=ring('tes-04-review', 'writeDb')),

        B(en='One step is left for each car: the MyEZToll key. That is the next episode.',
          es='Queda un paso para cada coche: la llave de MyEZToll. Ese es el próximo episodio.',
          shot='tes-03-connected', cam=look(ring('tes-03-connected', 'panel'), 1.6),
          ring=ring('tes-03-connected', 'panel')),
    ])


# =============================================================================== 47
EP47 = E(
    47, 'tesla-key',
    'Tesla: add the key and check your cars',
    'Tesla: agregue la llave y revise sus autos',
    'A car streams its route once the MyEZToll key is in it',
    'Un coche transmite su ruta en cuanto tiene la llave de MyEZToll',
    [
        B(en='This panel is your Tesla checklist. A car sends us its route only after the MyEZToll key has '
             'been added to it.',
          es='Este panel es su lista de control de Tesla. Un coche nos envía su ruta solo después de que se '
             'le agregue la llave de MyEZToll.',
          shot='tes-03-connected', url='/settings', cam=look(ring('tes-03-connected', 'panel'), 1.6),
          ring=ring('tes-03-connected', 'panel'),
          label_en='Settings · GPS Systems', label_es='Configuración · GPS Systems'),

        B(en='Add key to car opens the link that adds the key. Open it on your phone.',
          es='Agregar llave al auto abre el enlace que agrega la llave. Ábralo en su teléfono.',
          cam=look(ring('tes-03-connected', 'panel'), 1.6),
          point=at('tes-03-connected', 'addKey'), click=1.4, ring=ring('tes-03-connected', 'addKey')),

        B(en='Use the phone that has the Tesla app for this car’s account.',
          es='Use el teléfono que tiene la app de Tesla de la cuenta de este coche.',
          shot='tes-22-phone-key', url='@tesla.com', cam=WIDE, ring=FLOW[0],
          label_en='On your phone, in the car', label_es='En su teléfono, dentro del coche'),

        B(en='Sit in the car and open the link, or scan the QR code. The Tesla app asks you to approve the '
             'MyEZToll key. Approve it.',
          es='Siéntese en el coche y abra el enlace, o escanee el código QR. La app de Tesla le pide aprobar '
             'la llave de MyEZToll. Apruébela.',
          cam=WIDE, ring=FLOW[1]),

        B(en='Tesla checks that the phone is inside the car, so this is done at the car, once per car.',
          es='Tesla comprueba que el teléfono está dentro del coche, así que se hace junto al coche, una vez '
             'por coche.',
          cam=look({'en': NOTE[0], 'es': NOTE[0]}, 1.3), ring=NOTE[0]),

        B(en='The key only lets the car send its location. It does not let anyone open or drive it.',
          es='La llave solo permite que el coche envíe su ubicación. No permite a nadie abrirlo ni conducirlo.',
          cam=look({'en': NOTE[2], 'es': NOTE[2]}, 1.3), ring=NOTE[2]),

        B(en='Back in MyEZToll, press Check cars.',
          es='De vuelta en MyEZToll, pulse Revisar autos.',
          shot='tes-05-check-mixed', url='/settings', cam=look(ring('tes-05-check-mixed', 'panel'), 1.6),
          point=at('tes-05-check-mixed', 'check'), click=0.9, ring=ring('tes-05-check-mixed', 'check'),
          label_en='Settings · GPS Systems', label_es='Configuración · GPS Systems'),

        B(en='Each car shows its state. Key added, streaming: that car is done.',
          es='Cada coche muestra su estado. Llave agregada, transmitiendo: ese coche está listo.',
          cam=look(ring('tes-05-check-mixed', 'panel'), 1.6), ring=row('tes-05-check-mixed', 'vin1')),

        B(en='Key not added: that car still needs the key.',
          es='Llave no agregada: ese coche aún necesita la llave.',
          cam=look(ring('tes-05-check-mixed', 'panel'), 1.6), ring=row('tes-05-check-mixed', 'vin2')),

        B(en='Not streaming, with a reason, is Tesla’s answer. Here the car’s software is too old: '
             'update it, then check again.',
          es='Sin transmisión, con un motivo, es la respuesta de Tesla. Aquí el software del coche es '
             'demasiado antiguo: actualícelo y vuelva a revisar.',
          cam=look(ring('tes-05-check-mixed', 'panel'), 1.6), ring=row('tes-05-check-mixed', 'vin4')),

        B(en='When every car has the key, the link disappears and the count reads four of four. Tolls now '
             'come from each trip on their own.',
          es='Cuando todos los coches tienen la llave, el enlace desaparece y el contador dice cuatro de cuatro. '
             'Ahora los peajes salen de cada viaje solos.',
          shot='tes-06-check-all', cam=look(ring('tes-06-check-all', 'panel'), 1.6),
          ring=ring('tes-06-check-all', 'panel')),

        B(en='MyEZToll checks again by itself every six hours, so there is nothing else to do.',
          es='MyEZToll vuelve a revisar solo cada seis horas, así que no hay nada más que hacer.',
          cam=look(ring('tes-06-check-all', 'teslaCard'), 1.4)),
    ])


# =============================================================================== 48
EP48 = E(
    48, 'tesla-qr-sheet',
    'Tesla: a QR sheet for the whole lot',
    'Tesla: una hoja QR para toda la flota',
    'Add the key to many cars in one walk',
    'Agregue la llave a muchos coches en un solo recorrido',
    [
        B(en='With many cars, one link is slow. After Check cars, press Print QR sheet.',
          es='Con muchos coches, un solo enlace es lento. Después de Revisar autos, pulse Imprimir hoja QR.',
          shot='tes-05-check-mixed', url='/settings', cam=look(ring('tes-05-check-mixed', 'panel'), 1.6),
          point=at('tes-05-check-mixed', 'print'), click=2.0, ring=ring('tes-05-check-mixed', 'print'),
          label_en='Settings · GPS Systems', label_es='Configuración · GPS Systems'),

        B(en='The sheet lists only the cars that still need the key, one card per car.',
          es='La hoja muestra solo los coches que aún necesitan la llave, una tarjeta por coche.',
          shot='tes-07-qr-sheet', url='', cam=look({'en': (0.03, 0.04, 0.94, 0.42), 'es': (0.03, 0.04, 0.94, 0.42)}, 1.0),
          ring=ring('tes-07-qr-sheet', 'card'),
          label_en='The QR sheet', label_es='La hoja QR'),

        B(en='The last six characters of the VIN are printed large, so you can read them through the windshield.',
          es='Los últimos seis caracteres del VIN salen grandes, para leerlos a través del parabrisas.',
          cam=look(ring('tes-07-qr-sheet', 'card'), 1.8), ring=ring('tes-07-qr-sheet', 'tail')),

        B(en='Sit in that car, scan its code with the phone signed in to the cars’ Tesla account, approve, '
             'and tick the box.',
          es='Siéntese en ese coche, escanee su código con el teléfono de la cuenta de Tesla de los coches, '
             'apruebe y marque la casilla.',
          cam=look(ring('tes-07-qr-sheet', 'card'), 1.8), ring=span('tes-07-qr-sheet', 'qr', 'done')),

        B(en='Cars already streaming, or held back by old software, are left off: a key would not change them.',
          es='Los coches que ya transmiten, o que frena un software antiguo, no aparecen: una llave no los '
             'cambiaría.',
          cam=WIDE),

        B(en='When the walk is done, press Check cars again. Every car you ticked now shows key added.',
          es='Al terminar el recorrido, pulse Revisar autos otra vez. Cada coche que marcó muestra ahora llave '
             'agregada.',
          shot='tes-06-check-all', url='/settings', cam=look(ring('tes-06-check-all', 'panel'), 1.6),
          point=at('tes-06-check-all', 'check'), click=1.6, ring=ring('tes-06-check-all', 'panel'),
          label_en='Settings · GPS Systems', label_es='Configuración · GPS Systems'),
    ])


# =============================================================================== 49
EP49 = E(
    49, 'tesla-business',
    'Tesla for Business: connect a whole fleet',
    'Tesla for Business: conecte toda una flota',
    'One approval from the fleet admin brings in every car',
    'Una sola aprobación del administrador trae todos los coches',
    [
        B(en='A company that keeps its Teslas in a Tesla for Business account can connect them all at once.',
          es='Una empresa que tiene sus Tesla en una cuenta de Tesla for Business puede conectarlos todos a '
             'la vez.',
          shot='tes-23-business', cam=WIDE,
          label_en='Tesla for Business', label_es='Tesla for Business'),

        B(en='Send us the email of the company’s Tesla for Business administrator. We send the consent '
             'request from our side.',
          es='Envíenos el correo del administrador de Tesla for Business de la empresa. Enviamos la solicitud '
             'de consentimiento desde nuestro lado.',
          ring=FLOW[0]),

        B(en='The administrator approves it once, in Tesla for Business.',
          es='El administrador la aprueba una vez, en Tesla for Business.',
          ring=FLOW[1]),

        B(en='Tesla then gives us a code.',
          es='Tesla nos da entonces un código.',
          cam=look({'en': NOTE[1], 'es': NOTE[1]}, 1.3), ring=NOTE[1]),

        B(en='A MyEZToll administrator opens the client’s GPS Systems tab and pastes the code into the '
             'Tesla for Business card.',
          es='Un administrador de MyEZToll abre la pestaña GPS Systems del cliente y pega el código en la '
             'tarjeta Tesla for Business.',
          shot='tes-08-business', url='/settings', cam=look(ring('tes-08-business', 'biz'), 1.6),
          ring=ring('tes-08-business', 'biz'),
          label_en='Settings · GPS Systems (administrator)', label_es='Configuración · GPS Systems (administrador)'),

        B(en='Connect fleet. MyEZToll checks the code with Tesla straight away, so a mistake shows now, not '
             'later.',
          es='Conectar flota. MyEZToll comprueba el código con Tesla en el acto, así que un error se ve ahora, '
             'no después.',
          cam=look(ring('tes-08-business', 'biz'), 1.6),
          point=at('tes-08-business', 'bizConnect'), click=0.8, ring=ring('tes-08-business', 'bizConnect')),

        B(en='Every car of the business arrives, and the Tesla panel works exactly as for a single account.',
          es='Llegan todos los coches de la empresa, y el panel de Tesla funciona igual que con una sola cuenta.',
          shot='tes-09-business-fleet', cam=look(ring('tes-09-business-fleet', 'teslaCard'), 1.4),
          ring=ring('tes-09-business-fleet', 'panel')),

        B(en='Cars that need it still get the key once. The QR sheet from the last episode makes that quick.',
          es='Los coches que lo necesiten reciben la llave una vez. La hoja QR del episodio anterior lo hace '
             'rápido.',
          shot='tes-23-business', cam=look({'en': NOTE[2], 'es': NOTE[2]}, 1.3), ring=NOTE[2]),
    ])
EP49.audience = 'partner'
EP49.privacy = 'public'

# The paragraph under each video on YouTube (youtube.py reads ep.blurb before its own default).
BLURB = {
    'en': ('MyEZToll and Tesla: connect your Tesla account with one sign-in, add the MyEZToll key to '
           'each car, and every car reports its own location, so tolls land on the right booking '
           'with no tracker to install. Tesla for Business brings a whole fleet in at once.'),
    'es': ('MyEZToll y Tesla: conecte su cuenta de Tesla con un solo inicio de sesión, añada la llave '
           'de MyEZToll a cada coche, y cada coche informa su propia ubicación, así los peajes caen en '
           'la reserva correcta sin instalar ningún rastreador. Tesla for Business trae una flota entera '
           'de una vez.'),
}
for _ep in (EP46, EP47, EP48, EP49):
    _ep.blurb = BLURB
