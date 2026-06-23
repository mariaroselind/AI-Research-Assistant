# src/text_splitter.py
from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_text_documents(extracted_data: dict, chunk_size: int = 1000, chunk_overlap: int = 200) -> list:
    """
    Takes a dictionary of {filename: raw_text} and splits it into smaller chunks.
    Returns a list of dictionaries, where each dict represents a specific chunk 
    and its source metadata.
    """
    # Initialize the recursive text splitter algorithm
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    
    final_chunks = []
    
    # Process files one by one
    for filename, raw_text in extracted_data.items():
        if not raw_text.strip():
            continue  # Skip empty files
            
        # Split the current document's text into small string pieces
        text_pieces = splitter.split_text(raw_text)
        
        # Structure each piece so we don't lose track of its source file
        for index, piece in enumerate(text_pieces):
            chunk_object = {
                "text": piece,
                "metadata": {
                    "source": filename,
                    "chunk_id": index
                }
            }
            final_chunks.append(chunk_object)
            
    return final_chunks