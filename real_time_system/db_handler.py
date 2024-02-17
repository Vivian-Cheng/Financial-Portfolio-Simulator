import pymongo
from config import DB_NAME, DATA_MODEL, TTL
"""Handles query to the database.

This module provides function to setup connection to a database and performs all
kinds of queries to the database.

Typical usage example:
    TODO

"""

"""Setup connection to a database.

Implementation:
    1. Setup connection with the specified URL with the correct ip address
    using pymongo library.
    2. Apply appropriate error handling.

Args:
    url: A string representing the URL and IP address of the database.

Return:
    An pymongo.MongoClient() instance.
"""
def connect_mongodb(url):
    # TODO
    return None

"""Create a database in the given MongoDB instance.

Implementation:
    1. Check if the database exist.
    2. Create one with the given name if not exist.
    3. Error handling.
    4. In MongoDB, a database is not created until it gets content, so if this is
    the first time creating a database, we should create collection and create
    document in it.

Args:
    mongo_client: An pymongo.MongoClient() instance.
    name: A string representing the name of the database we want to create.

Return:
    A database instance in MongoDB.
"""
def create_database_if_not_exist(mongo_client, name):
    # TODO
    return None

"""Create a collection in the given MongoDB database.

Implementation:
    1. Check if the collection exist.
    2. Create one with the given name if not exist.
    3. Error handling.

Args:
    mongo_db: An MongoDB database instance.
    name: A string representing the name of the collection we want to create.

Return:
    A collection instance in MongoDB.
"""
def create_collection_if_not_exit(mongo_db, name):
    # TODO
    return None

def create_collection_with_ttl(mongo_db, name):
    collection = create_collection_if_not_exit(mongo_db, name)
    collection.create_index(DATA_MODEL['timestamp'], expireAfterSeconds = TTL)
    return collection

"""Insert a document into collection.

Implementation:
    1. Use insert_one() function in Pymongo library (or a similar one) to
    insert a document
    2. Error handling.

Args:
    collection: An MongoDB collection instance.
    doc: A dict representing the document(data) we want to insert.

Return:
    A number representing the ID of inserted document. (it could be the return
    value of insert_one() function in Pymongo library)
"""
def insert_one(collection, doc):
    # TODO
    return None

"""Insert documents into collection.

Implementation:
    1. Use insert_many() function in Pymongo library (or a similar one) to
    insert documents
    2. Error handling.

Args:
    collection: An MongoDB collection instance.
    docs: A list of dict representing the documents(data) we want to insert.

Return:
    A InsertManyResult object. (it could be the return
    value of insert_many() function in Pymongo library)
"""
def insert_many(collection, docs):
    # TODO
    return None

"""Setup connection to a database in the given MongoDB instance.

Args:
    node_url: A string representing the url of a MongoDB instance.

Return:
    A database instance in MongoDB.
"""
def start_mongodb(node_url):
    client = connect_mongodb(node_url)
    db = create_database_if_not_exist(client, DB_NAME)
    return db

"""Get the collection of the given stock symbol.

Implementation:
    1. Use hash function to find the key of corresponding MongoDB
    instance.
    2. Handle case when a collection is not found

Args:
    symbol: A string representing the stock symbol

Return:
    A collection instance of the given stock.
"""
def get_stock_collection(symbol):
    # TODO
    return None

"""Add stock data into a MongoDB instance.

Implementation:
    1. Use hash function to find the key of the MongoDB instace
    for the given stock symbol.
    2. Use get_stock_collection() to retrieve the collection of
    the stock
    3. Use insert_one() to insert data

Args:
    symbol: A string representing the stock symbol
    data: A dict representing the stock data

Return:
    A number representing the ID of inserted document.
"""
def add_stock_data(symbol, data):
    # TODO
    return None

"""Get the latest data of the given stock.

Implementation:
    1. Use get_stock_collection() to get the collection of the given stock.
    2. Query (ex: find_one() in pymongo library) to search for the latest data.

Args:
    symbol: A string representing the stock symbol

Return:
    data
"""
def get_latest_data(symbol):
    # TODO
    return None
