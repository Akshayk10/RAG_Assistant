from tools import calculator_tool, dictionary_tool
from vector_store import retrieve_chunks
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3)

def rag_llm_answer(chunks, query):
    context = "\n".join([doc.page_content for doc in chunks])
    prompt = f"Context:\n{context}\n\nAnswer this: {query}"
    return llm.invoke(prompt).content  # Added .content to get clean string

def agent_router(query, vector_store):
    query_lower = query.lower()
    
    # Calculator
    if any(tag in query_lower for tag in ["calculate", "compute", "+", "-", "*", "/"]):
        tool_result = calculator_tool(query)
        return {
            "tool": "Calculator",
            "answer": tool_result.get("formatted", str(tool_result)),
            "details": tool_result
        }
        
    # Dictionary
    elif any(tag in query_lower for tag in ["define", "meaning", "what does"]):
        tool_result = dictionary_tool(query)
        return {
            "tool": "Dictionary",
            "answer": tool_result.get("formatted", str(tool_result)),
            "details": tool_result
        }
        
    # Document Search
    chunks = retrieve_chunks(query, vector_store)
    answer = rag_llm_answer(chunks, query)
    return {
        "tool": "Document Search",
        "answer": answer,
        "snippets": [doc.page_content for doc in chunks]
    }
