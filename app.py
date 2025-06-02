#
# API Stock
# Versao 1.000.00 - 2025-05-31 
# Autor Marcelo Arnaldi
#
# GET  /purchases
# GET  /stock/<stock_symbol>/<date>
# POST /stock/<stock_symbol>
#
from flask                        import Flask, jsonify, request 
from flask_caching                import Cache
from models                       import db, Purchase
from services.external_services   import get_stock_data
from services.purchase_service    import create_purchase
from datetime                     import datetime
from config                       import Config
from logger_config                import setup_post_logger, setup_error_logger
    
app = Flask(__name__)
app.config.from_object(Config)
app.json.sort_keys = False

db.init_app(app)
cache = Cache(app)

post_logger  = setup_post_logger()
error_logger = setup_error_logger()
@app.before_request
def log_post_requests():
    if request.method == 'POST':
        post_logger.info(
            f"Endpoint: {request.path} | IP: {request.remote_addr} | Payload: {request.get_json(silent=True)}"
        )
@app.errorhandler(Exception)
def handle_exception(e):
    error_logger.error(
        f"Erro em {request.path} | IP: {request.remote_addr} | Exception: {str(e)}"
    )
    return jsonify({"error": "Erro interno do servidor"}), 500        

@app.route('/stock/<symbol>', methods=['GET','POST'])
@app.route('/stock/<symbol>/<date>', methods=['GET'])
def stock_info(symbol, date=None):
    if request.method == "POST":
        data = request.get_json()
        if not data or 'amount' not in data:
            return jsonify({'error': 'Missing amount in request body'}), 400
        amount = data['amount']            
        if not isinstance(amount, int) or amount <= 0:
            return jsonify({'error': 'amount must be a positive integer'}), 400
        data = request.get_json()
        try:
            new_purchase = create_purchase(symbol,amount)
            return jsonify(new_purchase.to_dict()), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400        
    else:
        if not date:
            date = datetime.today().strftime('%Y-%m-%d')
        try:
            cache_key = f"stock::{symbol}::{date}"
            cached = cache.get(cache_key)
            if cached:
                return jsonify(cached)
            response = get_stock_data(symbol, date)
            cache.set(cache_key, response)
            return jsonify(response)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/purchases', methods=['GET'])
def handle_purchase():
    users = Purchase.query.all()
    return jsonify([user.to_dict() for user in users])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(host="0.0.0.0", port=5000)