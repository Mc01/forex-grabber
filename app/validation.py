from decimal import Decimal

from app.const import DECIMAL_EXPONENT, DECIMAL_PRECISION, CURRENCY_ISO_LENGTH


def valid_currency_iso_format(value: str) -> bool:
    return len(value) == CURRENCY_ISO_LENGTH


def valid_decimal_exponent(value: Decimal) -> bool:
    return 0 >= value.as_tuple().exponent >= -1 * DECIMAL_EXPONENT


def valid_decimal_precision(value: Decimal) -> bool:
    return len(value.as_tuple().digits) <= DECIMAL_PRECISION
