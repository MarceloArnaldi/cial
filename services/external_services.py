from services.polygon_service     import get_polygon_data
from services.marketwatch_service import get_marketwatch_data

def get_stock_data(symbol: str, date: str):
    polygon = get_polygon_data(symbol.upper(), date)
    market  = get_marketwatch_data(symbol.upper())
    response = {
        'Status'           : polygon['status'],
        'purchased_amount' : 0,
        'purchased_status' : 'not_purchased',
        'request_data'     : polygon['date'],
        'company_code'     : polygon['symbol'],
        'company_name'     : market['company_name'],
        'Stock_values'     : {
            'open'  : polygon['open'],
            'high'  : polygon['high'],
            'low'   : polygon['low'],
            'close' : polygon['close'],
        },
        'performance_data' : market['performance_data'],
        'Competitors'      : market['competitors']
    }
    return response