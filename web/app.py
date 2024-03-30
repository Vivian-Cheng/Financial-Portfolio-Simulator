import streamlit as st
from time import sleep
from menu import make_menu

# Initialize st.session_state.role to None
if "role" not in st.session_state:
    st.session_state.role = None
st.session_state._role = st.session_state.role

make_menu()

st.title("🏦 Financial Portfolio Simulator")
st.write("Please log in to continue.")

# Callback function to save the role selection to Session State
def set_role():
    st.session_state.role = st.session_state._role

# Selectbox to choose role
st.selectbox(
    "Select your role:",
    ["user", "admin"],
    key="_role",
    index=None,
    on_change=set_role,
)

with st.container():
    username = st.text_input(
        "Enter username",
        disabled=st.session_state.role is None
    )
    password = st.text_input(
        "Enter password",
        type="password",
        disabled=st.session_state.role is None
    )

col_login, col_reg = st.columns(2)
with col_login:
    # TODO - check user and pwd
    if st.button("Log in", type="primary", disabled=st.session_state.role is None):
        if username == "test" and password == "test":
            st.session_state.logged_in = True
            st.success("Logged in successfully!")
            sleep(0.5)
            st.switch_page("pages/home.py")
        else:
            st.error("Incorrect username or password")
with col_reg:
    if st.button("Register", type="primary", disabled=st.session_state.role != "user"):
        # TODO - check whether user exist
        if username != "":
            # TODO - add user info to DB
            st.session_state.logged_in = True
            st.success("Register & Logged in successfully!")
            sleep(0.5)
            st.switch_page("pages/home.py")
        else:
            st.error("User already exists!")
