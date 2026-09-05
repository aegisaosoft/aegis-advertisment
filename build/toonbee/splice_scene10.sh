#!/bin/sh
# Put the drawn price list over scene 10 of the film.
#
#   sh splice_scene10.sh <lang>          # en | es
#
# Scene 10 runs 64.2s to 70.2s and is the film's price list: no subscription, no set-up
# fee, nothing per vehicle. ToonBee cannot letter it — the first pass wrote "5tv" and
# "3s" on the price discs, the regenerated pass cleared the discs and span nonsense
# around them — so the six seconds of picture are replaced by pricecard.<lang>.mp4,
# whose three labels appear on the narrator's own word stamps.
#
# The card is composited rather than cut in: it fades up out of the film's opening of
# the scene and back down into the next one, over a ground sampled from the film's own
# cyclorama, so the seams are not seen. The audio and the caption track are copied
# untouched — only the picture behind the voice changes.
set -e
FF=D:/ffmpeg/bin/ffmpeg.exe
HERE=$(dirname "$0")
LANG_=${1:-en}
FILM="C:/aegis-aa/aegis-advertisment/myeztoll-toonbee-$LANG_.mp4"
CARD="$HERE/pricecard.$LANG_.mp4"
OUT="C:/aegis-aa/aegis-advertisment/build/toonbee/spliced.$LANG_.mp4"

# All four numbers were measured frame by frame off the export. The film dissolves
# into this shot and out of it rather than cutting, and the lettering being covered is
# on screen right up to the end of the outgoing dissolve — so the card fades up once
# the incoming dissolve has finished, and only starts fading down once the next shot
# has almost fully arrived. Fading out any earlier shows the nonsense underneath.
AT=64.20           # the plate has fully arrived
IN=0.20            # dissolve from the film's own discs into the card
OUTAT=6.02         # 70.22s: the car interior is most of the way in
OUTD=0.16
DUR=6.30

[ -f "$FILM" ] || { echo "no film at $FILM"; exit 1; }
[ -f "$CARD" ] || { echo "no card at $CARD — run node pricecard.js $LANG_"; exit 1; }

END=$(awk -v a="$AT" -v d="$DUR" 'BEGIN{printf "%.2f", a+d}')

"$FF" -y -hide_banner -loglevel error -i "$FILM" -i "$CARD" \
  -filter_complex "[1:v]format=yuva420p,\
fade=t=in:st=0:d=$IN:alpha=1,fade=t=out:st=$OUTAT:d=$OUTD:alpha=1,\
setpts=PTS-STARTPTS+$AT/TB[card];\
[0:v][card]overlay=0:0:eof_action=pass:enable='between(t,$AT,$END)'[v]" \
  -map "[v]" -map 0:a -map 0:s? \
  -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -movflags +faststart \
  -c:a copy -c:s copy "$OUT"

mv -f "$OUT" "$FILM"
echo "$LANG_: scene 10 replaced in $(basename "$FILM")"
