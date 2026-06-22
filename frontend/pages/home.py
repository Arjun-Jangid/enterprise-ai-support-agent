import streamlit as st

st.set_page_config(page_title="home", page_icon="📄")

st.title("Test")
st.sidebar.header("Test")
st.write(
    """This demo illustrates a combination of plotting and animation with
Streamlit. We're generating a bunch of random numbers in a loop for around
5 seconds. Enjoy!"""
)

arr = [1, 2, 3, 4, 5]

for i in arr:
    st.write(i)