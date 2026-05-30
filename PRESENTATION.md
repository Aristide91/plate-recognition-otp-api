# 🎤 Guide de Présentation (L'Oral)

Voici quelques billes pour ton oral ou ton rapport. L'objectif : montrer que tu maîtrises ton sujet et que tu as anticipé les problèmes.

### 💡 Points forts à mettre en avant
1.  **La robustesse de l'OCR** : Explique comment tu "nettoies" les résultats (ex: transformer un `0` en `O` pour les lettres de plaques). C'est de la "post-processing" intelligente.
2.  **L'architecture propre** : Ton code est découpé en "services" (`ocr_service`, `otp_service`). C'est modulaire et facile à maintenir.
3.  **La gestion du "Mode Démo"** : Dans ton `otp_service`, tu as prévu des `try/except` qui simulent l'envoi si les clés API manquent. C'est super malin pour une démo sans stress !

### 🧠 Questions "Pièges" du Prof (et comment y répondre)
- **Q : "Pourquoi stocker les OTP en mémoire (`otp_storage`) et pas en base ?"**
    - *R : "Pour ce prototype, la rapidité était prioritaire. En prod, j'utiliserais Redis avec un TTL (Time To Live) pour que les codes expirent automatiquement."*
- **Q : "Comment ton OCR gère-t-il les mauvaises conditions lumineuses ?"**
    - *R : "Actuellement, il repose sur la puissance d'EasyOCR. Une amélioration serait d'ajouter un prétraitement avec OpenCV pour améliorer le contraste avant l'analyse."*
- **Q : "Est-ce que ton API est sécurisée ?"**
    - *R : "Oui, j'ai intégré un middleware CORS et l'authentification est déléguée à Keycloak, ce qui est un standard de l'industrie pour le SSO (Single Sign-On)."*

### 🛠️ Ce que tu as appris
- La manipulation de Regex complexes pour s'adapter aux différents formats de plaques internationaux.
- L'intégration de services tiers (Twilio, Keycloak) qui est une compétence très demandée en entreprise.
- La structuration d'une API asynchrone performante avec FastAPI.
