# API Stock

API em Flask que recupera dados financeiros de ações da [Polygon.io](https://polygon.io) e realiza extração de informações do site [MarketWatch](https://www.marketwatch.com).  
Permite também registrar solicitações de compra de ações, que são armazenadas em um banco PostgreSQL.

- [MarketWatch - Exemplo AAPL](https://www.marketwatch.com)
- https://api.polygon.io/v1/open-close/AAPL/2025-05-30

---

## Recursos 

### `GET /purchases`
Retorna todas as solicitações de compra de ações registradas.

---

### `GET /stock/<stock_symbol>/<date>`
Retorna dados detalhados sobre a ação no dia informado.

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
Cria uma nova solicitação de compra de ação.

#### Requisição (Headers):
```json
{
  "amount": <integer>
}
```

#### Resposta:
```json
{
  "id": "cbea481d-f4a1-431e-b056-87cfa85479ee",
  "stock_symbol": "AAPL",
  "purchase_date": "2025-06-01",
  "amount": 17
}
```

## Banco de Dados
- PostgreSQL 17.5
- Extensão UUID utilizada
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
- Log de Erros: logs/errors.log
- Log de Requisições POST: logs/post_requests.log
  
Os arquivos são rotacionados automaticamente após 1 MB.

## Instalação
```bash
git clone https://github.com/MarceloArnaldi/cial.git
cd cial
docker-compose up -d
```






