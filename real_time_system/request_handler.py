import requests
import datetime
import time
from config import API_RATE_LIMIT, API_KEYS, LAST_CALL_TIMES, API_URL, MARKET_API_URL, RETRY_COUNT, RETRY_DELAY

"""Handles interactions with the stock API.

This module provides functions to fetch stock data and schedule data retrieval
tasks.

Typical usage example:
    data = run_retrieval("TSLA") # this is the only function that will be called
    from main module
"""

#helper functions
def currenttime():
    """
    Get current time in seconds
    Return: current time as a floating point number
    """
    current_time = datetime.datetime.now()
    #return time in seconds
    return time.time()

def time_since_last_call(last_call_time):
    """
    Calculate the time since last API call
    """
    return currenttime()-last_call_time

def choose_api_key():
    """
    Choose an available API_key by checking
    (current time -last call time) is greater than (1 / API_RATE_LIMIT). 
    If an API_key isn't valid at this moment, try another one, until all API_key has been tried.
    Return: API_key
    """
    max_diff=-1
    chosen_key=None

    for key in API_KEYS:
        last_call_time=LAST_CALL_TIMES[key]
        if last_call_time is None:
            #Update last call time for the chosen key
            LAST_CALL_TIMES[key] = currenttime()
            return key
        else:
            difference = time_since_last_call(last_call_time)
            if difference < 1 / API_RATE_LIMIT:
                continue
            if difference >max_diff:
                max_diff=difference
                chosen_key=key

    #Update the last call time for the chosen key
    LAST_CALL_TIMES[chosen_key] = currenttime()
    #If all keys have reached rate limit, return None
    return chosen_key


#Main
def run_retrieval(symbol):
    """
    Retrieve stock quotes from Finnhub given parameter symbol
    Return: stock quotes in json format
    """
#     print(f"Start run retrieval {symbol}: {datetime.datetime.now()}")
    # Choose an available API key
    api_key = choose_api_key()
    url= f"{API_URL}?symbol={symbol}&token={api_key}"
#     print(f"Request URL: {url} with key {api_key}")
    for _ in range(RETRY_COUNT):
        try:
            response = requests.get(url, timeout=3)
            response.raise_for_status()  # Raise an exception for HTTP errors
        #     print(f"End run retrieval {symbol}: {datetime.datetime.now()}")
            return response.json()
        except requests.exceptions.RequestException as e:
            #Handle request exceptions
            print("Error fetching data:", e)
            time.sleep(RETRY_DELAY)
    return None
    

def check_market_status():
    """
    Check curent market status
    Return:
    If True, market is curently open
    If False, market is curently closed
    """
    api_key = choose_api_key()
    is_open = False
    status_forcelist=[429, 500, 502, 503, 504]
    params = {'exchange': 'US', 'token': api_key }
    for _ in range(RETRY_COUNT):
        try:
            res = requests.get(MARKET_API_URL, params=params)
            if res.status_code in status_forcelist:
                continue
            break
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            time.sleep(RETRY_DELAY)
    if res.status_code == 200:
        data = res.json()
        is_open = data.get('isOpen', False)
    else:
        #handle error cases
        print("Error fetching market status")
    return is_open


#test case
# sym = ["MMM", "AOS", "ABT", "ABBV", "ACN", "ADBE", "AMD", "AES", "AFL", "A", "APD", "ABNB", "AKAM", "ALB", 
#            "ARE", "ALGN", "ALLE", "LNT", "ALL", "GOOGL", "GOOG","MO", "AMZN", "AMCR", "AEE", "AAL", "AEP", "AXP"] 
# sym = ["MMM", "AOS", "ABT", "ABBV", "ACN", "ADBE", "AMD", "AES", "AFL", "A", "APD", "ABNB", "AKAM", "ALB", 
#            "ARE", "ALGN", "ALLE", "LNT", "ALL", "GOOGL", "GOOG","MO", "AMZN", "AMCR", "AEE", "AAL", "AEP", "AXP", 
#            "AIG", "AMT", "AWK", "AMP", "AME", "AMGN", "APH", "ADI", "ANSS", "AON", "APA", "AAPL", "AMAT", "APTV", 
#            "ACGL", "ADM", "ANET", "AJG", "AIZ", "T", "ATO", "ADSK", "ADP", "AZO", "AVB", "AVY", "AXON", "BKR", "BALL", 
#            "BAC", "BK", "BBWI", "BAX", "BDX", "BRK.B", "BBY", "BIO", "TECH", "BIIB", "BLK", "BX", "BA", "BKNG", "BWA", 
#            "BXP", "BSX", "BMY", "AVGO", "BR", "BRO", "BF.B", "BLDR", "BG", "CDNS", "CZR", "CPT", "CPB", "COF", "CAH", 
#            "KMX", "CCL", "CARR", "CTLT", "CAT", "CBOE", "CBRE", "CDW", "CE", "COR", "CNC", "CNP", "CF", "CHRW", "CRL", 
#            "SCHW", "CHTR", "CVX", "CMG", "CB", "CHD", "CI", "CINF", "CTAS", "CSCO", "C", "CFG", "CLX", "CME", "CMS", 
#            "KO", "CTSH", "CL", "CMCSA", "CMA", "CAG", "COP", "ED", "STZ", "CEG", "COO", "CPRT", "GLW", "CTVA", "CSGP", 
#            "COST", "CTRA", "CCI", "CSX", "CMI", "CVS", "DHR", "DRI", "DVA", "DAY", "DE", "DAL", "XRAY", "DVN", "DXCM", 
#            "FANG", "DLR","DFS", "DG", "DLTR", "D", "DPZ", "DOV", "DOW", "DHI", "DTE", "DUK", "DD", "EMN", "ETN", "EBAY", 
#            "ECL", "EIX", "EW", "EA", "ELV", "LLY", "EMR", "ENPH", "ETR", "EOG", "EPAM", "EQT", "EFX", "EQIX", "EQR", "ESS", 
#            "EL", "ETSY", "EG", "EVRG", "ES", "EXC", "EXPE", "EXPD", "EXR", "XOM", "FFIV", "FDS", "FICO", "FAST", "FRT", 
#            "FDX", "FIS", "FITB", "FSLR", "FE", "FI", "FLT", "FMC", "F", "FTNT", "FTV", "FOXA", "FOX", "BEN", "FCX", "GRMN", 
#            "IT", "GEHC", "GEN", "GNRC", "GD", "GE", "GIS", "GM", "GPC", "GILD", "GPN", "GL", "GS", "HAL", "HIG", "HAS", 
#            "HCA", "PEAK", "HSIC", "HSY", "HES", "HPE", "HLT", "HOLX", "HD", "HON", "HRL", "HST", "HWM", "HPQ", "HUBB", "HUM", 
#            "HBAN", "HII", "IBM", "IEX", "IDXX", "ITW", "ILMN", "INCY", "IR", "PODD", "INTC", "ICE", "IFF", "IP", "IPG", "INTU", 
#            "ISRG", "IVZ", "INVH", "IQV", "IRM", "JBHT", "JBL", "JKHY", "J", "JNJ", "JCI", "JPM", "JNPR", "K", "KVUE", "KDP", 
#            "KEY", "KEYS", "KMB", "KIM", "KMI", "KLAC", "KHC", "KR", "LHX", "LH", "LRCX", "LW", "LVS", "LDOS", "LEN", "LIN", 
#            "LYV", "LKQ", "LMT", "L", "LOW", "LULU", "LYB", "MTB", "MRO", "MPC", "MKTX", "MAR", "MMC", "MLM", "MAS", "MA", "MTCH", 
#            "MKC", "MCD", "MCK", "MDT", "MRK", "META", "MET", "MTD", "MGM", "MCHP", "MU", "MSFT", "MAA", "MRNA", "MHK", "MOH", 
#            "TAP", "MDLZ", "MPWR", "MNST", "MCO", "MS", "MOS", "MSI", "MSCI", "NDAQ", "NTAP", "NFLX", "NEM", "NWSA", "NWS", "NEE", 
#            "NKE", "NI", "NDSN", "NSC", "NTRS", "NOC", "NCLH", "NRG", "NUE", "NVDA", "NVR", "NXPI", "ORLY", "OXY", "ODFL", "OMC", 
#            "ON", "OKE", "ORCL", "OTIS", "PCAR", "PKG", "PANW", "PARA", "PH", "PAYX", "PAYC", "PYPL", "PNR", "PEP", "PFE", "PCG", 
#            "PM", "PSX", "PNW", "PXD", "PNC", "POOL", "PPG", "PPL", "PFG", "PG", "PGR", "PLD", "PRU", "PEG", "PTC", "PSA", "PHM", 
#            "QRVO", "PWR", "QCOM", "DGX", "RL", "RJF", "RTX", "O", "REG", "REGN", "RF", "RSG", "RMD", "RVTY", "RHI", "ROK", "ROL", 
#            "ROP", "ROST", "RCL", "SPGI", "CRM", "SBAC", "SLB", "STX", "SRE", "NOW", "SHW", "SPG", "SWKS", "SJM", "SNA", "SO", "LUV", 
#            "SWK", "SBUX", "STT", "STLD", "STE", "SYK", "SYF", "SNPS", "SYY", "TMUS", "TROW", "TTWO", "TPR", "TRGP", "TGT", "TEL", 
#            "TDY", "TFX", "TER","TSLA", "TXN", "TXT", "TMO", "TJX", "TSCO", "TT", "TDG", "TRV", "TRMB", "TFC", "TYL", "TSN", "USB", 
#            "UBER", "UDR", "ULTA", "UNP", "UAL", "UPS", "URI", "UNH", "UHS", "VLO", "VTR", "VLTO", "VRSN", "VRSK", "VZ", "VRTX", 
#            "VFC", "VTRS", "VICI", "V", "VMC", "WRB", "WAB", "WBA", "WMT", "DIS", "WBD", "WM", "WAT", "WEC", "WFC", "WELL", "WST", 
#            "WDC", "WRK", "WY", "WHR", "WMB", "WTW", "GWW", "WYNN", "XEL", "XYL", "YUM", "ZBRA", "ZBH", "ZION", "ZTS"]
# for s in sym:
#     data= run_retrieval(s)
#     print(data)
# print(LAST_CALL_TIMES)
# SYMBOLS_first_100 = sym[:150]
# start = time.time()
# with futures.ThreadPoolExecutor(max_workers=7) as executor:
#     res = executor.map(run_retrieval,SYMBOLS_first_100)
# end = time.time()
# print(f"run time: {end - start}")
# print(list(res))
# market_status = check_market_status()
# if market_status is not None:
#     if market_status:
#         print("The market is currently open.")
#     else:
#         print("The market is currently closed.")
# else:
#     print("Unable to determine market status at this time.")
