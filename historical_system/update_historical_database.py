import argparse
import pymysql.cursors
import requests
import time
from datetime import date

from config import SYMBOLS_100

SYSTEM_START_DATE = '2024-01-01'
DP_LIMIT_PER_REQUEST = 5000 # API data points limit
API_URL = 'https://api.twelvedata.com/time_series'
API_KEYS = ['20ef5859153949dbb34c56237f446abe']
API_KEY = API_KEYS[0]

db_connection = pymysql.connect(
    host='localhost',
    user='dsci551',
    password='',
    database='STOCK',
    cursorclass=pymysql.cursors.DictCursor
)


def update_table_stocks(symbols = SYMBOLS_100, names = SYMBOLS_100):
    assert len(symbols) == len(names)
    val = [(symbols[i], names[i]) for i in range(len(symbols))]
    with db_connection:
        with db_connection.cursor() as cursor:
            sql = "INSERT INTO stocks VALUES (%s, %s)"
            cursor.executemany(sql, val)
        db_connection.commit()


def get_historical_data(start = SYSTEM_START_DATE, end = date.today().isoformat(), \
                        symbols = SYMBOLS_100):
    dp_per_symbol = 1 + (date.fromisoformat(end) - date.fromisoformat(start)).days
    if dp_per_symbol <= 0: return []
    assert dp_per_symbol < DP_LIMIT_PER_REQUEST
    symbol_per_request = min(int(DP_LIMIT_PER_REQUEST / dp_per_symbol), 7)

    payload = {
        'symbol': '',
        'interval': '1day',
        'apikey': API_KEY,
        'order': 'ASC',
        'start_date': start,
        'end_date': end
    }

    res = {}
    request_cnt = 0
    total_cnt = 0
    for i in range(0, len(symbols), symbol_per_request):
        if(request_cnt + symbol_per_request > 7):
            time.sleep(70) # API minutely maximum: 8 symbols
            request_cnt = 0

        s = symbols[i : i + symbol_per_request]
        payload.update({'symbol': ','.join(s)})
        r = requests.get(API_URL, params=payload)
        r.raise_for_status()
        if r.status_code == 200 and ('code' not in r.json()):
            if len(s) > 1:
                res.update(r.json())
            else:
                res.update({s[0]: r.json()})
        else:
            assert False, "request error"

        request_cnt += symbol_per_request
        total_cnt += len(s)
        print(f"{total_cnt} out of {len(symbols)} completed")

    data = []
    for key, value in res.items():
        assert value['status'] == "ok"
        for dp in value['values']:
            data.append((key, dp['datetime'][0:10], dp['open'], dp['high'], dp['low'], \
                         dp['close'], dp['volume']))

    return data


def insert_into_sql_db(data):
    with db_connection:
        with db_connection.cursor() as cursor:
            sql = "INSERT INTO stockhistory VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, data)
        db_connection.commit()


if __name__ == '__main__':
    aparser = argparse.ArgumentParser()
    aparser.add_argument(
        "-s",
        "--symbol",
        action="store_true",
        help="only update table stocks"
    )
    args = aparser.parse_args()

    if args.symbol:
        update_table_stocks()
    else:
        data = get_historical_data()
        insert_into_sql_db(data)
