# -*- coding: utf-8 -*-
"""Episodes 12 to 14 — payments that failed, the Stripe connection, and the payout."""
from model import B, E


# =============================================================================== 12
EP12 = E(
    12, 'payments',
    'Failed payments and disputes', 'Pagos fallidos y disputas',
    'The two screens where money is still recoverable',
    'Las dos pantallas donde el dinero todavía se puede recuperar',
    [
        B(en='Payments, then Failed Payments. This is the page that pays for itself, and it '
             'is the one most owners never open.',
          es='Pagos, y luego Pagos fallidos. Esta es la página que se paga sola, y es la que '
             'la mayoría de propietarios nunca abre.',
          shot='64-failed-payments', url='/failed-payments', cam=(0.5, 0.35, 1.0),
          label_en='Failed Payments', label_es='Pagos fallidos'),

        B(en='It splits into two tabs, and the split is the whole idea. Driver Assigned means '
             'we know who was driving and the card simply refused — those are recoverable.',
          es='Se divide en dos pestañas, y esa división es toda la idea. Con conductor '
             'asignado significa que sabemos quién conducía y la tarjeta simplemente rechazó: '
             'esos son recuperables.',
          cam=(0.34, 0.33, 1.26),
          point=(0.406, 0.325), click=1.6,
          ring=(0.204, 0.301, 0.264, 0.051),
          label_en='Two tabs', label_es='Dos pestañas'),

        B(en='No Driver Assigned is the harder half: a toll with no booking behind it, so '
             'there is nobody to bill. That is the transponder problem from episode six, or a '
             'booking that was never created.',
          es='Sin conductor asignado es la mitad difícil: un peaje sin reserva detrás, así que '
             'no hay a quién facturar. Ese es el problema de transpondedores del episodio '
             'seis, o una reserva que nunca se creó.',
          cam=(0.30, 0.33, 1.26),
          point=(0.267, 0.325), click=1.5),

        B(en='The banner totals whichever half you are looking at. That figure is money you '
             'have already spent and not yet got back.',
          es='El banner suma la mitad que esté mirando. Esa cifra es dinero que usted ya ha '
             'gastado y todavía no ha recuperado.',
          cam=(0.5, 0.39, 1.24),
          ring=(0.216, 0.378, 0.756, 0.042),
          label_en='The total', label_es='El total'),

        B(en='Work the Driver Assigned tab first. A failed card is usually transient — expired, '
             'over its limit, a bank that blocked an unfamiliar merchant — and re-running it '
             'after the driver updates the card collects it.',
          es='Trabaje primero la pestaña con conductor asignado. Una tarjeta fallida suele ser '
             'algo pasajero — caducada, sin límite, un banco que bloqueó a un comercio '
             'desconocido — y volver a intentarlo tras actualizar la tarjeta lo cobra.',
          cam=(0.5, 0.35, 1.0)),

        B(en='Successful Payments is the mirror image, and it is the one to check when a '
             'driver says they were charged twice.',
          es='Pagos exitosos es la imagen reflejada, y es la que hay que mirar cuando un '
             'conductor dice que se le cobró dos veces.',
          shot='65-successful-payments', url='/successful-payments', cam=(0.5, 0.35, 1.0),
          label_en='Successful Payments', label_es='Pagos exitosos'),

        B(en='Same two tabs, same totals, opposite outcome. Between the two pages you can '
             'account for every toll that has ever been billed on this fleet.',
          es='Las mismas dos pestañas, los mismos totales, el resultado opuesto. Entre las dos '
             'páginas puede dar cuenta de cada peaje que se haya facturado en esta flota.',
          cam=(0.5, 0.39, 1.22),
          ring=(0.216, 0.378, 0.756, 0.042)),

        B(en='Then Disputes, which is different in kind: a driver has gone to their bank and '
             'asked for the money back.',
          es='Después, Disputas, que es de otra naturaleza: un conductor ha ido a su banco y '
             'ha pedido que le devuelvan el dinero.',
          shot='66-disputes', url='/disputes', cam=(0.5, 0.30, 1.0),
          label_en='Disputes', label_es='Disputas'),

        B(en='Three numbers tell you where you stand. Needs Response is the only one with a '
             'clock on it — a dispute with no answer by its deadline is lost automatically, '
             'whatever the facts were.',
          es='Tres cifras le dicen dónde está. Necesita respuesta es la única con un reloj: '
             'una disputa sin respuesta antes de su fecha límite se pierde automáticamente, '
             'sean cuales sean los hechos.',
          cam=(0.30, 0.23, 1.28),
          ring=(0.200, 0.172, 0.256, 0.118),
          label_en='Needs Response', label_es='Necesita respuesta'),

        B(en='Total Open Amount is what is currently at risk, and Win Rate over ninety days '
             'is how you have been doing. A fleet that can produce the trip and the toll '
             'record behind a charge tends to win them.',
          es='Importe abierto total es lo que está en riesgo ahora, y la tasa de éxito a '
             'noventa días es cómo le ha ido. Una flota que puede aportar el viaje y el '
             'registro del peaje detrás de un cargo suele ganarlas.',
          cam=(0.72, 0.23, 1.24),
          ring=(0.466, 0.172, 0.520, 0.118)),

        B(en='The table below carries the deadline, the reason the bank gave, and an Auto '
             'Response column: the system can answer routine disputes on its own, with the '
             'trip and the toll record attached as evidence.',
          es='La tabla de abajo lleva la fecha límite, el motivo que dio el banco, y una '
             'columna de respuesta automática: el sistema puede contestar disputas rutinarias '
             'por sí solo, adjuntando el viaje y el registro del peaje como prueba.',
          cam=(0.5, 0.51, 1.20),
          ring=(0.214, 0.506, 0.756, 0.042),
          label_en='Auto Response', label_es='Respuesta automática'),

        B(en='Refresh from Stripe pulls the current state straight from Stripe, because a '
             'dispute changes on their side, not on ours.',
          es='Actualizar desde Stripe trae el estado actual directamente de Stripe, porque una '
             'disputa cambia en su lado, no en el nuestro.',
          cam=(0.84, 0.14, 1.26),
          point=(0.922, 0.134), click=1.4,
          ring=(0.854, 0.115, 0.132, 0.038)),
    ])


# =============================================================================== 13
EP13 = E(
    13, 'banking',
    'Stripe, banking and invoices', 'Stripe, banca y facturas',
    'Without this connection nothing can be collected or paid out',
    'Sin esta conexión no se puede cobrar ni pagar nada',
    [
        B(en='Banking. Everything in the last four episodes assumed money can move. This is '
             'the page where that becomes true.',
          es='Banca. Todo lo de los últimos cuatro episodios daba por hecho que el dinero '
             'puede moverse. Esta es la página donde eso se vuelve cierto.',
          shot='68-banking', url='/banking', cam=(0.5, 0.28, 1.0),
          label_en='Banking', label_es='Banca'),

        B(en='Three tabs. Owner Account is your Stripe connection. Payment Methods is the '
             'cards on file. Settlement Settings is how and when you are paid.',
          es='Tres pestañas. Cuenta del propietario es su conexión con Stripe. Métodos de pago '
             'son las tarjetas guardadas. Ajustes de liquidación es cómo y cuándo se le paga.',
          cam=(0.36, 0.20, 1.26),
          ring=(0.203, 0.174, 0.329, 0.049)),

        B(en='The Stripe Connected Account card is the one that matters, and it is readable at '
             'a glance: green means it works.',
          es='La tarjeta de Cuenta conectada de Stripe es la que importa, y se lee de un '
             'vistazo: verde significa que funciona.',
          cam=(0.5, 0.30, 1.18),
          ring=(0.201, 0.248, 0.787, 0.134),
          label_en='Stripe Connected Account', label_es='Cuenta conectada de Stripe'),

        B(en='Onboarding Complete means Stripe has everything it needs about your business. '
             'Until that says so, nothing else on the card can be true.',
          es='Alta completada significa que Stripe tiene todo lo que necesita sobre su '
             'negocio. Hasta que eso lo diga, nada más de la tarjeta puede ser cierto.',
          cam=(0.30, 0.34, 1.30),
          ring=(0.214, 0.331, 0.108, 0.032)),

        B(en='Charges Enabled is permission to take money from drivers. Payouts Enabled is '
             'permission to send money to you. They are separate, and one can be on while the '
             'other is not.',
          es='Cobros habilitados es el permiso para cobrar a los conductores. Pagos '
             'habilitados es el permiso para enviarle dinero a usted. Son separados, y uno '
             'puede estar activo mientras el otro no.',
          cam=(0.42, 0.34, 1.30),
          ring=(0.322, 0.332, 0.154, 0.030),
          label_en='Two separate permissions', label_es='Dos permisos separados'),

        B(en='If either is off, the fix is on Stripe’s side, not here: they are waiting for a '
             'document. The refresh button re-reads the account once you have given it to '
             'them.',
          es='Si alguno está apagado, el arreglo está en el lado de Stripe, no aquí: están '
             'esperando un documento. El botón de actualizar vuelve a leer la cuenta cuando ya '
             'se lo haya dado.',
          cam=(0.86, 0.29, 1.28),
          point=(0.960, 0.289), click=1.5),

        B(en='Disconnect is there, and it does exactly what it says. Pressing it stops '
             'collection on every vehicle at once, so treat it as a last resort.',
          es='Desconectar está ahí, y hace exactamente lo que dice. Pulsarlo detiene el cobro '
             'en todos los vehículos a la vez, así que trátelo como último recurso.',
          cam=(0.84, 0.33, 1.28),
          point=(0.935, 0.331),
          ring=(0.896, 0.315, 0.078, 0.032)),

        B(en='Then Invoices to Pay, which is the other direction: what your company owes.',
          es='Después, Facturas por pagar, que es la otra dirección: lo que su empresa debe.',
          shot='69-invoices-to-pay', url='/invoices-to-pay', cam=(0.5, 0.28, 1.0),
          label_en='Invoices to pay', label_es='Facturas por pagar'),

        B(en='One row per billing period, with the amount and a status. Open is outstanding. '
             'Void is one that was cancelled and needs nothing from you.',
          es='Una fila por período de facturación, con el importe y un estado. Abierta está '
             'pendiente. Anulada es una que se canceló y no necesita nada de usted.',
          cam=(0.5, 0.30, 1.20),
          ring=(0.238, 0.248, 0.724, 0.150)),

        B(en='Only Open is actionable, and the row menu is where you pay it.',
          es='Solo Abierta requiere acción, y el menú de la fila es donde se paga.',
          cam=(0.62, 0.30, 1.28),
          point=(0.229, 0.299), click=1.3,
          ring=(0.824, 0.286, 0.040, 0.030)),

        B(en='The Show filter defaults to All, so a short list here is a short list — not a '
             'filter hiding something from you.',
          es='El filtro Mostrar viene en Todas, así que una lista corta aquí es una lista '
             'corta, no un filtro escondiéndole algo.',
          cam=(0.32, 0.22, 1.28),
          point=(0.278, 0.213), click=1.3,
          ring=(0.216, 0.194, 0.094, 0.038)),
    ])


# =============================================================================== 14
EP14 = E(
    14, 'distributions',
    'Toll distributions and payouts', 'Distribución de peajes y pagos',
    'Where the money you collected is split, and when it reaches you',
    'Dónde se reparte lo cobrado, y cuándo le llega',
    [
        B(en='Administration, then Toll Distributions. Everything collected from drivers ends '
             'up on this page, split between everyone with a claim on it.',
          es='Administración, y luego Distribución de peajes. Todo lo cobrado a los '
             'conductores acaba en esta página, repartido entre todos los que tienen derecho '
             'a algo.',
          shot='71-distribution-settings', url='/toll-distributions', cam=(0.5, 0.30, 1.0),
          label_en='Toll Distribution Settings', label_es='Ajustes de distribución'),

        B(en='Balance Overview reads top-left to bottom-right, and it is worth reading in that '
             'order. Pending Tolls is how many tolls are in this balance — a count, not money.',
          es='Resumen de saldo se lee de arriba a la izquierda hacia abajo a la derecha, y '
             'merece leerse en ese orden. Peajes pendientes es cuántos peajes hay en este '
             'saldo: un recuento, no dinero.',
          cam=(0.34, 0.27, 1.24),
          ring=(0.243, 0.244, 0.229, 0.064),
          label_en='Balance Overview', label_es='Resumen de saldo'),

        B(en='Gross Amount is what was taken from drivers. Stripe Fees is what the card '
             'network kept, and it is shown in red because it is the one number nobody in this '
             'picture gets.',
          es='Importe bruto es lo que se cobró a los conductores. Comisiones de Stripe es lo '
             'que se quedó la red de tarjetas, y sale en rojo porque es la única cifra que '
             'nadie de esta foto recibe.',
          cam=(0.72, 0.27, 1.22),
          ring=(0.482, 0.244, 0.468, 0.064),
          label_en='Gross, and what Stripe kept', label_es='Bruto, y lo de Stripe'),

        B(en='Net Amount is gross minus those fees — the real money that arrived, and the '
             'figure everything below is divided out of.',
          es='Importe neto es el bruto menos esas comisiones: el dinero real que llegó, y la '
             'cifra de la que se reparte todo lo de abajo.',
          cam=(0.34, 0.345, 1.26),
          ring=(0.243, 0.320, 0.229, 0.064),
          label_en='Net Amount', label_es='Importe neto'),

        B(en='Then the shares. Pending Owner Share is yours and not yet sent. Pending Partner '
             'Share is a partner’s, if a partner referred this business.',
          es='Luego, las partes. Parte pendiente del propietario es la suya, aún sin enviar. '
             'Parte pendiente del socio es la de un socio, si un socio trajo este negocio.',
          cam=(0.72, 0.345, 1.24),
          ring=(0.482, 0.320, 0.468, 0.064),
          label_en='Pending shares', label_es='Partes pendientes'),

        B(en='Platform Share and Toll Commission are the platform’s side of it. Read them '
             'against the owner share and you can see exactly what the arrangement costs you '
             'this period.',
          es='Parte de la plataforma y Comisión de peaje son el lado de la plataforma. Léalas '
             'frente a la parte del propietario y verá exactamente qué le cuesta el acuerdo '
             'este período.',
          cam=(0.48, 0.42, 1.22),
          ring=(0.243, 0.396, 0.468, 0.064)),

        B(en='And this line is the schedule. Last Payout, Next Scheduled Payout with a date '
             'and a time, and Total Paid Out over all time.',
          es='Y esta línea es el calendario. Último pago, Próximo pago programado con fecha y '
             'hora, y Total pagado desde siempre.',
          cam=(0.5, 0.49, 1.24),
          ring=(0.238, 0.476, 0.722, 0.028),
          label_en='The payout schedule', label_es='El calendario de pagos'),

        B(en='A payout is not something you press. It runs on that schedule, and everything '
             'pending at that moment goes out together.',
          es='Un pago no es algo que usted pulse. Se ejecuta según ese calendario, y todo lo '
             'pendiente en ese momento sale junto.',
          cam=(0.5, 0.49, 1.24)),

        B(en='Three tabs underneath. Payouts is the history.',
          es='Tres pestañas debajo. Pagos es el historial.',
          cam=(0.32, 0.54, 1.26),
          point=(0.309, 0.540), click=1.2,
          ring=(0.231, 0.522, 0.161, 0.035)),

        B(en='Search a date range and you get every payout in it. "No payouts yet" on a new '
             'account is expected — the first one waits for the first scheduled run.',
          es='Busque un rango de fechas y obtiene todos los pagos que haya. "Aún no hay pagos" '
             'en una cuenta nueva es lo esperado: el primero espera a la primera ejecución '
             'programada.',
          shot='72-distribution-payouts', cam=(0.5, 0.66, 1.16),
          point=(0.520, 0.626), click=1.8,
          ring=(0.233, 0.566, 0.727, 0.207),
          label_en='Payout History', label_es='Historial de pagos'),

        B(en='And the Charges tab underneath it breaks a payout back down into the individual '
             'charges that made it up — which is how you answer "what is this deposit?" '
             'without leaving the page.',
          es='Y la pestaña Cargos de debajo descompone un pago en los cargos concretos que lo '
             'formaron, que es como se responde a "¿qué es este ingreso?" sin salir de la '
             'página.',
          cam=(0.36, 0.54, 1.26),
          point=(0.364, 0.540), click=1.3),
    ])
