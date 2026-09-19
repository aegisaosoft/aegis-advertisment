# -*- coding: utf-8 -*-
"""Episodes 6 to 8 — transponders, prices, and the booking screen."""
from model import B, E


# =============================================================================== 06
EP06 = E(
    6, 'transponders',
    'Transponders — the step nobody should skip', 'Transpondedores: el paso que nadie debe saltarse',
    'A tag with no vehicle behind it cannot be billed to anyone',
    'Una etiqueta sin vehículo detrás no se le puede cobrar a nadie',
    [
        B(en='Open a toll account from Tolls and Violations and you get its own page: every '
             'vehicle and every transponder the agency holds for you.',
          es='Abra una cuenta de peaje desde Peajes y Multas y obtiene su propia página: '
             'cada vehículo y cada transpondedor que la agencia guarda para usted.',
          shot='25-toll-account-vehicles', url='/toll-provider', cam=(0.5, 0.35, 1.0),
          label_en='A toll provider account', label_es='Una cuenta de proveedor'),

        B(en='Two tabs. Vehicles is what the agency thinks you own. Transponders is the '
             'tags it has issued. The counts rarely match, and the gap between them is what '
             'this episode is about.',
          es='Dos pestañas. Vehículos es lo que la agencia cree que usted tiene. '
             'Transpondedores son las etiquetas que ha emitido. Los recuentos casi nunca '
             'coinciden, y ese hueco es de lo que trata este episodio.',
          cam=(0.34, 0.30, 1.22),
          ring=(0.204, 0.277, 0.200, 0.044)),

        B(en='Why it matters: a toll is billed to whoever was driving. The agency tells you '
             'a tag went through a gantry. Only the tag-to-vehicle link turns that into a '
             'car, and only a car has a booking, and only a booking has a driver with a card.',
          es='Por qué importa: un peaje se le cobra a quien iba conduciendo. La agencia le '
             'dice que una etiqueta pasó por un pórtico. Solo el enlace etiqueta-vehículo '
             'convierte eso en un coche; solo un coche tiene reserva, y solo una reserva '
             'tiene un conductor con tarjeta.',
          cam=(0.5, 0.35, 1.0)),

        B(en='So this legend is the most useful row on the page. Linked is done. No '
             'transponder in DB means the agency knows the car but we hold no tag for it. '
             'Transponder differs from DB means the two disagree and one of them is stale.',
          es='Por eso esta leyenda es la fila más útil de la página. Enlazado está listo. Sin '
             'transpondedor en la base significa que la agencia conoce el coche pero no '
             'tenemos etiqueta. El transpondedor difiere significa que ambos discrepan y uno '
             'está desactualizado.',
          cam=(0.42, 0.36, 1.26),
          ring=(0.204, 0.344, 0.432, 0.022),
          label_en='The five statuses', label_es='Los cinco estados'),

        B(en='No provider assigned means the car exists here but has no toll agency attached '
             'to it — that is the Toll Systems row from episode five. Not in DB means the '
             'agency has a vehicle we have never heard of.',
          es='Sin proveedor asignado significa que el coche existe aquí pero no tiene agencia '
             'de peaje enganchada: es la fila Sistemas de peaje del episodio cinco. No está '
             'en la base significa que la agencia tiene un vehículo del que nunca hemos oído.',
          cam=(0.60, 0.36, 1.26),
          ring=(0.478, 0.344, 0.158, 0.022)),

        B(en='The Status column repeats it per row, so you can work down the list and see '
             'exactly which cars are earning you nothing.',
          es='La columna Estado lo repite fila a fila, así que puede bajar por la lista y ver '
             'exactamente qué coches no le están dando nada.',
          cam=(0.32, 0.60, 1.24),
          ring=(0.272, 0.414, 0.106, 0.430),
          label_en='Status, per vehicle', label_es='Estado, por vehículo'),

        B(en='And the Transponder column on the right is the answer: filled in, that car can '
             'be billed. Empty, a toll from it arrives with nobody to charge and lands on you.',
          es='Y la columna Transpondedor de la derecha es la respuesta: rellena, ese coche se '
             'puede facturar. Vacía, un peaje suyo llega sin nadie a quien cobrar y acaba en '
             'usted.',
          cam=(0.80, 0.60, 1.24),
          ring=(0.766, 0.414, 0.124, 0.430),
          label_en='Transponder', label_es='Transpondedor'),

        B(en='Now the trap. This banner is telling you the transponder list is served from a '
             'cache, and it names the moment it was last read from the agency.',
          es='Ahora la trampa. Este aviso le dice que la lista de transpondedores viene de una '
             'caché, y nombra el momento en que se leyó por última vez de la agencia.',
          cam=(0.5, 0.21, 1.24),
          ring=(0.203, 0.181, 0.786, 0.069),
          label_en='The list is cached', label_es='La lista está en caché'),

        B(en='Any tag the agency issued after that time is simply not in this list. So when '
             'you are sure a transponder exists and cannot find it here, the list is old — it '
             'is not missing.',
          es='Cualquier etiqueta emitida por la agencia después de ese momento sencillamente '
             'no está en esta lista. Así que cuando esté seguro de que un transpondedor existe '
             'y no lo encuentre aquí, la lista está vieja: no es que falte.',
          cam=(0.5, 0.21, 1.24), hold=0.4),

        B(en='Refresh Vehicles and Transponders List goes back to the agency and reads it '
             'again. Press it before you conclude that anything is wrong.',
          es='Actualizar lista de vehículos y transpondedores vuelve a la agencia y la lee de '
             'nuevo. Púlselo antes de concluir que algo está mal.',
          cam=(0.80, 0.13, 1.24),
          point=(0.880, 0.134), click=1.6,
          ring=(0.769, 0.113, 0.223, 0.041),
          label_en='Refresh', label_es='Actualizar'),

        B(en='It takes a while, and it says so — it loads the vehicles first and then walks '
             'the full transponder inventory behind them.',
          es='Tarda un rato, y lo dice: primero carga los vehículos y después recorre el '
             'inventario completo de transpondedores.',
          shot='26-toll-account-transponders', cam=(0.5, 0.21, 1.20),
          ring=(0.203, 0.182, 0.786, 0.063)),

        B(en='Do this once for every toll account, on your first day, and again whenever the '
             'agency posts you a new tag. Skip it, and the tolls still arrive — they simply '
             'arrive addressed to you instead of to the driver.',
          es='Haga esto una vez por cada cuenta de peaje, en su primer día, y otra vez cada '
             'vez que la agencia le envíe una etiqueta nueva. Sáltelo, y los peajes siguen '
             'llegando: solo que llegan a su nombre en vez de al del conductor.',
          shot='25-toll-account-vehicles', cam=(0.5, 0.35, 1.0),
          label_en=' ', label_es=' '),
    ])


# =============================================================================== 07
EP07 = E(
    7, 'rates',
    'Rates and pricing seasons', 'Tarifas y temporadas de precios',
    'Price a whole category at once, then price the busy weeks differently',
    'Ponga precio a toda una categoría, y luego cobre distinto las semanas fuertes',
    [
        B(en='Vehicles, then Rates. This page prices your fleet without opening a single '
             'vehicle.',
          es='Vehículos, y luego Tarifas. Esta página pone precio a su flota sin abrir un '
             'solo vehículo.',
          shot='19-rates', url='/rates', cam=(0.5, 0.40, 1.0),
          label_en='Vehicles → Rates', label_es='Vehículos → Tarifas'),

        B(en='First choose which rate you are setting: daily, weekly or monthly. They are '
             'three separate prices, and the toggle changes every figure on the page.',
          es='Primero elija qué tarifa está fijando: diaria, semanal o mensual. Son tres '
             'precios distintos, y este selector cambia todas las cifras de la página.',
          cam=(0.80, 0.16, 1.28),
          point={'en': (0.874, 0.157), 'es': (0.870, 0.157)}, click=1.5,
          ring=(0.781, 0.138, 0.192, 0.037),
          label_en='Daily · Weekly · Monthly', label_es='Diaria · Semanal · Mensual'),

        B(en='The list underneath is your fleet grouped by category — Economic, Luxury, '
             'Premium, Sports, SUV — and each group opens into makes, models and finally '
             'individual cars.',
          es='La lista de abajo es su flota agrupada por categoría — Económico, Lujo, Premium, '
             'Deportivo, SUV — y cada grupo se abre en marcas, modelos y por fin coches '
             'concretos.',
          cam=(0.5, 0.50, 1.10),
          ring=(0.232, 0.305, 0.725, 0.410)),

        B(en='Read the figure before the box. A number means every car under that group is '
             'already at that price. The word "different" means they are not, and setting a '
             'value here will overwrite all of them.',
          es='Lea la cifra antes de la casilla. Un número significa que todos los coches de '
             'ese grupo ya están a ese precio. La palabra "diferente" significa que no, y '
             'poner un valor aquí los sobrescribirá todos.',
          cam=(0.80, 0.41, 1.30),
          ring=(0.782, 0.394, 0.048, 0.034),
          label_en='"different" is a warning', label_es='"diferente" es un aviso'),

        B(en='Type the new rate and press Apply, and it is written down to every car under '
             'that heading in one go.',
          es='Escriba la nueva tarifa y pulse Aplicar, y se escribe en todos los coches bajo '
             'ese encabezado de una sola vez.',
          cam=(0.86, 0.41, 1.32),
          point=(0.859, 0.410), click=1.3,
          ring=(0.827, 0.392, 0.062, 0.036)),

        B(en='Open a group first if you only meant one model. Applying at the top of a '
             'category is fast, and it is also the fastest way to reprice a car you did not '
             'mean to touch.',
          es='Abra el grupo primero si solo quería un modelo. Aplicar en lo alto de una '
             'categoría es rápido, y también es la forma más rápida de cambiar el precio de '
             'un coche que no quería tocar.',
          cam=(0.30, 0.34, 1.28),
          point=(0.254, 0.336), click=1.4),

        B(en='Then Pricing Seasons, which is the same idea over a date range.',
          es='Después, Temporadas de precios, que es la misma idea sobre un rango de fechas.',
          shot='20-pricing-seasons', url='/pricing-seasons', cam=(0.5, 0.30, 1.06),
          label_en='Pricing Seasons', label_es='Temporadas de precios'),

        B(en='A season is a name, a start, an end and a priority. Where two seasons overlap, '
             'the higher priority wins — that is how a holiday week sits inside a summer '
             'season and charges more.',
          es='Una temporada es un nombre, un inicio, un fin y una prioridad. Donde dos '
             'temporadas se solapan, gana la de mayor prioridad: así es como una semana de '
             'fiesta vive dentro de la temporada de verano y cobra más.',
          cam=(0.5, 0.34, 1.20),
          ring=(0.287, 0.263, 0.614, 0.169)),

        B(en='Add season, and it appears in this table.',
          es='Añadir temporada, y aparece en esta tabla.',
          cam=(0.76, 0.29, 1.28),
          point=(0.842, 0.293), click=1.1,
          ring=(0.799, 0.275, 0.087, 0.035)),

        B(en='Then pick the season here and price it exactly the way you priced the base '
             'rates: by category, by make, by model, or one car.',
          es='Luego elija la temporada aquí y póngale precio igual que puso las tarifas base: '
             'por categoría, por marca, por modelo, o por un solo coche.',
          cam=(0.44, 0.51, 1.26),
          point=(0.44, 0.505), click=1.4,
          ring=(0.369, 0.487, 0.146, 0.037),
          label_en='Car season prices', label_es='Precios de temporada'),

        B(en='The rule at the bottom is worth reading twice: leave a tier blank and that '
             'period falls back to the car’s base price. Blank is not zero.',
          es='La regla del final merece leerse dos veces: deje un nivel en blanco y ese '
             'período vuelve al precio base del coche. En blanco no es cero.',
          cam=(0.5, 0.735, 1.28),
          ring=(0.298, 0.732, 0.514, 0.024)),

        B(en='Which season applies is decided by the rental start date, not by the day the '
             'booking was made. A booking taken in April for August is priced as August.',
          es='Qué temporada se aplica lo decide la fecha de inicio del alquiler, no el día en '
             'que se hizo la reserva. Una reserva hecha en abril para agosto se cobra como '
             'agosto.',
          cam=(0.5, 0.20, 1.20),
          ring=(0.288, 0.170, 0.610, 0.040), label_en=' ', label_es=' '),
    ])


# =============================================================================== 08
EP08 = E(
    8, 'bookings',
    'The booking screen', 'La pantalla de reservas',
    'Two views of the same bookings, and ten actions on every row',
    'Dos vistas de las mismas reservas, y diez acciones en cada fila',
    [
        B(en='Bookings. Every reservation you have, in a list.',
          es='Reservas. Todas las reservas que tiene, en una lista.',
          shot='50-bookings', url='/bookings', cam=(0.5, 0.45, 1.0),
          label_en='Bookings', label_es='Reservas'),

        B(en='The status filter starts with eight statuses selected, not all of them. If a '
             'booking you know exists is not on this page, open that filter before you '
             'conclude anything.',
          es='El filtro de estado empieza con ocho estados seleccionados, no todos. Si una '
             'reserva que sabe que existe no está en esta página, abra ese filtro antes de '
             'concluir nada.',
          cam=(0.34, 0.22, 1.26),
          point=(0.279, 0.219), click=1.5,
          ring=(0.216, 0.199, 0.126, 0.036),
          label_en='Eight of the statuses', label_es='Ocho de los estados'),

        B(en='Two tabs: List and Scheduler. Same bookings, two ways of looking at them.',
          es='Dos pestañas: Lista y Planificador. Las mismas reservas, dos formas de verlas.',
          cam=(0.28, 0.30, 1.26),
          ring=(0.204, 0.276, 0.108, 0.046)),

        B(en='In the list, three columns carry the whole story. Rental Agreement shows '
             'whether the contract is signed, sent, or not needed.',
          es='En la lista, tres columnas cuentan toda la historia. Contrato de alquiler '
             'muestra si está firmado, enviado, o si no hace falta.',
          cam=(0.36, 0.55, 1.22),
          ring=(0.306, 0.366, 0.080, 0.424),
          label_en='Rental Agreement', label_es='Contrato de alquiler'),

        B(en='Status is the booking’s own state: Approved, Completed, Completed Early, '
             'Waiting for Card.',
          es='Estado es el estado propio de la reserva: Aprobada, Completada, Completada '
             'antes de tiempo, Esperando tarjeta.',
          cam=(0.44, 0.55, 1.22),
          ring=(0.386, 0.366, 0.082, 0.424),
          label_en='Status', label_es='Estado'),

        B(en='And Toll Payments is the money: Succeeded, Failed, Not charged, Payment stuck. '
             'This is the column to scan every morning.',
          es='Y Pagos de peaje es el dinero: Correcto, Fallido, Sin cobrar, Pago atascado. '
             'Esta es la columna que hay que repasar cada mañana.',
          cam=(0.54, 0.55, 1.22),
          ring=(0.483, 0.366, 0.084, 0.424),
          label_en='Toll Payments', label_es='Pagos de peaje'),

        B(en='A row like this one says it plainly: waiting for a card, nothing charged, and '
             'one condition still unmet. Nothing about that booking will collect money until '
             'it is fixed.',
          es='Una fila como esta lo dice claro: esperando tarjeta, nada cobrado, y una '
             'condición aún sin cumplir. Esa reserva no cobrará nada hasta que se arregle.',
          cam=(0.45, 0.60, 1.30),
          ring=(0.386, 0.575, 0.184, 0.048)),

        B(en='The three dots on a row open everything you can do to that booking.',
          es='Los tres puntos de una fila abren todo lo que puede hacerle a esa reserva.',
          cam=(0.28, 0.60, 1.28),
          point=(0.242, 0.601), click=1.2),

        B(en='It opens with the booking itself written at the top — who, which car, the '
             'dates, the status — so you never act on the wrong row.',
          es='Se abre con la reserva escrita arriba — quién, qué coche, las fechas, el estado '
             '— para que nunca actúe sobre la fila equivocada.',
          shot='52-booking-row-menu', cam=(0.47, 0.45, 1.26),
          ring=(0.368, 0.398, 0.204, 0.100),
          label_en='The row menu', label_es='El menú de la fila'),

        B(en='Change Car moves this booking onto a different vehicle. Reopen Booking brings a '
             'finished one back. Both of them move tolls with them, so use them deliberately.',
          es='Cambiar coche mueve esta reserva a otro vehículo. Reabrir reserva devuelve una '
             'terminada. Ambas arrastran los peajes consigo, así que úselas a conciencia.',
          cam=(0.47, 0.545, 1.28),
          point=(0.42, 0.520),
          ring=(0.368, 0.500, 0.204, 0.090)),

        B(en='Charges, Booking Info, View Tolls and View Violations are the read-only ones — '
             'what this booking has been billed, and why.',
          es='Cargos, Información de la reserva, Ver peajes y Ver multas son las de solo '
             'lectura: qué se le ha facturado a esta reserva, y por qué.',
          cam=(0.47, 0.660, 1.28),
          point=(0.42, 0.646),
          ring=(0.368, 0.592, 0.204, 0.176)),

        B(en='Create Invoice takes the unpaid tolls on this booking and turns them into one '
             'invoice for the driver — the tool for when the card is gone and the tolls are '
             'not.',
          es='Crear factura toma los peajes impagados de esta reserva y los convierte en una '
             'sola factura para el conductor: la herramienta para cuando la tarjeta ya no '
             'está y los peajes sí.',
          cam=(0.47, 0.718, 1.30),
          point=(0.42, 0.718),
          ring=(0.368, 0.700, 0.204, 0.038),
          label_en='Create Invoice', label_es='Crear factura'),

        B(en='Charge booking bills it now. Rental Agreement sends or re-sends the contract. '
             'Ten actions, and none of them need a different screen.',
          es='Cobrar reserva la factura ahora. Contrato de alquiler envía o reenvía el '
             'contrato. Diez acciones, y ninguna necesita otra pantalla.',
          cam=(0.47, 0.852, 1.28),
          point=(0.42, 0.835),
          ring=(0.368, 0.816, 0.204, 0.076)),

        B(en='The Scheduler is the same bookings drawn against time — one row per vehicle, '
             'one bar per booking.',
          es='El Planificador son las mismas reservas dibujadas contra el tiempo: una fila '
             'por vehículo, una barra por reserva.',
          shot='51-bookings-scheduler', cam=(0.5, 0.50, 1.02),
          point=(0.277, 0.264), click=1.4,
          label_en='Scheduler', label_es='Planificador'),

        B(en='The red line is today. A gap on a row is a car sitting idle, and a bar running '
             'past the right edge is a booking that has not ended yet.',
          es='La línea roja es hoy. Un hueco en una fila es un coche parado, y una barra que '
             'se sale por la derecha es una reserva que aún no ha terminado.',
          cam=(0.52, 0.50, 1.16),
          ring=(0.341, 0.324, 0.634, 0.041)),

        B(en='And the colours at the bottom are the same statuses as the list. Whichever view '
             'you prefer, you are reading the same four words.',
          es='Y los colores de abajo son los mismos estados de la lista. Prefiera la vista que '
             'prefiera, está leyendo las mismas cuatro palabras.',
          cam=(0.32, 0.855, 1.24),
          ring=(0.218, 0.856, 0.294, 0.024)),
    ])
