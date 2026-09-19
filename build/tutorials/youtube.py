# -*- coding: utf-8 -*-
"""Write the text that goes in the YouTube upload form, so nobody retypes it.

    python youtube.py

Out come `mp4/youtube-en.md` and `mp4/youtube-es.md`: for each episode its title, the
description, the tags, and the chapter list with real timestamps read off the built
timeline — so the chapters match the video rather than an estimate of it.

YouTube turns a description line beginning `0:00` into a chapter marker, and requires
the first one to be exactly 0:00 and at least three of them in ascending order. Each
episode's chapters are its captioned sections: a beat that changes the on-screen
caption starts a new one.
"""
import io
import json
import os
import re
import sys

import episodes

HERE = os.path.dirname(os.path.abspath(__file__))

BLURB = {
    'en': ('The MyEZToll owner portal, one screen at a time. This series walks through '
           'every page of the portal — what it is for, what each field does, and the '
           'mistakes that cost fleet owners money.'),
    'es': ('El portal del propietario de MyEZToll, pantalla a pantalla. Esta serie '
           'recorre cada página del portal: para qué sirve, qué hace cada campo, y los '
           'errores que le cuestan dinero a los dueños de flotas.'),
}

FOOTER = {
    'en': ('The written guide covers every field on every screen: myeztoll.com\n'
           'Portal: owner.myeztoll.com\n\n'
           'Subtitles are available on this video — turn them on with the CC button.'),
    'es': ('La guía escrita cubre cada campo de cada pantalla: myeztoll.com\n'
           'Portal: owner.myeztoll.com\n\n'
           'Este vídeo tiene subtítulos: actívelos con el botón CC.'),
}

TAGS = {
    'en': ['myeztoll', 'fleet management', 'car rental software', 'toll management',
           'rental fleet', 'tolls', 'car sharing', 'turo host', 'fleet owner', 'tutorial'],
    'es': ['myeztoll', 'gestión de flotas', 'software de alquiler de coches',
           'gestión de peajes', 'flota de alquiler', 'peajes', 'carsharing',
           'anfitrión turo', 'dueño de flota', 'tutorial'],
}

SERIES_NAME = {'en': 'MyEZToll Owner Portal', 'es': 'Portal del Propietario MyEZToll'}

# One playlist per language. Mixing them strands half the audience on every second
# video and teaches YouTube to recommend the series to people who cannot follow it.
PLAYLIST = {
    'en': {
        'title': 'MyEZToll Owner Portal — Full Tutorial Series',
        'language': 'English',
        'description': """Every screen of the MyEZToll owner portal, in order, from your first sign-in to the reports your accountant wants.

Twenty-six episodes. 1 to 8 are your first week — the tour, your settings, connecting toll agencies, loading the fleet, transponders, prices and bookings. 9 to 14 are the money: tolls, charges, violations, failed payments and disputes, Stripe, and payouts. 15 to 21 cover GPS and alerts, drivers, bookings that arrive from a platform, your storefront, reports, and the settings tabs that are easy to miss. 22 to 26 are Turo: your own mailbox, forwarding your Turo emails from Gmail, the phone app, tying listings to your cars, and pending bookings.

Watch in order the first time; after that each episode stands on its own.

Subtitles on every video. Written guide: myeztoll.com
Portal: owner.myeztoll.com""",
    },
    'es': {
        'title': 'Portal del Propietario MyEZToll — Serie completa de tutoriales',
        'language': 'Spanish',
        'description': """Cada pantalla del portal del propietario de MyEZToll, en orden, desde su primer inicio de sesión hasta los informes que le pide su contable.

Veintiséis episodios. Del 1 al 8 es su primera semana: el recorrido, sus ajustes, conectar las agencias de peaje, cargar la flota, los transpondedores, los precios y las reservas. Del 9 al 14, el dinero: peajes, cargos, multas, pagos fallidos y disputas, Stripe, y las liquidaciones. Del 15 al 21: GPS y alertas, conductores, reservas que llegan de una plataforma, su sitio, los informes, y las pestañas de configuración que se pasan por alto. Del 22 al 26, Turo: su propio buzón, reenviar sus correos de Turo desde Gmail, la aplicación del teléfono, atar los anuncios a sus coches, y las reservas pendientes.

La primera vez, véalos en orden; después cada episodio se sostiene solo.

Subtítulos en todos los vídeos. Guía escrita: myeztoll.com
Portal: owner.myeztoll.com""",
    },
}


def clock(seconds):
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return ('%d:%02d:%02d' % (h, m, s)) if h else ('%d:%02d' % (m, s))


def timeline(ep, lang):
    path = os.path.join(HERE, 'ep%02d.%s.html' % (ep.num, lang))
    if not os.path.exists(path):
        return None
    html = io.open(path, encoding='utf-8').read()
    return json.loads(re.search(r'var FILM = (\{.*?\});\n', html, re.S).group(1))


def chapters(film, lang):
    """One chapter per change of on-screen caption, starting at 0:00."""
    out, last = [], None
    for beat in film['beats']:
        label = (beat.get('label') or '').strip()
        if label and label != last:
            out.append((beat['t'], label))
            last = label
    if not out:
        return []
    # YouTube insists the first chapter is 0:00.
    out[0] = (0.0, out[0][1])
    return out


def main(argv):
    langs = [a for a in argv if a in ('en', 'es')] or ['en', 'es']
    # publish.py uploads from mp4/upload-queue.json; it is written here from the same data as the
    # .md files, so the descriptions and chapters it uploads are always the current ones.
    qpath = os.path.join(HERE, 'mp4', 'upload-queue.json')
    queue = json.loads(io.open(qpath, encoding='utf-8').read()) if os.path.exists(qpath) else {}
    for lang in langs:
        pl = PLAYLIST[lang]
        lines = ['# %s — YouTube metadata (%s)' % (SERIES_NAME[lang], lang), '',
                 'Upload the mp4 and attach the matching .srt as a caption track rather '
                 'than burning the subtitles in.', '',
                 '## The playlist', '',
                 '**Title**', '', '```', pl['title'], '```', '',
                 '**Description**', '', '```', pl['description'], '```', '',
                 '| Field | Set it to |',
                 '|---|---|',
                 '| Visibility | Public |',
                 '| **Default video order** | **Manual**, then drag 1 to %d into order |' % len(episodes.SERIES),
                 '| Language | %s |' % pl['language'],
                 '',
                 'The order matters more than it looks. YouTube offers *Date published '
                 '(newest)* by default, which would put the last episode first and run the '
                 'series backwards; *oldest* only works if the uploads happen in order '
                 'and none is ever re-uploaded. Manual is the one that survives both.',
                 '',
                 'Keep the two languages in separate playlists — a mixed one strands half '
                 'the audience on every second video.',
                 '']
        missing = []
        for ep in episodes.SERIES:
            film = timeline(ep, lang)
            if film is None:
                missing.append(ep.num)
                continue
            name = 'myeztoll-tutorial-%02d-%s-%s' % (ep.num, ep.slug, lang)
            title = '%s — %d. %s' % (SERIES_NAME[lang], ep.num, ep.title[lang])

            lines += ['---', '', '## %02d · %s' % (ep.num, ep.slug), '',
                      '**File:** `%s.mp4` · captions `%s.srt` · %s' %
                      (name, name, clock(film['total'])), '',
                      '**Title**', '', '```', title, '```', '',
                      '**Description**', '', '```']
            body = ['%s' % ep.sub[lang], '', BLURB[lang], '']
            marks = chapters(film, lang)
            if len(marks) >= 3:
                body.append('')
                for t, label in marks:
                    body.append('%s %s' % (clock(t), label))
                body.append('')
            body.append(FOOTER[lang])
            lines += body
            lines += ['```', '', '**Tags:** ' + ', '.join(TAGS[lang]), '']

            queue[name] = {
                'num': ep.num, 'lang': lang, 'title': title,
                'description': '\n'.join(body),
                'file': os.path.join(HERE, 'mp4', name + '.mp4'),
                'playlist': pl['title'],
            }

        out = os.path.join(HERE, 'mp4', 'youtube-%s.md' % lang)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        io.open(out, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
        note = (' (%d not built yet)' % len(missing)) if missing else ''
        print('  %s  %d episodes%s  ->  %s' %
              (lang, len(episodes.SERIES) - len(missing), note, os.path.basename(out)))
    io.open(qpath, 'w', encoding='utf-8').write(json.dumps(queue, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main(sys.argv[1:])
