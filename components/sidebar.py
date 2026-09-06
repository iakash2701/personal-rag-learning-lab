from __future__ import annotations

import streamlit as st
import auth
from utils.constants import (
    PAGE_OVERVIEW,
    PAGE_ADD_KNOWLEDGE,
    PAGE_DOCUMENTS,
    PAGE_SEARCH,
    PAGE_ASSISTANT,
    PAGE_DATABASE,
    PAGE_PIPELINE,
    PAGE_SETTINGS,
)
from utils.helpers import get_user_initials


def render_sidebar(user_info: dict, db_count: int) -> str:
    """Render 240px Linear-style sidebar navigation and profile card."""
    with st.sidebar:
        # Header Brand Mark
        st.markdown(
            """
            <div style="padding: 0.5rem 0 1.25rem 0;">
                <div style="font-weight: 800; font-size: 1.1rem; color: #FAFAFA; letter-spacing: -0.02em; display: flex; align-items: center; gap: 8px;">
                    <span style="color: #6366F1; font-size: 1.25rem;">◈</span> PERSONAL RAG
                </div>
                <div style="font-size: 0.75rem; color: #71717A; margin-top: 2px;">
                    Knowledge Workspace
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if "active_page" not in st.session_state:
            st.session_state["active_page"] = PAGE_OVERVIEW

        # Navigation Groups
        st.markdown("<div style='font-size: 0.7rem; font-weight: 700; color: #71717A; letter-spacing: 0.05em; margin-bottom: 0.35rem;'>MAIN</div>", unsafe_allow_html=True)
        if st.button("Overview", key="nav_overview", use_container_width=True, type="secondary" if st.session_state["active_page"] != PAGE_OVERVIEW else "primary"):
            st.session_state["active_page"] = PAGE_OVERVIEW
            st.rerun()

        st.markdown("<div style='font-size: 0.7rem; font-weight: 700; color: #71717A; letter-spacing: 0.05em; margin: 0.75rem 0 0.35rem 0;'>KNOWLEDGE</div>", unsafe_allow_html=True)
        if st.button("+ Add Knowledge", key="nav_add", use_container_width=True, type="secondary" if st.session_state["active_page"] != PAGE_ADD_KNOWLEDGE else "primary"):
            st.session_state["active_page"] = PAGE_ADD_KNOWLEDGE
            st.rerun()

        if st.button("Documents", key="nav_docs", use_container_width=True, type="secondary" if st.session_state["active_page"] != PAGE_DOCUMENTS else "primary"):
            st.session_state["active_page"] = PAGE_DOCUMENTS
            st.rerun()

        st.markdown("<div style='font-size: 0.7rem; font-weight: 700; color: #71717A; letter-spacing: 0.05em; margin: 0.75rem 0 0.35rem 0;'>INTELLIGENCE</div>", unsafe_allow_html=True)
        if st.button("Semantic Search", key="nav_search", use_container_width=True, type="secondary" if st.session_state["active_page"] != PAGE_SEARCH else "primary"):
            st.session_state["active_page"] = PAGE_SEARCH
            st.rerun()

        if st.button("AI Assistant", key="nav_assistant", use_container_width=True, type="secondary" if st.session_state["active_page"] != PAGE_ASSISTANT else "primary"):
            st.session_state["active_page"] = PAGE_ASSISTANT
            st.rerun()

        st.markdown("<div style='font-size: 0.7rem; font-weight: 700; color: #71717A; letter-spacing: 0.05em; margin: 0.75rem 0 0.35rem 0;'>SYSTEM</div>", unsafe_allow_html=True)
        if st.button("Vector Database", key="nav_db", use_container_width=True, type="secondary" if st.session_state["active_page"] != PAGE_DATABASE else "primary"):
            st.session_state["active_page"] = PAGE_DATABASE
            st.rerun()

        if st.button("RAG Pipeline", key="nav_pipeline", use_container_width=True, type="secondary" if st.session_state["active_page"] != PAGE_PIPELINE else "primary"):
            st.session_state["active_page"] = PAGE_PIPELINE
            st.rerun()

        if st.button("Settings", key="nav_settings", use_container_width=True, type="secondary" if st.session_state["active_page"] != PAGE_SETTINGS else "primary"):
            st.session_state["active_page"] = PAGE_SETTINGS
            st.rerun()

        st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

        # Profile Pill & Sign Out
        initials = get_user_initials(user_info.get("username", "User"))
        st.markdown(
            f"""
            <div class="user-profile-pill">
                <div class="avatar-circle">{initials}</div>
                <div>
                    <div class="user-name-text">{user_info.get('username', 'User')}</div>
                    <div class="user-email-text">{user_info.get('email', '')}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("Logout", key="btn_logout", use_container_width=True):
            auth.logout()
            st.rerun()

    return st.session_state["active_page"]
