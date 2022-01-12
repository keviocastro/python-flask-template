import logging
from http import HTTPStatus

import sqlalchemy
import werkzeug
from flask import jsonify
from werkzeug.exceptions import MethodNotAllowed, NotFound

from app import jwt
from app.services.errors import bp

logger = logging.getLogger(__name__)


class UnauthorizedError(Exception):
    def __init__(self, error, status_code=HTTPStatus.UNAUTHORIZED):
        Exception.__init__(self)
        self.error = error
        self.status_code = status_code


class ForbiddenError(Exception):
    def __init__(self, error='Resource not found',
                 status_code=HTTPStatus.FORBIDDEN):
        Exception.__init__(self)
        self.error = error
        self.status_code = status_code


class NotFoundError(Exception):
    def __init__(self, error='Resource not found',
                 status_code=HTTPStatus.NOT_FOUND):
        Exception.__init__(self)
        self.error = error
        self.status_code = status_code


class GenerateError(Exception):
    def __init__(self, error, status_code):
        Exception.__init__(self)
        self.error = error
        self.status_code = status_code


@bp.app_errorhandler(NotFound)
def not_found_exception(e):
    logger.exception(e)
    response = jsonify({
        "status": HTTPStatus.NOT_FOUND,
        "msg": "Resource not found"
    })
    response.status_code = HTTPStatus.NOT_FOUND
    return response


@bp.app_errorhandler(UnauthorizedError)
def unauthorized_exception(e):
    logger.exception(e)
    response = jsonify({
        "status": e.status_code,
        "msg": e.error
    })
    response.status_code = e.status_code
    return response


@bp.app_errorhandler(ForbiddenError)
def forbidden_exception(e):
    logger.exception(e)
    response = jsonify({
        "status": e.status_code,
        "msg": e.error
    })
    response.status_code = e.status_code
    return response


@bp.app_errorhandler(GenerateError)
def generate_exception(e):
    logger.exception(e)
    response = jsonify({
        "status": e.status_code,
        "msg": e.error
    })
    response.status_code = e.status_code
    return response


@bp.app_errorhandler(NotFoundError)
def forbidden_exception(e):
    logger.exception(e)
    response = jsonify({
        "status": e.status_code,
        "msg": e.error
    })
    response.status_code = e.status_code
    return response


@bp.app_errorhandler(MethodNotAllowed)
def method_exception(e):
    logger.exception(e)
    response = jsonify(
        {
            "status": HTTPStatus.METHOD_NOT_ALLOWED,
            "msg": "Method not Allowed"
        })
    response.status_code = HTTPStatus.METHOD_NOT_ALLOWED
    return response


@bp.app_errorhandler(sqlalchemy.exc.InternalError)
def sql_error(e):
    logger.exception(e)
    response = jsonify(
        {
            "status": HTTPStatus.INTERNAL_SERVER_ERROR,
            "msg": "SQL Error: {}".format(e.orig.args[1])
        })
    response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    return response


@bp.app_errorhandler(werkzeug.exceptions.BadRequest)
def bad_request(e):
    logger.exception(e)
    response = jsonify(
        {
            "status": HTTPStatus.BAD_REQUEST,
            "msg": "Bad request"
        })
    response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    return response


@bp.app_errorhandler(KeyError)
def key_error(e):
    logger.exception(e)
    response = jsonify(
        {
            "status": HTTPStatus.INTERNAL_SERVER_ERROR,
            "msg": "Internal error! Field not found: {}".format(e)
        })
    response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    return response


@bp.app_errorhandler(NameError)
def name_error(e):
    logger.exception(e)
    response = jsonify(
        {
            "status": HTTPStatus.INTERNAL_SERVER_ERROR,
            "msg": e.args[0]
        })
    response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    return response


@bp.app_errorhandler(Exception)
def exception(e):
    logger.exception(e)
    response = jsonify(
        {
            "status": HTTPStatus.INTERNAL_SERVER_ERROR,
            "msg": "Unexpected error"
        })
    response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    return response


@jwt.invalid_token_loader
def expired_token_callbacks(c):
    return jsonify({
        'status': 422,
        'msg': f'Unidentified Token'
    }), 422


@jwt.unauthorized_loader
def expired_token_callback(c):
    return jsonify({
        'status': 401,
        'msg': f'Token não enviado'
    }), 401
