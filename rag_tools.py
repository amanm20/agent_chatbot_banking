from .bedrock_client import generate_text, embed_text
from .utils.faiss_index import load_faiss

INDEX, DOCS = load_faiss("data/policies")

def retrieve_policy(query: str, k: int = 3) -> str:
    q_emb = embed_text(query)
    D, I = INDEX.search([q_emb], k)
    excerpts = [DOCS[i] for i in I[0]]
    prompt = (
        "You are a banking assistant. Use ONLY these excerpts:\n\n"
        + "\n---\n".join(excerpts)
        + f"\n\nQuestion: {query}\nAnswer:"
    )
    return generate_text(prompt)
