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

# The multilingual model speaks twenty-nine languages and is the better reader of all
# of them, so it stays the default. Armenian, Georgian, Persian and Urdu are not among
# the twenty-nine — only v3 speaks them — and asking the wrong model does not fail, it
# reads the letters as if they were something else.
MODEL = 'eleven_multilingual_v2'
V3 = 'eleven_v3'
V3_ONLY = ('hy', 'ka', 'fa', 'ur')
# Four more narrators than the film started with, all native speakers taken from the
# shared library — a library voice costs one of thirty free slots, not money. Chosen
# female throughout because both cuts that already exist are read by a woman.
VOICES = {
    'en': ('Alice', 'Xb7hH8MSUJpSbSDYk0k2'),
    'es': ('Terry', 'Y4K0Zmn5yVLFKu1SopbT'),
    'ru': ('Victoria', 'Phc1KhVrCoW3CD0K7bUS'),
    'de': ('Sunny Sonja', 'orCAaN7voZRSXS1JoEX2'),
    'fr': ('Nathalie', 'rS7c1woNY04WT3UAS83Y'),
    'pt': ('Camilla', 'YklVF5l1Q8os8glyd5SM'),
    'uk': ('Kateryna', 'X1WtgMmQUBwtiAPn4j1P'),
    'tr': ('Gamze Baykan', '4XumGDZjxmgp3U7xXaul'),
    'zh': ('Susan', '0H4ruoQ81Ei2FCwjW5j1'),
    # The last four have no native narrator anywhere in the shared library: the
    # language facet returns nothing for them and a search by name finds only English
    # voices with an accent. So each was chosen by audition instead — the same line
    # read by eight candidates, put back through Scribe with the language declared, and
    # scored on how many of the script's own words survived the round trip.
    #
    # Persian and Urdu went to the two voices actually recorded by speakers of those
    # languages; they scored level with the best and are the only ones that carry the
    # right vowels. Armenian and Georgian have no such voice at all, so they went to
    # the two that scored highest and read fast enough to fit the scenes.
    'hy': ('Victoria', 'Phc1KhVrCoW3CD0K7bUS'),
    'ka': ('Kateryna', 'X1WtgMmQUBwtiAPn4j1P'),
    'fa': ('Noushin', 'NZiuR1C6kVMSWHG27sIM'),
    'ur': ('Reva', 'UT6USLtoAlXHj5k4sOLY'),
}
SETTINGS = {'stability': 0.45, 'similarity_boost': 0.75, 'style': 0.15, 'use_speaker_boost': True}

# Room the narrator has inside a scene: a beat after the cut before speaking, and a
# beat of air before the next scene arrives.
# Both live in script.py, which is what the lines were written against.
LEAD = script.LEAD
TAIL = script.TAIL


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


def speak(voice_id, text, model=MODEL):
    req = urllib.request.Request(
        'https://api.elevenlabs.io/v1/text-to-speech/%s?output_format=mp3_44100_128' % voice_id,
        data=json.dumps({'text': text, 'model_id': model, 'voice_settings': SETTINGS}).encode(),
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


def record(voice_id, line, room, takes, path, model=MODEL):
    """Keep the reading that fits the scene.

    The model does not give the same length twice — the same sentence came back at
    8.0s and again at 9.2s — so a line that has to sit inside a six-second scene is
    read a few times and the best take is kept: the longest one that still fits, or,
    if none does, the shortest. A take that fits is kept immediately; the rest of the
    budget is not spent for nothing.
    """
    best, best_length = None, None
    for _ in range(max(1, takes)):
        blob = speak(voice_id, line, model)
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


# Recording is what this file does when run, not when imported: `key` and `speak` are
# borrowed by the account and voice-library helpers, and importing must not spend credits.
if __name__ == '__main__':
    lang = next((a for a in sys.argv[1:] if not a.startswith('-')), 'es')
    force = '--force' in sys.argv[1:]
    takes = next((int(a.split('=')[1]) for a in sys.argv[1:] if a.startswith('--takes=')), 4)
    if lang in script.SUBTITLED:
        sys.exit('%s is a subtitle track over the %s narration, not a recording'
                 % (lang, script.SUBTITLED[lang]))
    lines = script.LANGS[lang]
    name, voice_id = VOICES[lang]
    model = V3 if lang in V3_ONLY else MODEL
    folder = os.path.join(HERE, 'audio', lang)
    os.makedirs(folder, exist_ok=True)

    print('%s - %s (%s)' % (lang.upper(), name, model))
    over = 0
    for n, (line, length) in enumerate(zip(lines, script.SCENES), 1):
        path = os.path.join(folder, '%02d.mp3' % n)
        room = length - LEAD - TAIL
        if force or not os.path.exists(path):
            got, kept = record(voice_id, line, room, takes, path, model), ''
        else:
            got, kept = duration(path), '  (kept)'
            if got > room:
                got, kept = record(voice_id, line, room, takes, path, model), '  (recut)'
        flag = '  OVER by %.2fs' % (got - room) if got > room else ''
        print('  %2d  %5.2fs / %5.2fs%s%s' % (n, got, room, flag, kept))
        over += got > room
    print('%d of %d scenes overrun' % (over, len(lines)))
