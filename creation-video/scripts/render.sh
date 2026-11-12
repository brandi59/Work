#!/usr/bin/env bash
# Rendu final 9:16 : fond flou + image centrée + étiquettes traduites + miniature + sous-titres.
# Usage : render.sh <video_doublee.mp4> <caps.ass> <dossier_police_anton> <sortie.mp4>
#
# À ADAPTER À CHAQUE VIDÉO (coordonnées sur le canevas 1080x1920 ;
# image source à 1080 de large, centrée à partir de y=240 pour une source 3:4) :
#   THUMB : aplat qui nettoie le cadre de la miniature (1re image)
#   LAB   : étiquettes traduites (ex. AVANT / MAINTENANT) ; laisser vide si aucune
set -euo pipefail
IN=$1; ASS=$2; FONTS=$3; OUT=$4
F=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf

THUMB="drawbox=x=62:y=1205:w=956:h=286:color=0xF9DB53@1:t=fill:enable='lt(t,0.1)'"
E="enable='between(t,0.05,2.0)'"
LAB="drawbox=x=59:y=296:w=170:h=98:color=0xFFD400@1:t=fill:$E,drawbox=x=47:y=1067:w=162:h=92:color=0xFFD400@1:t=fill:$E,drawtext=fontfile=$F:text='AVANT':fontsize=46:fontcolor=black:x=63+(161-tw)/2:y=345-th/2:$E,drawtext=fontfile=$F:text='MAINTENANT':fontsize=46:fontcolor=black:box=1:boxcolor=0xFFD400:boxborderw=16:x=51:y=1112-th/2:$E"

EXTRA="$THUMB"
[ -n "$LAB" ] && EXTRA="$EXTRA,$LAB"

ffmpeg -v error -y -i "$IN" -filter_complex \
  "[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:2,eq=brightness=-0.08[bg];[b]scale=1080:-2[fg];[bg][fg]overlay=0:(H-h)/2,$EXTRA,ass=$ASS:fontsdir=$FONTS[v]" \
  -map "[v]" -map 0:a -c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p -c:a copy -movflags +faststart "$OUT"
ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT"
