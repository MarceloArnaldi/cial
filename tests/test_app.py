import pytest
from app import app, db
from models import Purchase

@pytest.fixture
def client():
    app.config['TESTING'] = True
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['CACHE_TYPE'] = 'null'  
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()

def test_get_stock_valid(client, mocker):
    response = client.get('/stock/AAPL/2025-05-30')
    assert response.status_code == 200
    data = response.get_json()
    assert data["company_code"] == "AAPL"

def test_post_stock_valid(client, mocker):
    mock_purchase = Purchase(stock_symbol='AAPL', amount=10)
    mock_purchase.id = 1
    mocker.patch('services.purchase_service.create_purchase', return_value=mock_purchase)

    response = client.post('/stock/AAPL', json={"amount": 10})
    assert response.status_code == 201
    data = response.get_json()
    assert data["stock_symbol"] == "AAPL"
    assert data["amount"] == 10

def test_post_stock_missing_amount(client):
    response = client.post('/stock/AAPL', json={})
    assert response.status_code == 400
    assert response.get_json()["error"] == "Missing amount in request body"

def test_post_stock_invalid_amount(client):
    response = client.post('/stock/AAPL', json={"amount": -5})
    assert response.status_code == 400
    assert response.get_json()["error"] == "amount must be a positive integer"

def test_get_purchases_valid(client):
    response = client.get('/purchases')
    assert response.status_code == 200