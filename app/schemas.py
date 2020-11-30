from decimal import Decimal

import simplejson

from marshmallow import ValidationError, fields
from marshmallow_sqlalchemy import auto_field

from app.const import CURRENCY_ISO_LENGTH, DECIMAL_EXPONENT, DECIMAL_PRECISION
from app.db import ma
from app.models import Ticker
from app.validation import (
    valid_currency_iso_format,
    valid_decimal_exponent,
    valid_decimal_precision,
)


def validate_currency(value: str):
    if not isinstance(value, str):
        raise ValidationError(f"Value has incorrect type: {type(value)}")
    if not valid_currency_iso_format(value):
        raise ValidationError(
            f"Value must be in ISO format with {CURRENCY_ISO_LENGTH} length"
        )


def validate_decimal(value: Decimal):
    if not isinstance(value, Decimal):
        raise ValidationError(f"Value has incorrect type: {type(value)}")
    if not valid_decimal_exponent(value):
        raise ValidationError(
            f"Exponent must be not greater than {DECIMAL_EXPONENT} places"
        )
    if not valid_decimal_precision(value):
        raise ValidationError(
            f"Precision must be not greater than {DECIMAL_PRECISION} places"
        )


class TickerSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Ticker
        render_module = simplejson

    currency_code = fields.String(validate=validate_currency)
    currency_rate = fields.Decimal(validate=validate_decimal)
    amount_requested = fields.Decimal(validate=validate_decimal)
    final_amount = fields.Decimal(validate=validate_decimal)
    created_at = auto_field(dump_only=True)
