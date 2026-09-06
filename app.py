from __future__ import annotations

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

# Custom premium styling for UI/UX
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    /* Global font override */
    html, body, [class*="css"], .stApp {
        font-family: 'Outfit', sans-serif !important;
    }
    
    /* Title and description styles */
    h1 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem !important;
    }
    h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
        color: #f1f5f9 !important;
    }
    
    /* Style metrics with custom glass cards */
    div[data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.4) !important;
        padding: 1.2rem !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1) !important;
        transition: all 0.3s ease !important;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px) !important;
        border-color: rgba(99, 102, 241, 0.3) !important;
        box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1) !important;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        color: #6366f1 !important;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
        color: #94a3b8 !important;
        font-weight: 500 !important;
    }
    
    /* Modern Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;
        background-color: rgba(21, 28, 44, 0.6) !important;
        padding: 6px !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    .stTabs [data-baseweb="tab"] {
        height: 42px !important;
        white-space: pre-wrap !important;
        background-color: transparent !important;
        border-radius: 6px !important;
        color: #94a3b8 !important;
        font-weight: 500 !important;
        padding: 0 20px !important;
        transition: all 0.2s ease !important;
        border: none !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #f8fafc !important;
        background-color: rgba(255, 255, 255, 0.03) !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2) !important;
    }
    .stTabs [data-baseweb="tab-highlight-container"] {
        display: none !important;
    }
    
    /* Style Buttons */
    div.stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.6rem 1.5rem !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 14px 0 rgba(99, 102, 241, 0.3) !important;
        width: 100%;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px 0 rgba(99, 102, 241, 0.5) !important;
        background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%) !important;
    }
    div.stButton > button:active {
        transform: translateY(1px) !important;
    }
    
    /* Style input elements */
    .stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] {
        background-color: #0b0f19 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        color: #f1f5f9 !important;
        transition: border-color 0.2s !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 1px #6366f1 !important;
    }
    
    /* Style Expander headers and content */
    .streamlit-expanderHeader {
        background-color: rgba(30, 41, 59, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        color: #f1f5f9 !important;
    }
    .streamlit-expanderContent {
        border-left: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
        background-color: rgba(21, 28, 44, 0.2) !important;
        border-bottom-left-radius: 8px !important;
        border-bottom-right-radius: 8px !important;
        padding: 1.2rem !important;
    }
    
    /* Styled container cards for custom markdown */
    .glass-card {
        background: rgba(30, 41, 59, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    /* Table modifications */
    .stDataFrame {
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 8px !important;
        overflow: hidden !important;
    }
    
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# AUTHENTICATION GATE
# -------------------------------------------------
if not st.session_state["authenticated"]:
    st.title("🧠 Personal RAG Learning Lab")
    st.markdown("### Welcome! Please log in or create an account to access the lab.")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        auth_tab1, auth_tab2 = st.tabs(["🔑 Login", "📝 Register Account"])
        
        with auth_tab1:
            st.subheader("Login to your account")
            username_input = st.text_input("Username", key="login_user")
            password_input = st.text_input("Password", type="password", key="login_pass")
            
            st.info("💡 **Demo Credentials**: Username `admin` | Password `admin123`")
            
            if st.button("Log In", type="primary", use_container_width=True):
                success, msg = auth.login(username_input, password_input)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

        with auth_tab2:
            st.subheader("Create a new account")
            new_username = st.text_input("Choose Username", key="reg_user")
            new_password = st.text_input("Choose Password", type="password", key="reg_pass")
            confirm_password = st.text_input("Confirm Password", type="password", key="reg_pass_confirm")
            
            if st.button("Create Account", use_container_width=True):
                if new_password != confirm_password:
                    st.error("Passwords do not match!")
                else:
                    success, msg = auth.register_user(new_username, new_password)
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)
    st.stop()


@st.cache_resource
def load_rag_system() -> PersonalRAG:
    """Load the embedding model and database only once."""
    return PersonalRAG()

rag = load_rag_system()

# Sidebar Layout for statistics, user info and quick guide
with st.sidebar:
    st.markdown("### 🧠 Personal RAG System")
    st.markdown(f"👤 **Logged in as:** `{st.session_state['user']}`")
    if st.button("🚪 Logout", use_container_width=True):
        auth.logout()
        st.rerun()

    st.markdown("---")
    st.metric(
        label="Chunks stored in Vector DB",
        value=rag.database_count(),
    )
    st.markdown("---")
    st.markdown(
        """
        #### ⚙️ Quick Navigation
        Use the tabs on the right to navigate:
        1. **Add Information**: Input facts, define category, chunk size and overlap, and generate embeddings.
        2. **Semantic Search**: Ask a natural question and let the vector DB retrieve similar context chunks.
        3. **Vector Database**: Explore, filter, inspect raw embeddings, or reset the collection.
        4. **How It Works**: Understand the full text-to-embedding-to-retrieval pipeline.
        """
    )
    st.markdown("---")
    st.markdown(
        """
        <div style="font-size: 0.8rem; color: #64748b; text-align: center;">
            Personal RAG Learning Lab v1.1.0
        </div>
        """,
        unsafe_allow_html=True
    )

st.title("🧠 Personal RAG Learning Lab")

st.markdown(
    """
    <div style='margin-bottom: 1.5rem; color: #94a3b8;'>
        Add your personal information, convert it into embeddings, store it in 
        ChromaDB and search it using semantic similarity.
    </div>
    """,
    unsafe_allow_html=True
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
    st.header("Add your personal information")

    title = st.text_input(
        "Title",
        placeholder="Example: Predictive Maintenance Project",
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
        "Enter information",
        height=250,
        placeholder=(
            "Example:\n"
            "I developed a predictive maintenance system using "
            "Random Forest and Isolation Forest..."
        ),
    )

    col1, col2 = st.columns(2)

    with col1:
        chunk_size = st.slider(
            "Chunk size in words",
            min_value=30,
            max_value=300,
            value=100,
            step=10,
        )

    with col2:
        overlap = st.slider(
            "Chunk overlap in words",
            min_value=0,
            max_value=50,
            value=20,
            step=5,
        )

    if st.button(
        "Generate Embeddings and Store",
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
                f"Stored {len(result['chunks'])} chunks successfully."
            )

            st.subheader("Generated chunks")

            for index, chunk in enumerate(result["chunks"]):
                with st.expander(
                    f"Chunk {index + 1}",
                    expanded=True,
                ):
                    st.write(chunk)

                    embedding = result["embeddings"][index]

                    st.write(
                        f"Embedding dimension: {len(embedding)}"
                    )

                    st.write("First 20 embedding values:")

                    st.code(
                        str(
                            [
                                round(float(value), 6)
                                for value in embedding[:20]
                            ]
                        )
                    )

                    with st.expander(
                        "View complete embedding"
                    ):
                        st.write(embedding.tolist())

        except ValueError as error:
            st.error(str(error))

        except Exception as error:
            st.exception(error)


# -------------------------------------------------
# TAB 2: SEARCH
# -------------------------------------------------
with tab2:
    st.header("Semantic search")

    question = st.text_input(
        "Ask a question about your information",
        placeholder="Example: Which project uses anomaly detection?",
    )

    top_k = st.slider(
        "Number of chunks to retrieve",
        min_value=1,
        max_value=10,
        value=3,
    )

    if st.button(
        "Search Vector Database",
        type="primary",
        use_container_width=True,
    ):
        try:
            result = rag.search(
                question=question,
                number_of_results=top_k,
            )

            st.subheader("Question")
            st.info(result["question"])

            st.subheader("Query embedding")

            query_embedding = result["query_embedding"]

            st.write(
                f"Embedding dimension: {len(query_embedding)}"
            )

            st.write("First 20 values:")

            st.code(
                str(
                    [
                        round(float(value), 6)
                        for value in query_embedding[:20]
                    ]
                )
            )

            with st.expander("View complete query embedding"):
                st.write(query_embedding.tolist())

            st.subheader("Similarity results")

            similarity_table = []

            for position, match in enumerate(
                result["matches"],
                start=1,
            ):
                metadata = match["metadata"]

                similarity_table.append(
                    {
                        "Rank": position,
                        "Title": metadata.get(
                            "title",
                            "Unknown",
                        ),
                        "Category": metadata.get(
                            "category",
                            "Unknown",
                        ),
                        "Chunk": metadata.get(
                            "chunk_number",
                            "Unknown",
                        ),
                        "Cosine Similarity": round(
                            match["cosine_similarity"],
                            4,
                        ),
                        "Database Distance": round(
                            match["database_distance"],
                            4,
                        ),
                    }
                )

            st.dataframe(
                pd.DataFrame(similarity_table),
                use_container_width=True,
                hide_index=True,
            )

            for position, match in enumerate(
                result["matches"],
                start=1,
            ):
                similarity = match["cosine_similarity"]
                metadata = match["metadata"]

                # Dynamic badge color based on similarity score
                if similarity >= 0.7:
                    badge_color = "#10b981"  # Emerald green
                elif similarity >= 0.4:
                    badge_color = "#f59e0b"  # Amber/Yellow
                else:
                    badge_color = "#ef4444"  # Red

                with st.expander(
                    (
                        f"Result {position} — "
                        f"Similarity: {similarity:.4f}"
                    ),
                    expanded=(position == 1),
                ):
                    st.markdown(
                        f"""
                        <div style='margin-bottom: 0.8rem; display: flex; align-items: center; gap: 8px;'>
                            <span style='background: {badge_color}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 600;'>
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
                        <div style='background: rgba(255, 255, 255, 0.02); padding: 12px; border-radius: 6px; border-left: 3px solid #6366f1; margin-bottom: 8px; line-height: 1.5; color: #cbd5e1;'>
                            {match["text"]}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            st.subheader("Retrieved context")

            st.text_area(
                "This context will later be sent to the LLM",
                value=result["context"],
                height=250,
                disabled=True,
            )

            st.subheader("Current answer")

            st.info(
                """
                Retrieval is working. The chunks above are the
                information found by semantic search.

                In the next stage, we will send this context and
                your question to an LLM to generate a natural answer.
                """
            )

        except ValueError as error:
            st.error(str(error))

        except Exception as error:
            st.exception(error)


# -------------------------------------------------
# TAB 3: DATABASE EXPLORER
# -------------------------------------------------
with tab3:
    st.header("Vector database explorer")

    st.write(
        f"Total stored chunks: **{rag.database_count()}**"
    )

    if st.button("Refresh database records"):
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
                    "Words": len(document.split()),
                    "Embedding Dimension": len(embedding),
                }
            )

        st.dataframe(
            pd.DataFrame(table_rows),
            use_container_width=True,
            hide_index=True,
        )

        st.subheader("Inspect individual records")

        for index, record_id in enumerate(records["ids"]):
            metadata = records["metadatas"][index]
            document = records["documents"][index]
            embedding = records["embeddings"][index]

            title_display = metadata.get("title", "Untitled Document")
            chunk_num = metadata.get("chunk_number", 1)
            total_chunks = metadata.get("total_chunks", 1)
            category = metadata.get("category", "General")

            with st.expander(f"📦 {title_display} (Chunk {chunk_num}/{total_chunks}) — {record_id[:8]}..."):
                st.markdown(
                    f"""
                    <div style='margin-bottom: 0.8rem; display: flex; align-items: center; gap: 8px;'>
                        <span style='background: #6366f1; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 600;'>
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
                    <div style='background: rgba(255, 255, 255, 0.02); padding: 12px; border-radius: 6px; border-left: 3px solid #a855f7; margin-bottom: 8px; line-height: 1.5; color: #cbd5e1;'>
                        {document}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.write(f"**Embedding Dimension**: `{len(embedding)}`")
                st.write("**First 20 values:**")
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
            "I understand that this will delete all records."
        )

        if st.button(
            "Clear Vector Database",
            disabled=not confirmation,
        ):
            rag.clear_database()
            st.success("Vector database cleared.")
            st.rerun()

    else:
        st.warning(
            "The vector database is empty. Add information first."
        )


# -------------------------------------------------
# TAB 4: EXPLANATION
# -------------------------------------------------
with tab4:
    st.header("How the system works")

    st.code(
        """
Personal Information
        ↓
Text Cleaning
        ↓
Chunking
        ↓
Sentence Transformer
        ↓
Embedding Vectors
        ↓
ChromaDB
        ↓
User Question
        ↓
Question Embedding
        ↓
Similarity Search
        ↓
Top Matching Chunks
        ↓
Retrieved Context
        ↓
LLM — added in the next stage
        ↓
Final RAG Answer
        """,
        language="text",
    )

    st.subheader("Current project stage")

    st.success(
        """
        This version implements:

        • Text input  
        • Text cleaning  
        • Chunking  
        • Embedding generation  
        • Persistent vector storage  
        • Semantic search  
        • Cosine similarity display  
        • Retrieved context display
        """
    )

    st.warning(
        """
        The final LLM generation is intentionally not added yet.
        First verify that storage and retrieval work correctly.
        """
    )