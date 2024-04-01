import pymongo
import hashlib
import logging
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from bisect import bisect, bisect_left, bisect_right
from real_time_system.config import DATA_MODEL, TTL, DB_NAME

"""Handles query to the database.

This module provides function to setup connection to a database and performs all
kinds of queries to the database.
"""

"""Setup connection to a MongoDB instance.

Args:
    addr: A string representing the URL and IP address of the database.

Return:
    An pymongo.MongoClient() instance or None when error occurs.
"""
def connect_mongodb(addr):
    try:
        client = pymongo.MongoClient(addr)
    except Exception as e:
        logging.error(f"Connect to MongoDB error: {e}")
        return None
    return client

"""Scan MongoDB server to get the number of available databases.

Args:
    client: An pymongo.MongoClient() instance
Return:
    An int representing the number of available databases.
"""
def scan_database(client):
    cnt = 0
    db_list = client.list_database_names()
    for db_name in db_list:
        cnt += 1 if DB_NAME in db_name else 0
    return cnt

"""Get a collection with specific name in the given database, or create
the collection with given name and TTL index if the collection doesn't exist.

Args:
    db: A MongoDB database instance.
    name: A string representing the name of the specific collection.

Return:
    A MongoDB collection instance.
"""
def get_or_create_collection(db, name):
    if name in db.list_collection_names():
        return db[name]
    collection = db[name]
    collection.create_index(DATA_MODEL['timestamp'], expireAfterSeconds = TTL)
    return collection

"""Insert a document into collection.

Args:
    collection: An MongoDB collection instance.
    doc: A dict representing the document(data) we want to insert.

Return:
    A string representing the ID of inserted document, or -1 if error occurs. 
"""
def insert_one(collection, doc):
    try:
        res = collection.insert_one(doc)
        return res.inserted_id
    except Exception as e:
        logging.error(f"Insert one document error: {e}")
        return -1

"""Insert documents into collection.

Args:
    collection: An MongoDB collection instance.
    docs: A list of dict representing the documents(data) we want to insert.

Return:
    A list of number representing the _id values of the inserted
    documents, or None if error occurs.
"""
def insert_many(collection, docs_list):
    try:
        res = collection.insert_many(docs_list)
        return res.inserted_ids
    except Exception as e:
        logging.error(f"Insert many documents error: {e}")
        return None

"""Creates an integer equivalent of a SHA256 hash and
takes a modulo with the total number of buckets in hash space.
"""
def hash_fn(key: str, num_bucket: int):
    return int(hashlib.sha256(bytes(key.encode('utf-8'))).hexdigest(), 16) % num_bucket


class ConsistentHash():
    """ConsistentHash represents an array based implementation of
    consistent hashing algorithm.
    ref: https://www.codementor.io/@arpitbhayani/consistent-hashing
    -with-binary-search-16rec8e8eh
    """
    def __init__(self, num_bucket, num_db = 0):
        self.keys = []  # array stores the hash keys of nodes in sorted order
        self.nodes = [] # node ids present int the ring
        self.num_bucket = num_bucket # total bucket in the ring
        if (num_db != 0):
            self.init_node(num_db)
    
    def init_node(self, num_node):
        """Initialize keys[] and nodes[]."""

        for i in range(num_node):
            self.add_node(str(i))

    def add_node(self, node_id: str):
        """Add a new node and return the inserted index."""

        # handle error when the hash space is full
        if len(self.keys) == self.num_bucket:
            raise Exception("Hash space is full!")
        # get the hash key of the given node
        key = hash_fn(node_id, self.num_bucket)
        # get the index where hash key should be inserted and maintain the
        # result sorted
        index = bisect(self.keys, key)
        # handle collistion error if the hash key already exists
        if index > 0 and self.keys[index - 1] == key:
            raise Exception("Collision occurred!")
        # insert the hash key and node id with the same index
        self.keys.insert(index, key)
        self.nodes.insert(index, node_id)

        return index

    def remove_node(self, node_id: str):
        """Remove a node and return its index."""

        # handle error when hash space is empty
        if len(self.keys) == 0:
            raise Exception("Hash space is empty!")
        # get the hash key of the given node
        key = hash_fn(node_id, self.num_bucket)
        # get the index where the node reside
        index = bisect_left(self.keys, key)
        # handle error if node does not exist
        if index >= len(self.keys) or self.keys[index] != key:
            raise Exception("Node does not exist")
        # remove the hash key and node id
        self.keys.pop(index)
        self.nodes.pop(index)

        return index
    
    def get_node(self, item: str):
        """Given an item, the function returns the node id it is associated
        with.
        """

        key = hash_fn(item, self.num_bucket)
        index = bisect_right(self.keys, key) % len(self.keys)
        return self.nodes[index]


def migrate_data(mongo_client, old_node, ch):
    old_db = mongo_client[old_node]
    collections = old_db.list_collection_names()
    for collection_name in collections:
        new_node = DB_NAME + ch.get_node(collection_name)
        if collection_name != "dummy" and new_node != old_node:
            logging.info(f"Move {collection_name} from {old_node} to {new_node}")
            new_db = mongo_client[new_node]
            collection = old_db[collection_name]
            target_collection = new_db[collection_name] 
            target_collection.insert_many(collection.find())
            collection.drop()
