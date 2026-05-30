from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SECRET_KEY: str = "supersecretkey"  # Change this in production!
    KEYCLOAK_REALM_URL: str = "http://localhost:8080/realms/mon_projet"
    KEYCLOAK_CLIENT_ID: str = "fastapi-client"
    KEYCLOAK_CLIENT_SECRET: str = "your-keycloak-client-secret"
    TWILIO_ACCOUNT_SID: str = "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    TWILIO_AUTH_TOKEN: str = "your_twilio_auth_token"
    TWILIO_PHONE_NUMBER: str = "+15017122661" # Your Twilio phone number

    # SMTP for Email OTP (example with Gmail)
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = "your_email@gmail.com"
    SMTP_PASSWORD: str = "your_email_password"
    SENDER_EMAIL: str = "your_email@gmail.com"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
