# process checklists mapping
PROCESS_CHECKLISTS = {
    "Company Incorporation": [
        "Memorandum of Association",
        "Articles of Association",
        "Incorporation Application",
        "UBO Declaration Form",
        "Register of Directors"
    ],
    # you can add other processes here later
}

def verify_checklist(process, detected_doc_types):
    required = PROCESS_CHECKLISTS.get(process, [])
    detected_set = set(detected_doc_types)
    missing = [d for d in required if d not in detected_set]
    return {
        "process": process,
        "required_documents": required,
        "detected_documents": detected_doc_types,
        "missing_documents": missing
    }