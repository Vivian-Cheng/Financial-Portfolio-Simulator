import os
import sys
from datetime import datetime
from flask import Flask, request, jsonify
import mysql.connector

# Flask app
app = Flask(__name__)

# Connect to MySQL database
mysql_conn = mysql.connector.connect(
    host='localhost',
    user='dsci551',
    password='',
    database='STOCK'
)

# Cursor for executing queries
mysql_cursor = mysql_conn.cursor()

#HISTORICAL
@app.route('/stock_data', methods=['GET'])
def get_stock_data():
    """
    Price in a time span from “start” to “end”
    Arg: Symbol,start,end
    Return: json
    """
    symbol = request.args.get('symbol')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = f"SELECT symbol, hdate, o, h, l, c FROM stockhistory WHERE symbol = %s AND hdate BETWEEN %s AND %s"
    mysql_cursor.execute(query,(symbol, start_date, end_date))
    data = mysql_cursor.fetchall()

    if data:
        return jsonify(data)
    else:
        return jsonify({"message": "No data found for the symbol"})


@app.route('/db_stats', methods=['GET'])
def get_db_stats():
    """
    Database Baisc Stats
    Arg: table_name, table_schema, engine, 
         table_rows (# of rows in a table),
         update_time (last time table was updated)
    Return: json
    """
    #Get summary
    mysql.cursor.execute("SELECT table_name, table_schema, engine, table_rows, update_time from information_schema.tables")
    summary_stats=mysql_cursor.fetchall()
    
    return jsonify(summary_stats)

@app.route('/data_availability', methods=['GET'])
def get_data_availability():
    """
    Display data updates
    Arg: Date, Availability
    Return: json
    """
    mysql.cursor.execute("""SELECT sh.hdate AS Date, CONCAT(count(sh.symbol),'/', s.total_stock_count) AS Availability 
                         FROM stockhistory sh 
                         JOIN (SELECT count(*) AS total_stock_count FROM stocks) AS s 
                         ON 1=1 
                         GROUP BY sh.hdate""")
    data_availability=mysql_cursor.fetchall()
    
    return jsonify(data_availability)

#PORTFOLIO
@app.route('/user_verif', methods=['GET'])
def user_verification():
    """
    Verify user log in information
    Arg: username, password
    Return: True/False
    """
    usrname = request.args.get('username')
    passwrd = request.args.get('password')
    query = """
            SELECT 
                CASE 
                    WHEN COUNT(*) > 0 THEN 'true'
                    ELSE 'false'
                END AS is_verified
            FROM 
                users
            WHERE 
                username = %s AND 
                password = %s
            """
    mysql_cursor.execute(query, (usrname, passwrd))
    result = mysql_cursor.fetchone()[0]
    
    return str(bool(result))


@app.route('/user_registration', methods=['POST'])
def user_registration():
    """
    User registration, insert data if user doesn't exist
    Arg: username
    Return: True/False
    """
    usrname = request.args.get('username')
    query = """
            INSERT IGNORE INTO users (username) 
            VALUES (%s)
            """
    try:
        mysql_cursor.execute(query, (usrname,))
        mysql_conn.commit()
        return True  #If successfully inserted
    except mysql.connector.Error as err:
        if err.errno == 1062:  #Duplicate entry error
            return False  #User already exists
        else:
            return 'Error: {}'.format(err)  # Other error


@app.route('/transaction', methods=['POST'])
def get_transaction():
    """
    Handles Buy/Sell on Webpage.
    If user purchase or sell stocks, database will be automatically updated with the changes
    Return: message
    """
    #NEED TO ADJUST CODE IN WEBPAGE TO ENSURE THAT WHEN USER PRESS "BUY" THE VOLUME IS POSITIVE, 
    #AND WHEN "SELL", THE VOLUME SHOULD BE THE INPUTET VOLUME VALUE*(-1)
    symbol = request.json.get('symbol')
    volume = request.json.get('volume')
    current_username= request.json.get('username') #I DONT KNOW HOW TO GET THIS!!!
    current_time= datetime.now()

    if not (symbol and volume and current_username):
        return jsonify({'message': 'Invalid request parameters.'}), 400
    
    #Retrieve the user ID corresponding to the provided username
    mysql_cursor.execute("SELECT id FROM users WHERE username = %s", (current_username,))
    user_id = mysql_cursor.fetchone()
    if not user_id:
        return jsonify({'message': f"User with username {current_username} not found."}), 404
    user_id = user_id[0]

    
    # Insert transaction into transactions table
    if volume > 0:
        # User is buying
        mysql_cursor.execute("INSERT INTO transactions (buyerId, symbol, volume, txnTime) VALUES (%s, %s, %s, %s)", 
                            (user_id, symbol, volume, current_time))
    elif volume < 0:
        # User is selling
        mysql_cursor.execute("INSERT INTO transactions (buyerId, symbol, volume, txnTime) VALUES (%s, %s, %s, %s)", 
                            (user_id, symbol, -volume, current_time))
    else:
        return jsonify({'message': 'Volume must be nonzero.'}), 400
    mysql_conn.commit()

    # Update inventory table
    if volume >0:
        mysql_cursor.execute("UPDATE inventory SET volume = volume + %s WHERE symbol = %s and userId= %s ", (volume, symbol, user_id))
    else:  #Sell
        mysql_cursor.execute("UPDATE inventory SET volume = volume - %s WHERE symbol = %s and userId= %s ", (-volume, symbol, user_id))
    
    mysql_conn.commit()

    return jsonify({'message': 'Transaction processed successful.'})


@app.route('/user_info', methods=['GET'])
def get_user_info():
    """
    Display user info in the Portfolio Page
    Arg: ID, username
    Return: json
    """
    usrname = request.args.get('username')
    query = "SELECT * FROM users WHERE username = %s"
    mysql_cursor.execute(query, (usrname, ))
    user_info = mysql_cursor.fetchone()
    
    return jsonify(user_info)

@app.route('/user_inventory', methods=['GET'])
def get_user_inventory():
    """
    Display current user's list of inventories
    Arg: symbol, volume
    Return: json
    """
    usrname = request.args.get('username')
    query = """SELECT symbol, volume 
                FROM inventory i
                JOIN users u ON i.userId=u.id
                WHERE u.username = %s"""
    mysql_cursor.execute(query, (usrname, ))
    user_inv = mysql_cursor.fetchall()
    
    return jsonify(user_inv)



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

