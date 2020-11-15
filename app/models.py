from datetime import datetime

from app.const import DECIMAL_PRECISION, DECIMAL_EXPONENT, CURRENCY_ISO_LENGTH
from main import db


class Ticker(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    currency_code = db.Column(db.String(length=CURRENCY_ISO_LENGTH), nullable=False, index=True)
    currency_rate = db.Column(db.Numeric(precision=DECIMAL_PRECISION, scale=DECIMAL_EXPONENT), nullable=False)
    amount_requested = db.Column(db.Numeric(precision=DECIMAL_PRECISION, scale=DECIMAL_EXPONENT), nullable=False)
    final_amount = db.Column(db.Numeric(precision=DECIMAL_PRECISION, scale=DECIMAL_EXPONENT), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'({self.id}) <Ticker for {self.currency_code}: {self.final_amount}>'
