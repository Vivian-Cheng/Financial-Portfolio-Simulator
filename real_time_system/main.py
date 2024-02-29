import sys
import sched
import time
import datetime
import threading
import logging
from queue import Queue
from config import SYMBOL_CALL_INTERVAL, SYMBOLS, MONGODB_SERVER_ADDR, DB_NAME, TOTAL_BUCKET, MARKET_API_URL
from request_handler import run_retrieval, check_market_status
from db_handler import connect_mongodb, scan_database, ConsistentHash, get_or_create_collection, insert_one
from data_processor import transform_data

"""Entry point for the real-time system script.

This script imports modules and orchestrates the data retrieval, processing,
and writing tasks.
"""

logging.basicConfig(level=logging.INFO)
# create a thread-safe processing queue
q = Queue()

"""First procedure of api thread.
"""
def run_api_thread(terminate_time):
    logging.info("Start api thread")
    scheduler = sched.scheduler(time.time, time.sleep)
    for symbol in SYMBOLS:
        scheduler.enter(0, 1, schedule_retrieval, 
                        (scheduler, symbol, terminate_time, ))
    scheduler.run()
    logging.info("End api thread: termination time")

"""Repeat the retrieval task for the given symbol to run every 
SYMBOL_CALL_INTERVAL second.
"""
def schedule_retrieval(scheduler, symbol, terminate_time):
    data = run_retrieval(symbol)
    if data == None:
        logging.error("Retrieve None data.")
    logging.info(f"Retrieve {symbol} data: {data}")
    q.put((symbol, data))
    if datetime.datetime.now() < terminate_time:
        scheduler.enter(SYMBOL_CALL_INTERVAL, 1, schedule_retrieval, 
                        (scheduler, symbol, terminate_time))

"""First procedure of data thread.
"""
def run_data_thread(client, consistent_hash, terminate_time):
    logging.info("Start data thread")
    while datetime.datetime.now() < terminate_time:
        if not q.empty():
            data = q.get()
            ret = process_data(data[0], data[1], client, consistent_hash)
            if ret == -1:
                raise Exception("Insert one data error!")
    print("End data thread: termination time")

"""Process data in queue and insert the transformed data into database.
"""
def process_data(symbol, data, client, consistent_hash):
    trans_data = transform_data(symbol, data)
    db_id = consistent_hash.get_node(symbol)
    db_name = DB_NAME + db_id
    collection = get_or_create_collection(db=client[db_name], name=symbol)
    ret = insert_one(collection=collection, doc=trans_data)
    logging.info(f"Insert one data intto database: {db_name} collection: {symbol}")
    return ret


def main():
    # get program termination time from input
    if len(sys.argv) < 2:
        raise Exception("Missing argument: termination time")
    terminate_time = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d %H:%M:%S")
    logging.info(f"Program start, will terminate at {terminate_time}")

    # check market status
    is_open = check_market_status()

    # establich connection to MongoDB server
    client = connect_mongodb(MONGODB_SERVER_ADDR)
    if client == None:
        raise Exception(f"Cannot establish connection to MongoDB server at {MONGODB_SERVER_ADDR}")
    logging.info(f"Establish connection to MongoDB server at {MONGODB_SERVER_ADDR}")
    # scan to get the number of available databases
    num_database = scan_database(client)
    if num_database == 0:
        raise Exception("No available database")
    logging.info(f"Scan databases: total {num_database} are available")

    # initialize consistent hash
    consistent_hash = ConsistentHash(num_bucket=TOTAL_BUCKET, num_db=num_database)

    if is_open:
        logging.info(f"Market is open today")
        # Set up API thread for handling request to API
        api_thread = threading.Thread(target=run_api_thread, args=(terminate_time, ))
        # Set up data thread for data processing tasks
        data_thread = threading.Thread(target=run_data_thread, args=(client, consistent_hash, terminate_time,))

        api_thread.start()
        data_thread.start()
        
        api_thread.join()
        data_thread.join()
    else: # fetch one data for each symbol if market is close today
        logging.info(f"Market is close today")
        for symbol in SYMBOLS:
            data = run_retrieval(symbol)
            q.put((symbol, data))
    
    # process remaining data in queue
    while not q.empty():
        data = q.get()
        ret = process_data(data[0], data[1], client, consistent_hash)
        if ret == -1:
            raise Exception("Insert one data error!")
    
if __name__ == '__main__':
    main()
