from decimal import ROUND_UP, Decimal
from typing import Union

from app.const import DECIMAL_EXPONENT


def convert_to_raw_decimal(value: Union[int, float, str, Decimal]) -> Decimal:
    if isinstance(value, float) or isinstance(value, int):
        value = str(value)

    if isinstance(value, str):
        value = Decimal(value)

    return value


def convert_to_rounded_decimal(value: Union[int, float, str, Decimal]) -> Decimal:
    value = convert_to_raw_decimal(value)

    exponent = Decimal(
        str(
            pow(
                base=10,
                exp=-1 * DECIMAL_EXPONENT,
            )
        )
    )

    return value.quantize(
        exp=exponent,
        rounding=ROUND_UP,
    )
