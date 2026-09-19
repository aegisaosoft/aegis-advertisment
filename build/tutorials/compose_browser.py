# -*- coding: utf-8 -*-
"""Turn a full-screen capture of a browser window into a film shot.

    python compose_browser.py <screen.png> <shot-key> [x0,y0,x1,y1 ...]

For pages that are not the portal (Gmail's settings, for the forwarding episode). The capture
is the whole 1920x1080 screen: the browser's tab strip, address and bookmarks bar are cut off
the top and the Windows taskbar off the bottom, so the shot shows the page and nothing of the
machine it was taken on. Each x0,y0,x1,y1 box (pixels of the capture) is blurred -- Gmail's
own label list, an account address. The result goes to `shots/en/` and `shots/es/`.
"""
import os
import sys

from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
TOP = 120       # tab strip + address bar + bookmarks bar at 100% scaling on a 1080p screen
BOTTOM = 1030   # the taskbar starts at 1040


def page_top(im):
    """Where the page starts. Chrome drops a "is being debugged" bar under the bookmarks bar while
    an automation tool is attached, in the bookmarks bar's own colour; walk down past both, and
    past the one-pixel rule under them."""
    bar = im.getpixel((300, TOP - 12))[:3]
    same = lambda y: all(abs(a - b) <= 3 for a, b in zip(im.getpixel((300, y))[:3], bar))
    y = TOP - 12
    while y < TOP + 90 and (same(y) or same(y + 2)):
        y += 1
    return max(y + 2, TOP)


def compose(src, key, boxes):
    im = Image.open(src).convert('RGB')
    top = page_top(im)
    for x0, y0, x1, y1 in boxes:
        region = im.crop((x0, y0, x1, y1)).filter(ImageFilter.GaussianBlur(9))
        im.paste(region, (x0, y0))
    # Off each side: a window under automation gets a tinted glow, wider while the bar is up.
    edge = 18 if top > TOP + 20 else 4
    page = im.crop((edge, top, im.size[0] - edge, BOTTOM - (10 if edge > 4 else 0)))
    page = page.resize((page.size[0] * 2, page.size[1] * 2), Image.LANCZOS)
    for lang in ('en', 'es'):
        out = os.path.join(HERE, 'shots', lang)
        os.makedirs(out, exist_ok=True)
        page.save(os.path.join(out, key + '.png'))
    return page.size


if __name__ == '__main__':
    boxes = [tuple(int(v) for v in a.split(',')) for a in sys.argv[3:]]
    print(sys.argv[2], compose(sys.argv[1], sys.argv[2], boxes))
