# -*- coding: utf-8 -*-
"""Put one captured card on a plain frame the size of every other screen in the series.

    python compose_card.py card.png out.png      # prints {"x","y","w","h","scale"} as JSON

The card comes in at deviceScaleFactor 2 (a 700px-wide card is 1400 pixels); the frame is
3200x2000, the 1600x1000 window at the same density. The card is centred and shrunk only when it
would not fit inside the margins, never enlarged — a blown-up card is soft text. The printed box is
in fractions of the frame, which is how the episodes write their rings.
"""
import json
import sys

from PIL import Image, ImageDraw, ImageFilter

W, H = 3200, 2000
MARGIN_X, MARGIN_Y = 160, 100          # at the 2x density: 80 and 50 CSS pixels
BACKGROUND = (245, 246, 251)


def compose(src, dst):
    card = Image.open(src).convert('RGB')
    scale = min(1.0, (W - 2 * MARGIN_X) / card.width, (H - 2 * MARGIN_Y) / card.height)
    if scale < 1.0:
        card = card.resize((round(card.width * scale), round(card.height * scale)), Image.LANCZOS)
    x, y = (W - card.width) // 2, (H - card.height) // 2

    frame = Image.new('RGB', (W, H), BACKGROUND)
    # A soft shadow, so the card reads as a card and not as a hole in the page.
    shadow = Image.new('L', (W, H), 0)
    ImageDraw.Draw(shadow).rounded_rectangle((x, y + 12, x + card.width, y + card.height + 12), 20, fill=70)
    shadow = shadow.filter(ImageFilter.GaussianBlur(24))
    frame.paste(Image.new('RGB', (W, H), (40, 44, 90)), (0, 0), shadow)
    frame.paste(card, (x, y))
    frame.save(dst)

    r = lambda v: round(v, 3)
    return {'x': r(x / W), 'y': r(y / H), 'w': r(card.width / W), 'h': r(card.height / H), 'scale': r(scale)}


if __name__ == '__main__':
    print(json.dumps(compose(sys.argv[1], sys.argv[2])))
