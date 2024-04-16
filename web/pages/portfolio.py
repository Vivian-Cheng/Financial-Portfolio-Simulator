import streamlit as st
import pandas as pd
from menu import make_menu
import requests
import app

# Access username from app.py
#TODO - Check if this appraoch is correct
username = app.st.session_state.username

def fetch_info_data():
    res = requests.get('http://127.0.0.1:8080/user_info', params={'username': username})
    return res.json()

def fetch_inventory_data():
    res = requests.get('http://127.0.0.1:8080/user_inventory', params={'username': username})
    return res.json()

make_menu()

st.title("User Portfolio")

# TODO - fetch user data from api

col_info_title, col_info_data = st.columns(2)
st.session_state.info_data = fetch_info_data(username)
info_data =st.session_state.info_data
info_title = f'''**ID:**  
    **Username:**  
    '''
with col_info_title:
    st.markdown(info_title)
with col_info_data:
    st.markdown(f"**{info_data['ID']}**")
    st.markdown(f"**{info_data['username']}**")

#stock ownership table
st.header("Stock Ownership")
st.session_state.stock_own_list = fetch_inventory_data()
stock_own_df = pd.DataFrame(st.session_state.stock_own_list['stats'])
st.dataframe(stock_own_df, use_container_width=True)

