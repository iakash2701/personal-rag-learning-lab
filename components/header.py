from __future__ import annotations

import streamlit as st


def render_header(active_page: str) -> None:
    """Render contextual top header with breadcrumbs and database online status."""
    st.markdown(
        f"""
        <div class="header-bar">
            <div class="breadcrumb">
                Personal RAG / <span>{active_page}</span>
            </div>
            <div style="display: flex; align-items: center; gap: 16px;">
                <div style="font-size: 0.75rem; color: #71717A; background: #141417; border: 1px solid rgba(255,255,255,0.08); padding: 3px 8px; border-radius: 6px;">
                    ⌘ K Search
                </div>
                <div class="status-badge">
                    <div class="status-dot"></div> Database Connected
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
