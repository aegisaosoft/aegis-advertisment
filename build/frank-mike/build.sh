#!/bin/sh
# Frank vs Mike: 8 generated shots + the drawn closing card, cut to the narration.
# The voice runs continuously (timeline.py); each shot is trimmed to its own line, and a
# line longer than its shot holds that shot's last frame. Captions come from the script.
#
#   sh build.sh <lang>
#
# uz  = English narration, Uzbek card and captions (no speech model speaks Uzbek).
# zh-Hant = the zh narration, Traditional card and captions.
# The shots are the generator's exports; SHOTS is where they were downloaded to.
set -e
L=$1; HERE=$(cd "$(dirname "$0")" && pwd); A=$HERE/audio
SHOTS=${SHOTS:-/d/Downloads}
C=$HERE/../short45; OUTDIR=$HERE/../..
VO=$L; [ "$L" = uz ] && VO=en; [ "$L" = zh-Hant ] && VO=zh
case $L in en) CARD=$C/endcard.png ;; es) CARD=$C/endcard.es-tu.png ;; *) CARD=$C/endcard.$L.png ;; esac
[ -f "$CARD" ] || { echo "no card for $L"; exit 1; }
eval "$(python "$HERE/timeline.py" $VO --sh)"   # STARTS SHOT_D CARD_D TOTAL
# Story order: street, mail, phone, letter, Mike's garage, hologram, $0, Frank looks in.
CLIPS="3682351749 3439427426 328671585 559783562 2827546893 2568051098 3979775174 920882951"
set -- ; i=0; FC=""
for c in $CLIPS; do
  f=$(ls $SHOTS/${c}_*.mp4); d=$(echo $SHOT_D | cut -d" " -f$((i+1)))
  set -- "$@" -i "$f"
  FC="$FC[$i:v]scale=1280:720,fps=24,setsar=1,format=yuv420p,tpad=stop_mode=clone:stop_duration=6,trim=duration=$d,setpts=PTS-STARTPTS[v$i];"
  i=$((i+1))
done
set -- "$@" -loop 1 -t $CARD_D -i "$CARD"
FC="$FC[8:v]scale=1280:720,fps=24,setsar=1,format=yuv420p,fade=t=in:d=0.4[v8];"
for k in 0 1 2 3 4 5 6 7 8; do FC="$FC[v$k]"; done; FC="${FC}concat=n=9:v=1:a=0[v];"
AM=""
for n in 1 2 3 4 5 6 7 8 9; do
  set -- "$@" -i $A/${VO}_0$n.wav; ms=$(echo $STARTS | cut -d" " -f$n)
  FC="$FC[$((n+8)):a]adelay=$ms|$ms[a$n];"; AM="$AM[a$n]"
done
FC="$FC${AM}amix=inputs=9:normalize=0,apad,atrim=0:$TOTAL,loudnorm=I=-16:TP=-1.5:LRA=11[a]"
ffmpeg -y -v error "$@" -filter_complex "$FC" -map "[v]" -map "[a]" -t $TOTAL -c:v libx264 -crf 20 -preset medium -c:a aac -b:a 192k -ar 48000 -movflags +faststart "$OUTDIR/myeztoll-frank-mike-$L.mp4"
PYTHONIOENCODING=utf-8 python "$HERE/captions.py" $L > "$OUTDIR/myeztoll-frank-mike-$L.vtt"
echo "built $L ($TOTAL s)"
