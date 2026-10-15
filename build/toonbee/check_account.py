# -*- coding: utf-8 -*-
"""What the ElevenLabs account can do today: plan, credits left, voices on hand.

    python check_account.py

Asked before committing to four more languages, because the answer decides whether
anything has to be bought: the multilingual model speaks all four, but the credits and
the voice list are finite.
"""
import io
import json
import os
import ssl
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tts import key  # same lookup: environment, then HKCU\Environment


def get(path):
    req = urllib.request.Request('https://api.elevenlabs.io' + path)
    req.add_header('xi-api-key', key())
    try:
        with urllib.request.urlopen(req, context=ssl.create_default_context(), timeout=60) as r:
            return json.loads(r.read())
    except ssl.SSLError:
        with urllib.request.urlopen(req, context=ssl._create_unverified_context(), timeout=60) as r:
            return json.loads(r.read())


sub = get('/v1/user/subscription')
print('plan            %s' % sub.get('tier'))
print('characters      %s used of %s  (%s left)'
      % (sub.get('character_count'), sub.get('character_limit'),
         sub.get('character_limit', 0) - sub.get('character_count', 0)))
print('resets          %s' % sub.get('next_character_count_reset_unix'))
print('voice slots     %s used of %s' % (sub.get('voice_slots_used'), sub.get('voice_limit')))
print('can extend      %s' % sub.get('can_extend_character_limit'))

voices = get('/v1/voices').get('voices', [])
print('\n%d voices on the account:' % len(voices))
for v in voices:
    labels = v.get('labels') or {}
    print('  %-22s %-10s %-9s %s'
          % (v.get('name'), labels.get('accent', '-'), labels.get('gender', '-'),
             labels.get('description', '')))
