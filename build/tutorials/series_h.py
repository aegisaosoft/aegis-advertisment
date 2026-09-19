# -*- coding: utf-8 -*-
"""Episodes 20 and 21 — the reports, and the last four settings tabs."""
from model import B, E


# =============================================================================== 20
EP20 = E(
    20, 'reports',
    'Reports', 'Informes',
    'The two documents your accountant actually wants',
    'Los dos documentos que su contable realmente quiere',
    [
        B(en='Reports, then Account Statement. This is a month of your business, in a form '
             'you can hand to somebody.',
          es='Informes, y luego Estado de cuenta. Esto es un mes de su negocio, en un formato '
             'que puede entregar a alguien.',
          shot='95-account-statement-report', url='/reports', cam=(0.5, 0.20, 1.0),
          label_en='Account Statement', label_es='Estado de cuenta'),

        B(en='Pick a year and a month, press Generate Report, and everything below is rebuilt '
             'for that period.',
          es='Elija un año y un mes, pulse Generar informe, y todo lo de abajo se reconstruye '
             'para ese período.',
          cam=(0.5, 0.24, 1.20),
          point=(0.853, 0.246), click=1.7,
          ring=(0.214, 0.230, 0.762, 0.030),
          label_en='Report Parameters', label_es='Parámetros del informe'),

        B(en='Three figures at the top. Total income, total expenses, and the net between '
             'them — the whole month in one line.',
          es='Tres cifras arriba. Ingresos totales, gastos totales, y el neto entre ambos: '
             'todo el mes en una línea.',
          cam=(0.5, 0.33, 1.18),
          ring=(0.201, 0.289, 0.790, 0.080),
          label_en='Income, expenses, net', label_es='Ingresos, gastos, neto'),

        B(en='Below them, every transaction that made up those figures. This is not a summary '
             '— it is the ledger.',
          es='Debajo, cada transacción que formó esas cifras. Esto no es un resumen: es el '
             'libro mayor.',
          cam=(0.5, 0.56, 1.12),
          ring=(0.216, 0.490, 0.750, 0.290),
          label_en='Transaction Details', label_es='Detalle de transacciones'),

        B(en='Category and type classify each line — Owner Share, Income — and the '
             'description names where it came from: which toll provider, or Stripe.',
          es='Categoría y tipo clasifican cada línea — Parte del propietario, Ingreso — y la '
             'descripción dice de dónde vino: qué proveedor de peaje, o Stripe.',
          cam=(0.52, 0.56, 1.24),
          ring=(0.476, 0.490, 0.164, 0.290)),

        B(en='And every line carries a transaction ID. That is the reference that ties a '
             'figure in this report back to a specific charge, which is what makes the report '
             'auditable rather than merely tidy.',
          es='Y cada línea lleva un identificador de transacción. Esa es la referencia que ata '
             'una cifra de este informe a un cargo concreto, y es lo que lo hace auditable en '
             'vez de solo ordenado.',
          cam=(0.82, 0.56, 1.24),
          ring=(0.748, 0.490, 0.204, 0.290),
          label_en='Transaction ID', label_es='ID de transacción'),

        B(en='Download Excel or Download PDF, and what comes out is what is on screen. The '
             'notice at the bottom says it plainly: suitable for tax submission, and check '
             'your own jurisdiction with your own advisor.',
          es='Descargar Excel o Descargar PDF, y lo que sale es lo que hay en pantalla. El '
             'aviso del final lo dice claro: sirve para la declaración de impuestos, y '
             'consulte su jurisdicción con su propio asesor.',
          cam=(0.86, 0.11, 1.24),
          point=(0.936, 0.103), click=1.6,
          ring=(0.760, 0.088, 0.234, 0.030)),

        B(en='Then the Annual Report, which is the same idea over a year.',
          es='Después, el Informe anual, que es la misma idea pero de un año.',
          shot='96-annual-report', cam=(0.5, 0.22, 1.0),
          label_en='Annual Report', label_es='Informe anual'),

        B(en='One parameter — the year — and four figures instead of three. The fourth is '
             'active vehicles and the transaction count behind them, which is the number that '
             'tells you whether the year’s income came from the whole fleet or from three '
             'cars.',
          es='Un solo parámetro, el año, y cuatro cifras en vez de tres. La cuarta son los '
             'vehículos activos y el número de transacciones detrás, que es la cifra que le '
             'dice si los ingresos del año vinieron de toda la flota o de tres coches.',
          cam=(0.5, 0.40, 1.14),
          ring=(0.201, 0.350, 0.790, 0.109),
          label_en='Four figures', label_es='Cuatro cifras'),

        B(en='Monthly Breakdown is the year month by month, with income, expenses and net on '
             'each row. This is the view that shows you your season.',
          es='Desglose mensual es el año mes a mes, con ingresos, gastos y neto en cada fila. '
             'Esta es la vista que le enseña su temporada.',
          cam=(0.5, 0.545, 1.16),
          ring=(0.201, 0.476, 0.790, 0.163),
          label_en='Monthly Breakdown', label_es='Desglose mensual'),

        B(en='And Category Breakdown is where the money came from, as a share of the whole. '
             'One bar at a hundred percent means one source — which is worth knowing before '
             'that source changes its terms.',
          es='Y Desglose por categoría es de dónde vino el dinero, como porcentaje del total. '
             'Una sola barra al cien por cien significa una sola fuente, y conviene saberlo '
             'antes de que esa fuente cambie sus condiciones.',
          cam=(0.5, 0.73, 1.16),
          ring=(0.201, 0.658, 0.790, 0.148),
          label_en='Category Breakdown', label_es='Desglose por categoría'),
    ])


# =============================================================================== 21
EP21 = E(
    21, 'extras',
    'Services, invitations and partners', 'Servicios, invitaciones y socios',
    'The four settings tabs that are easy to miss',
    'Las cuatro pestañas de configuración fáciles de pasar por alto',
    [
        B(en='Four tabs on the settings page we have not opened yet, and each one earns its '
             'place. Start with Services.',
          es='Cuatro pestañas de la página de configuración que aún no hemos abierto, y cada '
             'una se gana su sitio. Empecemos por Servicios.',
          shot='35-settings-services', url='/owners/settings', cam=(0.5, 0.30, 1.0),
          point=(0.703, 0.199), click=1.6,
          label_en='Settings → Services', label_es='Configuración → Servicios'),

        B(en='These are the extras a driver is offered at booking time: insurance, a child '
             'seat, a GPS unit. Name, price, currency.',
          es='Estos son los extras que se le ofrecen al conductor al reservar: seguro, silla '
             'infantil, un GPS. Nombre, precio, moneda.',
          cam=(0.5, 0.34, 1.22),
          ring=(0.214, 0.328, 0.758, 0.037),
          label_en='Additional services', label_es='Servicios adicionales'),

        B(en='Pricing is the part to get right: per minute, per hour, per day, per week, per '
             'month, a percentage, or one time. A child seat priced per day and a cleaning fee '
             'priced one time are very different amounts on a two-week rental.',
          es='El precio es la parte que hay que acertar: por minuto, por hora, por día, por '
             'semana, por mes, un porcentaje, o una sola vez. Una silla infantil por día y una '
             'tarifa de limpieza de una sola vez son cantidades muy distintas en un alquiler '
             'de dos semanas.',
          cam=(0.34, 0.42, 1.28),
          point=(0.34, 0.412), click=1.8,
          ring=(0.214, 0.392, 0.251, 0.037),
          label_en='Pricing', label_es='Precio'),

        B(en='Mandatory adds the service to every booking whether the driver picks it or not. '
             'Active is what takes it off the list without deleting it. Then Add service.',
          es='Obligatorio añade el servicio a cada reserva, lo elija el conductor o no. Activo '
             'es lo que lo quita de la lista sin borrarlo. Y luego, Añadir servicio.',
          cam=(0.5, 0.45, 1.26),
          point=(0.226, 0.455), click=1.5,
          ring=(0.212, 0.441, 0.132, 0.030)),

        B(en='Next, Invitation Messages. Every invitation the system sends a driver comes from '
             'a template, and these are the templates.',
          es='Después, Mensajes de invitación. Cada invitación que el sistema envía a un '
             'conductor sale de una plantilla, y estas son las plantillas.',
          shot='36-settings-invitations', cam=(0.5, 0.32, 1.0),
          point=(0.804, 0.199), click=1.5,
          label_en='Invitation Messages', label_es='Mensajes de invitación'),

        B(en='Pick which message, and which language. The star tells you English is the base '
             'language: edit that one, and the rest are filled in from it.',
          es='Elija qué mensaje, y en qué idioma. La estrella le dice que el inglés es el '
             'idioma base: edite ese, y el resto se rellena a partir de él.',
          cam=(0.5, 0.35, 1.22),
          ring=(0.214, 0.328, 0.758, 0.068)),

        B(en='The body is yours to write, and the chips underneath are the placeholders the '
             'system fills in: the driver’s name, the vehicle, the dates, the link they need '
             'to click. Click one to insert it.',
          es='El cuerpo es suyo, y las etiquetas de debajo son los marcadores que rellena el '
             'sistema: el nombre del conductor, el vehículo, las fechas, el enlace que tiene '
             'que pulsar. Pulse uno para insertarlo.',
          cam=(0.5, 0.52, 1.20),
          ring=(0.214, 0.424, 0.758, 0.204),
          label_en='Placeholders', label_es='Marcadores'),

        B(en='Write it once in English, press Auto-translate all languages, and every other '
             'language is regenerated from what you just wrote. Preview shows it as the driver '
             'will get it.',
          es='Escríbalo una vez en inglés, pulse Traducir automáticamente todos los idiomas, y '
             'todos los demás se regeneran a partir de lo que acaba de escribir. Vista previa '
             'lo muestra como lo recibirá el conductor.',
          cam=(0.80, 0.65, 1.26),
          point=(0.893, 0.653), click=1.6,
          ring=(0.812, 0.632, 0.161, 0.040),
          label_en='Auto-translate', label_es='Traducir automáticamente'),

        B(en='Turo Agents appears when a peer-to-peer platform is configured. The card at the '
             'top is the phone app that talks to the platform on your behalf, and "one of one '
             'online" is the only state you want to see.',
          es='Agentes de Turo aparece cuando hay una plataforma entre particulares '
             'configurada. La tarjeta de arriba es la aplicación de teléfono que habla con la '
             'plataforma en su nombre, y "uno de uno en línea" es el único estado que quiere '
             'ver.',
          shot='38-settings-turo-agents', cam=(0.5, 0.30, 1.04),
          point=(0.949, 0.199), click=1.5,
          ring=(0.201, 0.248, 0.787, 0.149),
          label_en='Turo Agents', label_es='Agentes de Turo'),

        B(en='Underneath, host accounts. Paste the address of a host page, press Add, and then '
             'Import cars reads that page and matches its vehicles against your fleet — with '
             'no platform login needed at all.',
          es='Debajo, cuentas de anfitrión. Pegue la dirección de una página de anfitrión, '
             'pulse Añadir, y después Importar coches lee esa página y empareja sus vehículos '
             'con su flota, sin necesidad de ningún inicio de sesión en la plataforma.',
          cam=(0.5, 0.56, 1.18),
          point=(0.50, 0.558), click=1.9,
          ring=(0.214, 0.536, 0.758, 0.044),
          label_en='Turo host accounts', label_es='Cuentas de anfitrión'),

        B(en='And last, Partners. Invite Partner sends someone the link that ties their '
             'account to yours, and Export Excel takes the list away with you.',
          es='Y por último, Socios. Invitar socio envía a alguien el enlace que ata su cuenta '
             'a la suya, y Exportar Excel se lleva la lista consigo.',
          shot='99-partners', url='/partners', cam=(0.5, 0.24, 1.02),
          point=(0.778, 0.133), click=1.5,
          ring=(0.730, 0.114, 0.257, 0.036),
          label_en='Partners', label_es='Socios'),

        B(en='A partner is somebody who brought you business and takes a share of what it '
             'earns — that Pending Partner Share tile from episode fourteen. An empty list '
             'here simply means nobody did.',
          es='Un socio es alguien que le trajo negocio y se lleva parte de lo que produce: esa '
             'casilla de Parte pendiente del socio del episodio catorce. Una lista vacía aquí '
             'significa sencillamente que nadie lo hizo.',
          cam=(0.5, 0.30, 1.10),
          ring=(0.214, 0.196, 0.704, 0.042)),

        B(en='That is the portal, end to end. Every screen it has, and what each one is '
             'actually for.',
          es='Ese es el portal, de principio a fin. Todas las pantallas que tiene, y para qué '
             'sirve de verdad cada una.',
          cam=(0.5, 0.24, 1.02), label_en=' ', label_es=' '),
    ])
