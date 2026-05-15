import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


def build_vector_store(sent_emails):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(sent_emails)
    embeddings = np.array(embeddings).astype("float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    return model, index


def retrieve_relevant_examples(
    cleaned_email,
    embedding_model,
    index,
    sent_emails,
    k=3
):
    query_embedding = embedding_model.encode([cleaned_email])
    query_embedding = np.array(query_embedding).astype("float32")

    _, indices = index.search(query_embedding, k)
    return "\n\n".join([sent_emails[i] for i in indices[0]])
