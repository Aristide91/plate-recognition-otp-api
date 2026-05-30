from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from keycloak import KeycloakOpenID
from app.core.config import settings

# Configuration Keycloak
keycloak_openid = KeycloakOpenID(
    server_url=settings.KEYCLOAK_REALM_URL.rsplit('/', 2)[0],
    realm_name=settings.KEYCLOAK_REALM_URL.split('/')[-1],
    client_id=settings.KEYCLOAK_CLIENT_ID,
    client_secret_key=settings.KEYCLOAK_CLIENT_SECRET,
)

# Schéma OAuth2 pour extraire le token du header Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# Cache pour la clé publique Keycloak
_cached_public_key = None

def get_keycloak_public_key():
    global _cached_public_key
    if _cached_public_key is None:
        _cached_public_key = f"-----BEGIN PUBLIC KEY-----\n{keycloak_openid.public_key()}\n-----END PUBLIC KEY-----"
    return _cached_public_key

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Obtenir la clé publique (depuis le cache si possible)
        keycloak_public_key = get_keycloak_public_key()
        
        # Décode le token JWT
        payload = jwt.decode(
            token,
            keycloak_public_key,
            algorithms=["RS256"],  # Keycloak utilise généralement RS256
            audience=settings.KEYCLOAK_CLIENT_ID,
            options={"verify_aud": False}
        )
        
        # Ici, vous pouvez ajouter d'autres vérifications sur le payload si nécessaire
        # Par exemple, vérifier les rôles, etc.

        return payload # Retourne le payload du token (informations utilisateur)

    except JWTError as e:
        print(f"JWT Error: {e}")
        raise credentials_exception
    except Exception as e:
        print(f"Keycloak or other error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during authentication",
        )
