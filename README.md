# 🧠 Personal RAG Workspace

> Your private, isolated AI-powered knowledge workspace. Upload knowledge, compute 384-dimensional vector embeddings, and retrieve information using semantic similarity.

Built with **Python**, **Streamlit**, **SQLite**, **ChromaDB**, **Sentence Transformers**, and a **Vercel / Linear-inspired dark UI/UX**.

---

## ✨ Features

- **🔐 SQLite Account System**: Registration & authentication with PBKDF2 password hashing (`users.db`).
- **🔒 Isolated Vector Databases**: Dedicated ChromaDB storage directory for every registered user (`./chroma_data/user_<id>_<email>/`).
- **📥 Content Ingestion & Chunking**: Upload files (`PDF`, `TXT`, `DOCX`) or paste text with configurable word chunking & overlap.
- **⚡ Semantic Search**: Perplexity-inspired query bar with match score percentage indicators (`96% MATCH`) and cosine similarity ranking.
- **💬 RAG Explorer**: Context explorer showing cited sources per retrieval prompt.
- **📦 Vector Database Inspector**: Inspect raw vector slices (384 dimensions) and document metadata schemas.
- **🎨 Linear & Vercel Design System**: Dark theme, Inter typography, 8px grid system, and micro-interactions.

---

## 🛠️ Architecture & Folder Structure

```
Personal-RAG-Learning-Lab/
├── app.py                 # Main router & state manager
├── auth.py                # SQLite authentication database
├── rag_engine.py          # ChromaDB vector engine & sentence-transformers
├── users.db               # SQLite user database
├── styles/
│   └── main.css           # Vercel/Linear CSS design system
├── components/
│   ├── sidebar.py         # 240px fixed navigation sidebar & user profile
│   ├── header.py          # Breadcrumb header & online status badge
│   ├── metrics.py         # Neutral metric cards
│   ├── search_results.py  # Linear issue-style match score cards
│   ├── upload_zone.py     # Ingestion dropzone
│   └── empty_states.py    # Empty state components
├── pages/
│   ├── overview.py        # Landing hero & timeline
│   ├── knowledge.py       # Add Knowledge ingestion workflow
│   ├── documents.py       # Knowledge Library document manager
│   ├── search.py          # Semantic search hero experience
│   ├── assistant.py       # AI Knowledge Assistant & cited sources
│   ├── database.py        # Vector database inspector & danger zone modal
│   ├── pipeline.py        # Architecture pipeline visualization
│   └── settings.py        # Workspace preferences & system info
└── utils/
    ├── constants.py       # Color tokens & page names
    ├── helpers.py         # Strings, timestamps & user initials
    └── formatters.py      # Vector & similarity formatters
```

---

## 🚀 Local Setup & Installation

1. **Activate Virtual Environment**:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

2. **Install Dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

3. **Run Application**:
   ```powershell
   python -m streamlit run app.py
   ```
