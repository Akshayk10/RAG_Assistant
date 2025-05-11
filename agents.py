from tools import calculator_tool, dictionary_tool
from vector_store import retrieve_chunks
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

# Load the .env file containing GOOGLE_API_KEY
load_dotenv()

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3)

def rag_llm_answer(chunks, query):
    context = "\n".join([doc.page_content for doc in chunks])
    prompt = f"Context:\n{context}\n\nAnswer this: {query}"
    return llm.invoke(prompt)

def agent_router(query, vector_store):
    query_lower = query.lower()
    
    # Calculator
    if any(tag in query_lower for tag in ["calculate", "compute", "+", "-", "*", "/"]):
        return {
            "tool": "Calculator",
            **calculator_tool(query)  # Unpacks all returned data
        }
        
    # Dictionary
    elif any(tag in query_lower for tag in ["define", "meaning", "what does"]):
        return {
            "tool": "Dictionary",
            **dictionary_tool(query)
        }
        
    # Default RAG flow
    return {
        "tool": "Document Search",
        "answer": agent_router(query, vector_store),
        "snippets": get_context_chunks(query, vector_store)
    }
