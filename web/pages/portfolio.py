import streamlit as st
import pandas as pd
from menu import make_menu

make_menu()

st.title("User Portfolio")

# TODO - fetch user data from api

col_info_title, col_info_data = st.columns(2)
info_title = f'''**UID:**  
    **Name:**  
    '''
info_data = f''' 123  
    John Smith
'''
with col_info_title:
    st.markdown(info_title)
with col_info_data:
    st.markdown(info_data)

st.header("Own Stock")
own_stock = pd.DataFrame({
'symbol': ['AAPL', 'MSFT', 'AMZN', 'TSLA'],
'volumn': [1, 2, 3, 4],
'value': [123, 456, 789, 1011]
})
stock_table = st.dataframe(own_stock, use_container_width=True)
