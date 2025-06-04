# API Stock

A Flask API that retrieves financial stock data from Polygon.io and extracts information from the MarketWatch website.  
It allows recording stock purchase requests, which are stored in a PostgreSQL database.

- [MarketWatch - Exemplo AAPL](https://www.marketwatch.com)
- https://api.polygon.io/v1/open-close/AAPL/2025-05-30

---

## Installation
```bash
git clone https://github.com/MarceloArnaldi/cial.git
cd cial
docker-compose up -d
```
## Demo on AWS EC2
Demo running with Gunicorn (WSGI)
```

```

## Resources 

### `GET /purchases`
Returns all recorded stock purchase requests.

---

### `GET /stock/<stock_symbol>/<date>`
Returns detailed data about the stock on the specified date.

#### Resposta:
```json
{
  "Status": "OK",
  "purchased_amount": 0,
  "purchased_status": "not_purchased",
  "request_data": "2025-05-30",
  "company_code": "AAPL",
  "company_name": "Apple Inc.",
  "Stock_values": {
    "open": 199.37,
    "high": 201.96,
    "low": 196.78,
    "close": 200.85
  },
  "performance_data": {
    "five_days": 2.86,
    "one_month": -2.19,
    "three_months": -16.95,
    "year_to_date": -19.79,
    "one_year": 4.47
  },
  "Competitors": [
    {
      "name": "Microsoft Corp.",
      "market_cap": {
        "Currency": "0.37%",
        "Value": "$3.41T"
      }
    }
  ]
}
```

### `POST /stock/<stock_symbol>`
Creates a new stock purchase request.

#### Request (Headers):
```json
{
  "amount": 17
}
```

#### Response:
```json
{
  "id": "cbea481d-f4a1-431e-b056-87cfa85479ee",
  "stock_symbol": "AAPL",
  "purchase_date": "2025-06-01",
  "amount": 17
}
```

## Database
- PostgreSQL 17.5
- UUID extension 
```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE purchases (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    stock_symbol VARCHAR(10) NOT NULL,
    purchase_date DATE NOT NULL,
    amount INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Logs
- Error Log: logs/errors.log
- POST Request Log: logs/post_requests.log
  
Files are automatically rotated after 1 MB.

## Test
pytest







