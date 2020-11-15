from datetime import datetime

from main import db


class Ticker(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    currency_code = db.Column(db.String(length=3), nullable=False)
    currency_rate = db.Column(db.Numeric(precision=8), nullable=False)
    amount_requested = db.Column(db.Numeric(precision=8), nullable=False)
    final_amount = db.Column(db.Numeric(precision=8), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'({self.id}) <Ticker for {self.currency_code}: {self.final_amount}>'
