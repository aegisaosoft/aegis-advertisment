# -*- coding: utf-8 -*-
"""The fourteen lines of the ToonBee cut, and the scene grid they are cut against.

EN is transcribed from the ToonBee project itself — the Scene Text of each of the
fourteen scenes, word for word, including the wording ToonBee rewrote when the scenes
were regenerated. Captions built from anything else drift: ToonBee's own caption
option is transcription-based and has already produced "cantry" for "gantry".

ES is the same film for the same audience — United States fleet owners, half of them
Latino — so it is US/Latin-American Spanish: carro, renta, manejar, costo, gasolina.
Never peninsular. The figures stay the English cut's figures because the picture
shows them: $412.68 over 39 crossings, and the "cuatro y doce" of line one is the
same number returning as a bill in line eight.

SCENES are the fourteen scene lengths read off the ToonBee timeline, confirmed
frame by frame against the export: the letter lands at 10.4s, the $412.68 board at
51.0s, the price discs at 64.2s, the fleet at 88.2s.
"""

SCENES = [10.4, 6.0, 6.0, 6.0, 6.0, 8.4, 8.2, 7.2, 6.0, 6.0, 6.0, 6.0, 6.0, 6.0]

EN = [
    "Tuesday. Four-twelve in the afternoon. One of your cars goes through a toll. Nobody pays. Not yet.",
    "Three weeks later, the bill arrives with your name attached.",
    "By then, the renter is gone, refunded, and the rental is closed.",
    "So you pay it, calling it the cost of doing business.",
    "The same thing happens with tickets, fuel, and vehicle damage.",
    "But the toll agencies knew. E-ZPass, SunPass, thirty-one networks in all, coast to coast.",
    "And the booking knew who was driving. MyEZToll puts those two together and collects, "
    "from the renter's card.",
    "One small fleet. One week. Four hundred twelve dollars \u2014 and it was going to be yours to swallow.",
    "So what does the platform actually cost your fleet?",
    "Nothing: no subscription, setup fee, or charge for each vehicle.",
    "Connecting the GPS you already use is free as well.",
    "The only paid option is our own telematics hardware.",
    "You pay nothing. The toll comes back to you in full \u2014 plus a share of our fee.",
    "Stop losing. Start earning.",
]

ES = [
    "Martes. Cuatro y doce de la tarde. Uno de sus carros cruza un peaje. Nadie lo paga. Todav\u00eda no.",
    "Tres semanas despu\u00e9s llega la factura, con su nombre.",
    "Para entonces el cliente ya se fue, le devolvieron el dep\u00f3sito y la renta est\u00e1 cerrada.",
    "As\u00ed que la paga usted, y lo llama el costo de hacer negocio.",
    "Lo mismo pasa con las multas, la gasolina y los da\u00f1os al veh\u00edculo.",
    "Pero las agencias de peaje s\u00ed lo sab\u00edan. E-ZPass, SunPass, treinta y una redes, "
    "de costa a costa.",
    "Y la reserva sab\u00eda qui\u00e9n manejaba. MyEZToll junta las dos cosas y cobra, "
    "a la tarjeta del cliente.",
    "Una flota peque\u00f1a. Una semana. Cuatrocientos doce d\u00f3lares \u2014 y los iba a pagar usted.",
    "\u00bfY cu\u00e1nto le cuesta en realidad la plataforma a su flota?",
    "Nada: sin suscripci\u00f3n, sin costo de instalaci\u00f3n, sin cargo por veh\u00edculo.",
    "Conectar el GPS que ya usa tambi\u00e9n es gratis.",
    "Lo \u00fanico de pago es nuestro propio equipo de telem\u00e1tica.",
    "Usted no paga nada. Recibe el peaje completo y parte de nuestra comisi\u00f3n.",
    "Deje de perder. Empiece a ganar.",
]

assert len(SCENES) == len(EN) == len(ES) == 14


def grid():
    """(start, end) of every scene, in seconds."""
    out, edge = [], 0.0
    for d in SCENES:
        out.append((edge, edge + d))
        edge += d
    return out
