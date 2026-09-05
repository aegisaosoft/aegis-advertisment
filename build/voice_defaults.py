# -*- coding: utf-8 -*-
"""The narrator is an adult woman — not a child.

The films narrate themselves with the voice pack on the viewer's own machine, and
two things were pushing that read towards a child:

* **The default pitch was 1.14.** The slider tops out at 1.35 and the label says as
  much — "higher reads younger" — so a seventh of the way up, on a voice already
  chosen for youth, is what made the narrator sound like a girl rather than a woman.
  A sales film about a fleet's toll losses cannot be read by a child.
* **Two of the neural voices *are* children.** Microsoft's en-GB **Maisie** and en-US
  **Ana** are child voices, and they score as female + natural + young, which is
  exactly the top of our ranking. They are now demoted below every adult voice —
  still in the list, so anyone who wants one can pick it by hand.

Both the assembler and the localiser take their player engine from the same source
film, so both call `adult_narrator()` on it; `pitch_markup()` does the matching edit
to the shell's slider. Each raises if its anchor is gone rather than quietly leaving
the old default in place.

`set_adult_narrator.py` applies the same edits to films that were already built.
"""

PITCH_JS_OLD = 'var pitchVal = 1.14;   // a touch above neutral reads younger'
PITCH_JS_NEW = ("var pitchVal = 1.0;    // an adult woman; the film is not read by a child\n"
                "                       // (the slider still goes up - see voice_defaults.py)")

PITCH_MARKUP_OLD = '<input type="range" id="pitchSel" min="0.85" max="1.35" step="0.01" value="1.14"'
PITCH_MARKUP_NEW = '<input type="range" id="pitchSel" min="0.85" max="1.35" step="0.01" value="1"'

# Maisie is a child voice; it has no business in the list that ranks voices *up*.
YOUNG_OLD = 'sonia|libby|maisie|aria|jenny'
YOUNG_NEW = 'sonia|libby|aria|jenny'

NATURAL_LINE = "  var NATURAL = /(natural|online|neural|google|premium|enhanced|siri)/;"
CHILD_BLOCK = NATURAL_LINE + """

  // Microsoft's en-GB "Maisie" and en-US "Ana" are child voices. They read as female,
  // natural and young, which is the top of the ranking above, so without this a viewer
  // on Edge hears a little girl narrate a fleet's toll losses. Demoted below every
  // adult voice; still selectable by hand from the voice list.
  var CHILD   = /(^|[^a-z])(maisie|ana)([^a-z]|$)/;"""

RANK_OLD = """    if (YOUNG.test(n.split(' - ')[0])) score += 10;
    return score;"""
RANK_NEW = """    if (YOUNG.test(n.split(' - ')[0])) score += 10;
    if (CHILD.test(n.split(' - ')[0])) score -= 40;
    return score;"""

# The nudge towards Edge was selling youth; it is naturalness that is worth having.
HINT_OLD = "' For a younger, more natural read, open this page in Microsoft Edge"
HINT_NEW = "' For a warmer, more natural read, open this page in Microsoft Edge"


def adult_narrator(engine, where='engine'):
    """Player JS with the adult-woman defaults. Raises if an anchor has moved.

    Each edit carries its own "already there" marker rather than testing for the
    replacement text: the child-voice block *starts with* the line it is anchored to,
    so asking whether the anchor is still present would re-apply it on every run.
    """
    edits = [
        # (anchor, replacement, marker that says this edit is already in)
        (PITCH_JS_OLD, PITCH_JS_NEW, 'var pitchVal = 1.0;'),
        (YOUNG_OLD, YOUNG_NEW, None),
        (NATURAL_LINE, CHILD_BLOCK, 'var CHILD   ='),
        (RANK_OLD, RANK_NEW, 'CHILD.test('),
        (HINT_OLD, HINT_NEW, HINT_NEW),
    ]
    for old, new, marker in edits:
        done = marker in engine if marker else (new in engine and old not in engine)
        if done:
            continue
        if old not in engine:
            raise SystemExit('[%s] voice_defaults anchor missing: %s' % (where, old[:60]))
        engine = engine.replace(old, new, 1)
    # Self-heal a film that was written by the earlier version of this function, which
    # re-appended the child-voice block each time it ran.
    duplicate = CHILD_BLOCK[len(NATURAL_LINE):]
    while engine.count('var CHILD   =') > 1:
        engine = engine.replace(duplicate + duplicate, duplicate, 1)
        if engine.count('var CHILD   =') > 1 and duplicate + duplicate not in engine:
            raise SystemExit('[%s] more than one child-voice block, and not adjacent' % where)
    return engine


def pitch_markup(html, where='shell'):
    """Shell markup with the slider starting where the narration actually starts."""
    if PITCH_MARKUP_NEW in html and PITCH_MARKUP_OLD not in html:
        return html
    if PITCH_MARKUP_OLD not in html:
        raise SystemExit('[%s] voice_defaults anchor missing: the pitch slider' % where)
    return html.replace(PITCH_MARKUP_OLD, PITCH_MARKUP_NEW, 1)
