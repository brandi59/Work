# Workflow montage TikTok — @chatvapasss (Spongi)

Contenu : Dragon Ball / JoJo façon « Le savais-tu ? », repris de vidéos anglaises ou espagnoles et traduit en français.

> Dès qu'un lien vidéo est envoyé : lancer tout le workflow automatiquement, sans redemander.

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
5. **Retirer les sous-titres d'origine (texte incrusté)** au lieu de les couper au recadrage :
   - `pip install opencv-python-headless numpy` si besoin, puis
     `python3 test-sous-titres/desub_auto.py <source.mp4> <source_sans_st.mp4>` (repère seul la zone des sous-titres, ~1 min par minute de vidéo).
   - Vérifier sur plusieurs images qu'il ne reste aucun sous-titre ; sinon ajuster les seuils dans `test-sous-titres/detect.py`.
   - Renvoyer la vidéo nettoyée dans le workspace du projet et l'utiliser pour la suite.
6. Format 9:16 : image recadrée au centre (sans couper pour les sous-titres), fond flou.
7. Ralentir la vidéo pour qu'elle dure autant que l'audio.
8. Couper le son d'origine, mettre la voix.
9. Exporter en MP4 9:16 et l'envoyer.

**Durée finale : toujours plus de 61 secondes.**

## 4. Sous-titres
- Une ligne de 2–3 mots, grosses capitales très grasses et serrées.
- Blanc, contour noir épais, mot prononcé en jaune.
- Calés gratuitement sur le texte traduit + pauses de la voix.
- Parfaitement synchronisés, mots identiques à la voix, sans clignotement.
- Toujours **dans l'image de l'anime** (pas dans le fond flou), bien visibles sans être trop gros.

## 5. Bruitages
- Ponctuels, variés, calés précisément sur les images (pas que des woosh).
- Whoosh quand un personnage entre dans l'image.
- Coups / impacts discrets pendant les combats.
- Sons trouvés librement par Claude, même hors bibliothèque AI Producer.
- Volume : celui de la vidéo Gogito SSJ10 v2.

## 6. Miniature
- Remplacer le texte anglais de la 1re image par une miniature en français.
- Vidéos JoJo : fond rose et noir quadrillé sur toute l'image.

## 7. Publication
- Écrire une description TikTok avec 4 hashtags.
- Ne jamais mettre `#whattowatch` (ajouté à la main).
