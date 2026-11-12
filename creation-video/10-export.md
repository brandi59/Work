# 10. Rendu et export final

1. Rendu local 9:16 avec fond flou, étiquettes traduites, miniature et sous-titres : `scripts/render.sh` (adapter les zones des étiquettes et du cadre de la miniature).
2. Vérifier sur des captures : miniature, début des sous-titres, sous-titres sur le flou, fin.
3. Envoyer le rendu dans **AI Producer** : `sign_upload` → PUT → `start_transcribe_project` (prompt : « sous-titres déjà incrustés, ne rien couper, seulement des bruitages »).
4. Vérifier qu'aucune couche de sous-titres AI Producer n'a été ajoutée (`list_workspace` sur `compositions/`).
5. Placer les bruitages (fiche 9).
6. `finish_project`, puis `start_export` et `wait_task` (~3 min).
7. `get_export_url` : donner le lien à l'utilisateur. Il ne marche qu'une fois et expire en 15 min ; la page du projet reste disponible.
8. Indiquer l'ID du projet final et les projets intermédiaires à supprimer.
