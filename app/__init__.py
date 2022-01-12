from flask import Flask

from app.services.extensions import migrate, jwt, ma, cache
from app.services.sqlalchemy.route import db


def create_app():
    """create and configure the flask application"""
    # app
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # extension
    cache.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)
    ma.init_app(app)

    # exceptions
    from app.services import errors
    errors.init_app(app)

    # auth
    from app import auth
    auth.init_app(app)

    # admin
    from app.admin import group
    group.init_app(app)
    from app.admin import user
    user.init_app(app)
    from app.admin import country
    country.init_app(app)
    from app.admin import state
    state.init_app(app)
    from app.admin import city
    city.init_app(app)

    # client
    from app import client
    client.init_app(app)

    return app
