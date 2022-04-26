class FieldValidationError(Exception):
    default_message = "Wrong field value"

    def __init__(self, message=default_message):
        self.message = message


class AlreadyExistsError(Exception):
    pass


class RoleAlreadyExists(Exception):
    message = 'Role to be created already exists'


class NotFoundError(Exception):
    default_message = "Resource not found"

    def __init__(self, message=default_message):
        self.message = message


class BadPasswordError(Exception):
    default_message = """
    Password must contain minimum eight characters, at least one uppercase letter, 
    one lowercase letter, one number and one special character
    """

    def __init__(self, message=default_message):
        self.message = message


class BadEmailError(Exception):
    default_message = "Wrong email"

    def __init__(self, message=default_message):
        self.message = message


class BadLengthError(Exception):
    default_message = "Wrong length of field"

    def __init__(self, message=default_message):
        self.message = message


class BadIdFormat(Exception):
    default_message = "Wrong id format"

    def __init__(self, message=default_message):
        self.message = message
