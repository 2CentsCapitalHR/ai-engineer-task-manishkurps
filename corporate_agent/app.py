import gradio as gr
import os
import shutil
from pathlib import Path
from parser import parse_docx
from classifier import classify_doc_type
from verifier import verify_checklist
from redflag import detect_redflags
from annotator import annotate_docx_simple
from reporter import build_report_and_save
from rag_indexer import SimpleRAGIndexer
from config import OPENAI_API_KEY, OUTPUT_DIR

# helper to save uploaded files from Gradio
def save_uploaded_file(uploaded, dest_folder="uploads"):
    os.makedirs(dest_folder, exist_ok=True)
    # uploaded might be a tempfile with .name or a bytes-like object
    if hasattr(uploaded, "name") and os.path.exists(uploaded.name):
        dest = os.path.join(dest_folder, os.path.basename(uploaded.name))
        shutil.copy(uploaded.name, dest)
        return dest
    else:
        dest = os.path.join(dest_folder, getattr(uploaded, "filename", "uploaded.docx"))
        with open(dest, "wb") as f:
            f.write(uploaded.read())
        return dest

# create/simple RAG retriever instance (if indexed)
rag = SimpleRAGIndexer()
rag.load_index()  # attempt to load pre-built index

def process_files(files, process_choice="Company Incorporation", use_rag=False):
    """
    files: list of uploaded files from Gradio (each is a tempfile-like)
    """
    if not files:
        return None, "No files uploaded."

    saved_paths = []
    parsed_docs = []
    detected_types = []
    for f in files:
        try:
            saved = save_uploaded_file(f)
            saved_paths.append(saved)
            parsed = parse_docx(saved)
            parsed_docs.append(parsed)
            dt = classify_doc_type(parsed)
            detected_types.append(dt)
        except Exception as e:
            return None, f"Error parsing {getattr(f, 'name', getattr(f,'filename', 'file'))}: {e}"

    # verify checklist
    checklist = verify_checklist(process_choice, detected_types)

    # detect red flags per document (optionally with RAG retriever)
    issues_all = []
    reviewed_paths = []
    for parsed in parsed_docs:
        issues = detect_redflags(parsed, use_rag=use_rag, retriever_fn=(lambda q,k: rag.query(q,k) if rag.index else []))
        issues_all.extend(issues)
        reviewed = annotate_docx_simple(parsed["path"], issues)
        reviewed_paths.append(reviewed)

    # build and save report
    json_path, report_data = build_report_and_save(process_choice, saved_paths, checklist, issues_all, reviewed_paths)

    # Prepare output: if single reviewed doc return that and report; if multiple, create a zip
    if len(reviewed_paths) == 1:
        return reviewed_paths[0], json_path
    else:
        zip_path = os.path.join(OUTPUT_DIR, "reviewed_bundle.zip")
        with shutil.ZipFile(zip_path, "w") as zf:
            for rp in reviewed_paths:
                zf.write(rp, arcname=os.path.basename(rp))
            zf.write(json_path, arcname=os.path.basename(json_path))
        return zip_path, json_path

# Build Gradio interface
title = "Corporate Agent — ADGM Document Reviewer (Intermediate Demo)"
description = "Upload one or more .docx documents. The tool will parse, classify, check a checklist for Company Incorporation (default), detect red flags, annotate the files, and return a reviewed .docx and JSON report. Optional: enable RAG after you index ADGM texts."

iface = gr.Interface(
    fn=process_files,
    inputs=[
        gr.Files(label="Upload .docx files", file_count="multiple", file_types=[".docx"]),
        gr.Dropdown(choices=["Company Incorporation"], value="Company Incorporation", label="Process"),
        gr.Checkbox(label="Use RAG (requires indexing ADGM texts in resources/adgm_texts/ and may require models)", value=False)
    ],
    outputs=[gr.File(label="Reviewed .docx or ZIP"), gr.File(label="JSON report")],
    title=title,
    description=description,
    allow_flagging="never"
)

if __name__ == "__main__":
    iface.launch()