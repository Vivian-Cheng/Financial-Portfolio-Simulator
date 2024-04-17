import streamlit as st
import requests
import pandas as pd
import altair as alt
from menu import make_menu

#initialize
if "historical_db_stats" not in st.session_state:
    st.session_state.historical_db_stats = None
if "data_availablity" not in st.session_state:
    st.session_state.data_availablity = None
if "user_list" not in st.session_state:
    st.session_state.user_list = None


# Redirect to app.py if not logged in, otherwise show the navigation menu
make_menu()

# Verify the user's role
if st.session_state.role not in ["admin"]:
    st.warning("You do not have permission to view this page.")
    st.stop()

def fetch_historical_db_stat():
    res = requests.get('http://127.0.0.1:8080/db_stats')
    return res.json()
def refresh():
    st.session_state.historical_db_stats = fetch_historical_db_stat()

def fetch_data_availability():
    res = requests.get('http://127.0.0.1:8080/data_availability')
    return res.json()

def fetch_user_list():
    res = requests.get('http://127.0.0.1:8080/user_list')
    return res.json()

def insert_user(username, password):
    payload = {'username': username, 'password': password}
    response = requests.post('http://127.0.0.1:8080/insert_user', json=payload)
    if response.status_code == 200:
        st.success('User inserted successfully')
    else:
        st.error('Failed to insert user')

def delete_user(username):
    payload = {'username': username}
    response = requests.post('http://127.0.0.1:8080/delete_user', json=payload)
    if response.status_code == 200:
        st.success('User deleted successfully')
    else:
        st.error('Failed to delete user')

st.title("Stock Quote historical DB")
col_title, col_btn = st.columns([4, 1])
with col_title:
    st.markdown('''### DB Stats''')
with col_btn:
    if st.button("Refresh"):
        refresh()
tab_stats, tab_availability, tab_users = st.tabs(["DB Stats", "Stock Data Availability", "Users"])
st.session_state.fetch_historical_db_stat = fetch_historical_db_stat()
st.session_state.data_availablity = fetch_data_availability()
st.session_state.user_list = fetch_user_list()
with tab_stats:
    historical_db_stats_df = pd.DataFrame(st.session_state.fetch_historical_db_stat)
    st.dataframe(historical_db_stats_df, use_container_width=True)
with tab_availability:
    avai_df = pd.DataFrame(st.session_state.data_availablity)
    st.dataframe(avai_df, use_container_width=True)
with tab_users:
    collections_df = pd.DataFrame(st.session_state.user_list)
    st.data_editor(collections_df, use_container_width=True)

    st.markdown('''#### Admin commands''')
    username = st.text_input('Enter username')
    password = st.text_input('Enter password', type='password')
    if st.button('Insert User'):
        insert_user(username, password)
        st.write(insert_user(username, password))

    if st.button('Delete User'):
        delete_user(username, password)
        st.write(delete_user(username, password))

