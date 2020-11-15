import pytest

from app.const import CURRENCY_ISO_LENGTH
from app.validation import valid_currency_iso_format
from tests.factories import currency_list, stretch_string


@pytest.mark.parametrize(
    "currency",
    currency_list(),
)
def test_currency_iso_format(currency: str):
    assert valid_currency_iso_format(currency)


@pytest.mark.parametrize(
    "currency",
    ["", " "]
    + [c[0 : CURRENCY_ISO_LENGTH - 1] for c in currency_list()]
    + [
        stretch_string(c, desired_length=CURRENCY_ISO_LENGTH + 1)
        for c in currency_list()
    ],
)
def test_invalid_currency_iso_format(currency: str):
    assert not valid_currency_iso_format(currency)
