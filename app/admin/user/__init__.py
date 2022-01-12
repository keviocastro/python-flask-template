from flask import Blueprint

from config import Config

bp = Blueprint("user_bp", __name__,
               url_prefix=f"/{Config.API_VERSION}/admin/users")
from . import views


def init_app(app):
    app.register_blueprint(bp)
