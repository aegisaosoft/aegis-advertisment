# -*- coding: utf-8 -*-
"""Episodes 31-33 — collections: when a debt leaves the portal and goes to an agency.

This part is about money that has already failed to arrive: the card declined, the reminder
series ran out, and the renter has gone home — often to another country. Everything here is
a decision the owner makes about a real person, so the narration stays plain about what
referral does and does not mean: the debt stays theirs, it can be recalled, and the agency's
commission comes out of the money before anybody's share is worked out.

Screens come from the dev portal (`col-*`, captured by capture-collections.js) against test
cases; no real debtor is shown, and the portal's own redaction rules blur the drivers behind
the rows anyway.
"""
from model import B, E


# =============================================================================== 31
EP31 = E(
    31, 'collections-referral',
    'Collections, part 1: when a debt goes to an agency',
    'Cobros, parte 1: cuándo una deuda pasa a una agencia',
    'The debts letters cannot collect, and what referring one actually means',
    'Las deudas que las cartas no cobran, y qué significa ceder una',
    [
        B(en='Some debts do not get paid. The card fails, the reminders go out, and the renter '
             'has gone home — often to another country.',
          es='Algunas deudas no se pagan. La tarjeta falla, los avisos salen, y el cliente ya se '
             'fue a casa, muchas veces a otro país.',
          shot='col-10-queue', url='/payments/collections', cam=(0.5, 0.20, 1.02),
          label_en='Collections', label_es='Cobros'),

        B(en='When the letters run out, the portal opens a case here. Nothing is sent anywhere '
             'yet — this queue is a list of debts worth a decision.',
          es='Cuando se acaban las cartas, el portal abre un expediente aquí. Todavía no se envía '
             'nada: esta cola es una lista de deudas que merecen una decisión.',
          cam=(0.5, 0.155, 1.22),
          ring=(0.105, 0.120, 0.760, 0.075)),

        B(en='Referring a debt is not selling it. The debt stays yours, and you can recall it at '
             'any moment — the line under the title says so.',
          es='Ceder una deuda no es venderla. La deuda sigue siendo suya y puede retirarla en '
             'cualquier momento: la línea bajo el título lo dice.',
          cam=(0.42, 0.115, 1.34),
          ring=(0.110, 0.108, 0.680, 0.030)),

        B(en='Before any of this works, you tell us which agency you have an agreement with. '
             'That is in Settings, under Collections.',
          es='Antes de nada, usted nos dice con qué agencia tiene un acuerdo. Eso está en '
             'Configuración, en Cobros.',
          shot='col-16-settings-agencies', url='/settings', cam=(0.5, 0.20, 1.04),
          label_en='Settings · Collections', label_es='Configuración · Cobros'),

        B(en='An agency works where it is licensed. A debtor who went home to Spain cannot be '
             'chased by an American agency — so the country on the case decides who gets it.',
          es='Una agencia trabaja donde tiene licencia. A un deudor que volvió a España no puede '
             'perseguirlo una agencia estadounidense, así que el país del expediente decide '
             'quién lo recibe.',
          cam=(0.5, 0.30, 1.12)),

        B(en='Your agreement also carries the commission you agreed. It matters: the claim the '
             'driver is asked for is the debt plus that commission.',
          es='Su acuerdo también lleva la comisión pactada. Importa: lo que se le reclama al '
             'conductor es la deuda más esa comisión.',
          cam=(0.5, 0.40, 1.16),
          hold=0.3),

        B(en='Small debts are left alone. Below the threshold the commission eats the money, and '
             'chasing a person for it is not worth doing.',
          es='Las deudas pequeñas se dejan estar. Por debajo del umbral la comisión se come el '
             'dinero, y perseguir a una persona por eso no merece la pena.',
          shot='col-10-queue', url='/payments/collections', cam=(0.5, 0.20, 1.02)),

        B(en='So what reaches this queue is what survived every gate: a real debt, a driver who '
             'was told, and a country somebody can work in.',
          es='Así que a esta cola llega lo que pasó todos los filtros: una deuda real, un '
             'conductor al que se avisó, y un país donde alguien puede actuar.',
          cam=(0.5, 0.20, 1.02)),
    ])


# =============================================================================== 32
EP32 = E(
    32, 'collections-queue',
    'Collections, part 2: the queue', 'Cobros, parte 2: la cola',
    'Reading a case, referring it, and turning one down',
    'Leer un expediente, cederlo, y rechazarlo',
    [
        B(en='The queue has one tab per stage: waiting for you, approved, with the agency, '
             'part-recovered, declined.',
          es='La cola tiene una pestaña por etapa: esperándole, aprobados, con la agencia, '
             'cobrados en parte, rechazados.',
          shot='col-10-queue', url='/payments/collections', cam=(0.5, 0.155, 1.20),
          ring=(0.105, 0.140, 0.420, 0.035),
          label_en='Awaiting approval', label_es='A la espera de aprobación'),

        B(en='A row is the whole story in one line: who, which rental, what is owed, and what '
             'would be claimed — the debt plus the agency fee underneath it.',
          es='Una fila es toda la historia en una línea: quién, qué alquiler, cuánto se debe, y '
             'qué se reclamaría: la deuda más la comisión de la agencia debajo.',
          cam=(0.62, 0.195, 1.30),
          ring=(0.560, 0.180, 0.180, 0.055),
          label_en='Owed · Claim', label_es='Debe · Reclamación'),

        B(en='Then how long it has been overdue, how many notices went out, which agency it is '
             'routed to, and where the case stands.',
          es='Después cuánto lleva vencida, cuántos avisos salieron, a qué agencia va, y en qué '
             'punto está el expediente.',
          cam=(0.83, 0.195, 1.30),
          ring=(0.745, 0.180, 0.220, 0.055)),

        B(en='Click the driver and the case opens. This is everything the decision rests on, '
             'frozen the day the case was made.',
          es='Pulse el conductor y el expediente se abre. Aquí está todo en lo que se apoya la '
             'decisión, congelado el día en que se creó.',
          shot='col-11-evidence', cam=(0.5, 0.20, 1.10),
          point=(0.150, 0.192), click=1.5,
          label_en='The case', label_es='El expediente'),

        B(en='What is owed, charge by charge — the tolls and the violations that were never '
             'paid, and the date the oldest one arose.',
          es='Qué se debe, cargo a cargo: los peajes y las multas que nunca se pagaron, y la '
             'fecha del más antiguo.',
          cam=(0.24, 0.30, 1.32),
          ring=(0.105, 0.265, 0.235, 0.085),
          label_en='What is owed', label_es='Qué se debe'),

        B(en='What the driver was sent, letter by letter, with the date each one went out.',
          es='Qué se le envió al conductor, carta por carta, con la fecha de cada envío.',
          cam=(0.50, 0.30, 1.32),
          ring=(0.345, 0.265, 0.255, 0.085),
          label_en='What was sent', label_es='Qué se envió'),

        B(en='And why the card did not pay, with the country we have for the driver — the two '
             'things an agency asks first.',
          es='Y por qué no pagó la tarjeta, con el país que tenemos del conductor: las dos cosas '
             'que pregunta primero una agencia.',
          cam=(0.76, 0.30, 1.32),
          ring=(0.605, 0.265, 0.270, 0.085),
          label_en='Why the card did not pay', label_es='Por qué no pagó la tarjeta'),

        B(en='If it is worth referring, tick the case and press Refer. You are asked to confirm, '
             'because from that moment a third party contacts your customer.',
          es='Si merece cederse, marque el expediente y pulse Ceder. Se le pide confirmación, '
             'porque desde ese momento un tercero contacta a su cliente.',
          shot='col-10-queue', cam=(0.30, 0.155, 1.30),
          point=(0.115, 0.175), click=1.4,
          label_en='Refer', label_es='Ceder'),

        B(en='If it is not, press Decline and say why. The reason is kept on the case, so next '
             'year it still says what you knew today.',
          es='Si no, pulse Rechazar y diga por qué. El motivo se guarda en el expediente, para '
             'que el año que viene siga diciendo lo que usted sabía hoy.',
          shot='col-15-declined', cam=(0.5, 0.20, 1.10),
          label_en='Declined', label_es='Rechazados'),

        B(en='Some agencies take no cases electronically. For those the case moves to Approved '
             'and offers you a file to download and send yourself.',
          es='Algunas agencias no reciben expedientes por vía electrónica. En ese caso el '
             'expediente pasa a Aprobado y le ofrece un archivo para descargar y enviar usted.',
          shot='col-12-approved', cam=(0.5, 0.20, 1.10),
          label_en='Approved', label_es='Aprobados'),
    ])


# =============================================================================== 33
EP33 = E(
    33, 'collections-money',
    'Collections, part 3: the money', 'Cobros, parte 3: el dinero',
    'What comes back, who takes what, and the half-payment that needs your word',
    'Qué vuelve, quién se lleva qué, y el pago a medias que necesita su palabra',
    [
        B(en='Once a case is with the agency, it sits on this tab and you wait. Nothing else is '
             'asked of you.',
          es='Cuando el expediente está con la agencia, se queda en esta pestaña y usted espera. '
             'No se le pide nada más.',
          shot='col-13-placed', url='/payments/collections', cam=(0.5, 0.20, 1.06),
          label_en='With the agency', label_es='Con la agencia'),

        B(en='If they collect it in full, the money comes back with the commission already taken '
             'out. The agency is paid first — out of the claim, not out of your share.',
          es='Si lo cobran entero, el dinero vuelve con la comisión ya descontada. A la agencia '
             'se le paga primero, del importe reclamado, no de su parte.',
          cam=(0.5, 0.30, 1.14)),

        B(en='What is left is split the ordinary way, and the charges behind the debt are closed '
             'on their own. You end up with the amount you were owed.',
          es='Lo que queda se reparte como siempre, y los cargos que había detrás se cierran '
             'solos. Usted termina con la cantidad que se le debía.',
          cam=(0.5, 0.30, 1.14),
          hold=0.3),

        B(en='A part payment is different, and the portal will not decide it for you.',
          es='Un pago parcial es distinto, y el portal no lo decide por usted.',
          shot='col-14-partial', cam=(0.5, 0.20, 1.06),
          label_en='Part-recovered', label_es='Cobrados en parte'),

        B(en='Accept and write off the rest closes the case and forgives the difference. Leave it '
             'and the debt stays open — but then the driver keeps getting letters for a debt that '
             'is already part-paid.',
          es='Aceptar y condonar el resto cierra el expediente y perdona la diferencia. Si no lo '
             'hace, la deuda sigue abierta, pero entonces el conductor seguirá recibiendo cartas '
             'por una deuda ya pagada en parte.',
          cam=(0.5, 0.31, 1.24),
          ring=(0.105, 0.265, 0.560, 0.075)),

        B(en='An agency with no electronic intake tells you by email instead. Then you record it: '
             'The agency collected it, and the amount.',
          es='Una agencia sin recepción electrónica se lo dirá por correo. Entonces lo registra '
             'usted: La agencia lo cobró, y el importe.',
          cam=(0.5, 0.31, 1.24),
          label_en='The agency collected it', label_es='La agencia lo cobró'),

        B(en='Type a wrong figure and there is a way back — I reported this by mistake puts the '
             'case back with the agency, untouched.',
          es='Si escribe una cifra equivocada, hay vuelta atrás: Lo registré por error devuelve '
             'el expediente a la agencia, intacto.',
          cam=(0.5, 0.31, 1.24)),

        B(en='And if the driver pays you directly — card, or cash at the counter — the case is '
             'recalled by itself. The agency is told to stop before the case is closed here.',
          es='Y si el conductor le paga directamente, con tarjeta o en efectivo, el expediente se '
             'retira solo. Se le dice a la agencia que pare antes de cerrar el expediente aquí.',
          shot='col-10-queue', cam=(0.5, 0.20, 1.02),
          label_en='Collections', label_es='Cobros'),

        B(en='Which is the whole point of the feature: the debt is chased by people who do that '
             'for a living, and it never stops being yours.',
          es='Y esa es toda la idea: de la deuda se ocupa quien vive de eso, y nunca deja de ser '
             'suya.',
          cam=(0.5, 0.20, 1.02)),
    ])
