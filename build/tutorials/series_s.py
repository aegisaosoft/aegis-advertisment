# -*- coding: utf-8 -*-
"""Episodes 55-56 — the integrations: FleetBold (GPS) and Fleetwire (rental software).

Frames: capture-integrations.js (`int-01..04` the dev portal as an empty test owner, the connected card staged in the
browser; `int-20, 21` drawn, because the path through Fleetwire is on Fleetwire's site) and compose_fleetbold.py
(`int-10..12` FleetBold's own sign-in and consent pages, English only, real screenshots from the connection of
2026-11-04). `31-`, `32-`, `60-` are the series' existing frames.

Facts the narration states, checked against the code or the partner's docs:
FleetBold — one-click OAuth, nothing to type (provider AuthKind oauth, OwnerGpsPluginsTab); the scopes on the consent
page ask only to read, no command scope (FleetBoldProvider.OAuth DefaultScope); the host picks all or selected vehicles
(consent page); a car already in the fleet is matched by VIN without a second copy (dev and prod, 2026-11-01 and -04);
Remove stops collection (GpsProviderController.Delete); revoke is under Connected apps in FleetBold (consent page).
Fleetwire — the path Connections, Toll and violation partners and the account created through our POST /owners with an
invite (Chad Hurin 2026-10-14, Partner API docs; the host's screens were not seen by us); charges match a rental by
plate and time, unmatched wait for the host's review (POST /companies/{id}/charges); billed on the rental's invoice
(FleetwirePlatformProvider); GPS-only crossings wait for the agency (BackgroundService, AttributedPlatformCharges).
"""
from model import B, E

ADD = {'en': (0.2025, 0.274, 0.106, 0.032), 'es': (0.2025, 0.274, 0.125, 0.032)}
SELECT = (0.219, 0.352, 0.387, 0.028)
CONNECT = {'en': (0.219, 0.446, 0.108, 0.034), 'es': (0.219, 0.446, 0.112, 0.034)}
CARD = (0.2025, 0.236, 0.420, 0.160)
SIGN_IN = (0.417, 0.540, 0.166, 0.089)
ASKS = (0.330, 0.185, 0.333, 0.337)
SCOPES = (0.351, 0.239, 0.291, 0.214)
VEHICLES = (0.351, 0.564, 0.291, 0.153)
APPROVE = (0.579, 0.809, 0.0625, 0.037)
FLOW_A = (0.0625, 0.330, 0.254, 0.220)
FLOW_B = (0.3725, 0.330, 0.254, 0.220)
FLOW_C = (0.684, 0.330, 0.254, 0.220)
STEPS = (0.206, 0.200, 0.588, 0.522)

# =============================================================================== 55
EP55 = E(
    55, 'fleetbold',
    'Connect FleetBold: find tolls from the GPS you already have',
    'Conecte FleetBold: encuentre peajes con el GPS que ya tiene',
    'One click, no new device: FleetBold sends the location, MyEZToll finds the tolls',
    'Un clic, sin aparato nuevo: FleetBold envía la ubicación, MyEZToll encuentra los peajes',
    [
        B(en='Do you use FleetBold for your cars? Then MyEZToll can read their location from there. You install nothing new.',
          es='¿Usa FleetBold para sus coches? Entonces MyEZToll puede leer su ubicación desde allí. No instala nada nuevo.',
          shot='int-01-gps-tab', url='/settings', cam=(0.42, 0.25, 1.5),
          label_en='Settings → GPS Systems', label_es='Configuración → Sistemas GPS'),

        B(en='We use that route to find tolls, and to tie each toll to the right car and the right trip.',
          es='Usamos esa ruta para encontrar peajes y para unir cada peaje con el coche y el viaje correctos.',
          cam=(0.42, 0.25, 1.5)),

        B(en='Open Settings, then GPS Systems. Press Add GPS provider.',
          es='Abra Configuración y luego Sistemas GPS. Pulse Añadir proveedor GPS.',
          cam=(0.36, 0.29, 1.8), ring=ADD, point=(0.255, 0.290), click=2.2),

        B(en='In the list, choose FleetBold.',
          es='En la lista, elija FleetBold.',
          shot='int-03-connect', cam=(0.41, 0.37, 1.8), ring=SELECT),

        B(en='There is nothing else to type. Press Connect FleetBold.',
          es='No hay nada más que escribir. Pulse Conectar FleetBold.',
          cam=(0.41, 0.40, 1.8), ring=CONNECT, point=(0.273, 0.463), click=1.8),

        B(en='FleetBold’s own page opens. Sign in with your FleetBold account. MyEZToll never sees your password.',
          es='Se abre la página de FleetBold. Inicie sesión con su cuenta de FleetBold. MyEZToll nunca ve su contraseña.',
          shot='int-10-fb-signin', url='@partners-api.fleetbold.com', cam=(0.5, 0.5, 1.5), ring=SIGN_IN,
          label_en='FleetBold', label_es='FleetBold'),

        B(en='FleetBold asks if MyEZToll may have access.',
          es='FleetBold pregunta si MyEZToll puede tener acceso.',
          shot='int-11-fb-consent', url='@partners-api.fleetbold.com', cam=(0.5, 0.36, 1.5), ring=ASKS),

        B(en='Here is the list. Read your vehicles, their location and their trips, and keep doing it while you are away. '
             'MyEZToll only reads. It does not ask to lock or control your cars.',
          es='Aquí está la lista. Leer sus vehículos, su ubicación y sus viajes, y seguir haciéndolo mientras usted no está. '
             'MyEZToll solo lee. No pide bloquear ni controlar sus coches.',
          shot='int-12-fb-vehicles', url='@partners-api.fleetbold.com', cam=(0.5, 0.36, 1.5), ring=SCOPES),

        B(en='Choose which cars to share: all of them, or only the ones you pick.',
          es='Elija qué coches compartir: todos, o solo los que usted seleccione.',
          cam=(0.5, 0.62, 1.5), ring=VEHICLES),

        B(en='Press Approve.',
          es='Pulse Approve.',
          cam=(0.5, 0.70, 1.5), ring=APPROVE, point=(0.610, 0.827), click=0.8),

        B(en='You are back in MyEZToll. Connected. Your cars are coming in.',
          es='Ya está de vuelta en MyEZToll. Conectado. Sus coches están llegando.',
          shot='int-04-connected', url='/settings', cam=(0.42, 0.32, 1.7), ring=CARD,
          label_en='Connected', label_es='Conectado'),

        B(en='A car that is already in your fleet is recognized by its VIN, so you do not get a second copy of it.',
          es='Un coche que ya está en su flota se reconoce por su VIN, así que no aparece una segunda copia.',
          cam=(0.42, 0.32, 1.7)),

        B(en='A toll found this way is an estimate from the route. When the agency reports the charge, you see the real amount under Tolls.',
          es='Un peaje encontrado así es una estimación según la ruta. Cuando la agencia informa el cargo, usted ve el importe real en Peajes.',
          shot='60-tolls', url='/tolls', cam=(0.5, 0.45, 1.0),
          label_en='Tolls', label_es='Peajes'),

        B(en='Want to stop? Press Remove on this card. You can also take the access back in your FleetBold account, under Connected apps.',
          es='¿Quiere detenerlo? Pulse Eliminar en esta tarjeta. También puede retirar el acceso en su cuenta de FleetBold, en Connected apps.',
          shot='int-04-connected', url='/settings', cam=(0.42, 0.32, 1.7), ring=CARD),
    ])

# =============================================================================== 56
EP56 = E(
    56, 'fleetwire',
    'Fleetwire: tolls and violations on your renter’s invoice',
    'Fleetwire: peajes y multas en la factura de su arrendatario',
    'MyEZToll finds the charges, Fleetwire bills them to the renter',
    'MyEZToll encuentra los cargos, Fleetwire se los cobra al arrendatario',
    [
        B(en='Do you run your rentals on Fleetwire? Here is how tolls and violations work with MyEZToll.',
          es='¿Lleva sus alquileres en Fleetwire? Así funcionan los peajes y las multas con MyEZToll.',
          shot='int-20-fw-flow', cam=(0.5, 0.45, 1.0),
          label_en='MyEZToll and Fleetwire', label_es='MyEZToll y Fleetwire'),

        B(en='The charges start at the toll agencies, and with parking and camera violations.',
          es='Los cargos empiezan en las agencias de peaje, y con las multas de estacionamiento y de cámara.',
          cam=(0.5, 0.45, 1.0), ring=FLOW_A),

        B(en='MyEZToll finds each one and gets it ready.',
          es='MyEZToll encuentra cada uno y lo prepara.',
          cam=(0.5, 0.45, 1.0), ring=FLOW_B),

        B(en='Then it goes to Fleetwire, and Fleetwire bills your renter.',
          es='Luego pasa a Fleetwire, y Fleetwire se lo cobra a su arrendatario.',
          cam=(0.5, 0.45, 1.0), ring=FLOW_C),

        B(en='To start, go to your Fleetwire account. Open Connections, then Toll and violation partners, and turn on MyEZToll.',
          es='Para empezar, vaya a su cuenta de Fleetwire. Abra Connections, luego Toll and violation partners, y active MyEZToll.',
          shot='int-21-fw-steps', cam=(0.5, 0.46, 1.25), ring=STEPS,
          label_en='In Fleetwire', label_es='En Fleetwire'),

        B(en='Your MyEZToll account is created for you. Watch for the invitation email, open it, and set your password.',
          es='Su cuenta de MyEZToll se crea por usted. Espere el correo de invitación, ábralo y elija su contraseña.',
          cam=(0.5, 0.46, 1.25), ring=STEPS),

        B(en='One step is yours. In MyEZToll, open Settings, then Toll Accounts.',
          es='Un paso le toca a usted. En MyEZToll, abra Configuración y luego Cuentas de peaje.',
          shot='31-settings-toll-accounts', url='/owners/settings', cam=(0.5, 0.30, 1.0),
          point=(0.520, 0.199), click=2.4,
          label_en='Settings → Toll Accounts', label_es='Configuración → Cuentas de peaje'),

        B(en='Press Add Toll Account, and add your login for each toll agency. That is where the tolls come from.',
          es='Pulse Añadir cuenta de peaje y agregue su acceso de cada agencia de peaje. De ahí vienen los peajes.',
          shot='32-settings-add-toll-account', cam=(0.5, 0.40, 1.20),
          point=(0.42, 0.381), click=1.5, ring=(0.348, 0.363, 0.146, 0.036),
          label_en='Add Toll Account', label_es='Añadir cuenta de peaje'),

        B(en='From then on the tolls appear here on their own. Nobody types them in.',
          es='Desde entonces los peajes aparecen aquí solos. Nadie los escribe.',
          shot='60-tolls', url='/tolls', cam=(0.5, 0.45, 1.0),
          label_en='Tolls', label_es='Peajes'),

        B(en='Fleetwire finds the rental from the plate and the time, and puts the charge on that rental’s invoice.',
          es='Fleetwire encuentra el alquiler por la matrícula y la hora, y pone el cargo en la factura de ese alquiler.',
          shot='int-20-fw-flow', cam=(0.5, 0.45, 1.0), ring=FLOW_C),

        B(en='If it cannot find the rental, the charge waits in Fleetwire for you to review it.',
          es='Si no encuentra el alquiler, el cargo espera en Fleetwire a que usted lo revise.',
          cam=(0.5, 0.45, 1.0), ring=FLOW_C),

        B(en='Only tolls the agency has billed go to Fleetwire. A toll seen only by GPS waits for the agency’s report, so your renter pays the real amount.',
          es='Solo pasan a Fleetwire los peajes que la agencia ya cobró. Un peaje visto solo por GPS espera el informe de la agencia, así su arrendatario paga el importe real.',
          cam=(0.5, 0.45, 1.0), ring=FLOW_B),
    ])
