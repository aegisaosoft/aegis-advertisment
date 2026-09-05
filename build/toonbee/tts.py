# -*- coding: utf-8 -*-
"""Record the ToonBee cut's narration through ElevenLabs, one clip per scene.

    python tts.py es            # record what is missing
    python tts.py es --force    # re-record everything

The voice is the one already bought for this campaign — Terry, Mexican Spanish —
because the audience is United States fleet owners and half of them are Latino. The
same reading is never re-cut by hand: each clip is checked against the length of the
scene it has to sit inside, and a clip that overruns is reported rather than trimmed,
so the line gets rewritten instead of the picture being stretched.
"""
import io
import json
import os
import ssl
import subprocess
import sys
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import script

HERE = os.path.dirname(os.path.abspath(__file__))
MODEL = 'eleven_multilingual_v2'
VOICES = {'es': ('Terry', 'Y4K0Zmn5yVLFKu1SopbT'), 'en': ('Alice', 'Xb7hH8MSUJpSbSDYk0k2')}
SETTINGS = {'stability': 0.45, 'similarity_boost': 0.75, 'style': 0.15, 'use_speaker_boost': True}

# Room the narrator has inside a scene: a beat after the cut before speaking, and a
# beat of air before the next scene arrives.
LEAD = 0.16
TAIL = 0.35


def key():
    value = os.environ.get('ELEVENLABS_API_KEY')
    if value:
        return value.strip()
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment') as k:
            return winreg.QueryValueEx(k, 'ELEVENLABS_API_KEY')[0].strip()
    except Exception:
        sys.exit('ELEVENLABS_API_KEY not set')


def speak(voice_id, text):
    req = urllib.request.Request(
        'https://api.elevenlabs.io/v1/text-to-speech/%s?output_format=mp3_44100_128' % voice_id,
        data=json.dumps({'text': text, 'model_id': MODEL, 'voice_settings': SETTINGS}).encode(),
        method='POST')
    req.add_header('xi-api-key', key())
    req.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(req, context=ssl.create_default_context(), timeout=180) as r:
            return r.read()
    except ssl.SSLError:
        with urllib.request.urlopen(req, context=ssl._create_unverified_context(), timeout=180) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        sys.exit('HTTP %s: %s' % (e.code, e.read().decode('utf-8', 'replace')[:300]))


def duration(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                          '-of', 'csv=p=0', path], capture_output=True, text=True)
    try:
        return float(out.stdout.strip())
    except ValueError:
        return 0.0


def record(voice_id, line, room, takes, path):
    """Keep the reading that fits the scene.

    The model does not give the same length twice — the same sentence came back at
    8.0s and again at 9.2s — so a line that has to sit inside a six-second scene is
    read a few times and the best take is kept: the longest one that still fits, or,
    if none does, the shortest. A take that fits is kept immediately; the rest of the
    budget is not spent for nothing.
    """
    best, best_length = None, None
    for _ in range(max(1, takes)):
        blob = speak(voice_id, line)
        io.open(path, 'wb').write(blob)
        got = duration(path)
        fits = got <= room
        better = (best is None
                  or (fits and (best_length > room or got > best_length))
                  or (not fits and best_length > room and got < best_length))
        if better:
            best, best_length = blob, got
        if fits:
            break
    io.open(path, 'wb').write(best)
    return best_length


lang = next((a for a in sys.argv[1:] if not a.startswith('-')), 'es')
force = '--force' in sys.argv[1:]
takes = next((int(a.split('=')[1]) for a in sys.argv[1:] if a.startswith('--takes=')), 4)
lines = {'es': script.ES, 'en': script.EN}[lang]
name, voice_id = VOICES[lang]
folder = os.path.join(HERE, 'audio', lang)
os.makedirs(folder, exist_ok=True)

print('%s - %s' % (lang.upper(), name))
over = 0
for n, (line, length) in enumerate(zip(lines, script.SCENES), 1):
    path = os.path.join(folder, '%02d.mp3' % n)
    room = length - LEAD - TAIL
    if force or not os.path.exists(path):
        got, kept = record(voice_id, line, room, takes, path), ''
    else:
        got, kept = duration(path), '  (kept)'
        if got > room:
            got, kept = record(voice_id, line, room, takes, path), '  (recut)'
    flag = '  OVER by %.2fs' % (got - room) if got > room else ''
    print('  %2d  %5.2fs / %5.2fs%s%s' % (n, got, room, flag, kept))
    over += got > room
print('%d of %d scenes overrun' % (over, len(lines)))
