from model_loader import nlp
from .lexicons import (
    TENSE_EFFECTS,
    TIMELINE_ORDER,
    TENSE_STRUCTURES
)


DEFAULT_EFFECTS = TENSE_EFFECTS

ORDER_MAP = {tense: i for i, tense in enumerate(TIMELINE_ORDER)}



def has_aux(token, lemmas):
    return any(
        c.dep_ in {"aux", "auxpass"} and c.lemma_ in lemmas
        for c in token.children
    )


def has_aux_sequence(token, lemmas):
    aux_lemmas = {
        c.lemma_
        for c in token.children
        if c.dep_ in {"aux", "auxpass"}
    }
    return all(l in aux_lemmas for l in lemmas)


def has_past_aux(token):
    return any(
        c.dep_ in {"aux", "auxpass"} and c.tag_ == "VBD"
        for c in token.children
    )


def is_modal(token):
    return any(
        c.dep_ == "aux" and c.tag_ == "MD"
        for c in token.children
    )


def is_going_to_future(token):
    if token.lemma_ != "go" or token.tag_ != "VBG":
        return False

    if not has_aux(token, {"be"}):
        return False

    return any(
        c.dep_ == "xcomp" and c.tag_ == "VB"
        for c in token.children
    )


def is_past_question(token):
    return any(
        c.dep_ == "aux"
        and c.lemma_ == "do"
        and c.tag_ == "VBD"
        for c in token.children
    )


def is_clause_head(token):
    return token.dep_ in {"ROOT", "conj", "advcl", "ccomp", "xcomp"}


def get_clean_phrase(token):
   
    core_deps = {"det", "poss", "nsubj", "nsubjpass", "aux", "auxpass", "neg", "prt", "dobj", "attr", "acomp"}
    
    core_tokens = [t for t in token.children if t.dep_ in core_deps]
    core_tokens.append(token) 
    
    
    sorted_phrase = sorted(core_tokens, key=lambda t: t.i)
    return " ".join(t.text for t in sorted_phrase)

def explain_tense(doc, effects=DEFAULT_EFFECTS):
    tense_map = {}

    for token in doc:
        if not is_clause_head(token) or token.pos_ not in {"VERB", "AUX"}:
            continue

    
        predicate = get_clean_phrase(token)
        tense = None

     
        
        #Future
        if is_going_to_future(token):
            tense = "Future (going to)"
        elif token.tag_ == "VBG" and has_aux_sequence(token, {"will", "have", "be"}):
            tense = "Future Perfect Continuous"
        elif token.tag_ == "VBN" and has_aux_sequence(token, {"will", "have"}):
            tense = "Future Perfect"
        elif token.tag_ == "VBG" and has_aux_sequence(token, {"will", "be"}):
            tense = "Future Continuous"
        elif token.tag_ == "VB" and has_aux(token, {"will"}):
            tense = "Future Simple"

        #Past
        elif token.tag_ == "VBG" and has_aux_sequence(token, {"have", "be"}) and has_past_aux(token):
            tense = "Past Perfect Continuous"
        elif token.tag_ == "VBN" and has_aux(token, {"have"}) and has_past_aux(token):
            tense = "Past Perfect"
        elif token.tag_ == "VBG" and has_aux(token, {"be"}) and has_past_aux(token):
            tense = "Past Continuous"
        elif is_past_question(token) or token.tag_ == "VBD":
            tense = "Past Simple"

        #Present
        elif token.tag_ == "VBG" and has_aux_sequence(token, {"have", "be"}) and not has_past_aux(token):
            tense = "Present Perfect Continuous"
        elif token.tag_ == "VBN" and has_aux(token, {"have"}) and not has_past_aux(token):
            tense = "Present Perfect"
        elif token.tag_ == "VBG" and has_aux(token, {"be"}):
            tense = "Present Continuous"
        elif token.tag_ in {"VBP", "VBZ"}:
            tense = "Present Simple"

        #Modal
        elif is_modal(token):
            tense = "Modal"

        if not tense:
            continue

    
        if tense not in tense_map:
            tense_map[tense] = {
                "category": "Tense",
                "topic": tense,
                "explanation": {
                    "effect_on_meaning": effects.get(tense),
                    "structure": TENSE_STRUCTURES.get(tense),
                    "examples": []
                }
            }

        if predicate and len(tense_map[tense]["explanation"]["examples"]) < 1:
            tense_map[tense]["explanation"]["examples"].append(predicate)

    return sorted(tense_map.values(), key=lambda x: ORDER_MAP.get(x["topic"], 999))