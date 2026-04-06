import csv
import re
import requests
from wordfreq import zipf_frequency
from deep_translator import GoogleTranslator
from model_loader import nlp



POS_MAP = {
    "NOUN": "noun",
    "VERB": "verb",
    "ADJ": "adjective",
    "ADV": "adverb",
    "ADP": "preposition"
}

def cefr_rank(level):
    return {"A1":1, "A2":2, "B1":3, "B2":4, "C1":5, "C2":6}.get(level, 99)

CEFR_DICT = {}
with open("data/ENGLISH_CERF_WORDS.csv", newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        word = row["headword"].lower().strip()
        new_level = row["CEFR"].strip().upper()
        
        if word not in CEFR_DICT or cefr_rank(new_level) < cefr_rank(CEFR_DICT[word]):
            CEFR_DICT[word] = new_level

def estimate_cefr_fallback(word: str) -> str:
    freq = zipf_frequency(word, "en")

    if freq >= 6: return "A1"
    if freq >= 5: return "A2"
    if freq >= 4: return "B1"
    if freq >= 3: return "B2"
    if freq >= 2: return "C1"
    return "C2"

def get_cefr(word: str) -> str:
    word = word.lower().strip()
    if word in CEFR_DICT:
        return CEFR_DICT[word]
    
    print(f"Debug: Word '{word}' not found in CSV, using fallback.")
    return estimate_cefr_fallback(word)



def clean_thai_spacing(text: str) -> str:
    if not text:
        return text

    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'(?<=[ก-๙])\s+(?=[ก-๙])', '', text)

    return text.strip()



def is_valid_english_word(word: str) -> bool:
    return zipf_frequency(word, "en") > 2


TRANSLATION_CACHE = {}
translator = GoogleTranslator(source="en", target="th")


def translate_to_thai(text: str) -> str:
    if not text:
        return None

    text = text.lower().strip()

    if text in TRANSLATION_CACHE:
        return TRANSLATION_CACHE[text]

    try:
        translated = translator.translate(text)
        cleaned = clean_thai_spacing(translated)

        TRANSLATION_CACHE[text] = cleaned
        return cleaned

    except Exception as e:
        print("Translate error:", e)
        return None



def suggest_vocab(sentence: str):

    results = []
    seen_words = set()
    doc = nlp(sentence)

    for token in doc:

        if not token.is_alpha:
            continue

        if token.is_stop:
            continue

        if token.pos_ not in POS_MAP:
            continue

        lemma = token.lemma_.lower()

        if lemma in seen_words:
            continue

        if not is_valid_english_word(lemma):
            continue

        seen_words.add(lemma)

        target_pos = POS_MAP[token.pos_]
        cefr_level = get_cefr(lemma)

      
        if cefr_rank(cefr_level) < cefr_rank("A1"):
            continue

        result = {
            "word": token.text,
            "lemma": lemma,
            "pos": target_pos,
            "cefr": cefr_level,
            "translation_th": translate_to_thai(lemma),
            "definition_en": None,
            "synonyms": []
        }

        
        try:
            dict_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{lemma}"
            dict_res = requests.get(dict_url, timeout=6)

            if dict_res.status_code != 200:
                results.append(result)
                continue

            data = dict_res.json()

            if not isinstance(data, list) or not data:
                results.append(result)
                continue

            entry = data[0]
            meanings = entry.get("meanings", [])

            matched_definition = None
            raw_synonyms = []

            for meaning in meanings:
                if meaning.get("partOfSpeech") == target_pos:
                    defs = meaning.get("definitions", [])
                    if defs:
                        matched_definition = defs[0].get("definition")
                        raw_synonyms = defs[0].get("synonyms", [])
                        break

            if matched_definition:
                result["definition_en"] = matched_definition

                seen_syn = set()
                filtered = []

                for s in raw_synonyms:
                    s_clean = s.lower().strip()

                    if s_clean in seen_syn:
                        continue
                    seen_syn.add(s_clean)

                    if " " in s_clean:
                        continue

                    if not is_valid_english_word(s_clean):
                        continue

                    level = get_cefr(s_clean)

                    if cefr_rank(level) <= cefr_rank(cefr_level):
                        filtered.append({
                            "word": s_clean,
                            "cefr": level
                        })

                result["synonyms"] = sorted(
                    filtered,
                    key=lambda x: cefr_rank(x["cefr"])
                )[:5]

        except requests.RequestException:
            pass

        results.append(result)

    return results



def merge_vocab_lists(original_list, simplified_list):
    merged = {}

    for item in original_list + simplified_list:
        lemma = item.get("lemma")
        if not lemma:
            continue

        if lemma not in merged:
            merged[lemma] = item

    return sorted(
        merged.values(),
        key=lambda x: cefr_rank(x["cefr"])
    )


def suggest_merged_vocab(original_text: str, simplified_text: str):
    original_vocab = suggest_vocab(original_text)
    simplified_vocab = suggest_vocab(simplified_text)

    return merge_vocab_lists(original_vocab, simplified_vocab)