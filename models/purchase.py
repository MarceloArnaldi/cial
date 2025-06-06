import uuid
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Purchase(db.Model):
    __tablename__ = 'purchases'
    
    id            = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    stock_symbol  = db.Column(db.String(10), nullable=False)
    purchase_date = db.Column(db.Date, default=datetime.utcnow)
    amount        = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'id': str(self.id),
            'stock_symbol': self.stock_symbol,
            'purchase_date': self.purchase_date.isoformat(),
            'amount': self.amount
        }