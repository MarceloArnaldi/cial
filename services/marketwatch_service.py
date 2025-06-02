import requests
from bs4 import BeautifulSoup

def get_marketwatch_data(symbol: str):
    url = f'https://www.marketwatch.com/investing/stock/{symbol.lower()}'
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
    if response.status_code != 200:
        raise Exception("Erro ao acessar a página da MarketWatch")

    soup = BeautifulSoup(response.text, 'lxml')

    # print('Classes of each table:')
    # for table in soup.find_all('table'):
    #     print(table.get('class'))

    company_name_tag = soup.find('h1', class_='company__name')
    company_name = company_name_tag.text.strip() if company_name_tag else 'N/A'

    # performance data
    performance_table = soup.find('table', class_='table table--primary no-heading c2')
    performance_data_ = {}
    if performance_table:
        rows = performance_table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) == 2:
                label = cols[0].text.strip().lower().replace(' ', '_')
                value_text = cols[1].text.strip().replace('%', '').replace(',', '')
                try:
                    value = float(value_text)
                except ValueError:
                    value = None
                performance_data_[label] = value
    else:
        performance_data_ = {
            '5_day'   : None,
            '1_month' : None,
            '3_month' : None,
            'ytd'     : None,
            '1_year'  : None
        }
    
    performance_data = {
        'five_days'    : performance_data_['5_day'],
        'one_month'    : performance_data_['1_month'],
        'three_months' : performance_data_['3_month'],
        'year_to_date' : performance_data_['ytd'],
        'one_year'     : performance_data_['1_year']
    }

    # competitors
    competitors_table = soup.find('table', {
        'class': 'table table--primary align--right',
        'aria-label': 'Competitors data table'
    })
    competitors = []
    rows = competitors_table.find_all('tr')
    for row in rows:
        col = row.find('td')
        cols = row.find_all('td')
        if cols:
            nome       = cols[0].find('a').get_text(strip=True)
            variacao   = cols[1].get_text(strip=True)
            market_cap = cols[2].get_text(strip=True)
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
