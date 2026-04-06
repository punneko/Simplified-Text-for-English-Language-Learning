from werkzeug.security import generate_password_hash, check_password_hash
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from config import Config

# local password functions
def hash_password(password: str):
    return generate_password_hash(password)

def verify_password(password: str, password_hash: str):
    return check_password_hash(password_hash, password)


# google token verify
def verify_google_token(google_token: str):
    try:
        idinfo = id_token.verify_oauth2_token(
            google_token, google_requests.Request(), Config.GOOGLE_CLIENT_ID
        )
        return {
            "email": idinfo.get("email"),
            "name": idinfo.get("name"),
            "sub": idinfo.get("sub"),  # Google unique ID
            "picture": idinfo.get("picture")
        }
    except Exception:
        return None
