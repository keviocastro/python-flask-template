from functools import wraps

from flask_jwt_extended import get_jwt_identity

from app.services.errors.exceptions import UnauthorizedError


def intercept_admin_user(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        jwt_group_id = get_jwt_identity()['group_id']

        if jwt_group_id == 5:
            raise UnauthorizedError('User not found!')

        return f(*args, **kwargs)

    return wrap
