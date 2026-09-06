from __future__ import annotations

import pandas as pd
import streamlit as st
from components.empty_states import render_empty_documents


def render_documents(rag_engine) -> None:
    """Render Knowledge Library documents list page."""
    st.markdown("<h1>Knowledge Library</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size: 0.9rem; color: #A1A1AA; margin-bottom: 1.5rem;'>Manage and inspect indexed documents in your private collection.</p>",
        unsafe_allow_html=True,
    )

    db_count = rag_engine.database_count()

    if db_count == 0:
        render_empty_documents()
        return

    records = rag_engine.get_all_records()
    documents_dict = {}

    for idx, record_id in enumerate(records["ids"]):
        metadata = records["metadatas"][idx]
        title = metadata.get("title", "Untitled Document")
        if title not in documents_dict:
            documents_dict[title] = {
                "title": title,
                "category": metadata.get("category", "General"),
                "chunks": 0,
                "words": 0,
            }
        documents_dict[title]["chunks"] += 1
        documents_dict[title]["words"] += len(records["documents"][idx].split())

    col1, col2 = st.columns([3, 1])
    with col1:
        search_filter = st.text_input("Filter documents", placeholder="Search document titles...", label_visibility="collapsed")

    rows = []
    for title, doc in documents_dict.items():
        if search_filter and search_filter.lower() not in title.lower():
            continue
        rows.append(
            {
                "Document Name": title,
                "Category": doc["category"],
                "Chunks": doc["chunks"],
                "Total Words": doc["words"],
                "Status": "● Indexed",
            }
        )

    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.info("No documents match your filter query.")
