#!/usr/bin/env bash
# Render every built episode in one language, skipping those whose mp4 is newer than their
# page (so a restart resumes instead of starting over). Usage: bash render_all.sh en|es LOG
cd "$(dirname "$0")"
lang="$1"; log="$2"
# The Turo part (22-26) first: it is new and goes out before the re-renders of 1-21.
for html in $(ls ep2[2-6]."$lang".html | sort) $(ls ep*."$lang".html | sort | grep -v -E '^ep2[2-6]\.'); do
  n=$(echo "$html" | sed -E 's/^ep0*([0-9]+)\..*/\1/')
  mp4=$(ls mp4/myeztoll-tutorial-$(printf '%02d' "$n")-*-"$lang".mp4 2>/dev/null | head -1)
  # A render cut off mid-write leaves an mp4 with no duration: only a playable one counts.
  if [ -n "$mp4" ] && [ "$mp4" -nt "$html" ] && ffprobe -v error -show_entries format=duration -of csv=p=0 "$mp4" 2>/dev/null | grep -q .; then echo "skip $html" >> "$log"; continue; fi
  node render.js "$n" "$lang" 2>&1 | tr '\r' '\n' | grep "→" >> "$log"
done
echo "DONE $lang" >> "$log"
