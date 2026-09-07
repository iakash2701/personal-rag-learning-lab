from __future__ import annotations

import streamlit as st


def render_assistant(rag_engine) -> None:
    """Render RAG Context Explorer interface with cited sources."""
    st.markdown("<h1>AI Knowledge Assistant</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size: 0.9rem; color: #A1A1AA; margin-bottom: 1.5rem;'>Query your indexed knowledge base to retrieve verified context and cited document sources.</p>",
        unsafe_allow_html=True,
    )

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    if not st.session_state["chat_history"]:
        st.markdown(
            """
            <div style="border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 2.5rem 1.5rem; text-align: center; background: #141417; margin-bottom: 1.5rem;">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem; color: #6366F1;">🧠</div>
                <div style="font-weight: 700; font-size: 1.25rem; color: #FAFAFA; margin-bottom: 0.25rem;">PERSONAL RAG LAB</div>
                <div style="font-size: 0.875rem; color: #71717A; max-width: 420px; margin: 0 auto;">
                    What would you like to explore from your indexed knowledge base today?
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    for message in st.session_state["chat_history"]:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if "sources" in message and message["sources"]:
                st.markdown("**Cited Sources:**")
                for src in message["sources"]:
                    st.caption(f"📄 {src['title']} (Chunk {src['chunk']}) — {src['similarity']}")

    user_query = st.chat_input("Ask a question based on your indexed documents...")
    if user_query:
        st.session_state["chat_history"].append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.write(user_query)

        try:
            result = rag_engine.search(question=user_query, number_of_results=3)
            sources = []
            for match in result["matches"]:
                meta = match["metadata"]
                sim = f"{int(match['cosine_similarity'] * 100)}% match"
                sources.append({
                    "title": meta.get("title", "Untitled"),
                    "chunk": meta.get("chunk_number", 1),
                    "similarity": sim,
                })

            response_text = f"**Retrieved Knowledge Context:**\n\n{result['context']}\n\n*Note: Retrieval completed. Context aggregated from vector store.*"

            st.session_state["chat_history"].append({
                "role": "assistant",
                "content": response_text,
                "sources": sources,
            })

            with st.chat_message("assistant"):
                st.write(response_text)
                st.markdown("**Cited Sources:**")
                for src in sources:
                    st.caption(f"📄 {src['title']} (Chunk {src['chunk']}) — {src['similarity']}")

        except Exception as err:
            st.error(f"Error executing retrieval: {str(err)}")
