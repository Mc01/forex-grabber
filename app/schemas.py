from marshmallow_sqlalchemy import auto_field
import simplejson

from app.models import Ticker
from main import ma


class TickerSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Ticker
        json_module = simplejson

    currency_code = auto_field()
    currency_rate = auto_field()
    amount_requested = auto_field()
    final_amount = auto_field()
    created_at = auto_field(dump_only=True)
