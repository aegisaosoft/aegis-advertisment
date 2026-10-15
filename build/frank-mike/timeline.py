# -*- coding: utf-8 -*-
"""Where each line of narration goes, and how long each shot runs around it.

The narration is continuous: line n+1 follows line n after a breath, not after the end
of a shot. The picture is cut to the voice instead — shot n lasts from just before its
line to just before the next one, so every shot carries its own line and no shot runs
on in silence. A line longer than its shot holds the shot's last frame.

    python timeline.py <lang>            ->  JSON
    python timeline.py <lang> --sh       ->  shell assignments for build.sh
"""
import json, os, subprocess, sys
V = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'audio')

LEAD = 0.15     # picture before the first word of a shot
BREATH = 0.3    # between two lines of the same passage
TURN = 0.6      # Frank's half to Mike's half, and the last line onto the closing card
HOLD = 1.5      # the closing card stays up after the slogan
TURNS = {5, 9}  # lines that open a new beat


def dur(p):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                                 '-of', 'csv=p=0', p], capture_output=True, text=True).stdout)


def starts(lang):
    """(start, end) of each of the nine lines, in seconds from the top of the cut."""
    out, end = [], None
    for n in range(1, 10):
        s = LEAD if end is None else end + (TURN if n in TURNS else BREATH)
        end = s + dur(os.path.join(V, '%s_%02d.wav' % (lang, n)))
        out.append((s, end))
    return out


def layout(lang):
    lines = starts(lang)
    cuts = [0.0] + [s - LEAD for s, _ in lines[1:]]           # where shots 1..9 begin
    shots = [b - a for a, b in zip(cuts, cuts[1:])]            # the eight generated shots
    card = max(lines[8][1] + HOLD - cuts[8], 3.0)              # the drawn closing card
    return {'starts_ms': [int(round(s * 1000)) for s, _ in lines],
            'shots': [round(x, 3) for x in shots], 'card': round(card, 3),
            'total': round(cuts[8] + card, 3)}


if __name__ == '__main__':
    got = layout(sys.argv[1])
    if '--sh' in sys.argv:
        print("STARTS='%s' SHOT_D='%s' CARD_D=%s TOTAL=%s" % (
            ' '.join(map(str, got['starts_ms'])), ' '.join(map(str, got['shots'])),
            got['card'], got['total']))
    else:
        print(json.dumps(got))
