from flask import Blueprint

from config import Config

bp = Blueprint('city', __name__,
               url_prefix=f"/{Config.API_VERSION}/admin/cities")
from . import views


def init_app(app):
    app.register_blueprint(bp)
