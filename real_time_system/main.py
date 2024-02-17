from config import SYMBOL_CALL_INTERVAL, SYMBOLS, MONGODB_SERVER
from db_handler import start_mongodb
from queue import Queue
import request_handler
import sched
import time
import threading

"""Entry point for the real-time system script.

This script imports modules and orchestrates the data retrieval, processing,
and writing tasks.
"""

ava_mongodb = {}

"""Schedule retrieval task.

Repeat the retrieval task for the given symbol to run every 
SYMBOL_CALL_INTERVAL second.

Args:
    scheduler: An sched.scheduler() instance.
    symbol: A string representing the stock symbol.
    q: An Queue instance.
"""
def schedule_retrieval(scheduler, symbol, q):
    data = request_handler.run_retrieval(symbol)
    q.put(data)
    scheduler.enter(SYMBOL_CALL_INTERVAL, 1, schedule_retrieval, (scheduler, symbol, q))

"""Process the fetched data and insert it into the database.

Args:
    q: An Queue instance.
"""
def process_data(q):
    while True:
        if not q.empty():
            #TODO
            print(q.get())
            print(time.strftime("%H:%M:%S", time.localtime()))
            q.task_done()

"""Setup connection to the available MongoDB instances.
"""
def setup_db():
    for node_key, url in MONGODB_SERVER.items():
        db = start_mongodb(url)
        if db == None:
            continue
        ava_mongodb[node_key] = db

# TODO Vivian - check the Python threading library and ensure all threads will be cleaned when program ends.
def main():
    q = Queue()
    scheduler = sched.scheduler(time.time, time.sleep)
    for symbol in SYMBOLS:
        scheduler.enter(0, 1, schedule_retrieval, (scheduler, symbol, q))
    # Setup a separating thread for data processing tasks
    threading.Thread(target=process_data, args=(q,), daemon=True).start()
    # Setup main thread for data retrieval tasks
    scheduler.run()

if __name__ == '__main__':
    main()
