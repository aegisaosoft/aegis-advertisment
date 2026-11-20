# -*- coding: utf-8 -*-
"""Episodes 9 to 11 — the tolls themselves, what they cost, and the tickets."""
from model import B, E


# =============================================================================== 09
EP09 = E(
    9, 'tolls',
    'Where your tolls land', 'Dónde aterrizan sus peajes',
    'The list the agencies fill in, and the one you pull yourself',
    'La lista que llenan las agencias, y la que usted trae a mano',
    [
        B(en='Tolls and Violations, then Tolls. Every toll the system has collected for you '
             'is here, newest first.',
          es='Peajes y Multas, y luego Peajes. Todos los peajes que el sistema ha recogido '
             'para usted están aquí, del más nuevo al más viejo.',
          shot='60-tolls', url='/tolls', cam=(0.5, 0.45, 1.0),
          label_en='Tolls', label_es='Peajes'),

        B(en='Hundreds of them on this account, ten to a page. Nobody typed any of them '
             'in — they arrived because the toll accounts from episode three are connected.',
          es='Cientos de ellos en esta cuenta, diez por página. Nadie tecleó ninguno: '
             'llegaron porque las cuentas de peaje del episodio tres están conectadas.',
          cam=(0.5, 0.78, 1.16),
          ring=(0.216, 0.780, 0.180, 0.040)),

        B(en='Read the row from the left. Date, time, plate, and the toll authority that '
             'billed it — GSP, NYSTA, NJTP, PANYNJ. That is which road, in the agency’s own '
             'shorthand.',
          es='Lea la fila de izquierda a derecha. Fecha, hora, matrícula, y la autoridad de '
             'peaje que lo facturó: GSP, NYSTA, NJTP, PANYNJ. Eso es qué carretera, en la '
             'abreviatura de la propia agencia.',
          cam=(0.40, 0.45, 1.18),
          ring=(0.228, 0.328, 0.335, 0.450)),

        B(en='Then two amounts, and the difference between them is the point. Amount is what '
             'the road charged. Adjusted Amount is what the driver is billed.',
          es='Luego dos importes, y la diferencia entre ellos es lo importante. Importe es lo '
             'que cobró la carretera. Importe ajustado es lo que se le factura al conductor.',
          cam=(0.76, 0.45, 1.24),
          ring=(0.700, 0.328, 0.184, 0.450),
          label_en='Amount vs Adjusted', label_es='Importe vs ajustado'),

        B(en='And Status is the outcome. Success means the money moved. New means it has not '
             'been billed yet. Failed means the card refused it — that one goes to the Failed '
             'Payments screen.',
          es='Y Estado es el desenlace. Correcto significa que el dinero se movió. Nuevo '
             'significa que aún no se ha facturado. Fallido significa que la tarjeta lo '
             'rechazó, y ese va a la pantalla de Pagos fallidos.',
          cam=(0.88, 0.45, 1.26),
          ring=(0.896, 0.328, 0.080, 0.450),
          label_en='Status', label_es='Estado'),

        B(en='Owner Trip is the one worth knowing. It means the car was not on a booking when '
             'it went through, so there is no driver to charge and the toll is yours. Seeing '
             'a lot of these usually means a booking is missing, not that you were driving.',
          es='Viaje del propietario es el que conviene conocer. Significa que el coche no '
             'estaba en una reserva al pasar, así que no hay conductor a quien cobrar y el '
             'peaje es suyo. Ver muchos de estos suele significar que falta una reserva, no '
             'que usted iba conduciendo.',
          cam=(0.88, 0.71, 1.30),
          ring=(0.896, 0.696, 0.080, 0.032),
          label_en='Owner Trip', label_es='Viaje del propietario'),

        B(en='Registration Fee rows are not road tolls at all — they are the once-per-booking '
             'fee, sitting in the same list because it is charged the same way.',
          es='Las filas de Cuota de registro no son peajes de carretera: son la cuota que se '
             'cobra una vez por reserva, en la misma lista porque se cobra igual.',
          cam=(0.64, 0.42, 1.26),
          ring=(0.606, 0.393, 0.090, 0.030)),

        B(en='That list is what the agencies pushed to you. There is a second screen for when '
             'you want to go and get them yourself.',
          es='Esa lista es lo que las agencias le enviaron. Hay una segunda pantalla para '
             'cuando quiera ir a buscarlos usted mismo.',
          shot='61-toll-transactions', url='/toll-transactions', cam=(0.5, 0.40, 1.0),
          label_en='Toll Transactions', label_es='Transacciones de peaje'),

        B(en='Pick an account, pick a date range, and press Load Transactions. It signs in '
             'and reads the agency portal live, right now, rather than waiting for the next '
             'scheduled collection.',
          es='Elija una cuenta, elija un rango de fechas, y pulse Cargar transacciones. Entra '
             'y lee el portal de la agencia en vivo, ahora mismo, en vez de esperar a la '
             'siguiente recogida programada.',
          cam=(0.42, 0.22, 1.24),
          point={'en': (0.665, 0.214), 'es': (0.672, 0.214)}, click=1.9,
          ring={'en': (0.200, 0.192, 0.530, 0.042),
                'es': (0.200, 0.192, 0.545, 0.042)},
          label_en='Load Transactions', label_es='Cargar transacciones'),

        B(en='What comes back is finer-grained than the toll list: provider, transponder, the '
             'named facility, and the entry and exit plazas.',
          es='Lo que vuelve es más detallado que la lista de peajes: proveedor, '
             'transpondedor, la instalación con nombre, y las plazas de entrada y salida.',
          cam={'en': (0.68, 0.50, 1.20), 'es': (0.68, 0.55, 1.20)},
          ring={'en': (0.626, 0.355, 0.256, 0.404),
                'es': (0.626, 0.406, 0.256, 0.404)},
          label_en='Facility, entry, exit', label_es='Instalación, entrada, salida'),

        B(en='Loading is only looking. Nothing you see here is in your system until you press '
             'Save to System — that is the button that commits it.',
          es='Cargar es solo mirar. Nada de lo que ve aquí está en su sistema hasta que pulse '
             'Guardar en el sistema: ese es el botón que lo confirma.',
          cam=(0.72, 0.22, 1.28),
          point={'en': (0.792, 0.214), 'es': (0.817, 0.214)}, click=1.7,
          ring={'en': (0.732, 0.193, 0.116, 0.040),
                'es': (0.746, 0.193, 0.140, 0.040)},
          label_en='Save to System', label_es='Guardar en el sistema'),

        B(en='Excel and PDF export exactly what is on screen, filters and all — which is the '
             'quickest way to answer a driver who says a toll is not theirs.',
          es='Excel y PDF exportan exactamente lo que está en pantalla, filtros incluidos, y '
             'es la forma más rápida de responder a un conductor que dice que un peaje no es '
             'suyo.',
          cam={'en': (0.86, 0.22, 1.28), 'es': (0.80, 0.24, 1.24)},
          point={'en': (0.885, 0.214), 'es': (0.924, 0.214)}, click=1.5,
          ring={'en': (0.854, 0.193, 0.124, 0.040),
                'es': (0.213, 0.193, 0.766, 0.098)}),
    ])


# =============================================================================== 10
EP10 = E(
    10, 'charges',
    'Charges — who actually pays', 'Cargos: quién paga de verdad',
    'One row per attempt to move money, and the four numbers on it',
    'Una fila por cada intento de mover dinero, y sus cuatro cifras',
    [
        B(en='Payments, then Charges. A toll is a thing that happened on a road. A charge is '
             'an attempt to take money for it, and that is what this page lists.',
          es='Pagos, y luego Cargos. Un peaje es algo que pasó en una carretera. Un cargo es '
             'un intento de cobrar por ello, y eso es lo que lista esta página.',
          shot='62-charges', url='/charges', cam=(0.5, 0.45, 1.0),
          label_en='Payments → Charges', label_es='Pagos → Cargos'),

        B(en='Payment status first, because it is the only column that tells you whether the '
             'money is actually yours.',
          es='Primero el estado del pago, porque es la única columna que le dice si el dinero '
             'es realmente suyo.',
          cam=(0.32, 0.45, 1.26),
          ring=(0.274, 0.326, 0.080, 0.470),
          label_en='Payment status', label_es='Estado del pago'),

        B(en='Success is money taken. Owner Trip, again, is a charge with nobody on the other '
             'end: the car was between bookings, so the amount is real but it is coming out '
             'of your pocket, not a driver’s.',
          es='Correcto es dinero cobrado. Viaje del propietario, otra vez, es un cargo sin '
             'nadie al otro lado: el coche estaba entre reservas, así que el importe es real '
             'pero sale de su bolsillo, no del de un conductor.',
          cam=(0.32, 0.50, 1.30),
          ring=(0.279, 0.489, 0.052, 0.026),
          label_en='Owner Trip', label_es='Viaje del propietario'),

        B(en='The small icon in Type says what kind of charge it is — a road toll, or the '
             'registration fee on a booking. Two different things, one list, because they are '
             'billed through the same card.',
          es='El pequeño icono de Tipo dice qué clase de cargo es: un peaje de carretera, o '
             'la cuota de registro de una reserva. Dos cosas distintas, una lista, porque se '
             'cobran con la misma tarjeta.',
          cam=(0.38, 0.45, 1.28),
          ring=(0.358, 0.326, 0.040, 0.470),
          label_en='Type', label_es='Tipo'),

        B(en='Then the money. Amount is what was asked for. Actual Amount is what came '
             'through. When those two differ, something was adjusted or partly refunded, and '
             'the row is worth opening.',
          es='Después, el dinero. Importe es lo que se pidió. Importe real es lo que entró. '
             'Cuando esos dos difieren, algo se ajustó o se devolvió en parte, y merece la '
             'pena abrir la fila.',
          cam=(0.74, 0.45, 1.26),
          ring=(0.698, 0.326, 0.140, 0.470),
          label_en='Amount vs Actual', label_es='Importe vs real'),

        B(en='Items is how many tolls this one charge covers. Several tolls on the same '
             'booking are collected into a single card transaction rather than a dozen small '
             'ones — cheaper for you, and less alarming for the driver.',
          es='Elementos es cuántos peajes cubre este único cargo. Varios peajes de la misma '
             'reserva se agrupan en una sola transacción de tarjeta en vez de una docena '
             'pequeñas: más barato para usted, y menos alarmante para el conductor.',
          cam=(0.84, 0.45, 1.28),
          ring=(0.864, 0.326, 0.038, 0.470),
          label_en='Items', label_es='Elementos'),

        B(en='And Total Commission is the platform’s share of what was recovered. Notice it '
             'is zero on every Owner Trip row: nothing was recovered from anybody, so nothing '
             'is taken.',
          es='Y Comisión total es la parte de la plataforma sobre lo recuperado. Fíjese en '
             'que es cero en cada fila de Viaje del propietario: no se recuperó nada de '
             'nadie, así que no se cobra nada.',
          cam=(0.92, 0.45, 1.26),
          ring=(0.930, 0.326, 0.066, 0.470),
          label_en='Total Commission', label_es='Comisión total'),

        B(en='The filter at the top starts on two statuses. Widen it when you are auditing a '
             'month and narrow it when you are chasing one problem.',
          es='El filtro de arriba empieza con dos estados. Ensánchelo cuando esté auditando '
             'un mes, y estréchelo cuando persiga un solo problema.',
          cam=(0.34, 0.23, 1.26),
          point=(0.279, 0.235), click=1.4,
          ring=(0.216, 0.212, 0.126, 0.040)),

        B(en='And the three dots on a row lead back to the booking the charge belongs to, so '
             'you are never more than one click from the driver who owes it.',
          es='Y los tres puntos de una fila llevan de vuelta a la reserva a la que pertenece '
             'el cargo, así que nunca está a más de un clic del conductor que lo debe.',
          cam=(0.28, 0.48, 1.28),
          point=(0.242, 0.470), click=1.3),
    ])


# =============================================================================== 11
# Re-shot 2026-11-08 on the current page (nov-01/02, capture-nov-features.js, demo rows): the Find Violations scan,
# the Date/Time/Car/Citation/Amount/Location/Agency columns, the Pay link, the row menu Info / Bookings / Paid by cash,
# and the new Add mailed ticket button (episode 57).
_V_FIND = {'en': (0.660, 0.098, 0.118, 0.048), 'es': (0.660, 0.098, 0.139, 0.048)}
_V_ADD = {'en': (0.776, 0.098, 0.131, 0.048), 'es': (0.798, 0.098, 0.147, 0.048)}
_V_WHEN = (0.306, 0.318, 0.146, 0.192)
_V_CAR = (0.458, 0.318, 0.142, 0.192)
_V_CIT = (0.598, 0.318, 0.134, 0.192)
_V_WHERE = (0.762, 0.318, 0.224, 0.192)
_V_PAY = (0.256, 0.380, 0.036, 0.032)
_V_MENU = {'en': (0.215, 0.434, 0.106, 0.122), 'es': (0.215, 0.434, 0.106, 0.142)}


def _vlook(r, z):
    if isinstance(r, dict):
        return dict((k, _vlook(v, z)) for k, v in r.items())
    x, y, w, h = r
    return (round(x + w / 2, 4), round(y + h / 2, 4), round(max(1.0, min(z, 0.9 / w, 0.85 / h)), 3))


EP11 = E(
    11, 'violations',
    'Violations', 'Multas',
    'Camera tickets are not tolls, and they arrive much later',
    'Las multas de cámara no son peajes, y llegan mucho más tarde',
    [
        B(en='Tolls and Violations, then Violations. These are camera tickets and citations — '
             'a different kind of debt from a toll, and worth its own screen.',
          es='Peajes e infracciones, y luego Infracciones. Estas son multas de cámara y citaciones: una '
             'clase de deuda distinta de un peaje, y merece su propia pantalla.',
          shot='nov-01-violations', url='/violations', cam=(0.5, 0.42, 1.0),
          label_en='Violations', label_es='Infracciones'),

        B(en='The first thing to understand is timing. A toll shows up within days. A '
             'violation is published by the issuing authority weeks later — often a week and a '
             'half after the car went past the camera.',
          es='Lo primero que hay que entender es el tiempo. Un peaje aparece en días. Una '
             'multa la publica la autoridad emisora semanas después, a menudo semana y media '
             'después de que el coche pasara ante la cámara.',
          cam=(0.5, 0.42, 1.0)),

        B(en='Which means a booking can be finished, the car returned and the driver gone, and '
             'the ticket only appears afterwards. That is normal: the system keeps looking on its own.',
          es='Lo que significa que una reserva puede estar terminada, el coche devuelto y el '
             'conductor lejos, y la multa aparecer solo después. Es normal: el sistema sigue buscando '
             'por su cuenta.',
          cam=(0.5, 0.42, 1.0)),

        B(en='Find Violations asks the agencies right now, for the dates you pick. The line under the '
             'buttons says when the last search ran.',
          es='Buscar infracciones pregunta a las agencias ahora mismo, para las fechas que elija. La línea '
             'bajo los botones dice cuándo fue la última búsqueda.',
          cam=_vlook(_V_FIND, 1.4), ring=_V_FIND,
          label_en='Find Violations', label_es='Buscar infracciones'),

        B(en='Date and time are when the authority says it happened, not when it reached you. That '
             'moment is what ties the ticket to a booking.',
          es='La fecha y la hora son cuándo dice la autoridad que ocurrió, no cuándo le llegó a usted. Ese '
             'momento es lo que une la multa a una reserva.',
          cam=_vlook(_V_WHEN, 1.3), ring=_V_WHEN,
          label_en='Date and time', label_es='Fecha y hora'),

        B(en='The car, with its plate and state exactly as on the vehicle — the pair from episode five.',
          es='El coche, con su matrícula y estado exactamente como en el vehículo: el par del episodio '
             'cinco.',
          cam=_vlook(_V_CAR, 1.3), ring=_V_CAR,
          label_en='Car', label_es='Vehículo'),

        B(en='The citation number you quote if you contest it, and the amount.',
          es='El número de citación que cita si la recurre, y el importe.',
          cam=_vlook(_V_CIT, 1.3), ring=_V_CIT,
          label_en='Citation and amount', label_es='Citación e importe'),

        B(en='Where it happened, and who issued it: a city transport department, a traffic authority, '
             'or a processing centre acting for one of them.',
          es='Dónde ocurrió, y quién la emitió: un departamento municipal de transporte, una autoridad de '
             'tráfico, o un centro de procesamiento que actúa por cuenta de alguno de ellos.',
          cam=_vlook(_V_WHERE, 1.25), ring=_V_WHERE,
          label_en='Location and agency', label_es='Ubicación y organismo'),

        B(en="Pay opens the agency's own page for that ticket.",
          es='Pagar abre la página de la propia agencia para esa multa.',
          cam=_vlook(_V_PAY, 1.6), ring=_V_PAY,
          label_en='Pay', label_es='Pagar'),

        B(en='The three dots open the row menu. Info shows everything about the ticket, Bookings opens '
             'the rental it belongs to, and Paid by cash is for a fine the driver paid you by hand.',
          es='Los tres puntos abren el menú de la fila. Información muestra todo sobre la multa, Reservas abre '
             'el alquiler al que pertenece, y Pagado en efectivo es para una multa que el conductor le '
             'pagó en mano.',
          shot='nov-02-row-menu', cam=_vlook(_V_MENU, 1.5), ring=_V_MENU,
          point=(0.2255, 0.396), click=0.6,
          label_en='Row menu', label_es='Menú de la fila'),

        B(en='And a ticket that came by mail? Add mailed ticket — that is the next episode.',
          es='¿Y una multa que llegó por correo? Añadir multa recibida: es el siguiente episodio.',
          shot='nov-01-violations', cam=_vlook(_V_ADD, 1.4), ring=_V_ADD,
          label_en='Add mailed ticket', label_es='Añadir multa recibida'),
    ])
