# BYD Charging Station - Guide de Finalisation

Ce projet intègre l'authentification **Keycloak**, l'analyse de carte grise par **OCR** (EasyOCR) et la vérification par **OTP** (SMS/Email).

## 1. Prérequis
- **Python 3.10+**
- **Keycloak** (lancé localement sur le port 8080)
- Une connexion internet (pour charger les modèles OCR au premier lancement)

## 2. Configuration Keycloak
Assurez-vous que votre instance Keycloak possède :
- Un Realm nommé : `mon_projet`
- Un Client Frontend : `byd-frontend` (Public, avec Web Origins `*` ou `http://localhost:*`)
- Un Client Backend : `fastapi-backend` (Confidential)

Mettez à jour le fichier `.env` avec le `CLIENT_SECRET` si nécessaire.

## 3. Installation et Lancement
```bash
# 1. Installation des dépendances
.\.venv\Scripts\pip install -r requirements.txt

# 2. Lancement du Backend (FastAPI)
.\.venv\Scripts\python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# 3. Lancement du Frontend
# Ouvrez simplement le fichier frontend/index.html dans votre navigateur.
```

## 4. Tests effectués
- **OCR Logic** : Validé par tests unitaires (extraction de plaque et VIN).
- **OTP Logic** : Validé par tests unitaires (génération, stockage et vérification).
- **Backend Integrity** : Le serveur démarre sans erreurs d'importation.
- **Interface UI** : Nouvelle interface BYD unifiée (Login -> OCR -> OTP -> Succès).

## 5. Problèmes potentiels
- **Accès Interdit (Access Denied)** : Si vous avez une erreur d'accès sur Windows, assurez-vous de bien utiliser `.\.venv\Scripts\python` au lieu de simplement `python`. Cela garantit que vous utilisez l'exécutable du projet et non un alias système (comme celui du Microsoft Store) qui pourrait être bloqué ou mal configuré.
- **EasyOCR** : Le premier scan peut être lent car il télécharge les modèles linguistiques.
- **CORS** : Si vous accédez au frontend via une URL différente de `localhost`, vérifiez les `Web Origins` dans Keycloak.
