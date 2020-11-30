from decimal import Decimal

from app.models import Ticker
from app.schemas import TickerSchema
from tests.factories import currency_list


def test_ticker_schema_json_to_model():
    currency_code = currency_list()[0]
    currency_rate = Decimal('10.00')
    amount_requested = Decimal('10.00')
    final_amount = Decimal('100.00')

    data = {
        "currency_code": currency_code,
        "currency_rate": currency_rate,
        "amount_requested": amount_requested,
        "final_amount": final_amount,
    }
    validated_data = TickerSchema().load(data)
    ticker = Ticker(**validated_data)

    assert ticker.currency_code == currency_code
    assert ticker.currency_rate == currency_rate
    assert ticker.amount_requested == amount_requested
    assert ticker.final_amount == final_amount


def test_ticker_schema_model_to_json():
    currency_code = currency_list()[0]
    currency_rate = Decimal('10.00')
    amount_requested = Decimal('10.00')
    final_amount = Decimal('100.00')

    ticker = Ticker(
        currency_code=currency_code,
        currency_rate=currency_rate,
        amount_requested=amount_requested,
        final_amount=final_amount,
    )
    data = TickerSchema().dump(obj=ticker)

    data.pop('created_at')
    assert data == {
        "currency_code": currency_code,
        "currency_rate": currency_rate,
        "amount_requested": amount_requested,
        "final_amount": final_amount,
    }
