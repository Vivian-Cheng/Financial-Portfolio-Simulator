"""Stores configuration settings for the real-time system.

This module contains all parameters used in the real-time system script.
"""

# The maximum number of calls per second per API key
API_RATE_LIMIT = 10
# A list of available API keys
API_KEYS = ["c844d4qad3ide9hefb20",
            "cnfda4pr01qi6ftoi2h0cnfda4pr01qi6ftoi2hg", 
            "c846b7qad3ide9hefshg",
            "cnj1521r01qkq94g71h0cnj1521r01qkq94g71hg",
            "cnj16q1r01qkq94g72u0cnj16q1r01qkq94g72ug",
            "cnj17a9r01qkq94g7390cnj17a9r01qkq94g739g",
            "cnj17m1r01qkq94g73i0cnj17m1r01qkq94g73ig"]
#Store last call time for each API keys
LAST_CALL_TIMES = {
    "c844d4qad3ide9hefb20": None, 
    "cnfda4pr01qi6ftoi2h0cnfda4pr01qi6ftoi2hg": None,        
    "c846b7qad3ide9hefshg": None,
    "cnj1521r01qkq94g71h0cnj1521r01qkq94g71hg": None,
    "cnj16q1r01qkq94g72u0cnj16q1r01qkq94g72ug": None,
    "cnj17a9r01qkq94g7390cnj17a9r01qkq94g739g": None,
    "cnj17m1r01qkq94g73i0cnj17m1r01qkq94g73ig": None
}
# Interval between calls for each symbol in second
SYMBOL_CALL_INTERVAL = 15
# API endpoint
API_URL = "https://finnhub.io/api/v1/quote"
MARKET_API_URL = "https://finnhub.io/api/v1/stock/market-status"
# A list contains all symbols we fetch in the system
SYMBOLS = ["MMM", "AOS", "ABT", "ABBV", "ACN", "ADBE", "AMD", "AES", "AFL", "A", "APD", "ABNB", "AKAM", "ALB", 
           "ARE", "ALGN", "ALLE", "LNT", "ALL", "GOOGL", "GOOG","MO", "AMZN", "AMCR", "AEE", "AAL", "AEP", "AXP", 
           "AIG", "AMT", "AWK", "AMP", "AME", "AMGN", "APH", "ADI", "ANSS", "AON", "APA", "AAPL", "AMAT", "APTV", 
           "ACGL", "ADM", "ANET", "AJG", "AIZ", "T", "ATO", "ADSK", "ADP", "AZO", "AVB", "AVY", "AXON", "BKR", "BALL", 
           "BAC", "BK", "BBWI", "BAX", "BDX", "BRK.B", "BBY", "BIO", "TECH", "BIIB", "BLK", "BX", "BA", "BKNG", "BWA", 
           "BXP", "BSX", "BMY", "AVGO", "BR", "BRO", "BF.B", "BLDR", "BG", "CDNS", "CZR", "CPT", "CPB", "COF", "CAH", 
           "KMX", "CCL", "CARR", "CTLT", "CAT", "CBOE", "CBRE", "CDW", "CE", "COR", "CNC", "CNP", "CF", "CHRW", "CRL", 
           "SCHW", "CHTR", "CVX", "CMG", "CB", "CHD", "CI", "CINF", "CTAS", "CSCO", "C", "CFG", "CLX", "CME", "CMS", 
           "KO", "CTSH", "CL", "CMCSA", "CMA", "CAG", "COP", "ED", "STZ", "CEG", "COO", "CPRT", "GLW", "CTVA", "CSGP", 
           "COST", "CTRA", "CCI", "CSX", "CMI", "CVS", "DHR", "DRI", "DVA", "DAY", "DE", "DAL", "XRAY", "DVN", "DXCM", 
           "FANG", "DLR","DFS", "DG", "DLTR", "D", "DPZ", "DOV", "DOW", "DHI", "DTE", "DUK", "DD", "EMN", "ETN", "EBAY", 
           "ECL", "EIX", "EW", "EA", "ELV", "LLY", "EMR", "ENPH", "ETR", "EOG", "EPAM", "EQT", "EFX", "EQIX", "EQR", "ESS", 
           "EL", "ETSY", "EG", "EVRG", "ES", "EXC", "EXPE", "EXPD", "EXR", "XOM", "FFIV", "FDS", "FICO", "FAST", "FRT", 
           "FDX", "FIS", "FITB", "FSLR", "FE", "FI", "FLT", "FMC", "F", "FTNT", "FTV", "FOXA", "FOX", "BEN", "FCX", "GRMN", 
           "IT", "GEHC", "GEN", "GNRC", "GD", "GE", "GIS", "GM", "GPC", "GILD", "GPN", "GL", "GS", "HAL", "HIG", "HAS", 
           "HCA", "PEAK", "HSIC", "HSY", "HES", "HPE", "HLT", "HOLX", "HD", "HON", "HRL", "HST", "HWM", "HPQ", "HUBB", "HUM", 
           "HBAN", "HII", "IBM", "IEX", "IDXX", "ITW", "ILMN", "INCY", "IR", "PODD", "INTC", "ICE", "IFF", "IP", "IPG", "INTU", 
           "ISRG", "IVZ", "INVH", "IQV", "IRM", "JBHT", "JBL", "JKHY", "J", "JNJ", "JCI", "JPM", "JNPR", "K", "KVUE", "KDP", 
           "KEY", "KEYS", "KMB", "KIM", "KMI", "KLAC", "KHC", "KR", "LHX", "LH", "LRCX", "LW", "LVS", "LDOS", "LEN", "LIN", 
           "LYV", "LKQ", "LMT", "L", "LOW", "LULU", "LYB", "MTB", "MRO", "MPC", "MKTX", "MAR", "MMC", "MLM", "MAS", "MA", "MTCH", 
           "MKC", "MCD", "MCK", "MDT", "MRK", "META", "MET", "MTD", "MGM", "MCHP", "MU", "MSFT", "MAA", "MRNA", "MHK", "MOH", 
           "TAP", "MDLZ", "MPWR", "MNST", "MCO", "MS", "MOS", "MSI", "MSCI", "NDAQ", "NTAP", "NFLX", "NEM", "NWSA", "NWS", "NEE", 
           "NKE", "NI", "NDSN", "NSC", "NTRS", "NOC", "NCLH", "NRG", "NUE", "NVDA", "NVR", "NXPI", "ORLY", "OXY", "ODFL", "OMC", 
           "ON", "OKE", "ORCL", "OTIS", "PCAR", "PKG", "PANW", "PARA", "PH", "PAYX", "PAYC", "PYPL", "PNR", "PEP", "PFE", "PCG", 
           "PM", "PSX", "PNW", "PXD", "PNC", "POOL", "PPG", "PPL", "PFG", "PG", "PGR", "PLD", "PRU", "PEG", "PTC", "PSA", "PHM", 
           "QRVO", "PWR", "QCOM", "DGX", "RL", "RJF", "RTX", "O", "REG", "REGN", "RF", "RSG", "RMD", "RVTY", "RHI", "ROK", "ROL", 
           "ROP", "ROST", "RCL", "SPGI", "CRM", "SBAC", "SLB", "STX", "SRE", "NOW", "SHW", "SPG", "SWKS", "SJM", "SNA", "SO", "LUV", 
           "SWK", "SBUX", "STT", "STLD", "STE", "SYK", "SYF", "SNPS", "SYY", "TMUS", "TROW", "TTWO", "TPR", "TRGP", "TGT", "TEL", 
           "TDY", "TFX", "TER","TSLA", "TXN", "TXT", "TMO", "TJX", "TSCO", "TT", "TDG", "TRV", "TRMB", "TFC", "TYL", "TSN", "USB", 
           "UBER", "UDR", "ULTA", "UNP", "UAL", "UPS", "URI", "UNH", "UHS", "VLO", "VTR", "VLTO", "VRSN", "VRSK", "VZ", "VRTX", 
           "VFC", "VTRS", "VICI", "V", "VMC", "WRB", "WAB", "WBA", "WMT", "DIS", "WBD", "WM", "WAT", "WEC", "WFC", "WELL", "WST", 
           "WDC", "WRK", "WY", "WHR", "WMB", "WTW", "GWW", "WYNN", "XEL", "XYL", "YUM", "ZBRA", "ZBH", "ZION", "ZTS"]

SYMBOLS_100 = SYMBOLS[:100]

RETRY_COUNT = 3
RETRY_DELAY = 1

# The port number of the MongoDB server in localhost
MONGODB_PORT = 8000
# The address of the MongoDB server
MONGODB_SERVER_ADDR = f"mongodb://localhost:{MONGODB_PORT}/"
# Name of the databases in the MongoDB instance
DB_NAME = "db_"
# The data model of a stock quote data
DATA_MODEL = {
    '_id': '_id',
    'current_price': 'c',
    'change': 'd',
    'percent_change': 'dp',
    'high_price': 'h',
    'low_price': 'l',
    'open_price': 'o',
    'prev_close_price': 'pc',
    't': 't',
    'timestamp': 't'
}
# TTL seconds
TTL = 86400
# total buckets for consistent hash
TOTAL_BUCKET = 50
