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
    """One beat: a line of narration and the screen that goes with it.

    English and Spanish are the two the series is written in. Any other language rides
    along as keyword arguments named by its code — `tr='…'`, `say_tr='…'`, `label_tr='…'`
    — or is added to a whole episode at once with `E.translate`.
    """

    def __init__(self, en, es, shot=None, url=None, cam=(0.5, 0.5, 1.0),
                 point=None, click=None, ring=None, ring_out=None,
                 label_en=None, label_es=None, hold=0.0, say_en=None, say_es=None, **more):
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
        # Whether this beat names its own caption (the ones after it inherit it).
        self.own_label = label_en is not None
        for key, value in more.items():
            if key.startswith('say_'):
                self.say[key[4:]] = value
            elif key.startswith('label_'):
                self.label[key[6:]] = value
            elif key in LANGS:
                self.text[key] = value
                self.say.setdefault(key, value)
            else:
                raise TypeError('unknown beat argument %r' % key)


class E(object):
    """One episode.

    `audience` is who the episode is for. 'owner' (the default) is the public owner series:
    the series playlist, the /tutorials page. 'partner' is for partners only: uploaded as
    unlisted, kept out of the owner series and off the website, shown only through its
    topic playlist — so a fleet owner is never shown what a partner is told about money.
    """

    audience = 'owner'
    # A partner episode is unlisted unless it says otherwise (series_n: the API episodes are public).
    privacy = None

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

    @property
    def langs(self):
        """The languages this episode can be built in: every one it has a title for."""
        return [lang for lang in LANGS if (self.title.get(lang) or '').strip()]

    def translate(self, lang, title, sub, lines):
        """Add a language to the whole episode.

        `lines` has one entry per beat, in order: the subtitle as a string, or a dict
        {'text': …, 'say': …, 'label': …}. A beat that names its own caption in English
        needs a 'label'; the beats after it inherit it, as they do in English.
        """
        if len(lines) != len(self.beats):
            raise ValueError('ep%02d %s: %d lines for %d beats' % (self.num, lang, len(lines), len(self.beats)))
        self.title[lang] = title
        self.sub[lang] = sub
        for b, line in zip(self.beats, lines):
            line = {'text': line} if isinstance(line, str) else line
            b.text[lang] = line['text']
            b.say[lang] = line.get('say') or line['text']
            if b.own_label:
                if not line.get('label'):
                    raise ValueError('ep%02d %s: a beat with its own caption needs a label' % (self.num, lang))
                # Inheriting beats share this dict, so they inherit the new language too.
                b.label[lang] = line['label']


# The languages the pipeline knows, in the order they are built. Every episode has 'en' and
# 'es'; the others are added per episode (E.translate). RTL are written right to left.
LANGS = ('en', 'es', 'tr', 'uk', 'uz', 'ka', 'hy', 'fa', 'ur')
RTL = ('fa', 'ur')

# The eyebrow over the title card of a partner episode (see E.audience).
PARTNER_EYEBROW = {'en': 'MyEZToll · Partner Guide', 'es': 'MyEZToll · Guía para socios'}

# The words on the two cards that top and tail every episode.
CARD = {
    'en': {'eyebrow': 'MyEZToll · Owner Portal',
           'end_title': 'That is the whole of it.',
           'end_sub': 'The written guide covers every field on every screen.'},
    'es': {'eyebrow': 'MyEZToll · Portal del Propietario',
           'end_title': 'Y eso es todo.',
           'end_sub': 'La guía escrita cubre cada campo de cada pantalla.'},
    'tr': {'eyebrow': 'MyEZToll · Sahip Portalı',
           'end_title': 'Hepsi bu kadar.',
           'end_sub': 'Yazılı kılavuz her ekrandaki her alanı anlatır.'},
    'uk': {'eyebrow': 'MyEZToll · Портал власника',
           'end_title': 'Ось і все.',
           'end_sub': 'Письмовий посібник описує кожне поле на кожному екрані.'},
    'uz': {'eyebrow': 'MyEZToll · Egasi portali',
           'end_title': 'Hammasi shu.',
           'end_sub': 'Yozma qo‘llanma har bir ekrandagi har bir maydonni tushuntiradi.'},
    'ka': {'eyebrow': 'MyEZToll · მფლობელის პორტალი',
           'end_title': 'სულ ეს არის.',
           'end_sub': 'წერილობითი სახელმძღვანელო აღწერს ყველა ველს ყველა ეკრანზე.'},
    'hy': {'eyebrow': 'MyEZToll · Սեփականատիրոջ պորտալ',
           'end_title': 'Այսքանը։',
           'end_sub': 'Գրավոր ուղեցույցը նկարագրում է յուրաքանչյուր էկրանի յուրաքանչյուր դաշտ։'},
    'fa': {'eyebrow': 'پورتال مالک · MyEZToll',   # RTL: the Persian first, so the line runs right to left
           'end_title': 'همین بود.',
           'end_sub': 'راهنمای نوشتاری همهٔ فیلدهای هر صفحه را توضیح می‌دهد.'},
    'ur': {'eyebrow': 'مالک پورٹل · MyEZToll',
           'end_title': 'بس اتنا ہی۔',
           'end_sub': 'تحریری گائیڈ ہر اسکرین کے ہر خانے کی وضاحت کرتی ہے۔'},
}
