"""Generate the narration with ElevenLabs.

    set ELEVENLABS_API_KEY=sk_...
    python tts_generate.py                 # everything
    python tts_generate.py --film B --lang en
    python tts_generate.py --list-voices

One multilingual voice reads all three languages, so the brand sounds like the
same person everywhere. Files already on disk are skipped, so an interrupted
run just continues, and deleting a single mp3 re-records only that line.
"""
import argparse
import io
import json
import os
import sys
import urllib.error
import urllib.request

API = 'https://api.elevenlabs.io/v1'

# Young British female. Override per language if you want different readers.
VOICE = {'en': 'Lily', 'es': 'Lily', 'ru': 'Lily'}

MODEL = 'eleven_multilingual_v2'
FORMAT = 'mp3_44100_128'      # available on every plan; embed_audio.py handles size

SETTINGS = {
    'stability': 0.42,        # a little variation reads younger and less robotic
    'similarity_boost': 0.80,
    'style': 0.28,
    'use_speaker_boost': True,
}


def key():
    k = os.environ.get('ELEVENLABS_API_KEY', '').strip()
    if not k:
        sys.exit('Set ELEVENLABS_API_KEY first (Windows: setx ELEVENLABS_API_KEY "sk_...")')
    return k


def call(path, data=None, method='GET'):
    req = urllib.request.Request(API + path, method=method)
    req.add_header('xi-api-key', key())
    if data is not None:
        req.add_header('Content-Type', 'application/json')
        req.data = json.dumps(data).encode('utf-8')
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', 'replace')[:400]
        raise SystemExit('ElevenLabs %s on %s\n%s' % (e.code, path, body))


def voices():
    return json.loads(call('/voices').decode('utf-8')).get('voices', [])


def resolve(name, all_voices):
    for v in all_voices:
        if v.get('name', '').lower() == name.lower():
            return v['voice_id']
    names = ', '.join(sorted(v.get('name', '?') for v in all_voices))
    raise SystemExit('Voice "%s" not in your account.\nAvailable: %s' % (name, names))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--film', choices=['A', 'B'])
    ap.add_argument('--lang', choices=['en', 'es', 'ru'])
    ap.add_argument('--list-voices', action='store_true')
    a = ap.parse_args()

    if a.list_voices:
        for v in sorted(voices(), key=lambda v: v.get('name', '')):
            lbl = v.get('labels', {}) or {}
            print('%-22s %s  %s' % (v.get('name'), v.get('voice_id'),
                                    ' '.join('%s=%s' % kv for kv in lbl.items())))
        return

    bank = json.load(io.open('narration/script.json', encoding='utf-8'))
    all_voices = voices()
    vid = {lg: resolve(nm, all_voices) for lg, nm in VOICE.items()}
    print('Voices: ' + ', '.join('%s=%s' % (lg, VOICE[lg]) for lg in VOICE))

    made = skipped = 0
    chars = 0
    for film in sorted(bank):
        if a.film and film != a.film:
            continue
        for lg in ('en', 'es', 'ru'):
            if a.lang and lg != a.lang:
                continue
            lines = bank[film]['lines'][lg]
            out = os.path.join('narration', 'audio', film, lg)
            os.makedirs(out, exist_ok=True)
            for lid in sorted(lines, key=lambda k: [int(x) for x in k.split('-')]):
                path = os.path.join(out, lid + '.mp3')
                if os.path.exists(path) and os.path.getsize(path) > 512:
                    skipped += 1
                    continue
                text = lines[lid]['text']
                audio = call('/text-to-speech/%s?output_format=%s' % (vid[lg], FORMAT),
                             {'text': text, 'model_id': MODEL, 'voice_settings': SETTINGS},
                             method='POST')
                io.open(path, 'wb').write(audio)
                made += 1
                chars += len(text)
                print('  %s/%s/%-6s %6d bytes  %s' % (film, lg, lid, len(audio), text[:52]))

    print('\n%d clips written, %d already present, %d characters billed.' % (made, skipped, chars))
    print('Next: python embed_audio.py')


main()
