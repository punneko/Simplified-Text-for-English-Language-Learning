def extract_structure(doc):

    structure = {
        "main": None,
        "subordinate": None,
        "root": None
    }

    subordinate_tokens = set()


    for token in doc:
        if token.dep_ in ["advcl", "relcl", "ccomp"]:
            subtree = list(token.subtree)

            structure["subordinate"] = {
                "start": subtree[0].i,
                "end": subtree[-1].i,
                "text": " ".join([t.text for t in subtree])
            }

            subordinate_tokens.update([t.i for t in subtree])
            break

    
    root = None
    for token in doc:
        if token.dep_ == "ROOT":
            root = token
            break

    if root:
        
        structure["root"] = {
            "index": root.i,
            "text": root.text
        }

        main_tokens = []

        for t in root.subtree:
            if t.i not in subordinate_tokens:
                if not (t.pos_ == "PUNCT" and t.i < root.i):
                    main_tokens.append(t)

        if main_tokens:
            structure["main"] = {
                "start": main_tokens[0].i,
                "end": main_tokens[-1].i,
                "text": " ".join([t.text for t in main_tokens])
            }

    return structure