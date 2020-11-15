from datetime import datetime
from decimal import Decimal
from math import ceil
from typing import List, Type

import factory
import pytest

from factory.fuzzy import FuzzyDateTime, FuzzyDecimal
from pytz import UTC

from app.const import CURRENCY_ISO_LENGTH, DECIMAL_EXPONENT
from app.models import Ticker


def stretch_string(value: str, desired_length: int):
    """
    >>> stretch_string("test", desired_length=5)
    'testt'
    >>> stretch_string("test", desired_length=2)
    'te'
    >>> stretch_string("", desired_length=2)
    ''
    >>> stretch_string("test", desired_length=0)
    ''
    """
    if not value:
        return ""
    return (value * ceil(desired_length / len(value)))[0:desired_length]


def currency_list() -> List[str]:
    _currency_list = ["USD", "EUR", "PLN", "TRY", "AED", "CZK", "GBP"]
    if CURRENCY_ISO_LENGTH != 3:
        _currency_list = [
            stretch_string(c, desired_length=CURRENCY_ISO_LENGTH)
            for c in _currency_list
        ]
    return _currency_list


@pytest.fixture
def ticker_factory(db_session) -> Type[factory.Factory]:
    def get_final_amount(ticker: Ticker):
        currency_rate: Decimal = Decimal(ticker.currency_rate)
        amount_requested: Decimal = Decimal(ticker.amount_requested)
        final_amount: Decimal = currency_rate * amount_requested
        return final_amount.quantize(Decimal(str(pow(10, -1 * DECIMAL_EXPONENT))))

    class TickerFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = Ticker
            sqlalchemy_session = db_session
            sqlalchemy_session_persistence = "commit"

        currency_code = factory.Iterator(currency_list())
        currency_rate = FuzzyDecimal(
            low=pow(10, -DECIMAL_EXPONENT),
            high=pow(10, DECIMAL_EXPONENT),
            precision=DECIMAL_EXPONENT,
        )
        amount_requested = FuzzyDecimal(
            low=pow(10, -DECIMAL_EXPONENT),
            high=pow(10, DECIMAL_EXPONENT),
            precision=DECIMAL_EXPONENT,
        )
        final_amount = factory.LazyAttribute(get_final_amount)
        created_at = FuzzyDateTime(
            start_dt=datetime(2020, 10, 1, tzinfo=UTC), end_dt=datetime.utcnow()
        )

    return TickerFactory
