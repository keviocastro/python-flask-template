from flask import Blueprint

bp = Blueprint('exception_handler_bp', __name__)
from . import exceptions


def init_app(app):
    app.register_blueprint(bp)
