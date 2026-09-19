# -*- coding: utf-8 -*-
"""Episodes 18 and 19 — bookings that arrive from a platform, and the storefront."""
from model import B, E


# =============================================================================== 18
EP18 = E(
    18, 'platform-bookings',
    'Bookings that arrive from a platform', 'Reservas que llegan de una plataforma',
    'Confirming, reviewing drivers, and matching cars you never entered',
    'Confirmar, revisar conductores, y emparejar coches que nunca introdujo',
    [
        B(en='If your cars are also listed on a peer-to-peer platform, the bookings arrive '
             'here rather than being typed in — and they arrive needing a decision.',
          es='Si sus coches también están listados en una plataforma entre particulares, las '
             'reservas llegan aquí en vez de teclearse, y llegan pidiendo una decisión.',
          shot='53-pending-bookings', url='/p2p-bookings', cam=(0.5, 0.30, 1.0),
          label_en='Pending bookings', label_es='Reservas pendientes'),

        B(en='Four tabs, and each is a queue of something waiting for you. Bookings awaiting '
             'confirmation is the first, and the count in the tab is the size of the queue.',
          es='Cuatro pestañas, y cada una es una cola de algo que le espera. Reservas '
             'pendientes de confirmación es la primera, y el número de la pestaña es el '
             'tamaño de la cola.',
          cam=(0.42, 0.24, 1.22),
          ring={'en': (0.217, 0.203, 0.524, 0.047),
                'es': (0.217, 0.203, 0.508, 0.047)}),

        B(en='Each row is a real reservation with a real number, the vehicle, the trip dates '
             'and the guest.',
          es='Cada fila es una reserva real con su número, el vehículo, las fechas del viaje '
             'y el huésped.',
          cam=(0.50, 0.36, 1.18),
          ring=(0.217, 0.300, 0.752, 0.112)),

        B(en='Match is the column to read before you press anything. "Car: None" means we '
             'have not worked out which of your vehicles this is. "Driver: None" means the '
             'guest is not yet one of your drivers.',
          es='Coincidencia es la columna que hay que leer antes de pulsar nada. "Coche: '
             'ninguno" significa que no hemos deducido cuál de sus vehículos es este. '
             '"Conductor: ninguno" significa que el huésped aún no es uno de sus conductores.',
          cam=(0.70, 0.35, 1.28),
          ring={'en': (0.646, 0.321, 0.092, 0.028),
                'es': (0.611, 0.338, 0.120, 0.028)},
          label_en='Match', label_es='Coincidencia'),

        B(en='Confirming with no car matched creates a booking with nothing to attach tolls '
             'to — which is exactly the "no driver assigned" case from episode twelve. Match '
             'first, confirm second.',
          es='Confirmar sin coche emparejado crea una reserva sin nada a lo que enganchar los '
             'peajes, que es exactamente el caso de "sin conductor asignado" del episodio '
             'doce. Primero empareje, después confirme.',
          cam=(0.84, 0.35, 1.28),
          point={'en': (0.877, 0.335), 'es': (0.871, 0.352)}, click=1.9,
          ring={'en': (0.842, 0.321, 0.120, 0.028),
                'es': (0.841, 0.338, 0.121, 0.028)}),

        B(en='Drivers awaiting review is the second queue, and it is where the matching '
             'actually happens.',
          es='Conductores pendientes de revisión es la segunda cola, y es donde ocurre el '
             'emparejamiento de verdad.',
          shot='54-pending-drivers', cam=(0.5, 0.35, 1.02),
          point={'en': (0.476, 0.226), 'es': (0.435, 0.226)}, click=1.3,
          label_en='Drivers awaiting review', label_es='Conductores pendientes'),

        B(en='Reason says why the row is here. "New driver" means we have never seen this '
             'person and approving creates them.',
          es='Motivo dice por qué está la fila aquí. "Conductor nuevo" significa que nunca '
             'hemos visto a esta persona y aprobar la crea.',
          cam=(0.74, 0.45, 1.24),
          ring=(0.706, 0.282, 0.102, 0.480),
          label_en='Reason', label_es='Motivo'),

        B(en='"Fuzzy match" is the one to slow down on: the system thinks this guest is '
             'probably an existing driver of yours, and the Candidate column names who. '
             'Approving merges them; approving the wrong one merges two different people.',
          es='"Coincidencia aproximada" es la que hay que mirar despacio: el sistema cree que '
             'este huésped es probablemente un conductor que usted ya tiene, y la columna '
             'Candidato dice quién. Aprobar los fusiona; aprobar al equivocado fusiona a dos '
             'personas distintas.',
          cam=(0.60, 0.51, 1.28),
          ring=(0.476, 0.497, 0.332, 0.032),
          label_en='Fuzzy match', label_es='Coincidencia aproximada'),

        B(en='These pile up, and they do not expire. Every one of them is a booking that '
             'cannot bill anybody until it is cleared.',
          es='Estos se acumulan y no caducan. Cada uno es una reserva que no puede facturar a '
             'nadie hasta que se resuelva.',
          cam=(0.30, 0.79, 1.24)),

        B(en='The third tab lists the cars in your own fleet that came from the platform, '
             'with their plates and VINs — so you can check what is already in.',
          es='La tercera pestaña enumera los coches de su propia flota que vinieron de la '
             'plataforma, con sus matrículas y VIN, para que compruebe lo que ya está dentro.',
          shot='55-pending-platform-cars', cam=(0.5, 0.45, 1.02),
          point={'en': (0.604, 0.226), 'es': (0.574, 0.226)}, click=1.4,
          ring=(0.217, 0.336, 0.744, 0.042),
          label_en='Platform cars', label_es='Coches de la plataforma'),

        B(en='The pencil only opens the car’s own page. To tie a listing to a car, tick '
             '"Remember this listing" when you confirm a booking, or use Import cars under '
             'Settings, Turo Agents. Do it once and the bookings that follow match themselves.',
          es='El lápiz solo abre la ficha del coche. Para atar un anuncio a un coche, marque '
             '"Recordar este anuncio" al confirmar una reserva, o use Importar vehículos en '
             'Configuración, Agentes de Turo. Hágalo una vez y las reservas que vengan '
             'después se emparejan solas.',
          cam=(0.32, 0.42, 1.30),
          point=(0.258, 0.403), click=1.4),

        B(en='And History is everything already dealt with — Confirmed, and AutoCancelled '
             'where the platform withdrew the request before anyone got to it.',
          es='E Historial es todo lo ya resuelto: Confirmadas, y Autocanceladas cuando la '
             'plataforma retiró la solicitud antes de que nadie llegara a ella.',
          shot='56-pending-history', cam=(0.5, 0.45, 1.02),
          point={'en': (0.703, 0.221), 'es': (0.680, 0.221)}, click=1.4,
          ring={'en': (0.384, 0.384, 0.078, 0.404), 'es': (0.372, 0.384, 0.086, 0.404)},
          label_en='History', label_es='Historial'),

        B(en='All of them, searchable by trip start date — which is '
             'how you find the booking behind a toll that arrived three weeks late.',
          es='Todas, con búsqueda por fecha de inicio del viaje, que es como '
             'se encuentra la reserva detrás de un peaje que llegó tres semanas tarde.',
          cam=(0.36, 0.29, 1.26),
          point=(0.35, 0.291), click=1.5,
          ring=(0.257, 0.270, 0.189, 0.039)),
    ])


# =============================================================================== 19
EP19 = E(
    19, 'storefront',
    'Your storefront, and the messages that go out', 'Su sitio, y los mensajes que salen',
    'How the fleet is shown, and every message the system has sent',
    'Cómo se muestra la flota, y cada mensaje que el sistema ha enviado',
    [
        B(en='Storefront Design. This is the public face of your fleet — the page a renter '
             'actually sees.',
          es='Diseño del sitio. Esta es la cara pública de su flota: la página que ve de '
             'verdad un arrendatario.',
          shot='92-storefront-design', url='/storefront', cam=(0.5, 0.30, 1.0),
          label_en='Storefront Design', label_es='Diseño del sitio'),

        B(en='Read this line before you type anything: you are editing in English, and the '
             'content is translated into every other language automatically when you save. '
             'You write once.',
          es='Lea esta línea antes de escribir nada: está editando en inglés, y el contenido '
             'se traduce a todos los demás idiomas automáticamente al guardar. Usted escribe '
             'una vez.',
          cam=(0.34, 0.22, 1.26),
          ring=(0.214, 0.207, 0.314, 0.024),
          label_en='Written once, translated', label_es='Se escribe una vez'),

        B(en='Six tabs. Design is colours and logo, Content and About are your words, Terms '
             'is your rental terms, and Languages picks which ones the storefront offers.',
          es='Seis pestañas. Diseño son colores y logo, Contenido y Acerca de son sus '
             'palabras, Términos son sus condiciones de alquiler, e Idiomas elige cuáles '
             'ofrece el sitio.',
          cam=(0.42, 0.30, 1.22),
          ring=(0.232, 0.271, 0.402, 0.049)),

        B(en='Main holds the single decision that changes the shape of the whole site: how '
             'the fleet is listed.',
          es='Principal contiene la única decisión que cambia la forma de todo el sitio: cómo '
             'se lista la flota.',
          cam=(0.5, 0.42, 1.16),
          point=(0.256, 0.295), click=1.2,
          label_en='How to show your vehicles', label_es='Cómo mostrar sus vehículos'),

        B(en='By models gives one card per make and model. Four identical Camrys become one '
             'listing — cleaner, and right when the renter does not care which particular car '
             'they get.',
          es='Por modelos da una tarjeta por marca y modelo. Cuatro Camry idénticos se '
             'convierten en un anuncio: más limpio, y acertado cuando al arrendatario le da '
             'igual qué coche concreto le toque.',
          cam=(0.32, 0.46, 1.26),
          ring=(0.232, 0.403, 0.237, 0.111)),

        B(en='By cars gives every vehicle its own card. Right for a fleet where the cars '
             'genuinely differ — different mileage, different trim, different photographs.',
          es='Por coches da a cada vehículo su propia tarjeta. Acertado para una flota donde '
             'los coches de verdad se diferencian: distinto kilometraje, distinto acabado, '
             'distintas fotos.',
          cam=(0.60, 0.46, 1.26),
          ring=(0.475, 0.403, 0.237, 0.111)),

        B(en='And Both lets the visitor switch between the two views themselves, which is the '
             'safe default when you are not sure.',
          es='Y Ambos deja que el visitante cambie entre las dos vistas, que es la opción '
             'segura cuando no está seguro.',
          cam=(0.86, 0.46, 1.26),
          point=(0.741, 0.442), click=1.4,
          ring=(0.719, 0.403, 0.237, 0.111),
          label_en='Both', label_es='Ambos'),

        B(en='Save, and the storefront changes for everyone immediately.',
          es='Guarde, y el sitio cambia para todos de inmediato.',
          cam=(0.82, 0.17, 1.28),
          point=(0.942, 0.164), click=1.2),

        B(en='Then SMS and Mail. Email is a real mailbox — the relay alias you set up in '
             'episode two, with an inbox and a sent folder.',
          es='Después, SMS y Correo. Correo es un buzón de verdad: el alias de reenvío que '
             'configuró en el episodio dos, con bandeja de entrada y de enviados.',
          shot='93-messages', url='/messages', cam=(0.5, 0.45, 1.0),
          label_en='Email', label_es='Correo'),

        B(en='Thousands of messages on this account, and Compose sends from your alias, so '
             'the driver sees your company and never your personal address.',
          es='Miles de mensajes en esta cuenta, y Redactar envía desde su alias, así que el '
             'conductor ve su empresa y nunca su dirección personal.',
          cam=(0.78, 0.17, 1.24),
          point=(0.928, 0.158), click=1.4,
          ring=(0.805, 0.140, 0.168, 0.038)),

        B(en='And the SMS and QR Log is every text the system has sent on your behalf.',
          es='Y el registro de SMS y QR es cada mensaje de texto que el sistema ha enviado en '
             'su nombre.',
          shot='94-sms-log', url='/sms-log', cam=(0.5, 0.42, 1.0),
          label_en='SMS & QR Log', label_es='Registro de SMS y QR'),

        B(en='Purpose says what it was for — a booking confirmation, an agreement, a '
             'registration. Status says whether it arrived.',
          es='Propósito dice para qué era: una confirmación de reserva, un contrato, un '
             'registro. Estado dice si llegó.',
          cam=(0.55, 0.55, 1.24),
          ring=(0.470, 0.336, 0.230, 0.430),
          label_en='Purpose and status', label_es='Propósito y estado'),

        B(en='Read the Error column even on a successful row. "No SMS consent — QR fallback" '
             'means the message went out as a QR code instead of a text, because that person '
             'has not agreed to receive SMS. It worked, but not the way you expected.',
          es='Lea la columna de Error incluso en una fila correcta. "Sin consentimiento de SMS '
             '— alternativa QR" significa que el mensaje salió como código QR en vez de texto, '
             'porque esa persona no ha aceptado recibir SMS. Funcionó, pero no como esperaba.',
          cam=(0.78, 0.60, 1.26),
          ring=(0.750, 0.585, 0.140, 0.030),
          label_en='Read the Error column', label_es='Lea la columna de Error'),

        B(en='Every one of them is here. When a driver says they were never told, this is the '
             'page that answers.',
          es='Todos están aquí. Cuando un conductor dice que nunca le avisaron, esta es la '
             'página que responde.',
          cam=(0.32, 0.81, 1.22),
          ring=(0.216, 0.802, 0.180, 0.030)),
    ])
