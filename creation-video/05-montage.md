# 5. Montage : voix, vitesse, 9:16

## Voix
Concaténer accroche + reste, retirer les blancs, accélérer à **×1,1 maximum**, normaliser le volume :

```sh
ffmpeg -i hook.mp3 -i rest.mp3 -filter_complex "[0:a]aresample=44100,aformat=channel_layouts=mono[a0];[1:a]aresample=44100,aformat=channel_layouts=mono[a1];[a0][a1]concat=n=2:v=0:a=1,silenceremove=start_periods=1:start_threshold=-45dB:stop_periods=-1:stop_duration=0.15:stop_threshold=-45dB,atempo=1.1,loudnorm=I=-14:TP=-1.5:LRA=11[o]" -map "[o]" -c:a pcm_s16le voice.wav
```

## Vidéo calée sur la voix
- Facteur = durée voix / durée vidéo. Accélérer (ou ralentir) la vidéo de ce facteur pour qu'elle dure exactement autant que la voix.
- Couper le son d'origine, mettre la voix.
- Vérifier : **durée > 61 s**.

```sh
ffmpeg -i video_propre.mp4 -i voice.wav -filter_complex "[0:v]setpts=<FACTEUR>*PTS,fps=30[v]" -map "[v]" -map 1:a -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest tiktok_vo.mp4
```

## Format 9:16 avec fond flou
Fait au rendu final avec les sous-titres : voir `scripts/render.sh`.
- Fond : la vidéo agrandie pour remplir 1080×1920, floutée et légèrement assombrie.
- Image : la vidéo à 1080 de large, centrée verticalement.
