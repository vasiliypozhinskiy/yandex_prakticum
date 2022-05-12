from http import HTTPStatus

from fastapi import HTTPException

MESSAGE_DATA_NOT_FOUND = 'data not found'
BY_COMEDY_SUBSCRIPTION = 'by comedy subscription'
INVALID_TOKEN = 'invalid token'


class NotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTPStatus.NOT_FOUND, detail=MESSAGE_DATA_NOT_FOUND
        )


class ComedySubscription(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTPStatus.FORBIDDEN, detail=BY_COMEDY_SUBSCRIPTION
        )


class InvalidToken(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTPStatus.UNAUTHORIZED, detail=INVALID_TOKEN
        )