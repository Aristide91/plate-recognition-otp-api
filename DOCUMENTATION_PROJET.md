# Documentation Technique : BYD Smart Charging Station

Ce document résume le fonctionnement technique du projet pour la présentation.

## 1. Architecture Globale
L'application est divisée en trois composants principaux :
- **Frontend** : Interface utilisateur moderne en HTML/Tailwind CSS, utilisant `keycloak.js` pour la sécurité.
- **Backend** : API REST construite avec **FastAPI** (Python), gérant l'OCR, l'OTP et la validation des jetons.
- **Keycloak** : Serveur d'Identité (IAM) gérant l'authentification et les comptes utilisateurs.

---

## 2. Authentification (Keycloak)
Le flux de connexion suit le standard **OpenID Connect (OIDC)** :
- **Identification** : L'utilisateur est redirigé vers Keycloak pour se connecter.
- **Sécurisation** : Une fois connecté, le Frontend reçoit un **JWT (JSON Web Token)**.
- **Validation** : Chaque appel vers le backend (`/analyze-registration-doc`, `/send-otp`, etc.) inclut ce jeton dans le header `Authorization`. Le backend vérifie la signature du jeton auprès de Keycloak avant d'exécuter la requête.

---

## 3. Analyse de Carte Grise (OCR)
Pour identifier le véhicule, nous utilisons la technologie **OCR (Optical Character Recognition)** :
- **Moteur** : **EasyOCR** (bibliothèque Python basée sur le Deep Learning).
- **Fonctionnement** :
    1. L'utilisateur upload une photo de sa carte grise.
    2. Le backend traite l'image pour extraire le texte.
    3. Des **expressions régulières (Regex)** sont utilisées pour isoler précisément le **Numéro de Plaque d'Immatriculation** et le **Code VIN**.
- **Avantage** : Automatise la saisie et réduit les erreurs humaines lors de l'identification du véhicule.

---

## 4. Vérification à Double Facteur (OTP)
Une fois le véhicule identifié, une couche de sécurité supplémentaire est ajoutée via un **OTP (One-Time Password)** :
- **Service** : L'application supporte l'envoi par **Email** (via SMTP/Gmail) et par **SMS** (via Twilio).
- **Logique** :
    1. Un code aléatoire à 6 chiffres est généré et stocké temporairement en mémoire (ou base de données).
    2. L'utilisateur reçoit le code et le saisit sur l'interface.
    3. Le backend valide le code. S'il est correct, la session de recharge est autorisée.

---

## 5. Résumé pour la Présentation
- **Sécurité** : Keycloak (Standard industriel).
- **Intelligence** : OCR avec EasyOCR pour la lecture automatique.
- **Fiabilité** : OTP multicanal (SMS/Email).
- **Interface** : Expérience fluide "Mobile-First".
