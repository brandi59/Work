# Workflow montage TikTok — @chatvapasss (Spongi)

Contenu : Dragon Ball / JoJo façon « Le savais-tu ? », repris de vidéos anglaises ou espagnoles et traduit en français.

> Dès qu'un lien vidéo est envoyé : lancer tout le workflow automatiquement, sans redemander.

> 📁 Toutes les tâches détaillées, étape par étape, sont dans le dossier [`creation-video/`](creation-video/README.md).

## 1. Texte
1. Recevoir le lien TikTok de la vidéo.
2. Récupérer la transcription via **Tokscript**.
3. Traduire en français et l'envoyer.
4. Garder le texte traduit **tel quel** (pas d'accroche, d'apport perso ni de boucle ajoutés).

## 2. Voix off (Fish Audio)
- Voix clonée « Brandon » : `64854779388d437591ac30c617816cc4`.
- 5–10 premières secondes (hook) : modèle acting **drama-3**, dynamique mais naturel, jamais crié.
- Reste de la vidéo : énergique, émotif, dans l'action, très naturel (pas fade).
- Intonations gérées librement par Claude pour une voix attractive et dynamique ; rythme global un peu accéléré.
- Pas de retranscription Fish Audio de la voix off.

## 3. Montage (AI Producer)
1. Recevoir l'audio + l'ID du projet AI Producer.
2. Retirer les blancs de l'audio.
3. Voix à vitesse naturelle (1.1x max).
4. Récupérer la vidéo source depuis le workspace du projet (pas via Drive).
5. Format 9:16 : image recadrée au centre, fond flou.
   - **Avant de recadrer : repérer où sont les sous-titres d'origine (texte incrusté) et ajuster le recadrage pour les couper entièrement — plus aucun bout visible.** À vérifier sur plusieurs images de la vidéo.
6. Ralentir la vidéo pour qu'elle dure autant que l'audio.
7. Couper le son d'origine, mettre la voix.
8. Exporter en MP4 9:16 et l'envoyer.

**Durée finale : toujours plus de 61 secondes.**

## 4. Sous-titres
- Une ligne de 2–3 mots, grosses capitales très grasses et serrées.
- Blanc, contour noir épais, mot prononcé en jaune.
- Calés gratuitement sur le texte traduit + pauses de la voix.
- Parfaitement synchronisés, mots identiques à la voix, sans clignotement.
- Toujours **dans l'image de l'anime** (pas dans le fond flou), bien visibles sans être trop gros.
- Méthode qui marche : incrustation ffmpeg (ASS, police Anton via npm `@fontsource/anton`), minutage mot à mot de la transcription AI Producer, puis nouveau projet AI Producer pour les bruitages et l'export.
- **Placer les sous-titres pile sur la zone floue des sous-titres d'origine retirés**, pour cacher le flou.
- Ne démarrer les sous-titres qu'après la miniature (1re image).
- Étiquettes incrustées en langue étrangère (ex. « Antes / Ahora ») : les recouvrir par leur traduction française.

## 5. Bruitages
- **Claude est autonome sur les bruitages** : les ajouter sans redemander.
- **Peu de bruitages (≈ 1 toutes les 5 s, ~12-15 pour 70 s), tous logiques avec l'image** — pas un son sur chaque coupe.
  - Changements d'image marquants : déclic d'appareil photo ; ouverture / saut dans le temps : whoosh.
  - Son en rapport avec ce qu'on voit ou entend : orage sur la pluie/l'éclair, zoom d'objectif sur un plan qui zoome, bip de mise au point quand un cadre rouge apparaît, impact sur une attaque, nappe angoissante sur un moment grave, boom grave sur la révélation finale.
  - Repérer les coupes avec ffmpeg (scene > 0.25) et vérifier visuellement avant de choisir.
- Sources : bibliothèque AI Producer en priorité, sinon Mixkit (mixkit.co, gratuit, sans attribution).
- Ponctuels, variés, calés précisément sur les images (pas que des woosh).
- Whoosh quand un personnage entre dans l'image.
- Coups / impacts discrets pendant les combats.
- Sons trouvés librement par Claude, même hors bibliothèque AI Producer.
- Volume : celui de la vidéo Gogito SSJ10 v2.

## 6. Miniature
- Remplacer le texte anglais de la 1re image par une miniature en français.
- Si la 1re image a un cadre (ex. carré jaune) : nettoyer les traces et y écrire le titre de la vidéo en français (Anton, noir, 2 lignes).
- Vidéos JoJo : fond rose et noir quadrillé sur toute l'image.

## 7. Publication
- Écrire une description TikTok avec 4 hashtags.
- Ne jamais mettre `#whattowatch` (ajouté à la main).
