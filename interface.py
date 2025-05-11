__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import os
import streamlit as st
from ingest_documents import load_and_chunk_pdfs, save_uploaded_files
from vector_store import create_vector_store, load_vector_store
from agents import agent_router
from dotenv import load_dotenv

# --- Initialization ---
load_dotenv()  # Load environment variables

# Initialize session state
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = load_vector_store() if os.path.exists("db") else None
if 'docs_processed' not in st.session_state:
    st.session_state.docs_processed = False

# --- Authentication ---
def get_api_key():
    """Safe API key loader for all environments"""
    try:
        return st.secrets["GOOGLE_API_KEY"]  # Streamlit Cloud
    except:
        try:
            return os.getenv("GOOGLE_API_KEY")  # Local .env
        except:
            st.error("""
            API key not found. Please set:
            1. Streamlit Secrets (production)
            2. .env file (local development)
            """)
            st.stop()

# --- Page Config ---
st.set_page_config(page_title="RAG Assistant", layout="wide")
st.title("📘 Document QA Assistant")

# --- Main Function ---
def main():
    # Always show upload section
    with st.sidebar:
        st.header("📤 Document Upload")
        uploaded_files = st.file_uploader(
            "Choose PDF files", 
            type="pdf", 
            accept_multiple_files=True,
            help="Upload one or more PDF documents to process"
        )
        
        if st.button("✨ Process Documents", 
                    disabled=not uploaded_files,
                    help="Extract text and build search index"):
            with st.spinner("Processing files..."):
                try:
                    # Save and process files
                    saved_files = save_uploaded_files(uploaded_files)
                    chunks = load_and_chunk_pdfs()
                    
                    if not chunks:
                        st.error("No text could be extracted from these PDFs")
                        return
                        
                    st.session_state.vector_store = create_vector_store(chunks)
                    st.session_state.docs_processed = True
                    st.success(f"✅ Processed {len(saved_files)} documents!")
                    st.balloons()
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Processing failed: {str(e)}")

    # Show appropriate interface
    if not st.session_state.docs_processed:
        st.warning("Vector store is empty. Please upload and process documents first.")
        st.info("ℹ️ Use the sidebar to upload PDF files and click 'Process Documents'")
    else:
        query = st.chat_input("Ask a question about your documents...")
        if query:
            with st.spinner("Analyzing documents..."):
                try:
                    result = agent_router(query, st.session_state.vector_store)
                    
                    # Display conversation-style results
                    with st.chat_message("user"):
                        st.write(query)
                    
                    with st.chat_message("assistant"):
                        # Answer section
                        st.markdown("#### Answer")
                        st.success(result["answer"])
                        
                        # Context section
                        if "snippets" in result:
                            with st.expander("🔍 View Source Context"):
                                st.markdown("#### Retrieved Contexts")
                                for i, snippet in enumerate(result["snippets"]):
                                    st.markdown(f"**Context {i+1}**")
                                    st.text(snippet[:500] + ("..." if len(snippet) > 500 else ""))
                                    st.divider()
                                    
                        # Tool used
                        st.caption(f"Tool used: {result['tool']}")
                        
                except Exception as e:
                    st.error(f"Error generating answer: {str(e)}")

if __name__ == "__main__":
    main()
