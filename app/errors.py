from werkzeug.exceptions import HTTPException


class InvalidInputArgumentFormat(HTTPException):
    pass


errors = {
    InvalidInputArgumentFormat.__name__: {
         "message": "Input fields have invalid format",
         "status": 400,
     },
}
