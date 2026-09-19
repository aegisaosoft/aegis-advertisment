# -*- coding: utf-8 -*-
"""Record the narration for the tutorial series, one clip per line, through ElevenLabs.

    python tts.py                 # record whatever is missing, both languages
    python tts.py es              # one language
    python tts.py 3 4 --force     # re-record episodes 3 and 4 from scratch

Writes `audio/<lang>/ep<NN>/<i>.mp3`. `build.py` measures those clips and lays the
picture out around them, so a re-recorded line moves the picture with it instead of
leaving it behind.

The same two voices carry the advertising films, so the product sounds like one
company: Alice for English, Terry for Spanish. Alice is listed on the account as a
"clear, engaging educator", which is the job.

The key comes from the environment, then HKCU\\Environment (setx writes there and a
process already running never sees it), then `C:\\aegis-aa\\_elevenlabs.key.txt`. It is
never printed and goes nowhere but api.elevenlabs.io.
"""
import io
import json
import os
import ssl
import sys
import urllib.error
import urllib.request

import episodes

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = 'https://api.elevenlabs.io'
MODEL = 'eleven_multilingual_v2'

VOICES = {
    'en': ('Alice', 'Xb7hH8MSUJpSbSDYk0k2'),
    'es': ('Terry', 'Y4K0Zmn5yVLFKu1SopbT'),
}

# Steadier than the advertising read: this voice is explaining a procedure, not selling.
SETTINGS = {'stability': 0.55, 'similarity_boost': 0.80, 'style': 0.05, 'use_speaker_boost': True}


def key():
    value = os.environ.get('ELEVENLABS_API_KEY')
    if value:
        return value.strip()
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment') as k:
            return winreg.QueryValueEx(k, 'ELEVENLABS_API_KEY')[0].strip()
    except Exception:
        pass
    path = os.path.join('C:\\aegis-aa', '_elevenlabs.key.txt')
    if os.path.exists(path):
        return io.open(path, encoding='utf-8').read().strip()
    sys.exit('ELEVENLABS_API_KEY not set and no _elevenlabs.key.txt')


def speak(voice_id, text):
    req = urllib.request.Request(
        '%s/v1/text-to-speech/%s?output_format=mp3_44100_128' % (BASE, voice_id),
        data=json.dumps({'text': text, 'model_id': MODEL, 'voice_settings': SETTINGS}).encode(),
        method='POST',
    )
    req.add_header('xi-api-key', key())
    req.add_header('Content-Type', 'application/json')
    for context in (ssl.create_default_context(), ssl._create_unverified_context()):
        try:
            with urllib.request.urlopen(req, context=context, timeout=180) as r:
                return r.read()
        except ssl.SSLError:
            continue
        except urllib.error.HTTPError as e:
            sys.exit('HTTP %s: %s' % (e.code, e.read().decode('utf-8', 'replace')[:400]))
    sys.exit('TLS handshake failed both ways')


def clip_path(lang, ep, i):
    return os.path.join(HERE, 'audio', lang, 'ep%02d' % ep.num, '%02d.mp3' % i)


def main(argv):
    force = '--force' in argv
    argv = [a for a in argv if a != '--force']
    langs = [a for a in argv if a in VOICES] or ['en', 'es']
    nums = [int(a) for a in argv if a.isdigit()]
    series = [e for e in episodes.SERIES if not nums or e.num in nums]

    spent = 0
    for lang in langs:
        name, voice_id = VOICES[lang]
        for ep in series:
            out_dir = os.path.dirname(clip_path(lang, ep, 0))
            os.makedirs(out_dir, exist_ok=True)
            print('ep%02d %s  %s  %s' % (ep.num, ep.slug, lang, name))
            for i, beat in enumerate(ep.beats):
                path = clip_path(lang, ep, i)
                text = beat.say[lang]
                if os.path.exists(path) and not force:
                    print('    %02d  have' % i)
                    continue
                audio = speak(voice_id, text)
                io.open(path, 'wb').write(audio)
                spent += len(text)
                print('    %02d  %4d chars  %6.1f KB' % (i, len(text), len(audio) / 1024.0))
    if spent:
        print('\n%d characters spent this run' % spent)


if __name__ == '__main__':
    main(sys.argv[1:])
