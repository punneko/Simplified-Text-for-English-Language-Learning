import csv
import torch
import re
from wordfreq import zipf_frequency
from lemminflect import getInflection
from model_loader import nlp, w2v, tokenizer, model




CEFR_ORDER = {
    "A1": 1, "A2": 2,
    "B1": 3, "B2": 4,
    "C1": 5, "C2": 6
}

cefr_dict = {}

with open("data/ENGLISH_CERF_WORDS.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cefr_dict[row["headword"].strip().lower()] = row["CEFR"].strip()


def estimate_cefr_fallback(word: str) -> str:
    freq = zipf_frequency(word, "en")

    if freq >= 6: return "A1"
    if freq >= 5: return "A2"
    if freq >= 4: return "B1"
    if freq >= 3: return "B2"
    if freq >= 2: return "C1"
    return "C2"


def get_cefr_numeric(word: str) -> int:
    word = word.lower()
    level = cefr_dict.get(word)

    if level in CEFR_ORDER:
        return CEFR_ORDER[level]

    fallback = estimate_cefr_fallback(word)
    return CEFR_ORDER[fallback]




def is_candidate(token):
    return (
        token.pos_ in {"NOUN", "VERB", "ADJ", "ADV"} and
        not token.is_stop and
        token.is_alpha and
        len(token.text) > 5 
    )


def pos_match(original_token, candidate_word):
    doc = nlp(candidate_word)
    if not doc:
        return False
    return doc[0].pos_ == original_token.pos_




def pick_best_synonym(orig_token, model, topn=20):

    lemma = orig_token.lemma_.lower()

    if lemma not in model:
        return None

    orig_cefr = get_cefr_numeric(lemma)

    if orig_cefr >= 4:   
        sim_threshold = 0.55
    else:
        sim_threshold = 0.7

    candidates = []

    for cand, sim in model.most_similar(lemma, topn=topn):

        cand = cand.lower()

        if sim < sim_threshold:
            continue

        if cand == lemma:
            continue

        if not pos_match(orig_token, cand):
            continue

        cand_cefr = get_cefr_numeric(cand)

        if cand_cefr >= orig_cefr:
            continue

        simplicity = (7 - cand_cefr) / 6
        score = (sim * 0.7) + (simplicity * 0.3)

        candidates.append((cand, score))

    if not candidates:
        return None

    best = max(candidates, key=lambda x: x[1])[0]

  
    return {
        "original": orig_token.text,
        "replacement": best
    }




def lexical_simplify(text):

    doc = nlp(text)
    new_tokens = []

    changes = []

    for token in doc:

        replacement = token.text

        if is_candidate(token):

            result = pick_best_synonym(token, w2v)

            if result:

                best = result["replacement"]

               
                if token.pos_ == "VERB":
                    inflected = getInflection(best, tag=token.tag_)
                    if inflected:
                        best = inflected[0]

            
                if token.text[0].isupper():
                    best = best.capitalize()

                replacement = best

                changes.append({
                    "original": result["original"],
                    "replacement": best
                })

        new_tokens.append(replacement)

    text_out = " ".join(new_tokens)
    text_out = re.sub(r"\s+([.,!?;:])", r"\1", text_out)

    return text_out.strip(), changes




def simplify_text(text, max_length=64):

    input_text = "simplify: " + text
    inputs = tokenizer(input_text, return_tensors="pt")

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=max_length,
            num_beams=4,
            no_repeat_ngram_size=3,
            repetition_penalty=1.2,
            length_penalty=0.9,
            early_stopping=True
        )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)



def fix_morphology_errors(text: str):
    doc = nlp(text)
    fixed = []

    for token in doc:
        word = token.text

        word = re.sub(r"(ed)+$", "ed", word)
        word = re.sub(r"(ing)+$", "ing", word)

        fixed.append(word)

    text_out = " ".join(fixed)
    text_out = re.sub(r"\s+([.,!?;:])", r"\1", text_out)

    return text_out.strip()



def full_simplify(text):

    t5_output = simplify_text(text)
    t5_output = fix_morphology_errors(t5_output)

    simplified, changes = lexical_simplify(t5_output)

    return {
        "simplified_text": simplified,
        "highlights": changes
    }