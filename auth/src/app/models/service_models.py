import re
from typing import Optional, List

from uuid import UUID

from pydantic import validator
from pydantic.main import BaseModel

from app.utils.exceptions import BadEmailError, BadPasswordError, BadLengthError

PASSWORD_REGEXP = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$')

# https://html.spec.whatwg.org/multipage/input.html#valid-e-mail-address
EMAIL_REGEXP = re.compile(r"^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$")


class User(BaseModel):
    id: Optional[UUID]
    login: str
    password: str
    is_superuser: Optional[bool]
    email: str
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]

    history_entries: Optional[List[UUID]]
    roles: Optional[List[str]]

    @validator('password')
    def validate_password(cls, password):
        if not re.fullmatch(PASSWORD_REGEXP, password):
            raise BadPasswordError
        return password

    @validator('email')
    def validate_email(cls, email):
        if not re.fullmatch(EMAIL_REGEXP, email):
            raise BadEmailError
        return email

    @validator('first_name', 'middle_name', 'last_name', 'login')
    def validate_length(cls, field):
        if len(field) > 100:
            raise BadLengthError(message=f'Wrong length of field. Max 100 characters')
        return field
