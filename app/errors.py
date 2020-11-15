from werkzeug.exceptions import HTTPException


class CommunicationIssueWithOER(HTTPException):
    pass


class MalformedDataReturned(HTTPException):
    pass


class NoRateAvailableForCurrency(HTTPException):
    pass


class DataValidationDuringSaveException(HTTPException):
    pass


errors = {
    CommunicationIssueWithOER.__name__: {
        "message": "Communication cannot be established with OER",
        "status": 500,
    },
    MalformedDataReturned.__name__: {
        "message": "Malformed data returned by OER",
        "status": 500,
    },
    NoRateAvailableForCurrency.__name__: {
        "message": "There is no currency rate on OER for given currency code",
        "status": 400,
    },
    DataValidationDuringSaveException.__name__: {
        "message": "Data was not able to pass validation during serialization",
        "status": 500,
    },
}
