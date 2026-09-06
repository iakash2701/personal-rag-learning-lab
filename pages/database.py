from __future__ import annotations

import pandas as pd
import streamlit as st
from utils.formatters import format_vector_slice


def render_database(rag_engine, user_info: dict) -> None:
    """Render developer-friendly Vector Database Inspector."""
    st.markdown("<h1>Vector Database Inspector</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size: 0.9rem; color: #A1A1AA; margin-bottom: 1.5rem;'>Inspect indexed vector collections and metadata schemas for your account.</p>",
        unsafe_allow_html=True,
    )

    db_count = rag_engine.database_count()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Vectors", value=db_count)
    with col2:
        st.metric(label="Embedding Dimension", value=384)
    with col3:
        st.metric(label="Database Status", value="Connected")

    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

    if st.button("Refresh Vector Records"):
        st.rerun()

    if db_count > 0:
        records = rag_engine.get_all_records()
        table_rows = []

        for idx, record_id in enumerate(records["ids"]):
            doc = records["documents"][idx]
            meta = records["metadatas"][idx]
            vec = records["embeddings"][idx]
            table_rows.append(
                {
                    "Chunk ID": record_id[:12] + "...",
                    "Title": meta.get("title"),
                    "Category": meta.get("category"),
                    "Chunk #": meta.get("chunk_number"),
                    "Words": len(doc.split()),
                    "Dimension": len(vec),
                }
            )

        st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)

        st.markdown("### Inspect Vector Slices")
        for idx, record_id in enumerate(records["ids"]):
            meta = records["metadatas"][idx]
            doc = records["documents"][idx]
            vec = records["embeddings"][idx]

            with st.expander(f"📦 Chunk #{meta.get('chunk_number', 1)} — {meta.get('title', 'Untitled')} ({record_id[:8]}...)"):
                st.write(doc)
                st.markdown(f"**Vector Dimension**: `{len(vec)}`")
                st.markdown("**First 20 Embeddings:**")
                st.code(format_vector_slice(vec, limit=20))

        st.markdown("---")
        st.markdown("<h3 style='color: #EF4444;'>Danger Zone</h3>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 0.85rem; color: #71717A;'>Permanently clear all indexed vectors from your isolated collection.</p>", unsafe_allow_html=True)

        confirm_clear = st.checkbox("I confirm that I want to delete all vectors from my database.")
        if st.button("Clear Vector Database", disabled=not confirm_clear, kind="secondary"):
            rag_engine.clear_database()
            st.success("Your isolated vector database has been cleared.")
            st.rerun()
    else:
        st.info("Your vector database is currently empty.")
