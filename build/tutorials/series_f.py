# -*- coding: utf-8 -*-
"""Episodes 15 to 17 — trackers, the alerts they raise, and the people who drive."""
from model import B, E


# =============================================================================== 15
EP15 = E(
    15, 'gps',
    'GPS — connecting trackers and reading the map', 'GPS: conectar rastreadores y leer el mapa',
    'What a tracker adds that a toll agency cannot',
    'Lo que aporta un rastreador y una agencia de peaje no puede',
    [
        B(en='Company, Settings, GPS Systems. A tracker is optional, and it changes what the '
             'system can prove.',
          es='Compañía, Configuración, GPS Systems. Un rastreador es opcional, y cambia lo que '
             'el sistema puede demostrar.',
          shot='33-settings-gps-systems', url='/owners/settings', cam=(0.5, 0.30, 1.0),
          point={'en': (0.617, 0.199), 'es': (0.675, 0.199)}, click=1.5,
          label_en='Settings → GPS Systems', label_es='Configuración → GPS Systems'),

        B(en='Without one, you know a transponder went through a gantry. With one, you know '
             'which car was at that gantry at that second — which is the difference between '
             'billing a driver and winning a dispute.',
          es='Sin él, usted sabe que un transpondedor pasó por un pórtico. Con él, sabe qué '
             'coche estaba en ese pórtico en ese segundo, que es la diferencia entre facturar '
             'a un conductor y ganar una disputa.',
          cam=(0.5, 0.30, 1.0)),

        B(en='Each provider you have connected is a card. The green tick and the last scan '
             'time are the health check: a provider that has not scanned recently is not '
             'feeding anything.',
          es='Cada proveedor conectado es una tarjeta. La marca verde y la hora del último '
             'escaneo son la comprobación de salud: un proveedor que no ha escaneado hace poco '
             'no está alimentando nada.',
          cam=(0.40, 0.33, 1.24),
          ring={'en': (0.201, 0.288, 0.424, 0.124), 'es': (0.201, 0.288, 0.424, 0.164)},
          label_en='One card per provider', label_es='Una tarjeta por proveedor'),

        B(en='Five buttons. Test connection checks the credentials. Scan now fetches positions '
             'immediately instead of waiting for the schedule.',
          es='Cinco botones. Probar conexión comprueba las credenciales. Escanear ahora trae '
             'las posiciones de inmediato en vez de esperar al calendario.',
          cam=(0.36, 0.37, 1.30),
          point=(0.268, 0.368), click=1.5,
          ring={'en': (0.214, 0.348, 0.390, 0.040),
                'es': (0.214, 0.348, 0.390, 0.082)}),

        B(en='Get Vehicles is the one that matters on your first day: it reads the provider’s '
             'vehicle list and matches it against your fleet, so a tracker finds its car by '
             'itself.',
          es='Obtener vehículos es la que importa el primer día: lee la lista de vehículos del '
             'proveedor y la cruza con su flota, para que un rastreador encuentre su coche '
             'solo.',
          cam=(0.44, 0.37, 1.30),
          point={'en': (0.446, 0.368), 'es': (0.482, 0.368)}, click=1.4,
          label_en='Get Vehicles', label_es='Obtener vehículos'),

        B(en='Add GPS provider connects another one. Several providers on one fleet is normal '
             '— trackers arrive with the cars.',
          es='Añadir proveedor GPS conecta otro. Varios proveedores en una misma flota es '
             'normal: los rastreadores vienen con los coches.',
          cam={'en': (0.30, 0.44, 1.28), 'es': (0.30, 0.486, 1.28)},
          point={'en': (0.256, 0.444), 'es': (0.265, 0.486)}, click=1.2,
          ring={'en': (0.199, 0.424, 0.111, 0.041),
                'es': (0.199, 0.466, 0.128, 0.041)}),

        B(en='Then the maps. Fleet Map is everything you own, right now.',
          es='Después, los mapas. Mapa de flota es todo lo que tiene, ahora mismo.',
          shot='80-gps-fleet-map', url='/gps', cam=(0.5, 0.45, 1.0),
          point=(0.242, 0.143), click=1.2,
          label_en='Fleet Map', label_es='Mapa de flota'),

        B(en='The pill at the top counts the fleet and, next to it in orange, how many of '
             'those are not reporting. Most of the fleet showing as quiet is a thing to look '
             'into, not a map problem.',
          es='La píldora de arriba cuenta la flota y, al lado en naranja, cuántos de esos no '
             'están reportando. Que casi toda la flota salga callada es algo que investigar, '
             'no un problema del mapa.',
          cam=(0.56, 0.24, 1.26),
          ring=(0.528, 0.182, 0.127, 0.036),
          label_en='How many are live', label_es='Cuántos están vivos'),

        B(en='A green pin is live. An orange one is a last known position with the age written '
             'on it, and an age in the tens of minutes is a car that has stopped talking, not '
             'a car that is parked.',
          es='Un pin verde está en vivo. Uno naranja es una última posición conocida con su '
             'antigüedad escrita, y una antigüedad de decenas de minutos es un coche que ha '
             'dejado de hablar, no un coche aparcado.',
          cam=(0.58, 0.72, 1.24)),

        B(en='Three controls on the right. Fit to fleet zooms out until everything is on '
             'screen. Toll booths draws the gantries. Only live hides the stale pins, and '
             'turning it off is how you find a tracker that has gone quiet.',
          es='Tres controles a la derecha. Ajustar a la flota aleja hasta que todo cabe en '
             'pantalla. Cabinas de peaje dibuja los pórticos. Solo en vivo esconde los pines '
             'viejos, y apagarlo es como se encuentra un rastreador que se ha callado.',
          cam=(0.86, 0.24, 1.26),
          point=(0.918, 0.279), click=1.7,
          ring=(0.904, 0.181, 0.090, 0.119),
          label_en='Map controls', label_es='Controles del mapa'),

        B(en='Trip Map is the other view: one vehicle, its route drawn out.',
          es='Mapa de viaje es la otra vista: un vehículo, con su ruta dibujada.',
          shot='81-gps-trip-map', cam=(0.5, 0.45, 1.0),
          point=(0.303, 0.143), click=1.2,
          label_en='Trip Map', label_es='Mapa de viaje'),

        B(en='Choose a car here and the map draws where it went. That trace is the evidence '
             'behind a toll the agency never billed you for, and behind a dispute you would '
             'otherwise lose.',
          es='Elija un coche aquí y el mapa dibuja por dónde fue. Ese trazo es la prueba detrás '
             'de un peaje que la agencia nunca le facturó, y detrás de una disputa que si no '
             'perdería.',
          cam=(0.34, 0.22, 1.28),
          point=(0.295, 0.206), click=1.5,
          ring=(0.209, 0.186, 0.172, 0.040)),
    ])


# =============================================================================== 16
EP16 = E(
    16, 'gps-alerts',
    'GPS alerts', 'Alertas de GPS',
    'Nine events, four switches each — and one warning before you start',
    'Nueve eventos, cuatro interruptores cada uno, y un aviso antes de empezar',
    [
        B(en='Company, Settings, GPS Alerts. This tab exists once you have a tracker, and it '
             'decides what the system tells you about.',
          es='Compañía, Configuración, Alertas de GPS. Esta pestaña aparece cuando tiene un '
             'rastreador, y decide de qué le avisa el sistema.',
          shot='37-settings-gps-alerts', url='/owners/settings', cam=(0.5, 0.20, 1.0),
          point=(0.910, 0.187), click=1.5,
          label_en='Settings → GPS Alerts', label_es='Configuración → Alertas de GPS'),

        B(en='Read the line at the top first. Every event has four switches: message the '
             'owner, message the driver, by SMS, by email. Any combination, per event.',
          es='Lea primero la línea de arriba. Cada evento tiene cuatro interruptores: avisar al '
             'propietario, avisar al conductor, por SMS, por correo. Cualquier combinación, '
             'por evento.',
          cam=(0.5, 0.25, 1.20),
          ring=(0.202, 0.235, 0.790, 0.046)),

        B(en='And before you touch any of them: turning a switch on sends messages to real '
             'phones. Make sure you are on the account you think you are on.',
          es='Y antes de tocar ninguno: activar un interruptor envía mensajes a teléfonos '
             'reales. Asegúrese de estar en la cuenta en la que cree que está.',
          cam=(0.5, 0.25, 1.20), hold=0.6,
          label_en='These reach real phones', label_es='Esto llega a teléfonos reales'),

        B(en='Ignition on and ignition off are the raw ones. Useful for a single high-value '
             'car, unbearable across a fleet of forty.',
          es='Encendido y apagado del contacto son los básicos. Útiles para un solo coche de '
             'alto valor, insoportables en una flota de cuarenta.',
          cam=(0.5, 0.34, 1.18),
          ring=(0.202, 0.290, 0.790, 0.110),
          label_en='Ignition on / off', label_es='Contacto encendido / apagado'),

        B(en='Trip ended fires once the ignition has been off long enough to call the trip '
             'finished — one message per trip rather than two.',
          es='Viaje terminado se dispara cuando el contacto lleva apagado lo suficiente para '
             'dar el viaje por terminado: un mensaje por viaje en vez de dos.',
          cam=(0.30, 0.455, 1.24),
          ring=(0.202, 0.404, 0.392, 0.109)),

        B(en='Towed is the one to turn on and leave on. It fires when the vehicle moves with '
             'the ignition off, which is either a tow truck or a theft, and both are things '
             'you want to hear about immediately.',
          es='Remolcado es el que hay que activar y dejar activado. Se dispara cuando el '
             'vehículo se mueve con el contacto apagado, que es o una grúa o un robo, y de '
             'ambos quiere enterarse al momento.',
          cam=(0.72, 0.455, 1.24),
          ring=(0.598, 0.404, 0.392, 0.109),
          label_en='Towed', label_es='Remolcado'),

        B(en='Speeding fires when the car was over the road’s own limit for a sustained '
             'stretch. Repeats are rate-limited, so one long fast stretch is one message, not '
             'forty.',
          es='Exceso de velocidad se dispara cuando el coche superó el límite de esa carretera '
             'durante un tramo sostenido. Las repeticiones están limitadas, así que un tramo '
             'largo rápido es un mensaje, no cuarenta.',
          cam=(0.30, 0.575, 1.22),
          ring=(0.202, 0.517, 0.392, 0.123),
          label_en='Speeding', label_es='Exceso de velocidad'),

        B(en='Reckless speed is an absolute number, whatever road it happened on. It is sent '
             'instead of the speeding alert, never as well, so you cannot be told twice about '
             'the same moment.',
          es='Velocidad temeraria es una cifra absoluta, sea cual sea la carretera. Se envía en '
             'lugar de la alerta de exceso, nunca además, así que no se le avisa dos veces del '
             'mismo momento.',
          cam=(0.72, 0.575, 1.22),
          point=(0.637, 0.592),
          ring=(0.598, 0.517, 0.392, 0.123),
          label_en='Reckless speed', label_es='Velocidad temeraria'),

        B(en='Device offline means the tracker stopped reporting — unplugged, cut, or '
             'shielded. Note what it says underneath: when a whole fleet goes quiet at once, '
             'the alerts are held back, because that is an outage on our side and not forty '
             'stolen cars.',
          es='Dispositivo desconectado significa que el rastreador dejó de reportar: '
             'desenchufado, cortado o apantallado. Fíjese en lo que dice debajo: cuando toda '
             'una flota se calla a la vez, las alertas se retienen, porque eso es una caída de '
             'nuestro lado y no cuarenta coches robados.',
          cam=(0.30, 0.715, 1.22),
          ring=(0.202, 0.644, 0.392, 0.124),
          label_en='Device offline', label_es='Dispositivo desconectado'),

        B(en='Idling reports an engine running with the vehicle not moving, once per idle stop '
             'rather than continuously.',
          es='Ralentí informa de un motor en marcha con el vehículo parado, una vez por parada '
             'y no de forma continua.',
          cam=(0.72, 0.715, 1.22),
          ring=(0.598, 0.644, 0.392, 0.124)),

        B(en='And GPS signal lost is the engine running with no satellite fix — a disconnected '
             'antenna, a failing device, or a jammer. A parked car losing its fix in a garage '
             'is normal and is not reported.',
          es='Y Señal GPS perdida es el motor en marcha sin cobertura de satélite: una antena '
             'desconectada, un aparato que falla, o un inhibidor. Un coche aparcado que pierde '
             'la señal en un garaje es normal y no se reporta.',
          cam=(0.30, 0.845, 1.22),
          ring=(0.202, 0.772, 0.392, 0.121),
          label_en='GPS signal lost', label_es='Señal GPS perdida'),

        B(en='Start with Towed and Device offline to the owner, by SMS. Add the rest only when '
             'you find you wanted them — an alert you ignore is worse than no alert at all.',
          es='Empiece con Remolcado y Dispositivo desconectado al propietario, por SMS. Añada '
             'el resto solo cuando descubra que los quería: una alerta que se ignora es peor '
             'que ninguna alerta.',
          cam=(0.5, 0.20, 1.06), label_en=' ', label_es=' '),
    ])


# =============================================================================== 17
EP17 = E(
    17, 'drivers',
    'Drivers and locations', 'Conductores y ubicaciones',
    'Who is allowed to drive, and where the cars are handed over',
    'Quién puede conducir, y dónde se entregan los coches',
    [
        B(en='Drivers. Everyone who has ever rented from you, and everyone who is about to.',
          es='Conductores. Todos los que le han alquilado alguna vez, y todos los que están a '
             'punto de hacerlo.',
          shot='90-drivers', url='/drivers', cam=(0.5, 0.45, 1.0),
          label_en='Drivers', label_es='Conductores'),

        B(en='Two tabs. My Drivers is the people attached to your account. New Registered '
             'Drivers is people who signed up through your storefront and have not been '
             'through yet.',
          es='Dos pestañas. Mis conductores son las personas asociadas a su cuenta. Conductores '
             'recién registrados son quienes se dieron de alta en su sitio y aún no han pasado '
             'por aquí.',
          cam=(0.32, 0.28, 1.26),
          point={'en': (0.372, 0.280), 'es': (0.416, 0.280)}, click=1.6,
          ring={'en': (0.205, 0.261, 0.230, 0.043),
                'es': (0.205, 0.261, 0.295, 0.043)}),

        B(en='The icon at the start of each row is that driver’s state at a glance: a document '
             'means their licence is on file, a paper plane means an invitation has gone out '
             'and is waiting to be accepted.',
          es='El icono al principio de cada fila es el estado de ese conductor de un vistazo: '
             'un documento significa que su licencia está archivada, un avión de papel que la '
             'invitación salió y espera aceptación.',
          cam=(0.30, 0.45, 1.28),
          ring=(0.282, 0.425, 0.030, 0.360),
          label_en='Licence, or invitation', label_es='Licencia, o invitación'),

        B(en='Two buttons add people. Add Driver enters them yourself, which you use when you '
             'have their details in front of you.',
          es='Dos botones añaden personas. Añadir conductor los registra usted mismo, que es lo '
             'que usa cuando tiene sus datos delante.',
          cam=(0.70, 0.14, 1.26),
          point={'en': (0.667, 0.127), 'es': (0.605, 0.127)}, click=1.4,
          ring={'en': (0.616, 0.109, 0.376, 0.036),
                'es': (0.542, 0.109, 0.450, 0.036)}),

        B(en='Invite Driver sends them a link instead, and they fill in their own details and '
             'upload their own licence. Fewer keystrokes for you and fewer typing mistakes on '
             'the document that matters.',
          es='Invitar conductor les envía un enlace, y ellos rellenan sus propios datos y suben '
             'su propia licencia. Menos tecleo para usted y menos erratas en el documento que '
             'importa.',
          cam=(0.76, 0.14, 1.28),
          point={'en': (0.762, 0.127), 'es': (0.729, 0.127)}, click=1.3,
          label_en='Invite Driver', label_es='Invitar conductor'),

        B(en='The filters narrow a long list down fast, and Additional contacts brings in the '
             'extra people on a booking — a second driver, somebody named on the '
             'agreement.',
          es='Los filtros reducen rápido una lista larga, y Contactos adicionales trae a las '
             'personas extra de una reserva: un segundo conductor, alguien nombrado '
             'en el contrato.',
          cam=(0.55, 0.21, 1.24),
          point={'en': (0.622, 0.205), 'es': (0.677, 0.205)}, click=1.5,
          ring={'en': (0.404, 0.187, 0.315, 0.038),
                'es': (0.404, 0.187, 0.375, 0.038)}),

        B(en='View Details on the right opens everything about that person: their documents, '
             'their bookings, their cards, their history with you.',
          es='Ver detalles a la derecha abre todo sobre esa persona: sus documentos, sus '
             'reservas, sus tarjetas, su historial con usted.',
          cam=(0.84, 0.45, 1.26),
          point={'en': (0.905, 0.432), 'es': (0.902, 0.432)}, click=1.4),

        B(en='Then Locations, which is a much smaller page and a surprisingly important one.',
          es='Después, Ubicaciones, que es una página mucho más pequeña y sorprendentemente '
             'importante.',
          shot='91-locations', url='/locations', cam=(0.5, 0.30, 1.0),
          label_en='Locations', label_es='Ubicaciones'),

        B(en='These are your pickup points. They appear on your storefront, and a renter '
             'searching a city finds you through them.',
          es='Estos son sus puntos de recogida. Aparecen en su sitio, y un arrendatario que '
             'busca en una ciudad le encuentra a través de ellos.',
          cam=(0.5, 0.32, 1.20),
          ring=(0.215, 0.282, 0.756, 0.104)),

        B(en='Source says where a location came from. Manual is one you typed. Sync from plugin '
             'pulls them out of your booking platform instead, and merges them into the shared '
             'search.',
          es='Origen dice de dónde vino una ubicación. Manual es una que escribió usted. '
             'Sincronizar desde el plugin las trae de su plataforma de reservas y las une a la '
             'búsqueda compartida.',
          cam=(0.66, 0.34, 1.28),
          point=(0.827, 0.159), click=1.7,
          ring=(0.596, 0.347, 0.041, 0.025),
          label_en='Sync from plugin', label_es='Sincronizar desde el plugin'),

        B(en='And the Assign Vehicles tab is where each car is told which location it lives at '
             '— which is what makes a search for a city return your fleet rather than nothing.',
          es='Y la pestaña Asignar vehículos es donde a cada coche se le dice en qué ubicación '
             'vive, que es lo que hace que una búsqueda por ciudad devuelva su flota en vez de '
             'nada.',
          cam=(0.32, 0.25, 1.26),
          point=(0.307, 0.236), click=1.4,
          ring=(0.215, 0.218, 0.128, 0.040),
          label_en='Assign Vehicles', label_es='Asignar vehículos'),
    ])
