from __future__ import annotations

import time
import streamlit as st
from components.upload_zone import render_upload_zone
from utils.constants import CATEGORIES


def render_knowledge(rag_engine) -> None:
    """Render Add Knowledge ingestion page with processing progress feedback."""
    st.markdown("<h1>Add Knowledge</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size: 0.9rem; color: #A1A1AA; margin-bottom: 1.5rem;'>Bring information into your personal AI workspace.</p>",
        unsafe_allow_html=True,
    )

    source_type = st.radio(
        "Source Type",
        options=["Upload File", "Paste Text"],
        horizontal=True,
        label_visibility="collapsed",
    )

    title = st.text_input(
        "Document Title",
        placeholder="e.g. Predictive Maintenance Architecture Specs",
    )

    category = st.selectbox("Category", CATEGORIES)

    information_content = ""

    if source_type == "Upload File":
        render_upload_zone()
        uploaded_file = st.file_uploader(
            "Select File",
            type=["txt", "pdf", "docx"],
            label_visibility="collapsed",
        )
        if uploaded_file is not None:
            try:
                information_content = uploaded_file.read().decode("utf-8")
                st.success(f"Loaded '{uploaded_file.name}' ({len(information_content.split())} words)")
            except Exception:
                st.error("Error reading file content. Please upload a plain text file.")
    else:
        information_content = st.text_area(
            "Document Content",
            height=220,
            placeholder="Paste your research notes, project documentation, or study facts here...",
        )

    col1, col2 = st.columns(2)
    with col1:
        chunk_size = st.slider("Chunk Size (words)", min_value=30, max_value=300, value=100, step=10)
    with col2:
        overlap = st.slider("Chunk Overlap (words)", min_value=0, max_value=50, value=20, step=5)

    if st.button("Index Document", type="primary", use_container_width=True):
        if not information_content.strip():
            st.error("Please enter or upload document content first.")
            return

        progress_text = st.empty()
        progress_bar = st.progress(0)

        progress_text.markdown("<b>Processing Document</b><br>✓ Text extracted", unsafe_allow_html=True)
        progress_bar.progress(25)
        time.sleep(0.2)

        progress_text.markdown("<b>Processing Document</b><br>✓ Document chunked", unsafe_allow_html=True)
        progress_bar.progress(50)
        time.sleep(0.2)

        progress_text.markdown("<b>Processing Document</b><br>● Generating embeddings...", unsafe_allow_html=True)
        progress_bar.progress(75)

        try:
            result = rag_engine.store_text(
                text=information_content,
                title=title or "Untitled Document",
                category=category,
                chunk_size=chunk_size,
                overlap=overlap,
            )

            progress_bar.progress(100)
            progress_text.empty()

            st.success("✓ Knowledge successfully indexed")

            st.markdown(
                f"""
                <div class="saas-card" style="margin-top: 1rem;">
                    <div style="font-weight: 700; color: #FAFAFA; font-size: 1.1rem; margin-bottom: 0.5rem;">
                        {title or 'Untitled Document'}
                    </div>
                    <div style="font-size: 0.875rem; color: #A1A1AA;">
                        • <b>{len(result['chunks'])}</b> chunks created<br>
                        • <b>{len(result['chunks'])}</b> embeddings stored in isolated database
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            with st.expander("Inspect Indexed Chunks"):
                for idx, chunk in enumerate(result["chunks"], start=1):
                    st.markdown(f"**Chunk #{idx}**")
                    st.write(chunk)

        except ValueError as err:
            st.error(str(err))
        except Exception as err:
            st.exception(err)
