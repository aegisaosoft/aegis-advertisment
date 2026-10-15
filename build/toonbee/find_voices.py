# -*- coding: utf-8 -*-
"""Shortlist native voices in the shared library for the languages we still need.

    python find_voices.py ru pt fr de

Adding a library voice costs a slot, not money, and the account has thirty free. What
matters is that the voice is a native speaker of the language it will read: the
multilingual model will happily read Russian in an English voice, and it sounds like it.
"""
import json
import os
import ssl
import sys
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tts import key

# The campaign is narrated by a woman in both existing cuts; keep that across languages.
WANT = {'gender': 'female', 'page_size': '30'}


def shared(language):
    query = dict(WANT, language=language)
    url = 'https://api.elevenlabs.io/v1/shared-voices?' + urllib.parse.urlencode(query)
    req = urllib.request.Request(url)
    req.add_header('xi-api-key', key())
    try:
        with urllib.request.urlopen(req, context=ssl.create_default_context(), timeout=60) as r:
            return json.loads(r.read())
    except ssl.SSLError:
        with urllib.request.urlopen(req, context=ssl._create_unverified_context(), timeout=60) as r:
            return json.loads(r.read())


for lang in sys.argv[1:] or ['ru', 'pt', 'fr', 'de']:
    data = shared(lang)
    voices = data.get('voices', [])
    print('\n=== %s: %d shared voices ===' % (lang.upper(), len(voices)))
    for v in voices[:10]:
        print('  %-28s %-16s %-12s uses=%-8s %s'
              % (v.get('name', '')[:28],
                 (v.get('accent') or '-')[:16],
                 (v.get('age') or '-')[:12],
                 v.get('cloned_by_count', 0),
                 (v.get('description') or '')[:46]))
        print('      id %s' % v.get('voice_id'))
