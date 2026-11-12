# 1. Récupérer la vidéo et sa transcription

1. Recevoir le lien TikTok (ou YouTube Shorts / Instagram Reels).
2. Transcription d'origine via **Tokscript** (`get_tiktok_transcript`, ou l'équivalent YouTube / Instagram).
3. Télécharger la vidéo via **Tokscript** (`download_video`).
4. Noter la langue d'origine (anglais, espagnol…), la durée et la résolution (`ffprobe`).
5. Faire une planche d'images (1 image toutes les 2 s) pour repérer :
   - les sous-titres incrustés (position, couleur, s'ils bougent) ;
   - les étiquettes ou titres en langue étrangère (ex. « Antes / Ahora ») ;
   - la 1re image (cadre ou zone de titre pour la miniature).

```sh
ffmpeg -i video.mp4 -vf "fps=1/2,scale=180:-1,drawtext=text='%{pts\:hms}':x=4:y=4:fontsize=16:fontcolor=yellow:box=1:boxcolor=black,tile=10x4" -frames:v 1 planche.jpg
```
