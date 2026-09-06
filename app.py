from __future__ import annotations

import re
import pandas as pd
import streamlit as st

import auth
from rag_engine import PersonalRAG

# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------
st.set_page_config(
    page_title="Personal RAG Learning Lab",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

auth.init_auth_state()

# -------------------------------------------------
# VERCEL / LINEAR DESIGN SYSTEM (CSS)
# -------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Reset & Base Canvas */
    html, body, [class*="css"], .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #09090b !important;
        color: #ededed !important;
    }
    
    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    /* Typography */
    h1 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 800 !important;
        letter-spacing: -0.03em !important;
        color: #ffffff !important;
        font-size: 2.25rem !important;
        margin-bottom: 0.25rem !important;
    }
    
    h2 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
        color: #f4f4f5 !important;
        font-size: 1.5rem !important;
        margin-bottom: 1rem !important;
    }

    h3, h4, h5 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: -0.01em !important;
        color: #e4e4e7 !important;
    }
    
    p, span, label {
        color: #a1a1aa;
    }
    
    /* Linear/Vercel Cards */
    .linear-card {
        background-color: #121215;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1.75rem;
        margin-bottom: 1.25rem;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }
    .linear-card:hover {
        border-color: rgba(255, 255, 255, 0.15);
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
    }
    
    /* Top Header Bar */
    .header-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-bottom: 1.25rem;
        margin-bottom: 1.5rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    .breadcrumb {
        font-size: 0.875rem;
        font-weight: 500;
        color: #71717a;
    }
    .breadcrumb span {
        color: #f4f4f5;
        font-weight: 600;
    }
    
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.25);
        color: #10b981;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.02em;
    }
    .status-dot {
        width: 6px;
        height: 6px;
        background-color: #10b981;
        border-radius: 50%;
        box-shadow: 0 0 8px #10b981;
    }

    /* Auth Centered Container */
    .auth-container {
        max-width: 440px;
        margin: 4rem auto 0 auto;
        background: #121215;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 2.5rem 2rem;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6);
    }
    .auth-brand {
        text-align: center;
        margin-bottom: 2rem;
    }
    .auth-brand-icon {
        width: 48px;
        height: 48px;
        background: #18181b;
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 12px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-bottom: 0.75rem;
    }
    .auth-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.02em;
    }
    .auth-subtitle {
        font-size: 0.875rem;
        color: #71717a;
        margin-top: 0.25rem;
    }

    /* Form Inputs */
    .stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] {
        background-color: #18181b !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        color: #f4f4f5 !important;
        padding: 0.65rem 0.85rem !important;
        font-size: 0.9rem !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.25) !important;
    }
    
    /* Buttons */
    div.stButton > button {
        background: #ffffff !important;
        color: #09090b !important;
        border: 1px solid #ffffff !important;
        padding: 0.65rem 1.25rem !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        transition: all 0.15s ease !important;
        width: 100%;
        cursor: pointer;
    }
    div.stButton > button:hover {
        background: #e4e4e7 !important;
        border-color: #e4e4e7 !important;
        transform: translateY(-1px);
    }
    div.stButton > button:active {
        transform: translateY(0);
    }

    /* Modern Tabs Navigation */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px !important;
        background-color: #141417 !important;
        padding: 4px !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    .stTabs [data-baseweb="tab"] {
        height: 38px !important;
        background-color: transparent !important;
        border-radius: 7px !important;
        color: #a1a1aa !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        padding: 0 18px !important;
        transition: all 0.15s ease !important;
        border: none !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #f4f4f5 !important;
        background-color: rgba(255, 255, 255, 0.04) !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #27272a !important;
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    .stTabs [data-baseweb="tab-highlight-container"] {
        display: none !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0c0c0e !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    .user-profile-pill {
        background: #141417;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 0.85rem;
        margin-bottom: 1.25rem;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .avatar-circle {
        width: 38px;
        height: 38px;
        border-radius: 50%;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        color: #ffffff;
        font-size: 0.95rem;
        flex-shrink: 0;
    }
    .user-name-text {
        font-weight: 600;
        color: #f4f4f5;
        font-size: 0.875rem;
        line-height: 1.2;
    }
    .user-email-text {
        color: #71717a;
        font-size: 0.75rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 140px;
    }

    /* Metrics Styling */
    div[data-testid="stMetric"] {
        background: #141417 !important;
        padding: 1rem 1.25rem !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.75rem !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        letter-spacing: -0.02em !important;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.8rem !important;
        color: #71717a !important;
        font-weight: 500 !important;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background-color: #141417 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        color: #f4f4f5 !important;
        font-size: 0.875rem !important;
    }
    .streamlit-expanderContent {
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-top: none !important;
        background-color: #0f0f12 !important;
        border-bottom-left-radius: 8px !important;
        border-bottom-right-radius: 8px !important;
        padding: 1.25rem !important;
    }

    /* Table Styling */
    .stDataFrame {
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 8px !important;
        overflow: hidden !important;
    }

    /* Linear Result Card */
    .result-card {
        background: #141417;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }
    .score-bar-bg {
        width: 100%;
        height: 6px;
        background: rgba(255, 255, 255, 0.08);
        border-radius: 3px;
        overflow: hidden;
        margin-top: 6px;
    }
    .score-bar-fill {
        height: 100%;
        border-radius: 3px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------
# AUTHENTICATION GATE
# -------------------------------------------------
if not st.session_state["authenticated"]:
    col1, col2, col3 = st.columns([1, 2.2, 1])

    with col2:
        st.markdown(
            """
            <div class="auth-container">
                <div class="auth-brand">
                    <div class="auth-brand-icon">🧠</div>
                    <div class="auth-title">Personal RAG Lab</div>
                    <div class="auth-subtitle">Isolated Retrieval-Augmented Generation Platform</div>
                </div>
            """,
            unsafe_allow_html=True,
        )

        auth_tab1, auth_tab2 = st.tabs(["Sign In", "Create Account"])

        with auth_tab1:
            st.markdown(
                "<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True
            )
            email_or_user_input = st.text_input(
                "Email or Username",
                key="login_email",
                placeholder="name@company.com",
            )
            password_input = st.text_input(
                "Password",
                type="password",
                key="login_pass",
                placeholder="••••••••",
            )

            st.markdown(
                "<div style='margin-top: 0.5rem;'></div>",
                unsafe_allow_html=True,
            )
            if st.button("Sign In", type="primary", use_container_width=True):
                success, msg = auth.login(email_or_user_input, password_input)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

        with auth_tab2:
            st.markdown(
                "<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True
            )
            reg_email = st.text_input(
                "Email Address",
                key="reg_email",
                placeholder="name@company.com",
            )
            reg_username = st.text_input(
                "Full Name", key="reg_user", placeholder="Alex Smith"
            )
            reg_password = st.text_input(
                "Password",
                type="password",
                key="reg_pass",
                placeholder="••••••••",
            )
            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                key="reg_pass_confirm",
                placeholder="••••••••",
            )

            st.markdown(
                "<div style='margin-top: 0.5rem;'></div>",
                unsafe_allow_html=True,
            )
            if st.button("Create Account", use_container_width=True):
                if reg_password != confirm_password:
                    st.error("Passwords do not match.")
                else:
                    success, msg = auth.register_user(
                        reg_email, reg_username, reg_password
                    )
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)

        st.markdown("</div>", unsafe_allow_html=True)

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
if not st.session_state.get("authenticated") or user_info is None:
    st.stop()

rag = load_user_rag_system(user_info["id"], user_info["email"])

# -------------------------------------------------
# SIDEBAR NAVIGATION & PROFILE
# -------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div style="font-weight: 700; font-size: 1rem; color: #ffffff; margin-bottom: 1rem; display: flex; align-items: center; gap: 8px;">
            <span>🧠</span> Personal RAG
        </div>
        """,
        unsafe_allow_html=True,
    )

    initials = (
        user_info["username"][:2].upper() if user_info["username"] else "U"
    )
    st.markdown(
        f"""
        <div class="user-profile-pill">
            <div class="avatar-circle">{initials}</div>
            <div>
                <div class="user-name-text">{user_info['username']}</div>
                <div class="user-email-text">{user_info['email']}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Sign Out", use_container_width=True):
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
        <div style="font-size: 0.8rem; color: #71717a; line-height: 1.6;">
            <b>Workspace Features</b><br>
            • Multi-user database isolation<br>
            • MiniLM-L6-v2 Embeddings (384d)<br>
            • Cosine similarity ranking<br>
            • SQLite user account store
        </div>
        """,
        unsafe_allow_html=True,
    )

# -------------------------------------------------
# MAIN DASHBOARD HEADER
# -------------------------------------------------
st.markdown(
    f"""
    <div class="header-bar">
        <div class="breadcrumb">
            Workspaces / <span>Personal RAG Lab</span>
        </div>
        <div class="status-badge">
            <div class="status-dot"></div> Dedicated DB Active
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.title("Personal RAG Workspace")
st.markdown(
    "<p style='margin-bottom: 1.5rem;'>Ingest documents, compute dense vector embeddings, and run semantic similarity retrieval.</p>",
    unsafe_allow_html=True,
)

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Add Content",
        "Semantic Search",
        "Vector Inspector",
        "Architecture",
    ]
)


# -------------------------------------------------
# TAB 1: ADD CONTENT
# -------------------------------------------------
with tab1:
    st.markdown("## Add Content")
    st.markdown(
        "<p style='font-size: 0.875rem;'>Convert text into chunk embeddings stored in your isolated database.</p>",
        unsafe_allow_html=True,
    )

    title = st.text_input(
        "Document Title",
        placeholder="e.g. Predictive Maintenance Architecture Specs",
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
        "Document Text",
        height=220,
        placeholder="Paste your notes or document text here...",
    )

    col1, col2 = st.columns(2)
    with col1:
        chunk_size = st.slider(
            "Chunk Size (words)",
            min_value=30,
            max_value=300,
            value=100,
            step=10,
        )
    with col2:
        overlap = st.slider(
            "Chunk Overlap (words)",
            min_value=0,
            max_value=50,
            value=20,
            step=5,
        )

    st.markdown(
        "<div style='margin-top: 0.5rem;'></div>", unsafe_allow_html=True
    )

    if st.button(
        "Compute Embeddings & Save", type="primary", use_container_width=True
    ):
        try:
            result = rag.store_text(
                text=information,
                title=title or "Untitled Document",
                category=category,
                chunk_size=chunk_size,
                overlap=overlap,
            )

            st.success(
                f"Successfully stored {len(result['chunks'])} chunk(s) in your vector database."
            )

            st.markdown("### Generated Chunks")
            for index, chunk in enumerate(result["chunks"]):
                with st.expander(
                    f"Chunk #{index + 1} — {len(chunk.split())} words",
                    expanded=(index == 0),
                ):
                    st.write(chunk)
                    embedding = result["embeddings"][index]

                    st.markdown(
                        f"**Embedding Dimension**: `{len(embedding)}`"
                    )
                    st.markdown("**First 20 Vector Values:**")
                    st.code(
                        str(
                            [
                                round(float(value), 6)
                                for value in embedding[:20]
                            ]
                        )
                    )

        except ValueError as error:
            st.error(str(error))
        except Exception as error:
            st.exception(error)


# -------------------------------------------------
# TAB 2: SEMANTIC SEARCH
# -------------------------------------------------
with tab2:
    st.markdown("## Semantic Search")
    st.markdown(
        "<p style='font-size: 0.875rem;'>Query your vector database using natural language embedding distance.</p>",
        unsafe_allow_html=True,
    )

    question = st.text_input(
        "Search Query",
        placeholder="e.g. Which project handles machine fault detection?",
    )

    top_k = st.slider(
        "Results to Retrieve (Top-K)",
        min_value=1,
        max_value=10,
        value=3,
    )

    st.markdown(
        "<div style='margin-top: 0.5rem;'></div>", unsafe_allow_html=True
    )

    if st.button("Run Search", type="primary", use_container_width=True):
        try:
            result = rag.search(
                question=question,
                number_of_results=top_k,
            )

            st.markdown("### Query Vector")
            query_embedding = result["query_embedding"]
            st.markdown(
                f"**Dimension**: `{len(query_embedding)}` | **First 20 Values:**"
            )
            st.code(
                str(
                    [
                        round(float(value), 6)
                        for value in query_embedding[:20]
                    ]
                )
            )

            st.markdown("### Search Results")

            for position, match in enumerate(result["matches"], start=1):
                similarity = match["cosine_similarity"]
                metadata = match["metadata"]
                percentage = int(max(0, min(100, similarity * 100)))

                if similarity >= 0.7:
                    bar_color = "#10b981"
                elif similarity >= 0.4:
                    bar_color = "#f59e0b"
                else:
                    bar_color = "#ef4444"

                st.markdown(
                    f"""
                    <div class="result-card">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                            <span style="font-weight: 600; font-size: 0.9rem; color: #ffffff;">
                                #{position} {metadata.get("title", "Untitled")}
                            </span>
                            <span style="font-weight: 700; font-size: 0.85rem; color: {bar_color};">
                                {similarity:.4f} ({percentage}%)
                            </span>
                        </div>
                        <div style="font-size: 0.8rem; color: #71717a; margin-bottom: 8px;">
                            Category: <b>{metadata.get("category", "General")}</b> | Chunk {metadata.get("chunk_number", 1)} of {metadata.get("total_chunks", 1)}
                        </div>
                        <div style="background: #09090b; padding: 12px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.06); font-size: 0.875rem; color: #d4d4d8; line-height: 1.5;">
                            {match["text"]}
                        </div>
                        <div class="score-bar-bg">
                            <div class="score-bar-fill" style="width: {percentage}%; background-color: {bar_color};"></div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown("### Aggregated Context Window")
            st.text_area(
                "Retrieved Context",
                value=result["context"],
                height=180,
                disabled=True,
            )

        except ValueError as error:
            st.error(str(error))
        except Exception as error:
            st.exception(error)


# -------------------------------------------------
# TAB 3: VECTOR INSPECTOR
# -------------------------------------------------
with tab3:
    st.markdown("## Vector Database Inspector")
    st.markdown(
        f"<p style='font-size: 0.875rem;'>Total stored records in your isolated database: <b>{rag.database_count()}</b></p>",
        unsafe_allow_html=True,
    )

    if st.button("Refresh Table"):
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
                    "ID": record_id[:12] + "...",
                    "Title": metadata.get("title"),
                    "Category": metadata.get("category"),
                    "Chunk": metadata.get("chunk_number"),
                    "Words": len(document.split()),
                    "Embedding Dim": len(embedding),
                }
            )

        st.dataframe(
            pd.DataFrame(table_rows),
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("### Record Slices")
        for index, record_id in enumerate(records["ids"]):
            metadata = records["metadatas"][index]
            document = records["documents"][index]
            embedding = records["embeddings"][index]

            with st.expander(
                f"📦 {metadata.get('title', 'Untitled')} (Chunk {metadata.get('chunk_number', 1)}) — ID: {record_id[:8]}"
            ):
                st.write(document)
                st.markdown(f"**Dimension**: `{len(embedding)}`")
                st.code(
                    str(
                        [
                            round(float(value), 6)
                            for value in embedding[:20]
                        ]
                    )
                )

        st.markdown("---")
        confirmation = st.checkbox(
            "I confirm that I want to clear my database."
        )
        if st.button("Clear Vector DB", disabled=not confirmation):
            rag.clear_database()
            st.success("Vector database cleared.")
            st.rerun()
    else:
        st.info("Your vector database is empty. Add content in Tab 1.")


# -------------------------------------------------
# TAB 4: ARCHITECTURE
# -------------------------------------------------
with tab4:
    st.markdown("## Architecture & RAG Pipeline")

    st.code(
        """
[ Document Ingestion ] ➔ [ Text Cleaning ] ➔ [ Word Chunking ]
                                                    │
                                                    ▼
[ Semantic Search Results ] ◄── [ ChromaDB ] ◄── [ MiniLM-L6-v2 Embeddings ]
        """,
        language="text",
    )

    st.markdown(
        """
        ### Technical Specifications
        - **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2` (384 Dimensions)
        - **Vector Store**: ChromaDB (Persistent storage isolated per user ID & email)
        - **User Authentication**: SQLite database (`users.db`) with PBKDF2 password hashing
        - **Similarity Metric**: Cosine Similarity via dot product over normalized vectors
        """
    )