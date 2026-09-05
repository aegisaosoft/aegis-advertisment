#!/bin/sh
# Put the drawn closing card on the end of a ToonBee export.
#
#   sh append_endcard.sh <in.mp4> <out.mp4> [card.png]
#
# Everything in the ToonBee cut is generated, and generated lettering drifts: the
# money figure counted itself down mid-shot and the price discs came out reading
# nothing at all. The last frame is the one whose wording has to be exact, so it is
# drawn (endcard.html) and stapled on here. The audio is padded first — without
# apad the mix ends on the last word and -shortest would cut the card off. The pad
# is one fade shorter than the hold, because the cross-fade overlaps the two.
#
# The mix is brought to -16 LUFS on the way out. ToonBee exports quiet - the English
# cut measured -25.4 - and the two language versions have to play at one level.
set -e
FF=D:/ffmpeg/bin/ffmpeg.exe
IN=$1
OUT=$2
CARD=${3:-C:/aegis-aa/aegis-advertisment/build/short45/endcard.png}
HOLD=3.4          # long enough to read the address, short enough not to stall
FADE=0.8          # cross-fade into the card
LEN=$("$FF" -hide_banner -i "$IN" 2>&1 | sed -n 's/.*Duration: \([0-9:.]*\).*/\1/p' \
      | awk -F: '{print ($1*3600)+($2*60)+$3}')
AT=$(awk -v l="$LEN" -v f="$FADE" 'BEGIN{printf "%.3f", l-f}')
PAD=$(awk -v h="$HOLD" -v f="$FADE" 'BEGIN{printf "%.3f", h-f}')
OFF=$(awk -v l="$LEN" 'BEGIN{printf "%.3f", l-1.8}')
"$FF" -y -hide_banner -loglevel error -i "$IN" -loop 1 -t "$HOLD" -i "$CARD" \
  -filter_complex "[1:v]scale=1920:1080,fps=30,format=yuv420p,setsar=1[c];\
[0:v]fps=30,format=yuv420p,setsar=1[v];\
[v][c]xfade=transition=fade:duration=$FADE:offset=$AT[vout];\
[0:a]loudnorm=I=-16:TP=-1.5:LRA=11,apad=pad_dur=$PAD,afade=t=out:st=$OFF:d=1.8[aout]" \
  -map "[vout]" -map "[aout]" -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p \
  -movflags +faststart -c:a aac -b:a 192k "$OUT"
echo "$OUT"
