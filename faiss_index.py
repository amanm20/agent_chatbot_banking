# src/utils/faiss_index.py

import os
import pickle
import numpy as np
import faiss
from pathlib import Path
from .bedrock_client import embed_text

# where to write
INDEX_PATH = "data/policies/index.faiss"
DOCS_PATH  = "data/policies/docs.pkl"

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    """
    Split `text` into chunks of up to chunk_size characters,
    with `overlap` characters overlap between chunks.
    """
    chunks = []
    start = 0
    length = len(text)
    while start < length:
        end = min(start + chunk_size, length)
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def build_and_save(policy_dir: str):
    # 1. load single policy file
    policy_path = Path(policy_dir) / "policy.txt"
    if not policy_path.exists():
        raise FileNotFoundError(f"{policy_path} not found")
    text = policy_path.read_text()

    # 2. chunk it
    docs = chunk_text(text, chunk_size=1000, overlap=200)

    # 3. embed each chunk
    embeddings = []
    for chunk in docs:
        emb = embed_text(chunk)
        embeddings.append(np.array(emb, dtype="float32"))

    # stack into matrix
    emb_matrix = np.vstack(embeddings)

    # 4. build FAISS index
    dim = emb_matrix.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(emb_matrix)

    # 5. save index + docs
    faiss.write_index(index, INDEX_PATH)
    with open(DOCS_PATH, "wb") as f:
        pickle.dump(docs, f)
    print(f"Built FAISS index with {len(docs)} chunks")

def load_faiss(policy_dir: str):
    # load index and chunk list
    idx = faiss.read_index(INDEX_PATH)
    with open(DOCS_PATH, "rb") as f:
        docs = pickle.load(f)
    return idx, docs
