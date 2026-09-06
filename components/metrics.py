from __future__ import annotations

import streamlit as st


def render_dashboard_metrics(doc_count: int, chunk_count: int, vector_count: int, search_count: int) -> None:
    """Render 4 neutral, compact metric overview cards."""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(label="Documents", value=doc_count)
    with col2:
        st.metric(label="Chunks", value=chunk_count)
    with col3:
        st.metric(label="Vectors", value=vector_count)
    with col4:
        st.metric(label="Searches", value=search_count)
