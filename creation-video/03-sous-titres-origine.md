# 3. Retirer les sous-titres d'origine : recadrer ou effacer

## Repérer
Prendre 1 image par seconde sur toute la vidéo et détecter le texte incrusté (blanc, jaune, vert, avec contour) : position, hauteur, s'il bouge, ce qu'il y a dessous.

## Décider

**Recadrer** quand :
- les sous-titres restent toujours dans une bande au bord (haut ou bas) ;
- la bande à couper fait moins d'environ 20 % de la hauteur ;
- on ne coupe ni visage ni action importante.

→ Ajuster le recadrage pour les couper **entièrement** (plus aucun bout visible), vérifier sur plusieurs images.

**Effacer (flou / reconstruction)** quand :
- les sous-titres sont au milieu de l'image ou sur les personnages ;
- leur position change d'un plan à l'autre ;
- recadrer couperait trop d'image ou des visages.

→ Outil `desub_auto.py` (branche `claude/wonderful-pascal-ab20kg`, dossier `test-sous-titres/`) : il trouve la zone tout seul et efface (~1 min pour 1 min de vidéo).
→ Noter la zone effacée (hauteur en % de l'image) : **les sous-titres français iront pile dessus** pour cacher la trace floue (fiche 7).

**Cas mixte** : recadrer pour la bande principale, puis effacer ou recouvrir les restes (titre d'intro, étiquettes).

**Cas limite** : montrer une capture à l'utilisateur avant de lancer tout le traitement.

Toujours dire à l'utilisateur quelle méthode a été choisie et pourquoi.
