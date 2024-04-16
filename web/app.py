import streamlit as st
import requests
from time import sleep
from menu import make_menu

# Initialize st.session_state.role to None
if "role" not in st.session_state:
    st.session_state.role = None
st.session_state._role = st.session_state.role

# Initialize st.session_state.username to None
if "username" not in st.session_state:
    st.session_state.username = None
    
make_menu()

st.title("🏦 Financial Portfolio Simulator")
st.write("Please log in to continue.")

# Callback function to save the role selection to Session State
def set_role():
    st.session_state.role = st.session_state._role
# Callback function to save the username to Session State
def set_username():
    st.session_state.username = st.session_state._username

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
    username = st.session_state._username
    password = st.text_input(
        "Enter password",
        type="password",
        disabled=st.session_state.role is None
    )

col_login, col_reg = st.columns(2)
with col_login:
    if st.button("Log in", type="primary", disabled=st.session_state.role is None):
        #check user and pwd
        # Call Flask API to verify user login
        response = requests.get('http://127.0.0.1:8080/user_verif', params={'username': username, \
                                'password': password, 'isadmin': st.session_state.role in ["admin"]})
        print(username, password, st.session_state.role in ["admin"])
        print(response.url)
        if response.status_code == 200:
            data = response.json()
            if data['is_verified'] == True:
                st.session_state.logged_in = True
                st.session_state.current_user_id = data['user_id']  #Store the user ID
                print(response.json())
                st.success("Logged in successfully!")
                sleep(0.5)
                st.switch_page("pages/home.py")
            else:
                st.error("Incorrect username, password or role")
        elif response.status_code == 400:
            st.error("Incorrect username, password or role")
        else:
            st.error("Error occurred while verifying user login")

with col_reg:
    if st.button("Register", type="primary", disabled=st.session_state.role != "user"):
        #check whether user exist
        if username != "" and password != "":
            # Check whether user exist and add user info to DB
            # Call Flask API to register user
            response = requests.post('http://127.0.0.1:8080/user_registration', json={'username': username, \
                                        'password': password, 'isadmin': st.session_state.role in ["admin"]})
            print(username, password, st.session_state.role in ["admin"])
            print(response.url)
            if response.status_code == 200:
                st.session_state.logged_in = True
                st.session_state.current_user_id = response.json()['user_id']  #Store the user ID
                print(response.json())
                st.success("Register & Logged in successfully!")
                sleep(0.5)
                st.switch_page("pages/home.py")
            else:
                st.error("User already exists!")
