import streamlit as st
import pandas as pd
import time
import requests
from menu import make_menu

# initialize session state variable
if "search_stock" not in st.session_state:
    st.session_state.search_stock = (None, None)

def fetch_stock_list():
    res = requests.get('http://127.0.0.1:8080/stock_list')
    print(res.json())
    return res.json()

def fetch_stock_search(symbol):
    params = {'symbol': symbol}
    res = requests.get('http://127.0.0.1:8080/search_stock', params=params)
    return res.json()[0] 

#fetch stock list from api, a dataframe
st.session_state.stock_list = fetch_stock_list()

make_menu()

st.title("Stock Search")
# Input field for user to enter a stock ticker symbol
symbol = st.text_input(
    "Enter a stock ticker symbol to search.",
    placeholder="Enter a stock ticker symbol"
)

# Check if the entered symbol is valid (exists in the stock list)
if symbol:
    if symbol in [stock['symbol'] for stock in st.session_state.stock_list]:
        company = fetch_stock_search(symbol)['company']
        st.session_state.search_stock = (symbol, company)
        with st.spinner('Searching symbol...'):
            time.sleep(2)
        st.switch_page("pages/symbol.py")
    else:
        st.error("Invalid input or symbol not found.")

#stock table
stock_list_df = pd.DataFrame(st.session_state.stock_list)
stock_table = st.dataframe(stock_list_df, use_container_width=True)
