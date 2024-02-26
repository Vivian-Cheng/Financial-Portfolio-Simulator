import requests
from config import API_RATE_LIMIT, API_KEYS, API_URL, SYMBOL_CALL_INTERVAL, MARKET_API_URL, RETRY_COUNT, RETRY_DELAY

"""Handles interactions with the stock API.

This module provides functions to fetch stock data and schedule data retrieval
tasks.

Implementation:
    1. [DO NOT NEED THIS NOW!]keep info about symbol and its last visit time
    2. keep info about API_key and its last call time
    3. [DO NOT NEED THIS NOW!] for the given symbol, check whether the (current time - last visit time)
    is greater or equal to SYMBOL_CALL_INTERVAL
    4. create method to choose an available API_key, check the (current time -
    last call time) is greater than (1 / API_RATE_LIMIT). If an API_key isn't 
    valid at this moment, try another one, until all API_key has been tried.
    5. run request to fetch stock quote using API_URL + symbol + API_key
    sample: https://finnhub.io/api/v1/quote?symbol=TSLA&token=API_KEY
    or see: https://finnhub.io/docs/api/quote
    6. assume we have: res = requests.get("https://dummy")
    return res.json()
    7. apply appropriate error handling

    Feel free to add more CONSTANT in config.py and add more functions in this
    module!

Typical usage example:
    data = run_retrieval("TSLA") # this is the only function that will be called
    from main module
"""


"""Run retrieval task.

Args:
    symbol: A string representing a stock symbol

Return:
    x.json() assuming x is the return object from requests
"""
def run_retrieval(symbol):
    # TODO
    return symbol

def check_market_status():
    # TODO - replace the API key with variable here
    is_open = False
    status_forcelist=[429, 500, 502, 503, 504]
    params = {'exchange': 'US', 'token': 'c844d4qad3ide9hefb20'}
    for _ in range(RETRY_COUNT):
        try:
            res = requests.get(MARKET_API_URL, params=params)
            if res.status_code in status_forcelist:
                continue
            break
        except requests.exceptions.RequestException as e:
            pass
    if res.status_code == 200:
        data = res.json()
        is_open = data.get('isOpen', False)
    return is_open


