# 🚗 Plate Recognition & OTP Backend

Bienvenue dans le backend de notre système de reconnaissance de plaques d'immatriculation et de vérification sécurisée par OTP.

## 📝 Description
Ce projet est une API robuste développée avec **FastAPI**. Elle permet de :
- Reconnaître automatiquement les plaques d'immatriculation (France, Tunisie, Maroc) à partir d'images grâce à l'OCR.
- Gérer la sécurité via des codes **OTP** (SMS via Twilio et Email via SMTP).
- Authentifier les utilisateurs via **Keycloak**.

## 🚀 Lancement Rapide (2 min)

1. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

2. **Lancer le serveur** :
   ```bash
   uvicorn app.main:app --reload
   ```
*L'API sera disponible sur `http://127.0.0.1:8000`. La doc interactive est sur `/docs`.*

## 🛠️ Stack Technique
- **Framework** : FastAPI (Python)
- **OCR** : EasyOCR & OpenCV
- **Sécurité** : Keycloak (OIDC), Twilio (SMS), SMTP (Email)
- **Data** : Pydantic pour la validation, SQLite (optionnel)
- **Frontend** : HTML5/CSS3/JS (disponible dans le dossier `/frontend`)

---
*Projet réalisé dans le cadre scolaire.*
