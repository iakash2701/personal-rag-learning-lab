from __future__ import annotations

import streamlit as st
from utils.formatters import format_similarity_percentage, get_similarity_color, format_vector_slice


def render_search_results(matches: list[dict]) -> None:
    """Render Linear issue-style match score result rows."""
    if not matches:
        st.info("No matching chunks found.")
        return

    for position, match in enumerate(matches, start=1):
        similarity = match.get("cosine_similarity", 0.0)
        percentage_str = format_similarity_percentage(similarity)
        percentage_val = max(0, min(100, int(similarity * 100)))
        color = get_similarity_color(similarity)
        metadata = match.get("metadata", {})

        st.markdown(
            f"""
            <div class="linear-result-row">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="font-weight: 700; font-size: 0.85rem; color: #6366F1;">#{position}</span>
                        <span style="font-weight: 600; font-size: 0.95rem; color: #FAFAFA;">{metadata.get("title", "Untitled Document")}</span>
                    </div>
                    <span style="font-weight: 700; font-size: 0.85rem; color: {color};">
                        {percentage_str} MATCH
                    </span>
                </div>
                <div style="font-size: 0.78rem; color: #71717A; margin-bottom: 10px;">
                    Category: <b style="color: #A1A1AA;">{metadata.get("category", "General")}</b> • Chunk {metadata.get("chunk_number", 1)} of {metadata.get("total_chunks", 1)}
                </div>
                <div style="background: #09090B; padding: 12px 14px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.06); font-size: 0.875rem; color: #D4D4D8; line-height: 1.5;">
                    {match.get("text", "")}
                </div>
                <div class="progress-bar-bg">
                    <div class="progress-bar-fill" style="width: {percentage_val}%; background-color: {color};"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
