import streamlit as st

def init_chat_session():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def get_messages():
    return st.session_state.messages

def add_user_message(question: str):
    st.session_state.messages.append({
        "role": "user",
        "content": question,
    })

def add_assistant_message(answer: str):
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })