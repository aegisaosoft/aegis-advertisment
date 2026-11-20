# -*- coding: utf-8 -*-
"""Lay the FleetBold sign-in and consent pages (browser screenshots) on the series' 3200x2000 frame.

    python compose_fleetbold.py <signin.jpg> <consent.jpg> <vehicles.jpg>

These pages are FleetBold's own and English only, so the same frames go to `shots/en/` and `shots/es/`.
"""
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
KEYS = ('int-10-fb-signin', 'int-11-fb-consent', 'int-12-fb-vehicles')


def main(paths):
    for src, key in zip(paths, KEYS):
        im = Image.open(src).convert('RGB')
        h = round(im.height * 3200 / im.width)
        im = im.resize((3200, h), Image.LANCZOS)
        frame = Image.new('RGB', (3200, 2000), (245, 245, 245))
        frame.paste(im, (0, (2000 - h) // 2))
        for lang in ('en', 'es'):
            os.makedirs(os.path.join(HERE, 'shots', lang), exist_ok=True)
            frame.save(os.path.join(HERE, 'shots', lang, key + '.png'))
        print(key, h, (2000 - h) // 2)


if __name__ == '__main__':
    main(sys.argv[1:])
