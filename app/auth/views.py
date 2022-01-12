from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.auth import bp
from app.auth.services.token import generate_user_jwt
from app.auth.services.user import select_user_by_jwt
from app.auth.services.validations import validate_token
from app.services.errors.exceptions import UnauthorizedError


@bp.route('/token', methods=["POST"])
def token():
    if request.method == 'POST':
        try:
            basic = request.headers.get("Authorization", None)
            dict_body = request.get_json()

            user, password = validate_token(basic, dict_body)

            if user is not None and user.check_password(password):
                token = generate_user_jwt(user)

                return token, 200
            else:
                raise UnauthorizedError("Usuário ou Senha incorreta!")
        except Exception as e:
            return {"Error": str(e)}, 500


@bp.route('/refresh', methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    if request.method == 'POST':
        try:
            user_jwt = get_jwt_identity()

            user = select_user_by_jwt(user_jwt)

            if user:
                token = generate_user_jwt(user)

                return token, 200
            else:
                raise UnauthorizedError("Usuário não autorizado!")
        except UnauthorizedError as e:
            return {"Error": str(e)}, 401
        except Exception as e:
            return {"Error": str(e)}, 500
