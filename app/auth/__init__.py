from flask import Blueprint

bp = Blueprint('auth', __name__, url_prefix="/auth")
from . import views


def init_app(app):
    app.register_blueprint(bp)
