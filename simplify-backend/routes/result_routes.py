from flask import Blueprint, request, jsonify
from services.simplify_service import full_simplify
from services.grammar_service import explain_grammar
from services.vocabulary_service import suggest_merged_vocab
from datetime import datetime
from bson import ObjectId
from services.db_service import history_collection
from services.translate_service import translate_text, clean_thai
from services.struc_service import extract_structure
from model_loader import nlp

result_bp = Blueprint("result_bp", __name__)


@result_bp.route("/simplify", methods=["POST"])
def simplify_text():
    try:
        user_id = request.headers.get("X-User-Id")
        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401

        try:
            user_object_id = ObjectId(user_id)
        except:
            return jsonify({"error": "Invalid user ID"}), 400

        data = request.get_json(silent=True) or {}
        text = data.get("text", "").strip()

        if not text:
            return jsonify({"error": "text is required"}), 400

        #1.Simplify 
        result = full_simplify(text)

        simplified_text = result["simplified_text"]
        highlights = result["highlights"]

        doc1 = nlp(text)
        doc2 = nlp(simplified_text)

        structure_data = {
            "original": extract_structure(doc1),
            "simplified": extract_structure(doc2)
        }

     

        #2.Translation
        original_translation = clean_thai(translate_text(text) or "")
        simplified_translation = clean_thai(translate_text(simplified_text) or "")

        #3.Grammar
        grammar_data = {
            "original": explain_grammar(text),
            "simplified": explain_grammar(simplified_text)
        }

        #4.Vocabulary
        vocab_data = suggest_merged_vocab(text, simplified_text)

        #5.Save history
        try:
            history_collection.insert_one({
                "user_id": user_object_id,
                "original_text": text,
                "simplified_text": simplified_text,
                "translation": {
                    "original": original_translation,
                    "simplified": simplified_translation
                },
                "grammar": grammar_data,
                "vocabulary": vocab_data,
                "created_at": datetime.utcnow()
            })
        except Exception as db_error:
            print("History save failed:", db_error)

        return jsonify({
            "original": text,
            "simplified": simplified_text,

            "tokens": {
                "original": [t.text for t in doc1],
                "simplified": [t.text for t in doc2]
            },
            "translation": {
                "original": original_translation,
                "simplified": simplified_translation
            },

            "grammar": grammar_data,
            "vocabulary": vocab_data,
            "structure": structure_data,
            "highlights": highlights
        })

    except Exception as e:
        print("Simplify error:", e)
        return jsonify({"error": "Internal server error"}), 500