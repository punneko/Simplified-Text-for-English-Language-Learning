
from grammar.conj import explain_conjunction
from grammar.tense import explain_tense
from grammar.passive import explain_voice
from grammar.relative_clause import explain_relative_clause
from grammar.svo import explain_svo
from model_loader import nlp

GRAMMAR_ORDER = {
    ("Clause", "Relative clause"): 1,

    ("Conjunction", "Coordinating conjunction"): 2,
    ("Conjunction", "Subordinating conjunction"): 3,

    ("Word Order", "Inversion"): 4, 

    ("Voice", "Passive voice"): 5
}


def priority(item):
    
    if item["category"] == "Tense":
        return 6

    return GRAMMAR_ORDER.get(
        (item["category"], item["topic"]),
        99
    )



def explain_grammar(text):
    doc = nlp(text)
    results = []

    results.extend(explain_relative_clause(doc))
    results.extend(explain_conjunction(doc))
    results.extend(explain_svo(doc))
    results.extend(explain_voice(doc))
    results.extend(explain_tense(doc))
    

    results = sorted(results, key=priority)

    return results
