from decimal import Decimal, setcontext, Context, ROUND_UP

from flask import make_response, Response
from flask_marshmallow import Schema
from flask_restful import Resource, reqparse
from flask_sqlalchemy import BaseQuery
from marshmallow import ValidationError

from app.db import db
from app.errors import InvalidInputArgumentFormat
from app.models import Ticker
from app.schemas import TickerSchema
from app.validation import valid_currency_iso_format, valid_decimal_exponent, valid_decimal_precision


def json_response(data) -> Response:
    response: Response = make_response(data)
    response.headers['content-type'] = 'application/json'
    return response


def currency_type(value):
    assert valid_currency_iso_format(value)
    return value


def decimal_type(value):
    decimal_value = Decimal(value)
    assert valid_decimal_exponent(decimal_value) and valid_decimal_precision(decimal_value)
    return decimal_value


class GrabAndSave(Resource):
    schema: Schema = TickerSchema()
    parser = reqparse.RequestParser()
    parser.add_argument(
        'currency', type=currency_type, required=True,
        help='Missing currency argument in correct format! Example: BTC',
    )
    parser.add_argument(
        'amount', type=decimal_type, required=True,
        help='Missing amount argument in correct format! Example: 16105.10',
    )

    def post(self):
        args = self.parser.parse_args()
        currency_code = args['currency']
        amount_requested = args['amount']

        currency_rate = Decimal('0.000062')

        setcontext(Context(prec=8, rounding=ROUND_UP))
        final_amount = currency_rate * amount_requested

        payload = {
            'currency_code': currency_code,
            'currency_rate': currency_rate,
            'amount_requested': amount_requested,
            'final_amount': final_amount,
        }
        try:
            validated_data = self.schema.load(data=payload)
        except ValidationError as e:
            from main import app
            app.logger.error(
                f'Exception: {e} '
                f'Payload: {payload}'
            )
            raise InvalidInputArgumentFormat

        ticker = Ticker(**validated_data)
        db.session.add(ticker)
        db.session.commit()

        return json_response(self.schema.dumps(obj=ticker))


class Last(Resource):
    schema: Schema = TickerSchema(many=True)
    parser = reqparse.RequestParser()
    parser.add_argument('currency', type=currency_type)
    parser.add_argument('number', type=int, default=1)

    def get(self):
        args = self.parser.parse_args()

        currency = args.get('currency')
        number = args.get('number')

        query_obj: BaseQuery = Ticker.query
        query = query_obj.order_by(Ticker.created_at.desc())

        if currency:
            query = query.filter_by(currency_code=currency)

        tickers = query.limit(number).all()
        return json_response(self.schema.dumps(obj=tickers))
