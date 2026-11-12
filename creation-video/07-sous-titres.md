# 7. Sous-titres français incrustés

## Style
- Une ligne de **2–3 mots** (14 caractères max), **capitales**, police **Anton** (très grasse et serrée).
- Blanc, contour noir épais, **mot prononcé en jaune** ; petit effet « pop » à chaque nouvelle ligne.
- Parfaitement synchronisés (minutage `words.txt`), mots identiques à la voix, sans clignotement.

## Position
- Toujours **dans l'image** (pas dans le fond flou).
- **Pile sur la zone floue des sous-titres d'origine effacés**, pour cacher la trace (fiche 3). Exemple : zone à ~75 % de la hauteur de la vidéo source → centre à y = 240 + 0,765 × 1440 ≈ 1345 sur le canevas 1080×1920.
- Si les sous-titres d'origine ont été recadrés (pas de flou) : bas de l'image, au-dessus de la zone des boutons TikTok.

## Timing
- **Commencer après la miniature** (1re image).

## Outils
- Police : `npm pack @fontsource/anton`, puis conversion du WOFF en TTF avec fontTools.
- `scripts/make_ass.py words.txt caps.ass --title "LIGNE 1\NLIGNE 2" --y 1345` produit le fichier de sous-titres et le titre de la miniature.
- Rendu : `scripts/render.sh` (fiche 10).
- Vérifier sur 4 à 6 captures : position sur le flou, lisibilité, accents.
