import requests
from bs4 import BeautifulSoup
from services.tools import extract_table_with_headers, parse_float, extract_table, get_value_by_key

def get_marketwatch_data(symbol: str):
    url = f'https://www.marketwatch.com/investing/stock/{symbol.lower()}'

    perf_selector = {
        'class': 'table table--primary no-heading c2'
    }
    comp_selector = {
        'class': 'table table--primary align--right',
        'aria-label': 'Competitors data table'
    }

    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/124.0.0.0 Safari/537.36'
        ),
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': 'https://www.google.com/',
    }   

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    company_name_tag = soup.find('h1', class_='company__name')
    company_name = company_name_tag.text.strip() if company_name_tag else 'N/A'

    # performance
    performance_data = extract_table(url, perf_selector)
    print(performance_data)
    print(get_value_by_key(performance_data,'5 Day'))
    performance_data = {
        'five_days'    : parse_float(get_value_by_key(performance_data,'5 Day')),
        'one_month'    : parse_float(get_value_by_key(performance_data,'1 Month')),
        'three_months' : parse_float(get_value_by_key(performance_data,'3 Month')),
        'year_to_date' : parse_float(get_value_by_key(performance_data,'YTD')),
        'one_year'     : parse_float(get_value_by_key(performance_data,'1 Year')),
    }
    # performance_data = extract_table_with_headers(url, perf_selector)
    # performance_data = {
    #     'five_days'    : parse_float(performance_data['5_day']),
    #     'one_month'    : parse_float(performance_data['1_month']),
    #     'three_months' : parse_float(performance_data['3_month']),
    #     'year_to_date' : parse_float(performance_data['ytd']),
    #     'one_year'     : parse_float(performance_data['1_year'])
    # }
    
    # competitors
    competitors = []
    competitors_ = extract_table(url, comp_selector)
    for competitor in competitors_:
        if competitor:
            nome       = competitor[0]
            variacao   = competitor[1]
            market_cap = competitor[2]
            it = { 
                'name' : nome,
                'market_cap' : {
                    'Currency': variacao,
                    'Value': market_cap
                }
            }
            competitors.append(it)

    return {
        'company_name'     : company_name,
        'performance_data' : performance_data,
        'competitors'      : competitors
    }
