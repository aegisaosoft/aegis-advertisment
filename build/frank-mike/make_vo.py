# -*- coding: utf-8 -*-
"""Frank vs Mike: shared ElevenLabs plumbing (voices, model and settings of the ToonBee cut).

The first pass recorded each line on its own; flow.py replaced that with continuous
readings. What flow.py still borrows from here is `speak`-free: tts, MAX, OUT and trim.
"""
import io, json, os, ssl, subprocess, sys, urllib.request, urllib.error

sys.path.insert(0, r'C:\aegis-aa\aegis-advertisment\build\toonbee')
import tts  # key(), VOICES, SETTINGS, MODEL

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'audio')
RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'takes')
os.makedirs(OUT, exist_ok=True); os.makedirs(RAW, exist_ok=True)

MAX = [3.0, 4.0, 3.6, 3.4, 3.4, 4.6, 3.2, 3.2, 4.0]
# Tone only via speed: 2-4 tired and slower, 5+ brighter.
SPEED = [1.0, 0.92, 0.92, 0.92, 1.06, 1.08, 1.04, 1.05, 1.04]
BRK = '<break time="0.45s" />'
EN = ["Two rental fleets. Same street.",
      "Frank's week: a pile of toll notices...",
      "...hours chasing renters...",
      "...and he still pays the late fees.",
      "Mike's week? A car comes back.",
      "MyEZToll matches every toll, bills the driver, and pays Mike a share.",
      "His cost? " + BRK + " Zero.",
      "Frank's asking the same question you are.",
      "MyEZToll. Stop losing. Start earning."]
ES = ["Dos flotas de alquiler. La misma calle.",
      "La semana de Frank: una montaña de avisos de peaje...",
      "...horas persiguiendo a los clientes...",
      "...y aun así él paga los recargos.",
      "¿La semana de Mike? Un auto regresa.",
      "MyEZToll identifica cada peaje, le cobra al conductor y le paga a Mike una parte.",
      "¿Cuánto le cuesta? " + BRK + " Nada.",
      "Frank se pregunta lo mismo que tú.",
      "MyEZToll. Deja de perder. Empieza a ganar."]


def speak(voice_id, text, speed, prev, nxt):
    vs = dict(tts.SETTINGS, speed=speed)
    body = {'text': text, 'model_id': tts.MODEL, 'voice_settings': vs}
    if prev: body['previous_text'] = prev
    if nxt: body['next_text'] = nxt
    req = urllib.request.Request(
        'https://api.elevenlabs.io/v1/text-to-speech/%s?output_format=mp3_44100_128' % voice_id,
        data=json.dumps(body).encode(), method='POST')
    req.add_header('xi-api-key', tts.key()); req.add_header('Content-Type', 'application/json')
    try:
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(req, context=ctx, timeout=180) as r: return r.read()
    except ssl.SSLError:
        with urllib.request.urlopen(req, context=ssl._create_unverified_context(), timeout=180) as r: return r.read()
    except urllib.error.HTTPError as e:
        sys.exit('HTTP %s: %s' % (e.code, e.read().decode('utf-8', 'replace')[:300]))


def trim(src, dst):
    # Strip leading/trailing silence, then pad 50 ms each side (< 0.1 s requirement).
    sr = 'silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.02'
    af = '%s,areverse,%s,areverse,adelay=50|50,apad=pad_dur=0.05' % (sr, sr)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', src, '-af', af,
                    '-ar', '44100', '-ac', '1', '-c:a', 'pcm_s16le', dst], check=True)
    return tts.duration(dst)


def run(lang, lines, takes=5):
    name, vid = tts.VOICES[lang]
    print('%s - %s %s (%s)' % (lang.upper(), name, vid, tts.MODEL))
    for i, text in enumerate(lines):
        prev = lines[i - 1].replace(BRK, '') if i else None
        nxt = lines[i + 1].replace(BRK, '') if i + 1 < len(lines) else None
        dst = os.path.join(OUT, '%s_%02d.wav' % (lang, i + 1))
        best = None
        for t in range(takes):
            raw = os.path.join(RAW, '%s_%02d_t%d.mp3' % (lang, i + 1, t))
            io.open(raw, 'wb').write(speak(vid, text, SPEED[i], prev, nxt))
            tmp = dst + '.t%d.wav' % t
            d = trim(raw, tmp)
            if best is None or (d <= MAX[i] and (best[0] > MAX[i] or d > best[0])) or \
               (d > MAX[i] and best[0] > MAX[i] and d < best[0]):
                best = (d, tmp)
            if d <= MAX[i]:
                break
        os.replace(best[1], dst)
        for f in os.listdir(OUT):
            if f.startswith(os.path.basename(dst) + '.t'): os.remove(os.path.join(OUT, f))
        flag = '' if best[0] <= MAX[i] else '  OVER by %.2fs' % (best[0] - MAX[i])
        print('  %02d  %.2fs / %.1fs%s' % (i + 1, best[0], MAX[i], flag))


if __name__ == '__main__':
    for lang in (sys.argv[1:] or ['en', 'es']):
        run(lang, EN if lang == 'en' else ES)
