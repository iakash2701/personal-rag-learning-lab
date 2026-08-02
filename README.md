# 🧠 Personal RAG Learning Lab

A modern, premium interactive dashboard for learning and experimenting with Retrieval-Augmented Generation (RAG) concepts. Built with Python, Streamlit, ChromaDB, and Sentence Transformers.

## ✨ Features
* **Add Information**: Input your documents/notes, clean text automatically, chunk dynamically (with custom size/overlap), and generate vector embeddings.
* **Semantic Similarity Search**: Ask questions and retrieve the most relevant context chunks ranked by Cosine Similarity.
* **Chroma Vector Database Explorer**: Inspect raw records, IDs, metadata schemas, and dimensions, or clear the database to start over.
* **Visualized Pipeline**: Interactive schema explaining the text-to-embedding-to-retrieval pipeline.

## 🛠️ Tech Stack
* **Frontend**: Streamlit (custom glassmorphic theme)
* **Vector Store**: ChromaDB
* **Embeddings**: Sentence Transformers (`all-MiniLM-L6-v2`)
* **Language**: Python

## 🚀 Local Setup

1. **Activate the Virtual Environment**:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

2. **Run the Streamlit application**:
   ```powershell
   python -m streamlit run app.py
   ```
