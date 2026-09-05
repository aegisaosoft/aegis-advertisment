"""Localised crops of the owner-web screens.

    python build_shots_lang.py fr pt de

The plate/transponder columns are blurred unconditionally on every screen that
has one. The capture run redacts them for some languages and not others (the
Spanish set shipped them in the clear), so this does not trust the source.
"""
import base64
import io
import json
import os
import sys

from PIL import Image, ImageFilter

SRC_ROOT = r'C:\aegis-aa\docs\images'
WIDTH = 1180
QUALITY = 80

# Blur bands over the identifying columns, in original-image coordinates.
# Deliberately generous: covering a neighbouring column costs nothing,
# leaking a plate costs a lot.
GUARD = {
    # start below the header row so column titles stay readable, and run wide:
    # German plates sit further right than Spanish ones.
    '61-toll-transactions.png':    [(700, 332, 950, 805)],
    '63-violations.png':           [(552, 300, 725, 650)],
    '62-charges.png':              [(838, 345, 1070, 805)],
}

SHOTS = {
    'tolls':     ('61-toll-transactions.png',        (324, 12, 1580, 800)),
    'violations':('63-violations.png',               (324, 12, 1580, 500)),
    'charges':   ('62-charges.png',                  (340, 258, 1570, 836)),
    'map':       ('81-gps-trip-map.png',             (618, 72, 1580, 908)),
    'driver':    ('73-distribution-charges.png',     (378, 618, 1522, 1600)),
    'income':    ('95-account-statement-report.png', (324, 318, 1582, 1112)),
}

# Some locales lay the toolbar out on one line instead of two; trim accordingly.
CROP_OVERRIDE = {
    'en': {'tolls': (324, 12, 1580, 742), 'violations': (324, 12, 1580, 694),
           'charges': (340, 262, 1570, 832)},
}


def build(lang):
    src = os.path.join(SRC_ROOT, lang)
    if not os.path.isdir(src):
        raise SystemExit('no screenshots for ' + lang)
    out = 'shots_' + lang
    os.makedirs(out, exist_ok=True)

    bank = {}
    for name, (fn, box) in SHOTS.items():
        box = CROP_OVERRIDE.get(lang, {}).get(name, box)
        im = Image.open(os.path.join(src, fn)).convert('RGB')
        for r in GUARD.get(fn, []):
            im.paste(im.crop(r).filter(ImageFilter.GaussianBlur(10)), r)
        im = im.crop(box)
        if im.width > WIDTH:
            im = im.resize((WIDTH, round(im.height * WIDTH / im.width)), Image.LANCZOS)
        path = os.path.join(out, name + '.webp')
        im.save(path, 'WEBP', quality=QUALITY, method=6)
        raw = io.open(path, 'rb').read()

        # Some capture runs caught the map before its tiles loaded (the Russian
        # one is a blank grey pane). A map carries no interface text, so borrowing
        # a good one from another locale changes nothing the viewer can read.
        if name == 'map' and len(raw) < 20 * 1024 and lang != 'en':
            alt = Image.open(os.path.join(SRC_ROOT, 'en', fn)).convert('RGB').crop(box)
            if alt.width > WIDTH:
                alt = alt.resize((WIDTH, round(alt.height * WIDTH / alt.width)), Image.LANCZOS)
            alt.save(path, 'WEBP', quality=QUALITY, method=6)
            raw = io.open(path, 'rb').read()
            print('  %-11s map was blank for %s - borrowed the English capture' % ('', lang))
        bank[name] = 'data:image/webp;base64,' + base64.b64encode(raw).decode('ascii')
        print('  %-11s %4dx%-4d %5.0f KB%s' % (name, im.width, im.height, len(raw) / 1024.0,
                                               '  [plates blurred]' if fn in GUARD else ''))

    io.open(os.path.join(out, 'shots.json'), 'w', encoding='utf-8').write(json.dumps(bank))
    print('  payload %.2f MB -> %s\n' % (sum(len(v) for v in bank.values()) / 1048576.0, out))


for lg in (sys.argv[1:] or ['fr', 'pt', 'de']):
    print(lg + ':')
    build(lg)
