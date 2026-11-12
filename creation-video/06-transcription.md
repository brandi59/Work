# 6. Transcription mot à mot de la voix off

1. Envoyer `tiktok_vo.mp4` dans **AI Producer** : `sign_upload` → PUT du fichier → `start_transcribe_project` (prompt : ne rien couper).
2. Attendre la fin (`wait_task`, ~3 min).
3. `get_transcript` (detail `words`) → chaque mot avec son début et sa fin en ms.
4. Écrire `words.txt`, une ligne par mot : `mot debut_ms fin_ms`.
   - Rattacher la ponctuation isolée au mot précédent (ex. `directement ?`).
   - Corriger les noms mal transcrits (ex. « Jesse » → « Jessie ») sans changer ce qui est dit.

Ce projet AI Producer ne sert qu'à la transcription : le signaler comme supprimable à la fin.
