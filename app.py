# app.py
import os
import streamlit as st
from dotenv import load_dotenv

# Import our complete pipeline architecture
from src.document_loader import process_uploaded_files
from src.text_splitter import split_text_documents
from src.embeddings import get_embedding_model
from src.vector_store import create_vector_store, search_top_k_chunks
from src.rag_pipeline import generate_llm_answer

load_dotenv()

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🤖",
    layout="wide"
)

# app.py (Modified Configuration Section)
import os
import streamlit as st
from dotenv import load_dotenv

from src.document_loader import process_uploaded_files
from src.text_splitter import split_text_documents
from src.embeddings import get_embedding_model
# NEW: Import load_local_vector_store
from src.vector_store import create_vector_store, search_top_k_chunks, load_local_vector_store

load_dotenv()

st.set_page_config(page_title="AI Research Assistant", page_icon="🤖", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome back! Upload your source materials in the sidebar, compile the dataset, and feel free to ask me anything about their contents."}
    ]

# --- NEW AUTO-LOAD LOGIC FOR PERSISTIST LAYER ---
if "vector_db" not in st.session_state:
    # Get the local embedding engine
    local_embeddings = get_embedding_model()
    # Check if a database folder already exists on the hard drive
    existing_db = load_local_vector_store(local_embeddings)
    
    if existing_db:
        st.session_state.vector_db = existing_db
        # Append a welcome confirmation notice silently
        st.sidebar.success("💾 Found and loaded an existing local knowledge base!")
    else:
        st.session_state.vector_db = None

# app.py (Updated Sidebar Section)
# Add this import at the top of app.py if it's missing:
from src.vector_store import create_vector_store, search_top_k_chunks, load_local_vector_store, delete_local_vector_store

# --- SIDEBAR: CLEAN CONTROL CENTER ---
with st.sidebar:
    st.title("📁 Document Control")
    st.markdown("Upload files to contextually power your conversational agent.")
    
    uploaded_files = st.file_uploader(
        label="Supported formats: PDF, DOCX, TXT",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )
    
    if uploaded_files:
        st.info(f"📎 {len(uploaded_files)} document(s) staged for processing.")
        
        if st.button("Index Knowledge Base", use_container_width=True, type="primary"):
            with st.spinner("Analyzing document semantics..."):
                raw_text_dict = process_uploaded_files(uploaded_files)
                semantic_chunks = split_text_documents(raw_text_dict)
                local_embeddings = get_embedding_model()
                
                st.session_state.vector_db = create_vector_store(semantic_chunks, local_embeddings)
                st.rerun()  # Fresh refresh to lock in states

    # --- NEW: RESET MANAGEMENT INTERFACE ---
    st.markdown("---")
    st.subheader("⚙️ System Management")
    
    if st.session_state.vector_db is not None:
        st.markdown("💡 *An active knowledge base is loaded on your hard drive.*")
        if st.button("🔴 Clear Knowledge Base", use_container_width=True):
            # 1. Wipe out physical folder on disk
            delete_local_vector_store()
            # 2. Reset the session memory variables
            st.session_state.vector_db = None
            st.session_state.messages = [
                {"role": "assistant", "content": "Knowledge base cleared successfully. Ready for new documents!"}
            ]
            # 3. Force Streamlit to instantly redraw the interface blank
            st.rerun()
    else:
        st.caption("No persistent data detected on disk. System is ready for fresh ingestion.")
# --- MAIN CHAT APPLICATION UI ---
st.title("🤖 AI Research Assistant")
st.caption("🚀 RAG-Powered Document Intelligence Platform")
st.markdown("---")

# Display conversational history stream
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User interacting with input string query
if user_query := st.chat_input("Ask a question about your documents..."):
    
    # Render user query instantly
    with st.chat_message("user"):
        st.write(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    # Process core business response pipeline
    with st.chat_message("assistant"):
        if st.session_state.vector_db is not None:
            with st.spinner("Scanning knowledge indexes..."):
                # 1. Fetch top documents matching query semantics
                context_docs = search_top_k_chunks(st.session_state.vector_db, user_query, k=3)
                
                # 2. Synthesize output string via Groq Core
                ai_response = generate_llm_answer(user_query, context_docs)
                
                # 3. Output structural answer to UI
                st.write(ai_response)
                
                # 4. Render references natively inside an isolated collapse container
                with st.expander("🔍 Look inside retrieved source snippets"):
                    for idx, doc in enumerate(context_docs):
                        st.markdown(f"**Reference Source {idx + 1}:** `{doc.metadata['source']}` (Chunk ID: {doc.metadata['chunk_id']})")
                        st.caption(doc.page_content)
                        st.markdown("---")
        else:
            ai_response = "I don't have access to your documentation yet. Please upload and index your research items in the control panel to start."
            st.warning(ai_response)
            
    # Keep response persistent in chat buffer streams
    st.session_state.messages.append({"role": "assistant", "content": ai_response})