import streamlit as st
import requests
import pandas as pd
import altair as alt
from menu import make_menu
from time import sleep

#initialize
if "historical_db_stats" not in st.session_state:
    st.session_state.historical_db_stats = None
if "data_availability" not in st.session_state:
    st.session_state.data_availability = None
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
    st.session_state.data_availability = fetch_data_availability()
    st.session_state.user_list = fetch_user_list()

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
refresh()
with tab_stats:
    historical_db_stats_df = pd.DataFrame(st.session_state.historical_db_stats)
    st.dataframe(historical_db_stats_df, use_container_width=True, hide_index=True)
with tab_availability:
    avai_df = pd.DataFrame(st.session_state.data_availability, columns=["Date", "Availability"])
    avai_df['Date'] = pd.to_datetime(avai_df['Date']).dt.strftime('%Y-%m-%d')
    st.dataframe(avai_df, use_container_width=True, hide_index=True)
with tab_users:
    collections_df = pd.DataFrame(st.session_state.user_list, columns=["id", "username", \
                                                                       "passcode", "isAdmin"])
    collections_df.index += 1
    st.dataframe(collections_df, use_container_width=True)

    st.markdown('''#### Admin commands''')
    username = st.text_input('Enter username')
    password = st.text_input('Enter password (Only needed by insert)', type='password')
    if st.button('Insert User'):
        with st.spinner("running command..."):
            res = insert_user(username, password)
            #st.write(res)

    if st.button('Delete User'):
        with st.spinner("running command..."):
            res = delete_user(username)
            #st.write(res)

