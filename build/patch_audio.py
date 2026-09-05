"""Teach both films to play recorded narration clips, falling back to the
browser's own speech synthesis whenever a clip for that line is absent."""
import io
import re

FILES = ['gantry-to-payout.html', 'stop-losing-start-earning.html']

AUDIO_DECL = '''  /* Recorded narration, keyed "<scene>-<cue>" per language. Empty until
     embed_audio.py inlines the clips; until then the browser speaks the lines. */
  var AUDIO = {};

'''

HELPERS = '''  var clipEl = null;

  function getClip(sceneIdx, cueIdx){
    var bank = AUDIO[lang];
    return bank ? bank[sceneIdx + '-' + cueIdx] : null;
  }

  function ensureClipEl(){
    if (!clipEl){
      clipEl = new Audio();
      clipEl.preload = 'auto';
    }
    return clipEl;
  }

  // A recorded clip wins over synthesis; synthesis is the fallback that keeps
  // the film narrated on any machine even before the voice-over exists.
  function speakCue(sceneIdx, cueIdx){
    if (!voiceOn || sceneIdx < 0 || cueIdx < 0) return;
    var cue = SCENES[sceneIdx] && SCENES[sceneIdx].cues[cueIdx];
    if (!cue) return;

    var clip = getClip(sceneIdx, cueIdx);
    if (clip){
      hushSynth();
      var a = ensureClipEl();
      a.pause();
      if (a.src !== clip) a.src = clip;
      a.currentTime = 0;
      var p = a.play();
      if (p && p.catch) p.catch(function(){});
      return;
    }
    speak(cue[lang]);
  }

'''


def patch(fn):
    s = io.open(fn, encoding='utf-8').read()

    # --- audio bank, declared before SCENES so embed_audio.py can find it -----
    s = s.replace('  var SCENES = [', AUDIO_DECL + '  var SCENES = [', 1)

    # --- split the old hush into synth-only + everything --------------------
    old_hush_a = "  function hushNarration(){\n    if (synth){ try { synth.cancel(); } catch(e){} }\n  }"
    old_hush_b = "  function hushNarration(){ if (synth){ try{ synth.cancel(); }catch(e){} } }"
    new_hush = ("  function hushSynth(){ if (synth){ try { synth.cancel(); } catch(e){} } }\n\n"
                "  function hushNarration(){\n"
                "    hushSynth();\n"
                "    if (clipEl){ try { clipEl.pause(); } catch(e){} }\n"
                "  }")
    if old_hush_a in s:
        s = s.replace(old_hush_a, new_hush, 1)
    elif old_hush_b in s:
        s = s.replace(old_hush_b, new_hush, 1)
    else:
        raise SystemExit('hushNarration not matched in ' + fn)

    # helpers go right before the hush definitions
    s = s.replace('  function hushSynth(){', HELPERS + '  function hushSynth(){', 1)

    # --- cue-anchored animation delays --------------------------------------
    apply_fn = '''  // Visual beats are anchored to cue indices, so re-recording the narration
  // moves the animation with the voice instead of leaving it behind.
  function applyCueDelays(el, cues){
    var nodes = el.querySelectorAll('[data-cue]');
    for (var i = 0; i < nodes.length; i++){
      var n = nodes[i];
      var c = parseInt(n.getAttribute('data-cue'), 10);
      var off = parseFloat(n.getAttribute('data-cue-offset')) || 0;
      if (cues[c]) n.style.animationDelay = (cues[c].t + off).toFixed(2) + 's';
    }
  }

'''
    s = s.replace('  function showScene(i, force){', apply_fn + '  function showScene(i, force){', 1)

    pat = re.compile(r"(function showScene\(i, force\)\{\n"
                     r"    if \(i === curScene && !force\) return;\n"
                     r"    curScene = i;\n)")
    s2, n = pat.subn(lambda m: m.group(1) + "    applyCueDelays(sceneEls[i], SCENES[i].cues);\n", s, count=1)
    if not n:
        raise SystemExit('showScene not matched in ' + fn)
    s = s2

    # --- route every narration trigger through speakCue ----------------------
    s = s.replace("if (idx >= 0 && playing) speak(cues[idx][lang]);",
                  "if (idx >= 0 && playing) speakCue(curScene, idx);", 1)
    s = s.replace("        if (curCue >= 0) speak(cues[curCue][lang]);",
                  "        if (curCue >= 0) speakCue(curScene, curCue);", 1)
    s = s.replace("      if (playing && curScene >= 0 && curCue >= 0) speak(SCENES[curScene].cues[curCue][lang]);",
                  "      if (playing && curScene >= 0 && curCue >= 0) speakCue(curScene, curCue);", 1)
    s = s.replace("      if (playing) speak(SCENES[curScene].cues[curCue][lang]);",
                  "      if (playing) speakCue(curScene, curCue);", 1)
    s = s.replace("    if (playing && curScene >= 0 && curCue >= 0) speak(SCENES[curScene].cues[curCue][lang]);",
                  "    if (playing && curScene >= 0 && curCue >= 0) speakCue(curScene, curCue);", 1)
    if 'speak(SCENES[curScene]' in s or 'speak(cues[curCue][lang])' in s:
        raise SystemExit('a narration call was left unrouted in ' + fn)

    # --- resume a paused clip when playback resumes --------------------------
    s = s.replace("    showScene(sceneAt(t), true);\n    curCue = -1;\n    paint();\n    startClock();",
                  "    showScene(sceneAt(t), true);\n    curCue = -1;\n    paint();\n"
                  "    if (clipEl && clipEl.src && !clipEl.ended){\n"
                  "      var r = clipEl.play(); if (r && r.catch) r.catch(function(){});\n"
                  "    }\n    startClock();", 1)

    io.open(fn, 'w', encoding='utf-8').write(s)
    print('patched', fn)


for f in FILES:
    patch(f)
