import streamlit as st
import datetime
import requests
from menu import make_menu
import pandas as pd
import altair as alt
from streamlit_autorefresh import st_autorefresh

# initialize session state variable
if "is_market_close" not in st.session_state:
    st.session_state.is_market_close = True
if "stock_info" not in st.session_state:
    st.session_state.stock_info = {}
if "stock_quote_chart" not in st.session_state:
    st.session_state.stock_quote_chart = []
# handle missing state when refresh
if "search_stock" not in st.session_state:
    st.switch_page("pages/home.py")


# TODO - set a api url variable

# check market status with simple time check
def check_market_close():
    # get current time (assume in LA time)
    curr_time = datetime.datetime.now()
    # time difference between Eastern and Western time
    eastern_offset = datetime.timedelta(hours=3)
    # current time in Eastern time
    curr_time_e = curr_time + eastern_offset
    if curr_time_e.weekday() < 5:
        # check if the current time is between 9:30 a.m. and 4:00 p.m. Eastern time
        market_open_time = curr_time_e.replace(hour=9, minute=30, second=0, microsecond=0)
        market_close_time = curr_time_e.replace(hour=16, minute=0, second=0, microsecond=0)
        if curr_time_e >= market_open_time and curr_time_e <= market_close_time:
            return False
    return True

# @st.cache_data(ttl=10)
def fetch_stock_quote():
    params = {'symbol': st.session_state.search_stock[0]}
    res = requests.get('http://127.0.0.1:8080/quote', params=params)
    return res.json()[0]

# @st.cache_data()
def fetch_stock_quote_chart(start, end):
    params = {'symbol': st.session_state.search_stock[0],
              'start': start,
              'end': end}
    res = requests.get('http://127.0.0.1:8080/quote_chart', params=params)
    print(res.json())
    return res.json()

def get_quote_chart(data):
    hover = alt.selection_point(
        fields=["timestamp"],
        nearest=True,
        on="mouseover",
        empty=False
    )

    lines = (
        alt.Chart(data, title="Real-time stock prices")
        .mark_line()
        .encode(
            x="timestamp",
            y = alt.Y("current_price", scale=alt.Scale(
                domain=[data['current_price'].min(), data['current_price'].max()]))
        )
    )

    # Draw points on the line, and highlight based on selection
    points = lines.transform_filter(hover).mark_circle(size=80)

    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="timestamp",
            y="current_price",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("timestamp", title="Time"),
                alt.Tooltip("current_price", title="Price (USD)"),
            ],
        )
        .add_params(hover)
    )
    return (lines + points + tooltips).interactive()

st.session_state.stock_info = fetch_stock_quote()
st.session_state.is_market_close = check_market_close()

make_menu()

st.title("Stock Information")
col_info_title_1, col_info_data_1, col_info_title_2, col_info_data_2, col_sum = st.columns([1,1,1,1,2])

info_title_1 = f'''**Stock Ticker Symbol:**  
    **Company Name:**  
    **Trading Day:**
    '''
info_title_2 = f'''**Previous Closing Price:**  
    **Opening Price:**  
    **High Price:**  
    **Low Price:**  
    '''
info_data_1 = f''' {st.session_state.search_stock[0]}  
    {st.session_state.search_stock[1]}  
    {datetime.date.today()}
'''
info_data_2 = f'''{st.session_state.stock_info.get('prev_close_price', None)}  
{st.session_state.stock_info.get('open_price', None)}  
{st.session_state.stock_info.get('high_price', None)}  
{st.session_state.stock_info.get('low_price', None)}
'''

with col_info_title_1:
    st.markdown(info_title_1)
with col_info_data_1:
    st.markdown(info_data_1)
with col_info_title_2:
    st.markdown(info_title_2)
with col_info_data_2:
    st.markdown(info_data_2)
with col_sum:
    st.metric(label="Current Price", 
              value=st.session_state.stock_info.get('current_price', None), 
              delta=st.session_state.stock_info.get('change', None), 
              delta_color="inverse")


# TODO: check user wallet
# TODO: transaction api
st.markdown("⚠️:orange[Transaction available when market is open]")
amt = st.number_input(
    'Input amount',
    min_value=0,
    step=1,
    disabled=st.session_state.is_market_close
    )
col_buy, col_sell = st.columns(2)
with col_buy:
    if st.button("Buy", disabled=st.session_state.is_market_close):
        st.write("buy!")
with col_sell:
    if st.button("Sell", disabled=st.session_state.is_market_close):
        st.write("sell!")

tab_realtime, tab_historical = st.tabs(["Real-time", "Historical"])
with tab_realtime:
    st.header("Real-time chart")
    col_start, col_end = st.columns(2)
    with col_start:
        start = st.time_input("Start time", datetime.time(0,0))
    with col_end:
        end = st.time_input("End time", "now")
    if start and end:
        st.session_state.stock_quote_chart = fetch_stock_quote_chart(start.strftime('%H:%M:%S'), 
                                                                     end.strftime('%H:%M:%S'))
    if len(st.session_state.stock_quote_chart) > 0:
        quote_chart_df = pd.DataFrame(st.session_state.stock_quote_chart, columns=["current_price", "timestamp"])
        quote_chart_df['timestamp'] = pd.to_datetime(quote_chart_df['timestamp'])
        quote_chart_df['timestamp'] = quote_chart_df['timestamp'].dt.strftime('%H:%M')
        # st.line_chart(quote_chart_df, x="timestamp", y="current_price")
        quote_chart = get_quote_chart(quote_chart_df)
        st.altair_chart(quote_chart, use_container_width=True)

with tab_historical:
    st.header("Historical chart")
    # TODO - historical chart

st_autorefresh(interval=60 * 1000, key="api_update")
st.session_state.stock_info = fetch_stock_quote()
st.session_state.is_market_close = check_market_close()
