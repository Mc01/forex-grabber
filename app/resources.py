import os

from decimal import Decimal

from flask import Response, current_app, make_response

from flask_marshmallow import Schema
from flask_restful import Resource, reqparse
from flask_sqlalchemy import BaseQuery
from marshmallow import ValidationError
from requests import HTTPError

from app.db import db
from app.errors import (
    CommunicationIssueWithOER,
    DataValidationDuringSaveException,
    MalformedDataReturned,
    NoRateAvailableForCurrency,
)
from app.models import Ticker
from app.schemas import TickerSchema
from app.utils import convert_to_raw_decimal, convert_to_rounded_decimal
from app.validation import (
    valid_currency_iso_format,
    valid_decimal_exponent,
    valid_decimal_precision,
)
from app.vendors import oer


def json_response(data) -> Response:
    response: Response = make_response(data)
    response.headers["content-type"] = "application/json"
    return response


def currency_type(value: str) -> str:
    assert valid_currency_iso_format(value)
    return value


def decimal_type(value: str) -> Decimal:
    decimal_value = convert_to_raw_decimal(value)
    assert valid_decimal_exponent(decimal_value) and valid_decimal_precision(
        decimal_value
    )
    return decimal_value


class GrabAndSave(Resource):
    schema: Schema = TickerSchema()
    parser = reqparse.RequestParser()
    parser.add_argument(
        "currency",
        type=currency_type,
        required=True,
        help="Missing currency argument in correct format! Example: BTC",
    )
    parser.add_argument(
        "amount",
        type=decimal_type,
        required=True,
        help="Missing amount argument in correct format! Example: 16105.10",
    )

    @staticmethod
    def _get_data_from_oer(currency_code, amount_requested: Decimal):
        try:
            raw_data = oer.get_latest_rates(
                app_id=current_app.config["OER_APP_ID"],
            )
        except HTTPError as e:
            current_app.logger.error(f"Exception: {e}")
            raise CommunicationIssueWithOER

        try:
            currency_rate = raw_data["rates"].get(currency_code)
        except KeyError:
            raise MalformedDataReturned

        if not currency_rate:
            raise NoRateAvailableForCurrency
        else:
            currency_rate = convert_to_rounded_decimal(currency_rate)

        """
        Note: I believe there's an error in task description:
        
        1)
        > Multiply the price for the amount passed in the POST request body and 
        > obtain a final amount
        
        2)
        > Store in MySQL the currency, the amount requested, the price given by 
        > open exchange rate and the final amount in USD
        
        3)
        > Use a precision of 8 decimal digits, and always round up
        
        To above for working correctly I should change base in API request
        to desired currency and retrieve (request_currency:USD) rate...
        
        However free API raises following:
        > Changing the API `base` currency is available for Developer, Enterprise 
        > and Unlimited plan clients. Please upgrade, or contact 
        > support@openexchangerates.org with any questions
        
        So to receive correct final_amount I decided to *divide* instead of multiply!
        
        To be compliant with description as much as possible I decided to always 
        follow rounding up :)
        
        Example:
        
        For following request: {"currency": "PLN", "amount": 100}
        I understand it as: 
        - how much in USD is worth 100 PLN?
        
        It gives following response: {"currency_rate": 3.78809000, "final_amount": 26.39852802}
        Which translates to:
        - 1 USD is worth 3.78809000 PLN
        - so 100 PLN is worth 26.39852802 USD
        """
        final_amount = convert_to_rounded_decimal(amount_requested / currency_rate)
        return {
            "currency_code": currency_code,
            "currency_rate": currency_rate,
            "amount_requested": amount_requested,
            "final_amount": final_amount,
        }

    def post(self):
        args = self.parser.parse_args()
        data = self._get_data_from_oer(
            currency_code=args["currency"],
            amount_requested=args["amount"],
        )

        try:
            validated_data = self.schema.load(data=data)
        except ValidationError as e:
            current_app.logger.error(f"Exception: {e}")
            raise DataValidationDuringSaveException

        ticker = Ticker(**validated_data)
        db.session.add(ticker)
        db.session.commit()

        return json_response(self.schema.dumps(obj=ticker))


class Last(Resource):
    schema: Schema = TickerSchema(many=True)
    parser = reqparse.RequestParser()
    parser.add_argument("currency", type=currency_type)
    parser.add_argument("number", type=int, default=1)

    def get(self):
        args = self.parser.parse_args()

        currency = args.get("currency")
        number = args.get("number")

        query_obj: BaseQuery = Ticker.query
        query = query_obj.order_by(Ticker.created_at.desc())

        if currency:
            query = query.filter_by(currency_code=currency)

        tickers = query.limit(number).all()
        return json_response(self.schema.dumps(obj=tickers))
