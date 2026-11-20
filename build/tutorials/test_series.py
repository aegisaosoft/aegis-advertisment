# -*- coding: utf-8 -*-
"""Check the series before anything is recorded or rendered.

    python test_series.py

Everything here is cheap and catches the mistakes this pipeline actually makes. A
mistyped coordinate does not raise — it renders a spotlight over empty page, or a
cursor that clicks the footer, and the only way to find out is to sit through a
five-minute render and look. So the coordinates are checked as numbers first.

Exit code 0 if the series is sound, 1 with a list otherwise.
"""
import io
import os
import sys

from PIL import Image

import build
import episodes

LANGS = ('en', 'es')          # every episode has these two; others are per episode (ep.langs)
FAILURES = []

# Characters a language must not contain: Persian writes ی and ک, not the Arabic ي and ك;
# Armenian has nothing in the Hebrew block (its own ։ and ՝ look alike but are not there).
FORBIDDEN = {
    'fa': u'يك',
    'hy': u''.join(chr(c) for c in range(0x0590, 0x0600)),
}


def fail(where, message):
    FAILURES.append('%-28s %s' % (where, message))


def frac(value, name, where, lo=0.0, hi=1.0):
    if not isinstance(value, (int, float)):
        fail(where, '%s is %r, not a number' % (name, value))
    elif not (lo <= value <= hi):
        fail(where, '%s = %s, outside %s..%s' % (name, value, lo, hi))


def check_beat(ep, i, b):
    where = 'ep%02d beat %d' % (ep.num, i)
    langs = ep.langs

    for lang in langs:
        if not (b.text[lang] or '').strip():
            fail(where, 'no %s subtitle' % lang)
        if not (b.say[lang] or '').strip():
            fail(where, 'no %s narration' % lang)
        # The narration is read aloud; markup in it is read aloud too.
        for bad in ('<', '>', '{{', '**'):
            if bad in b.say[lang]:
                fail(where, '%s narration contains %r' % (lang, bad))
        for bad in FORBIDDEN.get(lang, ''):
            if bad in b.text[lang] + b.say[lang] + (b.label.get(lang) or ''):
                fail(where, '%s text contains U+%04X' % (lang, ord(bad)))
        if lang not in LANGS and (b.label.get('en') or '').strip() and not (b.label.get(lang) or '').strip():
            fail(where, 'no %s caption' % lang)

    for lang in langs:
        cam, _ = build.pick(b.cam, lang)
        if not (isinstance(cam, (tuple, list)) and len(cam) == 3):
            fail(where, '%s cam is not (x, y, zoom)' % lang)
            continue
        frac(cam[0], 'cam x', where)
        frac(cam[1], 'cam y', where)
        # Zooming out past the window would show the paper behind the screenshot.
        frac(cam[2], 'cam zoom', where, 1.0, 2.5)

        point, _ = build.pick(b.point, lang)
        if point is not None:
            if not (isinstance(point, (tuple, list)) and len(point) == 2):
                fail(where, '%s point is not (x, y)' % lang)
            else:
                frac(point[0], 'point x', where)
                frac(point[1], 'point y', where)

        ring, _ = build.pick(b.ring, lang)
        if ring is not None:
            if not (isinstance(ring, (tuple, list)) and len(ring) == 4):
                fail(where, '%s ring is not (x, y, w, h)' % lang)
            else:
                for name, v in zip(('ring x', 'ring y', 'ring w', 'ring h'), ring):
                    frac(v, name, where)
                if ring[0] + ring[2] > 1.001:
                    fail(where, 'ring runs off the right edge (%.3f)' % (ring[0] + ring[2]))
                if ring[1] + ring[3] > 1.001:
                    fail(where, 'ring runs off the bottom (%.3f)' % (ring[1] + ring[3]))
                if ring[2] <= 0 or ring[3] <= 0:
                    fail(where, 'ring has no area')

    if b.click is not None:
        if not isinstance(b.click, (int, float)) or b.click < 0:
            fail(where, 'click at %r' % b.click)
        elif b.point is None:
            # A click with no cursor is a ripple appearing out of nowhere.
            fail(where, 'click with no point to click on')

    if b.hold < 0:
        fail(where, 'negative hold')


def check_shots(ep):
    """Every screenshot the episode names exists in both languages, same width."""
    for key in dict.fromkeys(b.shot for b in ep.beats):
        sizes = {}
        for lang in ep.langs:
            path = build.shot_file(lang, key)
            if not os.path.exists(path):
                fail('ep%02d' % ep.num, 'missing %s shot %s' % (lang, key))
            else:
                sizes[lang] = Image.open(path).size
        if len(sizes) == len(ep.langs):
            widths = [w for w, _ in sizes.values()]
            spread = max(widths) - min(widths)
            # A vertical scrollbar costs the content about 8 CSS pixels, so a page that
            # scrolls in one language and not the other is legitimately that much
            # narrower — 16 px in a 2x capture. That shifts an x fraction by a couple of
            # pixels on screen, which is invisible. Anything wider than a scrollbar is a
            # real layout difference and every x on that screen is suspect.
            if spread > 20:
                fail('ep%02d' % ep.num,
                     '%s differs in width beyond a scrollbar: %s' % (key, sizes))


def check_mapped(ep):
    """After mapping onto another language's capture, a ring still has to be on the page."""
    for lang in ep.langs:
        if lang == 'en':
            continue
        for i, b in enumerate(ep.beats):
            if not os.path.exists(build.shot_file(lang, b.shot)):
                continue                      # check_shots has already said so
            en_h = Image.open(build.shot_file('en', b.shot)).size[1]
            lang_h = Image.open(build.shot_file(lang, b.shot)).size[1]
            my = build.y_mapper(b.shot, lang, en_h, lang_h)
            ring, measured = build.pick(b.ring, lang)
            if not ring:
                continue
            top = ring[1] if measured else my(ring[1])
            bottom = (ring[1] + ring[3]) if measured else my(ring[1] + ring[3])
            if bottom > 1.001 or bottom <= top:
                fail('ep%02d beat %d' % (ep.num, i),
                     'ring maps off the %s capture (%.3f..%.3f)' % (lang, top, bottom))


def main():
    nums = [e.num for e in episodes.SERIES]
    if len(set(nums)) != len(nums):
        fail('series', 'duplicate episode number')
    if len(set(e.slug for e in episodes.SERIES)) != len(nums):
        fail('series', 'duplicate slug')
    if nums != sorted(nums):
        fail('series', 'episodes are out of order')

    for ep in episodes.SERIES:
        if not ep.beats:
            fail('ep%02d' % ep.num, 'no beats')
        for lang in LANGS:
            if not (ep.title.get(lang) or '').strip():
                fail('ep%02d' % ep.num, 'no %s title' % lang)
        for lang in ep.langs:
            if not (ep.sub.get(lang) or '').strip():
                fail('ep%02d' % ep.num, 'no %s subtitle line' % lang)
        check_shots(ep)
        check_mapped(ep)
        for i, b in enumerate(ep.beats):
            check_beat(ep, i, b)

    beats = sum(len(e.beats) for e in episodes.SERIES)
    if FAILURES:
        print('%d problems across %d episodes, %d beats:\n' % (len(FAILURES), len(nums), beats))
        for line in FAILURES:
            print('  ' + line)
        return 1
    extra = sorted(set(l for e in episodes.SERIES for l in e.langs) - set(LANGS))
    print('ok: %d episodes, %d beats, en+es%s' % (len(nums), beats, (' (+%s on some)' % ','.join(extra)) if extra else ''))
    return 0


if __name__ == '__main__':
    sys.exit(main())
