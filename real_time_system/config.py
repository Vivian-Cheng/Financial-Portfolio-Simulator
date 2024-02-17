"""Stores configuration settings for the real-time system.

This module contains all parameters used in the real-time system script.
"""

# The maximum number of calls per second per API key
API_RATE_LIMIT = 5
# A list of available API keys
# TODO: all - Put your API keys here.
API_KEYS = ["dummy_key_1", "dummy_key_2", 
            "dummy_key_3", "dummy_key_4", 
            "dummy_key_5", "dummy_key_6"]
# Interval between calls for each symbol in second
SYMBOL_CALL_INTERVAL = 15
# API endpoint
# TODO: Put API endpoint here. May create more constant if more that one endpoint.
API_URL = "https//dummy/url"
# A list contains all symbols we fetch in the system
# TODO: Put symbols here.
SYMBOLS = ["dummy_symbol_1", "dummy_symbol_2", "dummy_symbol_3", 
           "dummy_symbol_4", "dummy_symbol_5"]


#TODO: Any database-related constant?
# Available MongoDB instances
MONGODB_SERVER = {
    'dummy_server_1': 'dummy_server_1_url',
    'dummy_server_2': 'dummy_server_2_url'
}
# Name of database in each MongoDB instance
DB_NAME = "stock"
# The data model of a stock quote data
DATA_MODEL = {
    'current_price': 'c',
    'change': 'd',
    'percent_change': 'dp',
    'high_price': 'h',
    'low_price': 'l',
    'open_price': 'o',
    'prev_close_price': 'pc',
    'timestamp': 't'
}
# TTL seconds
TTL = 86400
