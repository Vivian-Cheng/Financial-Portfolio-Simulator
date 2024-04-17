import streamlit as st
import pandas as pd
from menu import make_menu
import requests

# initialize session state variable
if "current_user_id" not in st.session_state:
    st.switch_page("app.py")
user_id = st.session_state.current_user_id

# def fetch_info_data():
#     res = requests.get('http://127.0.0.1:8080/user_info', params={'username': username})
#     return res.json()

def fetch_inventory_data(id):
    res = requests.get('http://127.0.0.1:8080/user_inventory', params={'userId': id})
    return res.json()


make_menu()

st.title("User Portfolio")

# TODO - fetch user data from api

col_info_title, col_info_data = st.columns(2)
info_title = f'''**User ID:**  
    **User Name:**  
    '''
info_data = f'''{user_id}  
    {st.session_state.current_user_name}  
    '''
with col_info_title:
    st.markdown(info_title)
with col_info_data:
    st.markdown(info_data)

#stock ownership table
st.header("Stock Ownership")
stock_own_list = fetch_inventory_data(user_id)
stock_own_df = pd.DataFrame(stock_own_list)
st.dataframe(stock_own_df, use_container_width=True, hide_index=True)

