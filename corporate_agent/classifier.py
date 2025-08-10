# detect document type (keyword-based)
DOC_KEYWORDS = {
    "Articles of Association": ["articles of association", "aoa", "articles of association of"],
    "Memorandum of Association": ["memorandum of association", "moa", "memorandum"],
    "UBO Declaration Form": ["ultimate beneficial owner", "ubo", "ubo declaration"],
    "Incorporation Application": ["application for incorporation", "incorporation application"],
    "Register of Members": ["register of members", "register of members and directors"],
    "Register of Directors": ["register of directors"]
}

def classify_doc_type(parsed_doc):
    text = parsed_doc.get("full_text", "").lower()
    scores = {}
    for name, keywords in DOC_KEYWORDS.items():
        scores[name] = sum(1 for kw in keywords if kw in text)
    # pick highest score
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "Unknown"
