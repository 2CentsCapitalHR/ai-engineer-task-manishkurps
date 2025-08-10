# 🏛 Corporate Agent – ADGM Document Reviewer

An AI-powered assistant to **validate, verify, and check compliance** of `.docx` legal documents for **Abu Dhabi Global Market (ADGM)** processes.

---

## ✨ Features
- Upload `.docx` files via a simple **Gradio** web app.
- Classifies documents (AoA, MoA, UBO, etc.).
- Verifies required documents for a process (e.g., Company Incorporation).
- Detects red flags (missing jurisdiction, signatures, ambiguity).
- **Local RAG**: retrieves relevant ADGM law excerpts (no API key needed).
- Annotates reviewed `.docx` with comments + generates JSON report.

---

## 🚀 Quick Start
```bash
git clone https://github.com/2CentsCapitalHR/ai-engineer-task-manishkurps.git
cd corporate_agent
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
````

Place ADGM `.txt` references in:

```
resources/adgm_texts/
```

Index them:

```bash
python - <<'PY'
from rag_indexer import index_text_files_from_folder
index_text_files_from_folder("resources/adgm_texts", "outputs/rag_index")
PY
```

Run the app:

```bash
python app.py
```

Open the browser link, upload `.docx`, and get results.

---

## 📜 Output

* **Reviewed .docx** with highlights and comments.
* **JSON report** summarizing issues, missing docs, and ADGM references.

---

## 🛠 Tech

Python, Gradio, python-docx, docx2txt, sentence-transformers, FAISS.

```
