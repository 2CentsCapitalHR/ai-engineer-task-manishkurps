Here’s your **full README.md code** — you can copy it exactly into your GitHub `README.md` file.

```markdown
# 🏛 Corporate Agent — ADGM Document Reviewer

**Corporate Agent** is an **AI-powered legal assistant** designed to help users with **document validation, verification, and compliance checking** for **Abu Dhabi Global Market (ADGM)** processes such as company incorporation.

It accepts `.docx` files, parses and classifies them, checks against legal checklists, detects red flags, and integrates **local Retrieval-Augmented Generation (RAG)** from **official ADGM documents** — all without requiring paid API keys.

---

## 📌 Features

- **Upload & Parse**: Accepts `.docx` uploads, extracts text, headings, and tables.
- **Document Classification**: Identifies type (e.g., AoA, MoA, UBO Declaration).
- **Checklist Verification**: Checks if all required documents for a process (e.g., Company Incorporation) are present.
- **Red Flag Detection**: Rule-based checks for missing jurisdiction, missing signatures, ambiguous clauses, etc.
- **Local RAG**: Retrieves relevant clauses from **official ADGM laws & checklists** (no API key needed).
- **Contextual Annotations**: Highlights problematic sections and appends comments & legal references inside the `.docx`.
- **Structured JSON Report**: Summarizes detected issues, missing documents, and references.
- **Simple Web UI**: Powered by [Gradio](https://gradio.app/).

---

## 📂 Project Structure

```

corporate\_agent/
│
├── app.py                # Main Gradio app
├── config.py              # Configuration & env loader
├── parser.py              # DOCX parsing
├── classifier.py          # Document classification
├── verifier.py            # Checklist verification
├── redflag.py             # Rule-based + RAG red flag detection
├── annotator.py           # Add comments & highlights in DOCX
├── reporter.py            # JSON report generation
├── rag\_indexer.py         # Local ADGM text indexing & retrieval
├── requirements.txt       # Python dependencies
├── .env                   # (Optional) for API keys
│
├── resources/
│   └── adgm\_texts/        # ADGM legal reference text files
│
└── outputs/               # Reviewed DOCX + JSON reports

````

---

## 🚀 Installation & Setup

### 1️⃣ Clone the repo
```bash
git clone https://github.com/yourusername/corporate_agent.git
cd corporate_agent
````

### 2️⃣ Create a virtual environment

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## 📜 Preparing ADGM Legal References (RAG)

1. Download / copy text from the **official ADGM links** (provided in `Data Sources.docx`).
2. Save each reference as a `.txt` file into:

   ```
   resources/adgm_texts/
   ```

   Example:

   ```
   adgm_companies_regulations_2020.txt
   checklist_private_company_limited.txt
   ```
3. Index them for retrieval:

```bash
python - <<'PY'
from rag_indexer import index_text_files_from_folder
index_text_files_from_folder(folder="resources/adgm_texts", out_index_dir="outputs/rag_index")
PY
```

---

## ▶️ Running the App

```bash
python app.py
```

* Open the link shown in the terminal (e.g., `http://127.0.0.1:7860`).
* Upload one or more `.docx` documents.
* Select the legal process (e.g., **Company Incorporation**).
* The app will:

  * Parse and classify documents.
  * Check checklist compliance.
  * Detect red flags.
  * Retrieve relevant ADGM references.
  * Generate:

    * **Reviewed `.docx`** (with highlights & comments)
    * **JSON report** (with details & legal citations)

---

## 📊 Example JSON Report

```json
{
  "process": "Company Incorporation",
  "uploaded_files": ["Articles_of_Association.docx"],
  "checklist_result": {
    "process": "Company Incorporation",
    "required_documents": ["Memorandum of Association", "Articles of Association", "Incorporation Application", "UBO Declaration Form", "Register of Directors"],
    "detected_documents": ["Articles of Association"],
    "missing_documents": ["Memorandum of Association", "Incorporation Application", "UBO Declaration Form", "Register of Directors"]
  },
  "issues": [
    {
      "document": "Articles_of_Association.docx",
      "section": "Jurisdiction",
      "issue": "Jurisdiction clause does not mention ADGM.",
      "severity": "High",
      "suggestion": "Add ADGM jurisdiction clause.",
      "rag_matches": [
        {
          "text": "Article 2 - Jurisdiction: Unless otherwise expressly provided, the Courts of ADGM shall have exclusive jurisdiction...",
          "meta": {"title": "adgm_companies_regulations_2020.txt"}
        }
      ]
    }
  ],
  "reviewed_paths": ["outputs/Articles_of_Association.reviewed.docx"],
  "generated_at": "2025-08-10T12:34:56Z"
}
```

---

## 🛠 Tech Stack

* **Python**
* **Gradio** – web UI
* **python-docx** / **docx2txt** – DOCX parsing
* **sentence-transformers** – embeddings for RAG
* **FAISS** – vector database for retrieval
* **dotenv** – env variables management

---

## ⚠️ Edge Cases Handled

* Non-`.docx` files → rejected at upload.
* Missing documents → listed in JSON report.
* No ADGM mention in jurisdiction → flagged.
* No signature block → flagged.
* Ambiguous “may” usage in binding clauses → flagged.
* No API key needed — works fully offline with local ADGM references.

---

## 📌 Future Improvements

* Add advanced clause compliance checks with GPT/Claude (if API keys are available).
* Support PDF uploads with OCR.
* Multi-process legal checklists.
* Word-native comments (instead of inline text) using XML editing.

---

## 📜 License

MIT License – see [LICENSE](LICENSE) file for details.

---

## 👤 Author

**MANISH KUMAR**

```

---
