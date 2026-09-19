# -*- coding: utf-8 -*-
"""Episodes 1 to 5 — finding your way around, and setting the business up.

Every line is written against what the screenshot in `docs/images/<lang>/` actually
shows. Where the written guide describes a field the capture does not contain, the
field is left for the guide rather than narrated over a screen that has no such
control on it.
"""
from model import B, E


# =============================================================================== 01
EP01 = E(
    1, 'tour',
    'A tour of the portal', 'Un recorrido por el portal',
    'Where everything lives, and the one setting that hides your data',
    'Dónde está cada cosa, y el ajuste que le esconde sus datos',
    [
        B(en='Sign in at owner.myeztoll.com and this is the first thing you see: '
             'the Control Panel.',
          es='Entre en owner.myeztoll.com y esto es lo primero que ve: '
             'el Panel de Control.',
          say_en='Sign in at owner dot my e z toll dot com and this is the first thing '
                 'you see: the Control Panel.',
          say_es='Entre en owner punto my e z toll punto com y esto es lo primero que ve: '
                 'el Panel de Control.',
          shot='01-dashboard', url='/dashboard', cam=(0.5, 0.42, 1.0),
          label_en='The Control Panel', label_es='El Panel de Control'),

        B(en='Twelve cards, one for each thing you will do here. Each one carries a live '
             'number: how many vehicles you have, how many payments need attention.',
          es='Doce tarjetas, una por cada cosa que hará aquí. Cada una lleva un número '
             'real: cuántos vehículos tiene, cuántos pagos necesitan atención.',
          cam=(0.55, 0.42, 1.12),
          ring=(0.395, 0.415, 0.205, 0.235)),

        B(en='The real navigation is the sidebar on the left, and it is grouped by job '
             'rather than by screen.',
          es='La navegación de verdad es la barra lateral izquierda, agrupada por tarea '
             'y no por pantalla.',
          cam=(0.30, 0.48, 1.18),
          ring=(0.0, 0.262, 0.190, 0.485),
          label_en='The sidebar', label_es='La barra lateral'),

        B(en='Company, Billing, Bookings, Vehicles, Drivers, Partnership, Payments, '
             'Tolls and Violations, Reports, SMS and Mail, Administration. Click a group '
             'to open it.',
          es='Compañía, Facturación, Reservas, Vehículos, Conductores, Sociedad, Pagos, '
             'Peajes y Multas, Informes, SMS y Correo, Administración. Haga clic en un '
             'grupo para abrirlo.',
          cam=(0.24, 0.50, 1.30),
          point=(0.094, 0.735), click=1.5),

        B(en='The group unfolds in place. Nothing you were looking at goes away.',
          es='El grupo se despliega ahí mismo. Nada de lo que estaba mirando desaparece.',
          shot='02-navigation-menu', cam=(0.24, 0.60, 1.30),
          point=(0.094, 0.825),
          ring=(0.0, 0.720, 0.190, 0.200)),

        B(en='Top right: the language selector. Everything in this series works exactly '
             'the same in any of the languages listed there.',
          es='Arriba a la derecha: el selector de idioma. Todo en esta serie funciona '
             'igual en cualquiera de los idiomas de esa lista.',
          cam=(0.80, 0.10, 1.32),
          point={'en': (0.878, 0.042), 'es': (0.853, 0.041)},
          ring={'en': (0.855, 0.026, 0.048, 0.032), 'es': (0.830, 0.025, 0.047, 0.031)},
          label_en='Language', label_es='Idioma'),

        B(en='Next to it, Help. It knows which page you are on and answers about that '
             'page, not about the product in general.',
          es='A su lado, Ayuda. Sabe en qué página está y responde sobre esa página, '
             'no sobre el producto en general.',
          cam={'en': (0.76, 0.10, 1.32), 'es': (0.73, 0.10, 1.32)},
          point={'en': (0.820, 0.042), 'es': (0.789, 0.041)},
          ring={'en': (0.793, 0.026, 0.054, 0.032), 'es': (0.762, 0.025, 0.055, 0.031)},
          label_en='Help', label_es='Ayuda'),

        B(en='And top left, your company name. This one matters more than it looks.',
          es='Y arriba a la izquierda, el nombre de su compañía. Este importa más de lo '
             'que parece.',
          cam=(0.16, 0.16, 1.32),
          point=(0.10, 0.135),
          ring=(0.010, 0.098, 0.180, 0.085),
          label_en='Who you are working as', label_es='Como quién está trabajando'),

        B(en='If you are an administrator or a partner, you can work as any owner you '
             'have access to, and every page then shows that owner and no one else.',
          es='Si es administrador o socio, puede trabajar como cualquier propietario al '
             'que tenga acceso, y cada página muestra a ese propietario y a nadie más.',
          cam=(0.16, 0.16, 1.32)),

        B(en='So when a page looks empty and you are sure it should not be, look here '
             'first. Working as the wrong owner is the single most common reason a '
             'screen comes up blank.',
          es='Así que cuando una página se vea vacía y usted esté seguro de que no debería '
             'estarlo, mire aquí primero. Trabajar como el propietario equivocado es la '
             'causa más común de una pantalla en blanco.',
          cam=(0.16, 0.16, 1.32),
          ring=(0.010, 0.098, 0.180, 0.085), hold=0.5),

        B(en='That is the whole map. In the next episode we set the rules your business '
             'runs on, before a single booking exists.',
          es='Ese es todo el mapa. En el siguiente episodio fijamos las reglas con las que '
             'funciona su negocio, antes de que exista una sola reserva.',
          shot='01-dashboard', cam=(0.5, 0.42, 1.0), label_en=' ', label_es=' '),
    ])


# =============================================================================== 02
EP02 = E(
    2, 'settings',
    'The settings that decide everything', 'Los ajustes que lo deciden todo',
    'Company → Settings, before a single booking exists',
    'Compañía → Configuración, antes de que exista una sola reserva',
    [
        B(en='Company, then Settings. This page decides how your business behaves, and it '
             'is worth ten minutes before you take a single booking.',
          es='Compañía, y luego Configuración. Esta página decide cómo se comporta su '
             'negocio, y vale diez minutos antes de aceptar una sola reserva.',
          shot='30-settings-owner', url='/owners/settings', cam=(0.5, 0.14, 1.0),
          label_en='Company → Settings', label_es='Compañía → Configuración'),

        B(en='The tabs across the top are separate settings pages that happen to share one '
             'Save button. Toll Accounts, GPS Systems and Services each get an episode of '
             'their own later on.',
          es='Las pestañas de arriba son páginas de configuración distintas que comparten '
             'un mismo botón Guardar. Cuentas de peaje, GPS Systems y Servicios tienen su '
             'propio episodio más adelante.',
          cam=(0.5, 0.15, 1.14),
          ring=(0.203, 0.121, 0.792, 0.033)),

        B(en='This line says whose settings you are editing. On a platform with several '
             'owners on it, read that line before you change anything.',
          es='Esta línea dice de quién son los ajustes que está editando. En una plataforma '
             'con varios propietarios, léala antes de cambiar nada.',
          cam=(0.5, 0.185, 1.20),
          ring=(0.203, 0.174, 0.783, 0.026)),

        B(en='Company and Domain. The name here is the one your renters see on your '
             'storefront, and the domain is the web address that storefront answers on.',
          es='Empresa y dominio. El nombre de aquí es el que ven sus arrendatarios en su '
             'sitio, y el dominio es la dirección web en la que ese sitio responde.',
          cam=(0.5, 0.245, 1.22),
          ring=(0.203, 0.207, 0.783, 0.130),
          label_en='Company and Domain', label_es='Empresa y dominio'),

        B(en='Type the part you want in front of .myezwheels.com and press Create domain. '
             'Without a domain your vehicles have nowhere to be listed.',
          es='Escriba la parte que quiera delante de .myezwheels.com y pulse Crear dominio. '
             'Sin dominio sus vehículos no tienen dónde publicarse.',
          say_en='Type the part you want in front of dot my e z wheels dot com and press '
                 'Create domain. Without a domain your vehicles have nowhere to be listed.',
          say_es='Escriba la parte que quiera delante de punto my e z wheels punto com y '
                 'pulse Crear dominio. Sin dominio sus vehículos no tienen dónde publicarse.',
          cam=(0.62, 0.255, 1.30),
          point=(0.75, 0.281), click=1.4,
          ring=(0.598, 0.267, 0.300, 0.024)),

        B(en='Below it, Configuration. Minimum security deposit: any vehicle whose deposit '
             'is set lower than this is raised to it automatically.',
          es='Debajo, Configuración. Depósito de seguridad mínimo: todo vehículo cuyo '
             'depósito sea menor que este se sube automáticamente a este valor.',
          cam=(0.30, 0.405, 1.28),
          ring=(0.213, 0.376, 0.252, 0.064),
          label_en='Configuration', label_es='Configuración'),

        B(en='Charge uncertain GPS tolls. Off by default, and worth leaving off: it decides '
             'whether to bill low-confidence GPS-only tolls — the gantries with a free lane '
             'running alongside, which can false-match.',
          es='Cobrar peajes GPS inciertos. Desactivado por defecto, y conviene dejarlo así: '
             'decide si se facturan los peajes solo-GPS de baja confianza, los pórticos con '
             'un carril libre al lado, que pueden dar falsos positivos.',
          cam=(0.60, 0.405, 1.28),
          point=(0.705, 0.418),
          ring=(0.468, 0.381, 0.258, 0.054)),

        B(en='Retry declined toll charges. Also off by default. On, a card declined for a '
             'transient reason is retried over the following days. Off, the toll is left as '
             'failed for you to handle. Either way the renter gets a link to fix the card.',
          es='Reintentar cobros de peaje rechazados. También desactivado por defecto. '
             'Activado, una tarjeta rechazada por un motivo transitorio se reintenta los '
             'días siguientes. Desactivado, el peaje queda como fallido para que usted lo '
             'gestione. En ambos casos el arrendatario recibe un enlace para corregir la '
             'tarjeta.',
          cam=(0.84, 0.405, 1.24),
          point=(0.960, 0.418),
          ring=(0.723, 0.376, 0.252, 0.082)),

        B(en='Cleaning fee and smoking fee sit beside them, and minimum reservation days on '
             'the right. All three are defaults rather than rules: a vehicle can carry its '
             'own.',
          es='La tarifa de limpieza y la multa por fumar están al lado, y los días mínimos '
             'de reserva a la derecha. Los tres son valores por defecto y no reglas: un '
             'vehículo puede llevar los suyos.',
          cam=(0.5, 0.487, 1.24),
          ring=(0.213, 0.467, 0.762, 0.054)),

        B(en='And this block is the one that saves the most time. Pricing period, insurance, '
             'price per week, colours — every new vehicle you add starts with these already '
             'filled in.',
          es='Y este bloque es el que más tiempo ahorra. Período de precios, seguros, precio '
             'semanal, colores: cada vehículo nuevo que añada empieza con esto ya rellenado.',
          cam=(0.5, 0.595, 1.16),
          ring=(0.213, 0.538, 0.762, 0.118),
          label_en='Defaults for new vehicles', label_es='Valores por defecto'),

        B(en='Further down, Email Relay. You register a public alias at mail.myeztoll.com, '
             'and everything sent to it is forwarded to your real address.',
          es='Más abajo, Reenvío de correo. Usted registra un alias público en '
             'mail.myeztoll.com, y todo lo que llegue ahí se reenvía a su dirección real.',
          say_en='Further down, Email Relay. You register a public alias at mail dot my e z '
                 'toll dot com, and everything sent to it is forwarded to your real address.',
          say_es='Más abajo, Reenvío de correo. Usted registra un alias público en mail punto '
                 'my e z toll punto com, y todo lo que llegue ahí se reenvía a su dirección '
                 'real.',
          cam=(0.5, 0.755, 1.14),
          ring=(0.203, 0.673, 0.783, 0.242),
          label_en='Email Relay', label_es='Reenvío de correo'),

        B(en='Replies you send back go out through the alias, so the driver never learns '
             'your real email address.',
          es='Las respuestas que usted envíe salen por el alias, así que el conductor nunca '
             'llega a conocer su correo real.',
          cam=(0.36, 0.742, 1.30),
          point=(0.36, 0.744),
          ring=(0.213, 0.726, 0.302, 0.028)),

        B(en='One switch turns the whole relay off, and inbound mail is bounced instead of '
             'forwarded.',
          es='Un interruptor apaga todo el reenvío, y el correo entrante se rechaza en vez '
             'de reenviarse.',
          cam=(0.72, 0.790, 1.26),
          point=(0.960, 0.794),
          ring=(0.213, 0.778, 0.762, 0.032)),

        B(en='Then Save, at the top right. Leaving the page with unsaved changes asks you '
             'first — but it is easier to press Save.',
          es='Y luego Guardar, arriba a la derecha. Salir de la página con cambios sin '
             'guardar le pregunta antes, pero es más fácil pulsar Guardar.',
          cam=(0.74, 0.10, 1.28),
          point=(0.955, 0.097), click=1.5,
          ring=(0.916, 0.082, 0.074, 0.030),
          label_en='Save', label_es='Guardar'),
    ])
