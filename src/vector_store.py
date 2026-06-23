# src/vector_store.py
import os
import shutil  # <-- MAKE SURE THIS IS HERE!
from langchain_community.vectorstores import FAISS

DB_DIR = "faiss_index"

def create_vector_store(chunks: list, embedding_model):
    """
    Creates a FAISS database from text chunks and saves it locally to disk.
    """
    texts = [chunk["text"] for chunk in chunks]
    metadatas = [chunk["metadata"] for chunk in chunks]
    
    vector_store = FAISS.from_texts(
        texts=texts,
        embedding=embedding_model,
        metadatas=metadatas
    )
    
    vector_store.save_local(DB_DIR)
    return vector_store

def load_local_vector_store(embedding_model):
    """
    Attempts to load an existing FAISS index from disk if it exists.
    """
    if os.path.exists(DB_DIR):
        return FAISS.load_local(
            folder_path=DB_DIR, 
            embeddings=embedding_model, 
            allow_dangerous_deserialization=True
        )
    return None

def search_top_k_chunks(vector_store, query: str, k: int = 3):
    """
    Searches the FAISS database for the top K most relevant document chunks.
    """
    docs = vector_store.similarity_search(query, k=k)
    return docs

# <-- DOUBLE CHECK THIS IS AT THE VERY BOTTOM OF THE FILE
def delete_local_vector_store():
    """
    Permanently deletes the FAISS index folder from the hard drive.
    """
    if os.path.exists(DB_DIR):
        shutil.rmtree(DB_DIR)