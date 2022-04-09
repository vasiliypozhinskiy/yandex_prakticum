from http import HTTPStatus

from fastapi import HTTPException

MESSAGE_DATA_NOT_FOUND = 'data not found'


class NotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=HTTPStatus.NOT_FOUND, detail=MESSAGE_DATA_NOT_FOUND)
