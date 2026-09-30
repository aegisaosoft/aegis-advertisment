# -*- coding: utf-8 -*-
"""Episodes 41-45 — the Partner API, with examples. FOR PARTNERS (E.audience = 'partner').

  41  your key and the first call      — the reference, X-Api-Key, integrations, the envelope, paging
  42  cars, drivers and bookings       — your own ids, transponders, card check, card link
  43  tolls and fines                  — the money fields, renterCharge, reading every page
  44  GPS and webhooks                 — positions, mileage, webhooks and the signature check
  45  your charges and disputes        — POST /charges, POST /disputes, the evidence package

Every request and response on screen is the API's own catalog example (api-cards.js renders them from
api/catalog.prod.json); the two snippets we wrote — the paging loop and the webhook check — follow the
code: the signature is HMAC-SHA256(secret as UTF-8, "t.body") in lower-case hex
(PartnerWebhookService.Sign), with X-MyEzToll-Event and X-MyEzToll-Event-Id beside it. Key prefixes:
aegispk- owner key (PartnerApiKeysController), aegispi- integration token (PartnerIntegration).

The code frames are the same picture in both languages (code is code), so one set of boxes from
shots/_api_boxes.json serves both. The narration names fields as they are spelled, because a
developer will type them.
"""
import io
import json
import os

from model import B, E

HERE = os.path.dirname(os.path.abspath(__file__))


def _boxes():
    try:
        return json.loads(io.open(os.path.join(HERE, 'shots', '_api_boxes.json'), encoding='utf-8').read())
    except (OSError, ValueError):
        return {}


BOXES = _boxes()
PAD = 0.006


def box(frame, part, key=None):
    """A ring around the request box, the response box, or one highlighted line of a code frame."""
    b = BOXES.get(frame, {})
    r = (b.get('hl', {}) if key else b).get(key or part) or [0.05, 0.1, 0.9, 0.8]
    return (round(r[0] - PAD, 4), round(r[1] - PAD, 4), round(r[2] + 2 * PAD, 4), round(r[3] + 2 * PAD, 4))


def line(frame, key):
    return box(frame, None, key)


def join(*rects):
    x = min(r[0] for r in rects)
    y = min(r[1] for r in rects)
    return (x, y, max(r[0] + r[2] for r in rects) - x, max(r[1] + r[3] for r in rects) - y)


def look(r, zoom):
    """The camera on a ring, zoomed no further than lets the whole ring fit."""
    z = max(1.0, min(zoom, 0.9 / r[2], 0.85 / r[3]))
    return (round(r[0] + r[2] / 2, 4), round(r[1] + r[3] / 2, 4), round(z, 3))


# The paragraph under each video on YouTube (youtube.py reads ep.blurb before its own default).
BLURB = {
    'en': ('The MyEZToll Partner API, with examples: your key, cars, drivers and bookings with your '
           'own ids, tolls and fines, GPS, webhooks, and disputes on your own Stripe account. '
           'Reference: owner.myeztoll.com/api/partner/v1/index'),
    'es': ('La API para socios de MyEZToll, con ejemplos: su clave, coches, conductores y reservas '
           'con sus propios id, peajes y multas, GPS, webhooks, y disputas en su propia cuenta de '
           'Stripe. Referencia: owner.myeztoll.com/api/partner/v1/index'),
}


def partner(*eps):
    for ep in eps:
        ep.audience = 'partner'
        ep.blurb = BLURB
        ep.privacy = 'public'       # user 2026-09-30: the API videos are public (still off /tutorials)
    return eps


SW_TAGS = line('api-00-swagger', 'tags')
SW_AUTH = line('api-00-swagger', 'authorize')


# =============================================================================== 41
EP41 = E(
    41, 'api-first-call',
    'Partner API 1: your key and the first call',
    'API para socios 1: su clave y la primera llamada',
    'Where the reference is, how a call is signed in, and the shape of every answer',
    'Dónde está la referencia, cómo se autentica una llamada y la forma de cada respuesta',
    [
        B(en='The Partner API lets your own software work with our data: cars, drivers, bookings, '
             'tolls, fines and GPS.',
          es='La API para socios permite que su propio software trabaje con nuestros datos: coches, '
             'conductores, reservas, peajes, multas y GPS.',
          shot='api-00-swagger', url='/api/partner/v1/index', cam=(0.5, 0.5, 1.0),
          label_en='The reference', label_es='La referencia'),

        B(en='The full reference is public, at owner.myeztoll.com/api/partner/v1/index. Every '
             'function is listed there.',
          es='La referencia completa es pública, en owner.myeztoll.com/api/partner/v1/index. Cada '
             'función aparece ahí.',
          say_en='The full reference is public, at owner dot my e z toll dot com, slash api, slash '
                 'partner, slash v1, slash index. Every function is listed there.',
          say_es='La referencia completa es pública, en owner punto my e z toll punto com, barra '
                 'api, barra partner, barra v1, barra index. Cada función aparece ahí.',
          cam=look(SW_TAGS, 1.3), ring=SW_TAGS),

        B(en='Authorize takes your key. Then Try it out calls the API for real, straight from the '
             'page.',
          es='Authorize recibe su clave. Después, Try it out llama a la API de verdad, desde la '
             'propia página.',
          cam=look(SW_AUTH, 1.8), ring=SW_AUTH, point=(SW_AUTH[0] + SW_AUTH[2] / 2,
                                                         SW_AUTH[1] + SW_AUTH[3] / 2), click=1.4),

        B(en='Every call carries your key in the X-Api-Key header. An owner key acts for one owner.',
          es='Cada llamada lleva su clave en la cabecera X-Api-Key. Una clave de propietario actúa '
             'para un propietario.',
          shot='api-00b-keys', url='', cam=look(line('api-00b-keys', 'owner'), 1.5),
          ring=line('api-00b-keys', 'owner'),
          label_en='Your key', label_es='Su clave'),

        B(en='A platform serving many owners gets one integration token instead, and names the owner '
             'of each call in X-Owner-Id.',
          es='Una plataforma que atiende a muchos propietarios recibe un solo token de integración, y '
             'nombra al propietario de cada llamada en X-Owner-Id.',
          cam=look(join(line('api-00b-keys', 'integ'), line('api-00b-keys', 'ownerid')), 1.4),
          ring=join(line('api-00b-keys', 'integ'), line('api-00b-keys', 'ownerid'))),

        B(en='An owner connects your integration from their own portal. Only owners who did will '
             'answer.',
          es='Un propietario conecta su integración desde su propio portal. Solo responden los que lo '
             'han hecho.',
          cam=look(line('api-00b-keys', 'ownerid'), 1.4)),

        B(en='Keys come from us. Test first on the sandbox, dev-owner.myeztoll.com, with a key of its '
             'own.',
          es='Las claves se las damos nosotros. Pruebe primero en la zona de pruebas, '
             'dev-owner.myeztoll.com, con su propia clave.',
          say_en='Keys come from us. Test first on the sandbox, dev owner dot my e z toll dot com, '
                 'with a key of its own.',
          say_es='Las claves se las damos nosotros. Pruebe primero en la zona de pruebas, dev owner '
                 'punto my e z toll punto com, con su propia clave.',
          cam=look(line('api-00b-keys', 'sandbox'), 1.5), ring=line('api-00b-keys', 'sandbox')),

        B(en='The first call can be the catalog itself: every function, with an example call and '
             'answer.',
          es='La primera llamada puede ser el propio catálogo: cada función, con una llamada y una '
             'respuesta de ejemplo.',
          shot='api-01-catalog', cam=look(box('api-01-catalog', 'req'), 1.3),
          ring=box('api-01-catalog', 'req'),
          label_en='GET /', label_es='GET /'),

        B(en='Every answer has the same envelope: success, data and error. When success is false, '
             'error says why.',
          es='Cada respuesta tiene el mismo sobre: success, data y error. Cuando success es false, '
             'error dice por qué.',
          cam=look(box('api-01-catalog', 'res'), 1.2),
          ring=join(line('api-01-catalog', 'success'), line('api-01-catalog', 'error'))),

        B(en='baseUrl is the address every other call starts with.',
          es='baseUrl es la dirección con la que empiezan todas las demás llamadas.',
          cam=look(line('api-01-catalog', 'base'), 1.5), ring=line('api-01-catalog', 'base')),

        B(en='GET /me tells you what your key is: an owner key or an integration.',
          es='GET /me le dice qué es su clave: una clave de propietario o una integración.',
          shot='api-02-me', cam=look(box('api-02-me', 'res'), 1.4), ring=line('api-02-me', 'kind'),
          label_en='GET /me', label_es='GET /me'),

        B(en='An integration lists the owners it may act for with GET /owners.',
          es='Una integración lista los propietarios para los que puede actuar con GET /owners.',
          shot='api-03-owners', cam=look(box('api-03-owners', 'res'), 1.3),
          ring=line('api-03-owners', 'owner'),
          label_en='GET /owners', label_es='GET /owners'),

        B(en='Every list comes in pages. Keep asking while hasMore is true. And dates are UTC: a '
             'range includes from and excludes to.',
          es='Cada lista llega por páginas. Siga pidiendo mientras hasMore sea true. Y las fechas '
             'son UTC: un rango incluye from y excluye to.',
          cam=look(box('api-03-owners', 'res'), 1.3), ring=line('api-03-owners', 'paging')),
    ])


# =============================================================================== 42
EP42 = E(
    42, 'api-cars-drivers-bookings',
    'Partner API 2: cars, drivers and bookings',
    'API para socios 2: coches, conductores y reservas',
    'Your own ids everywhere, a transponder per car, and whether a driver can be charged',
    'Sus propios id en todas partes, un transpondedor por coche, y si se puede cobrar al conductor',
    [
        B(en='Start with the cars. POST /cars creates one. Give it your own id in externalId.',
          es='Empiece por los coches. POST /cars crea uno. Dele su propio id en externalId.',
          shot='api-04-car', cam=look(box('api-04-car', 'req'), 1.2), ring=box('api-04-car', 'req'),
          label_en='POST /cars', label_es='POST /cars'),

        B(en='From then on your id works anywhere ours does, and every answer carries both.',
          es='Desde entonces su id vale en cualquier sitio donde valga el nuestro, y cada respuesta '
             'lleva los dos.',
          cam=look(box('api-04-car', 'res'), 1.4),
          ring=join(line('api-04-car', 'id'), line('api-04-car', 'ext'))),

        B(en='Attach the car\'s toll transponder, so its tolls are matched to it.',
          es='Asocie el transpondedor de peaje del coche, para que sus peajes se le asignen.',
          shot='api-05-transponder', cam=look(box('api-05-transponder', 'req'), 1.2),
          ring=box('api-05-transponder', 'req'),
          label_en='Transponders', label_es='Transpondedores'),

        B(en='POST /drivers adds a driver, with licence photos if you have them. Sending the same '
             'email again updates the driver instead of adding a second one.',
          es='POST /drivers añade un conductor, con fotos de la licencia si las tiene. Enviar el '
             'mismo correo otra vez actualiza al conductor en lugar de añadir otro.',
          shot='api-06-driver', cam=look(box('api-06-driver', 'req'), 1.2),
          ring=box('api-06-driver', 'req'),
          label_en='POST /drivers', label_es='POST /drivers'),

        B(en='A booking ties a car, a driver and a time window together, with your own ids for all '
             'three.',
          es='Una reserva une un coche, un conductor y un periodo, con sus propios id para los tres.',
          shot='api-07-booking', cam=look(box('api-07-booking', 'req'), 1.2),
          ring=box('api-07-booking', 'req'),
          label_en='POST /bookings', label_es='POST /bookings'),

        B(en='It is only a record. Creating it charges nobody anything.',
          es='Es solo un registro. Crearla no cobra nada a nadie.',
          cam=look(box('api-07-booking', 'res'), 1.35),
          ring=join(line('api-07-booking', 'car'), line('api-07-booking', 'renter'))),

        B(en='Before a rental, ask whether the driver can be charged. hasCard says a card is on '
             'file. isValid says it can really be charged.',
          es='Antes de un alquiler, pregunte si se puede cobrar al conductor. hasCard dice que hay '
             'una tarjeta. isValid dice que de verdad se puede cobrar.',
          shot='api-08-card', cam=look(box('api-08-card', 'res'), 1.25),
          ring=join(line('api-08-card', 'has'), line('api-08-card', 'valid')),
          label_en='Can this driver be charged?', label_es='¿Se puede cobrar al conductor?'),

        B(en='If not, card-link returns a page where the driver adds a card.',
          es='Si no, card-link devuelve una página donde el conductor añade una tarjeta.',
          shot='api-09-card-link', cam=look(box('api-09-card-link', 'res'), 1.4),
          ring=line('api-09-card-link', 'url'),
          label_en='Card link', label_es='Enlace de tarjeta'),

        B(en='Bookings are optional. If you do not track rentals, you can still read every toll by '
             'car. That is the next video.',
          es='Las reservas son opcionales. Si no registra alquileres, igualmente puede leer cada '
             'peaje por coche. Eso es el próximo vídeo.',
          shot='api-11-car-tolls', cam=look(box('api-11-car-tolls', 'req'), 1.2),
          ring=box('api-11-car-tolls', 'req'),
          label_en='Tolls by car', label_es='Peajes por coche'),
    ])


# =============================================================================== 43
EP43 = E(
    43, 'api-tolls-fines',
    'Partner API 3: tolls and fines',
    'API para socios 3: peajes y multas',
    'What each field means, whether the driver paid, and reading every page',
    'Qué significa cada campo, si el conductor pagó, y cómo leer todas las páginas',
    [
        B(en='GET /tolls returns every priced toll in a period, from the toll agencies and from GPS.',
          es='GET /tolls devuelve cada peaje con precio de un periodo, de las agencias de peaje y '
             'del GPS.',
          shot='api-10-tolls', cam=look(line('api-10-tolls', 'source'), 1.5),
          ring=line('api-10-tolls', 'source'),
          label_en='GET /tolls', label_es='GET /tolls'),

        B(en='agencyAmount is what the road really cost. serviceFee is our separate fee. They are '
             'never added together for you.',
          es='agencyAmount es lo que costó de verdad la carretera. serviceFee es nuestra tarifa '
             'aparte. Nunca se suman por usted.',
          cam=look(join(line('api-10-tolls', 'amount'), line('api-10-tolls', 'fee')), 1.5),
          ring=join(line('api-10-tolls', 'amount'), line('api-10-tolls', 'fee'))),

        B(en='A toll inside a booking says where the booking came from, for example a Turo trip.',
          es='Un peaje dentro de una reserva dice de dónde vino la reserva, por ejemplo un viaje de '
             'Turo.',
          cam=look(line('api-10-tolls', 'booking'), 1.5), ring=line('api-10-tolls', 'booking')),

        B(en='renterCharge says whether the driver paid it back: charged, declined, invoiced, and so '
             'on.',
          es='renterCharge dice si el conductor lo devolvió: charged, declined, invoiced, etcétera.',
          cam=look(line('api-10-tolls', 'charge'), 1.5), ring=line('api-10-tolls', 'charge')),

        B(en='The list is a page. hasMore true means there is more to fetch.',
          es='La lista es una página. hasMore en true significa que hay más por traer.',
          cam=look(line('api-10-tolls', 'more'), 1.5), ring=line('api-10-tolls', 'more')),

        B(en='This loop reads every page: up to a thousand rows a time, until hasMore is false.',
          es='Este bucle lee todas las páginas: hasta mil filas cada vez, hasta que hasMore sea '
             'false.',
          shot='api-14-paging', cam=look(box('api-14-paging', 'res'), 1.15),
          ring=join(line('api-14-paging', 'page'), line('api-14-paging', 'more')),
          label_en='Every page', label_es='Todas las páginas'),

        B(en='No bookings? Read one car\'s tolls over any period, using your own car id.',
          es='¿Sin reservas? Lea los peajes de un coche en cualquier periodo, con su propio id de '
             'coche.',
          shot='api-11-car-tolls', cam=look(box('api-11-car-tolls', 'req'), 1.2),
          ring=box('api-11-car-tolls', 'req'),
          label_en='Tolls by car', label_es='Peajes por coche'),

        B(en='With bookings, read the tolls of one rental. A GPS toll carries an id that starts with '
             'gps.',
          es='Con reservas, lea los peajes de un alquiler. Un peaje por GPS lleva un id que empieza '
             'por gps.',
          shot='api-12-booking-tolls', cam=look(box('api-12-booking-tolls', 'res'), 1.2),
          ring=join(line('api-12-booking-tolls', 'gps'), line('api-12-booking-tolls', 'ext')),
          label_en='Tolls of one booking', label_es='Peajes de una reserva'),

        B(en='Fines work the same way. amount is the fine, serviceFee is ours, and isPaid says whether '
             'it is settled.',
          es='Las multas funcionan igual. amount es la multa, serviceFee es lo nuestro, e isPaid dice '
             'si está pagada.',
          shot='api-13-violations', cam=look(box('api-13-violations', 'res'), 1.2),
          ring=join(line('api-13-violations', 'amount'), line('api-13-violations', 'paid')),
          label_en='GET /violations', label_es='GET /violations'),
    ])


# =============================================================================== 44
EP44 = E(
    44, 'api-gps-webhooks',
    'Partner API 4: GPS and webhooks',
    'API para socios 4: GPS y webhooks',
    'Where the cars are, how far they drove, and being told instead of asking',
    'Dónde están los coches, cuánto recorrieron, y recibir avisos en lugar de preguntar',
    [
        B(en='GET /gps/positions shows where every tracked car is now.',
          es='GET /gps/positions muestra dónde está ahora cada coche con rastreador.',
          shot='api-15-positions', cam=look(line('api-15-positions', 'pos'), 1.5),
          ring=line('api-15-positions', 'pos'),
          label_en='GPS positions', label_es='Posiciones GPS'),

        B(en='online and ageSeconds tell you how fresh that position is.',
          es='online y ageSeconds le dicen lo reciente que es esa posición.',
          cam=look(join(line('api-15-positions', 'age'), line('api-15-positions', 'online')), 1.5),
          ring=join(line('api-15-positions', 'age'), line('api-15-positions', 'online'))),

        B(en='Mileage adds up how far a car drove in a period, or during one rental. Raw positions '
             'are kept thirty days; priced GPS tolls stay for good.',
          es='El kilometraje suma cuánto recorrió un coche en un periodo, o en un alquiler. Las '
             'posiciones se guardan treinta días; los peajes por GPS con precio se quedan siempre.',
          shot='api-16-mileage', cam=look(box('api-16-mileage', 'res'), 1.3),
          ring=line('api-16-mileage', 'miles'),
          label_en='Mileage', label_es='Kilometraje'),

        B(en='Instead of asking again and again, register a webhook. We post to your address when '
             'something happens.',
          es='En lugar de preguntar una y otra vez, registre un webhook. Le enviamos un aviso a su '
             'dirección cuando pasa algo.',
          shot='api-17-webhook', cam=look(box('api-17-webhook', 'req'), 1.2),
          ring=box('api-17-webhook', 'req'),
          label_en='Webhooks', label_es='Webhooks'),

        B(en='A star means every event: new tolls, charge updates, new fines, owners connecting, and '
             'dispute evidence.',
          es='Una estrella significa todos los eventos: peajes nuevos, cambios de cobro, multas '
             'nuevas, propietarios que se conectan, y pruebas de disputas.',
          cam=look(line('api-17-webhook', 'events'), 1.6), ring=line('api-17-webhook', 'events')),

        B(en='The answer carries a secret, shown once. Keep it: it signs every delivery.',
          es='La respuesta lleva un secreto, que se muestra una sola vez. Guárdelo: firma cada envío.',
          cam=look(line('api-17-webhook', 'secret'), 1.6), ring=line('api-17-webhook', 'secret')),

        B(en='Check each delivery like this: sign the timestamp, a dot and the body with your '
             'secret, and compare.',
          es='Compruebe cada envío así: firme la marca de tiempo, un punto y el cuerpo con su '
             'secreto, y compare.',
          shot='api-18-verify', cam=look(box('api-18-verify', 'res'), 1.15),
          ring=join(line('api-18-verify', 'signed'), line('api-18-verify', 'hmac')),
          label_en='The signature', label_es='La firma'),

        B(en='Refuse an old timestamp, so a copied message cannot be sent again.',
          es='Rechace una marca de tiempo antigua, para que un mensaje copiado no pueda reenviarse.',
          cam=look(box('api-18-verify', 'res'), 1.15), ring=line('api-18-verify', 'replay')),

        B(en='A delivery can arrive twice. Keep the event id and ignore a repeat.',
          es='Un envío puede llegar dos veces. Guarde el id del evento e ignore la repetición.',
          cam=look(box('api-18-verify', 'res'), 1.15), ring=line('api-18-verify', 'dedup')),

        B(en='And before going live, POST test on your webhook sends a test event.',
          es='Y antes de ponerlo en marcha, POST test en su webhook envía un evento de prueba.',
          shot='api-17-webhook', cam=look(box('api-17-webhook', 'req'), 1.2)),
    ])


# =============================================================================== 45
EP45 = E(
    45, 'api-charges-disputes',
    'Partner API 5: your charges and disputes',
    'API para socios 5: sus cobros y disputas',
    'Charges made on your own Stripe account, and the evidence we build when one is disputed',
    'Cobros hechos en su propia cuenta de Stripe, y las pruebas que preparamos si se disputa uno',
    [
        B(en='When you charge a driver on your own Stripe account, tell us with POST /charges which '
             'tolls, fines and fees it covered.',
          es='Cuando cobra a un conductor en su propia cuenta de Stripe, díganos con POST /charges '
             'qué peajes, multas y tarifas cubría.',
          shot='api-19-charge', cam=look(box('api-19-charge', 'req'), 1.15),
          ring=box('api-19-charge', 'req'),
          label_en='POST /charges', label_es='POST /charges'),

        B(en='We check the sum. If the items do not add up to the charge, a warning says so.',
          es='Comprobamos la suma. Si las partidas no suman el cobro, un aviso lo dice.',
          cam=look(line('api-19-charge', 'warn'), 1.5), ring=line('api-19-charge', 'warn')),

        B(en='If the driver disputes that charge, report it with POST /disputes.',
          es='Si el conductor disputa ese cobro, notifíquelo con POST /disputes.',
          shot='api-20-dispute', cam=look(box('api-20-dispute', 'req'), 1.15),
          ring=box('api-20-dispute', 'req'),
          label_en='POST /disputes', label_es='POST /disputes'),

        B(en='We start collecting the evidence at once, and send dispute.evidence_ready when it is '
             'done.',
          es='Empezamos a reunir las pruebas enseguida, y enviamos dispute.evidence_ready cuando '
             'terminamos.',
          cam=look(line('api-20-dispute', 'ev'), 1.6), ring=line('api-20-dispute', 'ev')),

        B(en='Then read the dispute. The evidence is keyed by Stripe\'s own field names.',
          es='Después lea la disputa. Las pruebas usan los nombres de campo del propio Stripe.',
          shot='api-21-evidence', cam=look(line('api-21-evidence', 'ev'), 1.4),
          ring=line('api-21-evidence', 'ev'),
          label_en='The evidence package', label_es='El paquete de pruebas'),

        B(en='Pass the text to Stripe as it is. Each file you download, upload to your Stripe account, '
             'and use its file id instead.',
          es='Pase el texto a Stripe tal cual. Cada archivo lo descarga, lo sube a su cuenta de '
             'Stripe, y usa su id de archivo en su lugar.',
          cam=look(line('api-21-evidence', 'file'), 1.5), ring=line('api-21-evidence', 'file')),

        B(en='recommendation says whether to contest or accept.',
          es='recommendation dice si conviene disputar o aceptar.',
          cam=look(line('api-21-evidence', 'rec'), 1.5), ring=line('api-21-evidence', 'rec')),

        B(en='Submit it on your side, then tell us with PATCH: submitted, and later won or lost. We '
             'never touch your Stripe account.',
          es='Envíela desde su lado y díganoslo con PATCH: submitted, y después won o lost. Nunca '
             'tocamos su cuenta de Stripe.',
          shot='api-22-dispute-patch', cam=look(box('api-22-dispute-patch', 'req'), 1.2),
          ring=box('api-22-dispute-patch', 'req'),
          label_en='PATCH /disputes', label_es='PATCH /disputes'),

        B(en='Every function, with its example, is in the reference. The written guide has the same '
             'examples.',
          es='Cada función, con su ejemplo, está en la referencia. La guía escrita tiene los mismos '
             'ejemplos.',
          shot='api-00-swagger', url='/api/partner/v1/index', cam=(0.5, 0.5, 1.0),
          label_en='The reference', label_es='La referencia'),
    ])


partner(EP41, EP42, EP43, EP44, EP45)
