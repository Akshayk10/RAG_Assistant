from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv

def get_api_key():
    """Get API key from safest available source"""
    try:
        # 1. Try Streamlit secrets (production)
        import streamlit as st
        return st.secrets["GOOGLE_API_KEY"]
    except:
        try:
            # 2. Try environment variable (local/dev)
            api_key = os.environ.get("GOOGLE_API_KEY")
            if not api_key:
                # 3. Try loading from .env file
                load_dotenv()
                api_key = os.environ.get("GOOGLE_API_KEY")
            
            if not api_key:
                raise ValueError("GOOGLE_API_KEY not found in environment variables or .env file")
            return api_key
        except ImportError:
            # Not in a Streamlit context, just try env vars
            load_dotenv()
            api_key = os.environ.get("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY not found in environment variables or .env file")
            return api_key

def initialize_vector_store():
    """Ensure vector store exists or create empty one"""
    if not os.path.exists("db"):
        os.makedirs("db", exist_ok=True)
        # Initialize empty vector store
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=get_api_key()
        )
        return Chroma(persist_directory="db", embedding_function=embeddings)
    return load_vector_store()

def create_vector_store(chunks, persist_directory="db"):
    """Create a new vector store from documents"""
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=get_api_key()
    )
    
    # Create vector store with persist_directory
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    # Data is automatically persisted when using persist_directory
    return vector_store

def load_vector_store(persist_directory="db"):
    """Load an existing vector store"""
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=get_api_key()
    )
    return Chroma(persist_directory=persist_directory, embedding_function=embeddings)

def retrieve_chunks(query, vector_store, k=3):
    """Retrieve similar chunks from the vector store"""
    return vector_store.similarity_search(query, k=k)
