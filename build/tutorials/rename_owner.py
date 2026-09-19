# -*- coding: utf-8 -*-
"""Repaint the documented owner's name in the portal screenshots the films use.

    python rename_owner.py <ocr-hits.tsv>

Every portal screen carries the signed-in company in its top-left corner: an avatar with the
initials and the name beside it. The films should show a neutral company, so this paints
"Your Company" / "YC" over it -- on the existing captures rather than by recapturing them, so
every camera, cursor and ring already measured against a screen stays exactly where it was.

The hits file is Windows OCR output (see ocr_find.ps1): one line per image where the name was
read, with its word boxes; the first word's box anchors the whole block, which sits in the same
place on every screen but one. Background and text colours are sampled from the image itself,
so a screen dimmed behind a dialog is repainted dimmed. Originals are copied to
`shots/_originals/` before anything is written.
"""
import io
import ntpath
import os
import shutil
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = ImageFont.truetype(r'C:\Windows\Fonts\Inter-Regular-slnt=0.ttf', 34)
BOLD = ImageFont.truetype(r'C:\Windows\Fonts\Inter-Bold-slnt=0.ttf', 36)
NAME, INITIALS = 'Your Company', 'YC'


def lum(p):
    return 0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]


def repaint(path, x, y):
    """`x, y`: top-left of the first word of the name, in image pixels."""
    im = Image.open(path).convert('RGB')
    d = ImageDraw.Draw(im)

    # ---- the name: two lines of text to the right of the avatar
    box = (x - 8, y - 12, x + 250, y + 78)
    region = im.crop(box)
    ink = min(region.getdata(), key=lum)
    bg = im.getpixel((x - 14, y + 20))
    d.rectangle(box, fill=bg)
    d.text((x - 1, y - 6), NAME, font=FONT, fill=ink)

    # ---- the initials inside the avatar circle
    cx, cy = x - 86, y + 73
    lx0, lx1, ly0, ly1 = cx - 36, cx + 36, cy - 22, cy + 22
    light = max(im.crop((lx0, ly0, lx1, ly1)).getdata(), key=lum)
    for yy in range(ly0, ly1 + 1):
        a, b = im.getpixel((lx0 - 4, yy)), im.getpixel((lx1 + 4, yy))
        for xx in range(lx0, lx1 + 1):
            t = (xx - lx0) / float(lx1 - lx0)
            im.putpixel((xx, yy), tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3)))
    w = d.textlength(INITIALS, font=BOLD)
    d.text((cx - w / 2, cy - 23), INITIALS, font=BOLD, fill=light)
    im.save(path)


def main(hits):
    done = set()
    for line in io.open(hits, encoding='utf-8', errors='replace'):
        parts = line.rstrip('\n').split('\t')
        if len(parts) < 3 or not parts[1].startswith('Luxury Wheels'):
            continue
        path = parts[0]
        if path in done:
            continue
        x, y = [int(v) for v in parts[2].split(' ')[0].split(',')[:2]]
        backup = os.path.join(HERE, 'shots', '_originals',
                              ntpath.basename(ntpath.dirname(path)), ntpath.basename(path))
        os.makedirs(os.path.dirname(backup), exist_ok=True)
        if not os.path.exists(backup):
            shutil.copy2(path, backup)
        repaint(path, x, y)
        done.add(path)
    print('repainted %d screenshots' % len(done))


if __name__ == '__main__':
    main(sys.argv[1])
