# src/document_loader.py
import pypdf
import docx2txt
import io

def extract_text_from_pdf(file_bytes) -> str:
    """Extracts raw text from a PDF binary stream."""
    text = ""
    # Wrap raw bytes in an in-memory file stream
    pdf_file = io.BytesIO(file_bytes)
    reader = pypdf.PdfReader(pdf_file)
    
    # Iterate through every single page and extract text
    for page_num, page in enumerate(reader.pages):
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
            
    return text

def extract_text_from_docx(file_bytes) -> str:
    """Extracts raw text from a DOCX binary stream."""
    docx_file = io.BytesIO(file_bytes)
    # docx2txt handles processing the Word file layout structure automatically
    text = docx2txt.process(docx_file)
    return text

def extract_text_from_txt(file_bytes) -> str:
    """Extracts text from a raw TXT file byte stream."""
    # Decode raw binary bytes into a standard readable UTF-8 string
    return file_bytes.decode("utf-8", errors="ignore")

def process_uploaded_files(uploaded_files) -> dict:
    """
    Processes multiple Streamlit uploaded files.
    Returns a dictionary mapping filename to its clean extracted text.
    """
    all_extracted_text = {}
    
    for uploaded_file in uploaded_files:
        filename = uploaded_file.name
        # Read the raw binary content of the file
        file_bytes = uploaded_file.read()
        
        try:
            if filename.endswith(".pdf"):
                extracted = extract_text_from_pdf(file_bytes)
            elif filename.endswith(".docx"):
                extracted = extract_text_from_docx(file_bytes)
            elif filename.endswith(".txt"):
                extracted = extract_text_from_txt(file_bytes)
            else:
                extracted = ""
                
            all_extracted_text[filename] = extracted
            
        except Exception as e:
            # Simple error catching per file to prevent entire app crash
            all_extracted_text[filename] = f"Error processing file: {str(e)}"
            
    return all_extracted_text