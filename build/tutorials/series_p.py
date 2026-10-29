# -*- coding: utf-8 -*-
"""Episode 51 — for partners: turning on a booking plugin for an owner they brought.

Since owner-web #654 (2026-10-19) the "+ Add booking plugin" picker on Settings → Booking Plugins is offered to
partners as well as administrators; the API already accepted a partner for the owners whose OwnerBalances.PartnerId
is that partner (OwnerRouteScope). Since owner-web #695 (2026-10-29) a partner also changes and removes a connected
plugin (RentalStatusCard: the Turo login, one account, Disconnect), so the closing beat no longer sends them to us;
the same release translated the tab label (pluginsPage.tabBooking: "Plugins de reservas" in Spanish).

The frames (`prt-0N-*`, capture-partner.js) are the real dev portal with the session switched to a partner's in the
browser, and DEMO DATA: two made-up owners ("Sunrise Car Rental", "Harbor Rentals") and a staged plugin list. Turning
Turo on is answered in the browser and never reaches the server. Where the picker, the tab and the Turo card landed
was measured during the capture (shots/_partner_boxes.json, per language); the sidebar's owner banner and the toast
are fixed fractions read off the frames (they do not move between the two languages).

Facts the narration states, checked against the code: Turo as a rental plugin is enabled by an empty config section
(OwnerBookingPluginsTab.handleAdd → PUT with no secrets) and that section is what lets RentalEmailRouter turn the
owner's forwarded Turo emails into bookings; a fleet plugin opens its credentials form (`renderFleetCard(..., 'add')`);
the car is found by make, model and year when no listing link exists (PendingVehicleMatcher).
"""
import io
import json
import os

from model import B, E

HERE = os.path.dirname(os.path.abspath(__file__))


def _boxes():
    try:
        return json.loads(io.open(os.path.join(HERE, 'shots', '_partner_boxes.json'), encoding='utf-8').read())
    except (OSError, ValueError):
        return {}


BOXES = _boxes()
PAD = 0.008
LANGS = ('en', 'es')


def _r(lang, shot, key):
    r = BOXES.get('%s/%s' % (lang, shot), {}).get(key)
    if not r:
        raise KeyError('no measured box %s for %s/%s — run capture-partner.js' % (key, lang, shot))
    return r


def ring(shot, key, pad=PAD):
    """The measured rectangle of `key` on `shot`, padded, per language."""
    out = {}
    for lang in LANGS:
        x, y, w, h = _r(lang, shot, key)
        out[lang] = (round(x - pad, 4), round(y - pad, 4), round(w + 2 * pad, 4), round(h + 2 * pad, 4))
    return out


def at(shot, key):
    """The cursor on the middle of a measured box."""
    out = {}
    for lang in LANGS:
        x, y, w, h = _r(lang, shot, key)
        out[lang] = (round(x + w / 2, 4), round(y + h / 2, 4))
    return out


def look(rings, zoom):
    """The camera on a ring (per language), zoomed no further than lets the whole ring fit."""
    out = {}
    for lang, (x, y, w, h) in rings.items():
        z = max(1.0, min(zoom, 0.9 / w, 0.85 / h))
        out[lang] = (round(x + w / 2, 4), round(y + h / 2, 4), round(z, 3))
    return out


def span(shot, *keys):
    """One ring around several measured boxes."""
    out = {}
    for lang in LANGS:
        rs = [_r(lang, shot, k) for k in keys]
        x = min(r[0] for r in rs) - PAD
        y = min(r[1] for r in rs) - PAD
        out[lang] = (round(x, 4), round(y, 4),
                     round(max(r[0] + r[2] for r in rs) + PAD - x, 4),
                     round(max(r[1] + r[3] for r in rs) + PAD - y, 4))
    return out


def both(r):
    return {'en': r, 'es': r}


# Read off the frames: the sidebar's "Viewing as owner" banner and the "Turo enabled" toast.
BANNER = both((0.006, 0.168, 0.176, 0.086))
TOAST = {'en': (0.406, 0.252, 0.188, 0.072), 'es': (0.386, 0.252, 0.227, 0.072)}
WIDE = (0.5, 0.5, 1.0)


# =============================================================================== 51
EP51 = E(
    51, 'partner-booking-plugins',
    'For partners: turn on Turo for an owner you brought',
    'Para socios: active Turo para un propietario que trajo',
    'Choose the owner, then Booking Plugins — no need to write to us',
    'Elija al propietario y luego Booking Plugins — sin escribirnos',
    [
        B(en='You brought an owner to My E-Z Toll. You can turn on Turo, or a booking system, for them yourself.',
          es='Trajo a un propietario a My E-Z Toll. Puede activarle Turo, o un sistema de reservas, usted mismo.',
          shot='prt-01-select-owner', url='/dashboard', cam=WIDE,
          label_en='For partners', label_es='Para socios'),

        B(en='Start on the Dashboard. At the top is Select Owner. It lists every owner you brought.',
          es='Empiece en el Panel de control. Arriba está Seleccionar propietario, con todos los propietarios que '
             'trajo.',
          cam=look(span('prt-01-select-owner', 'card', 'picker'), 1.3), ring=span('prt-01-select-owner', 'card', 'picker'),
          point=at('prt-01-select-owner', 'picker'), click=2.0,
          label_en='Dashboard · Select Owner', label_es='Panel de control · Seleccionar propietario'),

        B(en='Choose the owner.',
          es='Elija al propietario.',
          shot='prt-02-viewing-as', cam=look(ring('prt-02-viewing-as', 'picker'), 1.4),
          ring=ring('prt-02-viewing-as', 'picker')),

        B(en='On the left you now see whose account is open. What you do next is done for this owner.',
          es='A la izquierda ve ahora qué cuenta está abierta. Lo que haga a continuación se hace para este '
             'propietario.',
          cam=look(BANNER, 2.0), ring=BANNER),

        B(en='Open Administration, then Settings, and the Booking Plugins tab.',
          es='Abra Administración, luego Configuración, y la pestaña Plugins de reservas.',
          shot='prt-03-plugins-empty', url='/admin/settings', cam=look(ring('prt-03-plugins-empty', 'tab'), 1.6),
          ring=ring('prt-03-plugins-empty', 'tab'), point=at('prt-03-plugins-empty', 'tab'), click=1.4,
          label_en='Settings · Booking Plugins', label_es='Configuración · Plugins de reservas'),

        B(en='Nothing is on yet. Open Add booking plugin.',
          es='Todavía no hay nada activo. Abra Añadir plugin de reservas.',
          cam=look(ring('prt-03-plugins-empty', 'add'), 1.8), ring=ring('prt-03-plugins-empty', 'add'),
          point=at('prt-03-plugins-empty', 'add'), click=1.2),

        B(en='Choose Turo. It is on at once: Turo enabled for this owner.',
          es='Elija Turo. Queda activo al instante: Turo activado para este propietario.',
          shot='prt-04-turo-enabled', cam=look(TOAST, 1.6), ring=TOAST),

        B(en='From now on, bookings are made from the owner’s Turo emails. So the owner forwards those emails '
             'to their My E-Z Toll mailbox. Turo, part two, shows how.',
          es='A partir de ahora, las reservas se crean con los correos de Turo del propietario. Por eso el '
             'propietario reenvía esos correos a su buzón de My E-Z Toll. Turo, parte dos, muestra cómo.',
          say_en='From now on, bookings are made from the owner’s Turo emails. So the owner forwards those '
                 'emails to their My E Z Toll mailbox. Turo, part two, shows how.',
          say_es='A partir de ahora, las reservas se crean con los correos de Turo del propietario. Por eso el '
                 'propietario reenvía esos correos a su buzón de My E Z Toll. Turo, parte dos, muestra cómo.',
          cam=look(ring('prt-04-turo-enabled', 'card'), 1.5), ring=ring('prt-04-turo-enabled', 'card')),

        B(en='And each car needs the make, model and year of its Turo listing. That is how a booking finds its car.',
          es='Y cada coche necesita la marca, el modelo y el año de su anuncio en Turo. Así una reserva encuentra '
             'su coche.',
          cam=look(ring('prt-04-turo-enabled', 'card'), 1.5)),

        B(en='A booking system, like HQ Rental Software, opens a form for its login details instead. Fill it in '
             'and save.',
          es='Un sistema de reservas, como HQ Rental Software, abre en cambio un formulario para sus datos de '
             'acceso. Rellénelo y guárdelo.',
          cam=look(ring('prt-04-turo-enabled', 'add'), 1.8), ring=ring('prt-04-turo-enabled', 'add')),

        B(en='You can also change or remove a plugin yourself, here or from the Partners page.',
          es='También puede cambiar o quitar un plugin usted mismo, aquí o desde la página Socios.',
          cam=WIDE),

        B(en='When you are done, press the cross on the owner card, on the left, to go back to your own account.',
          es='Al terminar, pulse la cruz de la tarjeta del propietario, a la izquierda, para volver a su propia '
             'cuenta.',
          shot='prt-02-viewing-as', url='/dashboard', cam=look(BANNER, 2.0), ring=BANNER),
    ])
EP51.audience = 'partner'
EP51.privacy = 'public'
