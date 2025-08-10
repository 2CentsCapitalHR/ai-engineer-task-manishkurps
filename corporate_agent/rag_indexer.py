# simple retrieval (sentence-transformers + FAISS)
import os
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

MODEL_NAME = "all-MiniLM-L6-v2"  # small & fast

class SimpleRAGIndexer:
    def __init__(self, model_name=MODEL_NAME, index_dir="outputs/rag_index"):
        self.model = SentenceTransformer(model_name)
        self.index_dir = index_dir
        os.makedirs(index_dir, exist_ok=True)
        self.index_path = os.path.join(index_dir, "faiss.index")
        self.meta_path = os.path.join(index_dir, "meta.pkl")
        self.index = None
        self.metadatas = []  # list of dicts {'text':..., 'meta': {...}}

    def index_texts(self, texts_with_meta):
        """
        texts_with_meta: list of { 'text': str, 'meta': { 'title':..., 'source':... } }
        """
        texts = [t["text"] for t in texts_with_meta]
        embeddings = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
        # normalize for cosine similarity
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        embeddings = embeddings / (norms + 1e-9)
        d = embeddings.shape[1]
        index = faiss.IndexFlatIP(d)  # inner product = cosine on normalized vectors
        index.add(embeddings)
        faiss.write_index(index, self.index_path)
        with open(self.meta_path, "wb") as f:
            pickle.dump(texts_with_meta, f)
        self.index = index
        self.metadatas = texts_with_meta

    def load_index(self):
        if os.path.exists(self.index_path) and os.path.exists(self.meta_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.meta_path, "rb") as f:
                self.metadatas = pickle.load(f)
            return True
        return False

    def query(self, q, k=3):
        if self.index is None:
            loaded = self.load_index()
            if not loaded:
                return []
        q_emb = self.model.encode([q], convert_to_numpy=True)
        q_emb = q_emb / (np.linalg.norm(q_emb, axis=1, keepdims=True) + 1e-9)
        D, I = self.index.search(q_emb, k)
        results = []
        for idx in I[0]:
            if idx < len(self.metadatas):
                results.append({
                    "text": self.metadatas[idx]["text"],
                    "meta": self.metadatas[idx].get("meta", {})
                })
        return results

def index_text_files_from_folder(folder="resources/adgm_texts", out_index_dir="outputs/rag_index"):
    indexer = SimpleRAGIndexer(index_dir=out_index_dir)
    docs = []
    for filename in os.listdir(folder):
        if filename.lower().endswith(".txt"):
            path = os.path.join(folder, filename)
            with open(path, "r", encoding="utf-8") as f:
                txt = f.read()
            docs.append({"text": txt[:10000], "meta": {"title": filename, "source": path}})
    if not docs:
        print("No .txt files found in", folder)
        return False
    indexer.index_texts(docs)
    print("Indexed", len(docs), "documents.")
    return True

# simple usage:
# index_text_files_from_folder()
# rag = SimpleRAGIndexer()
# rag.load_index()
# rag.query("What does ADGM say about jurisdiction clause?", k=3)
