# -*- coding: utf-8 -*-
"""English VO read as continuous passages, then cut per line by character timings."""
import base64, io, json, os, ssl, subprocess, sys, urllib.request, urllib.error
import make_vo as m

HERE = os.path.dirname(os.path.abspath(__file__))
TAKES = os.path.join(HERE, 'takes'); os.makedirs(TAKES, exist_ok=True)
BRK = '<break time="0.5s" />'
# (speed, lines) per passage: 1-4 tired, 5-9 brighter.
PARTS_EN = [
    (0.94, ["Two rental fleets. Same street.",
            "Frank's week: a pile of violation notices, all past due,",
            "tolls charged to his account automatically,",
            "and all of it comes out of his pocket."]),
    (1.04, ["Mike's week? A car comes back.",
            "MyEZToll catches every toll and violation in time, and bills the driver, plus a fee.",
            "Mike gets it all back, and a share of that fee. His cost? " + BRK + " Zero.",
            "Frank's asking the same question you are.",
            "MyEZToll. Stop losing. Start earning."]),
]
PARTS_ES = [
    (0.96, ["Dos flotas de alquiler. La misma calle.",
            "La semana de Frank: una montaña de multas, todas vencidas,",
            "peajes cobrados a su cuenta automáticamente,",
            "y todo sale de su bolsillo."]),
    (1.08, ["¿La semana de Mike? Un auto regresa.",
            "MyEZToll detecta a tiempo cada peaje y multa, y se los cobra al conductor, con una comisión.",
            "Mike recupera todo, y parte de esa comisión. ¿Su costo? " + BRK + " Cero.",
            "Frank se pregunta lo mismo que tú.",
            "MyEZToll. Deja de perder. Empieza a ganar."]),
]
# Scenes are 6.04 s; line starts 0.3 s in. Line 9 sits on the 4.5 s end card.
m.MAX[:] = [3.0, 5.5, 5.5, 5.5, 3.4, 5.5, 5.5, 3.2, 4.0]
LANG = sys.argv[1] if len(sys.argv) > 1 else 'en'
import lines as LN
MODEL = m.tts.V3 if LANG in m.tts.V3_ONLY else m.tts.MODEL
if LANG in LN.LINES:
    # v3 ignores SSML breaks; the question mark carries the pause there.
    _L = [l.replace('{B}', '' if MODEL == m.tts.V3 else BRK).replace('  ', ' ') for l in LN.LINES[LANG]]
    PARTS = [(0.96, _L[:4]), ({'zh': 1.15, 'fa': 1.18, 'ur': 1.18}.get(LANG, 1.06), _L[4:])]
    m.MAX[:] = [5.5] * 8 + [4.5]
else:
    PARTS = PARTS_ES if LANG == 'es' else PARTS_EN
VID = m.tts.VOICES[LANG][1]


def speak(text, speed, prev_ids, prev_text):
    body = {'text': text, 'model_id': MODEL,
            'voice_settings': dict(m.tts.SETTINGS, speed=speed)}
    if MODEL == m.tts.V3:
        body['voice_settings']['stability'] = 0.5  # v3 accepts 0 / 0.5 / 1 only
    elif prev_ids: body['previous_request_ids'] = prev_ids
    elif prev_text: body['previous_text'] = prev_text
    req = urllib.request.Request(
        'https://api.elevenlabs.io/v1/text-to-speech/%s/with-timestamps?output_format=mp3_44100_128' % VID,
        data=json.dumps(body).encode(), method='POST')
    req.add_header('xi-api-key', m.tts.key()); req.add_header('Content-Type', 'application/json')
    try:
        r = urllib.request.urlopen(req, context=ssl.create_default_context(), timeout=180)
    except ssl.SSLError:
        r = urllib.request.urlopen(req, context=ssl._create_unverified_context(), timeout=180)
    except urllib.error.HTTPError as e:
        if e.code == 400 and (body.get('previous_request_ids') or 'speed' in body['voice_settings']):
            print('  400: %s -- retrying plain' % e.read().decode('utf-8', 'replace')[:200])
            body.pop('previous_request_ids', None); body['voice_settings'].pop('speed', None)
            req = urllib.request.Request(req.full_url, data=json.dumps(body).encode(), method='POST')
            req.add_header('xi-api-key', m.tts.key()); req.add_header('Content-Type', 'application/json')
            r = urllib.request.urlopen(req, context=ssl._create_unverified_context(), timeout=180)
        else:
            sys.exit('HTTP %s: %s' % (e.code, e.read().decode('utf-8', 'replace')[:300]))
    rid = r.headers.get('request-id')
    d = json.loads(r.read())
    return base64.b64decode(d['audio_base64']), d['alignment'], rid


def cuts(lines, al):
    """Cut points (seconds) between lines: middle of the gap between last char of a line
    and first char of the next, located by matching the alignment's character stream."""
    chars = ''.join(al['characters'])
    st, en = al['character_start_times_seconds'], al['character_end_times_seconds']
    pos, spans = 0, []
    for ln in lines:
        vis = ln.replace(BRK, '').replace('  ', ' ')
        # The break tag stays in the alignment stream, so match text on either side of it.
        first, last = ln.split(BRK)[0].strip()[:6], ln.split(BRK)[-1].strip()[-6:]
        a = chars.find(first, pos); b = chars.find(last, a) + len(last) - 1
        assert a >= 0 and b >= a, (ln, chars)
        spans.append((st[a], en[b])); pos = b + 1
    return spans


def run(part, takes=3):
    speed, lines = PARTS[part]
    prev = None
    ids = [open(os.path.join(TAKES, LANG + '_p0.id')).read().strip()] if part == 1 and os.path.exists(os.path.join(TAKES, LANG + '_p0.id')) else None
    for t in range(takes):
        audio, al, rid = speak(' '.join(lines), speed, ids, None)
        mp3 = os.path.join(TAKES, '%s_p%d_t%d.mp3' % (LANG, part, t))
        io.open(mp3, 'wb').write(audio)
        spans = cuts(lines, al)
        base = 0 if part == 0 else 4
        lens = [e - s for s, e in spans]
        over = sum(max(0, l + 0.12 - m.MAX[base + i]) for i, l in enumerate(lens))
        # A clipped or skipped phrase comes back far too short for its text.
        wide = [len(ln.replace(BRK, '')) * (2.5 if LANG == 'zh' else 1) for ln in lines]
        over += 10 * sum(1 for i, l in enumerate(lens) if l < 0.035 * wide[i])
        print('part %d take %d: %s over=%.2f' % (part, t, ' '.join('%.2f' % l for l in lens), over))
        if prev is None or over < prev[0]:
            prev = (over, mp3, spans, rid)
        if over == 0: break
    over, mp3, spans, rid = prev
    if part == 0 and rid: io.open(os.path.join(TAKES, LANG + '_p0.id'), 'w').write(rid)
    base = 0 if part == 0 else 4
    for i, (s, e) in enumerate(spans):
        out = os.path.join(m.OUT, '%s_%02d.wav' % (LANG, base + i + 1))
        a, b = max(0, s - 0.05), e + 0.06
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', mp3, '-ss', '%.3f' % a, '-to', '%.3f' % b,
                        '-af', 'afade=t=in:d=0.02,areverse,afade=t=in:d=0.03,areverse',
                        '-ar', '44100', '-ac', '1', '-c:a', 'pcm_s16le', out], check=True)
        print('  %s_%02d %.2fs / %.1f' % (LANG, base + i + 1, b - a, m.MAX[base + i]))


if __name__ == '__main__':
    parts = [int(a) for a in sys.argv[2:]] or [0, 1]
    for p in parts: run(p, takes=3 if p else 2)
