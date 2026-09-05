# -*- coding: utf-8 -*-
r"""Transcribe the ToonBee export through ElevenLabs Scribe for word-level timings.

    python stt.py <audio.mp3> <out.json> [language]

The captions must carry the script's words, not a transcriber's guesses — Scribe is
used only for *when* each word is said, never for what it says. align.py maps the
real script onto these timings, so a misheard word costs nothing.

The key comes from the environment, falling back to HKCU\Environment the way tts.py
does; it is never printed.
"""
import io
import json
import os
import ssl
import sys
import urllib.request
import uuid


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


def form(fields, filename, blob):
    line = '--%s' % uuid.uuid4().hex
    out = io.BytesIO()
    for name, value in fields.items():
        out.write(('--%s\r\nContent-Disposition: form-data; name="%s"\r\n\r\n%s\r\n'
                   % (line, name, value)).encode())
    out.write(('--%s\r\nContent-Disposition: form-data; name="file"; filename="%s"\r\n'
               'Content-Type: audio/mpeg\r\n\r\n' % (line, filename)).encode())
    out.write(blob)
    out.write(('\r\n--%s--\r\n' % line).encode())
    return 'multipart/form-data; boundary=%s' % line, out.getvalue()


src, dst = sys.argv[1], sys.argv[2]
fields = {'model_id': 'scribe_v1', 'timestamps_granularity': 'word'}
if len(sys.argv) > 3:
    fields['language_code'] = sys.argv[3]

ctype, body = form(fields, os.path.basename(src), io.open(src, 'rb').read())
req = urllib.request.Request('https://api.elevenlabs.io/v1/speech-to-text',
                             data=body, method='POST')
req.add_header('xi-api-key', key())
req.add_header('Content-Type', ctype)
try:
    with urllib.request.urlopen(req, context=ssl.create_default_context(), timeout=600) as r:
        payload = r.read()
except urllib.error.HTTPError as e:
    sys.exit('HTTP %s: %s' % (e.code, e.read().decode('utf-8', 'replace')[:400]))

data = json.loads(payload)
io.open(dst, 'w', encoding='utf-8').write(json.dumps(data, ensure_ascii=False, indent=1))
words = [w for w in data.get('words', []) if w.get('type') == 'word']
print('%d words, %.2fs .. %.2fs' % (len(words), words[0]['start'], words[-1]['end']))
print(' '.join(w['text'] for w in words[:30]) + ' ...')
