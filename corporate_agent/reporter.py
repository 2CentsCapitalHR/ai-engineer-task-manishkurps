# create JSON report and save files
import json
import os
from datetime import datetime
from config import OUTPUT_DIR

def build_report_and_save(process, uploaded_files, checklist_result, issues_all_docs, reviewed_paths):
    """
    Save a JSON report summarizing everything and return the path to the JSON.
    """
    report = {
        "process": process,
        "uploaded_files": uploaded_files,
        "checklist_result": checklist_result,
        "issues": issues_all_docs,
        "reviewed_paths": reviewed_paths,
        "generated_at": datetime.utcnow().isoformat() + "Z"
    }
    filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out_path = os.path.join(OUTPUT_DIR, filename)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    return out_path, report
