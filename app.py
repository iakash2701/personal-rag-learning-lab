from __future__ import annotations

import re
import pandas as pd
import streamlit as st

import auth
from rag_engine import PersonalRAG

st.set_page_config(
    page_title="Personal RAG Learning Lab",
    page_icon="🧠",
    layout="wide",
)

auth.init_auth_state()

# Modern CSS Styling for UI/UX
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: #090d16 !important;
    }
    
    /* Main Gradient Titles */
    h1 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #818cf8 0%, #c084fc 50%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.02em;
    }
    h2, h3, h4 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        color: #f8fafc !important;
    }
    
    /* Glassmorphic Container Cards */
    .glass-card {
        background: rgba(15, 23, 42, 0.65);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(0, 0, 0, 0.3);
    }
    
    /* Login Card Specific */
    .login-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    .login-icon {
        font-size: 3rem;
        margin-bottom: 0.5rem;
        display: inline-block;
        background: rgba(99, 102, 241, 0.15);
        padding: 1rem;
        border-radius: 20px;
        border: 1px solid rgba(99, 102, 241, 0.3);
    }
    
    /* Input Field Styling */
    .stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] {
        background-color: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 10px !important;
        color: #f8fafc !important;
        padding: 0.75rem 1rem !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #818cf8 !important;
        box-shadow: 0 0 0 2px rgba(129, 140, 248, 0.25) !important;
    }
    
    /* Metric Cards */
    div[data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.4) !important;
        padding: 1.25rem !important;
        border-radius: 14px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        transition: transform 0.2s ease !important;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px) !important;
        border-color: rgba(129, 140, 248, 0.3) !important;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 800 !important;
        color: #818cf8 !important;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
        color: #94a3b8 !important;
        font-weight: 600 !important;
    }
    
    /* Modern Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;
        background-color: rgba(15, 23, 42, 0.8) !important;
        padding: 8px !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    .stTabs [data-baseweb="tab"] {
        height: 44px !important;
        background-color: transparent !important;
        border-radius: 8px !important;
        color: #94a3b8 !important;
        font-weight: 600 !important;
        padding: 0 24px !important;
        transition: all 0.2s ease !important;
        border: none !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #f8fafc !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35) !important;
    }
    .stTabs [data-baseweb="tab-highlight-container"] {
        display: none !important;
    }
    
    /* Primary Action Buttons */
    div.stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 1.75rem !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 14px 0 rgba(99, 102, 241, 0.35) !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px 0 rgba(99, 102, 241, 0.5) !important;
        background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%) !important;
    }
    
    /* Sidebar Profile Card */
    .user-profile-card {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .user-avatar {
        width: 42px;
        height: 42px;
        border-radius: 50%;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        color: white;
        font-size: 1.1rem;
    }
    .user-details {
        overflow: hidden;
    }
    .user-name {
        font-weight: 700;
        color: #f8fafc;
        font-size: 0.95rem;
        line-height: 1.2;
    }
    .user-email {
        color: #94a3b8;
        font-size: 0.78rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------
# AUTHENTICATION GATE
# -------------------------------------------------
if not st.session_state["authenticated"]:
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown(
            """
            <div class="login-header">
                <div class="login-icon">🧠</div>
                <h1>Personal RAG Lab</h1>
                <p style="color: #94a3b8; font-size: 0.95rem; margin-top: 0.2rem;">
                    Secure, Isolated AI-Powered Retrieval-Augmented Generation
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        auth_tab1, auth_tab2 = st.tabs(["🔑 Sign In", "📝 Create Account"])

        with auth_tab1:
            st.markdown("#### Log in to your account")
            email_or_user_input = st.text_input(
                "Email Address or Username", key="login_email"
            )
            password_input = st.text_input(
                "Password", type="password", key="login_pass"
            )

            if st.button("Sign In", type="primary", use_container_width=True):
                success, msg = auth.login(email_or_user_input, password_input)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

        with auth_tab2:
            st.markdown("#### Register a new account")
            reg_email = st.text_input("Email Address", key="reg_email")
            reg_username = st.text_input("Full Name", key="reg_user")
            reg_password = st.text_input(
                "Choose Password", type="password", key="reg_pass"
            )
            confirm_password = st.text_input(
                "Confirm Password", type="password", key="reg_pass_confirm"
            )

            if st.button("Create Account", use_container_width=True):
                if reg_password != confirm_password:
                    st.error("Passwords do not match!")
                else:
                    success, msg = auth.register_user(
                        reg_email, reg_username, reg_password
                    )
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)

    st.stop()


# -------------------------------------------------
# AUTHENTICATED USER SESSION
# -------------------------------------------------
@st.cache_resource
def load_user_rag_system(user_id: int, email: str) -> PersonalRAG:
    """Load isolated vector database instance per logged-in user."""
    safe_email = re.sub(r"[^a-zA-Z0-9_-]", "_", email.lower())
    user_db_path = f"./chroma_data/user_{user_id}_{safe_email}"
    collection_name = f"rag_user_{user_id}"
    return PersonalRAG(
        database_path=user_db_path,
        collection_name=collection_name,
    )


user_info = st.session_state.get("user_info")
if user_info is None:
    st.stop()

rag = load_user_rag_system(user_info["id"], user_info["email"])

# Sidebar Layout
with st.sidebar:
    st.markdown("### 🧠 RAG Learning Lab")

    initials = (
        user_info["username"][:2].upper() if user_info["username"] else "U"
    )
    st.markdown(
        f"""
        <div class="user-profile-card">
            <div class="user-avatar">{initials}</div>
            <div class="user-details">
                <div class="user-name">{user_info['username']}</div>
                <div class="user-email">{user_info['email']}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("🚪 Sign Out", use_container_width=True):
        auth.logout()
        st.rerun()

    st.markdown("---")
    st.metric(
        label="Isolated Chunks in DB",
        value=rag.database_count(),
    )
    st.markdown("---")
    st.markdown(
        """
        #### ⚙️ Features
        1. **Add Information**: Input notes, chunk text, generate vector embeddings.
        2. **Semantic Search**: Retrieve context chunks by cosine similarity.
        3. **Vector DB Explorer**: Inspect raw vectors and metadata schemas.
        4. **Pipeline Diagram**: Understand the full RAG workflow.
        """
    )
    st.markdown("---")
    st.markdown(
        """
        <div style="font-size: 0.8rem; color: #64748b; text-align: center;">
            Personal RAG Learning Lab v1.2.0
        </div>
        """,
        unsafe_allow_html=True,
    )

# Dashboard Main Header
st.title("🧠 Personal RAG Learning Lab")

st.markdown(
    f"""
    <div style='margin-bottom: 1.5rem; display: flex; align-items: center; justify-content: space-between;'>
        <span style='color: #94a3b8;'>
            Store facts, convert to vectors in ChromaDB, and query using semantic similarity.
        </span>
        <span style='background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.3); color: #34d399; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600;'>
            🟢 Isolated DB Active
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "1. Add Information",
        "2. Search",
        "3. Vector Database",
        "4. How It Works",
    ]
)


# -------------------------------------------------
# TAB 1: ADD INFORMATION
# -------------------------------------------------
with tab1:
    st.header("Add information to your database")

    title = st.text_input(
        "Title",
        placeholder="Example: Predictive Maintenance Project Notes",
    )

    category = st.selectbox(
        "Category",
        [
            "Profile",
            "Education",
            "Skills",
            "Project",
            "Achievement",
            "Experience",
            "Certification",
            "Study Notes",
            "General",
        ],
    )

    information = st.text_area(
        "Enter text content",
        height=220,
        placeholder=(
            "Example:\n"
            "I developed a predictive maintenance system using "
            "Random Forest and Isolation Forest to detect machine faults..."
        ),
    )

    col1, col2 = st.columns(2)

    with col1:
        chunk_size = st.slider(
            "Chunk size (words)",
            min_value=30,
            max_value=300,
            value=100,
            step=10,
        )

    with col2:
        overlap = st.slider(
            "Chunk overlap (words)",
            min_value=0,
            max_value=50,
            value=20,
            step=5,
        )

    if st.button(
        "Generate Embeddings & Save to DB",
        type="primary",
        use_container_width=True,
    ):
        try:
            result = rag.store_text(
                text=information,
                title=title or "Untitled information",
                category=category,
                chunk_size=chunk_size,
                overlap=overlap,
            )

            st.success(
                f"Successfully stored {len(result['chunks'])} chunk(s) in your isolated database."
            )

            st.subheader("Generated Chunks & Embeddings")

            for index, chunk in enumerate(result["chunks"]):
                with st.expander(
                    f"📦 Chunk {index + 1}",
                    expanded=True,
                ):
                    st.write(chunk)

                    embedding = result["embeddings"][index]

                    st.write(f"**Embedding Dimension**: `{len(embedding)}`")
                    st.write("**First 20 Embedding Values:**")
                    st.code(
                        str(
                            [
                                round(float(value), 6)
                                for value in embedding[:20]
                            ]
                        )
                    )

                    with st.expander("View Complete Vector Embedding"):
                        st.write(embedding.tolist())

        except ValueError as error:
            st.error(str(error))

        except Exception as error:
            st.exception(error)


# -------------------------------------------------
# TAB 2: SEARCH
# -------------------------------------------------
with tab2:
    st.header("Semantic similarity search")

    question = st.text_input(
        "Ask a question about your stored information",
        placeholder="Example: Which project uses anomaly detection?",
    )

    top_k = st.slider(
        "Number of matching chunks to retrieve",
        min_value=1,
        max_value=10,
        value=3,
    )

    if st.button(
        "Run Semantic Search",
        type="primary",
        use_container_width=True,
    ):
        try:
            result = rag.search(
                question=question,
                number_of_results=top_k,
            )

            st.subheader("Query")
            st.info(result["question"])

            st.subheader("Query Vector Embedding")
            query_embedding = result["query_embedding"]
            st.write(f"**Embedding Dimension**: `{len(query_embedding)}`")
            st.write("**First 20 Vector Values:**")
            st.code(
                str(
                    [
                        round(float(value), 6)
                        for value in query_embedding[:20]
                    ]
                )
            )

            with st.expander("View Complete Query Vector"):
                st.write(query_embedding.tolist())

            st.subheader("Similarity Search Results")

            similarity_table = []
            for position, match in enumerate(result["matches"], start=1):
                metadata = match["metadata"]
                similarity_table.append(
                    {
                        "Rank": position,
                        "Title": metadata.get("title", "Unknown"),
                        "Category": metadata.get("category", "Unknown"),
                        "Chunk": metadata.get("chunk_number", "Unknown"),
                        "Cosine Similarity": round(
                            match["cosine_similarity"], 4
                        ),
                        "Database Distance": round(
                            match["database_distance"], 4
                        ),
                    }
                )

            st.dataframe(
                pd.DataFrame(similarity_table),
                use_container_width=True,
                hide_index=True,
            )

            for position, match in enumerate(result["matches"], start=1):
                similarity = match["cosine_similarity"]
                metadata = match["metadata"]

                if similarity >= 0.7:
                    badge_color = "#10b981"
                elif similarity >= 0.4:
                    badge_color = "#f59e0b"
                else:
                    badge_color = "#ef4444"

                with st.expander(
                    f"Result #{position} — Cosine Similarity: {similarity:.4f}",
                    expanded=(position == 1),
                ):
                    st.markdown(
                        f"""
                        <div style='margin-bottom: 0.8rem; display: flex; align-items: center; gap: 8px;'>
                            <span style='background: {badge_color}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 700;'>
                                {metadata.get("category", "General").upper()}
                            </span>
                            <span style='color: #94a3b8; font-size: 0.85rem;'>
                                Document: <b>{metadata.get("title", "Untitled")}</b> (Chunk {metadata.get("chunk_number", 1)}/{metadata.get("total_chunks", 1)})
                            </span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f"""
                        <div style='background: rgba(255, 255, 255, 0.02); padding: 14px; border-radius: 8px; border-left: 3px solid #818cf8; margin-bottom: 8px; line-height: 1.6; color: #cbd5e1;'>
                            {match["text"]}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            st.subheader("Retrieved Context Window")
            st.text_area(
                "This aggregated context block is supplied to the LLM for answer generation",
                value=result["context"],
                height=220,
                disabled=True,
            )

        except ValueError as error:
            st.error(str(error))
        except Exception as error:
            st.exception(error)


# -------------------------------------------------
# TAB 3: DATABASE EXPLORER
# -------------------------------------------------
with tab3:
    st.header("Vector database inspector")

    st.write(
        f"Total stored chunks in your isolated database: **{rag.database_count()}**"
    )

    if st.button("Refresh Database Records"):
        st.rerun()

    if rag.database_count() > 0:
        records = rag.get_all_records()
        table_rows = []

        for index, record_id in enumerate(records["ids"]):
            document = records["documents"][index]
            metadata = records["metadatas"][index]
            embedding = records["embeddings"][index]

            table_rows.append(
                {
                    "ID": record_id,
                    "Title": metadata.get("title"),
                    "Category": metadata.get("category"),
                    "Chunk": metadata.get("chunk_number"),
                    "Word Count": len(document.split()),
                    "Embedding Dimension": len(embedding),
                }
            )

        st.dataframe(
            pd.DataFrame(table_rows),
            use_container_width=True,
            hide_index=True,
        )

        st.subheader("Inspect Record Detail")

        for index, record_id in enumerate(records["ids"]):
            metadata = records["metadatas"][index]
            document = records["documents"][index]
            embedding = records["embeddings"][index]

            title_display = metadata.get("title", "Untitled Document")
            chunk_num = metadata.get("chunk_number", 1)
            total_chunks = metadata.get("total_chunks", 1)
            category = metadata.get("category", "General")

            with st.expander(
                f"📦 {title_display} (Chunk {chunk_num}/{total_chunks}) — ID: {record_id[:8]}..."
            ):
                st.markdown(
                    f"""
                    <div style='margin-bottom: 0.8rem; display: flex; align-items: center; gap: 8px;'>
                        <span style='background: #818cf8; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 700;'>
                            {category.upper()}
                        </span>
                        <span style='color: #94a3b8; font-size: 0.85rem;'>
                            Record ID: <code>{record_id}</code>
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f"""
                    <div style='background: rgba(255, 255, 255, 0.02); padding: 14px; border-radius: 8px; border-left: 3px solid #c084fc; margin-bottom: 8px; line-height: 1.6; color: #cbd5e1;'>
                        {document}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.write(f"**Embedding Dimension**: `{len(embedding)}`")
                st.write("**First 20 Vector Values:**")
                st.code(
                    str(
                        [
                            round(float(value), 6)
                            for value in embedding[:20]
                        ]
                    )
                )

        st.divider()

        confirmation = st.checkbox(
            "I understand that this will permanently clear my isolated database."
        )

        if st.button(
            "Clear My Isolated Database",
            disabled=not confirmation,
        ):
            rag.clear_database()
            st.success("Your vector database has been cleared.")
            st.rerun()

    else:
        st.warning("Your vector database is empty. Add information first.")


# -------------------------------------------------
# TAB 4: HOW IT WORKS
# -------------------------------------------------
with tab4:
    st.header("How the Personal RAG system works")

    st.code(
        """
Personal Information / Documents
        ↓
Text Cleaning & Preprocessing
        ↓
Word Chunking (with overlap)
        ↓
Sentence Transformer (all-MiniLM-L6-v2)
        ↓
Vector Embeddings (384 dimensions)
        ↓
Isolated ChromaDB Collection
        ↓
User Natural Language Question
        ↓
Question Vector Embedding
        ↓
Cosine Similarity Search
        ↓
Top Matching Context Chunks
        ↓
Aggregated Context Window
        ↓
LLM Generation (Next Stage)
        ↓
Final Verified Answer
        """,
        language="text",
    )

    st.subheader("System Architecture")
    st.success(
        """
        • **SQLite Authentication**: Email & Password registration with PBKDF2 password hashing.  
        • **Per-User Isolation**: Each account accesses a dedicated ChromaDB directory.  
        • **Dynamic Vectorization**: Normalizes embeddings for fast dot-product similarity calculations.  
        • **Interactive Inspector**: Inspect raw vector slices and document metadata in real-time.
        """
    )