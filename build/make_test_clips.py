"""Build silent but structurally valid MP3s so the embed/retime path can be
tested before a penny is spent on real narration. Not for shipping."""
import io
import json
import os

HDR = bytes([0xFF, 0xFB, 0x90, 0xC0])     # MPEG1 Layer III, 128 kbps, 44.1 kHz, mono
FRAME = 417
SEC_PER_FRAME = 1152.0 / 44100.0


def silent_mp3(seconds):
    frames = max(1, int(round(seconds / SEC_PER_FRAME)))
    return (HDR + b'\x00' * (FRAME - 4)) * frames


def main():
    bank = json.load(io.open('narration/script.json', encoding='utf-8'))
    made = 0
    for film in bank:
        for lg, lines in bank[film]['lines'].items():
            d = os.path.join('narration', 'audio', film, lg)
            os.makedirs(d, exist_ok=True)
            for lid, meta in lines.items():
                # deliberately off the planned budget, to prove retiming moves things
                secs = max(1.5, len(meta['text'].split()) / 2.35)
                io.open(os.path.join(d, lid + '.mp3'), 'wb').write(silent_mp3(secs))
                made += 1
    print('%d placeholder clips written' % made)


main()
