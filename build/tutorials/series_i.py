# -*- coding: utf-8 -*-
"""Episodes 22 onward — Turo: the mailbox, the phone agent, the fleet, and pending bookings.

Turo sends no webhooks. What the portal knows about a Turo trip it learns from Turo's own
notification emails, so this part starts where that mail has to arrive: a mailbox of the
owner's own, inside the portal.
"""
from model import B, E


# =============================================================================== 22
EP22 = E(
    22, 'turo-mailbox',
    'Turo, part 1: your own mailbox', 'Turo, parte 1: su propio buzón',
    'The address your Turo mail goes to, and where you read it',
    'La dirección a la que va su correo de Turo, y dónde lo lee',
    [
        B(en='Turo tells you about every booking by email. The portal reads those same emails. '
             'So the first step is an email address of your own, inside the portal.',
          es='Turo le avisa de cada reserva por correo. El portal lee esos mismos correos. Así '
             'que el primer paso es una dirección de correo propia, dentro del portal.',
          shot='30-settings-owner', url='/settings', cam=(0.5, 0.30, 1.0),
          label_en='Settings', label_es='Configuración'),

        B(en='Open Company, then Settings, and scroll to the bottom. The box you need is '
             'called Email Relay.',
          es='Abra Empresa, después Configuración, y baje hasta el final. El recuadro que '
             'necesita se llama Reenvío de correo.',
          cam=(0.60, 0.78, 1.10),
          ring=(0.204, 0.677, 0.785, 0.230),
          label_en='Email Relay', label_es='Reenvío de correo'),

        B(en='In Public alias, type a short name — your company name is fine. Small letters '
             'and numbers only, no spaces. It becomes your new address, ending in '
             '@mail.myeztoll.com.',
          es='En Alias público, escriba un nombre corto: el de su empresa sirve. Solo '
             'minúsculas y números, sin espacios. Será su nueva dirección, terminada en '
             '@mail.myeztoll.com.',
          cam=(0.38, 0.74, 1.40),
          point=(0.36, 0.744), click=1.6,
          ring=(0.216, 0.731, 0.380, 0.030),
          label_en='Public alias', label_es='Alias público',
          say_en='In Public alias, type a short name — your company name is fine. Small letters '
                 'and numbers only, no spaces. It becomes your new address, ending in at mail dot '
                 'my E Z toll dot com.',
          say_es='En Alias público, escriba un nombre corto: el de su empresa sirve. Solo '
                 'minúsculas y números, sin espacios. Será su nueva dirección, terminada en arroba '
                 'mail punto my E Z toll punto com.'),

        B(en='The full address appears underneath. Click it to copy it — you will need it in '
             'the next video.',
          es='Debajo aparece la dirección completa. Haga clic para copiarla: la necesitará en '
             'el próximo vídeo.',
          cam=(0.34, 0.75, 1.46),
          point=(0.29, 0.765), click=1.5,
          ring=(0.216, 0.755, 0.162, 0.020)),

        B(en='In Forward to, type the email you use every day. Only that email can send '
             'replies from the new address.',
          es='En Reenviar a, escriba el correo que usa cada día. Solo ese correo puede '
             'responder desde la nueva dirección.',
          cam=(0.78, 0.74, 1.40),
          ring=(0.598, 0.731, 0.380, 0.030),
          label_en='Forward to', label_es='Reenviar a'),

        B(en='Make sure Forwarding enabled is switched on. If it is off, emails from Turo are '
             'lost, and nothing warns you.',
          es='Asegúrese de que Reenvío activado está encendido. Si está apagado, los correos '
             'de Turo se pierden, y nada le avisa.',
          cam=(0.72, 0.80, 1.34),
          ring=(0.216, 0.771, 0.770, 0.040),
          label_en='Forwarding enabled', label_es='Reenvío activado'),

        B(en='Click Save. A green Active label in the corner means the address works.',
          es='Pulse Guardar. Una etiqueta verde de Activo en la esquina significa que la '
             'dirección funciona.',
          cam=(0.86, 0.76, 1.30),
          point=(0.942, 0.831), click=1.3,
          ring=(0.935, 0.681, 0.046, 0.022)),

        B(en="Recent senders shows who has written to your new address. Gmail's confirmation "
             'email will appear here in the next video.',
          es='Remitentes recientes muestra quién ha escrito a su nueva dirección. El correo de '
             'confirmación de Gmail aparecerá aquí en el próximo vídeo.',
          cam=(0.60, 0.87, 1.24),
          ring=(0.216, 0.880, 0.770, 0.024),
          label_en='Recent senders', label_es='Remitentes recientes'),

        B(en='To read the emails, open SMS and Mail, then Email. It works like any inbox: '
             'Inbox, Sent, search, and Compose.',
          es='Para leer los correos, abra SMS y correo, y después Correo. Funciona como '
             'cualquier bandeja: Entrada, Enviados, búsqueda y Redactar.',
          shot='93-messages', url='/messages', cam=(0.5, 0.28, 1.04),
          ring=(0.217, 0.196, 0.754, 0.046),
          label_en='Email', label_es='Correo'),

        B(en='Turo emails are kept here, in the portal — not in your usual inbox. This is the '
             'place to look for them.',
          es='Los correos de Turo se guardan aquí, en el portal, no en su bandeja habitual. '
             'Este es el sitio donde buscarlos.',
          cam=(0.30, 0.52, 1.24),
          ring=(0.217, 0.254, 0.242, 0.532)),

        B(en='Your address is ready. Next: telling Gmail to send your Turo emails here, '
             'automatically.',
          es='Su dirección está lista. A continuación: decirle a Gmail que envíe aquí sus '
             'correos de Turo, solo.',
          cam=(0.5, 0.40, 1.0), label_en=' ', label_es=' '),
    ])


# =============================================================================== 23
# The g*-shots are Gmail, captured from a real account and composed by compose_browser.py (the
# browser's own bars cut off, the label list blurred, the address shown as yourcompany). The
# screen is English Gmail; the Spanish narration names the controls as Spanish Gmail does.
EP23 = E(
    23, 'turo-gmail',
    'Turo, part 2: sending your Turo emails to the portal',
    'Turo, parte 2: enviar sus correos de Turo al portal',
    'Adding the address in Gmail, confirming it, and a filter that forwards only Turo',
    'Añadir la dirección en Gmail, confirmarla, y un filtro que reenvía solo lo de Turo',
    [
        B(en='Now we make Gmail send your Turo emails to your new portal address, by itself. '
             'In Gmail on a computer, open the gear, See all settings, then Forwarding and '
             'POP/IMAP.',
          es='Ahora hacemos que Gmail envíe sus correos de Turo a su nueva dirección del '
             'portal, solo. En Gmail, en el ordenador, abra la rueda, Ver todos los ajustes, y '
             'después Reenvío y correo POP/IMAP.',
          shot='g2-forwarding-added', url='@mail.google.com', cam=(0.5, 0.30, 1.0),
          ring=(0.533, 0.165, 0.120, 0.030),
          label_en='Gmail settings', label_es='Ajustes de Gmail'),

        B(en='Click Add a forwarding address.',
          es='Pulse Añadir una dirección de reenvío.',
          cam=(0.45, 0.30, 1.35),
          point=(0.390, 0.321), click=1.2,
          ring=(0.330, 0.303, 0.122, 0.034)),

        B(en='Type your portal address — yourcompany at mail.myeztoll.com, with your own name — '
             'and click Next.',
          es='Escriba su dirección del portal, sucompañía arroba mail.myeztoll.com, con su '
             'propio nombre, y pulse Siguiente.',
          shot='g3-add-dialog', cam=(0.5, 0.48, 1.30),
          point=(0.500, 0.519), click=None,
          ring=(0.330, 0.475, 0.340, 0.080),
          label_en='Add a forwarding address', label_es='Añadir dirección de reenvío',
          say_en='Type your portal address — your company at mail dot my E Z toll dot com, with '
                 'your own name — and click Next.',
          say_es='Escriba su dirección del portal, su compañía arroba mail punto my E Z toll '
                 'punto com, con su propio nombre, y pulse Siguiente.'),

        B(en='A small window opens and asks you to confirm. Click Proceed.',
          es='Se abre una ventana pequeña y le pide confirmar. Pulse Continuar.',
          shot='g7-confirm-window', cam=(0.5, 0.50, 1.25),
          point=(0.291, 0.526), click=1.4,
          ring=(0.258, 0.503, 0.068, 0.046),
          label_en='Confirm', label_es='Confirmar'),

        B(en='Gmail now sends a confirmation email to that address — so it arrives in the '
             'portal. Open SMS and Mail, then Email.',
          es='Gmail envía ahora un correo de confirmación a esa dirección, así que llega al '
             'portal. Abra SMS y correo, y después Correo.',
          shot='93-messages', url='/messages', cam=(0.5, 0.35, 1.05),
          ring=(0.217, 0.254, 0.242, 0.060),
          label_en='Email', label_es='Correo'),

        B(en='Open the Gmail Forwarding Confirmation email, click the link inside it, and then '
             'Confirm on the page that opens.',
          es='Abra el correo de confirmación de reenvío de Gmail, pulse el enlace que trae, y '
             'después Confirmar en la página que se abre.',
          cam=(0.34, 0.33, 1.30),
          point=(0.33, 0.285), click=1.6),

        B(en='Back in Gmail, your address is now on the list. Keep Disable forwarding selected — '
             'otherwise every email you receive would go to the portal, not only Turo.',
          es='De vuelta en Gmail, su dirección ya está en la lista. Deje marcado Inhabilitar el '
             'reenvío: si no, todo el correo que recibe iría al portal, no solo el de Turo.',
          shot='g2-forwarding-added', url='@mail.google.com', cam=(0.48, 0.26, 1.40),
          ring=(0.330, 0.222, 0.360, 0.056),
          label_en='Gmail settings', label_es='Ajustes de Gmail'),

        B(en='Now choose which emails go. Click the small icon at the right of the search bar. '
             'In From, type turo.com.',
          es='Ahora elija qué correos se envían. Pulse el icono pequeño a la derecha de la barra '
             'de búsqueda. En De, escriba turo.com.',
          shot='g4-filter-search', cam=(0.42, 0.22, 1.30),
          point=(0.623, 0.059), click=1.4,
          ring=(0.172, 0.105, 0.455, 0.045),
          label_en='Filter', label_es='Filtro'),

        B(en='Click Create filter.',
          es='Pulse Crear filtro.',
          cam=(0.45, 0.50, 1.30),
          point=(0.521, 0.674), click=1.0,
          ring=(0.490, 0.655, 0.062, 0.040)),

        B(en='Tick Forward it to, and choose your portal address in the list.',
          es='Marque Reenviar a, y elija su dirección del portal en la lista.',
          shot='g5-filter-forward', cam=(0.36, 0.40, 1.40),
          point=(0.359, 0.416), click=None,
          ring=(0.175, 0.395, 0.365, 0.036)),

        B(en='Click Create filter. Google may ask you to sign in again to confirm it is you — '
             'that is normal.',
          es='Pulse Crear filtro. Puede que Google le pida volver a iniciar sesión para '
             'confirmar que es usted: es normal.',
          cam=(0.50, 0.70, 1.30),
          point=(0.580, 0.855), click=1.2,
          ring=(0.535, 0.822, 0.092, 0.066)),

        B(en='Done. The filter list shows it: from turo.com, forward to your portal address. '
             'From now on every Turo email reaches the portal by itself.',
          es='Listo. La lista de filtros lo muestra: de turo.com, reenviar a su dirección del '
             'portal. A partir de ahora cada correo de Turo llega al portal solo.',
          shot='g6-filter-list', cam=(0.45, 0.30, 1.25),
          point=(0.359, 0.422), click=None,
          ring=(0.170, 0.296, 0.730, 0.068),
          label_en='Filters', label_es='Filtros'),

        B(en='Next: the phone app that does the rest of the Turo work.',
          es='A continuación: la aplicación del teléfono que hace el resto del trabajo con Turo.',
          cam=(0.5, 0.35, 1.0), label_en=' ', label_es=' '),
    ])


# =============================================================================== 24
# The p*-shots are phone captures laid on a 16:10 canvas by compose_phone.py; the phone screen
# spans x 0.359-0.641 and y 0.035-0.965 of it. The phone runs in English in both films.
EP24 = E(
    24, 'turo-phone-agent',
    'Turo, part 3: the phone agent', 'Turo, parte 3: el agente del teléfono',
    'Installing My E-Z Toll, the four settings that keep it alive, and checking it works',
    'Instalar My E-Z Toll, los cuatro ajustes que lo mantienen vivo, y comprobar que funciona',
    [
        B(en='Some Turo work has to happen on a phone, because Turo blocks our computers but '
             'not phones. So you install our app on one Android phone.',
          es='Parte del trabajo con Turo tiene que hacerse en un teléfono, porque Turo bloquea '
             'nuestros ordenadores pero no los teléfonos. Así que instala nuestra aplicación '
             'en un teléfono Android.',
          shot='39-download-app', url='/download', cam=(0.5, 0.40, 1.0),
          label_en='Download', label_es='Descargas'),

        B(en='To get the app, click the Android icon at the bottom of any page in the portal.',
          es='Para conseguir la aplicación, haga clic en el icono de Android al pie de '
             'cualquier página del portal.',
          cam=(0.52, 0.80, 1.30),
          point=(0.5275, 0.954), click=1.6,
          ring=(0.515, 0.940, 0.025, 0.030)),

        B(en='On the Android phone you will keep with your cars, tap Download Owner app. Do '
             'not use Google Play: that version cannot do this job.',
          es='En el teléfono Android que tendrá con sus coches, pulse Descargar app Owner. '
             'No use Google Play: esa versión no puede hacer este trabajo.',
          cam=(0.595, 0.34, 1.40),
          point=(0.594, 0.320), click=2.0,
          ring=(0.470, 0.240, 0.248, 0.110),
          label_en='My E-Z Toll — Owner', label_es='My E-Z Toll — Owner'),

        B(en='The first time, Android asks whether it may install apps from your browser. Say '
             'yes. How to install shows each step.',
          es='La primera vez, Android pregunta si puede instalar aplicaciones desde su '
             'navegador. Diga que sí. Cómo instalar enseña cada paso.',
          cam=(0.595, 0.55, 1.30),
          ring=(0.470, 0.664, 0.248, 0.050)),

        B(en='Open the app and sign in with your portal email and password. That is all it '
             'takes to start it — there is no extra button.',
          es='Abra la aplicación e inicie sesión con el correo y la contraseña del portal. No '
             'hace falta nada más para ponerla en marcha: no hay otro botón.',
          shot='p1-signin', url='@My E-Z Toll · Android', cam=(0.5, 0.45, 1.55),
          point=(0.5, 0.537), click=2.4,
          ring=(0.382, 0.345, 0.236, 0.225),
          label_en='My E-Z Toll app', label_es='App My E-Z Toll'),

        B(en='The app shows your business at a glance. The part that talks to Turo runs '
             'quietly in the background.',
          es='La aplicación le muestra su negocio de un vistazo. La parte que habla con Turo '
             'trabaja en silencio, en segundo plano.',
          shot='p2-dashboard', cam=(0.5, 0.40, 1.50)),

        B(en="Now four phone settings, so that Android does not stop the app. Open the phone's "
             'Settings, then Apps, then My E-Z Toll. First: Notifications must be allowed.',
          es='Ahora, cuatro ajustes del teléfono, para que Android no detenga la aplicación. '
             'Abra los Ajustes del teléfono, después Aplicaciones, después My E-Z Toll. '
             'Primero: las notificaciones deben estar permitidas.',
          shot='p3-appinfo', cam=(0.5, 0.35, 1.55),
          ring=(0.368, 0.265, 0.264, 0.075),
          label_en='App info', label_es='Información de la app'),

        B(en='Second: turn off Manage app if unused. Otherwise, after a few quiet weeks, '
             "Android takes the app's permissions away.",
          es='Segundo: desactive Gestionar app si no se usa. Si no, tras unas semanas '
             'tranquilas, Android le quita los permisos a la aplicación.',
          cam=(0.5, 0.50, 1.55),
          point=(0.604, 0.544), click=1.8,
          ring=(0.368, 0.505, 0.264, 0.075)),

        B(en='Third: Battery. Choose Unrestricted. Otherwise the phone puts the app to sleep, '
             'and Turo bookings wait for it.',
          es='Tercero: Batería. Elija Sin restricciones. Si no, el teléfono duerme la '
             'aplicación, y las reservas de Turo la esperan.',
          shot='p5-battery', cam=(0.5, 0.32, 1.55),
          point=(0.396, 0.306), click=1.8,
          ring=(0.368, 0.256, 0.264, 0.098),
          label_en='Battery', label_es='Batería'),

        B(en='Fourth: Appear on top — some phones call it Display over other apps. Turn it on. '
             'The app needs it to open Turo pages.',
          es='Cuarto: Mostrar encima; algunos teléfonos lo llaman Mostrar sobre otras apps. '
             'Actívelo. La aplicación lo necesita para abrir páginas de Turo.',
          shot='p6-appear-on-top', cam=(0.5, 0.28, 1.55),
          point=(0.603, 0.248), click=2.0,
          ring=(0.368, 0.222, 0.264, 0.052),
          label_en='Appear on top', label_es='Mostrar encima'),

        B(en='Now check it in the portal: Company, Settings, Turo Agents. Your phone should be '
             'listed there with a green Active label.',
          es='Ahora compruébelo en el portal: Empresa, Configuración, Agentes de Turo. Su '
             'teléfono debe aparecer ahí con una etiqueta verde de Activo.',
          shot='38-settings-turo-agents', url='/settings', cam=(0.58, 0.30, 1.14),
          ring=(0.214, 0.343, 0.755, 0.036),
          label_en='Turo Agents', label_es='Agentes de Turo'),

        B(en='You can sign in on more than one phone. Only one works at a time. The others '
             'wait, and take over if it stops.',
          es='Puede iniciar sesión en más de un teléfono. Solo uno trabaja a la vez. Los demás '
             'esperan, y lo relevan si se detiene.',
          cam=(0.58, 0.30, 1.14)),

        B(en='If your phone shows Offline, just open the app once. Keep the phone charged and '
             'connected to the internet, and that is all.',
          es='Si su teléfono aparece Desconectado, simplemente abra la aplicación una vez. '
             'Manténgalo cargado y conectado a internet, y eso es todo.',
          cam=(0.5, 0.30, 1.0), label_en=' ', label_es=' '),
    ])


# =============================================================================== 25
# 57-turo-import is the Import cars dialog after a real scan (capture-screenshots.js runs it and
# never clicks Link, Re-link or Unlink); 59-confirm-taken carries the "Remember this listing" box.
EP25 = E(
    25, 'turo-fleet',
    'Turo, part 4: tying listings to your cars', 'Turo, parte 4: atar los anuncios a sus coches',
    'Which cars need it, importing from your host page, and linking by hand',
    'Qué coches lo necesitan, importar desde su página de anfitrión, y enlazar a mano',
    [
        B(en='Your cars are already in the portal. On Turo, each of them has its own page — a '
             'listing. For Turo bookings to work, the portal must know which listing is which '
             'car.',
          es='Sus coches ya están en el portal. En Turo, cada uno tiene su propia página: un '
             'anuncio. Para que las reservas de Turo funcionen, el portal tiene que saber qué '
             'anuncio es qué coche.',
          shot='38-settings-turo-agents',
          url='/settings',
          cam=(0.5, 0.3, 1.0),
          label_en='Turo Agents', label_es='Agentes de Turo'),

        B(en='Most of the time it works this out on its own, from the plate or from the make, '
             'model and year. If you have only one car of a kind, there is nothing to do.',
          es='Casi siempre lo averigua solo, por la matrícula o por la marca, el modelo y el '
             'año. Si solo tiene un coche de cada tipo, no hay nada que hacer.',
          cam=(0.5, 0.3, 1.0)),

        B(en='It needs your help with identical cars — say, three white Camrys from the same '
             'year. This video is about them.',
          es='Necesita su ayuda con los coches idénticos: por ejemplo, tres Camry blancos del '
             'mismo año. Este vídeo trata de ellos.',
          cam=(0.5, 0.3, 1.0)),

        B(en='Open Company, then Settings, then Turo Agents. At the top, your phone must show '
             'a green Active label — the phone from the previous video does the reading.',
          es='Abra Empresa, después Configuración, después Agentes de Turo. Arriba, su '
             'teléfono debe tener una etiqueta verde de Activo: el teléfono del vídeo anterior '
             'es el que lee.',
          cam=(0.58, 0.3, 1.14),
          ring=(0.219, 0.343, 0.75, 0.034)),

        B(en='Under Turo host accounts, paste the link to your public page on Turo, and click '
             'Add. If you have more than one Turo account, add one line for each.',
          es='En Cuentas de anfitrión de Turo, pegue el enlace de su página pública en Turo, y '
             'pulse Añadir. Si tiene más de una cuenta de Turo, añada una línea por cada una.',
          cam=(0.58, 0.52, 1.16),
          point={'en': (0.944, 0.558), 'es': (0.94, 0.578)},
          click=2.2,
          ring={'en': (0.219, 0.54, 0.72, 0.036), 'es': (0.219, 0.56, 0.68, 0.038)},
          label_en='Turo host accounts', label_es='Cuentas de anfitrión'),

        B(en='Click Import cars. Your phone opens that page and reads your cars. It can take a '
             'minute or two.',
          es='Pulse Importar vehículos. Su teléfono abre esa página y lee sus coches. Puede '
             'tardar un minuto o dos.',
          cam=(0.86, 0.46, 1.24),
          point={'en': (0.935, 0.454), 'es': (0.92, 0.454)},
          click=1.6),

        B(en='Each car comes back with a label. linked means it was matched to one of your '
             'cars by itself. already-linked means it was done before.',
          es='Cada coche vuelve con una etiqueta. linked significa que se emparejó solo con '
             'uno de sus coches. already-linked significa que ya estaba hecho.',
          shot='57-turo-import',
          cam=(0.45, 0.42, 1.18),
          ring={'en': (0.322, 0.175, 0.08, 0.8), 'es': (0.305, 0.175, 0.075, 0.8)},
          label_en='Import cars', label_es='Importar vehículos'),

        B(en='ambiguous means several of your cars could be it; no-match means none. For '
             'those, pick the right car from the list and click Link.',
          es='ambiguous significa que podría ser cualquiera de varios coches suyos; no-match, '
             'que ninguno. Para esos, elija el coche correcto en la lista y pulse Vincular.',
          cam=(0.55, 0.44, 1.3),
          point={'en': (0.605, 0.426), 'es': (0.58, 0.426)},
          click=2.0,
          ring=(0.148, 0.405, 0.69, 0.042)),

        B(en='Re-link moves a listing to a different car. Unlink removes the connection. Both '
             'ask first, and neither changes bookings, history or tolls you already have.',
          es='Volver a vincular mueve un anuncio a otro coche. Desvincular quita la conexión. '
             'Los dos preguntan antes, y ninguno cambia las reservas, el historial ni los '
             'peajes que ya tiene.',
          cam={'en': (0.74, 0.26, 1.4), 'es': (0.72, 0.26, 1.4)},
          ring={'en': (0.715, 0.205, 0.125, 0.035), 'es': (0.652, 0.205, 0.18, 0.035)}),

        B(en='If a Turo car is not in your portal at all, the import will not add it. Add the '
             'car first, as shown in episode five, then import again.',
          es='Si un coche de Turo no está en su portal, la importación no lo añade. Añada '
             'primero el coche, como en el episodio cinco, y vuelva a importar.',
          cam=(0.5, 0.7, 1.3),
          ring=(0.148, 0.707, 0.69, 0.042)),

        B(en='There is also a way without the phone. When you confirm a Turo booking, leave '
             'this box ticked: Remember this listing for the selected car.',
          es='También hay una forma sin el teléfono. Al confirmar una reserva de Turo, deje '
             'marcada esta casilla: Recordar este anuncio para el vehículo seleccionado.',
          shot='59-confirm-taken',
          url='/p2p-bookings/turo',
          cam=(0.5, 0.52, 1.45),
          ring=(0.365, 0.548, 0.27, 0.034),
          label_en='Confirm pending booking', label_es='Confirmar reserva pendiente'),

        B(en='A connection made this way can be moved later, by ticking it again on another '
             'car. To remove it completely, use the import window.',
          es='Una conexión hecha así se puede mover después, marcándola de nuevo con otro '
             'coche. Para quitarla del todo, use la ventana de importación.',
          cam=(0.5, 0.52, 1.45)),

        B(en='Do this once for each identical car, and from then on every Turo booking finds '
             'the right car by itself.',
          es='Hágalo una vez por cada coche idéntico, y a partir de ahí cada reserva de Turo '
             'encontrará sola el coche correcto.',
          shot='57-turo-import',
          url='/settings',
          cam=(0.5, 0.4, 1.0),
          label_en=' ', label_es=' '),
    ])


# =============================================================================== 26
# 53-pending-bookings is the live queue with a "Vehicle taken" row in it; 58 and 59 are the Confirm
# dialog opened on its two rows (capture-screenshots.js opens them and never submits).
EP26 = E(
    26, 'turo-pending',
    'Turo, part 5: pending bookings, and a car that is already taken',
    'Turo, parte 5: reservas pendientes y un coche ya ocupado',
    'Confirming, rejecting, and what to do when two trips want one car',
    'Confirmar, rechazar, y qué hacer cuando dos viajes quieren un coche',
    [
        B(en='Every Turo booking arrives here first: Bookings, then Turo pending bookings. '
             'Many of them do not even stop here.',
          es='Cada reserva de Turo llega primero aquí: Reservas, y después Reservas pendientes '
             'de Turo. Muchas ni siquiera se quedan aquí.',
          shot='53-pending-bookings',
          url='/p2p-bookings/turo',
          cam=(0.5, 0.3, 1.0),
          label_en='Turo pending bookings', label_es='Reservas pendientes de Turo'),

        B(en='When the portal is sure which car it is and who the guest is, it creates the '
             'booking by itself within minutes. What you see in this list is what needs you.',
          es='Cuando el portal está seguro de qué coche es y quién es el huésped, crea la '
             'reserva solo en pocos minutos. Lo que ve en esta lista es lo que le necesita a '
             'usted.',
          cam=(0.55, 0.36, 1.12),
          ring={'en': (0.217, 0.3, 0.752, 0.112), 'es': (0.217, 0.3, 0.752, 0.16)}),

        B(en='Look at the Match column first. Green means sure. Red None means the portal '
             'could not find the car or the driver.',
          es='Mire primero la columna Coincidencia. Verde significa seguro. Rojo, None, '
             'significa que el portal no encontró el coche o el conductor.',
          cam=(0.7, 0.35, 1.28),
          ring={'en': (0.646, 0.321, 0.092, 0.028), 'es': (0.611, 0.338, 0.12, 0.028)},
          label_en='Match', label_es='Coincidencia'),

        B(en='Click Confirm to open the booking before it is created. You see the dates, and '
             'you choose the car and the driver.',
          es='Pulse Confirmar para abrir la reserva antes de crearla. Ve las fechas, y elige '
             'el coche y el conductor.',
          shot='58-confirm-pending',
          cam=(0.5, 0.48, 1.45),
          ring=(0.37, 0.425, 0.26, 0.13),
          label_en='Confirm', label_es='Confirmar'),

        B(en='If the guest is new, click New driver to add them. Below, Will create booking as '
             'tells you what happens next — for example, waiting for a credit card.',
          es='Si el huésped es nuevo, pulse Nuevo conductor para añadirlo. Debajo, La reserva '
             'se creará como le dice qué pasa después: por ejemplo, esperando una tarjeta.',
          cam=(0.5, 0.58, 1.45),
          point=(0.5925, 0.54),
          click=2.2,
          ring=(0.37, 0.578, 0.26, 0.096)),

        B(en='Click Create Booking. If a card or a signature is missing, the guest gets a link '
             'to add it. If you do not want the trip, click Reject in the list instead.',
          es='Pulse Crear reserva. Si falta una tarjeta o una firma, el huésped recibe un '
             'enlace para añadirla. Si no quiere el viaje, pulse Rechazar en la lista.',
          cam=(0.5, 0.62, 1.4),
          point=(0.5825, 0.728),
          click=2.0,
          ring=(0.534, 0.714, 0.097, 0.03)),

        B(en='Now a common problem. A red label that says Vehicle taken means that car is '
             'already booked for some of these days.',
          es='Ahora, un problema habitual. Una etiqueta roja que dice Vehículo ocupado '
             'significa que ese coche ya está reservado en alguno de esos días.',
          shot='53-pending-bookings',
          cam=(0.76, 0.39, 1.3),
          ring={'en': (0.737, 0.374, 0.108, 0.026), 'es': (0.612, 0.432, 0.125, 0.022)},
          label_en='Vehicle taken', label_es='Vehículo ocupado'),

        B(en='Open it, and the window explains it in red. Create Booking stays grey until you '
             'fix it, because one car cannot be with two drivers at once.',
          es='Ábrala, y la ventana lo explica en rojo. Crear reserva sigue en gris hasta que '
             'lo arregle, porque un coche no puede estar con dos conductores a la vez.',
          shot='59-confirm-taken',
          cam=(0.5, 0.47, 1.45),
          ring=(0.37, 0.404, 0.26, 0.136)),

        B(en='The first fix: choose a different, free car in the Car list. The red message '
             'goes away at once.',
          es='El primer arreglo: elija otro coche libre en la lista de Vehículo. El mensaje '
             'rojo desaparece al momento.',
          cam=(0.5, 0.42, 1.45),
          point=(0.5, 0.376),
          click=1.8,
          ring=(0.37, 0.36, 0.26, 0.034)),

        B(en='The second fix is for when the car is really free: the earlier trip came back '
             'early, but the portal still thinks it is out.',
          es='El segundo arreglo es para cuando el coche en realidad está libre: el viaje '
             'anterior volvió antes, pero el portal todavía cree que está fuera.',
          cam=(0.5, 0.47, 1.3)),

        B(en='Go to Bookings, open the menu of that earlier booking, and choose Complete '
             'Early. The car is free from that moment. If that trip never happened, cancel it '
             'instead.',
          es='Vaya a Reservas, abra el menú de esa reserva anterior, y elija Completar antes. '
             'El coche queda libre desde ese momento. Si ese viaje no llegó a ocurrir, '
             'cancélelo.',
          shot='52-booking-row-menu',
          url='/bookings',
          cam=(0.5, 0.52, 1.35),
          point=(0.43, 0.51),
          click=2.6,
          ring=(0.38, 0.497, 0.262, 0.026),
          label_en='Complete Early', label_es='Completar antes'),

        B(en='Drivers have the same rule: one driver, one trip at a time. If the guest already '
             'has a trip with you on those days, fix that trip first.',
          es='Los conductores tienen la misma regla: un conductor, un viaje a la vez. Si el '
             'huésped ya tiene un viaje con usted en esos días, arregle antes ese viaje.',
          cam=(0.5, 0.52, 1.15)),

        B(en='Changes made on Turo come through by themselves. New dates move the booking; a '
             'cancellation cancels it — even after you confirmed it.',
          es='Los cambios hechos en Turo llegan solos. Fechas nuevas mueven la reserva; una '
             'cancelación la cancela, incluso después de que la confirmara.',
          shot='53-pending-bookings',
          url='/p2p-bookings/turo',
          cam=(0.55, 0.36, 1.12),
          ring={'en': (0.217, 0.3, 0.752, 0.112), 'es': (0.217, 0.3, 0.752, 0.16)},
          label_en='Turo pending bookings', label_es='Reservas pendientes de Turo'),

        B(en='Unless the new dates would clash with another booking. Then the change waits, '
             'and the row says Platform dates not applied. The same two fixes work.',
          es='Salvo que las fechas nuevas choquen con otra reserva. Entonces el cambio espera, '
             'y la fila dice Fechas de la plataforma no aplicadas. Sirven los mismos dos '
             'arreglos.',
          cam=(0.76, 0.39, 1.3),
          ring={'en': (0.737, 0.374, 0.108, 0.026), 'es': (0.612, 0.432, 0.125, 0.022)}),

        B(en='Check this list every day or two. A booking that waits here cannot collect a '
             'single toll.',
          es='Revise esta lista cada uno o dos días. Una reserva que espera aquí no puede '
             'cobrar ni un solo peaje.',
          cam=(0.5, 0.3, 1.0),
          label_en=' ', label_es=' '),
    ])
