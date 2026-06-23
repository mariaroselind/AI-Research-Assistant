# src/embeddings.py
from langchain_community.embeddings import HuggingFaceEmbeddings

def get_embedding_model():
    """
    Initializes and returns the HuggingFace embedding model.
    Using the community module to maximize cross-platform cloud stability.
    """
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return embedding_model