from flask import Blueprint

from config import Config

bp = Blueprint("group", __name__,
               url_prefix=f'/{Config.API_VERSION}/admin/groups')
from . import views


def init_app(app):
    app.register_blueprint(bp)
