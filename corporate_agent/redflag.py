# rule-based red flags + optional RAG assistance
import re
import os
from config import OPENAI_API_KEY
from typing import List, Dict

# simple rule checks that return a list of issues
def rule_based_checks(parsed):
    text = parsed.get("full_text", "") or ""
    issues = []

    # 1. Jurisdiction check (ADGM presence)
    if "adgm" not in text.lower():
        issues.append({
            "document": parsed["path"],
            "section": "Jurisdiction",
            "snippet": "",  # no snippet available
            "issue": "Jurisdiction clause does not explicitly mention ADGM.",
            "severity": "High",
            "suggestion": "Add an ADGM jurisdiction clause (e.g., 'This Agreement shall be governed by the laws of ADGM...')."
        })

    # 2. Signature block check
    if not re.search(r"(signed by|signature|signature:|signed:|name:)\s*", text, re.I):
        issues.append({
            "document": parsed["path"],
            "section": "Signatures",
            "snippet": "",
            "issue": "No signatory block detected.",
            "severity": "High",
            "suggestion": "Add signatory block with printed name, signature line, capacity and date."
        })

    # 3. Ambiguity: check use of 'may' in critical clauses (naive)
    if re.search(r"\bmay\b", text):
        issues.append({
            "document": parsed["path"],
            "section": "Ambiguity",
            "snippet": "may",
            "issue": "Use of 'may' in clauses might be ambiguous where mandatory language is expected.",
            "severity": "Medium",
            "suggestion": "Review instances of 'may' in operative clauses; replace with 'shall' if mandatory."
        })
    return issues

# optional: if you have a local RAG retriever and an OpenAI key, use them to get a legal check
def rag_check_clause(clause_text: str, retriever_fn):
    """
    retriever_fn(query, k) -> list of { 'text':..., 'meta': {...} }
    This function will fetch context and (if OPENAI_API_KEY set) call OpenAI to evaluate.
    """
    contexts = retriever_fn(clause_text, k=3)
    # return contexts to caller for further use; actual LLM check handled in app
    return contexts

def detect_redflags(parsed, use_rag=False, retriever_fn=None):
    """
    Main function to detect issues.
    If use_rag=True and retriever_fn provided, it will retrieve context for the top suspicious snippets.
    """
    issues = rule_based_checks(parsed)
    if use_rag and retriever_fn:
        # for brevity, only run RAG on the highest severity issues with a snippet or small extract
        for issue in list(issues):
            snippet = issue.get("snippet") or issue.get("section") or parsed.get("full_text", "")[:500]
            contexts = rag_check_clause(snippet, retriever_fn)
            # attach contexts
            issue["rag_contexts"] = contexts
    return issues
