from __future__ import annotations

import streamlit as st


def render_upload_zone() -> None:
    """Render premium document drag-and-drop visual dropzone."""
    st.markdown(
        """
        <div style="border: 2px dashed rgba(255, 255, 255, 0.12); border-radius: 12px; padding: 2.5rem 1.5rem; text-align: center; background: #0F0F12; margin-bottom: 1.25rem;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem; color: #6366F1;">📄</div>
            <div style="font-weight: 700; font-size: 1.1rem; color: #FAFAFA; margin-bottom: 0.25rem;">Upload Knowledge</div>
            <div style="font-size: 0.85rem; color: #71717A; margin-bottom: 0.75rem;">Drag & drop your documents here or browse files</div>
            <div style="display: inline-block; font-size: 0.75rem; color: #A1A1AA; background: rgba(255,255,255,0.04); padding: 4px 12px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.08);">
                Supported Formats: PDF • TXT • DOCX
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
