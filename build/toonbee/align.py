# -*- coding: utf-8 -*-
"""Turn a script plus Scribe word timings into one timed span per line.

Scribe hears the words; the script knows what they are. The two are matched word by
word with an ordinary edit-distance alignment, so a misheard word ("cantry" for
"gantry", "my easy toll" for "MyEZToll") costs only that word's timing and never
reaches the caption. A line's span runs from the first word of it Scribe placed to
the last, so a line whose every word was misheard would raise rather than guess.
"""
import io
import json
import math
import re
import unicodedata


def fold(word):
    """Compare words the way a listener would: letters and digits, no accents, no case."""
    text = unicodedata.normalize('NFD', word.lower())
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]', '', text)


def tokens(line):
    return [t for t in (fold(w) for w in re.findall(r"[\w'\u2019-]+", line)) if t]


def load(path):
    data = json.load(io.open(path, encoding='utf-8'))
    return [(fold(w['text']), float(w['start']), float(w['end']))
            for w in data.get('words', [])
            if w.get('type') == 'word' and fold(w['text'])]


def match(script_words, heard):
    """Index of the heard word each script word maps to, or None. Global alignment."""
    n, m = len(script_words), len(heard)
    # Row-by-row Needleman-Wunsch; the backtrace is kept as one byte per cell.
    back = []
    prev = list(range(m + 1))
    for i in range(1, n + 1):
        cur = [i] + [0] * m
        row = bytearray(m + 1)
        row[0] = 2  # came from above: script word unmatched
        for j in range(1, m + 1):
            diag = prev[j - 1] + (0 if script_words[i - 1] == heard[j - 1][0] else 1)
            up, left = prev[j] + 1, cur[j - 1] + 1
            best = min(diag, up, left)
            cur[j] = best
            row[j] = 1 if best == diag else (2 if best == up else 3)
        back.append(row)
        prev = cur

    out = [None] * n
    i, j = n, m
    while i > 0 and j > 0:
        step = back[i - 1][j]
        if step == 1:
            if script_words[i - 1] == heard[j - 1][0]:
                out[i - 1] = j - 1
            i -= 1
            j -= 1
        elif step == 2:
            i -= 1
        else:
            j -= 1
    return out


def spans(lines, words_path, tail=0.20):
    heard = load(words_path)
    flat, owner = [], []
    for n, line in enumerate(lines):
        for token in tokens(line):
            flat.append(token)
            owner.append(n)

    where = match(flat, heard)
    hit = [[] for _ in lines]
    for token_index, heard_index in enumerate(where):
        if heard_index is not None:
            hit[owner[token_index]].append(heard_index)

    out = []
    for n, indexes in enumerate(hit):
        if not indexes:
            raise SystemExit('line %d was not heard at all: %r' % (n + 1, lines[n][:60]))
        out.append((heard[min(indexes)][1], heard[max(indexes)][2] + tail))

    # Lines are spoken in order; a caption may not start before the previous one ends.
    for n in range(1, len(out)):
        if out[n][0] < out[n - 1][1]:
            mid = (out[n][0] + out[n - 1][1]) / 2.0
            out[n - 1] = (out[n - 1][0], mid)
            out[n] = (mid, out[n][1])
    return out, [len(h) for h in hit], [len(tokens(l)) for l in lines]


def stamp(seconds):
    ms = int(round(max(0.0, seconds) * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return '%02d:%02d:%02d,%03d' % (h, m, s, ms)


def write_srt(path, lines, timing):
    out = []
    for n, ((a, b), text) in enumerate(zip(timing, lines), 1):
        out += [str(n), '%s --> %s' % (stamp(a), stamp(b)), text, '']
    io.open(path, 'w', encoding='utf-8-sig').write('\n'.join(out))


# --- captions -------------------------------------------------------------
# Two rows of about forty characters is what a viewer reads without effort and what
# every player has room for, so a spoken line longer than that becomes several cues.

WIDTH = 40
MAX_CHARS = 80
MIN_SHOW = 1.1


def word_times(lines, words_path):
    """[(word, start, end)] per line, with unheard words given a share of their neighbours."""
    heard = load(words_path)
    flat, owner = [], []
    for n, line in enumerate(lines):
        for word in re.findall(r"[\w'\u2019\u2013-]+", line):
            if fold(word):
                flat.append(word)
                owner.append(n)

    where = match([fold(w) for w in flat], heard)
    times = [None] * len(flat)
    for i, j in enumerate(where):
        if j is not None:
            times[i] = [heard[j][1], heard[j][2]]

    # Words Scribe missed sit evenly between the words on either side of them; a word
    # missed at the very start is backdated by a typical word's length, so the first
    # caption still appears when the line is actually spoken rather than one word late.
    anchors = [i for i, t in enumerate(times) if t]
    if not anchors:
        raise SystemExit('nothing was heard')
    spans = sorted(t[1] - t[0] for t in times if t)
    typical = spans[len(spans) // 2] or 0.3
    for i in range(len(times)):
        if times[i]:
            continue
        before = max((a for a in anchors if a < i), default=None)
        after = min((a for a in anchors if a > i), default=None)
        if before is None:
            back = typical * (after - i)
            times[i] = [max(0.0, times[after][0] - back),
                        max(0.0, times[after][0] - back + typical)]
        elif after is None:
            times[i] = [times[before][1], times[before][1] + typical]
        else:
            a, b = times[before][1], times[after][0]
            step = (b - a) / float(after - before)
            times[i] = [a + step * (i - before - 1), a + step * (i - before)]

    out = [[] for _ in lines]
    for i, word in enumerate(flat):
        out[owner[i]].append((word, times[i][0], times[i][1]))
    return out


def wrap(text):
    """Break a cue into rows a player can show without shrinking the type.

    Filling each row to the brim leaves the second row a stub and splits phrases that
    belong together \u2014 "Four hundred / twelve dollars". So the rows are balanced, and a
    break that lands after a full stop or a comma is preferred over one mid-phrase.
    """
    words = text.split()
    if len(' '.join(words)) <= WIDTH:
        return ' '.join(words)

    rows = max(2, int(math.ceil(len(' '.join(words)) / float(WIDTH))))
    target = len(' '.join(words)) / float(rows)

    best, cuts = None, None
    def walk(start, left, taken, cost):
        nonlocal best, cuts
        if left == 1:
            row = ' '.join(words[start:])
            if len(row) > WIDTH:
                return
            total = cost + (len(row) - target) ** 2
            if best is None or total < best:
                best, cuts = total, taken + [len(words)]
            return
        for end in range(start + 1, len(words)):
            row = ' '.join(words[start:end])
            if len(row) > WIDTH:
                break
            # A row that ends where the sentence does reads at a glance; one that
            # splits "setup fee" or "four hundred twelve" does not, so mid-phrase
            # breaks cost far more than an uneven pair of rows.
            seam = 0.0 if re.search(r'[.!?]$', words[end - 1]) else (
                6.0 if re.search(r'[,;:\u2014]$', words[end - 1]) else 90.0)
            walk(end, left - 1, taken + [end], cost + (len(row) - target) ** 2 + seam)

    walk(0, rows, [], 0.0)
    if cuts is None:
        # Nothing balanced fits; fall back to filling each row in turn.
        rows_out, row = [], ''
        for word in words:
            if row and len(row) + 1 + len(word) > WIDTH:
                rows_out.append(row)
                row = word
            else:
                row = (row + ' ' + word).strip()
        if row:
            rows_out.append(row)
        return '\n'.join(rows_out)

    out, start = [], 0
    for end in cuts:
        out.append(' '.join(words[start:end]))
        start = end
    return '\n'.join(out)


def split_line(pieces, target, max_chars):
    """Cut one spoken line into balanced caption cards.

    Greedy filling leaves orphans \u2014 "\u2026coast to" on one card and "coast." on the next.
    So the number of cards is fixed first, and the breaks are then chosen to make the
    cards even and to fall where the sentence already breaks: a full stop is the best
    place to end a card, a comma the next best, mid-clause the worst.
    """
    n = len(pieces)
    length = [len(p.strip()) + 1 for p in pieces]
    best = [None] * (n + 1)
    best[0] = (0.0, 0)
    for end in range(1, n + 1):
        for start in range(end):
            if best[start] is None:
                continue
            size = sum(length[start:end]) - 1
            if size > max_chars and end - start > 1:
                continue
            tail = pieces[end - 1]
            if re.search(r'[.!?][\u2019")\u00bb]*\s*$', tail):
                seam = 0.0
            elif re.search(r'[,;:\u2014]\s*$', tail) or end == n:
                seam = 6.0
            else:
                seam = 26.0
            cost = best[start][0] + (size - target) ** 2 / 40.0 + seam
            if best[end] is None or cost < best[end][0]:
                best[end] = (cost, start)

    cuts, at = [], n
    while at:
        cuts.append((best[at][1], at))
        at = best[at][1]
    return list(reversed(cuts))


def cues(lines, words_path, tail=0.25, beat=0.85):
    """One caption per readable chunk, timed from the words actually spoken.

    A line is also cut at a sentence end the listener can hear — a pause longer than a
    beat — so a card is never left up through a silence that belongs to the next thought.
    """
    spoken = word_times(lines, words_path)
    out = []
    for line, words in zip(lines, spoken):
        # The leading class keeps an opening ¿ or ¡ attached to its sentence.
        pieces = re.findall(r"[^\w]*[\w'\u2019\u2013-]+[^\w]*", line)
        pieces = [p for p in pieces if re.search(r"[\w]", p)]
        if len(pieces) != len(words):
            raise SystemExit('cannot line punctuation up with the timing: %r' % line[:50])

        # Audible pauses come first: they are breaks the viewer already hears.
        groups, at = [], 0
        for i in range(len(pieces) - 1):
            sentence = re.search(r'[.!?][\u2019")\u00bb]*\s*$', pieces[i]) is not None
            if sentence and words[i + 1][1] - words[i][2] > beat:
                groups.append((at, i + 1))
                at = i + 1
        groups.append((at, len(pieces)))

        for g0, g1 in groups:
            chunk = pieces[g0:g1]
            size = len(''.join(chunk).strip())
            cards = max(1, int(math.ceil(size / float(MAX_CHARS))))
            for a, b in split_line(chunk, size / float(cards), MAX_CHARS):
                out.append([''.join(chunk[a:b]).strip(),
                            words[g0 + a][1], words[g0 + b - 1][2]])

    for i, cue in enumerate(out):
        cue[2] += tail
        cue[2] = max(cue[2], cue[1] + MIN_SHOW)
        if i + 1 < len(out):
            cue[2] = min(cue[2], out[i + 1][1] - 0.04)
    return [(wrap(t), a, b) for t, a, b in out]


def write_vtt(path, cues_):
    """The same captions as WebVTT, which is what a <video> element can load."""
    out = ['WEBVTT', '']
    for text, a, b in cues_:
        out += ['%s --> %s' % (stamp(a).replace(',', '.'), stamp(b).replace(',', '.')),
                text, '']
    io.open(path, 'w', encoding='utf-8').write('\n'.join(out))
