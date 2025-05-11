__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import os
import streamlit as st
from ingest_documents import load_and_chunk_pdfs, save_uploaded_files
from vector_store import create_vector_store, load_vector_store

# Initialize session state
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = None
if 'docs_processed' not in st.session_state:
    st.session_state.docs_processed = False

def initialize_app():
    """Initialize or reload vector store"""
    try:
        st.session_state.vector_store = load_vector_store()
        st.session_state.docs_processed = os.path.exists("db") and len(os.listdir("db")) > 0
    except Exception as e:
        st.error(f"Initialization error: {str(e)}")
        st.session_state.vector_store = None
        st.session_state.docs_processed = False

# Page config
st.set_page_config(page_title="RAG Assistant", layout="wide")
st.title("📘 Document QA Assistant")

# Sidebar for uploads
with st.sidebar:
    st.header("📤 Document Upload")
    uploaded_files = st.file_uploader(
        "Choose PDF files", 
        type="pdf", 
        accept_multiple_files=True,
        key="file_uploader"
    )
    
    if st.button("Process Documents", disabled=not uploaded_files):
        with st.spinner("Processing files..."):
            try:
                # Save uploaded files
                saved_files = save_uploaded_files(uploaded_files)
                if not saved_files:
                    st.error("No files were saved successfully")
                    st.stop()
                
                # Process and create vector store
                chunks = load_and_chunk_pdfs()
                if not chunks:
                    st.error("Failed to extract text from documents")
                    st.stop()
                
                st.session_state.vector_store = create_vector_store(chunks)
                st.session_state.docs_processed = True
                st.success(f"Processed {len(saved_files)} documents!")
                st.rerun()
                
            except Exception as e:
                st.error(f"Processing failed: {str(e)}")

# Main interface
initialize_app()

if not st.session_state.docs_processed:
    st.warning("Vector store is empty. Please upload and process documents first.")
    st.info("Use the sidebar to upload PDF files and click 'Process Documents'")
else:
    query = st.text_input("🔍 Ask a question about your documents")
    if query:
        with st.spinner("Searching documents..."):
            try:
                result = agent_router(query, st.session_state.vector_store)
                st.markdown(f"### 💬 Answer")
                st.success(result["answer"])
                
                if "snippets" in result:
                    with st.expander("📄 Source Excerpts"):
                        for i, snippet in enumerate(result["snippets"]):
                            st.text(f"Source {i+1}:\n{snippet[:500]}...")
            except Exception as e:
                st.error(f"Error generating answer: {str(e)}")
