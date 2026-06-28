import streamlit as st
import requests
from config import BACKEND_URL

def signup_handler(name, email, password):
    data = {
            "name": name,
            "email": email,
            "password": password,
        }
    
    try:
        response = requests.post(f"{BACKEND_URL}/sign-up", json=data)
        data = response.json()

        if response.status_code == 200:
            st.session_state["token"] = data["access_token"]
            st.session_state["logged_in"] = True

            st.success(data["message"])
            st.switch_page("index.py")

        elif response.status_code == 422:
            for err in data["detail"]:
                st.error(err["msg"])
        else:
            st.error(data["detail"])

    except Exception as e:
        st.error(f"Error - {e}")
        print(e)
        

with st.form("SignUp"):
    st.markdown("### Create your account")
    st.markdown("Sign up to access your AI Enterprise Assistant.")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Signup")

st.page_link(
    "pages/login.py",
    label="Already have an account? Login"
)

if submit and name and email and password:
    signup_handler(name, email, password)
elif submit:
    st.warning("Please fill all the fields.")