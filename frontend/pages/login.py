import streamlit as st
import requests
from config import BACKEND_URL

def login_handler(email, password):
    payload = {
            "email": email,
            "password": password,
        }
    
    try:
        response = requests.post(f"{BACKEND_URL}/login", json=payload)
        data = response.json()

        if response.status_code == 200:
            st.session_state.token = data["access_token"]
            st.session_state.logged_in = True
            st.session_state.user_id = data["user_id"]

            st.success(data["message"])
            st.switch_page("index.py")

        elif response.status_code == 422:
            for err in data["detail"]:
                st.error(err["msg"])
        else:
            st.error(data.get("detail", "Login failed."))

    except Exception as e:
        print(e)
        st.error("Unable to connect to the server.")

        

with st.form("login"):
    st.markdown("### Welcome back")
    st.markdown("Login to continue to your AI Enterprise Assistant.")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Login")

st.page_link(
    "pages/signup.py",
    label="Don't have an account? Sign up"
)


if submit:
    if not email or not password:
        st.warning("Please fill both fields.")
    else:
        with st.spinner("Logging in..."):
            login_handler(email, password)