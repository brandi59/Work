# Workflow montage TikTok — @chatvapasss (Spongi)

Contenu : Dragon Ball / JoJo façon « Le savais-tu ? », repris de vidéos anglaises ou espagnoles et traduit en français.

> Dès qu'un lien vidéo est envoyé : lancer tout le workflow automatiquement, sans redemander.

## 1. Texte
1. Recevoir le lien TikTok de la vidéo.
2. Récupérer la transcription via **Tokscript**.
3. Traduire en français et l'envoyer.
4. Garder le texte traduit **tel quel** (pas d'accroche, d'apport perso ni de boucle ajoutés).

## 2. Voix off (Fish Audio) — recette « Bishop/Euphoria » (validée le 17/11, à utiliser pour TOUTES les voix off)
**Génération**
- Voix clonée « Brandon » : `64854779388d437591ac30c617816cc4`, modèle **s2.1-pro**.
- Accroche (2 premières phrases) : générée à part avec la balise `[excited]`.
- Reste du script : un seul appel, **sans balise**.
- Aucun autre réglage (pas de vitesse, pitch ou émotion en plus).
- Pas de retranscription Fish Audio de la voix off.

**Après Fish Audio (ffmpeg)**
- Suppression des blancs : pauses ≥ 60 ms coupées, 25 ms gardés de chaque côté.
- Égalisation : coupe sous 90 Hz, −3,5 dB à 220 Hz, −1,5 dB à 500 Hz, +3,5 dB à 3200 Hz, +4 dB au-dessus de 8500 Hz.
- Débruitage léger, de-esser, compression douce (seuil −22 dB, ratio 2,5).
- Normalisation à −13 LUFS.
- Exemple de chaîne : `highpass=f=90,equalizer=f=220:t=q:w=1:g=-3.5,equalizer=f=500:t=q:w=1:g=-1.5,equalizer=f=3200:t=q:w=1:g=3.5,highshelf=f=8500:g=4,afftdn=nr=8,deesser,acompressor=threshold=-22dB:ratio=2.5:attack=10:release=150,loudnorm=I=-13:TP=-1.5:LRA=11`
- Vidéo Diego (17/11) : voix accélérée de 7 % au montage (`atempo=1.07`).

## 3. Montage (autonome, sans AI Producer)
Ne pas demander d'ID de projet : tout se fait à partir du lien TikTok.
1. Télécharger la vidéo source depuis le lien TikTok avec **yt-dlp** :
   `pip install yt-dlp` si besoin, puis `yt-dlp -o source.mp4 -f "best[ext=mp4]/best" <lien>` (dans le scratchpad).
2. Retirer les blancs de l'audio (ffmpeg `silenceremove`).
3. Voix à vitesse naturelle (1.1x max).
4. Monter localement avec **ffmpeg**.
5. **Retirer les sous-titres d'origine (texte incrusté)** au lieu de les couper au recadrage :
   - `pip install opencv-python-headless numpy` si besoin, puis
     `python3 test-sous-titres/desub_auto.py <source.mp4> <source_sans_st.mp4>` (repère seul la zone des sous-titres, ~1 min par minute de vidéo).
   - Vérifier sur plusieurs images qu'il ne reste aucun sous-titre ; sinon refaire une passe ciblée avec `DESUB_RATIO=0.18` (ou ajuster les seuils dans `test-sous-titres/detect.py`).
6. Format 9:16 : image recadrée au centre (sans couper pour les sous-titres), fond flou.
7. Ralentir la vidéo pour qu'elle dure autant que l'audio.
8. Couper le son d'origine, mettre la voix.
9. Exporter en MP4 9:16 et l'envoyer.

**Durée finale : toujours plus de 61 secondes.**

**Fichiers :** ne jamais commiter les vidéos, audios ni miniatures dans le dépôt (`livrables/` et les médias sont ignorés par `.gitignore`). Les envoyer directement à l'utilisateur ; le dépôt ne contient que le workflow et les scripts.

## 4. Sous-titres
- Une ligne de 2–3 mots, grosses capitales très grasses et serrées.
- Blanc, contour noir épais, mot prononcé en jaune.
- Calés gratuitement sur le texte traduit + pauses de la voix.
- Parfaitement synchronisés, mots identiques à la voix, sans clignotement.
- Toujours **dans l'image de l'anime** (pas dans le fond flou), bien visibles sans être trop gros.
- Ne démarrer les sous-titres qu'après la miniature (1re image).

## 5. Bruitages
- **Entre 10 et 15 bruitages maximum par vidéo** : aucun bruitage inutile.
- Un petit « POC » à chaque flèche ou encadrement qui apparaît à l'écran.
- Le reste : quelques transitions bien placées (changement de scène important, révélation).
- Ponctuels, variés, calés précisément sur les images (pas que des woosh).
- Whoosh quand un personnage entre dans l'image.
- Coups / impacts discrets pendant les combats.
- Sons trouvés librement par Claude, même hors bibliothèque AI Producer.
- Volume : celui de la vidéo Gogito SSJ10 v2.

## 6. Miniature
- Remplacer le texte anglais de la 1re image par une miniature en français.
- Si la 1re image a un cadre (ex. carré jaune) : nettoyer les traces du texte d'origine et y écrire le titre de la vidéo en français (police Anton, noir, 2 lignes).
- Vidéos JoJo : fond rose et noir quadrillé sur toute l'image.

## 7. Publication
- Écrire une description TikTok avec 4 hashtags.
- Ne jamais mettre `#whattowatch` (ajouté à la main).
