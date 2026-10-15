#!/bin/sh
# Build one language's cut of the film, end to end.
#
#   sh build_film.sh ru
#
# The picture is the ToonBee export and never changes; everything else is ours. The
# narration recorded by tts.py and laid on the scene grid by assemble.py replaces the
# export's audio outright — there is no music under it, so nothing is lost — and then the
# two frames the generator cannot letter are composited over it: the price list of scene
# 10 and the closing card.
#
# Captions come last because they are measured off the finished narration.
set -e
HERE=$(dirname "$0")
ROOT=C:/aegis-aa/aegis-advertisment
FF=D:/ffmpeg/bin/ffmpeg.exe
LANG_=$1
[ -n "$LANG_" ] || { echo "usage: sh build_film.sh <lang>"; exit 1; }

SOURCE="$ROOT/Stop Losing Revenue.mp4"
TRACK="$HERE/$LANG_.wav"
CARD="$ROOT/build/short45/endcard.$LANG_.png"
FILM="$ROOT/myeztoll-toonbee-$LANG_.mp4"
BODY="$HERE/body.$LANG_.mp4"

# Uzbek is the one cut with no narration of its own: no model speaks it, so the film
# keeps the export's English voice and everything a viewer reads — captions, price
# list, closing card — is Uzbek.
case "$LANG_" in uz) DUBBED=no ;; *) DUBBED=yes ;; esac

for f in "$SOURCE" "$CARD" "$HERE/pricecard.$LANG_.mp4"; do
  [ -f "$f" ] || { echo "missing: $f"; exit 1; }
done
[ "$DUBBED" = no ] || [ -f "$TRACK" ] || { echo "missing: $TRACK"; exit 1; }

# 1. The export's picture, our narration. -shortest because the track is cut to the
#    grid exactly and the video carries a few frames more.
if [ "$DUBBED" = yes ]; then
  "$FF" -y -hide_banner -loglevel error -i "$SOURCE" -i "$TRACK" \
    -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest "$BODY"
else
  "$FF" -y -hide_banner -loglevel error -i "$SOURCE" \
    -map 0:v -map 0:a -c:v copy -c:a aac -b:a 192k "$BODY"
fi

# 2. The closing card, and the loudness both cuts already share.
sh "$HERE/append_endcard.sh" "$BODY" "$FILM" "$CARD"

# 3. The drawn price list over scene 10.
sh "$HERE/splice_scene10.sh" "$LANG_"

# 4. Captions from the script, timed off the recording.
python "$HERE/make_captions.py" "$LANG_"

# 5. The same captions as an optional track inside the file.
case "$LANG_" in
  ru) TAG=rus ;; de) TAG=deu ;; fr) TAG=fra ;; pt) TAG=por ;; es) TAG=spa ;;
  uk) TAG=ukr ;; tr) TAG=tur ;; zh) TAG=zho ;;
  hy) TAG=hye ;; ka) TAG=kat ;; fa) TAG=fas ;; ur) TAG=urd ;; uz) TAG=uzb ;;
  *) TAG=eng ;;
esac
"$FF" -y -hide_banner -loglevel error -i "$FILM" -i "$ROOT/myeztoll-toonbee-$LANG_.srt" \
  -map 0:v -map 0:a -map 1 -c copy -c:s mov_text \
  -metadata:s:s:0 language=$TAG -disposition:s:0 0 "$HERE/final.$LANG_.mp4"
mv -f "$HERE/final.$LANG_.mp4" "$FILM"
rm -f "$BODY"

echo "$LANG_: $(basename "$FILM") built"
