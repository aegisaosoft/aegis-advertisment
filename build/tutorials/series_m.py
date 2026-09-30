# -*- coding: utf-8 -*-
"""Episodes 36-40 — the partner guide to payments: how a partner's clients pay, and how much.

FOR PARTNERS, NOT OWNERS (E.audience = 'partner'). A partner brings fleet owners to us and
earns a share of what we make from them, so a partner has to know every way an owner can pay
and every amount behind it. The owner series says something simpler on purpose — to an owner
the offer is "you pay nothing" — so these episodes are uploaded unlisted, kept out of the owner
series playlist and off /tutorials, and reached only through the partner playlist.

  36  option 1, the driver pays us          — "Who collects payments" = Us (Aegis)
  37  option 2, the owner's booking system  — "Booking plugin"; our share is invoiced; Charge Target
  38  option 3, a flat fee per car          — "Pay per plate"
  39  the amounts: tolls and fines          — toll service fee, fee mode, range max charge, owner
                                              share, violation fee, partner share
  40  the amounts: rentals, GPS, per car    — booking commission, registration fee, GPS navigator
                                              fee, the per-car price

What each sentence rests on, so the narration can be checked against the code:
  - collectors per category off | platform | plugin; defaults toll & violation = platform,
    booking = off (PaymentCollectorCard.tsx, BookingPluginCredentialsStore.cs);
  - plugin collects the toll + fee into the owner's gateway, the owner owes PlatformShare +
    PartnerShare, billed by OwnerBillingService every BillingPeriodHours (default 168 = weekly);
  - Charge Target Driver | Owner (no money moves, no fee) | PlatformInvoice (one invoice per trip
    to the rental platform), fleet-platform bookings only;
  - toll service fee per toll or once per booking (TollServiceFeePolicy); range max charge bills
    the top rate and the difference is the markup (TollPaymentService); owner share splits the
    markup and our fee, admin 0-80 %, partner 0-20 % (OwnerTollBalanceController);
  - violation fee fixed $ or % of the fine, default $25 fixed; the driver pays fine + fee;
  - partner share default 20 % of our income from the owner, for the partner's earning period
    (PartnerShareTerm, default 365 days);
  - booking commission default 10 %, taken from the owner's payout on bookings we charge, split
    with the partner (BookingCommissionDefaults, RecordBookingCommissionAsync);
  - registration fee default $5.52, per booking or per rental day, 0 = off, minimum $0.50
    (OwnerSettings.DefaultRegistrationFee, TollPaymentService.ResolveRegistrationFee);
  - GPS navigator fee per active navigator we supply, last day of the month, default $10, 0 waives
    (GpsNavigatorFeeService); per-car price default $5.00 a day, every non-deleted car, partner
    share 0 (PlateFeeService: PartnerShareAmount = 0).

Not said, on purpose: the calculator on the Distribution Settings card (it hard-codes a $0.50
fee and disagrees with the real one — hidden before the shutter by capture-payments.js), and
any figure that is merely what our own test account holds.

The switches and amounts are admin-set, so the episodes say "tell us, we set it"; the two a
partner can change itself — Charge Target and Owner Share up to 20 % — are said as such. The
drawn screens (`pay-0N-*`) come from pay-diagrams.js; the portal cards (`pay-1N-*`) from
capture-payments.js, one card per frame, placed as recorded in shots/_pay_boxes.json.
"""
import io
import json
import os

from model import B, E

HERE = os.path.dirname(os.path.abspath(__file__))

# The three option cards on pay-01-overview, as rings (x, y, w, h) — pay-diagrams.js BOX.over.
OPT = [(0.055, 0.25, 0.28, 0.50), (0.36, 0.25, 0.28, 0.50), (0.665, 0.25, 0.28, 0.50)]
# The three flow boxes on pay-02..04 — pay-diagrams.js BOX.flow.
FLOW = [(0.05, 0.25, 0.20, 0.24), (0.40, 0.25, 0.20, 0.24), (0.75, 0.25, 0.20, 0.24)]
# The numbered notes under a flow (pay-02, pay-04), one row each.
NOTE = [(0.06, 0.58, 0.88, 0.07), (0.06, 0.669, 0.88, 0.07), (0.06, 0.758, 0.88, 0.07)]


def centre(r, zoom):
    x, y, w, h = r
    return (x + w / 2, y + h / 2, zoom)


def _boxes():
    try:
        return json.loads(io.open(os.path.join(HERE, 'shots', '_pay_boxes.json'), encoding='utf-8').read())
    except (OSError, ValueError):
        return {}


BOXES = _boxes()


PAD = 0.006        # a ring stands a little off the field it lights, never on its edge


def card(shot, rx=0.0, ry=0.0, rw=1.0, rh=1.0):
    """A rectangle inside a captured card, per language.

    (rx, ry, rw, rh) are fractions OF THE CARD, measured once on the English frame. Where the card
    sits on the frame differs by language (Spanish labels wrap to more lines, so a card is taller
    and starts higher), and capture-payments.js records exactly where it put each one — so the
    same field lands right in both languages without a Spanish coordinate written by hand.
    """
    out = {}
    for lang in ('en', 'es'):
        b = BOXES.get('%s/%s' % (lang, shot)) or BOXES.get('en/%s' % shot) or \
            {'x': 0.0, 'y': 0.0, 'w': 1.0, 'h': 1.0}
        pad = 0.0 if (rw, rh) == (1.0, 1.0) else PAD
        out[lang] = (round(b['x'] + rx * b['w'] - pad, 4), round(b['y'] + ry * b['h'] - pad, 4),
                     round(rw * b['w'] + 2 * pad, 4), round(rh * b['h'] + 2 * pad, 4))
    return out


def join(a, b):
    """The smallest per-language rectangle holding two card() rectangles side by side."""
    out = {}
    for lang in ('en', 'es'):
        (ax, ay, aw, ah), (bx, by, bw, bh) = a[lang], b[lang]
        x, y = min(ax, bx), min(ay, by)
        out[lang] = (x, y, max(ax + aw, bx + bw) - x, max(ay + ah, by + bh) - y)
    return out


def look(rect, zoom):
    """The camera centred on a per-language rectangle from card().

    The zoom asked for is an upper bound: it is lowered until the whole rectangle fits in the
    window with a margin, so a wide field is never cut off at the sides (the first cut lost the
    left half of the violation example at 1.5).
    """
    out = {}
    for lang, r in rect.items():
        z = max(1.0, min(zoom, 0.9 / r[2], 0.85 / r[3]))
        out[lang] = centre(r, round(z, 3))
    return out


def spot(rect, fx=0.5, fy=0.5):
    """A cursor point inside a per-language rectangle."""
    return dict((lang, (round(r[0] + fx * r[2], 4), round(r[1] + fy * r[3], 4))) for lang, r in rect.items())


# The fields the episodes point at, fractions of their card (measured on the English frames).
COLLECTOR = card('pay-10-collector')
COL_OFF = card('pay-10-collector', 0.082, 0.37, 0.304, 0.56)
COL_US = card('pay-10-collector', 0.387, 0.37, 0.304, 0.56)
COL_PLUGIN = card('pay-10-collector', 0.691, 0.37, 0.304, 0.56)
PLATE = card('pay-11-collector-per-plate')
PLATE_BTN = card('pay-11-collector-per-plate', 0.90, 0.11, 0.086, 0.19)
PLATE_FEE = card('pay-11-collector-per-plate', 0.013, 0.37, 0.972, 0.50)
DIST = card('pay-12-charge-target')
DIST_TARGET = card('pay-12-charge-target', 0.015, 0.33, 0.37, 0.12)
DIST_SHARE = card('pay-12-charge-target', 0.015, 0.523, 0.478, 0.124)
TOLL = card('pay-13-toll-service')
TOLL_FEE = card('pay-13-toll-service', 0.015, 0.107, 0.484, 0.164)
TOLL_MODE = card('pay-13-toll-service', 0.015, 0.30, 0.484, 0.194)
TOLL_RANGE = card('pay-13-toll-service', 0.508, 0.107, 0.28, 0.164)
TOLL_SOURCE = card('pay-13-toll-service', 0.015, 0.53, 0.84, 0.30)
VIOL = card('pay-14-violation-fee')
VIOL_ON = card('pay-14-violation-fee', 0.015, 0.325, 0.47, 0.14)
VIOL_AMOUNT = join(card('pay-14-violation-fee', 0.015, 0.513, 0.485, 0.232),
                   card('pay-14-violation-fee', 0.508, 0.513, 0.485, 0.232))
VIOL_EXAMPLE = card('pay-14-violation-fee', 0.015, 0.781, 0.977, 0.172)
BOOK = card('pay-15-booking-settings')
BOOK_COMMISSION = card('pay-15-booking-settings', 0.015, 0.20, 0.484, 0.34)
BOOK_REGFEE = card('pay-15-booking-settings', 0.508, 0.20, 0.484, 0.34)
BOOK_REGMODE = card('pay-15-booking-settings', 0.015, 0.645, 0.80, 0.287)
GPS = card('pay-16-gps-fee')
PARTNER = card('pay-17-partner-share')
PARTNER_SHARE = card('pay-17-partner-share', 0.508, 0.42, 0.48, 0.52)


def partner(*eps):
    for ep in eps:
        ep.audience = 'partner'
    return eps


# =============================================================================== 36
EP36 = E(
    36, 'pay-driver-pays',
    'Payment options 1: the driver pays us',
    'Formas de pago 1: el conductor nos paga',
    'The owner pays nothing: we charge the driver and pay the owner back',
    'El propietario no paga nada: cobramos al conductor y le devolvemos el dinero',
    [
        B(en='Every one of your clients pays us in the way that suits them. There are three ways.',
          es='Cada uno de sus clientes nos paga de la forma que le conviene. Hay tres formas.',
          shot='pay-01-overview', cam=(0.5, 0.5, 1.0),
          label_en='Three ways to pay', label_es='Tres formas de pagar'),

        B(en='The driver pays us. The owner\'s booking system collects. Or a flat fee for each '
             'car.',
          es='El conductor nos paga. Cobra el sistema de reservas del propietario. O una tarifa '
             'fija por cada coche.',
          cam=(0.5, 0.5, 1.0), hold=0.6),

        B(en='This video is the first way. With it, the owner pays nothing at all.',
          es='Este vídeo es la primera forma. Con ella, el propietario no paga nada.',
          cam=centre(OPT[0], 1.35), ring=OPT[0],
          label_en='1 · The driver pays us', label_es='1 · El conductor nos paga'),

        B(en='Here is how the money moves. The toll agency takes the toll from the owner '
             'automatically, as it always does.',
          es='Así se mueve el dinero. La agencia de peaje cobra el peaje al propietario '
             'automáticamente, como siempre.',
          shot='pay-02-driver-pays', cam=(0.5, 0.5, 1.0)),

        B(en='We charge the driver\'s card: the toll, plus our fee.',
          es='Nosotros cobramos a la tarjeta del conductor: el peaje, más nuestra tarifa.',
          cam=(0.33, 0.40, 1.30), ring=(0.05, 0.25, 0.55, 0.24)),

        B(en='The toll goes back to the owner, together with the owner\'s share of our fee, '
             'paid out to the owner\'s bank.',
          es='El peaje vuelve al propietario, junto con su parte de nuestra tarifa, pagado a '
             'su banco.',
          cam=(0.67, 0.40, 1.30), ring=(0.40, 0.25, 0.55, 0.24)),

        B(en='Fines work the same way. We show each fine in time to pay it before any late '
             'penalty, and the driver pays it back.',
          es='Las multas funcionan igual. Mostramos cada multa a tiempo para pagarla antes de '
             'cualquier recargo, y el conductor la devuelve.',
          cam=(0.5, 0.70, 1.25), ring=NOTE[1]),

        B(en='We can charge the rental too, if the owner wants. Then an agreed commission comes '
             'out of the rental payout.',
          es='También podemos cobrar el alquiler, si el propietario quiere. Entonces una '
             'comisión acordada se descuenta del pago del alquiler.',
          cam=(0.5, 0.79, 1.25), ring=NOTE[2]),

        B(en='In the portal the switch is called Who collects payments. It has three lines: '
             'Booking, Tolls and Violations.',
          es='En el portal, el interruptor se llama Quién cobra los pagos. Tiene tres líneas: '
             'Reserva, Peajes e Infracciones.',
          shot='pay-10-collector', cam=look(COLLECTOR, 1.15), ring=COLLECTOR,
          label_en='Who collects payments', label_es='Quién cobra los pagos'),

        B(en='Us, Aegis, means we charge the driver. Tolls and fines start that way. The rental '
             'stays off until the owner asks for it.',
          es='Nosotros (Aegis) significa que cobramos al conductor. Peajes e infracciones '
             'empiezan así. El alquiler queda apagado hasta que el propietario lo pida.',
          cam=look(COL_US, 1.6), ring=COL_US),

        B(en='Don\'t charge means nobody is charged for that line: the owner handles it.',
          es='No cobrar significa que no se cobra a nadie por esa línea: el propietario se '
             'encarga.',
          cam=look(COL_OFF, 1.6), ring=COL_OFF),

        B(en='This card is ours to set. Tell us what each client wants on each line, and we '
             'switch it on.',
          es='Esta tarjeta la configuramos nosotros. Díganos qué quiere cada cliente en cada '
             'línea y lo activamos.',
          cam=look(COLLECTOR, 1.15)),

        B(en='The owner\'s money arrives through Banking, Owner Account. It must say '
             'Onboarding Complete, with charges and payouts enabled.',
          es='El dinero del propietario llega por Banca, Cuenta del propietario. Debe decir '
             'Registro completado, con cargos y pagos habilitados.',
          shot='68-banking', url='/banking', cam=(0.45, 0.30, 1.35),
          ring=(0.203, 0.252, 0.782, 0.128),
          label_en='Banking · Owner Account', label_es='Banca · Cuenta del propietario'),

        B(en='And every charge that went through is listed under Payments, Successful '
             'Payments.',
          es='Y cada cobro realizado aparece en Pagos, Pagos exitosos.',
          shot='65-successful-payments', url='/successful-payments', cam=(0.5, 0.35, 1.0),
          label_en='Successful Payments', label_es='Pagos exitosos'),
    ])


# =============================================================================== 37
EP37 = E(
    37, 'pay-plugin-collects',
    'Payment options 2: the owner\'s booking system collects',
    'Formas de pago 2: cobra el sistema de reservas del propietario',
    'The owner\'s own software charges the driver; we invoice only our share',
    'El software del propietario cobra al conductor; facturamos solo nuestra parte',
    [
        B(en='The second way: the owner\'s own booking system collects the money.',
          es='La segunda forma: el propio sistema de reservas del propietario cobra el dinero.',
          shot='pay-01-overview', cam=centre(OPT[1], 1.35), ring=OPT[1],
          label_en='2 · The booking system collects',
          label_es='2 · Cobra el sistema de reservas'),

        B(en='If the owner runs rentals in booking software, like HQ Rental Software, it can '
             'charge the driver itself.',
          es='Si el propietario gestiona sus alquileres con un software de reservas, como HQ '
             'Rental Software, este puede cobrar al conductor por sí mismo.',
          shot='pay-03-plugin-collects', cam=(0.5, 0.5, 1.0)),

        B(en='We send it the toll or the fine, with our fee added. It charges the driver '
             'through the owner\'s own payment gateway.',
          es='Le enviamos el peaje o la multa, con nuestra tarifa incluida. Él cobra al '
             'conductor por la pasarela de pago del propietario.',
          cam=(0.33, 0.40, 1.30), ring=(0.05, 0.25, 0.55, 0.24)),

        B(en='So the whole amount lands with the owner.',
          es='Así el importe completo llega al propietario.',
          cam=centre(FLOW[1], 1.45), ring=FLOW[1]),

        B(en='We then invoice the owner only for our share of the fee. Once a week, unless we '
             'agree another period.',
          es='Después facturamos al propietario solo nuestra parte de la tarifa. Una vez por '
             'semana, salvo que acordemos otro periodo.',
          cam=centre(FLOW[2], 1.45), ring=FLOW[2]),

        B(en='On the Who collects payments card this is Booking plugin. It needs the booking '
             'system connected to us first.',
          es='En la tarjeta Quién cobra los pagos, esto es Complemento de reservas. Primero el '
             'sistema de reservas tiene que estar conectado con nosotros.',
          shot='pay-10-collector', cam=look(COL_PLUGIN, 1.6), ring=COL_PLUGIN,
          label_en='Who collects payments', label_es='Quién cobra los pagos'),

        B(en='Each line is separate. The booking system can collect the tolls while we collect '
             'the fines, or the other way round.',
          es='Cada línea es independiente. El sistema de reservas puede cobrar los peajes '
             'mientras nosotros cobramos las infracciones, o al revés.',
          cam=look(COLLECTOR, 1.15), ring=COLLECTOR),

        B(en='Our invoices appear under Billing, Invoices to pay. Open means it is waiting to '
             'be paid.',
          es='Nuestras facturas aparecen en Facturación, Facturas por pagar. Abierta significa '
             'que espera el pago.',
          shot='69-invoices-to-pay', url='/billing/invoices', cam=(0.6, 0.28, 1.25),
          ring=(0.203, 0.172, 0.782, 0.32),
          label_en='Invoices to pay', label_es='Facturas por pagar'),

        B(en='To pay them, the owner adds a card or a bank account under Banking, Payment '
             'Methods.',
          es='Para pagarlas, el propietario añade una tarjeta o una cuenta bancaria en Banca, '
             'Métodos de pago.',
          shot='68-banking', url='/banking', cam=(0.36, 0.22, 1.35),
          point={'en': (0.358, 0.198), 'es': (0.386, 0.198)}, click=1.6,
          label_en='Banking · Payment Methods', label_es='Banca · Métodos de pago'),

        B(en='Settlement Settings decides whether each invoice is paid by hand or '
             'automatically, and how often.',
          es='Configuración de liquidación decide si cada factura se paga a mano o '
             'automáticamente, y con qué frecuencia.',
          cam=(0.42, 0.22, 1.35),
          point={'en': (0.477, 0.198), 'es': (0.522, 0.198)}, click=1.6),

        B(en='For bookings that come from a rental platform, there are two more choices.',
          es='Para las reservas que llegan de una plataforma de alquiler, hay dos opciones '
             'más.',
          shot='pay-03-plugin-collects', cam=(0.5, 0.72, 1.20),
          ring=(0.06, 0.60, 0.88, 0.16)),

        B(en='Owner absorbs: the owner pays the toll. Nobody is charged, and there is no fee.',
          es='El propietario asume: el propietario paga el peaje. No se cobra a nadie y no hay '
             'tarifa.',
          cam=(0.28, 0.72, 1.40), ring=(0.06, 0.645, 0.432, 0.11)),

        B(en='Platform invoice: we bill the rental platform directly, one invoice per trip.',
          es='Factura de plataforma: facturamos directamente a la plataforma de alquiler, '
             'una factura por viaje.',
          cam=(0.72, 0.72, 1.40), ring=(0.508, 0.645, 0.432, 0.11)),

        B(en='That setting is Charge Target, on the owner\'s Distribution Settings. Driver is '
             'the standard. You can change it for your own clients.',
          es='Ese ajuste es Destino del cargo, en la Configuración de distribución del '
             'propietario. Conductor es lo normal. Usted puede cambiarlo para sus clientes.',
          shot='pay-12-charge-target', cam=look(DIST_TARGET, 1.7), ring=DIST_TARGET,
          label_en='Charge Target', label_es='Destino del cargo'),
    ])


# =============================================================================== 38
EP38 = E(
    38, 'pay-per-car',
    'Payment options 3: a flat fee per car',
    'Formas de pago 3: una tarifa fija por coche',
    'One price per car per day, one invoice per period',
    'Un precio por coche y día, una factura por periodo',
    [
        B(en='The third way is the simplest: a flat fee for each car.',
          es='La tercera forma es la más sencilla: una tarifa fija por cada coche.',
          shot='pay-01-overview', cam=centre(OPT[2], 1.35), ring=OPT[2],
          label_en='3 · A flat fee per car', label_es='3 · Una tarifa fija por coche'),

        B(en='The owner pays one fixed price per car, per day. The standard price is $5.00.',
          es='El propietario paga un precio fijo por coche y por día. El precio estándar es '
             '$5.00.',
          say_en='The owner pays one fixed price per car, per day. The standard price is five '
                 'dollars.',
          say_es='El propietario paga un precio fijo por coche y por día. El precio estándar es '
                 'cinco dólares.',
          shot='pay-04-per-car', cam=(0.5, 0.5, 1.0)),

        B(en='Or a price we agree for that client.',
          es='O un precio que acordemos para ese cliente.',
          cam=centre(FLOW[1], 1.45), ring=FLOW[1]),

        B(en='Every car in the account counts, every day. Remove a car, and it stops counting.',
          es='Cada coche de la cuenta cuenta, cada día. Si se quita un coche, deja de contar.',
          cam=centre(FLOW[0], 1.45), ring=FLOW[0]),

        B(en='In this mode we do not charge the owner\'s drivers at all. We still find every '
             'toll and every fine and show them.',
          es='En este modo no cobramos nada a los conductores del propietario. Seguimos '
             'encontrando cada peaje y cada multa y los mostramos.',
          cam=(0.5, 0.615, 1.25), ring=NOTE[0]),

        B(en='Once per billing period the owner gets one invoice for it.',
          es='Una vez por periodo, el propietario recibe una sola factura por ello.',
          cam=centre(FLOW[2], 1.45), ring=FLOW[2]),

        B(en='Worth knowing as a partner: this fee is all ours. No partner share is paid on it.',
          es='Conviene saberlo como socio: esta tarifa es toda nuestra. No se paga parte al '
             'socio.',
          cam=(0.5, 0.79, 1.25), ring=NOTE[2]),

        B(en='On the Who collects payments card, this is the Pay per plate switch at the top.',
          es='En la tarjeta Quién cobra los pagos, esto es el interruptor Pago por matrícula, '
             'arriba.',
          shot='pay-11-collector-per-plate', cam=look(PLATE, 1.2), ring=PLATE_BTN,
          point=spot(PLATE_BTN), click=1.6,
          label_en='Pay per plate', label_es='Pago por matrícula'),

        B(en='The price per car per day goes here. Left empty, the standard five dollars '
             'applies. The category lines turn off.',
          es='El precio por coche y día va aquí. Si se deja vacío, se aplican los cinco '
             'dólares estándar. Las líneas por categoría se apagan.',
          cam=look(PLATE_FEE, 1.35), ring=PLATE_FEE),

        B(en='The invoices arrive under Billing, Invoices to pay, and are paid like any other: '
             'card or bank, by hand or automatically.',
          es='Las facturas llegan a Facturación, Facturas por pagar, y se pagan como '
             'cualquier otra: tarjeta o banco, a mano o automáticamente.',
          shot='69-invoices-to-pay', url='/billing/invoices', cam=(0.6, 0.28, 1.25),
          ring=(0.203, 0.172, 0.782, 0.32),
          label_en='Invoices to pay', label_es='Facturas por pagar'),

        B(en='Three ways, one portal. Tell us which one each client chose, and we switch it on. '
             'It can be changed later.',
          es='Tres formas, un portal. Díganos cuál eligió cada cliente y la activamos. Se '
             'puede cambiar más adelante.',
          shot='pay-01-overview', url='', cam=(0.5, 0.5, 1.0),
          label_en='Three ways to pay', label_es='Tres formas de pagar'),
    ])


# =============================================================================== 39
EP39 = E(
    39, 'amounts-tolls-fines',
    'Setting the amounts: tolls and fines',
    'Fijar los importes: peajes y multas',
    'Our fee per toll, the markup, the owner\'s share, the fine fee and yours',
    'Nuestra tarifa por peaje, el margen, la parte del propietario, la tarifa de multas y la suya',
    [
        B(en='Every amount we charge is set for each client separately. This video is tolls '
             'and fines.',
          es='Cada importe que cobramos se fija para cada cliente por separado. Este vídeo trata '
             'los peajes y las multas.',
          shot='pay-13-toll-service', cam=look(TOLL, 1.1), ring=TOLL,
          label_en='Toll Service Settings', label_es='Servicio de peaje'),

        B(en='Toll Service Fee is our fee, in dollars, added to a toll. We agree it with each '
             'client.',
          es='Tarifa del servicio de peaje es nuestra tarifa, en dólares, que se suma a un '
             'peaje. La acordamos con cada cliente.',
          cam=look(TOLL_FEE, 1.6), ring=TOLL_FEE),

        B(en='Toll Fee Mode says how often. Per toll puts the fee on every toll. Per booking '
             'charges it once: the first toll of a booking carries it, the rest go without.',
          es='Modo de tarifa de peaje dice con qué frecuencia. Por peaje pone la tarifa en cada '
             'peaje. Por reserva la cobra una vez: el primer peaje de la reserva la lleva, los '
             'demás no.',
          cam=look(TOLL_MODE, 1.6), ring=TOLL_MODE),

        B(en='Range Max Charge bills the highest price of a toll road instead of the price '
             'actually paid. The difference is the markup, and it is shared like our fee.',
          es='Cargo máximo por rango factura el precio más alto de la carretera en lugar del '
             'precio pagado. La diferencia es el margen, y se reparte como nuestra tarifa.',
          cam=look(TOLL_RANGE, 1.7), ring=TOLL_RANGE),

        B(en='Toll charge source picks the amount billed: what the toll agency charged, or the '
             'estimate from GPS. Tolls the agency never reported can be added from GPS too.',
          es='Origen del importe del peaje elige el importe facturado: lo que cobró la agencia, '
             'o la estimación por GPS. Los peajes que la agencia nunca informó también pueden '
             'añadirse desde el GPS.',
          cam=look(TOLL_SOURCE, 1.3), ring=TOLL_SOURCE),

        B(en='How the money is split lives on the owner\'s Distribution Settings.',
          es='Cómo se reparte el dinero está en la Configuración de distribución del '
             'propietario.',
          shot='pay-12-charge-target', cam=look(DIST, 1.1), ring=DIST,
          label_en='Distribution Settings', label_es='Configuración de distribución'),

        B(en='Owner Share is the owner\'s part of our fee and of the markup. You can set it for '
             'your own clients, up to twenty percent. Above that, ask us.',
          es='Parte del propietario es su parte de nuestra tarifa y del margen. Usted puede '
             'fijarla para sus clientes, hasta el veinte por ciento. Por encima, pídanoslo.',
          cam=look(DIST_SHARE, 1.6), ring=DIST_SHARE),

        B(en='Fines have their own card. Charging can be switched on or off for each owner.',
          es='Las multas tienen su propia tarjeta. El cobro se puede activar o desactivar para '
             'cada propietario.',
          shot='pay-14-violation-fee', cam=look(VIOL_ON, 1.5), ring=VIOL_ON,
          label_en='Violation Fee Settings', label_es='Tarifas de infracciones'),

        B(en='The fee is either a fixed amount or a percentage of the fine. The standard is '
             'twenty-five dollars.',
          es='La tarifa es un importe fijo o un porcentaje de la multa. Lo estándar son '
             'veinticinco dólares.',
          cam=look(VIOL_AMOUNT, 1.25), ring=VIOL_AMOUNT),

        B(en='The example line does the sum: the driver pays the fine plus the fee. The owner '
             'shares the fee, never the fine.',
          es='La línea de ejemplo hace la cuenta: el conductor paga la multa más la tarifa. El '
             'propietario comparte la tarifa, nunca la multa.',
          cam=look(VIOL_EXAMPLE, 1.5), ring=VIOL_EXAMPLE),

        B(en='And your part. Partner Share is your percentage of what we earn from an owner you '
             'brought. The standard is twenty percent.',
          es='Y su parte. Porcentaje del socio es su porcentaje de lo que ganamos con un '
             'propietario que usted trajo. Lo estándar es el veinte por ciento.',
          shot='pay-17-partner-share', cam=look(PARTNER, 1.2), ring=PARTNER_SHARE,
          label_en='Partner Share', label_es='Porcentaje del socio'),

        B(en='It is paid for your earning period, counted from the day each owner registered. '
             'The standard period is one year.',
          es='Se paga durante su período de ganancias, contado desde el día en que se registró '
             'cada propietario. El período estándar es un año.',
          cam=look(PARTNER, 1.2)),
    ])


# =============================================================================== 40
EP40 = E(
    40, 'amounts-rentals-gps',
    'Setting the amounts: rentals, GPS and the per-car price',
    'Fijar los importes: alquileres, GPS y el precio por coche',
    'Booking commission, registration fee, the GPS navigator fee and the fee per car',
    'Comisión por reserva, tarifa de registro, la cuota de GPS y la tarifa por coche',
    [
        B(en='Rentals first. Booking Settings has two amounts.',
          es='Primero los alquileres. Configuración de reservas tiene dos importes.',
          shot='pay-15-booking-settings', cam=look(BOOK, 1.15), ring=BOOK,
          label_en='Booking Settings', label_es='Configuración de reservas'),

        B(en='Booking commission is our percentage of a rental we charge. It comes out of the '
             'owner\'s payout, not the driver\'s price, and you share in it.',
          es='Comisión por reserva es nuestro porcentaje de un alquiler que cobramos. Sale del '
             'pago al propietario, no del precio del conductor, y usted participa en ella.',
          cam=look(BOOK_COMMISSION, 1.6), ring=BOOK_COMMISSION),

        B(en='Left empty, the standard ten percent applies.',
          es='Si se deja vacío, se aplica el diez por ciento estándar.',
          cam=look(BOOK_COMMISSION, 1.6)),

        B(en='Registration Fee is charged to the driver once, when the booking is registered. '
             'The standard is $5.52. Zero switches it off.',
          es='Tarifa de registro se cobra al conductor una vez, al registrar la reserva. Lo '
             'estándar son $5.52. Cero la desactiva.',
          say_en='Registration Fee is charged to the driver once, when the booking is '
                 'registered. The standard is five dollars fifty-two. Zero switches it off.',
          say_es='Tarifa de registro se cobra al conductor una vez, al registrar la reserva. Lo '
                 'estándar son cinco dólares con cincuenta y dos. Cero la desactiva.',
          cam=look(BOOK_REGFEE, 1.6), ring=BOOK_REGFEE),

        B(en='Its mode is per booking, a flat amount, or per day: the fee times the number of '
             'rental days.',
          es='Su modo es por reserva, un importe fijo, o por día: la tarifa por el número de '
             'días de alquiler.',
          cam=look(BOOK_REGMODE, 1.5), ring=BOOK_REGMODE),

        B(en='GPS next. When we supply the GPS navigators, each active one is billed monthly, on '
             'the last day of the month, on its own invoice.',
          es='Después, el GPS. Cuando suministramos los navegadores GPS, cada uno activo se '
             'factura cada mes, el último día del mes, en su propia factura.',
          shot='pay-16-gps-fee', cam=look(GPS, 1.2), ring=GPS,
          label_en='GPS Navigator Billing', label_es='Navegadores GPS'),

        B(en='Left empty, the platform price applies: ten dollars a navigator. Zero waives it. '
             'A GPS the owner already has is connected for free.',
          es='Si se deja vacío, se aplica el precio de la plataforma: diez dólares por '
             'navegador. Cero lo anula. Un GPS que el propietario ya tiene se conecta gratis.',
          cam=look(GPS, 1.35)),

        B(en='And the per-car price from the third payment option: five dollars a car a day, '
             'unless we agree another.',
          es='Y el precio por coche de la tercera forma de pago: cinco dólares por coche y día, '
             'salvo que acordemos otro.',
          shot='pay-11-collector-per-plate', cam=look(PLATE_FEE, 1.35), ring=PLATE_FEE,
          label_en='Pay per plate', label_es='Pago por matrícula'),

        B(en='All of these are set by us, per client. Send us the amounts each client agreed '
             'to, and we enter them.',
          es='Todos estos los fijamos nosotros, por cliente. Envíenos los importes que acordó '
             'cada cliente y los introducimos.',
          shot='pay-01-overview', cam=(0.5, 0.5, 1.0),
          label_en='Three ways to pay', label_es='Tres formas de pagar'),
    ])


partner(EP36, EP37, EP38, EP39, EP40)
