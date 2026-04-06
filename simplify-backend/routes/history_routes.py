from flask import Blueprint, request, jsonify
from services.db_service import history_collection
from bson import ObjectId
from bson.json_util import dumps

history_bp = Blueprint("history_bp", __name__)

@history_bp.route("/history", methods=["GET"])
def get_history():
    user_id = request.headers.get("X-User-Id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    history_cursor = history_collection.find(
        {"user_id": ObjectId(user_id)}
    ).sort("created_at", -1)

    history_list = []
    for h in history_cursor:
        history_list.append({
            "id": str(h["_id"]),
            "original_text": h["original_text"],
            "simplified_text": h["simplified_text"],
            "vocabulary": h.get("vocabulary", {}),
            "grammar": h.get("grammar", {}),
            "created_at": h["created_at"].strftime("%d/%m/%Y %H:%M:%S")
        })

    return jsonify(history_list)
