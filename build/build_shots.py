"""Crop the owner-web screenshots down to the part that carries the message,
then encode them for inlining.

The sidebar and footer are cropped away on purpose: they carry the tenant's own
company name and contact details, and they steal room from the data that
actually sells. Source images are already blur-redacted (docs/images/_manifest
records blurred: true).
"""
import base64
import io
import json
import os

from PIL import Image

SRC = r'C:\aegis-aa\docs\images\en'
OUT = 'shots'
WIDTH = 1180          # plenty for a 16:9 stage, keeps the payload small
QUALITY = 80

# name -> (file, crop box, what it is for)
SHOTS = {
    'tolls':     ('61-toll-transactions.png',        (324, 12, 1580, 742),  'Toll Transactions, total for the week'),
    'violations':('63-violations.png',               (324, 12, 1580, 694),  'Violations with agency and amount'),
    'charges':   ('62-charges.png',                  (340, 262, 1570, 832), 'Charges, each matched and billed'),
    'map':       ('81-gps-trip-map.png',             (618, 72, 1580, 908),  'GPS map around the crossings'),
    'driver':    ('73-distribution-charges.png',     (378, 618, 1522, 1600),'Charge log: the driver is charged'),
    'income':    ('95-account-statement-report.png', (324, 318, 1582, 1112),'Account statement: owner share income'),
}


def main():
    os.makedirs(OUT, exist_ok=True)
    bank = {}
    for name, (fn, box, note) in SHOTS.items():
        im = Image.open(os.path.join(SRC, fn)).convert('RGB')
        im = im.crop(box)
        if im.width > WIDTH:
            h = round(im.height * WIDTH / im.width)
            im = im.resize((WIDTH, h), Image.LANCZOS)
        path = os.path.join(OUT, name + '.webp')
        im.save(path, 'WEBP', quality=QUALITY, method=6)
        raw = io.open(path, 'rb').read()
        bank[name] = 'data:image/webp;base64,' + base64.b64encode(raw).decode('ascii')
        print('%-11s %-32s %4dx%-4d  %5.0f KB   %s'
              % (name, fn, im.width, im.height, len(raw) / 1024.0, note))

    io.open(os.path.join(OUT, 'shots.json'), 'w', encoding='utf-8').write(json.dumps(bank))
    total = sum(len(v) for v in bank.values())
    print('\ninlined payload: %.2f MB' % (total / 1048576.0))


main()
