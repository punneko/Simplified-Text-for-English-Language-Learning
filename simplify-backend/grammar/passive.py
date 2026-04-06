from model_loader import nlp
from grammar.lexicons import PASSIVE_TYPE_EXPLANATIONS


def is_be_passive(verb):
    #มีauxpass
    if any(c.dep_ == "auxpass" for c in verb.children):
        return True
    #be+v3
    if verb.tag_ == "VBN":
        for c in verb.children:
            if c.dep_ == "aux" and c.lemma_ == "be":
                return True

    return False


def is_get_passive(verb):
    #get+vbn
    if verb.tag_ == "VBN":
        for c in verb.children:
            if c.dep_ in ("aux", "auxpass") and c.lemma_ == "get":
                return True
    return False


def is_reduced_passive(verb):
    if verb.tag_ == "VBN":
        has_aux = any(c.dep_ in ("aux", "auxpass") for c in verb.children)
        if not has_aux and verb.dep_ in ("amod", "acl", "relcl"):
            return True
    return False


def get_passive_agent(verb):
    for c in verb.children:
        if c.dep_ == "agent" and c.lemma_ == "by":
            return " ".join(t.text for t in c.subtree)
    return None

def explain_voice(doc):
    
    grouped_results = {}

    for token in doc:
        if token.pos_ != "VERB":
            continue

        passive_type = None
        if is_be_passive(token):
            passive_type = "be-passive"
        elif is_get_passive(token):
            passive_type = "get-passive"
        elif is_reduced_passive(token):
            passive_type = "reduced-passive"

        if not passive_type:
            continue

        
        if passive_type in grouped_results:
            grouped_results[passive_type]["triggers"].append(token.text)
            continue

        
        grouped_results[passive_type] = {
            "category": "Voice",
            "topic": "Passive voice",
            "type": passive_type,
            "triggers": [token.text], 
            "explanation": {
                "what_it_is": "Passive voice คือรูปประโยคที่ประธานทำหน้าที่เป็นผู้ถูกกระทำ",
                "effect_on_meaning": "เน้นที่สิ่งที่เกิดขึ้นหรือผลลัพธ์ มากกว่าผู้กระทำ",
                "usage_note": "มักใช้เมื่อไม่ทราบผู้กระทำ หรือในงานเขียนเชิงวิชาการ",
                "what_it_does_here": PASSIVE_TYPE_EXPLANATIONS.get(passive_type, "ใช้โครงสร้าง passive")
            }
        }

    return list(grouped_results.values())