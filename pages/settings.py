from __future__ import annotations

import streamlit as st


def render_settings(user_info: dict) -> None:
    """Render Settings page with preferences and account details."""
    st.markdown("<h1>Settings</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size: 0.9rem; color: #A1A1AA; margin-bottom: 1.5rem;'>Manage workspace appearance, search preferences, and account info.</p>",
        unsafe_allow_html=True,
    )

    st.markdown("### Appearance")
    st.selectbox("Theme Preference", ["Dark (Vercel/Linear Default)", "Light", "System Default"], index=0)

    st.markdown("### Search Preferences")
    st.slider("Default Top-K Results", min_value=1, max_value=10, value=3)

    st.markdown("### Account Details")
    st.markdown(
        f"""
        <div class="saas-card">
            <div style="font-size: 0.9rem; color: #FAFAFA; margin-bottom: 4px;"><b>Full Name:</b> {user_info.get('username', 'N/A')}</div>
            <div style="font-size: 0.9rem; color: #FAFAFA; margin-bottom: 4px;"><b>Email Address:</b> {user_info.get('email', 'N/A')}</div>
            <div style="font-size: 0.9rem; color: #FAFAFA;"><b>User Account ID:</b> #{user_info.get('id', 'N/A')}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### System Information")
    st.markdown(
        """
        <div class="saas-card">
            <div style="font-size: 0.85rem; color: #71717A;">
                • Platform Version: <b>v2.0.0 (Modular Release)</b><br>
                • Vector Database: <b>ChromaDB Local Engine</b><br>
                • Authentication DB: <b>SQLite (users.db)</b><br>
                • Embedding Model: <b>sentence-transformers/all-MiniLM-L6-v2</b>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
