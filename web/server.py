import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from datetime import datetime, date
from flask import Flask, request, jsonify
from real_time_system.config import MONGODB_SERVER_ADDR, TOTAL_BUCKET, DB_NAME
from real_time_system.db_handler import connect_mongodb, scan_database, ConsistentHash

# Flask app
app = Flask(__name__)

# Connect to MongoDB
mongo_client = connect_mongodb(MONGODB_SERVER_ADDR)
if mongo_client == None:
    raise Exception(f"Cannot establish connection to MongoDB server at {MONGODB_SERVER_ADDR}")
num_db = scan_database(mongo_client)
if num_db == 0:
    raise Exception("No available database")
ch = ConsistentHash(num_bucket=TOTAL_BUCKET, num_db=num_db)

def get_realtime_stock_collection(symbol):
    db_id = ch.get_node(symbol)
    db_name = DB_NAME + db_id
    print(db_name)
    return mongo_client[db_name][symbol]

"""sample output:
[
  {
    "_id": "AAPL_2024-03-14 18:58:34.912639",
    "change": 1.87,
    "current_price": 173,
    "high_price": 174.3078,
    "low_price": 172.05,
    "open_price": 172.94,
    "percent_change": 1.0927,
    "prev_close_price": 171.13,
    "t": 1710446401,
    "timestamp": "Thu, 14 Mar 2024 18:58:34 GMT"
  }
]
"""
@app.route('/quote', methods=['GET'])
def quote():
    symbol = request.args.get("symbol")
    collection = get_realtime_stock_collection(symbol)
    latest_data = collection.find().sort('timestamp', -1).limit(1)
    return jsonify(list(latest_data))

"""sample output:
[
  {
    "current_price": 173,
    "timestamp": "Thu, 14 Mar 2024 18:58:34 GMT"
  },
  {
    "current_price": 173,
    "timestamp": "Thu, 14 Mar 2024 21:58:52 GMT"
  }
]
"""
@app.route('/quote_chart', methods=['GET'])
def quote_chart():
    symbol = request.args.get('symbol')
    start = request.args.get('start')
    end = request.args.get('end')

    format_start = datetime.combine(date.today(), datetime.strptime(start, '%H:%M:%S').time())
    format_end = datetime.combine(date.today(), datetime.strptime(end, '%H:%M:%S').time())

    query = {
        'timestamp': {
            '$gte': format_start,
            '$lte': format_end
        }
    }

    collection = get_realtime_stock_collection(symbol)
    data = collection.find(query, {'_id': 0, 'current_price': 1, 'timestamp': 1})
    
    return jsonify(list(data))



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
