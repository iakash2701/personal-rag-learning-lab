from __future__ import annotations

import time
import streamlit as st
from components.search_results import render_search_results
from components.empty_states import render_empty_search


def render_search(rag_engine) -> None:
    """Render Perplexity/Linear-inspired Semantic Search hero experience."""
    st.markdown("<h1>Semantic Search</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size: 0.9rem; color: #A1A1AA; margin-bottom: 1.5rem;'>Search across your personal knowledge base using dense vector embeddings.</p>",
        unsafe_allow_html=True,
    )

    col_search, col_k = st.columns([4, 1])
    with col_search:
        question = st.text_input(
            "Search Query",
            placeholder="Ask anything from your knowledge base...",
            label_visibility="collapsed",
        )
    with col_k:
        top_k = st.selectbox("Top K", [1, 2, 3, 5, 10], index=2, label_visibility="collapsed")

    col_btn, col_hint = st.columns([1, 4])
    with col_btn:
        search_clicked = st.button("Search", type="primary", use_container_width=True)
    with col_hint:
        st.markdown("<div style='font-size: 0.78rem; color: #71717A; padding-top: 8px;'>Shortcut: <b>Ctrl + Enter</b></div>", unsafe_allow_html=True)

    if not question and not search_clicked:
        render_empty_search()
        return

    if question or search_clicked:
        if not question.strip():
            st.error("Please enter a search query.")
            return

        start_time = time.time()
        try:
            result = rag_engine.search(question=question, number_of_results=top_k)
            elapsed = time.time() - start_time

            # Increment search counter in session state
            st.session_state["search_count"] = st.session_state.get("search_count", 0) + 1

            st.markdown(
                f"""
                <div style="font-size: 0.85rem; color: #71717A; margin: 1rem 0 1.25rem 0;">
                    Found <b>{len(result['matches'])}</b> relevant result(s) in <b>{elapsed:.2f} seconds</b>
                </div>
                """,
                unsafe_allow_html=True,
            )

            render_search_results(result["matches"])

            st.markdown("### Retrieved Context Window")
            st.text_area(
                "Aggregated Context",
                value=result["context"],
                height=180,
                disabled=True,
            )

        except ValueError as err:
            st.error(str(err))
        except Exception as err:
            st.exception(err)
