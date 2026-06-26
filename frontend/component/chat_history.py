import streamlit as st

def render_chat_history(messages, ):
    st.subheader("Chat History")

    for msg in messages:
        role = "You" if msg["role"] == "user" else "Assistant"

        st.markdown(
            f"""
            <div style="font-size:14px; padding:8px 12px; margin:4px 0;
                        background:#0e1117; border-radius:8px;line-height: 1.5;">
                <b>{role}:</b> {msg["content"]}
            </div>
            """,
            unsafe_allow_html=True,
        )

        if msg["role"] == "assistant":
            with st.expander("Retrieved Chunks"):
                for source in msg["sources"]:
                    st.markdown(
                        f"""
                            <div style='font-size:14px;line-height: 1.5;padding-bottom: 10px;'>
                            <b>Chunk ID:</b> {source["chunk_id"]}<br>
                            <b>Source:</b> {source["source"]}<br>
                            <b>Similarity:</b> {source["similarity"]:.3f}
                            </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    with st.expander("View Chunk"):
                        st.markdown(f"<div style='font-size:14px;line-height: 1.5;'>{source["content"]}</div>", unsafe_allow_html=True)
            