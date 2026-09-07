from __future__ import annotations

import streamlit as st


def render_pipeline() -> None:
    """Render interactive RAG Pipeline architecture visualization."""
    st.markdown("<h1>RAG Pipeline Architecture</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size: 0.9rem; color: #A1A1AA; margin-bottom: 1.5rem;'>Visualize the end-to-end text ingestion, vector embedding, and retrieval pipeline.</p>",
        unsafe_allow_html=True,
    )

    st.code(
        """
DOCUMENT ➔ EXTRACT TEXT ➔ CHUNKING ➔ EMBEDDINGS ➔ CHROMADB ➔ RETRIEVAL ➔ RESPONSE
        """,
        language="text",
    )

    st.markdown("### Pipeline Status")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            <div class="saas-card">
                <div style="font-weight: 700; color: #FAFAFA; font-size: 1rem; margin-bottom: 4px;">Document Ingestion Engine</div>
                <div style="font-size: 0.85rem; color: #22C55E;">● Active & Ready</div>
                <div style="font-size: 0.8rem; color: #71717A; margin-top: 8px;">Parses text documents, cleans linebreaks, and normalizes whitespaces.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="saas-card">
                <div style="font-weight: 700; color: #FAFAFA; font-size: 1rem; margin-bottom: 4px;">Embedding Vector Model</div>
                <div style="font-size: 0.85rem; color: #22C55E;">● Loaded (all-MiniLM-L6-v2)</div>
                <div style="font-size: 0.8rem; color: #71717A; margin-top: 8px;">Generates normalized 384-dimensional dense semantic vectors.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="saas-card">
                <div style="font-weight: 700; color: #FAFAFA; font-size: 1rem; margin-bottom: 4px;">Chunking Engine</div>
                <div style="font-size: 0.85rem; color: #22C55E;">● Active</div>
                <div style="font-size: 0.8rem; color: #71717A; margin-top: 8px;">Splits text into overlapping word windows (e.g. 100 words, 20 overlap).</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="saas-card">
                <div style="font-weight: 700; color: #FAFAFA; font-size: 1rem; margin-bottom: 4px;">ChromaDB Storage</div>
                <div style="font-size: 0.85rem; color: #22C55E;">● Connected & Isolated</div>
                <div style="font-size: 0.8rem; color: #71717A; margin-top: 8px;">Stores vectors, document text, and metadata isolated per user account.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
