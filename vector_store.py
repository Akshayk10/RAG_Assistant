__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
import streamlit as st
from dotenv import load_dotenv

def get_api_key():
    """Safe API key loader for all environments"""
    try:
        # 1. Try Streamlit secrets (production)
        return st.secrets["GOOGLE_API_KEY"]
    except:
        try:
            # 2. Try environment variable (local/dev)
            load_dotenv()
            return os.getenv("GOOGLE_API_KEY")
        except:
            raise ValueError(
                "API key not found. Set GOOGLE_API_KEY in:\n"
                "1. Streamlit Secrets (production)\n"
                "2. .env file (local development)"
            )

def initialize_empty_vector_store(persist_directory="db"):
    """Create empty vector store if none exists"""
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=get_api_key()
    )
    os.makedirs(persist_directory, exist_ok=True)
    return Chroma(persist_directory=persist_directory, embedding_function=embeddings)

def create_vector_store(chunks, persist_directory="db"):
    """Create and persist vector store from documents"""
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=get_api_key()
    )
    
    # Clear existing data if needed
    if os.path.exists(persist_directory):
        for f in os.listdir(persist_directory):
            os.remove(os.path.join(persist_directory, f))
    
    return Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )

def load_vector_store(persist_directory="db"):
    """Load existing vector store with validation"""
    if not os.path.exists(persist_directory) or not os.listdir(persist_directory):
        return initialize_empty_vector_store(persist_directory)
        
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=get_api_key()
    )
    
    try:
        return Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings
        )
    except Exception as e:
        st.error(f"Failed loading vector store: {str(e)}")
        return initialize_empty_vector_store(persist_directory)

def retrieve_chunks(query, vector_store, k=3):
    """Safe document retrieval with error handling"""
    try:
        return vector_store.similarity_search(query, k=k)
    except Exception as e:
        st.error(f"Search failed: {str(e)}")
        return []
