"""Spanish-language crops of the owner-web screens.

The Spanish capture run left the plate column readable on the Infracciones
screen (the English one is redacted), so those cells are blurred here before
anything is cropped or published.
"""
import base64
import io
import json
import os

from PIL import Image, ImageFilter

SRC = r'C:\aegis-aa\docs\images\es'
OUT = 'shots_es'
WIDTH = 1180
QUALITY = 80

# name -> (file, crop box, [redact boxes on the ORIGINAL image], note)
SHOTS = {
    'tolls':     ('61-toll-transactions.png',        (324, 12, 1580, 800),  [],
                  'Transacciones de peaje, total de la semana'),
    'violations':('63-violations.png',               (324, 12, 1580, 500),
                  [(566, 310, 700, 440)],
                  'Infracciones (plate column redacted here)'),
    'charges':   ('62-charges.png',                  (340, 258, 1570, 836),
                  [(858, 380, 985, 790)],
                  'Cargos, cada peaje emparejado (plate column redacted here)'),
    'map':       ('81-gps-trip-map.png',             (618, 72, 1580, 908),  [],
                  'Mapa GPS de los corredores de peaje'),
    'driver':    ('73-distribution-charges.png',     (378, 618, 1522, 1600),[],
                  'Registro de cargos: se cobra al conductor'),
    'income':    ('95-account-statement-report.png', (324, 318, 1582, 1112),[],
                  'Estado de cuenta: ingresos del propietario'),
}


def main():
    os.makedirs(OUT, exist_ok=True)
    bank = {}
    for name, (fn, box, redact, note) in SHOTS.items():
        im = Image.open(os.path.join(SRC, fn)).convert('RGB')

        for r in redact:
            region = im.crop(r).filter(ImageFilter.GaussianBlur(9))
            im.paste(region, r)

        im = im.crop(box)
        if im.width > WIDTH:
            h = round(im.height * WIDTH / im.width)
            im = im.resize((WIDTH, h), Image.LANCZOS)
        path = os.path.join(OUT, name + '.webp')
        im.save(path, 'WEBP', quality=QUALITY, method=6)
        raw = io.open(path, 'rb').read()
        bank[name] = 'data:image/webp;base64,' + base64.b64encode(raw).decode('ascii')
        print('%-11s %-32s %4dx%-4d %5.0f KB  %s%s'
              % (name, fn, im.width, im.height, len(raw) / 1024.0,
                 'REDACTED ' if redact else '', note))

    io.open(os.path.join(OUT, 'shots.json'), 'w', encoding='utf-8').write(json.dumps(bank))
    print('\ninlined payload: %.2f MB' % (sum(len(v) for v in bank.values()) / 1048576.0))


main()
