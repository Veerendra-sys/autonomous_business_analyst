# synthesizer/embedding_store.py
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_texts(texts):
    """Return embeddings as torch tensors."""
    return model.encode(texts, convert_to_tensor=True)

def top_k_similar(query, corpus_texts, corpus_embeddings, k=3):
    q_emb = model.encode(query, convert_to_tensor=True)
    cos_scores = util.cos_sim(q_emb, corpus_embeddings)[0]
    hits = sorted(range(len(cos_scores)), key=lambda i: cos_scores[i], reverse=True)[:k]
    return hits, [float(cos_scores[i]) for i in hits]
