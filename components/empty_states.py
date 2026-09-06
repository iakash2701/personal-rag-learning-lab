from __future__ import annotations

import streamlit as st


def render_empty_documents() -> None:
    """Render empty state when no documents exist in database."""
    st.markdown(
        """
        <div style="border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 3rem 1.5rem; text-align: center; background: #141417; margin: 1.5rem 0;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem; color: #71717A;">📂</div>
            <div style="font-weight: 700; font-size: 1.15rem; color: #FAFAFA; margin-bottom: 0.35rem;">No Knowledge Indexed Yet</div>
            <div style="font-size: 0.875rem; color: #A1A1AA; max-width: 400px; margin: 0 auto 1.25rem auto;">
                Upload documents or paste text notes to build your personal isolated knowledge base.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_empty_search() -> None:
    """Render empty state prompt suggestions for Semantic Search."""
    st.markdown(
        """
        <div style="margin-top: 1.5rem;">
            <div style="font-size: 0.8rem; font-weight: 700; color: #71717A; letter-spacing: 0.05em; margin-bottom: 0.75rem;">
                TRY ASKING:
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 10px;">
                <div style="background: #141417; border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 12px; font-size: 0.85rem; color: #A1A1AA;">
                    • Explain machine learning concepts
                </div>
                <div style="background: #141417; border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 12px; font-size: 0.85rem; color: #A1A1AA;">
                    • Summarize key project architecture
                </div>
                <div style="background: #141417; border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 12px; font-size: 0.85rem; color: #A1A1AA;">
                    • Find fault detection algorithms
                </div>
                <div style="background: #141417; border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 12px; font-size: 0.85rem; color: #A1A1AA;">
                    • What are the main study notes findings?
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
