# -*- coding: utf-8 -*-
"""Pull the frames where a person could be named, as one contact sheet per language.

    python pii_check.py            # both languages
    python pii_check.py en

Every screen in the series that can carry a customer's name, phone, email or licence
plate is listed below with the region to look at. For each, this finds the second the
rendered episode is showing that screen, cuts the frame out of the mp4, crops the
region and stacks the crops into `stills/pii-<lang>.png`.

**Look at the sheet. Do not measure it.** Edge energy over a table reads the same for a
blurred name column beside sharp timestamps as it does for a legible one — that metric
has now twice come within one step of shipping real customers' names, once by claiming a
leak that was not there and once by missing one that was. A crop and a pair of eyes
settles in five seconds what the number argues about.
"""
import io
import json
import os
import re
import subprocess
import sys

from PIL import Image, ImageDraw

import build
import episodes

# shot -> (label, crop as fractions of the frame: x0, y0, x1, y1)
# The crop is in FRAME coordinates, not source-screenshot coordinates, because the
# camera has already placed and zoomed the screenshot by the time it is a frame.
WATCH = {
    '54-pending-drivers':      ('ep18 Drivers awaiting review - NAME',    (.20, .30, .62, .86)),
    '90-drivers':              ('ep17 Drivers - NOMBRE / APELLIDO',       (.18, .35, .70, .90)),
    '93-messages':             ('ep19 Email - senders and subjects',      (.20, .25, .55, .85)),
    '94-sms-log':              ('ep19 SMS log - PHONE / RENTER',          (.30, .30, .99, .85)),
    '50-bookings':             ('ep08 Bookings - renter column',          (.18, .30, .75, .88)),
    '52-booking-row-menu':     ('ep08 Row menu header - renter name',     (.30, .30, .70, .60)),
    '56-pending-history':      ('ep18 History - reservation rows',        (.18, .30, .90, .85)),
    '64-failed-payments':      ('ep12 Failed payments - driver rows',     (.18, .30, .90, .85)),
    '65-successful-payments':  ('ep12 Successful payments - driver rows', (.18, .30, .90, .85)),
    '66-disputes':             ('ep12 Disputes - table',                  (.18, .40, .90, .90)),
    '62-charges':              ('ep10 Charges - table',                   (.18, .30, .90, .85)),
    '99-partners':             ('ep21 Partners - owner list',             (.18, .20, .90, .60)),
    '38-settings-turo-agents': ('ep21 Turo agents - host accounts',       (.18, .35, .90, .90)),
    '19-rates':                ('ep07 Rates - group rows',                (.18, .30, .90, .85)),
    '80-gps-fleet-map':        ('ep15 Fleet map - pins',                  (.20, .25, .90, .90)),
    '25-toll-account-vehicles': ('ep06 Toll account - vehicle rows',      (.18, .35, .95, .90)),
    '61-toll-transactions':    ('ep09 Toll transactions - PLATE / TRANSPONDER', (.18, .30, .95, .85)),
    '67-stripe-dashboard':     ('ep13 Stripe - CUSTOMER column',          (.18, .25, .95, .85)),
    '63-violations':           ('ep11 Violations - PLATE / ADDRESS',      (.18, .30, .95, .85)),
    '26-toll-account-transponders': ('ep06 Transponder inventory',        (.18, .30, .95, .85)),
    '69-invoices-to-pay':      ('ep13 Invoices to pay - rows',            (.18, .20, .95, .70)),
    '72-distribution-payouts': ('ep14 Payout history - rows',             (.18, .40, .95, .90)),
}

HERE = os.path.dirname(os.path.abspath(__file__))
WIDE = 900


def moment(ep, lang, shot):
    """A second at which that episode is showing that screen, past the camera move."""
    path = os.path.join(HERE, 'ep%02d.%s.html' % (ep.num, lang))
    if not os.path.exists(path):
        return None
    html = io.open(path, encoding='utf-8').read()
    film = json.loads(re.search(r'var FILM = (\{.*?\});\n', html, re.S).group(1))
    for b in film['beats']:
        if b['shot'] == shot:
            return b['t'] + 1.6
    return None


def video(ep, lang):
    for root in ('mp4', os.path.join('mp4', 'small')):
        for f in os.listdir(os.path.join(HERE, root)) if os.path.isdir(os.path.join(HERE, root)) else []:
            if f.startswith('myeztoll-tutorial-%02d-' % ep.num) and f.endswith('-%s.mp4' % lang):
                return os.path.join(HERE, root, f)
    return None


def main(argv):
    langs = [a for a in argv if a in ('en', 'es')] or ['en', 'es']
    os.makedirs(os.path.join(HERE, 'stills'), exist_ok=True)

    for lang in langs:
        rows, missing = [], []
        for ep in episodes.SERIES:
            for shot in dict.fromkeys(b.shot for b in ep.beats):
                if shot not in WATCH:
                    continue
                label, box = WATCH[shot]
                mp4 = video(ep, lang)
                t = moment(ep, lang, shot)
                if not mp4 or t is None:
                    missing.append('%s %s' % (shot, lang))
                    continue
                tmp = os.path.join(HERE, 'stills', '_pii_tmp.png')
                r = subprocess.run([build.FFMPEG, '-y', '-v', 'error', '-ss', '%.2f' % t,
                                    '-i', mp4, '-frames:v', '1', tmp], capture_output=True)
                if r.returncode != 0:
                    missing.append('%s %s (unreadable, still rendering?)' % (shot, lang))
                    continue
                im = Image.open(tmp)
                w, h = im.size
                c = im.crop((int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h)))
                c = c.resize((WIDE, max(1, int(c.height * WIDE / c.width))))
                rows.append(('ep%02d  %s' % (ep.num, label), c))

        if not rows:
            print('%s: nothing to check yet (%s)' % (lang, ', '.join(missing) or 'no videos'))
            continue
        bar = 26
        sheet = Image.new('RGB', (WIDE, sum(r[1].height + bar for r in rows)), (18, 16, 34))
        d = ImageDraw.Draw(sheet)
        y = 0
        for label, c in rows:
            d.text((8, y + 6), label, fill=(255, 190, 110))
            y += bar
            sheet.paste(c, (0, y))
            y += c.height
        out = os.path.join(HERE, 'stills', 'pii-%s.png' % lang)
        sheet.save(out)
        print('%s: %d crops -> %s%s' % (lang, len(rows), out,
                                        ('  (skipped: %s)' % '; '.join(missing)) if missing else ''))


if __name__ == '__main__':
    main(sys.argv[1:])
