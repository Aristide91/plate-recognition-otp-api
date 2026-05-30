# 🚗 Plate Recognition & Secure OTP Backend

Ce projet est un backend d'API REST robuste développé avec **FastAPI**, conçu pour la reconnaissance automatique de plaques d'immatriculation et la gestion sécurisée d'accès via OTP.

## 🌟 Fonctionnalités Clés

- **Reconnaissance de Plaques (OCR)** : Intégration de services de reconnaissance de plaques d'immatriculation pour différents pays (France, Tunisie, Maroc).
- **Authentification Sécurisée** : Gestion de l'authentification centralisée via **Keycloak**.
- **Système OTP Multi-canal** : Vérification en deux étapes par SMS (Twilio) et Email (SMTP).
- **Architecture Moderne** : API asynchrone, gestion fine des erreurs et documentation automatique (Swagger/ReDoc).
- **Déploiement Docker** : Prêt pour la conteneurisation avec `docker-compose`.

## 🛠️ Stack Technique

- **Langage** : Python 3.10+
- **Framework** : FastAPI
- **Sécurité** : Keycloak, JWT, OTP (Twilio/SMTP)
- **Traitement d'Image** : EasyOCR / Services OCR dédiés
- **DevOps** : Docker, Docker Compose

## 🚀 Installation Rapide

1. **Cloner le projet**
   ```bash
   git clone https://github.com/Aristide91/PythonProject-BYD.git
   cd PythonProject-BYD
   ```

2. **Configurer l'environnement**
   Copiez le fichier `.env.example` en `.env` et remplissez vos identifiants (Keycloak, Twilio, etc.).

3. **Lancer avec Docker**
   ```bash
   docker-compose up --build
   ```

4. **Accéder à la documentation**
   L'API est documentée interactivement sur `http://localhost:8000/docs`.

---
*Projet réalisé dans le cadre d'un cursus d'ingénierie à l'ESIEA.*
