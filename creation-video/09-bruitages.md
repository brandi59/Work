# 9. Bruitages

**Claude est autonome : les ajouter sans redemander.**

## Règle
- **Peu de bruitages** : environ 1 toutes les 5 s (12 à 15 pour 70 s). Pas un son sur chaque coupe.
- **Tous logiques avec l'image** :

| À l'image | Bruitage |
|---|---|
| Changement d'image marquant | déclic d'appareil photo |
| Ouverture, saut dans le temps (« des années plus tard ») | whoosh |
| Personnage qui entre dans l'image | whoosh |
| Pluie, éclair | tonnerre |
| Plan qui zoome | zoom d'objectif |
| Cadre rouge / cercle qui apparaît | bip de mise au point |
| Attaque, combat | impact discret |
| Moment grave, maladie, tristesse | nappe angoissante |
| Révélation finale | boom grave |

## Méthode
1. Repérer les coupes : `ffmpeg -i video.mp4 -vf "select='gt(scene,0.25)',metadata=print:file=scenes.txt" -an -f null -`.
2. Faire une planche des images avant/après chaque coupe et regarder ce qui se passe.
3. Choisir ~12–15 moments et le son qui correspond.
4. Placer avec `place_sound_effects` (bibliothèque AI Producer ; `replace: true` pour remplacer les précédents). Gain par défaut ; −3 dB sur les booms et impacts forts.
5. Sons manquants : Mixkit (mixkit.co, gratuit, sans attribution).

Volume de référence : la vidéo Gogito SSJ10 v2.
