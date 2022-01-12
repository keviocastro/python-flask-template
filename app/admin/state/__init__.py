from flask import Blueprint

from config import Config

bp = Blueprint('state', __name__,
               url_prefix=f"/{Config.API_VERSION}/admin/states")
from . import views


def init_app(app):
    app.register_blueprint(bp)
