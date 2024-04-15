import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from datetime import datetime, date
from flask import Flask, request, jsonify
from real_time_system.config import MONGODB_SERVER_ADDR, TOTAL_BUCKET, DB_NAME
from real_time_system.db_handler import connect_mongodb, scan_database, ConsistentHash, migrate_data

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

@app.route('/realtime/dbstats', methods=['GET'])
def dbstats():
    db_list = [name for name in mongo_client.list_database_names() if name.startswith(DB_NAME)]
    db_stat = {'stats':{}, 'collections':{}}
    for db_name in db_list:
        db = mongo_client[db_name]
        db_stat['stats'][db_name] = db.command('dbStats')
        db_stat['collections'][db_name] = {"collections": db.list_collection_names()}
    return jsonify(db_stat)

@app.route('/realtime/commands', methods=['GET'])
def commands():
    db = request.args.get("db")
    collection = request.args.get("collection")
    action = request.args.get("action")
    query = request.args.get("query")

    if action == "drop":
        try:
            result = mongo_client[db][collection].drop()
            print(result)
            return jsonify(message="Success!")
        except Exception as e:
            print(e)
            return jsonify(message="Fail!")
    if action == "count":
        res = mongo_client[db][collection].count_documents({})
        return jsonify(res)
    if action == "remove_expired":
        format_time = datetime.combine(date.today(), 
                                       datetime.strptime("00:00:00", '%H:%M:%S').time())
        res = mongo_client[db][collection].delete_many(
            {'timestamp': {'$lt': format_time}})
        return jsonify(res.deleted_count)
    if action == "drop_all":
        collections = mongo_client[db].list_collection_names()
        for c in collections:
            if c != "dummy":
                mongo_client[db][c].drop()
        return jsonify(message="Success!")
        
@app.route('/realtime/addnode', methods=['GET'])
def addnode():
    new_idx = ch.add_node(str(len(ch.nodes)))
    old_idx = (new_idx + 1) % len(ch.nodes)
    new_node = f"{DB_NAME}{ch.nodes[new_idx]}"
    old_node = f"{DB_NAME}{ch.nodes[old_idx]}"
    migrate_data(mongo_client=mongo_client, old_node=old_node, ch=ch)
    return jsonify({"new_db": new_node, "old_db": old_node})

@app.route('/realtime/deletenode', methods=['GET'])
def deletenode():
    node_id = len(ch.nodes) - 1
    if node_id < 0:
        return jsonify(message="No node to delete")
    node = f"{DB_NAME}{node_id}"
    ch.remove_node(str(node_id))
    migrate_data(mongo_client=mongo_client, old_node=node, ch=ch)
    return jsonify({"db": node})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)