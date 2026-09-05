# -*- coding: utf-8 -*-
"""Record the 55-second cut's narration through ElevenLabs, one clip per line.

    python tts.py             # record what is missing
    python tts.py --force     # re-record everything
    python tts.py en          # one language

Reads `narration.<lang>.md` — the same file a human voice artist would be handed —
and writes `audio/<lang>/<scene>-<cue>.mp3`, the naming the film's player already
expects. Prints each clip against the budget written in the script, because a line
that overruns pushes its whole scene: the film is retimed to the recording, not the
other way round.

The API key comes from the environment, falling back to HKCU\\Environment (setx
writes there, and a process that was already running never sees it). It is never
printed and goes nowhere but api.elevenlabs.io.
"""
import io
import json
import os
import re
import ssl
import subprocess
import sys
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = 'https://api.elevenlabs.io'
MODEL = 'eleven_multilingual_v2'

# Chosen by ear from the audition in `audition/`, one line read by every candidate.
# British for English and Mexican for Spanish are deliberate: the fleet owners this
# film is aimed at are in the United States, and half of them are Latino.
VOICES = {
    'en': ('Alice', 'Xb7hH8MSUJpSbSDYk0k2'),
    'es': ('Terry', 'Y4K0Zmn5yVLFKu1SopbT'),
}

# Steady enough to be trusted with somebody's money, loose enough not to sound synthetic.
SETTINGS = {'stability': 0.45, 'similarity_boost': 0.75, 'style': 0.15, 'use_speaker_boost': True}


def key():
    value = os.environ.get('ELEVENLABS_API_KEY')
    if value:
        return value.strip()
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment') as k:
            return winreg.QueryValueEx(k, 'ELEVENLABS_API_KEY')[0].strip()
    except Exception:
        sys.exit('ELEVENLABS_API_KEY not set — run: setx ELEVENLABS_API_KEY "sk_..."')


def speak(voice_id, text):
    req = urllib.request.Request(
        '%s/v1/text-to-speech/%s?output_format=mp3_44100_128' % (BASE, voice_id),
        data=json.dumps({'text': text, 'model_id': MODEL, 'voice_settings': SETTINGS}).encode(),
        method='POST',
    )
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


def cues(lang):
    """(id, budget_seconds, text) for every line in that language's script."""
    path = os.path.join(HERE, 'narration.%s.md' % lang)
    text = io.open(path, encoding='utf-8').read()
    found = re.findall(r'^\*\*(\d+-\d+)\*\*\s*_\(max ([\d.]+)s\)_\s*\n\s*\n>\s*(.+?)\s*$',
                       text, re.M)
    if not found:
        sys.exit('%s: no cues parsed — has the script format changed?' % path)
    return [(cid, float(budget), line) for cid, budget, line in found]


def duration(path):
    out = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path],
        capture_output=True, text=True)
    try:
        return float(out.stdout.strip())
    except ValueError:
        return 0.0


force = '--force' in sys.argv[1:]
langs = [a for a in sys.argv[1:] if not a.startswith('-')] or list(VOICES)

for lang in langs:
    name, voice_id = VOICES[lang]
    folder = os.path.join(HERE, 'audio', lang)
    os.makedirs(folder, exist_ok=True)
    print('\n%s — %s' % (lang.upper(), name))

    spoken = over = 0.0
    for cid, budget, line in cues(lang):
        path = os.path.join(folder, '%s.mp3' % cid)
        fresh = force or not os.path.exists(path)
        if fresh:
            io.open(path, 'wb').write(speak(voice_id, line))
        got = duration(path)
        spoken += got
        flag = ''
        if got > budget:
            over += got - budget
            flag = '  OVER by %.1fs' % (got - budget)
        print('  %-5s %4.1fs / %4.1fs%s%s  %s' % (cid, got, budget, flag, '' if fresh else '  (kept)', line[:52]))

    # Scenes are stretched to the voice later, so this is the film's real length:
    # every line, plus a breath between them and a beat at each scene edge.
    n = len(cues(lang))
    runtime = spoken + 0.55 * (n - 4) + 1.3 * 4
    print('  spoken %.1fs over %d lines → film runs about %d:%02d%s'
          % (spoken, n, int(runtime // 60), int(runtime % 60),
             ('  (%.1fs past the written budgets)' % over) if over else ''))
