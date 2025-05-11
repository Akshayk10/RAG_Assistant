**import**('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import os
import streamlit as st
from agents import agent_router
from vector_store import load_vector_store, create_vector_store
from ingest_documents import load_and_chunk_pdfs
from dotenv import load_dotenv
# --- Configuration ---
st.set_page_config(page_title="Multi-Agent FAQ Assistant", layout="wide")
load_dotenv()  # Load .env file if exists
# --- Authentication ---
def get_api_key():
    """Get API key from safest available source"""
    try:
        # 1. Try Streamlit secrets (production)
        return st.secrets["GOOGLE_API_KEY"]
    except:
        try:
            # 2. Try environment variable (local/dev)
            return os.environ["GOOGLE_API_KEY"]
        except:
            st.error("""
            Missing Google API Key. Please:
            1. For local use: Create .env file with GOOGLE_API_KEY
            2. For deployment: Set in Streamlit Secrets
            """)
            st.stop()
# --- Vector Store Initialization ---
def initialize_app():
    """Handle vector store setup"""
    try:
        vector_store = load_vector_store()
        if len(vector_store.get()['ids']) == 0:
            st.error("Vector store is empty. Please upload documents first.")
            st.stop()
        return vector_store
    except Exception as e:
        st.error(f"Initialization error: {str(e)}")
        st.stop()
# --- Main App ---
vector_store = initialize_app()
api_key = get_api_key()  # Validates auth
st.title("📘 Multi-Agent FAQ Assistant")
# Document Upload (Simplified)
with st.sidebar:
    st.header("Upload Documents")
    uploaded_files = st.file_uploader(
        "Choose PDF files", 
        type="pdf", 
        accept_multiple_files=True
    )
    
    if uploaded_files and st.button("Process Files"):
        os.makedirs("data", exist_ok=True)
        for file in uploaded_files:
            with open(f"data/{file.name}", "wb") as f:
                f.write(file.getbuffer())
        
        with st.spinner("Creating vector store..."):
            chunks = load_and_chunk_pdfs()
            create_vector_store(chunks)  # This should recreate the DB
        st.rerun()
# Query Interface (Original Format)
query = st.text_input("🔍 Ask a question")
if query:
    with st.spinner("Thinking..."):
        result = agent_router(query, vector_store)
    
    st.markdown(f"### 🔧 Tool Used: `{result['tool']}`")
    
    if "snippets" in result:
        st.markdown("### 📚 Retrieved Context:")
        for i, snippet in enumerate(result["snippets"]):
            st.write(f"**Snippet {i+1}:** {snippet[:400]}...")
    
    st.markdown("### 💬 Answer:")
    st.success(result["answer"])
