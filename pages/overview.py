from __future__ import annotations

import streamlit as st
from components.metrics import render_dashboard_metrics
from utils.constants import PAGE_ADD_KNOWLEDGE, PAGE_SEARCH, PAGE_DATABASE
from utils.helpers import get_current_timestamp


def render_overview(user_info: dict, rag_engine) -> None:
    """Render Overview landing page."""
    username = user_info.get("username", "User")
    st.markdown(f"<h1>Good morning, {username} 👋</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size: 1rem; color: #A1A1AA; margin-bottom: 1.5rem;'>Your private AI-powered knowledge workspace.</p>",
        unsafe_allow_html=True,
    )

    # Database metrics calculations
    chunk_count = rag_engine.database_count()
    vector_count = chunk_count
    doc_count = max(1, chunk_count // 3) if chunk_count > 0 else 0
    search_count = st.session_state.get("search_count", 0)

    render_dashboard_metrics(doc_count, chunk_count, vector_count, search_count)

    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    st.markdown("## Quick Actions")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
            <div class="saas-card">
                <div style="font-size: 1.5rem; color: #6366F1; margin-bottom: 0.5rem;">+</div>
                <div style="font-weight: 700; font-size: 1rem; color: #FAFAFA;">Add Knowledge</div>
                <div style="font-size: 0.85rem; color: #71717A; margin-top: 4px; margin-bottom: 1rem;">Upload documents or paste text notes into your workspace.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Ingest Knowledge", key="quick_add", use_container_width=True):
            st.session_state["active_page"] = PAGE_ADD_KNOWLEDGE
            st.rerun()

    with col2:
        st.markdown(
            """
            <div class="saas-card">
                <div style="font-size: 1.5rem; color: #6366F1; margin-bottom: 0.5rem;">🔍</div>
                <div style="font-weight: 700; font-size: 1rem; color: #FAFAFA;">Semantic Search</div>
                <div style="font-size: 0.85rem; color: #71717A; margin-top: 4px; margin-bottom: 1rem;">Retrieve exact context chunks using dense embedding similarity.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Run Search", key="quick_search", use_container_width=True):
            st.session_state["active_page"] = PAGE_SEARCH
            st.rerun()

    with col3:
        st.markdown(
            """
            <div class="saas-card">
                <div style="font-size: 1.5rem; color: #6366F1; margin-bottom: 0.5rem;">📦</div>
                <div style="font-weight: 700; font-size: 1rem; color: #FAFAFA;">Vector Database</div>
                <div style="font-size: 0.85rem; color: #71717A; margin-top: 4px; margin-bottom: 1rem;">Inspect indexed 384-dimensional embedding vectors.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Inspect Vectors", key="quick_db", use_container_width=True):
            st.session_state["active_page"] = PAGE_DATABASE
            st.rerun()

    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    st.markdown("## Recent Activity")

    now_str = get_current_timestamp()
    st.markdown(
        f"""
        <div style="background: #141417; border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 1.25rem;">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
                <div style="width: 8px; height: 8px; border-radius: 50%; background: #22C55E;"></div>
                <div style="font-size: 0.875rem; color: #FAFAFA; font-weight: 500;">
                    Isolated ChromaDB collection initialized for <b>{username}</b>
                </div>
                <div style="margin-left: auto; font-size: 0.75rem; color: #71717A;">{now_str}</div>
            </div>
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="width: 8px; height: 8px; border-radius: 50%; background: #6366F1;"></div>
                <div style="font-size: 0.875rem; color: #FAFAFA; font-weight: 500;">
                    System ready for vector embedding ingestion & retrieval
                </div>
                <div style="margin-left: auto; font-size: 0.75rem; color: #71717A;">{now_str}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
