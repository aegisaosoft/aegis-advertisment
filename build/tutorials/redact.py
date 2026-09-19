# -*- coding: utf-8 -*-
"""Blur what the documentation capture missed — nothing, as of 2026-09-06.

    python redact.py            # rebuild every redacted shot (REGIONS is empty)
    python redact.py --check    # say what is missing, change nothing

This pass existed because `docs/tools/capture-screenshots.js --blur` did not reach two
screens: `94-sms-log` shipped real mobile numbers and customers' names in its Phone and
Renter columns, and `93-messages` shipped subject lines reading "<first name> has sent
you a message about your car". A screenshot in a written guide is one thing; a frame of
a video published to YouTube is another, so these were blurred again here.

**Both are fixed at the source and this pass is now empty.** The capture rules cover
the mail list's subject lines and the SMS log's columns, `docs/tools/redaction-dom.test.js`
holds them to it, and all eight languages were recaptured. Measured per band on the
recaptured shots — edge energy, a blurred block sits near 1 and text sits in the teens
and up:

    93-messages  subject lines   27.5 -> 1.8    timestamps 24.8 (left readable)
    94-sms-log   Phone column    13.7 -> 1.3    Renter 0.9,  Date 12.2 (readable)

An earlier note in this file said `93-messages` was NOT fixed and gave numbers for it.
Those numbers came from a region covering the whole message list, timestamps included —
and the timestamps are deliberately left sharp, so the region read as "text" whatever
happened to the subjects. Measure the subject bands on their own.

REGIONS is kept rather than deleted: if a future screen ever needs a second pass, this
is where it goes. With it empty, `build.py` finds nothing under `shots/` and falls back
to `docs/images` for every screen, which is the point.
"""
import io
import os
import sys

from PIL import Image, ImageFilter

import build

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = 'C:\\aegis-aa\\docs\\images'
OUT = os.path.join(HERE, 'shots')
LANGS = ('en', 'es')

# key -> regions as fractions of the image (x, y, w, h).
# key -> regions as fractions of the image (x, y, w, h).
#
# Empty: the capture harness redacts both screens itself now. Leaving an entry here
# would paste pixel blur over the real redaction and blur the timestamps and the
# status column with it.
REGIONS = {}

RADIUS = 14


def source(lang, key):
    """The best available original, skipping this pass's own output."""
    for root in build.SHOT_DIRS[1:]:
        p = os.path.join(root, lang, key + '.png')
        if os.path.exists(p):
            return p
    return None


def redact(lang, key, regions):
    src = source(lang, key)
    if src is None:
        return None
    im = Image.open(src).convert('RGB')
    w, h = im.size
    for fx, fy, fw, fh in regions:
        box = (int(fx * w), int(fy * h), int((fx + fw) * w), int((fy + fh) * h))
        # Blur the crop and paste it back: blurring the whole image and masking would
        # pull unblurred pixels in from outside the box at its edges.
        im.paste(im.crop(box).filter(ImageFilter.GaussianBlur(RADIUS)), box)
    out_dir = os.path.join(OUT, lang)
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, key + '.png')
    im.save(dest)
    return dest


def main(argv):
    if '--check' in argv:
        missing = [(lang, key) for lang in LANGS for key in REGIONS
                   if not os.path.exists(os.path.join(OUT, lang, key + '.png'))]
        print('missing: %s' % (missing or 'none'))
        return 1 if missing else 0
    for lang in LANGS:
        for key, regions in REGIONS.items():
            dest = redact(lang, key, regions)
            print('  %s  %s  %s' % (lang, key, 'written' if dest else 'no source'))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
