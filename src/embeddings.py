# src/embeddings.py
from langchain_huggingface import HuggingFaceEmbeddings

def get_embedding_model():
    """
    Initializes and returns a completely free, local HuggingFace embedding engine.
    This runs entirely on your own computer without needing an API key or internet!
    """
    # This model runs lightweight and fast on local CPUs
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    return embeddings