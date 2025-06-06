import requests
from bs4 import BeautifulSoup
from typing import Optional

def extract_table_with_headers(
    url: str,
    attrs: Optional[dict[str, str]] = None,
    **kwargs
) -> dict:

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

    # print('Classes of each table:')
    # for table in soup.find_all('table'):
    #     print(table.get('id'),table.get('class'))

    if attrs:
        table = soup.find('table', attrs=attrs)
    else:
        table = soup.find('table', **kwargs)
    if not table:
        return {}

    rows = table.find_all('tr')
    if not rows or len(rows) == 0:
        return {}

    data = {}
    for row in rows:
        cells = row.find_all('td')
        values = [cell.get_text(strip=True) for cell in cells]
        data[values[0].replace(' ','_').lower()] = values[1]

    return data

def parse_float(value: str) -> Optional[float]:
    if not isinstance(value, str):
        return None

    cleaned = value.strip().replace(',', '.').replace('%', '')
    
    try:
        number = float(cleaned)
        return number
    except ValueError:
        return None


def extract_table(
    url: str,
    attrs: Optional[dict[str, str]] = None,
    **kwargs
) -> [dict]:

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

    if attrs:
        table = soup.find('table', attrs=attrs)
    else:
        table = soup.find('table', **kwargs)
    if not table:
        return []

    rows = table.find_all('tr')    
    if not rows or len(rows) == 0:
        return []

    data = []
    for row in rows:
        cells = row.find_all('td')
        # print('->',cells)
        values = [cell.get_text(strip=True) for cell in cells]
        # print('--->',values)
        if values: data.append(values)
        # data[values[0].replace(' ','_').lower()] = values[1]

    return data

def get_value_by_key(data: list[list[str]], key: str) -> Optional[str]:
    for item in data:
        if len(item) == 2 and item[0] == key:
            return item[1].replace('.', ',')
    return None
