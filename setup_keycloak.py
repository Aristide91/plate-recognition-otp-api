import os
import time
from keycloak import KeycloakAdmin

def setup_keycloak():
    admin_user = os.getenv("KEYCLOAK_ADMIN", "admin")
    admin_password = os.environ["KEYCLOAK_ADMIN_PASSWORD"]

    print("Waiting for Keycloak to be ready...")
    admin = None
    for i in range(30):
        try:
            admin = KeycloakAdmin(
                server_url="http://localhost:8080/",
                username=admin_user,
                password=admin_password,
                realm_name="master",
                verify=True
            )
            print("Connected to Keycloak!")
            break
        except Exception as e:
            time.sleep(5)
            print(f"Retrying... ({i+1}/30)")

    if not admin:
        print("Could not connect to Keycloak.")
        return

    realm_name = "mon_projet"
    
    # Create Realm
    try:
        realm_config = {
            "realm": realm_name,
            "enabled": True,
            "registrationAllowed": True,
            "registrationEmailAsUsername": False,
            "rememberMe": True,
            "verifyEmail": False
        }
        admin.create_realm(payload=realm_config, skip_exists=True)
        # If realm exists, update it to ensure registration is allowed
        admin.update_realm(realm_name=realm_name, payload=realm_config)
        print(f"Realm '{realm_name}' created/updated with registration enabled.")
    except Exception as e:
        print(f"Error handling realm: {e}")

    admin.realm_name = realm_name

    # Create Frontend Client
    try:
        clients = admin.get_clients()
        if not any(c['clientId'] == "byd-frontend" for c in clients):
            frontend_client = {
                "clientId": "byd-frontend",
                "publicClient": True,
                "directAccessGrantsEnabled": True,
                "webOrigins": ["*"],
                "redirectUris": ["*"],
                "enabled": True
            }
            admin.create_client(payload=frontend_client)
            print("Frontend client 'byd-frontend' created.")
        else:
            print("Frontend client 'byd-frontend' already exists.")
    except Exception as e:
        print(f"Error handling frontend client: {e}")

    # Create Backend Client
    try:
        clients = admin.get_clients()
        if not any(c['clientId'] == "fastapi_backend" for c in clients):
            backend_client = {
                "clientId": "fastapi_backend",
                "publicClient": False,
                "secret": "dummy_secret",
                "serviceAccountsEnabled": True,
                "enabled": True
            }
            admin.create_client(payload=backend_client)
            print("Backend client 'fastapi_backend' created.")
        else:
            print("Backend client 'fastapi_backend' already exists.")
    except Exception as e:
        print(f"Error handling backend client: {e}")

    # Create a test user
    test_user = {
        "username": "testuser",
        "enabled": True,
        "email": "test@example.com",
        "firstName": "Test",
        "lastName": "User",
        "credentials": [{"type": "password", "value": "testpassword", "temporary": False}]
    }
    try:
        admin.create_user(payload=test_user, exist_ok=True)
        print("Test user 'testuser' created with password 'testpassword'.")
    except Exception as e:
        print(f"Error creating test user: {e}")

if __name__ == "__main__":
    setup_keycloak()
