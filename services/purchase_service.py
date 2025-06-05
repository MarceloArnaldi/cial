from models.purchase import db, Purchase
from datetime import datetime

def create_purchase(stock: str, amount_: str):
    try:
        purchase = Purchase(
            stock_symbol=stock,
            amount=int(amount_)
        )
        print('purchase')
        print(purchase)
        db.session.add(purchase)
        db.session.commit()
        return purchase
    except Exception as e:
        db.session.rollback()
        raise e