import datetime
from config import DATA_MODEL

"""Handles data processing tasks.

This module provides functions for processing data before writing it to the
database.
"""

"""Convert Unix timestamp to Python datetime object.

Args:
    timestamp: A Unix timestamp.
Return:
    A datetime object.
"""
def unix_timestamp_to_datetime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)

"""Transform data to match the db schema.

Args:
    symbol: A string representing a stock symbol.
    data: a dict from API result.
Return:
    A dict representing the data.
"""
def transform_data(symbol, data):
    trans_data = {}
    for key in DATA_MODEL.keys():
        trans_data[key] = data.get(DATA_MODEL[key], None)
    # convert the date format
    if trans_data['timestamp'] is not None:
        trans_data['timestamp'] = unix_timestamp_to_datetime(trans_data['timestamp']) 
    else:
        trans_data['timestamp'] = datetime.datetime.today()
    # assign _id
    trans_data['_id'] = f'{symbol}_{datetime.datetime.today()}'
    return trans_data
    
