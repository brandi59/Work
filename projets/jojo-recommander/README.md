# JoJo — « Pourquoi JoJo est si dur à recommander ? » (20/11)
Source : https://www.tiktok.com/@tuan.khan0/video/7709497967857683726 (1080x1080, 90,7 s)

- `texte_fr.txt` : traduction (voix off Fish Audio, Brandon s2.1-pro ; accroche = 2 premières phrases en `[excited]`).
- `mots.json` : timing mot à mot de la voix traitée (avant décalage miniature de 0,4 s).

## Effacement (LaMa)
```
python3 test-sous-titres/desub_lama.py source.mp4 sans_st.mp4 lama_fp32.onnx --zone 255,830,825,952 \
  --overlay 0.4,4.7,160,170,890,390,yellow --overlay 6.2,10.7,0,0,690,240,pink --overlay 10.1,13.7,320,600,1080,830,blue
```

## Montage
- Vidéo : `setpts=PTS*0.98824` (dure autant que la voix), 9:16 fond flou, image 1080x1080 à y=420, miniature 0,4 s devant.
- Voix : `adelay=400`. Sous-titres : `outils/incruster_mots.py` (centre 540,1305).
- Bruitages (id Freesound, départ s, volume) :
  683101 0.18 0.5 · 461017 13.04 0.5 · 493913 17.55 0.4 · 377303 27.05 0.4 · 530448 31.74 0.45 · 648729 41.00 0.5 ·
  683101 42.90 0.45 · 493911 49.38 0.35 · 216781 50.30 0.3 · 754771 61.37 0.45 · 879797 72.90 0.8 · 461017 75.00 0.45 · 377303 87.00 0.5

## Description TikTok
Pourquoi JoJo est-il si dur à recommander aux nouveaux ? 🤔 Ce n'est pas toi qui choisis JoJo… c'est JoJo qui te choisit. ✨
#jojo #jojosbizarreadventure #anime #lesavaistu
