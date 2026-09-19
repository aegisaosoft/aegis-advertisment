# -*- coding: utf-8 -*-
"""Episodes 3 to 5 — the toll agencies, the vehicle list, and getting cars into it."""
from model import B, E


# =============================================================================== 03
EP03 = E(
    3, 'toll-accounts',
    'Connecting your toll agencies', 'Conectar sus agencias de peaje',
    'The credentials that let the system collect tolls without you',
    'Las credenciales con las que el sistema cobra peajes sin usted',
    [
        B(en='Company, Settings, and the Toll Accounts tab. This is where you hand the '
             'system the logins it uses to collect your tolls.',
          es='Compañía, Configuración, y la pestaña Cuentas de peaje. Aquí le entrega al '
             'sistema las credenciales con las que recoge sus peajes.',
          shot='31-settings-toll-accounts', url='/owners/settings', cam=(0.5, 0.30, 1.0),
          point=(0.520, 0.199), click=1.6,
          label_en='Settings → Toll Accounts', label_es='Configuración → Cuentas de peaje'),

        B(en='Understand what it is doing first. It signs in to each agency portal on your '
             'behalf, on a schedule, and downloads the tolls your vehicles ran up. There is '
             'no feed and no API — it is the same website you would open yourself.',
          es='Primero entienda qué hace. Entra en el portal de cada agencia en su nombre, '
             'de forma programada, y descarga los peajes que acumularon sus vehículos. No '
             'hay ningún feed ni API: es el mismo sitio web que usted abriría a mano.',
          cam=(0.5, 0.30, 1.0)),

        B(en='Toll Network Coverage at the top shows one chip per network, with a tick when '
             'you have credentials for it. One E-ZPass account covers all eighteen-plus '
             'E-ZPass agencies — do not create one per state.',
          es='Cobertura de red de peaje, arriba, muestra un chip por red, con una marca '
             'cuando usted tiene credenciales. Una sola cuenta E-ZPass cubre las más de '
             'dieciocho agencias E-ZPass: no cree una por estado.',
          cam=(0.5, 0.34, 1.06),
          ring=(0.203, 0.250, 0.783, 0.228),
          label_en='Toll Network Coverage', label_es='Cobertura de red de peaje'),

        B(en='To add one, press Add Account.',
          es='Para añadir una, pulse Añadir cuenta.',
          cam=(0.72, 0.29, 1.22),
          point=(0.921, 0.293), click=1.1,
          ring=(0.869, 0.276, 0.101, 0.034)),

        B(en='Choose the provider, then give it a nickname if you keep more than one '
             'account with the same agency. The nickname is only for you.',
          es='Elija el proveedor, y póngale un apodo si mantiene más de una cuenta con la '
             'misma agencia. El apodo es solo para usted.',
          shot='32-settings-add-toll-account', cam=(0.5, 0.40, 1.20),
          point=(0.42, 0.381), click=1.5,
          ring=(0.348, 0.363, 0.146, 0.036),
          label_en='Add Toll Account', label_es='Añadir cuenta de peaje'),

        B(en='Account number, login, password — exactly the ones you use on the agency '
             'site. The account number is optional; some agencies do not use one.',
          es='Número de cuenta, usuario y contraseña: exactamente los que usa en el sitio '
             'de la agencia. El número de cuenta es opcional; algunas agencias no lo usan.',
          cam=(0.5, 0.53, 1.24),
          ring=(0.348, 0.499, 0.305, 0.045)),

        B(en='The password is stored encrypted and is never shown back to you, or to '
             'support, in plain text.',
          es='La contraseña se guarda cifrada y nunca se le muestra de vuelta, ni a usted '
             'ni al soporte, en texto claro.',
          cam=(0.45, 0.62, 1.26),
          ring=(0.348, 0.610, 0.145, 0.042)),

        B(en='Save, and the account appears as a card.',
          es='Guarde, y la cuenta aparece como una tarjeta.',
          cam=(0.55, 0.68, 1.24),
          point=(0.617, 0.694), click=1.0,
          ring=(0.584, 0.674, 0.068, 0.038)),

        B(en='Each card carries a row of small icons on the right, and two of them are the '
             'ones you will actually use.',
          es='Cada tarjeta lleva una fila de iconos pequeños a la derecha, y dos de ellos '
             'son los que de verdad usará.',
          shot='31-settings-toll-accounts', cam=(0.42, 0.54, 1.28),
          ring=(0.203, 0.501, 0.385, 0.070),
          label_en='One card per account', label_es='Una tarjeta por cuenta'),

        B(en='The lightning bolt is Test connection. Press it now, while you are sitting '
             'here, rather than finding out in three weeks that nothing was collected.',
          es='El rayo es Probar conexión. Púlselo ahora, mientras está aquí, en vez de '
             'descubrir en tres semanas que no se recogió nada.',
          cam=(0.52, 0.54, 1.34),
          point=(0.506, 0.536), click=1.6,
          ring=(0.497, 0.522, 0.020, 0.028),
          label_en='Test connection', label_es='Probar conexión'),

        B(en='The shield is Verify device. The first time the system signs in from a new '
             'machine, most agencies email a code — press the shield and enter it, and '
             'unattended collection can carry on without you.',
          es='El escudo es Verificar dispositivo. La primera vez que el sistema entra desde '
             'una máquina nueva, casi todas las agencias envían un código por correo: pulse '
             'el escudo, introdúzcalo, y la recogida automática puede seguir sin usted.',
          cam=(0.54, 0.54, 1.34),
          point=(0.5225, 0.536), click=1.7,
          ring=(0.513, 0.522, 0.021, 0.028),
          label_en='Verify device', label_es='Verificar dispositivo'),

        B(en='The small plug on the left of each card tells you whether the software that '
             'drives that agency is installed on the server. Green is loaded. Red means it '
             'is missing, and that is one for support, not for you.',
          es='El pequeño enchufe a la izquierda de cada tarjeta le dice si el software que '
             'maneja esa agencia está instalado en el servidor. Verde, cargado. Rojo '
             'significa que falta, y eso es para el soporte, no para usted.',
          cam=(0.42, 0.54, 1.30),
          point=(0.491, 0.536),
          ring=(0.484, 0.522, 0.018, 0.028)),

        B(en='With the accounts connected, tolls start arriving on their own. Next: getting '
             'your vehicles into the system so those tolls have something to attach to.',
          es='Con las cuentas conectadas, los peajes empiezan a llegar solos. A continuación: '
             'meter sus vehículos en el sistema para que esos peajes tengan a qué engancharse.',
          cam=(0.5, 0.30, 1.0), label_en=' ', label_es=' '),
    ])


# =============================================================================== 04
EP04 = E(
    4, 'vehicle-list',
    'The vehicle list', 'La lista de vehículos',
    'Reading it, filtering it, and the menu hidden on every row',
    'Cómo leerla, filtrarla, y el menú escondido en cada fila',
    [
        B(en='Vehicles, then All Vehicles. Every car you own is on this page, whichever way '
             'it got here.',
          es='Vehículos, y luego Todos los vehículos. Cada coche que usted tiene está en '
             'esta página, sea cual sea la vía por la que llegó.',
          shot='10-all-vehicles', url='/vehicles', cam=(0.5, 0.42, 1.0),
          label_en='Vehicles → All Vehicles', label_es='Vehículos → Todos los vehículos'),

        B(en='Five buttons across the top. Import takes a spreadsheet, Add Vehicle takes one '
             'car by hand, Show Details widens the table, Reload re-reads it, and Assign '
             'Providers attaches toll agencies to several vehicles at once.',
          es='Cinco botones arriba. Importar toma una hoja de cálculo, Añadir vehículo toma '
             'un coche a mano, Mostrar detalles ensancha la tabla, Recargar la vuelve a '
             'leer, y Asignar proveedores engancha agencias de peaje a varios vehículos a la '
             'vez.',
          cam=(0.70, 0.16, 1.18),
          ring={'en': (0.524, 0.120, 0.468, 0.040),
                'es': (0.474, 0.108, 0.400, 0.080)}),

        B(en='Under them, the filters. Type, status, toll setup, and a search box that '
             'matches a plate, a name, an email or a type — you do not have to say which. '
             'Toll setup is the one to remember: it narrows the list to the cars that are '
             'wired up to an agency, or the ones that are not.',
          es='Debajo, los filtros. Tipo, estado, configuración de peaje, y un cuadro de '
             'búsqueda que encuentra una matrícula, un nombre, un correo o un tipo: no '
             'hace falta decir cuál. La configuración de peaje es la que hay que recordar: '
             'reduce la lista a los coches enganchados a una agencia, o a los que no.',
          cam=(0.5, 0.23, 1.18),
          ring=(0.218, 0.207, 0.706, 0.043),
          label_en='Filters', label_es='Filtros'),

        B(en='The table itself. Licence plate and title carry a red asterisk, and that is '
             'the system telling you they are required: a plate identifies a vehicle '
             'everywhere else in the product.',
          es='La tabla. Matrícula y título llevan un asterisco rojo, y eso es el sistema '
             'diciéndole que son obligatorios: una matrícula identifica al vehículo en todo '
             'el resto del producto.',
          cam=(0.5, 0.35, 1.16),
          ring=(0.218, 0.313, 0.744, 0.056),
          label_en='The columns', label_es='Las columnas'),

        B(en='Booking status says whether the car is on a live booking. Payment status is '
             'the one to scan: "No tolls" is fine, "Failed" is a card that did not go '
             'through, and "Reservation payment stuck" wants looking at today.',
          es='El estado de reserva dice si el coche está en una reserva activa. El estado de '
             'pago es el que hay que repasar: "Sin peajes" está bien, "Fallido" es una '
             'tarjeta que no pasó, y "Pago de reserva atascado" hay que mirarlo hoy.',
          cam=(0.62, 0.50, 1.22),
          ring=(0.594, 0.313, 0.150, 0.500),
          label_en='Payment status', label_es='Estado de pago'),

        B(en='On the left of every row is a strip of icons: a map, diagnostics, a calendar, '
             'and information. A vehicle with no tracker simply shows fewer of them.',
          es='A la izquierda de cada fila hay una tira de iconos: un mapa, diagnóstico, un '
             'calendario e información. Un vehículo sin rastreador simplemente muestra '
             'menos.',
          cam=(0.28, 0.42, 1.30),
          ring=(0.233, 0.376, 0.084, 0.037)),

        B(en='And the three dots open the menu that does the real work.',
          es='Y los tres puntos abren el menú que hace el trabajo de verdad.',
          cam=(0.28, 0.44, 1.30),
          point=(0.242, 0.395), click=1.2),

        B(en='Book Reservation starts a booking on this car. View Bookings shows the ones it '
             'already has. All EZ Tolls lists every toll it has ever run up.',
          es='Reservar inicia una reserva con este coche. Ver reservas muestra las que ya '
             'tiene. Todos los peajes EZ lista cada peaje que ha acumulado.',
          shot='12-vehicle-context-menu', cam=(0.42, 0.55, 1.26),
          ring=(0.367, 0.428, 0.124, 0.302),
          label_en='The row menu', label_es='El menú de la fila'),

        B(en='Trip draws where it has been, Diagnostics reads the tracker, and Edit opens '
             'the full vehicle form. Six things, one click from any row.',
          es='Viaje dibuja por dónde ha estado, Diagnóstico lee el rastreador, y Editar abre '
             'el formulario completo del vehículo. Seis cosas, a un clic desde cualquier '
             'fila.',
          cam=(0.42, 0.64, 1.28),
          point=(0.400, 0.663)),

        B(en='At the bottom, the count and the pager. Ten rows to a page by default — change '
             'it here, because a fleet of forty is four pages of scrolling otherwise.',
          es='Abajo, el recuento y el paginador. Diez filas por página por defecto: cámbielo '
             'aquí, porque si no una flota de cuarenta son cuatro páginas de desplazamiento.',
          shot='10-all-vehicles', cam=(0.5, 0.85, 1.20),
          ring=(0.218, 0.828, 0.744, 0.048),
          label_en='Paging', label_es='Paginación'),
    ])


# =============================================================================== 05
EP05 = E(
    5, 'add-vehicles',
    'Getting your fleet in', 'Meter su flota',
    'A spreadsheet, one car by hand, or straight from an agency',
    'Una hoja de cálculo, un coche a mano, o directo de una agencia',
    [
        B(en='There is more than one way to get vehicles into the system, and the fastest '
             'one depends on where your list already lives.',
          es='Hay más de una forma de meter vehículos en el sistema, y la más rápida depende '
             'de dónde esté ya su lista.',
          shot='10-all-vehicles', url='/vehicles', cam=(0.5, 0.42, 1.0),
          label_en='Five ways in', label_es='Cinco vías de entrada'),

        B(en='If you already use a booking platform — HQ Rental, Renteon, RENTALL, TSD — '
             'pull the fleet from there and it arrives with its bookings. If a toll agency '
             'already knows your cars, create them from the agency and the transponder link '
             'comes free.',
          es='Si ya usa una plataforma de reservas — HQ Rental, Renteon, RENTALL, TSD — '
             'traiga la flota desde ahí y llega con sus reservas. Si una agencia de peaje ya '
             'conoce sus coches, créelos desde la agencia y el enlace del transpondedor '
             'viene gratis.',
          cam=(0.5, 0.42, 1.0)),

        B(en='If what you have is a spreadsheet, press Import.',
          es='Si lo que tiene es una hoja de cálculo, pulse Importar.',
          cam=(0.62, 0.16, 1.22),
          point={'en': (0.565, 0.141), 'es': (0.518, 0.127)}, click=1.1,
          ring={'en': (0.526, 0.122, 0.074, 0.038),
                'es': (0.475, 0.109, 0.081, 0.033)}),

        B(en='Drop the file in. CSV, xlsx and xls all work, and the columns are matched for '
             'you — you are not asked to map anything by hand.',
          es='Suelte el archivo aquí. CSV, xlsx y xls funcionan, y las columnas se '
             'corresponden solas: no le piden mapear nada a mano.',
          shot='13-import-vehicles-modal', cam=(0.5, 0.50, 1.14),
          point=(0.50, 0.532), click=1.7,
          ring=(0.150, 0.452, 0.700, 0.160),
          label_en='Import Vehicles', label_es='Importar vehículos'),

        B(en='Two columns are required: plate number and plate state. Those two together are '
             'what identifies a vehicle to a toll agency, and a file without the state can '
             'be filled in afterwards in one action.',
          es='Dos columnas son obligatorias: número de matrícula y estado de la matrícula. '
             'Esos dos juntos son lo que identifica un vehículo ante una agencia de peaje, y '
             'a un archivo sin el estado se le puede rellenar después en una sola acción.',
          cam=(0.5, 0.50, 1.14)),

        B(en='For one or two cars it is quicker by hand. Add Vehicle.',
          es='Para uno o dos coches es más rápido a mano. Añadir vehículo.',
          shot='10-all-vehicles', cam=(0.66, 0.16, 1.22),
          point={'en': (0.651, 0.141), 'es': (0.616, 0.127)}, click=1.2,
          ring={'en': (0.604, 0.122, 0.094, 0.038),
                'es': (0.559, 0.109, 0.111, 0.033)}),

        B(en='Three tabs: Basic Info, Pricing, Location. You can save from any of them; the '
             'other two can be filled in later.',
          es='Tres pestañas: Información básica, Precios y Ubicación. Puede guardar desde '
             'cualquiera de ellas; las otras dos se pueden rellenar después.',
          shot='14-add-vehicle-basic', url='/vehicles/new', cam=(0.5, 0.17, 1.16),
          ring=(0.204, 0.144, 0.226, 0.035),
          label_en='Add New Vehicle', label_es='Añadir vehículo nuevo'),

        B(en='Title and description are what a renter reads. The title is required, and it '
             'is the name this car will carry on every other screen.',
          es='El título y la descripción son lo que lee un arrendatario. El título es '
             'obligatorio, y es el nombre que este coche llevará en todas las demás '
             'pantallas.',
          cam=(0.5, 0.30, 1.18),
          ring=(0.217, 0.283, 0.760, 0.030)),

        B(en='Two checkboxes decide whether it is visible at all. Publish listing puts it on '
             'your storefront; Show on My E-Z Wheels adds it to the shared marketplace.',
          es='Dos casillas deciden si es visible siquiera. Publicar anuncio lo pone en su '
             'sitio; Mostrar en My E-Z Wheels lo añade al mercado compartido.',
          cam=(0.36, 0.44, 1.28),
          point=(0.226, 0.438), click=1.5,
          ring=(0.214, 0.430, 0.395, 0.024),
          label_en='Where it is listed', label_es='Dónde se publica'),

        B(en='Toll Systems is the row that decides whether this car can be billed at all. '
             'Add attaches an agency to it — and an empty list here is the commonest reason '
             'a toll arrives with nobody to charge.',
          es='Sistemas de peaje es la fila que decide si este coche se puede facturar. '
             'Añadir le engancha una agencia, y una lista vacía aquí es el motivo más común '
             'de que llegue un peaje sin nadie a quien cobrar.',
          cam=(0.5, 0.47, 1.22),
          point=(0.960, 0.469), click=1.8,
          ring=(0.214, 0.458, 0.762, 0.044),
          label_en='Toll Systems', label_es='Sistemas de peaje'),

        B(en='Then Vehicle Information. Type, country, brand, model, year, colours — most of '
             'this is already filled in from the defaults you set in episode two.',
          es='Después, Información del vehículo. Tipo, país, marca, modelo, año, colores: '
             'casi todo esto ya viene relleno con los valores por defecto que fijó en el '
             'episodio dos.',
          cam=(0.5, 0.66, 1.14),
          ring=(0.203, 0.561, 0.783, 0.312),
          label_en='Vehicle Information', label_es='Información del vehículo'),

        B(en='Plate number and plate state. These two matter more than anything else on the '
             'form: get the state wrong and the agency will never match this car.',
          es='Número y estado de la matrícula. Estos dos importan más que cualquier otra '
             'cosa del formulario: si el estado está mal, la agencia nunca reconocerá este '
             'coche.',
          cam=(0.62, 0.775, 1.26),
          ring=(0.472, 0.769, 0.504, 0.030)),

        B(en='VIN and GPS tracker IMEI are optional, but the IMEI is what ties a tracker to '
             'this car, and a tracker is what lets the system find a toll the agency never '
             'billed you for.',
          es='El VIN y el IMEI del rastreador son opcionales, pero el IMEI es lo que ata un '
             'rastreador a este coche, y un rastreador es lo que permite al sistema '
             'encontrar un peaje que la agencia nunca le facturó.',
          cam=(0.62, 0.836, 1.26),
          ring=(0.216, 0.830, 0.760, 0.030)),

        B(en='Save Vehicle. That is one car in. Next: the step people skip, and then spend '
             'a month wondering where their money went.',
          es='Guardar vehículo. Ya está un coche dentro. A continuación: el paso que la '
             'gente se salta, y luego pasa un mes preguntándose dónde se fue su dinero.',
          cam=(0.80, 0.11, 1.24),
          point=(0.940, 0.103), click=1.4,
          ring=(0.888, 0.089, 0.102, 0.028),
          label_en='Save Vehicle', label_es='Guardar vehículo'),
    ])
