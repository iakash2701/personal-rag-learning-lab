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

PAGES_LIST = [
    PAGE_OVERVIEW,
    PAGE_ADD_KNOWLEDGE,
    PAGE_DOCUMENTS,
    PAGE_SEARCH,
    PAGE_ASSISTANT,
    PAGE_DATABASE,
    PAGE_PIPELINE,
    PAGE_SETTINGS,
]


def render_sidebar(user_info: dict, db_count: int) -> str:
    """Render 240px Linear-style sidebar navigation using reliable session radio state."""
    with st.sidebar:
        # Header Brand Mark
        st.markdown(
            """
            <div style="padding: 0.5rem 0 1rem 0;">
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

        if "active_page" not in st.session_state or st.session_state["active_page"] not in PAGES_LIST:
            st.session_state["active_page"] = PAGE_OVERVIEW

        current_index = PAGES_LIST.index(st.session_state["active_page"])

        st.markdown(
            "<div style='font-size: 0.7rem; font-weight: 700; color: #71717A; letter-spacing: 0.05em; margin-bottom: 0.35rem;'>NAVIGATION</div>",
            unsafe_allow_html=True,
        )

        selected_page = st.radio(
            "Navigation",
            options=PAGES_LIST,
            index=current_index,
            key="sidebar_nav_radio",
            label_visibility="collapsed",
        )

        if selected_page != st.session_state["active_page"]:
            st.session_state["active_page"] = selected_page
            st.rerun()

        st.markdown("<div style='margin-top: 1.25rem;'></div>", unsafe_allow_html=True)

        # Profile Pill & Sign Out
        initials = get_user_initials(user_info.get("username", "User"))
        st.markdown(
            f"""
            <div class="user-profile-pill">
                <div class="avatar-circle">{initials}</div>
                <div style="overflow: hidden;">
                    <div class="user-name-text">{user_info.get('username', 'User')}</div>
                    <div class="user-email-text">{user_info.get('email', '')}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("Sign Out", key="btn_logout", use_container_width=True):
            auth.logout()
            st.rerun()

    return st.session_state["active_page"]
