
from .lexicons import (
    RELATIVE_PRONOUNS,
    RELATIVE_ADVERBS
)
from model_loader import nlp


def explain_relative_clause(doc):
    results = []

    for token in doc:
        if token.dep_ != "relcl":
            continue

        clause_tokens = list(token.subtree)
        clause = " ".join(t.text for t in clause_tokens)
        head_noun = token.head.text

        
        relative_word = None
        relative_meaning = None

        for t in clause_tokens:
            word = t.text.lower()
            if word in RELATIVE_PRONOUNS:
                relative_word = word
                relative_meaning = RELATIVE_PRONOUNS[word]
                break
            elif word in RELATIVE_ADVERBS:
                relative_word = word
                relative_meaning = RELATIVE_ADVERBS[word]
                break

        has_comma = any(
            t.text == "," and abs(t.i - token.head.i) <= 3
            for t in doc
        )

        clause_type = (
            "Non-defining relative clause"
            if has_comma
            else "Defining relative clause"
        )

        if clause_type == "Defining relative clause":
            explanation = {
                "what_it_is": (
                    "Relative clause เป็นประโยคย่อยที่ใช้ขยายหรือระบุคำนามอย่างเฉพาะเจาะจง"
                ),
                "effect_on_meaning": (
                    "ช่วยให้ทราบว่ากำลังกล่าวถึงคำนามใดโดยเฉพาะ "
                    "หากตัดออก ความหมายของประโยคจะไม่ชัดเจน"
                ),
                "usage_note": (
                    "ประโยคย่อยชนิดนี้จำเป็นต่อความหมายของประโยค "
                    "และไม่ใช้เครื่องหมายจุลภาค"
                ),
                "what_it_does_here": (
                    f"ในประโยคนี้ '{relative_word}' {relative_meaning} "
                    f"เพื่อขยายคำนาม '{head_noun}'"
                    if relative_word and relative_meaning
                    else f"ในประโยคนี้ ใช้ขยายคำนาม '{head_noun}'"
                ),
            }
        else:
            explanation = {
                "what_it_is": (
                    "Non-defining relative clause เป็นประโยคย่อยที่ให้ข้อมูลเพิ่มเติมเกี่ยวกับคำนาม"
                ),
                "effect_on_meaning": (
                    "ช่วยเพิ่มข้อมูลเกี่ยวกับคำนาม "
                    "แต่ไม่จำเป็นต่อความหมายหลักของประโยค"
                ),
                "usage_note": (
                    "ประโยคย่อยชนิดนี้มักคั่นด้วยเครื่องหมายจุลภาค (,)"
                ),
                "what_it_does_here": (
                    f"ในประโยคนี้ '{relative_word}' {relative_meaning} "
                    f"เพื่อขยายคำนาม '{head_noun}'"
                    if relative_word and relative_meaning
                    else f"ในประโยคนี้ ใช้ขยายคำนาม '{head_noun}'"
                ),
            }

        results.append({
            "category": "Clause",
            "topic": "Relative clause",
            "subtype": clause_type,
            "clause_or_span": clause,
            "explanation": explanation
        })

    return results
