# -*- coding: utf-8 -*-
"""Put a phone screenshot on a 16:10 canvas so the film can treat it like a portal capture.

    python compose_phone.py <source.png> <shot-key>

The film fills its window with the screenshot (cover-scaling), so a 1080x2340 portrait capture
dropped in as-is would be blown up to the width of the window and show a sliver of it. This
draws the phone at the centre of a 3200x2000 canvas instead — the same size as the 2x portal
captures — and writes it to `shots/en/` and `shots/es/` (the phone runs in English in both
films; build.SHOT_DIRS reads `shots/` first).

The top of the capture is the Android status bar: the clock, and the icons of whatever other
apps the phone owner has notifications from. It is cut off rather than blurred.

Coordinates in the episode files are fractions of the canvas; `to_canvas` prints where a point
of the phone capture lands, so a control can be measured on the capture and written once.
"""
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
CANVAS = (3200, 2000)
BG = (238, 240, 246)
BEZEL = (22, 22, 30)
STATUS_BAR = 110          # px of the 1080-wide capture taken by the status bar
PHONE_H = 1860            # height of the drawn screen on the canvas
BEZEL_W = 26
RADIUS = 70


def layout(src_size):
    w, h = src_size
    h -= STATUS_BAR
    scale = PHONE_H / float(h)
    sw, sh = int(round(w * scale)), PHONE_H
    x = (CANVAS[0] - sw) // 2
    y = (CANVAS[1] - sh) // 2
    return scale, x, y, sw, sh


def to_canvas(src_size, px, py):
    """Fraction of the canvas where pixel (px, py) of the original capture lands."""
    scale, x, y, _, _ = layout(src_size)
    return ((x + px * scale) / CANVAS[0], (y + (py - STATUS_BAR) * scale) / CANVAS[1])


def compose(src, key):
    im = Image.open(src).convert('RGB')
    scale, x, y, sw, sh = layout(im.size)
    screen = im.crop((0, STATUS_BAR, im.size[0], im.size[1])).resize((sw, sh), Image.LANCZOS)

    canvas = Image.new('RGB', CANVAS, BG)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((x - BEZEL_W, y - BEZEL_W, x + sw + BEZEL_W, y + sh + BEZEL_W),
                           radius=RADIUS + BEZEL_W, fill=BEZEL)
    mask = Image.new('L', (sw, sh), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, sw, sh), radius=RADIUS, fill=255)
    canvas.paste(screen, (x, y), mask)

    for lang in ('en', 'es'):
        out = os.path.join(HERE, 'shots', lang)
        os.makedirs(out, exist_ok=True)
        canvas.save(os.path.join(out, key + '.png'))
    return canvas


if __name__ == '__main__':
    compose(sys.argv[1], sys.argv[2])
    a = to_canvas((1080, 2340), 0, STATUS_BAR)
    b = to_canvas((1080, 2340), 1080, 2340)
    print('%s: screen spans x %.3f-%.3f, y %.3f-%.3f' % (sys.argv[2], a[0], b[0], a[1], b[1]))
