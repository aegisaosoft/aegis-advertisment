# -*- coding: utf-8 -*-
"""Episodes 34-35 — getting started: registering as an owner, and as a partner.

Everything else in the series assumes an account. These two go back to the moment before
one exists: the public registration page, the agreement that follows it, and Stripe, where
the bank account that receives the money is entered. The owner episode ends where episodes
3 and 5 begin — toll agencies and cars — so a newcomer knows what to watch next.

The screens (`reg-*`, captured by capture-register.js) come from the public sandbox with a
made-up person typed into the form: nobody real is registered, and the sandbox's own marks
are hidden because the production page has none. Stripe's page is Stripe's, shown once: its
later steps ask each person for their own details and their own bank, and are the same
for every business that uses Stripe. The finished state is the portal's Banking page from
the written guide.

Two things are deliberately said plainly. The email on the form becomes the login. And the
agreement cannot be accepted until it has been scrolled to the end and every section ticked
— the page enforces it, and a viewer who knows that does not think the button is broken.
"""
from model import B, E


# =============================================================================== 34
EP34 = E(
    34, 'register-owner',
    'Getting started: register as an owner',
    'Primeros pasos: registrarse como propietario',
    'From the sign-up page to a connected bank account, in one sitting',
    'De la página de registro a una cuenta bancaria conectada, de una vez',
    [
        B(en='Registration is at owner.myeztoll.com/create-owner. The Start button on '
             'myeztoll.com brings you to the same page.',
          es='El registro está en owner.myeztoll.com/create-owner. El botón Empezar de '
             'myeztoll.com le trae a esta misma página.',
          say_en='Registration is at owner dot my e z toll dot com, slash create owner. The '
                 'Start button on my e z toll dot com brings you to the same page.',
          say_es='El registro está en owner punto my e z toll punto com, barra create owner. '
                 'El botón Empezar de my e z toll punto com le trae a esta misma página.',
          shot='reg-11-owner-welcome', url='/create-owner', cam=(0.5, 0.35, 1.0),
          label_en='Owner Registration', label_es='Registro de propietario'),

        B(en='Pick your language at the top right first. Everything that follows, the '
             'agreement included, comes in that language.',
          es='Elija primero su idioma arriba a la derecha. Todo lo que sigue, contrato '
             'incluido, sale en ese idioma.',
          cam=(0.60, 0.20, 1.25),
          point=(0.654, 0.042), ring=(0.612, 0.022, 0.085, 0.040)),

        B(en='Then Get Started.',
          es='Luego, Comenzar.',
          cam=(0.5, 0.40, 1.20),
          point=(0.500, 0.476), click=0.9),

        B(en='Three steps: your information, your primary location, and a review.',
          es='Tres pasos: su información, su ubicación principal, y una revisión.',
          shot='reg-12-owner-info', cam=(0.5, 0.30, 1.20),
          ring=(0.385, 0.122, 0.235, 0.060),
          label_en='Step 1 · Your Information', label_es='Paso 1 · Tu información'),

        B(en='Company name is optional. First name, last name, email and phone are '
             'required — and the email is your login from now on.',
          es='El nombre de la empresa es opcional. Nombre, apellido, correo y teléfono son '
             'obligatorios, y el correo es su usuario de aquí en adelante.',
          cam=(0.5, 0.47, 1.26),
          ring=(0.312, 0.318, 0.380, 0.290)),

        B(en='SMS consent stays on: it is how we reach you about tolls and your account.',
          es='El consentimiento de SMS queda activado: es como le avisamos de los peajes y '
             'de su cuenta.',
          cam=(0.62, 0.58, 1.34),
          point=(0.649, 0.580)),

        B(en='Choose a password of at least eight characters and type it twice.',
          es='Elija una contraseña de al menos ocho caracteres y escríbala dos veces.',
          cam=(0.5, 0.78, 1.28),
          ring=(0.302, 0.735, 0.395, 0.115)),

        B(en='Next.',
          es='Siguiente.',
          cam=(0.5, 0.80, 1.20),
          point=(0.662, 0.890), click=0.8),

        B(en='Your primary location: street, city, state and ZIP. This is the address that '
             'goes on your agreement.',
          es='Su ubicación principal: calle, ciudad, estado y código postal. Es la dirección '
             'que va en su contrato.',
          shot='reg-13-owner-location', cam=(0.5, 0.36, 1.22),
          ring=(0.305, 0.270, 0.390, 0.235),
          label_en='Step 2 · Primary Location', label_es='Paso 2 · Ubicación principal'),

        B(en='Next again.',
          es='Siguiente otra vez.',
          cam=(0.5, 0.45, 1.20),
          point=(0.662, 0.554), click=0.8),

        B(en='Read it over once. Previous goes back to fix anything; Next creates the '
             'account.',
          es='Léalo una vez. Anterior vuelve atrás para corregir; Siguiente crea la cuenta.',
          shot='reg-14-owner-review', cam=(0.5, 0.40, 1.20),
          ring=(0.305, 0.268, 0.390, 0.335),
          point=(0.662, 0.644), click=2.6,
          label_en='Step 3 · Review', label_es='Paso 3 · Revisar'),

        B(en='The account exists now, and the agreement opens: the Owner Service and '
             'Revenue-Sharing Agreement, made out to you.',
          es='La cuenta ya existe, y se abre el contrato: el Contrato de servicios al '
             'propietario y reparto de ingresos, a su nombre.',
          shot='reg-15-agreement', cam=(0.5, 0.25, 1.18),
          ring=(0.330, 0.045, 0.340, 0.075),
          label_en='The owner agreement', label_es='El contrato de propietario'),

        B(en='It is read in the box, and it has to be scrolled to the very end before '
             'anything below it unlocks. The yellow line says so.',
          es='Se lee dentro del recuadro, y hay que llegar hasta el final antes de que se '
             'active lo de abajo. La línea amarilla lo dice.',
          cam=(0.5, 0.55, 1.22),
          ring=(0.272, 0.645, 0.450, 0.030)),

        B(en='Eight sections each ask you to confirm you have read them. Tick the box as you '
             'pass it.',
          es='Ocho secciones piden que confirme que las ha leído. Marque la casilla al pasar.',
          shot='reg-16-agreement-sign', cam=(0.5, 0.30, 1.24),
          point=(0.294, 0.284), click=1.6,
          label_en='Eight acknowledgements', label_es='Ocho confirmaciones'),

        B(en='Under the text, two more: the SMS consent, and the one that says you agree to '
             'all of it.',
          es='Bajo el texto, dos más: el consentimiento de SMS, y la que dice que acepta '
             'todo.',
          cam=(0.5, 0.48, 1.26),
          point=(0.280, 0.524), click=1.4,
          ring=(0.270, 0.462, 0.455, 0.095)),

        B(en='Then sign in the box — with the mouse, or a finger on a phone.',
          es='Después firme en el recuadro, con el ratón o con el dedo en el teléfono.',
          cam=(0.5, 0.68, 1.26),
          ring=(0.322, 0.652, 0.350, 0.182)),

        B(en='With every box ticked and a signature in place, Accept Agreement turns green. '
             'Press it.',
          es='Con todas las casillas marcadas y la firma puesta, Aceptar el contrato se pone '
             'verde. Púlselo.',
          shot='reg-17-agreement-signed', cam=(0.5, 0.75, 1.24),
          point=(0.497, 0.913), click=2.2,
          label_en='Accept Agreement', label_es='Aceptar el contrato'),

        B(en='You are signed in, and Stripe opens. Stripe is where your bank account lives: '
             'we never see the account number ourselves.',
          es='Ya está dentro, y se abre Stripe. Stripe es donde vive su cuenta bancaria: '
             'nosotros nunca vemos el número de cuenta.',
          shot='reg-18-stripe-onboarding', url='@connect.stripe.com', cam=(0.5, 0.35, 1.0),
          label_en='Stripe · bank account', label_es='Stripe · cuenta bancaria'),

        B(en='It starts with your phone number and a code, then asks for your personal '
             'details and the bank account the money should go to. Follow it to the end.',
          es='Empieza con su teléfono y un código, luego pide sus datos personales y la '
             'cuenta bancaria a la que debe ir el dinero. Sígalo hasta el final.',
          cam=(0.55, 0.40, 1.24),
          ring={'en': (0.405, 0.315, 0.260, 0.165), 'es': (0.405, 0.335, 0.260, 0.165)},
          point={'en': (0.535, 0.456), 'es': (0.535, 0.476)}),

        B(en='If you leave Stripe early, nothing is lost. Back in the portal, Banking says '
             'the account is not set up yet, and Connect Stripe Account takes you in again.',
          es='Si sale de Stripe antes de tiempo, no se pierde nada. De vuelta en el portal, '
             'Banca dice que la cuenta aún no está configurada, y Conectar cuenta de Stripe '
             'le lleva otra vez.',
          shot='reg-19-banking-pending', url='/stripe-cards', cam=(0.5, 0.25, 1.12),
          point=(0.814, 0.291), click=2.8,
          ring=(0.204, 0.250, 0.780, 0.097),
          label_en='Banking', label_es='Banca'),

        B(en='When Stripe is done, the card turns green: Onboarding Complete, Charges '
             'Enabled, Payouts Enabled. Toll money can now reach you.',
          es='Cuando Stripe termina, la tarjeta se pone verde: Registro completado, Cargos '
             'habilitados, Pagos habilitados. El dinero de los peajes ya puede llegarle.',
          shot='68-banking', cam=(0.5, 0.28, 1.14),
          ring=(0.204, 0.250, 0.780, 0.135),
          label_en='Onboarding Complete', label_es='Registro completado'),

        B(en='Two things come next. Under Settings, Toll Accounts, add the accounts you hold '
             'with the toll agencies — episode 3 walks through it.',
          es='Quedan dos cosas. En Configuración, Cuentas de peaje, añada las cuentas que '
             'tiene con las agencias de peaje: el episodio 3 lo explica paso a paso.',
          shot='31-settings-toll-accounts', url='/owners/settings', cam=(0.5, 0.30, 1.0),
          point=(0.520, 0.199), click=1.8,
          label_en='Next: Settings → Toll Accounts', label_es='Siguiente: Configuración → Cuentas de peaje'),

        B(en='And under Vehicles, add your cars, one at a time or from a file — that is '
             'episode 5.',
          es='Y en Vehículos, añada sus coches, de uno en uno o desde un archivo: eso es el '
             'episodio 5.',
          shot='14-add-vehicle-basic', url='/vehicles/new', cam=(0.5, 0.17, 1.16),
          ring=(0.204, 0.144, 0.226, 0.035),
          label_en='Next: Vehicles → Add New Vehicle', label_es='Siguiente: Vehículos → Añadir vehículo nuevo'),

        B(en='From there the portal does the work: tolls arrive, drivers are charged, and '
             'your share is paid out.',
          es='A partir de ahí el portal hace el trabajo: llegan los peajes, se cobra a los '
             'conductores, y su parte se le paga.',
          shot='01-dashboard', url='/dashboard', cam=(0.5, 0.42, 1.0),
          label_en='The Control Panel', label_es='El Panel de Control'),
    ])


# =============================================================================== 35
EP35 = E(
    35, 'register-partner',
    'Getting started: register as a partner',
    'Primeros pasos: registrarse como socio',
    'The same form, one extra role, and the page where your referrals live',
    'El mismo formulario, un papel más, y la página donde viven sus referidos',
    [
        B(en='A partner brings fleet owners to My E-Z Toll and earns a share of what the '
             'platform makes from them: twenty percent, for a full year, from every owner '
             'they refer.',
          es='Un socio trae propietarios de flotas a My E-Z Toll y gana una parte de lo que '
             'la plataforma obtiene de ellos: el veinte por ciento, durante un año entero, '
             'por cada propietario que recomienda.',
          shot='reg-21-partner-welcome', url='/create-partner', cam=(0.5, 0.35, 1.0),
          label_en='Partner Registration', label_es='Registro de socio'),

        B(en='Partner registration is at owner.myeztoll.com/create-partner. The heading '
             'says what it does: you register as an owner and a partner at once.',
          es='El registro de socio está en owner.myeztoll.com/create-partner. El '
             'encabezado dice lo que hace: se registra como propietario y socio a la vez.',
          say_en='Partner registration is at owner dot my e z toll dot com, slash create '
                 'partner. The heading says what it does: you register as an owner and a '
                 'partner at once.',
          say_es='El registro de socio está en owner punto my e z toll punto com, barra '
                 'create partner. El encabezado dice lo que hace: se registra como '
                 'propietario y socio a la vez.',
          cam=(0.42, 0.12, 1.30),
          ring=(0.300, 0.018, 0.230, 0.058)),

        B(en='The form is the one owners fill in. Get Started.',
          es='El formulario es el mismo que rellenan los propietarios. Comenzar.',
          cam=(0.5, 0.40, 1.20),
          point=(0.500, 0.482), click=1.6),

        B(en='Your details and a password, then your address and a review — exactly as in '
             'the previous episode.',
          es='Sus datos y una contraseña, luego su dirección y una revisión: exactamente '
             'como en el episodio anterior.',
          shot='reg-22-partner-info', cam=(0.5, 0.45, 1.20),
          ring=(0.312, 0.322, 0.380, 0.290),
          label_en='The same three steps', label_es='Los mismos tres pasos'),

        B(en='So is what follows: the agreement to read and sign, and Stripe for the bank '
             'account. Partner earnings are paid out the same way as toll money.',
          es='Y lo que sigue también: el contrato que se lee y se firma, y Stripe para la '
             'cuenta bancaria. Las ganancias de socio se pagan igual que el dinero de los '
             'peajes.',
          shot='reg-17-agreement-signed', cam=(0.5, 0.70, 1.20),
          ring=(0.322, 0.652, 0.350, 0.182),
          label_en='Agreement, then Stripe', label_es='Contrato, y luego Stripe'),

        B(en='Once inside, the menu has a section owners do not have: Partnership. In it, '
             'Partners.',
          es='Una vez dentro, el menú tiene una sección que los propietarios no tienen: '
             'Asociación. Dentro, Socios.',
          shot='99-partners', url='/partners', cam=(0.5, 0.40, 1.0),
          point=(0.043, 0.586), click=1.8,
          label_en='Partnership → Partners', label_es='Asociación → Socios'),

        B(en='This page lists every owner you have referred, with their share settings and '
             'what you have earned from each. A new partner sees it empty.',
          es='Esta página lista a cada propietario que ha recomendado, con sus ajustes de '
             'reparto y lo que ha ganado con cada uno. Un socio nuevo la ve vacía.',
          cam=(0.6, 0.30, 1.18),
          ring=(0.203, 0.178, 0.782, 0.230)),

        B(en='Invite Partner sends an owner a link, by text message or by email. An owner '
             'who registers through it is yours from the first day.',
          es='Invitar socio envía a un propietario un enlace, por SMS o por correo. Un '
             'propietario que se registra por ese enlace es suyo desde el primer día.',
          cam=(0.70, 0.18, 1.30),
          point=(0.778, 0.132), click=1.8,
          ring=(0.733, 0.115, 0.090, 0.035),
          label_en='Invite Partner', label_es='Invitar socio'),

        B(en='The link is the owner registration page with your id on it, so it also '
             'works pasted into your own emails or on your website.',
          es='El enlace es la página de registro de propietario con su identificador, así '
             'que también sirve pegado en sus propios correos o en su web.',
          cam=(0.70, 0.18, 1.30)),

        B(en='Referred owners pay nothing; you earn from what the platform earns. The term '
             'runs a year from the day each owner joins, and the Earns Until column shows '
             'when it ends.',
          es='Los propietarios recomendados no pagan nada; usted gana de lo que gana la '
             'plataforma. El plazo dura un año desde el día en que entra cada propietario, '
             'y la columna Gana hasta muestra cuándo termina.',
          cam=(0.5, 0.40, 1.0)),

        B(en='Everything else works as it does for any owner. Your own cars, if you have '
             'them, live here too.',
          es='Todo lo demás funciona como para cualquier propietario. Sus propios coches, '
             'si los tiene, también viven aquí.',
          shot='01-dashboard', url='/dashboard', cam=(0.5, 0.42, 1.0),
          label_en='The Control Panel', label_es='El Panel de Control'),
    ])
