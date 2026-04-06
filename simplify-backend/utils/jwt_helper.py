import jwt
from datetime import datetime, timedelta
from config import Config

def create_jwt_token(user_info):
    payload = {
        "sub": user_info["email"],
        "name": user_info["name"],
        "exp": datetime.utcnow() + timedelta(days=7)
    }
    token = jwt.encode(payload, Config.JWT_SECRET, algorithm="HS256")
    return token

def verify_jwt_token(token):
    try:
        payload = jwt.decode(token, Config.JWT_SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
