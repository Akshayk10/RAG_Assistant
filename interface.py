__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import os
import streamlit as st
from ingest_documents import load_and_chunk_pdfs, save_uploaded_files
from vector_store import create_vector_store, load_vector_store

# Initialize session state
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = load_vector_store() if os.path.exists("db") else None
if 'show_upload' not in st.session_state:
    st.session_state.show_upload = True  # Always show upload option

# Page config
st.set_page_config(page_title="RAG Assistant", layout="wide")
st.title("📘 Document QA Assistant")

# Main function
def main():
    # Always show upload section
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
                    # Save and process files
                    saved_files = save_uploaded_files(uploaded_files)
                    chunks = load_and_chunk_pdfs()
                    st.session_state.vector_store = create_vector_store(chunks)
                    st.success(f"Processed {len(saved_files)} documents!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Processing failed: {str(e)}")

    # Show appropriate message based on state
    if not st.session_state.vector_store:
        st.warning("No documents processed yet. Please upload PDFs using the sidebar.")
    else:
        query = st.text_input("🔍 Ask a question about your documents")
        if query:
            with st.spinner("Searching documents..."):
                result = agent_router(query, st.session_state.vector_store)
                st.markdown("### 💬 Answer")
                st.success(result["answer"])
                
                if "snippets" in result:
                    with st.expander("📄 Source Excerpts"):
                        for i, snippet in enumerate(result["snippets"]):
                            st.text(f"Source {i+1}:\n{snippet[:500]}...")

if __name__ == "__main__":
    main()
