# 🤖 RAG-Powered AI Research Assistant

A production-grade, local-first Retrieval-Augmented Generation (RAG) platform that allows users to upload complex research papers (PDF, DOCX, TXT), index them semantically, and interview their documents using high-speed open-source LLMs.

---

## 💡 Key Features
- **Multi-Format Ingestion:** Dynamic binary processing of PDF, DOCX, and plain text files.
- **Semantic Window Segmentation:** Recursive character text splitting with overlapping safety buffers to maintain context.
- **Zero-Cost Local Embeddings:** Utilizes HuggingFace `all-MiniLM-L6-v2` to compute 384-dimensional text vectors locally.
- **Persistent Vector Indexes:** Built-in hard drive caching using Meta's FAISS library to avoid redundant file processing across app reboots.
- **Blazing Fast Analytics:** Integrated with Groq Cloud running `Llama 3.1` for near-instant contextual responses.
- **Production UI:** Sleek Streamlit dashboard featuring live citation/source reference expanding menus and an instant knowledge base database wipe control.

---

## 🛠️ System Architecture

1. **Document Loading:** Files are uploaded via the Streamlit interface and parsed into memory.
2. **Chunking:** Documents are split into 1,000-character chunks with a 200-character overlap.
3. **Embedding & Indexing:** Chunks are converted to vectors and stored in a local FAISS database.
4. **Retrieval:** When a user asks a question, the top 3 most relevant chunks are fetched via similarity search.
5. **Generation:** The context chunks and user question are passed securely to the Llama 3.1 model via Groq API to synthesize a highly accurate answer.

---

## ⚙️ Local Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/mariaroselind/AI-Research-Assistant.git](https://github.com/mariaroselind/AI-Research-Assistant.git)
   cd AI-Research-Assistant
