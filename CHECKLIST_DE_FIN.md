# ✅ LA CHECKLIST DE FIN (Le mémo pour pas rater la moyenne)

Salut ! Avant d'envoyer ton projet au prof, fais un petit tour de piste avec cette liste. C'est ce qui fait la différence entre un projet "étudiant" et un projet "pro".

### 📂 Organisation des fichiers
- [ ] **Le fichier `.gitignore`** : **CRITIQUE !** Tu ne l'as pas à la racine. Sans lui, tu vas envoyer tes dossiers `.venv`, `venv`, et `.idea` au prof. C'est lourd et pas propre.
- [ ] **Nettoyage des environnements** : Tu as deux dossiers `.venv` et `venv`. Choisis-en un et supprime l'autre. En général, on garde `.venv`.
- [ ] **Suppression des brouillons** : Supprime `note.txt`, `plan.txt` et le `main.py` à la racine (c'est juste le fichier par défaut de PyCharm, ton vrai code est dans `app/main.py`).
- [ ] **Le fichier `.env`** : Vérifie que ton `.env` n'est pas sur ton Git (il doit être dans le `.gitignore`). Par contre, assure-toi que `.env.example` contient bien toutes les clés vides pour que le prof sache quoi remplir.

### 💻 Propreté du Code
- [ ] **Noms de variables** : Évite les `a`, `b`, `truc`. Dans `ocr_service.py`, tes noms sont déjà pas mal (`plate_fr_eu_match`), garde cette rigueur partout !
- [ ] **Commentaires utiles** : Ton code est assez clair, mais quelques commentaires sur les Regex complexes dans l'OCR feraient plaisir au prof (expliquer pourquoi on cherche tel pattern pour tel pays).
- [ ] **Docstrings** : Ajoute une petite phrase au début de chaque fonction importante pour dire ce qu'elle fait (tu l'as déjà fait sur `_clean_ocr_result`, c'est top, continue !).

### ⚙️ Dépendances
- [ ] **`requirements.txt`** : Assure-toi qu'il est à jour. Si tu as installé un truc sans le noter, fais un `pip freeze > requirements.txt` (attention à bien être dans ton environnement virtuel).

### 🧪 Tests
- [ ] **Lancer les tests une dernière fois** : Un projet qui arrive avec des tests qui échouent, c'est pas cool. Lance un petit `pytest` pour être sûr.

---
*Conseil de tuteur : Un projet bien rangé, c'est 50% de la note. Le prof sera de bonne humeur dès l'ouverture du dossier !*
