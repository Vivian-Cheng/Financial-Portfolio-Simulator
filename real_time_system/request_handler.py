from config import API_RATE_LIMIT, API_KEYS, API_URL, SYMBOL_CALL_INTERVAL

"""Handles interactions with the stock API.

This module provides functions to fetch stock data and schedule data retrieval
tasks.

Implementation:
    1. keep info about symbol and its last visit time
    2. keep info about API_key and its last call time
    3. for the given symbol, check whether the (current time - last visit time)
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

