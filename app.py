from __future__ import annotations

import os
import re
import streamlit as st

import auth
from rag_engine import PersonalRAG

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
from components.sidebar import render_sidebar
from components.header import render_header

from pages.overview import render_overview
from pages.knowledge import render_knowledge
from pages.documents import render_documents
from pages.search import render_search
from pages.assistant import render_assistant
from pages.database import render_database
from pages.pipeline import render_pipeline
from pages.settings import render_settings

# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------
st.set_page_config(
    page_title="Personal RAG Lab",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------------------------------
# LOAD GLOBAL STYLESHEET
# -------------------------------------------------
css_path = os.path.join(os.path.dirname(__file__), "styles", "main.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

auth.init_auth_state()

# -------------------------------------------------
# AUTHENTICATION GATE (VERCEL / LINEAR STYLE)
# -------------------------------------------------
if not st.session_state.get("authenticated"):
    col1, col2, col3 = st.columns([1, 2.2, 1])

    with col2:
        st.markdown(
            """
            <div class="auth-container">
                <div class="auth-brand">
                    <div class="auth-brand-icon">🧠</div>
                    <div class="auth-title">Personal RAG Lab</div>
                    <div class="auth-subtitle">Private AI Knowledge Workspace</div>
                </div>
            """,
            unsafe_allow_html=True,
        )

        auth_tab1, auth_tab2 = st.tabs(["Sign In", "Create Account"])

        with auth_tab1:
            st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
            email_or_user_input = st.text_input(
                "Email or Username", key="login_email", placeholder="name@company.com"
            )
            password_input = st.text_input(
                "Password", type="password", key="login_pass", placeholder="••••••••"
            )

            st.markdown("<div style='margin-top: 0.5rem;'></div>", unsafe_allow_html=True)
            if st.button("Sign In", type="primary", use_container_width=True):
                success, msg = auth.login(email_or_user_input, password_input)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

        with auth_tab2:
            st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
            reg_email = st.text_input(
                "Email Address", key="reg_email", placeholder="name@company.com"
            )
            reg_username = st.text_input(
                "Full Name", key="reg_user", placeholder="Alex Smith"
            )
            reg_password = st.text_input(
                "Choose Password", type="password", key="reg_pass", placeholder="••••••••"
            )
            confirm_password = st.text_input(
                "Confirm Password", type="password", key="reg_pass_confirm", placeholder="••••••••"
            )

            st.markdown("<div style='margin-top: 0.5rem;'></div>", unsafe_allow_html=True)
            if st.button("Create Account", use_container_width=True):
                if reg_password != confirm_password:
                    st.error("Passwords do not match.")
                else:
                    success, msg = auth.register_user(reg_email, reg_username, reg_password)
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)

        st.markdown("</div>", unsafe_allow_html=True)

    st.stop()


# -------------------------------------------------
# AUTHENTICATED USER SESSION & VECTOR ENGINE
# -------------------------------------------------
@st.cache_resource
def load_user_rag_system(user_id: int, email: str) -> PersonalRAG:
    """Load isolated vector database instance per logged-in user."""
    safe_email = re.sub(r"[^a-zA-Z0-9_-]", "_", email.lower())
    user_db_path = f"./chroma_data/user_{user_id}_{safe_email}"
    collection_name = f"rag_user_{user_id}"
    return PersonalRAG(
        database_path=user_db_path,
        collection_name=collection_name,
    )


user_info = st.session_state.get("user_info")
if not st.session_state.get("authenticated") or user_info is None:
    st.stop()

if st.session_state.get("authenticated") and user_info is not None:
    rag_engine = load_user_rag_system(user_info["id"], user_info["email"])

    # -------------------------------------------------
    # SIDEBAR & HEADER ROUTER
    # -------------------------------------------------
    active_page = render_sidebar(user_info, rag_engine.database_count())
    render_header(active_page)

    # -------------------------------------------------
    # PAGE ROUTING
    # -------------------------------------------------
    if active_page == PAGE_OVERVIEW:
        render_overview(user_info, rag_engine)

    elif active_page == PAGE_ADD_KNOWLEDGE:
        render_knowledge(rag_engine)

    elif active_page == PAGE_DOCUMENTS:
        render_documents(rag_engine)

    elif active_page == PAGE_SEARCH:
        render_search(rag_engine)

    elif active_page == PAGE_ASSISTANT:
        render_assistant(rag_engine)

    elif active_page == PAGE_DATABASE:
        render_database(rag_engine, user_info)

    elif active_page == PAGE_PIPELINE:
        render_pipeline()

    elif active_page == PAGE_SETTINGS:
        render_settings(user_info)