# Multi-Agent FAQ Assistant with RAG

[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-streamlit-app-url.streamlit.app/)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)

A smart document assistant that combines Retrieval-Augmented Generation (RAG) with specialized tools for comprehensive question answering.

## Features

- **Document Intelligence**: Answers questions from uploaded PDFs
- **Multi-Tool Integration**: Built-in calculator and dictionary
- **Persistent Knowledge Base**: Maintains vector store between sessions
- **Secure Deployment**: Supports both local and cloud configurations

## Architecture

```mermaid
graph TD
    A[Streamlit UI] --> B[Agent Router]
    B --> C{Route Query}
    C -->|Calculation| D[Calculator Tool]
    C -->|Definition| E[Dictionary Tool]
    C -->|General| F[RAG Pipeline]
    F --> G[Vector Store]
    G --> H[LLM Generation]


### Key Sections Included:

1. **Badges**: For quick visibility of deployment status
2. **Visual Architecture**: Mermaid diagram showing component relationships
3. **Step-by-Step Setup**: Clean installation instructions
4. **Usage Examples**: With both local and cloud deployment
5. **Troubleshooting Table**: Common issues and solutions
6. **Contributing Guidelines**: Standard GitHub workflow
7. **License Info**: MIT license notice

### How to Add This to Your Project:

1. Create a new file named `README.md` in your project root
2. Paste this content
3. Replace placeholder values (yourusername, API key instructions, etc.)
4. Commit to your repository:
   ```bash
   git add README.md
   git commit -m "Add comprehensive README"
   git push origin main
