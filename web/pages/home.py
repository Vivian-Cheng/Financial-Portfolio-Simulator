import streamlit as st
import pandas as pd
import time
from menu import make_menu

# initialize session state variable
if "search_stock" not in st.session_state:
    st.session_state.search_stock = (None, None)

# TODO: fetch stock list from api, a dataframe?
stock_list = pd.DataFrame({
    'symbol': ['AAPL', 'MSFT', 'AMZN', 'TSLA'],
    'company': ['Apple', 'Microsoft', 'Amazon', 'Tesla']
})

make_menu()

st.title("Stock Search")
symbol = st.text_input(
    "Enter a stock ticker symbol to search.",
    placeholder="Enter a stock ticker symbol"
    )
if symbol in stock_list['symbol'].values:
    company = stock_list.loc[stock_list['symbol'] == symbol, 'company'].values[0]
    st.session_state.search_stock = (symbol, company)
#     with st.spinner('Search symbol...'):
#         time.sleep(2)
    st.switch_page("pages/symbol.py")
elif symbol != "":
    st.error("Invalid Input")


stock_table = st.dataframe(stock_list, use_container_width=True)
