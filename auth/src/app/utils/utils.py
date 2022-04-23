import bcrypt


def hide_password(dict_):
    if dict_.get('password'):
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


def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = getattr(row, column.name)

    return d

