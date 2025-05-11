from langchain_community.document_loaders import PyPDFLoader, UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import logging
import shutil

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clear_data_directory(pdf_dir="data"):
    """Clear existing PDFs and create fresh directory"""
    if os.path.exists(pdf_dir):
        shutil.rmtree(pdf_dir)
    os.makedirs(pdf_dir, exist_ok=True)
    return pdf_dir

def save_uploaded_files(uploaded_files, pdf_dir="data"):
    """Save Streamlit uploaded files to disk"""
    os.makedirs(pdf_dir, exist_ok=True)
    saved_files = []
    for file in uploaded_files:
        try:
            file_path = os.path.join(pdf_dir, file.name)
            with open(file_path, "wb") as f:
                f.write(file.getbuffer())
            saved_files.append(file_path)
        except Exception as e:
            logging.error(f"Error saving {file.name}: {str(e)}")
    return saved_files

def load_and_chunk_pdfs(pdf_dir="data", chunk_size=1000, chunk_overlap=200):
    """Process PDFs with enhanced error handling"""
    all_documents = []
    
    if not os.path.exists(pdf_dir) or not os.listdir(pdf_dir):
        logging.warning(f"No PDFs found in {pdf_dir}")
        return []

    for filename in os.listdir(pdf_dir):
        if filename.endswith(".pdf"):
            file_path = os.path.join(pdf_dir, filename)
            try:
                # Try structured extraction first
                loader = PyPDFLoader(file_path)
                docs = loader.load()
                
                # Fallback to unstructured if no content
                if not docs or all(not doc.page_content.strip() for doc in docs):
                    loader = UnstructuredPDFLoader(file_path)
                    docs = loader.load()
                
                all_documents.extend(docs)
                logging.info(f"Processed {filename} successfully")
                
            except Exception as e:
                logging.error(f"Failed to process {filename}: {str(e)}")
                continue

    if not all_documents:
        return []

    # Improved text splitting
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(all_documents)
