API Stock
Aplicação API que recupera dados de ações da API financeira polygon.io e realiza extração de dados do site financeiro Marketwatch, de acordo com o sigla da ação fornecida.
A aplicação recebe solicitação de compra e armazena.

Recursos

GET  /purchases <- retorna todas solicitações de compra de ações
GET  /stock/<stock_symbol>/<date> <- retorna dados da ação
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
POST /stock/<stock_symbol> <- envia um pedido de compra de ação
    payload de requisição
    header
    {
        "amount": <amount>
    }
    payload de resposta
    {
        "id": "cbea481d-f4a1-431e-b056-87cfa85479ee",
        "stock_symbol": "AAPL",
        "purchase_date": "2025-06-01",
        "amount": 17
    }

PostgreSQL 17.5

Bibliotecas

Flask
requests
beautifulsoup4
lxml
python-dotenv

Fontes

https://www.marketwatch.com/investing/stock/aapl
api.polygon.io/v1/open-close/AAPL/2025-05-30

Esquema da banco de dados 
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE purchases (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    stock_symbol VARCHAR(10) NOT NULL,
    purchase_date DATE NOT NULL,
    amount INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

Demo Deploy em Docker/EC2: http://52.70.224.64:8000
Esse demo não tem gerenciamento de API como (API Gateway/API Management/Apigee), nenhum controle de consumo e proteção de ataques (WAF).

Log
log de erros        : logs\errors.log
log de solicitação  : logs\post_requests.log

Instalação

git clone https://github.com/MarceloArnaldi/cial.git
docker-compose up -d
