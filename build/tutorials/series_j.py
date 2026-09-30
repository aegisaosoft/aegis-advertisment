# -*- coding: utf-8 -*-
"""Episodes 27-30 — HQ Rental Software: the two keys, the cars, the bookings, the money.

Unlike Turo, HQ is a system the owner already works in every day, and the connection runs
both ways: bookings and cars come to the portal, tolls and violations go back to HQ as
external charges and are taken from the card HQ holds. So this part alternates between two
screens — HQ's own pages (captured by capture-hq.js, shots named `hq-*`) and the portal's
(`hq-p-*`) — and the narration says which of the two it is on every time it changes.

HQ renders in English for both languages of the series: the Spanish lines name each HQ
control in English and give the meaning beside it, the way somebody explaining a foreign
menu would. The portal's own screens are captured in Spanish as usual.
"""
from model import B, E


# =============================================================================== 27
EP27 = E(
    27, 'hq-connect',
    'HQ Rental Software, part 1: connecting it', 'HQ Rental Software, parte 1: conectarlo',
    'The two keys HQ gives you, and what happens once we have them',
    'Las dos claves que le da HQ, y qué pasa cuando las tenemos',
    [
        B(en='If you run your rentals in HQ Rental Software, the portal can read them straight '
             'from it. You keep working in HQ. Nothing is typed twice.',
          es='Si lleva sus alquileres en HQ Rental Software, el portal puede leerlos directamente '
             'de allí. Usted sigue trabajando en HQ. Nada se escribe dos veces.',
          shot='hq-p-50-bookings', url='/bookings', cam=(0.5, 0.22, 1.0),
          label_en='Your bookings, in the portal', label_es='Sus reservas, en el portal'),

        B(en='Your bookings arrive with a label that says where they came from, and the tolls of '
             'each one are collected the way HQ collects everything else.',
          es='Sus reservas llegan con una etiqueta que dice de dónde vienen, y los peajes de cada '
             'una se cobran como HQ cobra todo lo demás.',
          cam=(0.33, 0.33, 1.34),
          ring=(0.276, 0.290, 0.140, 0.100),
          label_en='Where the booking came from', label_es='De dónde viene la reserva'),

        B(en='To set this up we need two keys from HQ. Both are already there. You only have to '
             'find them and copy them.',
          es='Para conectarlo necesitamos dos claves de HQ. Las dos ya existen. Solo hay que '
             'encontrarlas y copiarlas.',
          shot='hq-10-integrations', url='HQ · Settings › Integrations', cam=(0.5, 0.30, 1.0),
          label_en='HQ · Integrations', label_es='HQ · Integraciones'),

        B(en='In HQ, open Settings — the gear on the left — and then Integrations.',
          es='En HQ, abra Settings, el engranaje de la izquierda, y después Integrations, que son '
             'las integraciones.',
          cam=(0.12, 0.22, 1.20),
          point=(0.052, 0.228), click=1.4),

        B(en='The first card is Custom Integration Kit. It should say Enabled. If it says Enable, '
             'press it once — that creates the user the portal signs in as.',
          es='La primera tarjeta es Custom Integration Kit. Debe decir Enabled, activado. Si dice '
             'Enable, púlselo una vez: eso crea el usuario con el que entra el portal.',
          cam=(0.457, 0.42, 1.18),
          ring=(0.357, 0.274, 0.200, 0.308),
          label_en='Custom Integration Kit', label_es='Custom Integration Kit'),

        B(en='Now the first key. Go back to Settings and open the section called Integrations.',
          es='Ahora la primera clave. Vuelva a Settings y abra la sección llamada Integrations.',
          shot='hq-12-tenant-token', url='HQ · Settings', cam=(0.5, 0.45, 1.0),
          point=(0.181, 0.510), click=1.5,
          label_en='Tenant API Token', label_es='Tenant API Token'),

        B(en='On the right is Tenant API Token. That key says which company you are. Select it '
             'and copy it.',
          es='A la derecha está Tenant API Token. Esa clave dice qué empresa es usted. '
             'Selecciónela y cópiela.',
          cam=(0.60, 0.575, 1.42),
          ring=(0.455, 0.545, 0.300, 0.050)),

        B(en='Treat it like a password. Anybody holding it can read your bookings.',
          es='Trátela como una contraseña. Quien la tenga puede leer sus reservas.',
          cam=(0.60, 0.575, 1.42),
          hold=0.4),

        B(en='The second key belongs to a user. Open User Management, then Users.',
          es='La segunda clave es de un usuario. Abra User Management, y después Users.',
          shot='hq-13-users', url='HQ · Settings › Users', cam=(0.12, 0.30, 1.20),
          point=(0.055, 0.330), click=1.5,
          label_en='Users', label_es='Users'),

        B(en='In the list, the one you want is called Custom Integration. Click the name.',
          es='En la lista, el que busca se llama Custom Integration. Haga clic en el nombre.',
          cam=(0.30, 0.31, 1.30),
          point=(0.256, 0.304), click=1.6,
          ring=(0.206, 0.292, 0.130, 0.028)),

        B(en='A form opens. Near the bottom is User API Token. That is the second key — copy it '
             'as well.',
          es='Se abre un formulario. Abajo está User API Token. Esa es la segunda clave: '
             'cópiela también.',
          shot='hq-14-user-token', cam=(0.45, 0.56, 1.34),
          ring=(0.312, 0.535, 0.290, 0.050),
          label_en='User API Token', label_es='User API Token'),

        B(en='Beside it there is Generate new token. Press that only if the key has leaked — a '
             'new one stops the old one working, and the connection stops with it.',
          es='Al lado está Generate new token, generar una clave nueva. Púlselo solo si la clave '
             'se ha filtrado: la nueva anula la anterior, y la conexión se detiene con ella.',
          cam=(0.45, 0.56, 1.34),
          ring=(0.386, 0.541, 0.112, 0.022)),

        B(en='Send both keys to MyEZToll support. We enter them and switch the connection on — '
             'there is nothing for you to fill in on our side.',
          es='Envíe las dos claves al soporte de MyEZToll. Nosotros las introducimos y activamos '
             'la conexión: en nuestro lado usted no tiene que rellenar nada.',
          shot='hq-p-53-pending', url='/p2p-bookings/hqrental', cam=(0.5, 0.20, 1.06),
          label_en='The portal · HQ Rental Software',
          label_es='El portal · HQ Rental Software'),

        B(en='When it is on, this page appears, named after HQ. One tab for bookings waiting for '
             'you, one for drivers, one for the cars found in HQ, and a history.',
          es='Cuando está activa aparece esta página, con el nombre de HQ. Una pestaña para las '
             'reservas que le esperan, otra para los conductores, otra para los coches '
             'encontrados en HQ, y un historial.',
          cam=(0.42, 0.115, 1.30),
          ring=(0.172, 0.088, 0.480, 0.046)),

        B(en='And the Bookings page grows a button: Get from HQ Rental Software. Press it once, '
             'and the first load runs.',
          es='Y la página de reservas gana un botón: Get from HQ Rental Software, traer de HQ. '
             'Púlselo una vez y se hace la primera carga.',
          shot='hq-p-50-bookings', url='/bookings', cam=(0.72, 0.10, 1.34),
          point=(0.757, 0.044), click=1.7,
          ring=(0.690, 0.030, 0.145, 0.030),
          label_en='Get from HQ Rental Software', label_es='Get from HQ Rental Software'),

        B(en='After that you do not press anything. The portal asks HQ by itself, about once an '
             'hour, and the next three videos show what it brings.',
          es='Después ya no hay que pulsar nada. El portal le pregunta a HQ por su cuenta, más o '
             'menos una vez por hora, y los tres vídeos siguientes muestran lo que trae.',
          cam=(0.5, 0.22, 1.0)),
    ])


# =============================================================================== 28
EP28 = E(
    28, 'hq-cars',
    'HQ Rental Software, part 2: your cars', 'HQ Rental Software, parte 2: sus coches',
    'The fleet arrives by itself — and the two things you still fill in',
    'La flota llega sola, y las dos cosas que usted todavía rellena',
    [
        B(en='The first thing the connection brings is your fleet. You do not add a single car by '
             'hand.',
          es='Lo primero que trae la conexión es su flota. Usted no añade ni un coche a mano.',
          shot='hq-p-55-platform-cars', url='/p2p-bookings/hqrental', cam=(0.5, 0.20, 1.04),
          label_en='HQ Rental Software Cars', label_es='HQ Rental Software Cars'),

        B(en='The tab named after HQ lists every car the portal found there, with the number '
             'beside the name.',
          es='La pestaña con el nombre de HQ enumera todos los coches que el portal encontró '
             'allí, con la cantidad al lado del nombre.',
          cam=(0.51, 0.115, 1.34),
          ring=(0.440, 0.090, 0.130, 0.044)),

        B(en='A car that matches one of yours is linked to it. A car the portal has not seen '
             'before waits here until you say it is the same car.',
          es='Un coche que coincide con uno suyo queda enlazado. Un coche que el portal no '
             'conoce espera aquí hasta que usted diga que es el mismo coche.',
          cam=(0.5, 0.33, 1.20)),

        B(en='Linked cars sit in Vehicles, next to everything else you own. From here on they are '
             'ordinary cars of yours.',
          es='Los coches enlazados están en Vehículos, junto a todo lo demás. A partir de aquí '
             'son coches suyos normales.',
          shot='hq-p-10-vehicles', url='/all-vehicles', cam=(0.5, 0.25, 1.0),
          label_en='Vehicles', label_es='Vehículos'),

        B(en='Two things HQ does not send, and the portal must not guess. Both decide whether a '
             'toll ever reaches the right car.',
          es='Hay dos cosas que HQ no envía y que el portal no debe adivinar. Las dos deciden si '
             'un peaje llega alguna vez al coche correcto.',
          cam=(0.5, 0.25, 1.0),
          hold=0.3),

        B(en='The first is the state the plate belongs to. HQ keeps the number only. The same '
             'number exists in other states, on other cars, so fill the state in yourself.',
          es='La primera es el estado al que pertenece la matrícula. HQ guarda solo el número. '
             'El mismo número existe en otros estados, en otros coches, así que ponga el estado '
             'usted mismo.',
          shot='hq-p-62-charges', url='/payments/charges', cam=(0.50, 0.24, 1.34),
          ring=(0.500, 0.200, 0.075, 0.060),
          label_en='Plate state', label_es='Estado de la matrícula'),

        B(en='The second is the toll tag — the transponder number. In HQ it sits on the vehicle, '
             'in the column Toll Tag.',
          es='La segunda es la etiqueta de peaje, el número del transpondedor. En HQ está en el '
             'vehículo, en la columna Toll Tag.',
          shot='hq-15-vehicles', url='HQ · Fleet › Vehicles', cam=(0.90, 0.33, 1.28),
          ring=(0.925, 0.195, 0.070, 0.620),
          label_en='HQ · Toll Tag', label_es='HQ · Toll Tag'),

        B(en='If that column is empty, the toll agency is the one to ask: the tag number is on '
             'the transponder itself and in your agency account.',
          es='Si esa columna está vacía, pregunte a la agencia de peajes: el número está en el '
             'propio transpondedor y en su cuenta de la agencia.',
          cam=(0.90, 0.33, 1.28)),

        B(en='A car with no tag brings in no tolls. Not fewer — none. Nothing tells the agency '
             'which car drove through.',
          es='Un coche sin etiqueta no trae ningún peaje. No menos: ninguno. Nada le dice a la '
             'agencia qué coche pasó.',
          shot='hq-p-10-vehicles', url='/all-vehicles', cam=(0.5, 0.30, 1.10),
          hold=0.4),

        B(en='So the vehicle list colours those cars for you — one colour for a car without a '
             'toll agency, another for a car without a tag. Clear them, and the fleet is done.',
          es='Por eso la lista de coches los colorea: un color para el coche sin agencia de '
             'peajes, otro para el coche sin etiqueta. Déjela sin colores y la flota está lista.',
          cam=(0.5, 0.30, 1.10)),
    ])


# =============================================================================== 29
EP29 = E(
    29, 'hq-bookings',
    'HQ Rental Software, part 3: bookings and drivers',
    'HQ Rental Software, parte 3: reservas y conductores',
    'Every reservation, who rented the car, and the window that decides who pays',
    'Cada reserva, quién alquiló el coche, y la ventana que decide quién paga',
    [
        B(en='Every reservation you make in HQ turns up in the portal by itself, usually within '
             'the hour.',
          es='Cada reserva que hace en HQ aparece en el portal por su cuenta, normalmente dentro '
             'de la hora.',
          shot='hq-p-50-bookings', url='/bookings', cam=(0.5, 0.22, 1.02),
          label_en='Bookings', label_es='Reservas'),

        B(en='The Source column says where each one came from. HQ Rental means HQ made it; Our '
             'booking means it was made here, on your own site.',
          es='La columna Source dice de dónde viene cada una. HQ Rental significa que la hizo '
             'HQ; Our booking, que se hizo aquí, en su propio sitio.',
          cam=(0.33, 0.33, 1.38),
          ring=(0.276, 0.290, 0.105, 0.100),
          label_en='Source', label_es='Origen'),

        B(en='And the filter above the list shows one kind at a time, when you want to look at '
             'HQ bookings only.',
          es='Y el filtro de arriba muestra un tipo cada vez, cuando quiere ver solo las reservas '
             'de HQ.',
          cam=(0.24, 0.13, 1.34),
          point=(0.225, 0.117), click=1.5,
          ring=(0.176, 0.100, 0.105, 0.034)),

        B(en='The dates of the booking are the important part. A toll is charged to whoever had '
             'the car at that minute, so the window decides who pays.',
          es='Las fechas de la reserva son lo importante. Un peaje se cobra a quien tenía el '
             'coche en ese minuto, así que la ventana decide quién paga.',
          cam=(0.5, 0.33, 1.10),
          hold=0.3),

        B(en='If you shorten a booking in HQ, the change comes across, and a toll that now falls '
             'outside the window stops belonging to that renter. Shorten one only when the car '
             'really came back early.',
          es='Si acorta una reserva en HQ, el cambio llega aquí, y un peaje que ahora queda fuera '
             'de la ventana deja de ser de ese cliente. Acorte una solo si el coche volvió '
             'de verdad antes.',
          cam=(0.5, 0.33, 1.10)),

        B(en='The people come across too. Whoever rents the car in HQ becomes a driver here.',
          es='Las personas también llegan. Quien alquila el coche en HQ se convierte en conductor '
             'aquí.',
          shot='hq-p-90-drivers', url='/users', cam=(0.5, 0.25, 1.02),
          label_en='Drivers', label_es='Conductores'),

        B(en='One person, one card, one history — however many bookings they have had with you.',
          es='Una persona, una tarjeta, un historial, por muchas reservas que haya tenido con '
             'usted.',
          cam=(0.42, 0.30, 1.22)),

        B(en='A driver the portal cannot match to anyone it knows waits for you on the drivers '
             'tab, so two people with the same name never quietly become one.',
          es='Un conductor que el portal no puede emparejar con nadie conocido le espera en la '
             'pestaña de conductores, para que dos personas con el mismo nombre nunca se '
             'conviertan en una sin que usted lo sepa.',
          shot='hq-p-53-pending', url='/p2p-bookings/hqrental', cam=(0.38, 0.115, 1.34),
          ring=(0.330, 0.088, 0.120, 0.046),
          label_en='Drivers awaiting review', label_es='Conductores por revisar'),

        B(en='It works the other way as well. A booking taken on your own site is written into '
             'HQ, with the car and the customer, so HQ stays the one place where the calendar '
             'lives.',
          es='También funciona al revés. Una reserva hecha en su propio sitio se escribe en HQ, '
             'con el coche y el cliente, para que HQ siga siendo el único sitio donde vive el '
             'calendario.',
          shot='hq-17-reservations', url='HQ · Car Rental › Reservations', cam=(0.5, 0.25, 1.04),
          label_en='HQ · Reservations', label_es='HQ · Reservations'),

        B(en='Which means you never have to remember which system a car is free in. There is only '
             'one answer, and both sides have it.',
          es='Lo que significa que nunca tiene que recordar en qué sistema está libre un coche. '
             'Solo hay una respuesta, y la tienen los dos lados.',
          cam=(0.5, 0.25, 1.04)),
    ])


# =============================================================================== 30
EP30 = E(
    30, 'hq-money',
    'HQ Rental Software, part 4: tolls, violations and the money',
    'HQ Rental Software, parte 4: peajes, multas y el dinero',
    'Where a toll goes after we find it, and what to do when something is missing',
    'Adónde va un peaje después de encontrarlo, y qué hacer si algo falta',
    [
        B(en='Here is the part the connection is really for. We find the tolls; HQ takes the '
             'money.',
          es='Esta es la parte para la que sirve de verdad la conexión. Nosotros encontramos los '
             'peajes; HQ cobra el dinero.',
          shot='hq-p-60-tolls', url='/payments/tolls', cam=(0.5, 0.22, 1.02),
          label_en='Tolls', label_es='Peajes'),

        B(en='A toll arrives from the toll agency, the portal finds the car by its tag, and the '
             'booking that was open at that minute tells it who was driving.',
          es='Un peaje llega de la agencia, el portal encuentra el coche por su etiqueta, y la '
             'reserva que estaba abierta en ese minuto le dice quién conducía.',
          cam=(0.5, 0.33, 1.16)),

        B(en='Then it goes back to HQ. On that reservation a line appears under External Charges '
             '— the amount, the date, the tag and the agency.',
          es='Después vuelve a HQ. En esa reserva aparece una línea en External Charges, cargos '
             'externos: el importe, la fecha, la etiqueta y la agencia.',
          shot='hq-16-external-charges', url='HQ · Car Rental › External Charges',
          cam=(0.5, 0.30, 1.08),
          label_en='HQ · External Charges', label_es='HQ · External Charges'),

        B(en='The receipt from the agency is attached to it, so the customer can be shown exactly '
             'what they are paying for.',
          es='El recibo de la agencia se adjunta, para poder enseñarle al cliente exactamente '
             'qué está pagando.',
          cam=(0.85, 0.35, 1.25),
          ring=(0.820, 0.255, 0.140, 0.545),
          label_en='Tag and agency', label_es='Etiqueta y agencia'),

        B(en='And the card HQ already holds for that reservation is charged. Paid means the money '
             'is in. Waiting Payment means it is not, yet.',
          es='Y se cobra la tarjeta que HQ ya tiene para esa reserva. Paid, pagado, significa que '
             'el dinero entró. Waiting Payment, en espera, que todavía no.',
          cam=(0.68, 0.38, 1.25),
          ring=(0.648, 0.262, 0.090, 0.550),
          label_en='Paid · Waiting Payment', label_es='Paid · Waiting Payment'),

        B(en='If the reservation has no card, HQ sends the customer a payment link instead. '
             'Nothing is lost — it is waiting for them to pay it.',
          es='Si la reserva no tiene tarjeta, HQ le envía al cliente un enlace de pago. No se '
             'pierde nada: queda esperando a que lo pague.',
          cam=(0.68, 0.38, 1.25)),

        B(en='Violations travel the same road: found here, charged there, with the notice '
             'attached.',
          es='Las multas siguen el mismo camino: se encuentran aquí, se cobran allí, con la '
             'notificación adjunta.',
          shot='hq-p-62-charges', url='/payments/charges', cam=(0.5, 0.22, 1.02),
          label_en='Charges', label_es='Cargos'),

        B(en='On your side, Charges is the ledger: every toll and every violation, what it cost, '
             'and whether it was collected.',
          es='En su lado, Cargos es el libro: cada peaje y cada multa, lo que costó, y si se '
             'cobró.',
          cam=(0.5, 0.35, 1.18)),

        B(en='Three things explain almost every case of "it is not there".',
          es='Tres cosas explican casi todos los casos de "no está".',
          cam=(0.5, 0.30, 1.06),
          hold=0.3),

        B(en='The booking is missing — press Get from HQ Rental Software on the bookings page '
             'rather than waiting for the hour to pass.',
          es='Falta la reserva: pulse Get from HQ Rental Software en la página de reservas en vez '
             'de esperar a que pase la hora.',
          shot='hq-p-50-bookings', url='/bookings', cam=(0.72, 0.10, 1.34),
          point=(0.757, 0.044), click=1.6,
          ring=(0.690, 0.030, 0.145, 0.030)),

        B(en='The toll is there but belongs to nobody — the car had no tag when the trip '
             'happened, or the dates of the booking do not cover it.',
          es='El peaje está pero no es de nadie: el coche no tenía etiqueta cuando se hizo el '
             'viaje, o las fechas de la reserva no lo cubren.',
          shot='hq-p-60-tolls', url='/payments/tolls', cam=(0.5, 0.33, 1.16)),

        B(en='Or the charge reached HQ and stayed unpaid — that one is a card question, and HQ '
             'is where it is answered.',
          es='O el cargo llegó a HQ y quedó sin pagar: eso es cosa de la tarjeta, y HQ es donde '
             'se resuelve.',
          shot='hq-16-external-charges', url='HQ · Car Rental › External Charges',
          cam=(0.68, 0.38, 1.25),
          ring=(0.648, 0.262, 0.090, 0.550)),

        B(en='Everything else runs without you. That is the whole of the HQ connection.',
          es='Todo lo demás funciona sin usted. Eso es toda la conexión con HQ.',
          shot='hq-p-50-bookings', url='/bookings', cam=(0.5, 0.22, 1.0)),
    ])
