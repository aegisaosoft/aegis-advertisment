# -*- coding: utf-8 -*-
"""Assemble the 55-second cut: shell + timeline measured off the recorded voice.

    python build.py            # both languages
    python build.py es

Nothing here decides how long anything is. The recording does: every cue starts
where the previous one actually stopped speaking, scenes end a beat after their
last word, and the visual beats are declared against cue ids rather than seconds,
so re-recording a line moves the picture with it instead of leaving it behind.

Out come `film.<lang>.html` — one self-contained file each, the narration inlined
as a data: URI — and `audio/<lang>/track.mp3`, which render.js muxes into the mp4
rather than recording the browser's speakers.
"""
import base64
import io
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ADV = os.path.dirname(os.path.dirname(HERE))

LEAD = 0.35   # beat before a scene's first word
GAP = 0.55    # breath between lines
TAIL = 1.05   # beat after a scene's last word, before the cut
END = 1.6     # the film holds on the last card

# Which cues belong to which scene, in the order the scripts are written.
SCENES = [['0-0', '0-1', '0-2'], ['1-0', '1-1', '1-2'], ['2-0', '2-1', '2-2'], ['3-0', '3-1', '3-2', '3-3']]

# Where the figures come from
# --------------------------
# `total` and `crossings` are read off that language's own screenshot. The violation
# amount is production: dbo.Violations holds 169 of them over the last 180 days,
# $50.00 to $145.00, average $69.31, and $75.00 is the second most common single
# amount. Fuel and damage carry no figure at all, because production holds none to
# quote: AdditionalServices is empty and so is BookingServices — the booking side of
# the platform works, it simply has no customer on it yet, against 1,306 imported
# bookings. Inventing a plausible fuel charge would have made it the only fabricated
# number in the film.

# Each cut shows its own locale's screenshot, so each quotes that screen's figures.
# The captures were taken on different days and genuinely differ; the narration is
# written to match, and this is the table both have to agree with.
FIGURES = {
    'en': {'total': 412.68, 'crossings': 39, 'clock': '4:12'},
    'es': {'total': 100.89, 'crossings': 15, 'clock': '3:15'},
}

# The film's own words. The narration lives in narration.<lang>.md; these are the
# things printed on screen, which are not spoken and so are not in that file.
COPY = {
    'en': {
        'TITLE': 'Four-Twelve · MyEZToll',
        'CLOCK': '4:12',
        'TOLL_AMOUNT': '$412.68',
        'VIOL_AMOUNT': '$75.00',
        'EYEBROW': 'One week · one small fleet',
        'PM': 'PM · Tuesday',
        'BILL_TITLE': 'Account statement',
        'BILL_WHO': 'Billed to: the owner',
        'ITEM_TOLL': 'Tolls · 39 crossings',
        'ITEM_CAMERA': 'Camera violations',
        'ITEM_FUEL': 'Fuel',
        'ITEM_DENT': 'Damage',
        'F_GPS': 'The car',
        'F_GPS_P': 'At that gantry, at that second.',
        'F_BOOKING': 'The booking',
        'F_BOOKING_P': 'Names the driver. Holds the card.',
        'TOTAL_LABEL': 'One week · one small fleet',
        'FREELINE': 'You pay <b>nothing</b>. And you get a share of everything that comes back.',
        'SLOGAN': 'Stop losing.<br><em>Start earning.</em>',
        'KICKER': 'A film for fleet owners',
        'POSTER_TITLE': 'Four-twelve on a Tuesday',
    },
    'es': {
        'TITLE': 'Tres y Quince · MyEZToll',
        'CLOCK': '3:15',
        'TOLL_AMOUNT': '$100.89',
        'VIOL_AMOUNT': '$75.00',
        'EYEBROW': 'Una semana · una flota pequeña',
        'PM': 'PM · Martes',
        'BILL_TITLE': 'Estado de cuenta',
        'BILL_WHO': 'A cargo del propietario',
        'ITEM_TOLL': 'Peajes · 15 cruces',
        'ITEM_CAMERA': 'Multas de cámara',
        'ITEM_FUEL': 'Gasolina',
        'ITEM_DENT': 'Daños',
        'F_GPS': 'El carro',
        'F_GPS_P': 'En ese peaje, en ese segundo.',
        'F_BOOKING': 'La reserva',
        'F_BOOKING_P': 'Dice quién manejaba. Tiene la tarjeta.',
        'TOTAL_LABEL': 'Una semana · una flota pequeña',
        'FREELINE': 'A usted no le cuesta <b>nada</b>. Y recibe parte de todo lo que se recupera.',
        'SLOGAN': 'Deje de perder.<br><em>Empiece a ganar.</em>',
        'KICKER': 'Para propietarios de flotas',
        'POSTER_TITLE': 'Tres y quince, un martes',
    },
}

# Visual beats, anchored to cues: (element, cue, in_offset, hold_until_cue, out_offset).
# `hold_until` None means the element leaves 1.4s after it arrived.
BEATS = [
    ('eyebrow',     '0-0', -0.25, '0-2', -0.10),
    ('clock',       '0-0', +0.10, '0-2', -0.15),
    ('road',        '0-0', +0.00, '0-2', -0.15),
    ('gantry',      '0-0', +0.00, '0-2', -0.15),
    ('car',         '0-0', +0.00, '0-2', -0.15),
    ('bill',        '0-2', +0.25, '2-0', -0.45),
    ('billWho',     '0-2', +0.70, '2-0', -0.50),
    ('billRow0',    '0-2', +1.05, '2-0', -0.55),
    ('billRow1',    '1-2', +0.15, '2-0', -0.60),
    ('billRow2',    '1-2', +0.85, '2-0', -0.65),
    ('billRow3',    '1-2', +1.55, '2-0', -0.70),
    ('factGps',     '2-0', +0.35, '3-0', -0.35),
    ('factBooking', '2-1', +0.10, '3-0', -0.40),
    ('snap',        '2-2', +0.25, '3-0', -0.45),
    ('total',       '3-0', +0.05, '3-2', -0.30),
    ('shot',        '3-0', +0.85, '3-2', -0.30),
    ('freeline',    '3-2', +0.05, '3-3', -0.25),
    ('wordmark',    '3-3', +0.00, None, None),
    ('slogan',      '3-3', +0.20, None, None),
    ('url',         '3-3', +0.65, None, None),
]

FADE = 0.55   # how long a beat takes to arrive or leave


def cues(lang):
    path = os.path.join(HERE, 'narration.%s.md' % lang)
    found = re.findall(r'^\*\*(\d+-\d+)\*\*\s*_\(max [\d.]+s\)_\s*\n\s*\n>\s*(.+?)\s*$',
                       io.open(path, encoding='utf-8').read(), re.M)
    if not found:
        sys.exit('%s: no cues parsed' % path)
    return dict(found), [c for c, _ in found]


def duration(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                          '-of', 'csv=p=0', path], capture_output=True, text=True)
    return float(out.stdout.strip())


def timeline(lang):
    """Absolute start and length for every cue, driven by the clips themselves."""
    text, order = cues(lang)
    clip = {cid: os.path.join(HERE, 'audio', lang, '%s.mp3' % cid) for cid in order}
    missing = [c for c in order if not os.path.exists(clip[c])]
    if missing:
        sys.exit('%s: no recording for %s — run tts.py first' % (lang, ', '.join(missing)))

    at, t = {}, 0.0
    for scene in SCENES:
        t += LEAD
        for i, cid in enumerate(scene):
            at[cid] = round(t, 3)
            t += duration(clip[cid]) + (GAP if i < len(scene) - 1 else 0)
        t += TAIL
    total = round(t - TAIL + END, 2)
    return text, order, at, {c: duration(clip[c]) for c in order}, total


def beats(at, dur, order):
    out = {}
    for el, cue, offset, until, until_offset in BEATS:
        start = at[cue] + offset
        if until:
            gone = at[until] + until_offset
        else:
            gone = at[order[-1]] + dur[order[-1]] + END
        out[el] = [round(start, 3), round(start + FADE, 3),
                   round(gone, 3), round(gone + FADE, 3)]
    return out


def track(lang, at, order, total):
    """One audio file with every clip at the second it is spoken."""
    folder = os.path.join(HERE, 'audio', lang)
    out = os.path.join(folder, 'track.mp3')
    args = ['ffmpeg', '-y', '-v', 'error']
    for cid in order:
        args += ['-i', os.path.join(folder, '%s.mp3' % cid)]
    parts, tags = [], ''
    for i, cid in enumerate(order):
        parts.append('[%d]adelay=%d|%d[a%d]' % (i, int(at[cid] * 1000), int(at[cid] * 1000), i))
        tags += '[a%d]' % i
    # apad matters: the track has to run the film's full length, silence included.
    # Without it the mix ends on the last word, and the renderer's -shortest then
    # cuts the closing card off mid-hold.
    chain = ';'.join(parts) + ';' + tags + 'amix=inputs=%d:normalize=0,apad[m]' % len(order)
    args += ['-filter_complex', chain, '-map', '[m]', '-t', str(total),
             '-c:a', 'libmp3lame', '-b:a', '192k', out]
    subprocess.run(args, check=True)
    return out


def shot(lang):
    """That language's own Toll Transactions screen.

    The Spanish cut shows the Spanish interface — that is the point of having six
    captures — which is exactly why the Spanish narration quotes $100.89 over 15
    crossings while the English quotes $412.68 over 39. A screen that contradicts
    the voice is the defect this repository has already had to go back and fix once.
    """
    shots = json.load(io.open(os.path.join(ADV, lang, 'screens', 'shots.json'), encoding='utf-8'))
    return shots['tolls']


def build(lang):
    text, order, at, dur, total = timeline(lang)
    audio = track(lang, at, order, total)
    film = {
        'total': total,
        'cues': [{'id': c, 't': at[c], 'text': text[c],
                  # the closing card carries the last line itself
                  'mute': c == order[-1]} for c in order],
        'beats': beats(at, dur, order),
        'car': [round(at['0-0'] + 0.15, 3), round(at['0-0'] + dur['0-0'] + 0.15, 3)],
        'count': [round(at['3-0'] + 0.25, 3), round(at['3-0'] + 1.75, 3)],
        'money': FIGURES[lang]['total'],
    }

    html = io.open(os.path.join(HERE, 'film_shell.html'), encoding='utf-8').read()
    html = html.replace('__TIMELINE__', json.dumps(film, ensure_ascii=False))
    html = html.replace('__AUDIO__', 'data:audio/mpeg;base64,' +
                        base64.b64encode(io.open(audio, 'rb').read()).decode('ascii'))
    html = html.replace('__SHOT__', shot(lang))
    for token, value in COPY[lang].items():
        html = html.replace('__%s__' % token, value)

    left = re.findall(r'__[A-Z_]+__', html)
    if left:
        sys.exit('%s: unfilled placeholders %s' % (lang, sorted(set(left))))

    out = os.path.join(HERE, 'film.%s.html' % lang)
    io.open(out, 'w', encoding='utf-8').write(html)
    print('%s  %5.1f s  %d cues  %.1f MB  %s'
          % (lang, total, len(order), len(html.encode('utf-8')) / 1048576.0, os.path.basename(out)))


for lg in (sys.argv[1:] or ['en', 'es']):
    build(lg)
