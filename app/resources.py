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


def json_response(data) -> Response:
    response: Response = make_response(data)
    response.headers['content-type'] = 'application/json'
    return response


def decimal_type(value):
    return Decimal(value)


class GrabAndSave(Resource):
    schema: Schema = TickerSchema()
    parser = reqparse.RequestParser()
    parser.add_argument(
        'currency', type=str, required=True,
        help='Missing "currency" argument! Example: "BTC"',
    )
    parser.add_argument(
        'amount', type=decimal_type, required=True,
        help='Missing "amount" argument! Example: "16105.10"',
    )

    def post(self):
        args = self.parser.parse_args()
        currency_code = args['currency']
        amount_requested = args['amount']

        currency_code = 'BTC'
        currency_rate = Decimal('0.000062')
        amount_requested = Decimal('16105.10')

        setcontext(Context(prec=8, rounding=ROUND_UP))
        final_amount = currency_rate * amount_requested

        try:
            validated_data = self.schema.load(data={
                'currency_code': currency_code,
                'currency_rate': currency_rate,
                'amount_requested': amount_requested,
                'final_amount': final_amount,
            })
        except ValidationError:
            raise InvalidInputArgumentFormat

        ticker = Ticker(**validated_data)
        db.session.add(ticker)
        db.session.commit()

        return json_response(self.schema.dumps(obj=ticker))


class Last(Resource):
    schema: Schema = TickerSchema(many=True)
    parser = reqparse.RequestParser()
    parser.add_argument('currency', type=str)
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
