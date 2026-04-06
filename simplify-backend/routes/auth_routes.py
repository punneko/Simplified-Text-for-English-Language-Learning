from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import jwt
import re  
from config import Config
from services.db_service import users_collection
from services.auth_service import hash_password, verify_password, verify_google_token

auth_bp = Blueprint("auth_bp", __name__)


def is_valid_password(password: str) -> bool:
    pattern = re.compile(r"^(?=.*[a-z])(?=.*[A-Z]).{8,}$")
    return bool(pattern.match(password))



@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    name = data.get("name")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    if not is_valid_password(password):
        return jsonify({
            "error": "Password must be at least 8 characters and include uppercase and lowercase letters"
        }), 400

    if users_collection.find_one({"email": email}):
        return jsonify({"error": "Email already exists"}), 400

    new_user = users_collection.insert_one({
        "auth_provider": "local",
        "email": email,
        "name": name,
        "password_hash": hash_password(password),
        "created_at": datetime.utcnow(),
        "last_login": datetime.utcnow()
    })

    payload = {
        "sub": email,
        "name": name,
        "exp": datetime.utcnow() + timedelta(days=7)
    }
    token = jwt.encode(payload, Config.JWT_SECRET, algorithm="HS256")
    if isinstance(token, bytes):
        token = token.decode("utf-8")

    return jsonify({
        "user_id": str(new_user.inserted_id),
        "name": name,
        "email": email,
        "token": token
    }), 201



@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = users_collection.find_one({"email": email})
    if not user or not verify_password(password, user["password_hash"]):
        return jsonify({"error": "Invalid credentials"}), 401

    users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {"last_login": datetime.utcnow()}}
    )

    payload = {
        "sub": email,
        "name": user.get("name"),
        "exp": datetime.utcnow() + timedelta(days=7)
    }
    token = jwt.encode(payload, Config.JWT_SECRET, algorithm="HS256")
    if isinstance(token, bytes):
        token = token.decode("utf-8")

    return jsonify({
        "user_id": str(user["_id"]),
        "name": user.get("name"),
        "email": email,
        "token": token
    })



@auth_bp.route("/google-login", methods=["POST"])
def google_login():
    data = request.get_json()
    google_token = data.get("credential")

    if not google_token:
        return jsonify({"error": "Missing token"}), 400

    user_info = verify_google_token(google_token)
    if not user_info:
        return jsonify({"error": "Invalid token"}), 401

    user = users_collection.find_one({"email": user_info["email"]})
    if user:
        users_collection.update_one(
            {"_id": user["_id"]},
            {"$set": {"google_id": user_info["sub"], "last_login": datetime.utcnow()}}
        )
        user_id = str(user["_id"])
    else:
        new_user = users_collection.insert_one({
            "auth_provider": "google",
            "email": user_info["email"],
            "name": user_info.get("name"),
            "password_hash": None,
            "google_id": user_info["sub"],
            "created_at": datetime.utcnow(),
            "last_login": datetime.utcnow()
        })
        user_id = str(new_user.inserted_id)

    payload = {
        "sub": user_info["email"],
        "name": user_info.get("name"),
        "picture": user_info.get("picture"),
        "exp": datetime.utcnow() + timedelta(days=7)
    }
    token = jwt.encode(payload, Config.JWT_SECRET, algorithm="HS256")
    if isinstance(token, bytes):
        token = token.decode("utf-8")

    return jsonify({
        "user_id": user_id,
        "name": user_info.get("name"),
        "email": user_info["email"],
        "token": token
    })
