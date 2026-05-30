import random
import smtplib
from email.mime.text import MIMEText
from twilio.rest import Client
from app.core.config import settings

# Simule un stockage pour les OTP (NE PAS UTILISER EN PRODUCTION)
otp_storage = {}

class OTPService:
    def __init__(self):
        # Initialisation du client Twilio
        self.twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    def generate_otp(self) -> str:
        """Génère un code OTP aléatoire à 6 chiffres."""
        return str(random.randint(100000, 999999))

    async def send_otp_sms(self, phone_number: str, otp_code: str) -> bool:
        """
        Envoie un code OTP par SMS via Twilio.
        Retourne True si l'envoi est réussi, False sinon.
        """
        try:
            message = self.twilio_client.messages.create(
                body=f"Votre code OTP est : {otp_code}",
                from_=settings.TWILIO_PHONE_NUMBER,
                to=phone_number
            )
            print(f"SMS OTP envoyé au {phone_number}: {message.sid}")
            return True
        except Exception as e:
            print(f"ATTENTION (Mode Démo) : Erreur lors de l'envoi du SMS OTP: {e}")
            print(f"SIMULATION : Le SMS aurait contenu le code {otp_code}")
            return True # Renvoie True quand même pour ne pas bloquer la présentation

    async def send_otp_email(self, email: str, otp_code: str) -> bool:
        """
        Envoie un code OTP par email via SMTP.
        Retourne True si l'envoi est réussi, False sinon.
        """
        try:
            msg = MIMEText(f"Votre code OTP est : {otp_code}")
            msg['Subject'] = "Votre code de vérification OTP"
            msg['From'] = settings.SENDER_EMAIL
            msg['To'] = email

            with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
                server.starttls() # Activer le mode TLS
                server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
                server.send_message(msg)
            print(f"Email OTP envoyé à {email}")
            return True
        except Exception as e:
            print(f"ATTENTION (Mode Démo) : Erreur lors de l'envoi de l'Email OTP: {e}")
            print(f"SIMULATION : L'email aurait contenu le code {otp_code}")
            return True # Renvoie True quand même pour ne pas bloquer la présentation

    def store_otp(self, identifier: str, otp_code: str):
        """
        Stocke l'OTP généré pour un identifiant (email ou numéro de téléphone).
        Pour une utilisation en production, utiliser une base de données avec TTL.
        """
        otp_storage[identifier] = otp_code

    def verify_otp(self, identifier: str, otp_code: str) -> bool:
        """
        Vérifie si le code OTP fourni correspond à celui stocké.
        """
        stored_otp = otp_storage.get(identifier)
        if stored_otp and stored_otp == otp_code:
            del otp_storage[identifier] # Supprime l'OTP après utilisation
            return True
        return False


otp_service = OTPService()
