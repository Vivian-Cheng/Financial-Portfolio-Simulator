Financial-Portfolio-Simulator
===

## Overview
Financial Portfolio Simulator is a comprehensive system for managing financial portfolios. It includes real-time and historical data processing systems, as well as a web application for user interaction.

The real-time system fetches stock quotes from an API periodically during market hours and stores the data in a distributed MongoDB database. The historical system processes this data daily into a MySQL database, along with user-specific data from the web app.

The web application, built using Flask for the backend and Streamlit for the frontend, provides users with a platform to view their portfolios, search for stock symbols, and access administrative tools for managing databases.

## Project Structure
```
Financial-Portfolio-Simulator/
│
├── real_time_system/
│   ├── config.py
│   ├── main.py
│   ├── request_handler.py
│   ├── data_processor.py
│   └── db_handler.py
│
└── web/
    ├── server.py
    ├── app.py
    ├── menu.py
    ├── pages/
    │   ├── home.py
    │   ├── symbol.py
    │   ├── portfolio.py
    │   ├── admin_realtime.py
    │   └── admin_historical.py
    │
    └── .streamlit/
        └── config.toml
└── historical_system/
    ├── config.py
    ├── create_initial_databases.sql
    ├── transfer_daily_data.py
    └── update_historical_database.py
```

## real_time_system
This directory implements the required functions for the real-time system, which periodically fetches stock quotes from an API and stores the data into a distributed database.

### Data Model
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

### Files
* `config.py`: Sets up all the global variables and configuration parameters.
* `main.py`: Entry point for the real-time system script. This script imports modules and orchestrates the data retrieval, processing, and writing tasks.
* `request_handler.py`: Provides functions to schedule crawling tasks to retrieve stock quote data.
* `data_processor.py`: Provides functions for processing data before writing it to the database.
* `db_handler.py`: Sets up connections to a database and performs all kinds of queries. Implements data partitioning and other horizontal scaling logic to distribute data.

### Usage

```
python3 real_time_system/main.py "$current_date 13:00:00"
```
## historical_system

## web
This directory implements the required functions for the web system, which includes a backend script implemented using Flask, and frontend scripts implemented using Streamlit.

### Files
* `server.py`: Implements the backend API.
* `app.py`: Implements the login page of the web application.
* `menu.py`: Sets up the menu bar of the web application.
* `pages/home.py`: Implements the home page of the web application.
* `pages/symbol.py`: Implements the page for searched symbols and displays all stock information.
* `pages/portfolio.py`: Implements the user portfolio page of the web application.
* `pages/admin_realtime.py`: Implements the administration page for MongoDB databases.
* `pages/admin_historical.py`: Implements the administration page for MySQL databases.
* `.streamlit/config.toml`: Configuration file for the Streamlit web system.

### Usage
1. run backend script

```
python3 web/server.py
```
2. run frontend app (must run in web folder)
```
cd web
streamlit run app.py
```
