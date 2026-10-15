# -*- coding: utf-8 -*-
"""Which of the site's languages ElevenLabs can actually narrate, and with which model.

    python check_models.py

Asked before promising the remaining nine: the multilingual model the film uses covers
twenty-nine languages, and several of the site's are not among them. The answer decides
whether a language is a recording or a subtitle track.
"""
import json
import os
import ssl
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tts import key

# What the site speaks, minus the six the film is already narrated in.
WANTED = {
    'uk': 'Ukrainian', 'tr': 'Turkish', 'uz': 'Uzbek', 'hy': 'Armenian', 'ka': 'Georgian',
    'fa': 'Persian', 'ur': 'Urdu', 'zh': 'Chinese',
}

req = urllib.request.Request('https://api.elevenlabs.io/v1/models')
req.add_header('xi-api-key', key())
try:
    with urllib.request.urlopen(req, context=ssl.create_default_context(), timeout=60) as r:
        models = json.loads(r.read())
except ssl.SSLError:
    with urllib.request.urlopen(req, context=ssl._create_unverified_context(), timeout=60) as r:
        models = json.loads(r.read())

for code, name in sorted(WANTED.items(), key=lambda kv: kv[1]):
    can = []
    for m in models:
        langs = {l.get('language_id') for l in (m.get('languages') or [])}
        if code in langs:
            can.append(m.get('model_id'))
    print('%-10s %s' % (name, ', '.join(can) if can else 'NO MODEL SPEAKS IT'))

print()
for m in models:
    langs = m.get('languages') or []
    if langs:
        print('%-28s %d languages' % (m.get('model_id'), len(langs)))
