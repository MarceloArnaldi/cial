import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("POLYGON_API_KEY")

def get_polygon_data(symbol: str, date: str):
    url = f'https://api.polygon.io/v1/open-close/{symbol}/{date}?adjusted=true&apiKey={API_KEY}'
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200 or data.get("status") != "OK":
        raise Exception("Erro ao buscar dados da Polygon.io")

    return {
        'status' : data.get('status'),
        'symbol' : data.get('symbol'),
        'date'   : data.get('from'),
        'open'   : data.get('open'),
        'high'   : data.get('high'),
        'low'    : data.get('low'),
        'close'  : data.get('close')
    }
