# Création d'une vidéo TikTok à partir d'un lien

Chaîne : @chatvapasss (Spongi). Vidéos « Le savais-tu ? » reprises de vidéos anglaises ou espagnoles, traduites et doublées en français.

> Dès qu'un lien vidéo est envoyé : dérouler toutes les tâches ci-dessous **automatiquement, sans redemander**. Ne s'arrêter que pour un vrai cas limite (montrer une capture et demander).

## Checklist complète

| # | Tâche | Fiche | Résultat |
|---|---|---|---|
| 1 | Récupérer la vidéo et sa transcription | [01-recuperation.md](01-recuperation.md) | vidéo source + texte d'origine |
| 2 | Traduire le texte en français | [02-traduction.md](02-traduction.md) | script français (envoyé à l'utilisateur) |
| 3 | Retirer les sous-titres d'origine (recadrer **ou** effacer) | [03-sous-titres-origine.md](03-sous-titres-origine.md) | vidéo propre |
| 4 | Générer la voix off (Fish Audio) | [04-voix-off.md](04-voix-off.md) | accroche + reste en MP3 |
| 5 | Monter : voix, vitesse, 9:16, fond flou | [05-montage.md](05-montage.md) | vidéo doublée 9:16 |
| 6 | Transcrire la voix (minutage mot à mot) | [06-transcription.md](06-transcription.md) | `words.txt` |
| 7 | Sous-titres français incrustés | [07-sous-titres.md](07-sous-titres.md) | sous-titres sur la zone floue |
| 8 | Miniature (1re image) + étiquettes traduites | [08-miniature.md](08-miniature.md) | titre FR dans la 1re image |
| 9 | Bruitages (peu, logiques avec l'image) | [09-bruitages.md](09-bruitages.md) | ~12-15 sons |
| 10 | Export final | [10-export.md](10-export.md) | MP4 9:16 téléchargeable |
| 11 | Description TikTok | [11-publication.md](11-publication.md) | texte + 4 hashtags |
| 12 | Mettre à jour ce dossier si une nouvelle règle est donnée | — | dossier à jour |

## Règles qui s'appliquent partout

- **Durée finale : toujours plus de 61 s.**
- Format 9:16 (1080×1920), image au centre, fond flou.
- Texte traduit **tel quel** : pas d'accroche, d'apport perso ni de boucle ajoutés.
- Réponses courtes à l'utilisateur, sans explications inutiles.
- Toujours vérifier sur des captures avant d'envoyer (sous-titres, miniature, étiquettes).
- Donner à la fin : lien de téléchargement, ID du projet AI Producer final, projets intermédiaires à supprimer.

## Outils

| Outil | Rôle |
|---|---|
| Tokscript | Transcription de la vidéo TikTok d'origine |
| Outil `desub_auto.py` (branche `claude/wonderful-pascal-ab20kg`, dossier `test-sous-titres/`) | Effacement automatique des sous-titres d'origine |
| Fish Audio | Voix off avec la voix clonée « Brandon » |
| ffmpeg | Montage, 9:16, fond flou, sous-titres incrustés (libass) |
| AI Producer (OpusClip) | Transcription mot à mot, bruitages (bibliothèque), export |
| Mixkit (mixkit.co) | Bruitages de secours, gratuits, sans attribution |
| `scripts/` | Scripts réutilisables (sous-titres, rendu) |
