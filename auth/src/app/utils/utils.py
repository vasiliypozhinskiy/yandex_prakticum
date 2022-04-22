import bcrypt


def remove_password(dict_):
    dict_.update({'password': '****'})
    return dict_


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)


def check_password(password: str) -> bool:
    hashed = hash_password(password)

    if bcrypt.checkpw(password.encode(), hashed):
        return True
    else:
        return False

