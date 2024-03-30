Financial-Portfolio-Simulator
===

## System Design

### Real-time system
Periodically fetch stock quote from API and store data into a distributed database.

**1. Request Scheduler**
Check the market opening hour on a daily basis and schedule Request Handler.

**2. Request Handler**
Schedule crawling task to retrieve stock quote data.

**3. DB Handler**
Implement data partitioning and other  horizontal scaling logic to distribute data.

**4. Distributed DB**
Construct a distributed database.

#### Data Model
In the MongoDB setup, each stock's data is distributed across multiple databases within a single MongoDB server. In each database, stock data is stored in a collection named after the stock symbol. Below is an example:
```jsonld
'AAPL' // collection name
{
    '_id': 'a unique id of this data, ex: AAPL_timestamp',
    'current_price': 'current price',
    'change': 'change',
    'percent_change': 'percent change',
    'high_price': 'high price',
    'low_price': 'low price',
    'open_price': 'open price',
    'prev_close_price': 'prev close price',
    't': 'timestamp from API',
    'timestamp': ISODate()

},{
    ...
}
```

## Web
How to run the app
1. run backend script

```
python3 web/server.py
```
2. run frontend app (must run in web folder)
```
cd web
streamlit run app.py
```
