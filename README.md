# 🧠 Multi-Agent FAQ Assistant with RAG

[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ragassistant-hpgwit2q5qxyktmfvryask.streamlit.app/)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)

A smart document assistant that combines Retrieval-Augmented Generation (RAG) with specialized tools (Calculator & Dictionary) for context-aware and intelligent question answering.

---

## 🚀 Features

- 📘 **Document Intelligence**: Ask questions from your uploaded PDFs
- 🛠️ **Multi-Tool Integration**: Built-in calculator and dictionary for factual and mathematical queries
- 💾 **Persistent Knowledge Base**: Retains your processed data between sessions
- 🔐 **Secure Deployment**: Compatible with local development and cloud deployment using secrets

---

## 🏗️ Architecture

```mermaid
graph TD
    A[Streamlit UI] --> B[Agent Router]
    B --> C{Route Query}
    C -->|Calculation| D[Calculator Tool]
    C -->|Definition| E[Dictionary Tool]
    C -->|General| F[RAG Pipeline]
    F --> G[Vector Store]
    G --> H[LLM Generation]
