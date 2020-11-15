from decimal import Decimal

from app.const import (
    CURRENCY_ISO_LENGTH,
    DECIMAL_EXPONENT,
    DECIMAL_PRECISION,
    MAX_NUMBER_LAST_TICKERS,
)


def valid_currency_iso_format(value: str) -> bool:
    return len(value) == CURRENCY_ISO_LENGTH


def valid_decimal_exponent(value: Decimal) -> bool:
    return 0 >= value.as_tuple().exponent >= -1 * DECIMAL_EXPONENT


def valid_decimal_precision(value: Decimal) -> bool:
    return len(value.as_tuple().digits) <= DECIMAL_PRECISION


def valid_number_limit(value: int) -> bool:
    return 0 < value <= MAX_NUMBER_LAST_TICKERS
