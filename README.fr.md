# 🚗 API de reconnaissance de plaques et OTP

🇬🇧 [English version](README.md)

Un prototype de backend **FastAPI** pour l'enregistrement à une borne de recharge de véhicule électrique. L'utilisateur se connecte avec **Keycloak** et envoie une photo de sa carte grise. L'API lit **la plaque d'immatriculation et le numéro VIN par OCR**, puis confirme l'utilisateur avec un **code à usage unique** envoyé par SMS ou par e-mail.

Projet d'école réalisé pendant mon semestre d'échange à l'EPI Digital School (Sousse, Tunisie).

## Fonctionnalités

- **OCR sur la carte grise** avec EasyOCR : extraction du VIN et de la plaque, avec des règles regex pour les formats **France/UE, Tunisie et Maroc**, et correction des erreurs d'OCR fréquentes (`0`↔`O`, `8`↔`B`…).
- **Authentification** déléguée à **Keycloak** (OpenID Connect) : l'API vérifie le JWT sur chaque route protégée.
- **Vérification OTP** par SMS (**Twilio**) ou e-mail (**SMTP**), avec un mode démo quand aucune clé d'API n'est configurée.
- **Front web minimal** (`frontend/`) : connexion → scan du document → OTP → validation, plus une petite page d'administration.
- **Tests unitaires** de l'analyse OCR et de la logique OTP.
- Documentation interactive de l'API générée par FastAPI (Swagger UI).

## Stack technique

Python 3.10+ · FastAPI · Pydantic Settings · Keycloak · python-jose · EasyOCR / OpenCV · Twilio · SQLite · Docker Compose

## API

| Méthode | Route | Description |
|---|---|---|
| `GET` | `/api/v1/auth/me` | Utilisateur courant, d'après le jeton Keycloak |
| `POST` | `/api/v1/vehicles/analyze-registration-doc` | Envoi d'une image : renvoie la plaque, le VIN, le pays et le texte brut |
| `POST` | `/api/v1/otp/send-otp` | Envoie un code à 6 chiffres par SMS ou e-mail |
| `POST` | `/api/v1/otp/verify-otp` | Vérifie le code |
| `GET` | `/api/v1/admin/reservations` | Liste des réservations |

## Lancer le projet en local

```bash
cp .env.example .env              # puis renseigner KEYCLOAK_ADMIN_PASSWORD (et les clés Twilio/SMTP si vous en avez)
docker compose up -d              # démarre Keycloak sur http://localhost:8080

python -m venv .venv
.venv/bin/pip install -r requirements.txt    # Windows : .venv\Scripts\pip
export KEYCLOAK_ADMIN_PASSWORD=...           # même valeur que dans .env
.venv/bin/python setup_keycloak.py           # crée le realm, les clients et un utilisateur de test
.venv/bin/uvicorn app.main:app --reload      # API sur http://localhost:8000/docs
```

Ouvrir ensuite `frontend/index.html` dans un navigateur. EasyOCR télécharge ses modèles au premier scan : la première requête est lente.

Lancer les tests :

```bash
python -m unittest discover tests
```

## Limites connues

C'est un prototype, pas du code de production :

- Les codes OTP sont gardés en mémoire (en production : Redis avec une durée de vie).
- La route d'administration n'est pas protégée et CORS accepte toutes les origines.
- Seul Keycloak tourne dans Docker ; l'API tourne en local.
