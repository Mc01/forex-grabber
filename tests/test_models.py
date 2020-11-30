from decimal import Decimal

from app.models import Ticker
from tests.factories import currency_list


def test_ticker_model(db_session):
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
    db_session.add(ticker)
    db_session.commit()

    ticker_in_db = db_session.query(Ticker).get(1)
    assert ticker_in_db.id == 1
    assert ticker_in_db.currency_code == currency_code
    assert ticker_in_db.currency_rate == currency_rate
    assert ticker_in_db.amount_requested == amount_requested
    assert ticker_in_db.final_amount == final_amount
