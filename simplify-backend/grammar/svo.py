from model_loader import nlp
from grammar.lexicons import INVERSION_TRIGGERS


def starts_with_prepositional_phrase(doc):
    return len(doc) > 0 and doc[0].pos_ == "ADP"


def starts_with_negative_adverb(doc):
    return (
        len(doc) > 0
        and doc[0].lower_ in INVERSION_TRIGGERS["negative"]
    )


def starts_with_conditional(doc):
    return (
        len(doc) > 0
        and doc[0].lower_ in INVERSION_TRIGGERS["conditional"]
        and is_aux_inversion(doc)
    )


def starts_with_restrictive(doc):
    return (
        len(doc) > 0
        and doc[0].lower_ in INVERSION_TRIGGERS["restrictive"]
        and is_aux_inversion(doc)
    )


def find_root(doc):
    for token in doc:
        if token.dep_ == "ROOT":
            return token
    return None


def find_auxiliary(doc):
    for token in doc:
        if token.dep_ in ("aux", "auxpass"):
            return token
    return None


def find_subject(doc):
    for token in doc:
        if token.dep_ in ("nsubj", "nsubjpass", "expl"):
            return token

    # fallback
    root = find_root(doc)
    if root:
        for child in root.children:
            if child.pos_ in ("NOUN", "PROPN", "PRON"):
                return child

    return None


def is_locative_inversion(doc):
    if not starts_with_prepositional_phrase(doc):
        return False

    subj = find_subject(doc)
    root = find_root(doc)

    return bool(subj and root and root.i < subj.i)


def is_aux_inversion(doc):
    subj = find_subject(doc)
    aux = find_auxiliary(doc)

    return bool(subj and aux and aux.i < subj.i)


def is_root_inversion(doc):
    subj = find_subject(doc)
    root = find_root(doc)

    return bool(subj and root and root.i < subj.i)


def is_inverted(doc):
    return (
        is_aux_inversion(doc)
        or is_locative_inversion(doc)
        or is_root_inversion(doc)
    )


def classify_inversion(doc):

    if len(doc) == 0:
        return None

    
    if doc[0].tag_ in ("VBP", "VBZ", "VBD", "MD"):
        return "Question Inversion"

    if starts_with_conditional(doc):
        return "Conditional Inversion"

    if starts_with_restrictive(doc):
        return "Restrictive Inversion"

    if starts_with_negative_adverb(doc):
        return "Negative Inversion"

    if is_locative_inversion(doc):
        return "Locative Inversion"

    return "General Inversion"


def explain_svo(doc):

    results = []

    if not is_inverted(doc):
        return results

    root = find_root(doc)
    subj = find_subject(doc)
    aux = find_auxiliary(doc)

    inversion_type = classify_inversion(doc)

    explanation = {
        "what_it_is": (
            "Inversion คือการสลับตำแหน่งระหว่างประธาน (Subject) "
            "และกริยา (Verb/Auxiliary) จากลำดับปกติของภาษาอังกฤษ (SVO)"
        ),
        "effect_on_meaning": (
            "การสลับลำดับช่วยเน้นองค์ประกอบที่นำหน้าประโยค "
            "เช่น สถานที่ คำปฏิเสธ เงื่อนไข หรือโครงสร้างคำถาม"
        ),
        "usage_note": (
            "มักพบในงานเขียนเชิงพรรณนา วรรณกรรม "
            "ภาษาทางการ โครงสร้างคำถาม และ conditional clauses"
        ),
        "what_it_does_here": (
            f"ในประโยคนี้ ประธาน '{subj.text if subj else ''}' "
            f"ปรากฏหลัง "
            f"{'auxiliary' if aux and subj and aux.i < subj.i else 'verb'} "
            f"จึงเป็น {inversion_type}"
        ),
    }

    results.append({
        "category": "Word Order",
        "topic": "Inversion",
        "type": inversion_type,
        "trigger": root.text if root else None,
        "subject": subj.text if subj else None,
        "auxiliary": aux.text if aux else None,
        "clause_or_span": doc.text,
        "explanation": explanation
    })

    return results
