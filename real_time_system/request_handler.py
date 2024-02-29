import requests
import datetime
import time
from config import API_RATE_LIMIT, API_KEYS, LAST_CALL_TIMES, API_URL, SYMBOL_CALL_INTERVAL, MARKET_API_URL, RETRY_COUNT, RETRY_DELAY

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


#helper functions
def currenttime():
    """
    Get current time in seconds
    Return: current time as a floating point number
    """
    current_time = datetime.datetime.now()
    #return time in seconds
    return time.time()

def time_since_last_call(last_call_time):
    """
    Calculate the time since last API call
    """
    return currenttime()-last_call_time

def choose_api_key():
    """
    Choose an available API_key by checking
    (current time -last call time) is greater than (1 / API_RATE_LIMIT). 
    If an API_key isn't valid at this moment, try another one, until all API_key has been tried.
    Return: API_key
    """
    max_diff=-1
    chosen_key=None

    for key in API_KEYS:
        last_call_time=LAST_CALL_TIMES[key]
        if last_call_time is None:
            #Update last call time for the chosen key
            LAST_CALL_TIMES[key] = currenttime()
            return key
        else:
            difference = time_since_last_call(last_call_time)
            if difference >max_diff:
                max_dif=difference
                chosen_key=key

    #Update the last call time for the chosen key
    LAST_CALL_TIMES[chosen_key] = currenttime()
    #If all keys have reached rate limit, return None
    return chosen_key


#Main
def run_retrieval(symbol):
    """
    Retrieve stock quotes from Finnhub given parameter symbol
    Return: stock quotes in json format
    """
    # Choose an available API key
    api_key = choose_api_key()
    url= f"{API_URL}?symbol={symbol}&token={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        #Handle request exceptions
        print("Error fetching data:", e)
        return None
    

def check_market_status():
    """
    Check curent market status
    Return:
    If True, market is curently open
    If False, market is curently closed
    """
    # TODO - replace the API key with variable here DONE
    api_key = choose_api_key()
    is_open = False
    status_forcelist=[429, 500, 502, 503, 504]
    params = {'exchange': 'US', 'token': api_key }
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
    else:
        #handle error cases
        print("Error fetching market status")
    return is_open


#test case
# sym = ["MMM", "AOS", "ABT", "ABBV", "ACN", "ADBE", "AMD", "AES", "AFL", "A", "APD", "ABNB", "AKAM", "ALB", 
#            "ARE", "ALGN", "ALLE", "LNT", "ALL", "GOOGL", "GOOG","MO", "AMZN", "AMCR", "AEE", "AAL", "AEP", "AXP"] 
# for s in sym:
#     data= run_retrieval(s)
#     print(data)
# print(LAST_CALL_TIMES)

# market_status = check_market_status()
# if market_status is not None:
#     if market_status:
#         print("The market is currently open.")
#     else:
#         print("The market is currently closed.")
# else:
#     print("Unable to determine market status at this time.")
