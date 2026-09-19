# -*- coding: utf-8 -*-
"""What an episode is made of. No content lives here — see `series_*.py` for that.

A beat is one spoken line plus the state of the screen while that line is spoken. The
recording decides how long a beat lasts, so writing a longer line moves the picture
rather than desynchronising it.

Coordinates are fractions, never pixels, and they are written against the **English**
capture. `docs/images/en` and `docs/images/es` are the same width and laid out from the
top, differing only in total height where a translated footer wraps differently, so
build.py re-bases every vertical fraction onto the target language automatically. Only
a horizontal position that genuinely moves — a right-aligned control pushed by a longer
label — needs writing out per language, as `{'en': ..., 'es': ...}`.

    cam   = (focus x, focus y, zoom). Zoom 1.0 is the page filling the window.
    point = (x, y) the cursor travels to, or None for no cursor.
    click = seconds into the beat when the click lands, or None.
    ring  = (x, y, w, h) lit through a dimmed page, or None.
"""


class B(object):
    """One beat: a line of narration and the screen that goes with it."""

    def __init__(self, en, es, shot=None, url=None, cam=(0.5, 0.5, 1.0),
                 point=None, click=None, ring=None, ring_out=None,
                 label_en=None, label_es=None, hold=0.0, say_en=None, say_es=None):
        # What the subtitle shows. `say` is what the voice reads, when the two differ:
        # a subtitle wants "owner.myeztoll.com" and a narrator wants it spelled out.
        self.text = {'en': en, 'es': es}
        self.say = {'en': say_en or en, 'es': say_es or es}
        self.shot = shot
        self.url = url
        self.cam = cam
        self.point = point
        self.click = click
        self.ring = ring
        self.ring_out = ring_out
        self.label = {'en': label_en, 'es': label_es}
        self.hold = hold          # extra seconds held after the line, for a busy screen


class E(object):
    """One episode."""

    def __init__(self, num, slug, title_en, title_es, sub_en, sub_es, beats):
        self.num = num
        self.slug = slug
        self.title = {'en': title_en, 'es': title_es}
        self.sub = {'en': sub_en, 'es': sub_es}
        self.beats = beats
        # A beat inherits the shot and the caption of the beat before it, so only the
        # changes have to be written down.
        shot, url, label = None, None, {'en': None, 'es': None}
        for b in beats:
            if b.shot is None:
                b.shot, b.url = shot, url
            else:
                shot = b.shot
                url = b.url if b.url is not None else url
                b.url = url
            if b.label['en'] is None:
                b.label = label
            else:
                label = b.label


# The words on the two cards that top and tail every episode.
CARD = {
    'en': {'eyebrow': 'MyEZToll · Owner Portal',
           'end_title': 'That is the whole of it.',
           'end_sub': 'The written guide covers every field on every screen.'},
    'es': {'eyebrow': 'MyEZToll · Portal del Propietario',
           'end_title': 'Y eso es todo.',
           'end_sub': 'La guía escrita cubre cada campo de cada pantalla.'},
}
