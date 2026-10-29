# -*- coding: utf-8 -*-
"""Episode 54 — for partners: the owners they brought, from the Partners page.

Since owner-web #695 (2026-10-29) a row of Partnership → Partners has a menu (right-click, or the three dots):
Payment Settings, Owner Settings, Booking Plugins, Page Visibility. The last three open one tab of Administration →
Settings for that owner at /partners/<owner>/<section>, without switching the account the partner is viewing
(OwnerSettingsPage ownerOverride + singleTab). A double-click on a row opens Payment Settings. On Booking Plugins a
partner now changes a connected Turo plugin too (RentalStatusCard canManage = admin or partner): the Turo account email,
removing one of several accounts, Disconnect.

The frames (`prt-05..09-*`, capture-partner.js) are the real dev portal shown as a partner, with DEMO DATA: two
made-up owners ("Sunrise Car Rental", "Harbor Rentals") and a staged Turo card with two accounts. Nothing is written.
Rings come from shots/_partner_boxes.json, per language.

Facts the narration states, checked against the code: the menu items and the double-click (PartnersPage menuItems,
onRowDoubleClick → /owners/<id>); search matches first name, last name or email (OwnerTollBalanceController
my-partnership-owners-paged); Owner Settings and Page Visibility save with Save (OwnerSettingsPage handleSave),
plugin changes apply at once (ownerBookingPluginsApi.set / delete / removeAccount); Disconnect deletes the owner's
plugin section (OwnerBookingPluginsController.Delete → store.DeleteAsync), so bookings are no longer made from the
owner's Turo emails (RentalEmailRouter needs that section); a partner may set Owner Share up to 20 % (Payment
Settings, OwnerTollBalanceController).
"""
from model import B, E
from series_p import WIDE, at, look, ring, span

# =============================================================================== 54
EP54 = E(
    54, 'partner-owner-pages',
    'For partners: manage your owners from the Partners page',
    'Para socios: gestione a sus propietarios desde la página Socios',
    'One menu per owner: payments, settings, booking plugins, visible pages',
    'Un menú por propietario: pagos, configuración, plugins de reservas, páginas visibles',
    [
        B(en='Open Partnership, then Partners. Here are all the owners you brought.',
          es='Abra Asociación y luego Socios. Aquí están todos los propietarios que trajo.',
          shot='prt-05-partners-list', url='/partners', cam=WIDE,
          label_en='Partnership · Partners', label_es='Asociación · Socios'),

        B(en='Looking for one? Type a name or an email in the search box.',
          es='¿Busca uno? Escriba un nombre o un correo en el buscador.',
          cam=look(ring('prt-05-partners-list', 'search'), 1.5), ring=ring('prt-05-partners-list', 'search')),

        B(en='Right-click the owner. Or press the three dots at the start of the row.',
          es='Haga clic derecho sobre el propietario. O pulse los tres puntos al principio de la fila.',
          cam=look(ring('prt-05-partners-list', 'row'), 1.4), ring=ring('prt-05-partners-list', 'row'),
          point=at('prt-05-partners-list', 'dots'), click=1.4),

        B(en='A menu opens with four choices.',
          es='Se abre un menú con cuatro opciones.',
          shot='prt-06-row-menu', cam=look(ring('prt-06-row-menu', 'menu'), 1.8), ring=ring('prt-06-row-menu', 'menu')),

        B(en='Payment Settings: the owner’s share and payouts. A double-click on the row opens it too.',
          es='Ajustes de pago: la parte del propietario y los pagos. Un doble clic en la fila también lo abre.',
          cam=look(ring('prt-06-row-menu', 'menu'), 1.8), ring=ring('prt-06-row-menu', 'payment')),

        B(en='Owner Settings opens the owner’s settings.',
          es='Configuración del Propietario abre la configuración del propietario.',
          cam=look(ring('prt-06-row-menu', 'menu'), 1.8), ring=ring('prt-06-row-menu', 'owner'),
          point=at('prt-06-row-menu', 'owner'), click=1.0),

        B(en='The owner’s name is at the top, so you always know whose settings these are. Change what you need, '
             'then press Save.',
          es='El nombre del propietario está arriba, así siempre sabe de quién es esta configuración. Cambie lo que '
             'necesite y pulse Guardar.',
          shot='prt-07-owner-settings', url='/partners/…/owner-settings',
          cam=look(span('prt-07-owner-settings', 'title', 'owner'), 1.6), ring=span('prt-07-owner-settings', 'title', 'owner'),
          label_en='Owner Settings', label_es='Configuración del Propietario'),

        B(en='Next, Booking Plugins.',
          es='Después, Plugins de reservas.',
          shot='prt-08-owner-plugins', url='/partners/…/booking-plugins',
          cam=look(span('prt-08-owner-plugins', 'title', 'owner'), 1.6), ring=span('prt-08-owner-plugins', 'title', 'owner'),
          label_en='Booking Plugins', label_es='Plugins de reservas'),

        B(en='Here you turn on Turo or a booking system for the owner, change it, or remove it. Changes apply at once.',
          es='Aquí activa Turo o un sistema de reservas para el propietario, lo cambia o lo quita. Los cambios se '
             'aplican al instante.',
          cam=look(ring('prt-08-owner-plugins', 'card'), 1.3), ring=ring('prt-08-owner-plugins', 'card')),

        B(en='On the Turo card you can change the Turo account email, then save it.',
          es='En la tarjeta de Turo puede cambiar el correo de la cuenta de Turo y guardarlo.',
          cam=look(ring('prt-08-owner-plugins', 'login'), 1.8), ring=ring('prt-08-owner-plugins', 'login')),

        B(en='Does the owner have several Turo accounts? Remove one with the bin next to it.',
          es='¿El propietario tiene varias cuentas de Turo? Quite una con la papelera de al lado.',
          cam=look(span('prt-08-owner-plugins', 'accounts', 'remove'), 1.6), ring=ring('prt-08-owner-plugins', 'remove'),
          point=at('prt-08-owner-plugins', 'remove')),

        B(en='Disconnect takes Turo off this owner. Bookings are then no longer made from their Turo emails.',
          es='Desconectar quita Turo a este propietario. Entonces ya no se crean reservas con sus correos de Turo.',
          cam=look(ring('prt-08-owner-plugins', 'disconnect'), 1.8), ring=ring('prt-08-owner-plugins', 'disconnect'),
          point=at('prt-08-owner-plugins', 'disconnect')),

        B(en='And Page Visibility decides which pages the owner sees.',
          es='Y Visibilidad de páginas decide qué páginas ve el propietario.',
          shot='prt-09-owner-visibility', url='/partners/…/page-visibility',
          cam=look(span('prt-09-owner-visibility', 'title', 'owner'), 1.6), ring=span('prt-09-owner-visibility', 'title', 'owner'),
          label_en='Page Visibility', label_es='Visibilidad de páginas'),

        B(en='Pick a preset — Minimal, Medium or Full — then switch single pages on or off, and press Save.',
          es='Elija un preajuste — Mínimo, Medio o Completo —, luego active o desactive páginas sueltas y pulse '
             'Guardar.',
          cam=look(ring('prt-09-owner-visibility', 'preset'), 1.6), ring=ring('prt-09-owner-visibility', 'preset'),
          point=at('prt-09-owner-visibility', 'preset')),

        B(en='These pages work for that one owner. Your own account stays as it is.',
          es='Estas páginas trabajan para ese propietario. Su propia cuenta sigue igual.',
          shot='prt-06-row-menu', url='/partners', cam=WIDE),
    ])
EP54.audience = 'partner'
EP54.privacy = 'public'
